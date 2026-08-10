import React, { useEffect, useState } from 'react';
import api from '../../services/api';
import styles from './BackendStatus.module.css';

const BackendStatus = () => {
  const [status, setStatus] = useState('Checking...');
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const checkStatus = async () => {
      try {
        await api.get('/api/health');
        setStatus('Backend Connected');
        setIsConnected(true);
      } catch (error) {
        setStatus('Backend Offline');
        setIsConnected(false);
        console.error("FastAPI CORS configuration is blocking http://localhost:5173", error);
      }
    };
    checkStatus();
  }, []);

  return (
    <div className={`${styles.statusContainer} ${isConnected ? styles.connected : styles.offline}`}>
      <span className={styles.dot}>●</span> {status}
    </div>
  );
};

export default BackendStatus;
