import { Link } from 'react-router-dom'
import AvailabilityBadge from './AvailabilityBadge'
import BookActions from './BookActions'

function BookCard({ book }) {
    return (
        <div className="book-card">
            <h3>
                <Link to={`/books/${book.isbn}`}>{book.title}</Link>
            </h3>

            <p>Authors: {book.authors.join(', ')}</p>
            <p>Category: {book.category}</p>
            <p>Pages: {book.pages}</p>
            <p>Price: ₹{book.price}</p>
            <p>Available: {book.available} / {book.total}</p>

            <AvailabilityBadge available={book.available} />

            <BookActions book={book} />
        </div>
    )
}

export default BookCard
