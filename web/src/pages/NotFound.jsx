
import { Link } from 'react-router-dom'

function NotFound() {
    return (
        <main className="catalogue">
            <h1>404 - Page Not Found</h1>

            <p>Sorry, the page you are looking for does not exist.</p>

            <Link to="/">Go back to LibraryHub</Link>
        </main>
    )
}

export default NotFound
