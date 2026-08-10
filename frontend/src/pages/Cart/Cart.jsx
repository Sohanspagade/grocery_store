import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { CartContext } from '../../context/CartContext';
import { getCurrentUser } from '../../services/authService';
import Loading from '../../components/Loading/Loading';
import { Minus, Plus, Trash2 } from 'lucide-react';
import styles from './Cart.module.css';

const Cart = () => {
  const { cart, removeFromCart, updateQuantity } = useContext(CartContext);
  const user = getCurrentUser();

  if (!user) {
    return (
      <div className={styles.emptyCart}>
        <h2>Please login to view your cart</h2>
        <Link to="/login" className={styles.primaryBtn}>Login</Link>
      </div>
    );
  }

  if (!cart) return <Loading />;

  if (cart.items.length === 0) {
    return (
      <div className={styles.emptyCart}>
        <img src="https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?auto=format&fit=crop&q=80&w=400" alt="Empty Cart" className={styles.emptyImg} />
        <h2>Your cart is empty</h2>
        <p>Looks like you haven't added anything to your cart yet.</p>
        <Link to="/products" className={styles.primaryBtn}>Start Shopping</Link>
      </div>
    );
  }

  const formatCurrency = (val) => new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR"
  }).format(val);

  return (
    <div className={styles.cartPage}>
      <h1 className={styles.title}>Shopping Cart</h1>
      
      <div className={styles.container}>
        <div className={styles.cartItems}>
          <div className={styles.tableHeader}>
            <div className={styles.colProduct}>Product</div>
            <div className={styles.colPrice}>Price</div>
            <div className={styles.colQuantity}>Quantity</div>
            <div className={styles.colSubtotal}>Subtotal</div>
            <div className={styles.colAction}></div>
          </div>
          
          {cart.items.map(item => (
            <div key={item.product_id} className={styles.cartRow}>
              <div className={styles.colProduct}>
                <Link to={`/products/${item.product_id}`} className={styles.productName}>{item.name}</Link>
              </div>
              <div className={styles.colPrice}>{formatCurrency(item.price)}</div>
              <div className={styles.colQuantity}>
                <div className={styles.quantityControl}>
                  <button onClick={() => updateQuantity(item.product_id, item.quantity - 1)} disabled={item.quantity <= 1}>
                    <Minus size={14} />
                  </button>
                  <span>{item.quantity}</span>
                  <button onClick={() => updateQuantity(item.product_id, item.quantity + 1)}>
                    <Plus size={14} />
                  </button>
                </div>
              </div>
              <div className={styles.colSubtotal}>{formatCurrency(item.subtotal)}</div>
              <div className={styles.colAction}>
                <button className={styles.removeBtn} onClick={() => removeFromCart(item.product_id)}>
                  <Trash2 size={18} />
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className={styles.summarySection}>
          <h2 className={styles.summaryTitle}>Order Summary</h2>
          <div className={styles.summaryRow}>
            <span>Subtotal</span>
            <span>{formatCurrency(cart.subtotal)}</span>
          </div>
          <div className={styles.summaryRow}>
            <span>Delivery Fee</span>
            <span>{cart.delivery_fee === 0 ? 'Free' : formatCurrency(cart.delivery_fee)}</span>
          </div>
          {cart.discount > 0 && (
            <div className={`${styles.summaryRow} ${styles.discountRow}`}>
              <span>Discount</span>
              <span>-{formatCurrency(cart.discount)}</span>
            </div>
          )}
          <div className={styles.totalRow}>
            <span>Total</span>
            <span>{formatCurrency(cart.total)}</span>
          </div>
          <button className={styles.checkoutBtn}>Proceed to Checkout</button>
          
          {cart.subtotal < 500 && (
            <p className={styles.deliveryNote}>Add {formatCurrency(500 - cart.subtotal)} more for free delivery!</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Cart;
