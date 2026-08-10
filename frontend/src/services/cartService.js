import api from './api';

export const getCart = async (userId) => {
  const response = await api.get(`/api/cart/${userId}`);
  return response.data;
};

export const addToCart = async (userId, productId, quantity) => {
  const response = await api.post('/api/cart', {
    user_id: userId,
    product_id: productId,
    quantity
  });
  return response.data;
};

export const updateCartItem = async (userId, productId, quantity) => {
  const response = await api.put(`/api/cart/${userId}/${productId}`, { quantity });
  return response.data;
};

export const removeCartItem = async (userId, productId) => {
  const response = await api.delete(`/api/cart/${userId}/${productId}`);
  return response.data;
};

export const clearCart = async (userId) => {
  const response = await api.delete(`/api/cart/${userId}`);
  return response.data;
};
