import React from 'react';
import { Link } from 'react-router-dom';
import { Heart, Star } from 'lucide-react';
import styles from './ProductCard.module.css';

const ProductCard = ({ product, onAdd }) => {
  const { id, name, price, original_price, unit, rating, category, image_url, stock } = product;

  const formattedPrice = new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR"
  }).format(price);

  const formattedOriginalPrice = new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR"
  }).format(original_price);

  const discount = Math.round(((original_price - price) / original_price) * 100);

  return (
    <div className={styles.card}>
      {discount > 0 && <div className={styles.discountBadge}>-{discount}%</div>}
      <button className={styles.wishlistBtn}><Heart size={18} /></button>
      
      <Link to={`/products/${id}`} className={styles.imageContainer}>
        <img src={image_url || `https://source.unsplash.com/400x400/?grocery,${encodeURIComponent(name)}`} alt={name} className={styles.image} onError={(e) => { e.target.src = 'https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&q=80&w=400'; }} />
      </Link>
      
      <div className={styles.content}>
        <div className={styles.category}>{category}</div>
        <Link to={`/products/${id}`} className={styles.name}>{name}</Link>
        
        <div className={styles.meta}>
          <span className={styles.rating}><Star size={14} fill="currentColor" /> {rating}</span>
          <span className={styles.unit}>{unit}</span>
        </div>
        
        <div className={styles.priceRow}>
          <div className={styles.prices}>
            <span className={styles.price}>{formattedPrice}</span>
            {original_price > price && <span className={styles.originalPrice}>{formattedOriginalPrice}</span>}
          </div>
          <button 
            className={styles.addBtn} 
            onClick={() => onAdd(id)}
            disabled={stock <= 0}
          >
            {stock > 0 ? 'Add' : 'Out'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
