import React, { useEffect, useState, useContext } from 'react';
import { useSearchParams } from 'react-router-dom';
import { getProducts, getCategories } from '../../services/productService';
import { CartContext } from '../../context/CartContext';
import ProductCard from '../../components/ProductCard/ProductCard';
import Loading from '../../components/Loading/Loading';
import { Search } from 'lucide-react';
import styles from './Products.module.css';

const Products = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialCategory = searchParams.get('category') || '';
  
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Filters
  const [searchQuery, setSearchQuery] = useState(searchParams.get('search') || '');
  const [selectedCategory, setSelectedCategory] = useState(initialCategory);
  const [sort, setSort] = useState('');
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  
  const { addToCart } = useContext(CartContext);

  useEffect(() => {
    getCategories().then(setCategories).catch(console.error);
  }, []);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const params = {};
      if (searchQuery) params.search = searchQuery;
      if (selectedCategory) params.category = selectedCategory;
      if (sort) params.sort = sort;
      if (minPrice) params.min_price = minPrice;
      if (maxPrice) params.max_price = maxPrice;
      
      const data = await getProducts(params);
      setProducts(data);
    } catch (error) {
      console.error("Failed to fetch products", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
    // Update URL to match state
    const newParams = new URLSearchParams();
    if (searchQuery) newParams.set('search', searchQuery);
    if (selectedCategory) newParams.set('category', selectedCategory);
    setSearchParams(newParams);
  }, [searchQuery, selectedCategory, sort, minPrice, maxPrice]);

  return (
    <div className={styles.productsPage}>
      <div className={styles.pageHeader}>
        <h1 className={styles.title}>All Groceries</h1>
        <div className={styles.searchBar}>
          <Search size={20} className={styles.searchIcon} />
          <input 
            type="text" 
            placeholder="Search products..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className={styles.searchInput}
          />
        </div>
      </div>

      <div className={styles.content}>
        <aside className={styles.sidebar}>
          <div className={styles.filterSection}>
            <h3 className={styles.filterTitle}>Category</h3>
            <div className={styles.filterOptions}>
              <label className={styles.radioLabel}>
                <input 
                  type="radio" 
                  name="category" 
                  checked={selectedCategory === ''}
                  onChange={() => setSelectedCategory('')} 
                /> All
              </label>
              {categories.map(cat => (
                <label key={cat.id} className={styles.radioLabel}>
                  <input 
                    type="radio" 
                    name="category" 
                    checked={selectedCategory === cat.name}
                    onChange={() => setSelectedCategory(cat.name)} 
                  /> {cat.name}
                </label>
              ))}
            </div>
          </div>
          
          <div className={styles.filterSection}>
            <h3 className={styles.filterTitle}>Price Range</h3>
            <div className={styles.priceInputs}>
              <input 
                type="number" 
                placeholder="Min" 
                value={minPrice} 
                onChange={(e) => setMinPrice(e.target.value)}
                className={styles.priceInput}
              />
              <span>-</span>
              <input 
                type="number" 
                placeholder="Max" 
                value={maxPrice} 
                onChange={(e) => setMaxPrice(e.target.value)}
                className={styles.priceInput}
              />
            </div>
          </div>
          
          <div className={styles.filterSection}>
            <h3 className={styles.filterTitle}>Sort By</h3>
            <select 
              value={sort} 
              onChange={(e) => setSort(e.target.value)}
              className={styles.sortSelect}
            >
              <option value="">Default</option>
              <option value="price_asc">Price: Low to High</option>
              <option value="price_desc">Price: High to Low</option>
            </select>
          </div>
        </aside>

        <main className={styles.main}>
          {loading ? (
            <Loading />
          ) : products.length === 0 ? (
            <div className={styles.emptyState}>
              <p>No products found matching your criteria.</p>
              <button 
                onClick={() => {
                  setSearchQuery('');
                  setSelectedCategory('');
                  setMinPrice('');
                  setMaxPrice('');
                  setSort('');
                }}
                className={styles.resetBtn}
              >
                Reset Filters
              </button>
            </div>
          ) : (
            <div className={styles.productGrid}>
              {products.map(product => (
                <ProductCard 
                  key={product.id} 
                  product={product} 
                  onAdd={(id) => addToCart(id, 1)} 
                />
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default Products;
