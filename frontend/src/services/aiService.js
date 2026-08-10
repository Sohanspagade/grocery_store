import api from './api';

export const chatWithAI = async (userId, message) => {
  const response = await api.post('/api/ai/chat', { user_id: userId, message });
  return response.data;
};

export const generateShoppingList = async (data) => {
  const response = await api.post('/api/ai/shopping-list', data);
  return response.data;
};
