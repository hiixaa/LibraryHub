
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useBasket } from '../context/BasketContext'
import { useMember } from '../context/MemberContext'

function Basket() {
    const { state, dispatch } = useBasket()
    const { memberId } = useMember()

    const [checkingOut, setCheckingOut] = useState(false)
    const [results, setResults] = useState([])

    const basketItems = state.items

    async function handleCheckout() {
        setCheckingOut(true)
        setResults([])

        const checkoutResults = []

        for (const book of basketItems) {
            try {
                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/loans`,
                    {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            member_id: memberId,
                            isbn: book.isbn,
                        }),
                    }
                )

                const data = await response.json()

                if (!response.ok) {
                    throw new Error(
                        data.message ||
                        data.detail?.message ||
                        'Unable to borrow this book.'
                    )
                }

                checkoutResults.push({
                    title: book.title,
                    success: true,
                    loanId: data.loan_id,
                    dueDate: data.due_date,
                })

                dispatch({
                    type: 'REMOVE_ITEM',
                    payload: book.isbn,
                })
            } catch (error) {
                checkoutResults.push({
                    title: book.title,
                    success: false,
                    message: error.message,
                })
            }
        }

        setResults(checkoutResults)
        setCheckingOut(false)
    }

    return (
        <main className="catalogue basket-page">
            <header className="page-header">
                <h1>Borrow Basket</h1>
                <p>Your selected books</p>
                <div className="header-divider"></div>
            </header>

            {basketItems.length === 0 && (
                <section className="empty-basket">
                    <h2>Your basket is currently empty.</h2>
                    <p>Find something interesting to read in our catalogue.</p>
                    <Link to="/" className="basket-browse-link">
                        Browse Catalogue
                    </Link>
                </section>
            )}

            {basketItems.length > 0 && (
                <section className="basket-section">
                    <div className="basket-list">
                        {basketItems.map((book) => (
                            <article className="basket-card" key={book.isbn}>
                                <div>
                                    <h3>{book.title}</h3>
                                    <p>ISBN: {book.isbn}</p>
                                    <p>Price: ₹{book.price}</p>
                                </div>

                                <button
                                    className="remove-button"
                                    disabled={checkingOut}
                                    onClick={() => {
                                        dispatch({
                                            type: 'REMOVE_ITEM',
                                            payload: book.isbn,
                                        })
                                    }}
                                >
                                    Remove
                                </button>
                            </article>
                        ))}
                    </div>

                    <div className="basket-summary">
                        <p>Total items: {basketItems.length}</p>

                        <button
                            className="checkout-button"
                            onClick={handleCheckout}
                            disabled={checkingOut}
                        >
                            {checkingOut ? 'Processing...' : 'Checkout'}
                        </button>
                    </div>
                </section>
            )}

            {results.length > 0 && (
                <section className="checkout-results">
                    <h2>Checkout Results</h2>

                    {results.map((result, index) => (
                        <article className="checkout-result-card" key={index}>
                            <h3>{result.title}</h3>

                            {result.success ? (
                                <>
                                    <p className="checkout-success">
                                        Borrowed successfully!
                                    </p>
                                    <p>Loan ID: {result.loanId}</p>
                                    <p>Due date: {result.dueDate}</p>
                                </>
                            ) : (
                                <p className="error-message">
                                    Failed: {result.message}
                                </p>
                            )}
                        </article>
                    ))}
                </section>
            )}
        </main>
    )
}

export default Basket
