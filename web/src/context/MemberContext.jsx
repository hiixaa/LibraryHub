
import { createContext, useContext, useEffect, useState } from 'react'

const MemberContext = createContext()

export function MemberProvider({ children }) {
    const [memberId, setMemberId] = useState('M002')
    const [member, setMember] = useState(null)
    const [loadingMember, setLoadingMember] = useState(true)

    useEffect(() => {
        async function fetchMember() {
            try {
                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/members/${memberId}/loans`
                )

                if (!response.ok) {
                    throw new Error('Unable to load member details')
                }

                const data = await response.json()
                setMember(data)
            } catch (error) {
                console.error(error)
                setMember(null)
            } finally {
                setLoadingMember(false)
            }
        }

        fetchMember()
    }, [memberId])

    return (
        <MemberContext.Provider
            value={{ memberId, setMemberId, member, loadingMember }}
        >
            {children}
        </MemberContext.Provider>
    )
}

export function useMember() {
    return useContext(MemberContext)
}
