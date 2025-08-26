import React, { useState } from 'react';
import authService from '../services/authService';
import Alert from '../components/Alert';

const ForgotPasswordPage = () => {
  const [username, setUsername] = useState('');
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus(null);
    setLoading(true);
    try {
      await authService.forgot(username);
      setStatus({ type: 'success', message: 'If the user exists a reset token has been generated (check backend logs / future email).' });
    } catch (err) {
      setStatus({ type: 'error', message: err.message || 'Request failed' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-split">
      <div className="auth-hero">
        <h1>VaultUpload</h1>
        <p>Securely upload, share, and retrieve files with confidence.<br/>Built-in scanning & expiring links.</p>
      </div>
      <div className="container auth-card auth-form-panel">
        <h2>Forgot Password</h2>
        {status && <Alert type={status.type} message={status.message} />}
        <form onSubmit={handleSubmit} className="vertical-form">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={e => setUsername(e.target.value)}
            required
          />
          <button type="submit" disabled={loading}>{loading ? 'Sending...' : 'Send Reset Link'}</button>
        </form>
        <p style={{marginTop:'1rem', fontSize:'0.75rem', textAlign:'center'}}>Demo: reset token is logged server-side (email optional).</p>
      </div>
    </div>
  );
};

export default ForgotPasswordPage;
