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
      //const encodedPath = encodeURIComponent(urlPath.replace(/^\//, ''));
      navigate(`/${urlPath}`, { replace: true });
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
          {file_version.version_number > 1 && (
          <div className="versions-list">
            {[...Array(file_version.version_number)].map((_, i) => (
              <div key={i} onClick={() => handleFileClick(file_version.url_path + "?revision="+i)} style={{
                color: 'blue',
                textDecoration: 'underline',
                cursor: 'pointer'
              }}>
                Version {i + 1}
              </div>
            ))}
          </div>
        )}
      </Card.Body>
    </Card>
  ));
}


function FileVersions() {
  const [data, setData] = useState([]);
  
  const API_BASE_URL = "http://localhost:8001/api/"
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

        const response = await fetch(`${API_BASE_URL}file_versions/`, {
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
      <h1>Your Latest Files</h1>
      <div>
        <FileVersionsList file_versions={data} />
      </div>
    </div>
  );
}

export default FileVersions;
