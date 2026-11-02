
import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import AvailabilityBadge from '../components/AvailabilityBadge'
import BookActions from '../components/BookActions'

function BookDetails() {
    const { isbn } = useParams()

    const [book, setBook] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    useEffect(() => {
        async function fetchBook() {
            try {
                setLoading(true)
                setError('')

                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/books/${isbn}`
                )

                if (!response.ok) {
                    throw new Error('Book not found')
                }

                const data = await response.json()
                setBook(data)
            } catch (err) {
                setError(err.message)
            } finally {
                setLoading(false)
            }
        }

        fetchBook()
    }, [isbn])

    if (loading) {
        return <main className="catalogue"><p>Loading book details...</p></main>
    }

    if (error) {
        return (
            <main className="catalogue">
                <p>{error}</p>
                <Link to="/">Back to catalogue</Link>
            </main>
        )
    }

    return (
        <main className="catalogue book-details">
            <Link className="back-link" to="/">
                ← Back to catalogue
            </Link>

            <section className="book-details-card">
                <h1>{book.title}</h1>

                <p className="book-detail-author">
                    By {book.authors.join(', ')}
                </p>

                <div className="book-detail-divider"></div>

                <p><strong>ISBN:</strong> {book.isbn}</p>
                <p><strong>Category:</strong> {book.category}</p>
                <p><strong>Type:</strong> {book.item_type}</p>
                <p><strong>Pages:</strong> {book.pages ?? 'N/A'}</p>
                <p><strong>Price:</strong> ₹{book.price}</p>
                <p>
                    <strong>Available copies:</strong>{' '}
                    {book.available} / {book.total}
                </p>

                <AvailabilityBadge available={book.available} />

                <div className="book-detail-actions">
                    <BookActions book={book} />
                </div>
            </section>
        </main>
    )
}

export default BookDetails
