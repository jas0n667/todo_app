import axios from 'axios';

// Настройка базового URL
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000', // URL вашего FastAPI приложения
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
