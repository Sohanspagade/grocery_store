import React, { createContext, useState, useEffect } from 'react';
import * as cartService from '../services/cartService';
import { getCurrentUser, getCartUserId } from '../services/authService';

export const CartContext = createContext();

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState(null);
  const user = getCurrentUser();
  const cartUserId = getCartUserId();

  const fetchCart = async () => {
    if (cartUserId) {
      try {
        const data = await cartService.getCart(cartUserId);
        setCart(data);
      } catch (error) {
        console.error("Failed to fetch cart", error);
      }
    }
  };

  useEffect(() => {
    fetchCart();
  }, [cartUserId]);

  const addToCart = async (productId, quantity = 1) => {
    if (!cartUserId) return;
    await cartService.addToCart(cartUserId, productId, quantity);
    await fetchCart();
  };

  const removeFromCart = async (productId) => {
    if (!cartUserId) return;
    await cartService.removeCartItem(cartUserId, productId);
    await fetchCart();
  };

  const updateQuantity = async (productId, quantity) => {
    if (!cartUserId) return;
    await cartService.updateCartItem(cartUserId, productId, quantity);
    await fetchCart();
  };

  const clearCart = async () => {
    if (!cartUserId) return;
    await cartService.clearCart(cartUserId);
    await fetchCart();
  };

  const cartCount = cart?.items?.reduce((total, item) => total + item.quantity, 0) || 0;

  return (
    <CartContext.Provider value={{ cart, addToCart, removeFromCart, updateQuantity, clearCart, cartCount, fetchCart }}>
      {children}
    </CartContext.Provider>
  );
};
