import React, { useEffect, useState, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getProduct } from '../../services/productService';
import { CartContext } from '../../context/CartContext';
import Loading from '../../components/Loading/Loading';
import { Star, Minus, Plus } from 'lucide-react';
import styles from './ProductDetails.module.css';

const ProductDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const { addToCart } = useContext(CartContext);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const data = await getProduct(id);
        setProduct(data);
      } catch (error) {
        console.error("Error fetching product", error);
      } finally {
        setLoading(false);
      }
    };
    fetchProduct();
  }, [id]);

  if (loading) return <Loading />;
  if (!product) return <div className={styles.error}>Product not found</div>;

  const handleAdd = () => {
    addToCart(product.id, quantity);
    navigate('/cart');
  };

  const formattedPrice = new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR"
  }).format(product.price);

  const formattedOriginal = new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR"
  }).format(product.original_price);

  return (
    <div className={styles.detailsPage}>
      <div className={styles.container}>
        <div className={styles.imageSection}>
          <img 
            src={product.image_url || `https://source.unsplash.com/600x600/?grocery,${encodeURIComponent(product.name)}`} 
            alt={product.name} 
            className={styles.image}
            onError={(e) => { e.target.src = 'https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&q=80&w=600'; }}
          />
        </div>
        
        <div className={styles.infoSection}>
          <div className={styles.category}>{product.category}</div>
          <h1 className={styles.name}>{product.name}</h1>
          
          <div className={styles.meta}>
            <div className={styles.rating}>
              <Star size={18} fill="currentColor" /> {product.rating}
            </div>
            <div className={styles.unit}>{product.unit}</div>
          </div>
          
          <div className={styles.priceRow}>
            <span className={styles.price}>{formattedPrice}</span>
            {product.original_price > product.price && (
              <span className={styles.originalPrice}>{formattedOriginal}</span>
            )}
          </div>
          
          <p className={styles.description}>{product.description}</p>
          
          <div className={styles.stockInfo}>
            Status: <span className={product.stock > 0 ? styles.inStock : styles.outOfStock}>
              {product.stock > 0 ? `In Stock (${product.stock} available)` : 'Out of Stock'}
            </span>
          </div>
          
          <div className={styles.actionRow}>
            <div className={styles.quantityControl}>
              <button 
                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                disabled={quantity <= 1}
              ><Minus size={18} /></button>
              <span>{quantity}</span>
              <button 
                onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                disabled={quantity >= product.stock}
              ><Plus size={18} /></button>
            </div>
            
            <button 
              className={styles.addToCartBtn}
              onClick={handleAdd}
              disabled={product.stock === 0}
            >
              {product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetails;
