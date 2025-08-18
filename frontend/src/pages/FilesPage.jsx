import React, { useEffect, useState } from 'react';
import fileService from '../services/fileService';
import FileList from '../components/FileList';
import Alert from '../components/Alert';

const FilesPage = () => {
  const [files, setFiles] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    fileService.listFiles()
      .then(setFiles)
      .catch(() => setError('Failed to fetch files'));
  }, []);

  const refresh = () => {
    fileService.listFiles()
      .then(setFiles)
      .catch(() => setError('Failed to fetch files'));
  };

  return (
    <div className="container">
      <h2>Your Files</h2>
      <button onClick={refresh} style={{marginBottom:'1rem'}}>Refresh</button>
      {error && <Alert type="error" message={error} />}
      <FileList files={files} setFiles={setFiles} />
    </div>
  );
};

export default FilesPage;
