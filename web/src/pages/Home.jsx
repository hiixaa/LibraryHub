
import { useEffect, useState } from 'react'
import BookList from '../components/BookList'
import AddItemForm from '../components/AddItemForm'

function Home() {
    const [books, setBooks] = useState([])
    const [search, setSearch] = useState('')
    const [debouncedSearch, setDebouncedSearch] = useState('')
    const [category, setCategory] = useState('All')
    const [sort, setSort] = useState('title')

    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [formMessage, setFormMessage] = useState('')

    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedSearch(search)
        }, 350)

        return () => clearTimeout(timer)
    }, [search])

    useEffect(() => {
        const controller = new AbortController()

        async function fetchBooks() {
            setLoading(true)
            setError('')

            try {
                const params = new URLSearchParams()

                if (debouncedSearch.trim()) {
                    params.append('q', debouncedSearch.trim())
                }

                params.append('sort', sort)

                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/books?${params}`,
                    { signal: controller.signal }
                )

                if (!response.ok) {
                    throw new Error('Failed to load books')
                }

                const data = await response.json()
                setBooks(data)
            } catch (err) {
                if (err.name !== 'AbortError') {
                    setError("Can't reach the library server.")
                }
            } finally {
                if (!controller.signal.aborted) {
                    setLoading(false)
                }
            }
        }

        fetchBooks()

        return () => controller.abort()
    }, [debouncedSearch, sort])

    const categories = [
        'All',
        ...new Set(books.map((book) => book.category)),
    ]

    const filteredBooks = category === 'All'
        ? books
        : books.filter((book) => book.category === category)

    async function handleAddItem(item) {
        setFormMessage('')

        try {
            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/items`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(item),
                }
            )

            const data = await response.json()

            if (!response.ok) {
                throw new Error(
                    data.message || data.detail?.message || 'Unable to add item.'
                )
            }

            setFormMessage('Item added successfully!')
            setSearch('')
            setCategory('All')
            setDebouncedSearch('')
        } catch (err) {
            setFormMessage(err.message)
        }
    }

    return (
        <main className="catalogue">
            <header className="catalogue-header">
                <h1>LibraryHub</h1>
                <div className="header-divider" />
            </header>

            <section className="catalogue-section">
                <h2>Browse the Catalogue</h2>

                <div className="filters">
                    <input
                        type="search"
                        aria-label="Search catalogue"
                        placeholder="Search by title, author or ISBN..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />

                    <select
                        aria-label="Filter by category"
                        value={category}
                        onChange={(e) => setCategory(e.target.value)}
                    >
                        {categories.map((item) => (
                            <option key={item} value={item}>
                                {item === 'All' ? 'All Categories' : item}
                            </option>
                        ))}
                    </select>

                    <select
                        aria-label="Sort catalogue"
                        value={sort}
                        onChange={(e) => setSort(e.target.value)}
                    >
                        <option value="title">Sort by Title</option>
                        <option value="category">Sort by Category</option>
                    </select>
                </div>

                {!loading && !error && (
                    <p className="result-count">
                        {filteredBooks.length}{' '}
                        {filteredBooks.length === 1 ? 'result' : 'results'}
                    </p>
                )}

                {loading && (
                    <p className="status-message">Loading catalogue...</p>
                )}

                {error && (
                    <p className="error-message">{error}</p>
                )}

                {!loading && !error && filteredBooks.length === 0 && (
                    <p className="status-message">
                        No items match '{search}'. Try a different word.
                    </p>
                )}

                {!loading && !error && (
                    <BookList books={filteredBooks} />
                )}
            </section>

            <section className="admin-section">
                <AddItemForm onAdd={handleAddItem} />

                {formMessage && (
                    <p className="form-message">{formMessage}</p>
                )}
            </section>
        </main>
    )
}

export default Home
