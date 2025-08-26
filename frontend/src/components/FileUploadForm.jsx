import React, { useState, useEffect } from 'react';
import fileService from '../services/fileService';
import Alert from './Alert';

const FileUploadForm = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [expiryHours, setExpiryHours] = useState(24);
  const [secretWord, setSecretWord] = useState('');
  const [shareInfo, setShareInfo] = useState(null);
  const [scanning, setScanning] = useState(false);
  const [revealed, setRevealed] = useState(false);

  // Auto-hide share token after first visibility change or navigation
  useEffect(() => {
    const handleVisibility = () => {
      if (document.hidden && shareInfo) {
        // remove token from state when user leaves tab
        setShareInfo(prev => prev ? { ...prev, token: undefined } : prev);
      }
    };
    const handleBeforeUnload = () => {
      if (shareInfo) {
        setShareInfo(prev => prev ? { ...prev, token: undefined } : prev);
      }
    };
    document.addEventListener('visibilitychange', handleVisibility);
    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => {
      document.removeEventListener('visibilitychange', handleVisibility);
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, [shareInfo]);

  const handleChange = (e) => {
    setFile(e.target.files[0]);
    setMessage('');
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }
    try {
      setScanning(true);
      const uploadResp = await fileService.uploadFile(file, { expiryHours, secretWord });
      setMessage('File uploaded successfully');
      // share info now comes embedded (with share_token & receive_link)
      setShareInfo({
        fileId: uploadResp.metadata.file_id,
        token: uploadResp.metadata.share_token,
        expiresAtIST: uploadResp.metadata.expires_at_ist,
        receiveLink: uploadResp.metadata.receive_link,
        requiresSecret: !!uploadResp.metadata.secret_hash
      });
      setFile(null);
    } catch (e) {
      setError('Upload failed: ' + e.message);
    } finally {
      setScanning(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="upload-form">
      {message && <Alert type="success" message={message} />}
      {error && <Alert type="error" message={error} />}
      <div className="form-row">
        <label className="form-label">File</label>
        <input type="file" onChange={handleChange} className="control" />
      </div>
      <div className="form-row inline">
        <div className="field">
          <label className="form-label">Expiry (hrs)</label>
          <input type="number" min={1} max={24} value={expiryHours} onChange={e => setExpiryHours(Number(e.target.value))} className="control small" />
        </div>
        <div className="field">
          <label className="form-label">Secret (optional)</label>
          <input type="text" value={secretWord} onChange={e => setSecretWord(e.target.value)} placeholder="Enter secret" className="control" />
        </div>
      </div>
      <div className="actions"><button type="submit" className="primary">Upload</button></div>
      {shareInfo && (
        <div className="share-panel surface raised">
          <h4>Share Details</h4>
          <div className="kv"><span className="kv-key">File ID</span><code>{shareInfo.fileId}</code></div>
          <div className="kv"><span className="kv-key">Expiry (IST)</span><strong>{shareInfo.expiresAtIST}</strong></div>
          <div className="kv"><span className="kv-key">Requires Secret</span><strong>{shareInfo.requiresSecret ? 'Yes' : 'No'}</strong></div>
          <div className="kv"><span className="kv-key">Receive Link</span><code className="break-all">{shareInfo.receiveLink}</code></div>
          {shareInfo.token && (
            <details className="token-details" open={revealed} onToggle={e => setRevealed(e.target.open)}>
              <summary>Show Share Token (one-time copy)</summary>
              <div className="token-value"><code className="break-all">{shareInfo.token}</code></div>
            </details>
          )}
          <div className="disclaimer-box">
            <strong>Important:</strong> Copy the link & token now; they won't be shown again later.
          </div>
        </div>
      )}
      {scanning && (
        <div className="scan-overlay">
          <div className="scan-modal">
            <div className="spinner" />
            <p>File is being scanned for potential security concerns...</p>
          </div>
        </div>
      )}
    </form>
  );
};

export default FileUploadForm;
