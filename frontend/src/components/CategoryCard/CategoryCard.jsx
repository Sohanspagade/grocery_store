import React from 'react';
import { Link } from 'react-router-dom';
import styles from './CategoryCard.module.css';

const CategoryCard = ({ category, image_url, count }) => {
  return (
    <Link to={`/products?category=${encodeURIComponent(category)}`} className={styles.card}>
      <div className={styles.imageCircle}>
        <img src={image_url || '/placeholder.png'} alt={category} className={styles.image} onError={(e) => { e.target.src = '/placeholder.png'; }} />
      </div>
      <h3 className={styles.name}>{category}</h3>
      <p className={styles.count}>{count} Products</p>
    </Link>
  );
};

export default CategoryCard;
