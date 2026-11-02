
import { useEffect, useState } from 'react'

function MyLoans() {
    const [loans, setLoans] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    const memberId = 'M002'

    useEffect(() => {
        async function fetchLoans() {
            try {
                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/members/${memberId}/loans`
                )

                if (!response.ok) {
                    throw new Error('Unable to load your loans.')
                }

                const data = await response.json()
                setLoans(data)
            } catch (err) {
                setError(err.message)
            } finally {
                setLoading(false)
            }
        }

        fetchLoans()
    }, [])

    if (loading) {
        return <main className="catalogue"><p>Loading your loans...</p></main>
    }

    if (error) {
        return <main className="catalogue"><p>{error}</p></main>
    }

    return (
        <main className="catalogue my-loans-page">
            <header className="page-header">
                <h1>My Loans</h1>
                <p>Your borrowing record</p>
                <div className="header-divider"></div>
            </header>

            <section className="member-summary">
                <h2>{loans.member}</h2>

                <div className="member-info">
                    <p><strong>Membership:</strong> {loans.membership_type}</p>
                    <p><strong>Maximum items:</strong> {loans.max_items}</p>
                    <p><strong>Unpaid fines:</strong> ₹{loans.unpaid_fines}</p>
                </div>
            </section>

            <section className="loans-section">
                <h2>Active Loans</h2>

                {loans.active.length === 0 ? (
                    <p className="empty-loans">You have no active loans.</p>
                ) : (
                    <div className="loans-list">
                        {loans.active.map((loan) => (
                            <article className="loan-card" key={loan.loan_id}>
                                <h3>{loan.title}</h3>
                                <p><strong>Loan ID:</strong> {loan.loan_id}</p>
                                <p><strong>Due date:</strong> {loan.due_date}</p>

                                {loan.days_overdue > 0 ? (
                                    <p className="overdue-text">
                                        {loan.days_overdue} days overdue
                                    </p>
                                ) : (
                                    <p className="on-time-text">Not overdue</p>
                                )}
                            </article>
                        ))}
                    </div>
                )}
            </section>
        </main>
    )
}

export default MyLoans
