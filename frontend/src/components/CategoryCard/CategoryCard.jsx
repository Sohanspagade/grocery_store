import React from 'react';
import { Link } from 'react-router-dom';
import styles from './CategoryCard.module.css';

const CategoryCard = ({ category, image_url, count }) => {
  return (
    <Link to={`/products?category=${encodeURIComponent(category)}`} className={styles.card}>
      <div className={styles.imageCircle}>
        <img src={image_url || `https://source.unsplash.com/150x150/?${encodeURIComponent(category)},food`} alt={category} className={styles.image} onError={(e) => { e.target.src = 'https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&q=80&w=150'; }} />
      </div>
      <h3 className={styles.name}>{category}</h3>
      <p className={styles.count}>{count} Products</p>
    </Link>
  );
};

export default CategoryCard;
