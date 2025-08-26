import React, { useState, useEffect } from 'react';
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
  const [autoTried, setAutoTried] = useState(false);
  const [downloading, setDownloading] = useState(false);

  const handleAccess = async (e) => {
    if(e) e.preventDefault();
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

  // Auto-attempt if token & fileId present and no secret word yet (optimistic) only once
  useEffect(()=>{
    if(!autoTried && fileId && token && !secretWord){
      setAutoTried(true);
      handleAccess();
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [fileId, token]);

  return (
    <div className="container wide receive-dashboard">
      <div className="page-header">
        <div>
          <h2>Receive File</h2>
          <p className="muted">Provide the File ID, Share Token and Secret (if required) to securely download.</p>
        </div>
      </div>
      <div className="panel surface">
        {status && <Alert type={status.type} message={status.message} />}
        <form onSubmit={handleAccess} className="receive-form-grid">
          <div className="form-row">
            <label className="form-label">File ID</label>
            <input className="control" type="text" value={fileId} onChange={(e) => setFileId(e.target.value.trim())} required placeholder="uuid_filename" />
          </div>
          <div className="form-row">
            <label className="form-label">Share Token</label>
              <input className="control" type="text" value={token} onChange={(e) => setToken(e.target.value.trim())} required placeholder="Paste token" />
          </div>
          <div className="form-row">
            <label className="form-label">Secret Word</label>
            <input className="control" type="password" value={secretWord} onChange={(e) => setSecretWord(e.target.value)} placeholder="Secret (if required)" />
          </div>
          <div className="actions">
            <button type="submit" className="primary" disabled={downloading}>{downloading ? 'Downloading...' : 'Access File'}</button>
          </div>
        </form>
        <div className="meta-note">If you used a full share link, fields are pre-filled automatically.</div>
      </div>
    </div>
  );
};

export default ReceivePage;
