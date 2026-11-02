
import { createContext, useContext, useReducer } from 'react'

const BasketContext = createContext()

const initialState = {
    items: [],
}

function basketReducer(state, action) {
    switch (action.type) {
        case 'ADD_ITEM':
            return {
                ...state,
                items: [...state.items, action.payload],
            }

        case 'REMOVE_ITEM':
            return {
                ...state,
                items: state.items.filter(
                    (item) => item.isbn !== action.payload
                ),
            }

        case 'CLEAR_BASKET':
            return initialState

        default:
            return state
    }
}

export function BasketProvider({ children }) {
    const [state, dispatch] = useReducer(
        basketReducer,
        initialState
    )

    return (
        <BasketContext.Provider value={{ state, dispatch }}>
            {children}
        </BasketContext.Provider>
    )
}

export function useBasket() {
    return useContext(BasketContext)
}
