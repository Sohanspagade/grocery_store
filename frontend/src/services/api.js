import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      if (error.response.status === 401) {
        console.error('Unauthorized - Handle logout or token refresh');
      } else if (error.response.status >= 500) {
        console.error('Server Error:', error.response.data);
      }
    }
    return Promise.reject(error);
  }
);

export default api;
