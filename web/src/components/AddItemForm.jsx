
import { useState } from 'react'

function AddItemForm({ onAdd }) {
    const [form, setForm] = useState({
        isbn: '',
        title: '',
        authors: '',
        category: '',
        item_type: 'Book',
        pages: '',
        price: '',
        total_copies: '1',
    })

    const [errors, setErrors] = useState({})

    function validate() {
        const newErrors = {}

        if (!/^\d{13}$/.test(form.isbn)) {
            newErrors.isbn = 'ISBN must be exactly 13 digits.'
        }

        if (!form.title.trim()) {
            newErrors.title = 'Title is required.'
        }

        if (!Number.isInteger(Number(form.total_copies)) ||
            Number(form.total_copies) < 1) {
            newErrors.total_copies = 'Copies must be at least 1.'
        }

        if (!form.category.trim()) {
            newErrors.category = 'Category is required.'
        }

        if (!form.authors.trim()) {
            newErrors.authors = 'Authors are required.'
        }

        if (form.pages && Number(form.pages) < 1) {
            newErrors.pages = 'Pages must be at least 1.'
        }

        if (form.price && Number(form.price) < 0) {
            newErrors.price = 'Price cannot be negative.'
        }

        setErrors(newErrors)
        return Object.keys(newErrors).length === 0
    }

    function handleChange(event) {
        const { name, value } = event.target

        setForm((previous) => ({
            ...previous,
            [name]: value,
        }))

        const newErrors = {}

        if (name === 'isbn' && !/^\d{13}$/.test(value)) {
            newErrors.isbn = 'ISBN must be exactly 13 digits.'
        }

        if (name === 'title' && !value.trim()) {
            newErrors.title = 'Title is required.'
        }

        if (name === 'authors' && !value.trim()) {
            newErrors.authors = 'Authors are required.'
        }

        if (name === 'category' && !value.trim()) {
            newErrors.category = 'Category is required.'
        }

        if (name === 'pages' && value !== '' && Number(value) < 1) {
            newErrors.pages = 'Pages must be greater than or equal to 1.'
        }

        if (name === 'price' && value !== '' && Number(value) < 0) {
            newErrors.price = 'Price must be greater than or equal to 0.'
        }

        if (name === 'total_copies' &&
            (!Number.isInteger(Number(value)) || Number(value) < 1)) {
            newErrors.total_copies = 'Copies must be greater than or equal to 1.'
        }

        setErrors((previous) => ({
            ...previous,
            [name]: newErrors[name] || '',
        }))
    }

    function handleSubmit(event) {
        event.preventDefault()

        if (!validate()) return

        onAdd({
            ...form,
            authors: form.authors.split(',').map((author) => author.trim()),
            pages: Number(form.pages || 0),
            price: Number(form.price || 0),
            total_copies: Number(form.total_copies),
        })
    }

    const isValid =
        /^\d{13}$/.test(form.isbn) &&
        form.title.trim() !== '' &&
        form.authors.trim() !== '' &&
        form.category.trim() !== '' &&
        Number.isInteger(Number(form.total_copies)) &&
        Number(form.total_copies) >= 1 &&
        (!form.pages || Number(form.pages) >= 1) &&
        (!form.price || Number(form.price) >= 0)

    return (
        <form className="add-item-form" onSubmit={handleSubmit}>
            <h2>Add New Library Item</h2>

            <label htmlFor="isbn">ISBN</label>
            <input
                id="isbn"
                name="isbn"
                value={form.isbn}
                onChange={handleChange}
                placeholder="13-digit ISBN"
                aria-invalid={Boolean(errors.isbn)}
            />
            {errors.isbn && <p className="field-error">{errors.isbn}</p>}

            <label htmlFor="title">Title</label>
            <input
                id="title"
                name="title"
                value={form.title}
                onChange={handleChange}
                placeholder="Enter title"
                aria-invalid={Boolean(errors.title)}
            />
            {errors.title && <p className="field-error">{errors.title}</p>}

            <label htmlFor="authors">Authors</label>
            <input
                id="authors"
                name="authors"
                value={form.authors}
                onChange={handleChange}
                placeholder="Separate multiple authors with commas"
                aria-invalid={Boolean(errors.authors)}
            />
            {errors.authors && <p className="field-error">{errors.authors}</p>}

            <label htmlFor="category">Category</label>
            <input
                id="category"
                name="category"
                value={form.category}
                onChange={handleChange}
                placeholder="Enter category"
                aria-invalid={Boolean(errors.category)}
            />
            {errors.category && <p className="field-error">{errors.category}</p>}

            <label htmlFor="item_type">Item Type</label>
            <select
                id="item_type"
                name="item_type"
                value={form.item_type}
                onChange={handleChange}
            >
                <option value="Book">Book</option>
                <option value="Magazine">Magazine</option>
                <option value="Reference">Reference Item</option>
            </select>

            <label htmlFor="pages">Pages</label>
            <input
                id="pages"
                type="number"
                name="pages"
                min="1"
                value={form.pages}
                onChange={handleChange}
                aria-invalid={Boolean(errors.pages)}
            />
            {errors.pages && <p className="field-error">{errors.pages}</p>}

            <label htmlFor="price">Price (₹)</label>
            <input
                id="price"
                type="number"
                name="price"
                min="0"
                value={form.price}
                onChange={handleChange}
                aria-invalid={Boolean(errors.price)}
            />
            {errors.price && <p className="field-error">{errors.price}</p>}

            <label htmlFor="total_copies">Total Copies</label>
            <input
                id="total_copies"
                type="number"
                name="total_copies"
                min="1"
                value={form.total_copies}
                onChange={handleChange}
                aria-invalid={Boolean(errors.total_copies)}
            />
            {errors.total_copies && (
                <p className="field-error">{errors.total_copies}</p>
            )}

            <button type="submit" disabled={!isValid}>
                Add Item
            </button>
        </form>
    )
}

export default AddItemForm
