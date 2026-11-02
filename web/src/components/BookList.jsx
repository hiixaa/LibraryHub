
import BookCard from './BookCard'

function BookList({ books }) {
    if (books.length === 0) {
        return null
    }

    return (
        <div className="book-list">
            {books.map((book) => (
                <BookCard key={book.isbn} book={book} />
            ))}
        </div>
    )
}

export default BookList
