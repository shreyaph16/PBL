import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  analyzeText: async (text) => {
    const response = await client.post('/analyze', { text });
    return response.data;
  },
  getReviews: async () => {
    const response = await client.get('/reviews');
    return response.data;
  },
  submitReview: async (reviewData) => {
    const response = await client.post('/reviews', reviewData);
    return response.data;
  },
  getProducts: async () => {
    const response = await client.get('/products');
    return response.data;
  },
  getProductReviews: async (productName) => {
    // New URL structure to support slashes in product names
    const response = await client.get(`/products/reviews/${encodeURIComponent(productName)}`);
    return response.data;
  },
  analyzeProductBatch: async (productName) => {
    // New URL structure to support slashes in product names
    const response = await client.post(`/products/analyze-all/${encodeURIComponent(productName)}`);
    return response.data;
  },
};

export default client;
