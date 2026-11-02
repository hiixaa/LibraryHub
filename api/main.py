
from datetime import date
import os
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from library import Library
from items import Book, Magazine, ReferenceItem


app = FastAPI(title="LibraryHub API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

library = Library()
library.load_data()


# --------------------------------------------------
# DATE HANDLING
# --------------------------------------------------

def get_today():
    today_value = os.getenv("TODAY")
    return date.fromisoformat(today_value) if today_value else date.today()


# --------------------------------------------------
# REQUEST MODELS
# --------------------------------------------------

class LoanRequest(BaseModel):
    member_id: str
    isbn: str


class ItemRequest(BaseModel):
    isbn: str
    title: str
    authors: list[str]
    category: str
    item_type: Literal["Book", "Magazine", "Reference"]
    pages: int = 0
    price: float
    total_copies: int


# --------------------------------------------------
# ERROR HANDLING
# --------------------------------------------------

def raise_api_error(error):
    message = str(error)
    error_name = type(error).__name__

    if error_name in ("MemberNotFoundError", "ItemNotFoundError"):
        status_code = 404
    elif error_name == "InvalidISBNError":
        status_code = 422
    else:
        status_code = 409

    raise HTTPException(
        status_code=status_code,
        detail={
            "error": error_name,
            "message": message,
        },
    )


# --------------------------------------------------
# ROOT
# --------------------------------------------------

@app.get("/")
def root():
    return {"message": "Welcome to LibraryHub API"}


# --------------------------------------------------
# GET ALL BOOKS
# --------------------------------------------------

@app.get("/books")
def get_books(
    q: str = Query(default=""),
    sort: str = Query(default="title"),
):
    books = []

    for item in library.items.values():
        books.append({
            "isbn": item.isbn,
            "title": item.title,
            "authors": item.authors,
            "category": item.category,
            "item_type": type(item).__name__,
            "available": item.available_copies,
            "total": item.total_copies,
            "pages": item.pages,
            "price": item.price,
        })

    search = q.strip().lower()

    if search:
        books = [
            book for book in books
            if search in book["title"].lower()
            or any(
                search in author.lower()
                for author in book["authors"]
            )
        ]

    if sort == "title":
        books.sort(key=lambda book: book["title"].lower())
    elif sort == "category":
        books.sort(key=lambda book: book["category"].lower())

    return books


# --------------------------------------------------
# GET BOOK BY ISBN
# --------------------------------------------------

@app.get("/books/{isbn}")
def get_book(isbn: str):
    try:
        item = library.get_item(isbn)
    except Exception as error:
        raise_api_error(error)

    return {
        "isbn": item.isbn,
        "title": item.title,
        "authors": item.authors,
        "category": item.category,
        "item_type": type(item).__name__,
        "available": item.available_copies,
        "total": item.total_copies,
        "pages": item.pages,
        "price": item.price,
    }


# --------------------------------------------------
# ADD NEW ITEM
# --------------------------------------------------

@app.post("/items", status_code=201)
def create_item(request: ItemRequest):

    item_classes = {
        "Book": Book,
        "Magazine": Magazine,
        "Reference": ReferenceItem,
    }

    try:
        item_class = item_classes[request.item_type]

        item = item_class(
            request.isbn,
            request.title,
            request.authors,
            request.category,
            request.pages if request.pages > 0 else None,
            request.price,
            request.total_copies,
        )

        library.add_item(item)

        return {
            "message": "Item added successfully.",
            "isbn": item.isbn,
            "title": item.title,
        }

    except Exception as error:
        raise_api_error(error)


# --------------------------------------------------
# CREATE LOAN
# --------------------------------------------------

@app.post("/loans", status_code=201)
def create_loan(request: LoanRequest):
    try:
        loan = library.borrow(
            request.isbn,
            request.member_id,
            get_today(),
        )

        return {
            "loan_id": loan.loan_id,
            "due_date": loan.due_date.isoformat(),
        }

    except Exception as error:
        raise_api_error(error)


# --------------------------------------------------
# RETURN LOAN
# --------------------------------------------------

@app.post("/loans/{loan_id}/return")
def return_loan(loan_id: str):

    loan = next(
        (
            loan
            for loan in library.loans
            if loan.loan_id == loan_id
        ),
        None,
    )

    if loan is None or loan.is_returned:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "LoanNotFoundError",
                "message": f"No active loan found with ID {loan_id}.",
            },
        )

    try:
        today = get_today()
        fine_amount = loan.calculate_fine(today)
        days_late = max(0, (today - loan.due_date).days)

        returned_loan = library.return_item(
            loan.item.isbn,
            loan.member.member_id,
            today,
        )

        return {
            "loan_id": returned_loan.loan_id,
            "days_late": days_late,
            "fine": fine_amount,
            "next_in_waiting_list": (
                library.last_notified_member.name
                if library.last_notified_member
                else None
            ),
        }

    except Exception as error:
        raise_api_error(error)


# --------------------------------------------------
# GET ALL MEMBERS
# --------------------------------------------------

@app.get("/members")
def get_members():

    return [
        {
            "member_id": member.member_id,
            "name": member.name,
            "membership_type": type(member).__name__,
            "max_items": member.max_items,
            "unpaid_fines": member.unpaid_fines,
        }
        for member in library.members.values()
    ]


# --------------------------------------------------
# GET MEMBER LOANS
# --------------------------------------------------

@app.get("/members/{member_id}/loans")
def get_member_loans(member_id: str):

    try:
        member = library.get_member(member_id)
    except Exception as error:
        raise_api_error(error)

    active_loans = [
        loan
        for loan in library.loans
        if (
            loan.member.member_id == member_id
            and not loan.is_returned
        )
    ]

    return {
        "member": member.name,
        "membership_type": type(member).__name__,
        "max_items": member.max_items,
        "unpaid_fines": member.unpaid_fines,
        "active": [
            {
                "loan_id": loan.loan_id,
                "title": loan.item.title,
                "due_date": loan.due_date.isoformat(),
                "days_overdue": max(
                    0,
                    (get_today() - loan.due_date).days,
                ),
            }
            for loan in active_loans
        ],
    }
