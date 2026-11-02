
import {
    createContext,
    useContext,
    useEffect,
    useState
} from 'react'

const MemberContext = createContext()

export function MemberProvider({ children }) {
    const [members, setMembers] = useState([])
    const [memberId, setMemberId] = useState('M002')
    const [member, setMember] = useState(null)

    const [loadingMembers, setLoadingMembers] = useState(true)
    const [loadingMember, setLoadingMember] = useState(true)

    // Fetch all members
    useEffect(() => {
        async function fetchMembers() {
            try {
                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/members`
                )

                if (!response.ok) {
                    throw new Error('Unable to load members')
                }

                const data = await response.json()
                setMembers(data)
            } catch (error) {
                console.error('Members error:', error)
                setMembers([])
            } finally {
                setLoadingMembers(false)
            }
        }

        fetchMembers()
    }, [])

    // Fetch selected member's details and loans
    useEffect(() => {
        async function fetchMember() {
            setLoadingMember(true)

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
                console.error('Member details error:', error)
                setMember(null)
            } finally {
                setLoadingMember(false)
            }
        }

        fetchMember()
    }, [memberId])

    return (
        <MemberContext.Provider
            value={{
                members,
                memberId,
                setMemberId,
                member,
                loadingMembers,
                loadingMember
            }}
        >
            {children}
        </MemberContext.Provider>
    )
}

export function useMember() {
    return useContext(MemberContext)
}
