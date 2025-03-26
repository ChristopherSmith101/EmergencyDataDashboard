import React from "react";
import { Link } from "react-router-dom";
import "./Navbar.css"; // For styling

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          📊 Data Dashboard
        </Link>
        <ul className="nav-menu">
          <li className="nav-item">
            <Link to="/" className="nav-link">Home</Link>
          </li>
          <li className="nav-item">
            <Link to="/whatsapp" className="nav-link">WhatsApp Numbers</Link>
          </li>
          <li className="nav-item">
            <Link to="/map" className="nav-link">Map</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
