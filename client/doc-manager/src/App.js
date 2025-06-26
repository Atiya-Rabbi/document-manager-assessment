import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import FileVersions from './FileVersions'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import RegisterForm from './components/auth/RegisterForm';
import LoginForm from './components/auth/LoginForm';
import Navbar from './components/auth/Navbar';
import { useEffect, useState } from 'react';
import {AuthProvider} from './context/AuthContext';

function App() {
  // const [isAuthenticated, setIsAuthenticated] = useState(false);

  // useEffect(() => {
  //   const token = localStorage.getItem('token');
  //   setIsAuthenticated(!!token);
    
  //   const handleStorageChange = () => {
  //     setIsAuthenticated(!!localStorage.getItem('token'));
  //   };
    
  //   window.addEventListener('storage', handleStorageChange);
  //   return () => window.removeEventListener('storage', handleStorageChange);
  // }, []);
  return (
    <AuthProvider>
    <Router>
      <Navbar />
      <div className="container mt-4">
        <Routes>
          <Route path="/login" element={<LoginForm /> } />
          <Route path="/register" element={<RegisterForm /> } />
          <Route path="/files" element={<FileVersions /> } />
          <Route path="/" element={<Navigate to={"/login"} />} />
        </Routes>
      </div>
    </Router>
    </AuthProvider>
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
