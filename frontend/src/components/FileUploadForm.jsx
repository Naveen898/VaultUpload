import React, { useState } from 'react';
import fileService from '../services/fileService';
import Alert from './Alert';

const FileUploadForm = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [expiryHours, setExpiryHours] = useState(24);
  const [secretWord, setSecretWord] = useState('');
  const [shareInfo, setShareInfo] = useState(null);

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
      const uploadResp = await fileService.uploadFile(file, { expiryHours, secretWord });
      setMessage('File uploaded successfully');
      // Fetch share token
      const share = await fileService.getShareToken(uploadResp.file_id);
      setShareInfo({
        fileId: uploadResp.file_id,
        token: share.share_token,
        expiresAt: share.expires_at,
        requiresSecret: share.requires_secret
      });
      setFile(null);
    } catch (e) {
      setError('Upload failed: ' + e.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {message && <Alert type="success" message={message} />}
      {error && <Alert type="error" message={error} />}
      <input type="file" onChange={handleChange} />
      <div>
        <label>Expiry (hours, 1-24): </label>
        <input type="number" min={1} max={24} value={expiryHours} onChange={e => setExpiryHours(Number(e.target.value))} />
      </div>
      <div>
        <label>Secret Word (optional): </label>
        <input type="text" value={secretWord} onChange={e => setSecretWord(e.target.value)} placeholder="Enter secret" />
      </div>
      <button type="submit">Upload</button>
      {shareInfo && (
        <div style={{marginTop:'1rem'}}>
          <h4>Share Details</h4>
          <div><strong>File ID:</strong> {shareInfo.fileId}</div>
          <div><strong>Share Token:</strong> <code style={{wordBreak:'break-all'}}>{shareInfo.token}</code></div>
          <div><strong>Expires At:</strong> {shareInfo.expiresAt}</div>
          <div><strong>Secret Required:</strong> {shareInfo.requiresSecret ? 'Yes' : 'No'}</div>
          <div><strong>Download (secured access endpoint):</strong> /api/uploads/access/{'{file_id}'}</div>
        </div>
      )}
    </form>
  );
};

export default FileUploadForm;
