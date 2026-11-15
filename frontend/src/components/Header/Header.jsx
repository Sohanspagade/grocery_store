import React, { useContext, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShoppingCart, Heart, User, Search, MapPin, Menu } from 'lucide-react';
import { CartContext } from '../../context/CartContext';
import { getCurrentUser, logout } from '../../services/authService';
import styles from './Header.module.css';

const Header = () => {
  const { cartCount } = useContext(CartContext);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const user = getCurrentUser();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className={styles.header}>
      {/* Top Promotional Strip */}
      <div className={styles.promoStrip}>
        <div className={styles.promoContent}>
          <span>Call Us: +123-456-789</span>
          <span className={styles.promoCenter}>Sign up and GET 25% OFF for your first order.</span>
          <Link to="/signup" className={styles.signUpLink}>Sign up now</Link>
        </div>
      </div>

      {/* Main Header */}
      <div className={styles.mainHeader}>
        <div className={styles.logoSection}>
          <Link to="/" className={styles.logo}>
            <ShoppingCart className={styles.logoIcon} />
            SmartCart
          </Link>
          <div className={styles.location}>
            <MapPin size={16} />
            <span>New York, USA</span>
          </div>
        </div>

        <div className={styles.searchSection}>
          <input type="text" placeholder="Search for products..." className={styles.searchInput} />
          <button className={styles.searchButton}>
            <Search size={18} />
          </button>
        </div>

        <div className={styles.actionsSection}>
          <Link to="/wishlist" className={styles.actionIcon}>
            <Heart size={24} />
          </Link>
          <Link to="/cart" className={styles.actionIcon}>
            <ShoppingCart size={24} />
            {cartCount > 0 && <span className={styles.cartBadge}>{cartCount}</span>}
          </Link>
          
          {user ? (
            <div className={styles.userMenu}>
              <span className={styles.userName}>Hi, {user.name}</span>
              <button onClick={handleLogout} className={styles.logoutBtn}>Logout</button>
            </div>
          ) : (
            <Link to="/login" className={styles.actionIcon}>
              <User size={24} />
            </Link>
          )}

          <button className={styles.mobileMenuBtn} onClick={() => setIsMenuOpen(!isMenuOpen)}>
            <Menu size={24} />
          </button>
        </div>
      </div>

      {/* Navigation */}
      <nav className={`${styles.navigation} ${isMenuOpen ? styles.navOpen : ''}`}>
        <div className={styles.navLinks}>
          <Link to="/">Home</Link>
          <Link to="/products">Shop</Link>
          <Link to="/products?category=Fruits">Fruits</Link>
          <Link to="/products?category=Vegetables">Vegetables</Link>
          <Link to="/products?category=Beverages">Beverages</Link>
          <Link to="/ai-assistant">AI Assistant</Link>
        </div>
        <Link to="/products" className={styles.browseAllBtn}>
          Browse All Categories
        </Link>
      </nav>
    </header>
  );
};

export default Header;
