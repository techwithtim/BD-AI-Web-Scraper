import React from "react";
import logo from "../assets/logo.png";
import "../css/Footer.css";

const Footer = () => {
  return (
    <footer className="footer">
      <div class="column">
        <img src={logo} alt="Logo" className="footer-logo" />
        <div className="social-icons"></div>
      </div>

      <div className="column">
        <p className="subtitle">Links</p>
        <div className="links">
          <a href="#" className="footer-link">
            Terms Of Service
          </a>
          <a href="#" className="footer-link">
            Privacy Policy
          </a>
        </div>
      </div>
      <div className="column">
        <p className="subtitle">Contact</p>
        <a href="mailto:info@scrapegen.com" className="contact">
          info@scrapegen.com
        </a>
      </div>
    </footer>
  );
};

export default Footer;
