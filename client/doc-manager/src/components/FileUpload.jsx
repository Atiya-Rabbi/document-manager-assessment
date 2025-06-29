import React, { useState } from 'react';
import api from '../api/axios';
import { Alert, Button, ProgressBar, Form, Card } from 'react-bootstrap';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [path, setPath] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [progress, setProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setIsUploading(true);

    if (!file || !path) {
      setError('Both file and path are required');
      setIsUploading(false);
      return;
    }

    const fileExtension = file.name.split('.').pop().toLowerCase();
    const pathExtension = path.split('.').pop().toLowerCase();

    if (fileExtension !== pathExtension) {
      setError('File extension and path extension must match');
      setIsUploading(false);
      return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('path', path);

    try {
      const response = await api.post( 
        'file_versions/upload/', 
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data' // Override for file upload
          },
          onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setProgress(percentCompleted);
          }
        }
      );

      if (response.status === 201) {
        setSuccess(`Uploaded v${response.data.version_number}: ${response.data.file_name}`);
      } else if (response.status === 200) {
        setSuccess(`Content unchanged. Using v${response.data.version.version_number}`);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed. Check console for details.');
      console.error('Upload error:', err);
    } finally {
      setIsUploading(false);
      setProgress(0);
    }
  };

  return (
    <Card className="mt-4">
      <Card.Header as="h5">Upload Document</Card.Header>
      <Card.Body>
        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>File URL</Form.Label>
            <Form.Control
              type="text"
              value={path}
              onChange={(e) => setPath(e.target.value)}
              placeholder="e.g. /documents/report.pdf"
              required
            />
            <Form.Text className="text-muted">
              Desired URL to view the file
            </Form.Text>
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Select File</Form.Label>
            <Form.Control 
              type="file"
              onChange={(e) => setFile(e.target.files[0])}
              required
            />
          </Form.Group>

          {progress > 0 && (
            <ProgressBar 
              now={progress} 
              label={`${progress}%`}
              striped 
              animated 
              className="mb-3"
            />
          )}

          <Button 
            variant="primary" 
            type="submit"
            disabled={!file || !path || isUploading}
          >
            {isUploading ? 'Uploading...' : 'Upload'}
          </Button>

          {error && (
            <Alert variant="danger" className="mt-3">
              {error}
            </Alert>
          )}

          {success && (
            <Alert variant="success" className="mt-3">
              {success}
            </Alert>
          )}
        </Form>
      </Card.Body>
    </Card>
  );
};

export default FileUpload;