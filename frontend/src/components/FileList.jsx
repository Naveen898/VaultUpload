import React from 'react';
import fileService from '../services/fileService';

const FileList = ({ files, setFiles }) => {
  const handleDelete = async (fileId) => {
    await fileService.deleteFile(fileId);
    setFiles(files.filter(f => f.file_id !== fileId));
  };

  return (
    <ul className="file-list">
      {files.map(file => (
        <li key={file.file_id}>
          <a href={file.downloadUrl} target="_blank" rel="noopener noreferrer">{file.name}</a>
          <span> (Expires: {file.expires_at?.split('T')[0] || 'N/A'})</span>
          <button onClick={() => handleDelete(file.file_id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
};

export default FileList;
