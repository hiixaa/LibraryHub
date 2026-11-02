
import { Link } from 'react-router-dom'

function Navbar() {
    return (
        <nav className="navbar">
            <h2>LibraryHub</h2>

            <div className="nav-links">
                <Link to="/">Catalogue</Link>
                <Link to="/me">My Loans</Link>
                <Link to="/basket">Borrow Basket</Link>
            </div>
        </nav>
    )
}

export default Navbar
