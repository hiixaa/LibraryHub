
import { useBasket } from '../context/BasketContext'
import { useMember } from '../context/MemberContext'

function BookActions({ book }) {
    const { state, dispatch } = useBasket()
    const { member, loadingMember } = useMember()

    const alreadyAdded = state.items.some(
        (item) => item.isbn === book.isbn
    )

    if (book.item_type === 'ReferenceItem') {
        return (
            <p className="reference-message">
                Reference item: read in the library only
            </p>
        )
    }

    if (book.available === 0) {
        return (
            <button className="waiting-button" disabled>
                Join waiting list
            </button>
        )
    }

    if (loadingMember) {
        return <button disabled>Loading member...</button>
    }

    if (!member) {
        return <button disabled>Member details unavailable</button>
    }

    if (alreadyAdded) {
        return (
            <button className="basket-button" disabled>
                Already in basket
            </button>
        )
    }

    const limitReached =
        state.items.length + member.active.length >= member.max_items


    return (
        <button
            className="basket-button"
            disabled={limitReached}
            onClick={() =>
                dispatch({
                    type: 'ADD_ITEM',
                    payload: book,
                })
            }
        >
            {limitReached ? 'Borrow limit reached' : 'Add to basket'}
        </button>
    )
}

export default BookActions
