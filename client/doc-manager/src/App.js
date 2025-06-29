import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import FileVersions from './components/FileVersions';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import RegisterForm from './components/auth/RegisterForm';
import LoginForm from './components/auth/LoginForm';
import Navbar from './components/auth/Navbar';
import { useEffect, useState } from 'react';
import {AuthProvider} from './context/AuthContext';
import FileUpload from './components/FileUpload';
import { useAuth } from './context/AuthContext';
import FileViewer from './components/FileViewer';

function App() {
  function ProtectedRoute({ children }) {
  const { user } = useAuth();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
  return (
    <AuthProvider>
    <Router>
      <Navbar />
      <div className="container mt-4">
        <Routes>
          <Route path="/login" element={<LoginForm /> } />
          <Route path="/register" element={<RegisterForm /> } />
          <Route path="/files" element={ <ProtectedRoute><FileVersions /></ProtectedRoute> } />
          <Route path="/fileupload" element={<ProtectedRoute><FileUpload /></ProtectedRoute> } />
          <Route path="/*" element={<ProtectedRoute> <FileViewer /> </ProtectedRoute>}/>
        </Routes>
      </div>
    </Router>
    </AuthProvider>
  );
}
  export default App;
