import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import authService from '../services/authService';

const Navbar = () => {
  const navigate = useNavigate();
  const isLoggedIn = authService.isAuthenticated();

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <Link to="/files">VaultUpload</Link>
        {isLoggedIn ? (
          <>
            <Link to="/upload">Upload</Link>
            <Link to="/receive">Receive</Link>
            <button onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/receive">Receive</Link>
            <Link to="/login">Login</Link>
          </>
        )}
    </nav>
  );
};

export default Navbar;
