import React, { useEffect, useState, useContext } from 'react';
import { Link } from 'react-router-dom';
import { getCategories, getProducts } from '../../services/productService';
import { CartContext } from '../../context/CartContext';
import CategoryCard from '../../components/CategoryCard/CategoryCard';
import ProductCard from '../../components/ProductCard/ProductCard';
import Loading from '../../components/Loading/Loading';
import BackendStatus from '../../components/BackendStatus/BackendStatus';
import { ArrowRight, Star } from 'lucide-react';
import styles from './Home.module.css';

const Home = () => {
  const [categories, setCategories] = useState([]);
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const { addToCart } = useContext(CartContext);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [catsRes, prodsRes] = await Promise.all([
          getCategories(),
          getProducts({ limit: 8 })
        ]);
        setCategories(catsRes);
        setFeaturedProducts(prodsRes);
      } catch (error) {
        console.error("Error fetching home data:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className={styles.home}>
      <BackendStatus />
      
      {/* Hero Section */}
      <section className={styles.heroSection}>
        <div className={styles.heroContainer}>
          <div className={styles.heroLeft}>
            <span className={styles.heroBadge}>The Best Online Grocery Store</span>
            <h1 className={styles.heroTitle}>
              Your One-Stop Shop<br/>
              for <span className={styles.highlight}>Quality Groceries</span>
            </h1>
            <p className={styles.heroDesc}>
              Fresh groceries delivered to your doorstep with simple, smart shopping.
            </p>
            
            <div className={styles.heroButtons}>
              <Link to="/products" className={styles.primaryBtn}>Shop Now</Link>
              <Link to="/products" className={styles.secondaryBtn}>View All Products</Link>
            </div>
            
            <div className={styles.trustIndicators}>
              <div className={styles.trustItem}>
                <Star className={styles.trustIcon} fill="currentColor" />
                <span><strong>4.8</strong> Ratings+</span>
              </div>
              <div className={styles.trustItem}>
                <span>Trusted by <strong>75K+</strong> Customers</span>
              </div>
            </div>
          </div>
          
          <div className={styles.heroRight}>
            <img src="https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&q=80&w=800" alt="Fresh Groceries" className={styles.heroImg} />
          </div>
        </div>
      </section>
      
      {/* Categories Section */}
      <section className={styles.section}>
        <div className={styles.sectionHeader}>
          <div>
            <h2 className={styles.sectionTitle}>Featured Categories</h2>
            <p className={styles.sectionSubtitle}>Explore our grocery categories</p>
          </div>
        </div>
        
        {loading ? <Loading /> : (
          <div className={styles.categoryGrid}>
            {categories.map((cat, idx) => (
              <CategoryCard 
                key={cat.id} 
                category={cat.name} 
                count={Math.floor(Math.random() * 50) + 10} 
              />
            ))}
          </div>
        )}
      </section>

      {/* Featured Products */}
      <section className={styles.section}>
        <div className={styles.sectionHeader}>
          <div>
            <h2 className={styles.sectionTitle}>Featured Products</h2>
            <p className={styles.sectionSubtitle}>Top picks for you</p>
          </div>
          <Link to="/products" className={styles.viewAllLink}>
            View All <ArrowRight size={16} />
          </Link>
        </div>
        
        {loading ? <Loading /> : (
          <div className={styles.productGrid}>
            {featuredProducts.map(product => (
              <ProductCard 
                key={product.id} 
                product={product} 
                onAdd={(id) => addToCart(id, 1)} 
              />
            ))}
          </div>
        )}
      </section>

      {/* Discount Banner */}
      <section className={styles.discountBanner}>
        <div className={styles.bannerContent}>
          <h2 className={styles.bannerTitle}>Summer Discount</h2>
          <p className={styles.bannerSubtitle}>Get 20% off selected groceries.</p>
          <Link to="/products" className={styles.primaryBtn}>Shop Now</Link>
        </div>
        <div className={styles.bannerOverlay}></div>
      </section>
    </div>
  );
};

export default Home;
