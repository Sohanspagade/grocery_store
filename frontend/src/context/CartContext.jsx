import React, { createContext, useState, useEffect } from 'react';
import * as cartService from '../services/cartService';
import { getCurrentUser } from '../services/authService';

export const CartContext = createContext();

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState(null);
  const user = getCurrentUser();

  const fetchCart = async () => {
    if (user) {
      try {
        const data = await cartService.getCart(user.id);
        setCart(data);
      } catch (error) {
        console.error("Failed to fetch cart", error);
      }
    }
  };

  useEffect(() => {
    fetchCart();
  }, [user?.id]);

  const addToCart = async (productId, quantity = 1) => {
    if (!user) return alert("Please login to add to cart");
    await cartService.addToCart(user.id, productId, quantity);
    await fetchCart();
  };

  const removeFromCart = async (productId) => {
    if (!user) return;
    await cartService.removeCartItem(user.id, productId);
    await fetchCart();
  };

  const updateQuantity = async (productId, quantity) => {
    if (!user) return;
    await cartService.updateCartItem(user.id, productId, quantity);
    await fetchCart();
  };

  const clearCart = async () => {
    if (!user) return;
    await cartService.clearCart(user.id);
    await fetchCart();
  };

  const cartCount = cart?.items?.reduce((total, item) => total + item.quantity, 0) || 0;

  return (
    <CartContext.Provider value={{ cart, addToCart, removeFromCart, updateQuantity, clearCart, cartCount, fetchCart }}>
      {children}
    </CartContext.Provider>
  );
};
