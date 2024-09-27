import React from "react";
import "../css/Navbar.css";
import logo from "../assets/logo.png";

const Navbar = ({ credits, isLoggedIn, login, logout }) => {
  if (!credits) credits = 0;

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <img src={logo} alt="Logo" className="navbar-logo" />
      </div>
      <div className="navbar-right">
        {isLoggedIn ? (
          <>
            <span className="navbar-text">Credits: {credits}</span>
            <button className="navbar-button" onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            <span className="navbar-text"></span>
            <button className="navbar-button" onClick={login}>Login</button>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
