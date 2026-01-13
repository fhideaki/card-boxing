import { Link } from "react-router-dom";

export default function Navbar() {
    return (
        <nav className="navbar-container">
            <div className="logo">
                <Link to="/">Robot Card Boxing</Link>
            </div>

            <ul className="nav-links">
                <li><Link to="/cards">Cartas</Link></li>
                <li><Link to="/parts">Partes</Link></li>
                <li><Link to="/robots">Meus Robôs</Link></li>
                <li><Link to="/login">Login</Link></li>
            </ul>
        </nav>
    )
}