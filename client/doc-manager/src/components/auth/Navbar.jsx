import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Navbar = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = (e) => {
    e.preventDefault();
    logout();
    navigate('/login', { replace: true });
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        <Link className="navbar-brand" to="/">File Manager</Link>
        
        <div className="navbar-nav">
          {user ? (
            <>
              <Link className="nav-link" to="/files">Files</Link>
              <button 
                className="nav-link btn btn-link" 
                onClick={handleLogout}
                style={{ 
                  border: 'none', 
                  background: 'transparent', 
                  cursor: 'pointer',
                  color: 'rgba(255, 255, 255, 0.55)'
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