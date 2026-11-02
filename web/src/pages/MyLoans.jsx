
import { useMember } from '../context/MemberContext'

function MyLoans() {
    const {
        members,
        memberId,
        setMemberId,
        member,
        loadingMembers,
        loadingMember
    } = useMember()

    if (loadingMembers) {
        return (
            <main className="catalogue">
                <p>Loading members...</p>
            </main>
        )
    }

    if (members.length === 0) {
        return (
            <main className="catalogue">
                <p>Unable to load library members.</p>
            </main>
        )
    }

    return (
        <main className="catalogue my-loans-page">
            <header className="page-header">
                <h1>My Loans</h1>
                <p>Your borrowing record</p>
                <div className="header-divider"></div>
            </header>

            {/* MEMBER SELECTION */}
            <section className="member-summary">
                <label htmlFor="member-select">
                    Select Member
                </label>

                <select
                    id="member-select"
                    value={memberId}
                    onChange={(e) => setMemberId(e.target.value)}
                >
                    {members.map((item) => (
                        <option
                            key={item.member_id}
                            value={item.member_id}
                        >
                            {item.name} ({item.member_id})
                        </option>
                    ))}
                </select>

                {loadingMember ? (
                    <p>Loading member details...</p>
                ) : !member ? (
                    <p>Unable to load this member's details.</p>
                ) : (
                    <>
                        <h2>{member.member}</h2>

                        <div className="member-info">
                            <p>
                                <strong>Membership:</strong>{' '}
                                {member.membership_type}
                            </p>

                            <p>
                                <strong>Maximum items:</strong>{' '}
                                {member.max_items}
                            </p>

                            <p>
                                <strong>Unpaid fines:</strong>{' '}
                                ₹{member.unpaid_fines}
                            </p>
                        </div>

                        <section className="loans-section">
                            <h2>Active Loans</h2>

                            {member.active.length === 0 ? (
                                <p className="empty-loans">
                                    You have no active loans.
                                </p>
                            ) : (
                                <div className="loans-list">
                                    {member.active.map((loan) => (
                                        <article
                                            className="loan-card"
                                            key={loan.loan_id}
                                        >
                                            <h3>{loan.title}</h3>

                                            <p>
                                                <strong>Loan ID:</strong>{' '}
                                                {loan.loan_id}
                                            </p>

                                            <p>
                                                <strong>Due date:</strong>{' '}
                                                {loan.due_date}
                                            </p>

                                            {loan.days_overdue > 0 ? (
                                                <p className="overdue-text">
                                                    {loan.days_overdue} days overdue
                                                </p>
                                            ) : (
                                                <p className="on-time-text">
                                                    Not overdue
                                                </p>
                                            )}
                                        </article>
                                    ))}
                                </div>
                            )}
                        </section>
                    </>
                )}
            </section>
        </main>
    )
}

export default MyLoans
