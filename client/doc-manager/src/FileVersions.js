import React, { useState, useEffect } from "react";
import api from "./api/axios";
import { useAuth } from "./context/AuthContext";
import { useNavigate } from 'react-router-dom';
import "./FileVersions.css";

function FileVersionsList(props) {
  const file_versions = props.file_versions;
  
  const handleFileClick = async (urlPath) => {
    try {
      const encodedPath = encodeURIComponent(urlPath.replace(/^\//, ''));
      const response = await api.get(`file_versions/retrieve/${encodedPath}/`, {
        responseType: 'blob'
      });

      // Get the filename from Content-Disposition or URL
      const fileName = response.headers['content-disposition']
        ? response.headers['content-disposition'].split('filename=')[1].replace(/"/g, '')
        : urlPath.split('/').pop();

      // // Create blob URL with proper type
      // const blob = new Blob([response.data], { type: response.headers['content-type'] });
      // const fileUrl = window.URL.createObjectURL(blob);

      // // For PDFs/images - open in new tab
      // if (response.headers['content-type'].match(/(pdf|image)/)) {
      //   const viewerWindow = window.open(fileUrl, '_blank');
      //   viewerWindow.onload = () => URL.revokeObjectURL(fileUrl);
      // } 
      // Create object URL
      const fileUrl = URL.createObjectURL(response.data);
      
      // Determine if we should view or download
      const isViewable = response.headers['content-type'].match(/(pdf|image)/);
      
      if (isViewable) {
        window.open(fileUrl, '_blank');
        // The URL will be revoked when the window is closed
      }
      // For other files - download
      else {
        const link = document.createElement('a');
        link.href = fileUrl;
        link.setAttribute('download', fileName);
        document.body.appendChild(link);
        link.click();
        link.remove();
        setTimeout(() => URL.revokeObjectURL(fileUrl), 100);
      }
    } catch (error) {
      console.error('File open error:', error);
      // Show error to user
    }
  };
  
  return file_versions.map((file_version) => (
    <div className="file-version" key={file_version.id}>
      <h2>File Name: {file_version.file_name}</h2>
      <p>
        ID: {file_version.id} Version: {file_version.version_number}
        <p>
            Path: {' '}
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
      </p>
    </div>
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
        <FileVersionsList file_versions={data} />h
      </div>
    </div>
  );
}

export default FileVersions;
