import { Link, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';

const Navbar = () => {
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Sync auth state with localStorage
  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
  }, []);

  const handleLogout = (e) => {
    e.preventDefault();
    
    // Clear auth data
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    
    // Navigate to login with replace to prevent back navigation
    navigate('/login', { replace: true });
    
    // Optional: Reset any other application state here
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        <Link className="navbar-brand" to="/">File Manager</Link>
        
        <div className="navbar-nav">
          {isLoggedIn ? (
            <>
              <Link className="nav-link" to="/files">Files</Link>
              <button 
                className="nav-link btn btn-link" 
                onClick={handleLogout}
                style={{ 
                  border: 'none', 
                  background: 'transparent', 
                  cursor: 'pointer',
                  color: 'rgba(255, 255, 255, 0.55)' // Match nav-link color
                }}
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link className="nav-link" to="/login">Login</Link>
              <Link className="nav-link" to="/register">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;