import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import authService from '../services/authService';
import Alert from '../components/Alert';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [hcaptchaToken, setHcaptchaToken] = useState('');
  const siteKey = import.meta.env.VITE_HCAPTCHA_SITE_KEY; // define in .env e.g. VITE_HCAPTCHA_SITE_KEY=your_site_key
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (siteKey && !hcaptchaToken) {
      setError('Please complete captcha');
      return;
    }
    try {
      await authService.login(username, password, hcaptchaToken);
      navigate('/files');
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  // Load hCaptcha script once if site key present
  useEffect(() => {
    if (!siteKey) return;
    if (document.querySelector('script[data-hcaptcha]')) return; // already added
    const script = document.createElement('script');
    script.src = 'https://hcaptcha.com/1/api.js';
    script.async = true;
    script.defer = true;
    script.setAttribute('data-hcaptcha', 'true');
    document.head.appendChild(script);
    // Global callback referenced by data-callback attribute
    window.onHCaptchaSuccess = (token) => setHcaptchaToken(token);
    return () => { delete window.onHCaptchaSuccess; };
  }, [siteKey]);

  return (
  <div className="auth-split">
    <div className="auth-hero">
      <h1>VaultUpload</h1>
      <p>Securely upload, share, and retrieve files with confidence.<br/>Built-in scanning & expiring links.</p>
    </div>
    <div className="container auth-card auth-form-panel">
      <h2>Login</h2>
      {error && <Alert type="error" message={error} />}
  <form onSubmit={handleSubmit} className="vertical-form">
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />
        {siteKey && (
          <div style={{marginTop:'0.25rem'}}>
            <div className="h-captcha" data-sitekey={siteKey} data-callback="onHCaptchaSuccess"></div>
          </div>
        )}
        <button type="submit">Login</button>
  <div className="center-links" style={{marginTop:'0.5rem', fontSize:'0.8rem'}}>
          <Link to="/register">Create account</Link> · <Link to="/forgot">Forgot password?</Link>
        </div>
      </form>
    </div>
  </div>
  );
};

export default LoginPage;
