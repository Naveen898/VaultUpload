import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import fileService from '../services/fileService';
import Alert from '../components/Alert';

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

const ReceivePage = () => {
  const query = useQuery();
  const [fileId, setFileId] = useState(query.get('fileId') || '');
  const [token, setToken] = useState(query.get('token') || '');
  const [secretWord, setSecretWord] = useState('');
  const [status, setStatus] = useState(null);
  const [downloading, setDownloading] = useState(false);

  const handleAccess = async (e) => {
    e.preventDefault();
    setStatus(null);
    setDownloading(true);
    try {
      const blob = await fileService.accessFile({ fileId, token, secretWord });
      if (!blob || blob.error) {
        setStatus({ type: 'error', message: blob?.error || 'Access failed' });
      } else {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = fileId; // Fallback: we don't have original filename on frontend yet
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        setStatus({ type: 'success', message: 'Download started' });
      }
    } catch (err) {
      setStatus({ type: 'error', message: err.message || 'Access error' });
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="container">
      <h2>Receive a File</h2>
      <p>Enter the File ID, the Share Token you received, and the Secret Word if one was set.</p>
      {status && <Alert type={status.type} message={status.message} />}
      <form onSubmit={handleAccess} style={{maxWidth:'480px'}}>
        <div style={{marginBottom:'0.75rem'}}>
          <label>File ID</label>
          <input
            type="text"
            value={fileId}
            onChange={(e) => setFileId(e.target.value.trim())}
            required
            placeholder="e.g. 3f8d2c..."
          />
        </div>
        <div style={{marginBottom:'0.75rem'}}>
          <label>Share Token (JWT)</label>
          <input
            type="text"
            value={token}
            onChange={(e) => setToken(e.target.value.trim())}
            required
            placeholder="Paste the share token"
          />
        </div>
        <div style={{marginBottom:'0.75rem'}}>
          <label>Secret Word (if required)</label>
          <input
            type="password"
            value={secretWord}
            onChange={(e) => setSecretWord(e.target.value)}
            placeholder="Secret word"
          />
        </div>
        <button type="submit" disabled={downloading}>{downloading ? 'Downloading...' : 'Access File'}</button>
      </form>
      <div style={{marginTop:'1rem'}}>
        <h4>Have a full link?</h4>
        <p>You can paste it in the browser directly. If this page was opened with query parameters, fields are prefilled.</p>
      </div>
    </div>
  );
};

export default ReceivePage;
