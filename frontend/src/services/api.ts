import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터 - 토큰 추가
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 응답 인터셉터 - 401 에러 처리
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  signup: (email: string, password: string, phone_number?: string) =>
    api.post('/auth/signup', { email, password, phone_number }),
  getCurrentUser: () => api.get('/auth/me'),
};

// Stock Trade API
export const tradesAPI = {
  getList: (skip = 0, limit = 10, filters?: any) =>
    api.get('/trades', { params: { skip, limit, ...filters } }),
  getById: (id: number) => api.get(`/trades/${id}`),
  create: (trade: any) => api.post('/trades', trade),
  update: (id: number, trade: any) => api.put(`/trades/${id}`, trade),
  delete: (id: number) => api.delete(`/trades/${id}`),
  getSummary: () => api.get('/trades/stats/summary'),
};

// Subscription API
export const subscriptionsAPI = {
  getList: () => api.get('/subscriptions'),
  create: (subscription: any) => api.post('/subscriptions', subscription),
  update: (id: number, subscription: any) =>
    api.put(`/subscriptions/${id}`, subscription),
  toggle: (id: number) => api.post(`/subscriptions/${id}/toggle`),
  delete: (id: number) => api.delete(`/subscriptions/${id}`),
};
