import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import LoginPage from './pages/LoginPage';
import UploadPage from './pages/UploadPage';
import FilesPage from './pages/FilesPage';
import ReceivePage from './pages/ReceivePage';
import NotFoundPage from './pages/NotFoundPage';
import authService from './services/authService';

const PrivateRoute = ({ children }) => {
  return authService.isAuthenticated() ? children : <Navigate to="/login" />;
};

const App = () => (
  <Router>
    <Navbar />
    <div className="main-content">
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/upload" element={<PrivateRoute><UploadPage /></PrivateRoute>} />
          <Route path="/files" element={<PrivateRoute><FilesPage /></PrivateRoute>} />
          <Route path="/receive" element={<ReceivePage />} />
        <Route path="/" element={<Navigate to="/files" />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </div>
  </Router>
);

export default App;