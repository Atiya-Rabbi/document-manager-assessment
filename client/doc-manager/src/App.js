import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import FileVersions from './FileVersions'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import RegisterForm from './components/auth/RegisterForm';
import LoginForm from './components/auth/LoginForm';
import Navbar from './components/auth/Navbar';
import { useEffect, useState } from 'react';


function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
    
    const handleStorageChange = () => {
      setIsAuthenticated(!!localStorage.getItem('token'));
    };
    
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);
  return (
    <Router>
      <Navbar />
      <div className="container mt-4">
        <Routes>
          <Route path="/login" element={!isAuthenticated ? <LoginForm /> : <Navigate to="/files" />} />
          <Route path="/register" element={!isAuthenticated ? <RegisterForm /> : <Navigate to="/files" />} />
          <Route path="/files" element={isAuthenticated ? <FileVersions /> : <Navigate to="/login" />} />
          <Route path="/" element={<Navigate to={isAuthenticated ? "/files" : "/login"} />} />
        </Routes>
      </div>
    </Router>
  );
}
  
//   return (
//     <AuthProvider>
//       <Router>
//         <div className="App">
//           {/* <Navbar /> */}
//           <div className="container mt-4">
//             <Routes>
//               {/* Public Routes */}
//               <Route path="/register" element={<RegisterForm />} />
//               <Route 
//                 path="/files" 
//                 element={
//                   <ProtectedRoute>
//                     <FileVersions />
//                   </ProtectedRoute>
//                 } 
//               />
//               </Routes>
//             </div>
//           </div>
//         </Router>
//       </AuthProvider>
//   );
// }

// // Protected Route Component
// const ProtectedRoute = ({ children }) => {
//   const { isAuthenticated } = useAuth();
//   return isAuthenticated ? children : <Navigate to="/login" />;
// };

export default App;
