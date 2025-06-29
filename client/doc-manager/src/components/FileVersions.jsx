import React, { useState, useEffect } from "react";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from 'react-router-dom';
import { Card } from 'react-bootstrap';

function FileVersionsList(props) {
  const file_versions = props.file_versions;
  const navigate = useNavigate();
  const handleFileClick = async (urlPath) => {
    try {
      const encodedPath = encodeURIComponent(urlPath.replace(/^\//, ''));
      navigate(`/${encodedPath}`, { replace: true });
    } catch (error) {
      console.error('File open error:', error);
    }
  };
  
  return file_versions.map((file_version) => (
    <Card className="mt-4" key={file_version.id}>
      <Card.Header as="h5">File Name: {file_version.file_name}</Card.Header>
      <Card.Body>
        ID: {file_version.id} Version: {file_version.version_number}
        <p>
            File URL: {' '}
            <span 
              onClick={() => handleFileClick(file_version.url_path)}
              style={{
                color: 'blue',
                textDecoration: 'underline',
                cursor: 'pointer'
              }}
            >
              {file_version.url_path}
            </span>
          </p>
      </Card.Body>
    </Card>
  ));
}


function FileVersions() {
  const [data, setData] = useState([]);
  
  const navigate = useNavigate();
  console.log(data);

  useEffect(() => {
    
    const dataFetch = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          navigate('/login');
          return;
        }

        const response = await fetch('http://localhost:8001/api/file_versions/', {
          headers: {
            'Authorization': `Token ${token}`
          }
        });

        if (response.status === 401) {
          localStorage.removeItem('token');
          navigate('/login');
          return;
        }

        const data = await response.json();
        setData(data);
      } catch (err) {
        console.error('Failed to fetch files:', err);
      }

    };

    dataFetch();
  },[navigate]);
  return (
    <div>
      <h1>Found {data.length} File Versions</h1>
      <div>
        <FileVersionsList file_versions={data} />
      </div>
    </div>
  );
}

export default FileVersions;
