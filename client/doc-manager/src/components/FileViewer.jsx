import React, { useState, useContext, useEffect } from 'react';
import { Button, Form, Card, ListGroup, Alert } from 'react-bootstrap';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';
import { useLocation, useSearchParams, useNavigate } from 'react-router-dom';


const FileViewer = () => {
  const [searchParams] = useSearchParams();
  const revision = searchParams.get('revision');
  const [fileUrl, setFileUrl] = useState(null);
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const location = useLocation();
  const filePath = location.pathname;
  
  console.log(filePath.length)
  useEffect(() => {
    // Check for empty path
    if (filePath.length === 1) {
      navigate('/files', { replace: true }); // Replace in history
      return;
    }
    const fetchAndDisplayFile = async () => {
      try {
        const encodedPath = encodeURIComponent(filePath);
        
        // Construct the base URL
        let apiUrl = `http://localhost:8001/api/file_versions/retrieve${encodedPath}/`;
        
        // Add revision if it exists
        if (revision) {
          apiUrl += `?revision=${revision}`;
        }
        const response = await fetch(apiUrl, {
          headers: {
            'Authorization': `Token ${localStorage.getItem('token')}`
          }
        });

        if (!response.ok) {
          //console.log(response)
          throw new Error('Failed to fetch file')
          
        };

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        setFileUrl(url);

      } catch (err) {
        //console.error('Error:', err);
        setError("Failed to fetch file")
      }
    };  
    fetchAndDisplayFile();

    return () => {
      if (fileUrl) URL.revokeObjectURL(fileUrl);
    };
  }, [filePath]);

  const renderFileContent = () => {
    if (!fileUrl) {
      return (
        <div>
          {error && (
            <Alert variant="warning" className="mt-3">
              {error}
            </Alert>
          )}
        </div>
      );
    }

    const fileExtension = filePath.split('.').pop().toLowerCase();

    switch(fileExtension) {
      // Documents
      case 'pdf':
        return <embed src={fileUrl} type="application/pdf" width="100%" height="600px" />;
      case 'txt':
      case 'csv':
      case 'html':
      case 'htm':
        return <iframe src={fileUrl} title="text-viewer" style={{ width: '100%', height: '500px' }} />;

      // Images
      case 'jpg':
      case 'jpeg':
      case 'png':
      case 'gif':
      case 'webp':
      case 'svg':
      case 'bmp':
        return <img src={fileUrl} alt="Preview" style={{ maxWidth: '100%' }} />;

      
      default:
        return (
          <div>
            <p>Preview not available for .{fileExtension} files</p>
            <a href={fileUrl} download className="download-button">
              Download File
            </a>
          </div>
        );
    }
  };

  return (
    <div className="file-viewer-container">
      {renderFileContent()}
    </div>
  );
};
export default FileViewer;