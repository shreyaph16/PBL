import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { Send, Zap, Sparkles, Clock, ShieldCheck, AlertCircle, Laptop, ListFilter, ChevronRight, BarChart, Info } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const AnalyzePage = () => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [batchLoading, setBatchLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [batchResult, setBatchResult] = useState(null);
  const [error, setError] = useState(null);
  
  // Product Selection States
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState('');
  const [sampleReviews, setSampleReviews] = useState([]);
  const [showProductDropdown, setShowProductDropdown] = useState(false);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const data = await api.getProducts();
        setProducts(data.products || []);
      } catch (err) {
        console.error("Failed to load products:", err);
      }
    };
    fetchProducts();
  }, []);

  const handleProductSelect = async (product) => {
    setSelectedProduct(product);
    setShowProductDropdown(false);
    setResult(null);
    setBatchResult(null);
    try {
      const data = await api.getProductReviews(product);
      setSampleReviews(data.reviews || []);
    } catch (err) {
      console.error("Failed to load reviews:", err);
    }
  };

  const handleAnalyzeAll = async () => {
    if (!selectedProduct) return;
    setBatchLoading(true);
    setResult(null);
    setError(null);
    try {
      const data = await api.analyzeProductBatch(selectedProduct);
      if (data.status === 'success') {
        setBatchResult(data);
      } else {
        setError(data.message || "Batch analysis failed.");
      }
    } catch (err) {
      console.error(err);
      setError("Batch engine encountered an error. Check backend logs.");
    } finally {
      setBatchLoading(false);
    }
  };

  const handleAnalyze = async (e) => {
    if (e) e.preventDefault();
    if (!text.trim()) return;

    setLoading(true);
    setBatchResult(null);
    setError(null);
    try {
      const data = await api.analyzeText(text);
      setResult(data);
    } catch (err) {
      console.error(err);
      setError("Analysis engine unreachable. Please check backend connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <header className="text-center">
        <h1 className="text-4xl font-black text-white mb-2 tracking-tight">Product <span className="text-indigo-400">Intelligence</span></h1>
        <p className="text-slate-400 max-w-2xl mx-auto">Analyze individual feedback or run a full batch evaluation of product sentiment using LangGraph and RoBERTa.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Dataset Navigator (Sidebar) */}
        <div className="lg:col-span-1 space-y-4">
          <div className="glass p-6 rounded-3xl h-full flex flex-col border border-white/10">
            <h3 className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] mb-4 flex items-center gap-2">
              <ListFilter size={14} /> Dataset Explorer
            </h3>
            
            <div className="relative mb-4">
              <button 
                onClick={() => setShowProductDropdown(!showProductDropdown)}
                className="w-full flex items-center justify-between gap-2 px-4 py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-left transition-colors"
              >
                <div className="flex items-center gap-2 truncate">
                  <Laptop size={18} className="text-indigo-400" />
                  <span className="truncate text-sm font-medium">{selectedProduct || "Select a Laptop..."}</span>
                </div>
                <ChevronRight className={`transition-transform flex-shrink-0 ${showProductDropdown ? 'rotate-90' : ''}`} size={16} />
              </button>

              <AnimatePresence>
                {showProductDropdown && (
                  <motion.div 
                    initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}
                    className="absolute top-full left-0 right-0 mt-2 bg-slate-900 border border-white/10 rounded-xl shadow-2xl z-30 max-h-60 overflow-y-auto"
                  >
                    {products.map((p, i) => (
                      <button key={i} onClick={() => handleProductSelect(p)} className="w-full px-4 py-3 text-left text-xs hover:bg-indigo-500/20 text-slate-300 hover:text-white border-b border-white/5 last:border-0 transition-colors">
                        {p}
                      </button>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {selectedProduct && (
              <button 
                onClick={handleAnalyzeAll}
                disabled={batchLoading}
                className={`w-full mb-6 py-3 px-4 rounded-xl flex items-center justify-center gap-2 font-bold text-xs uppercase tracking-widest transition-all ${
                  batchLoading ? "bg-slate-800 text-slate-500" : "bg-gradient-to-r from-indigo-600 to-purple-600 hover:scale-[1.02] shadow-lg shadow-indigo-500/20 text-white"
                }`}
              >
                {batchLoading ? <Zap className="animate-spin" size={16} /> : <BarChart size={16} />}
                {batchLoading ? "Running Batch..." : "Analyze All Reviews"}
              </button>
            )}

            <div className="flex-grow space-y-2 overflow-y-auto max-h-[400px] scrollbar-thin pr-2">
              {selectedProduct ? (
                <>
                  <p className="text-[10px] text-slate-500 font-black mb-2 uppercase tracking-widest">Available Samples</p>
                  {sampleReviews.map((r, i) => (
                    <button key={i} onClick={() => setText(r)} className="w-full p-3 text-left bg-white/5 hover:bg-indigo-500/10 rounded-lg text-xs leading-relaxed text-slate-400 transition-all border border-transparent hover:border-white/10">
                      {r.length > 70 ? r.substring(0, 70) + '...' : r}
                    </button>
                  ))}
                </>
              ) : (
                <div className="flex flex-col items-center justify-center p-8 text-center space-y-2 opacity-20 py-20 mt-10">
                  <Laptop size={48} />
                  <p className="text-xs">Pick a product above to start research</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Input & Form */}
        <div className="lg:col-span-3 space-y-6">
          <div className="glass p-1 rounded-3xl overflow-hidden focus-within:ring-2 ring-indigo-500/50 transition-all">
            <form onSubmit={handleAnalyze} className="bg-slate-900/40 p-6 rounded-[22px] space-y-4">
              <textarea 
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Enter review text or click a sample from the explorer..."
                className="w-full h-40 bg-transparent border-none focus:ring-0 text-slate-100 placeholder:text-slate-500 resize-none text-lg"
              />
              <div className="flex justify-between items-center pt-4 border-t border-white/5">
                <div className="flex gap-4 text-xs text-slate-500 font-bold">
                  <span className="flex items-center gap-1.5"><Clock size={14} /> ROBUST ENGINE</span>
                  {selectedProduct && <span className="flex items-center gap-1.5 text-indigo-400/70"><Info size={14} /> CONTEXT: {selectedProduct.split('-')[0]}</span>}
                </div>
                <button type="submit" disabled={loading || !text.trim()} className={`flex items-center gap-2 px-8 py-3 rounded-xl font-black uppercase text-xs tracking-widest transition-all ${loading || !text.trim() ? 'bg-slate-800 text-slate-500' : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-xl shadow-indigo-900/40 active:scale-95'}`}>
                  {loading ? <Zap className="animate-pulse fill-white" size={16} /> : <Send size={16} />}
                  {loading ? 'Analyzing' : 'Run Single Analysis'}
                </button>
              </div>
            </form>
          </div>

          <AnimatePresence mode="wait">
            {error && (
              <motion.div key="error" initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }} className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-100 flex items-center gap-3">
                <AlertCircle size={20} className="text-red-400" /> {error}
              </motion.div>
            )}

            {result && (
              <motion.div key="result" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="glass p-8 rounded-3xl flex flex-col items-center justify-center text-center">
                  <p className="text-slate-500 text-[10px] font-black uppercase tracking-[0.2em] mb-4">RoBERTa Result</p>
                  <h2 className={`text-5xl font-black uppercase tracking-tighter mb-4 ${result.label === 'positive' ? 'text-emerald-400' : result.label === 'negative' ? 'text-rose-400' : 'text-blue-400'}`}>{result.label}</h2>
                  <div className="w-full bg-white/5 h-1.5 rounded-full overflow-hidden">
                    <motion.div initial={{ width: 0 }} animate={{ width: `${result.confidence * 100}%` }} className={`h-full ${result.label === 'positive' ? 'bg-emerald-500' : result.label === 'negative' ? 'bg-rose-500' : 'bg-blue-500'}`} />
                  </div>
                  <p className="mt-4 text-xs text-slate-500 font-medium">Model Confidence: {(result.confidence * 100).toFixed(1)}%</p>
                </div>
                <div className="glass p-8 rounded-3xl relative">
                  <h3 className="text-sm font-black text-white mb-4 flex items-center gap-2 uppercase tracking-widest"><Sparkles size={16} className="text-indigo-400" /> Gemini Reasoning</h3>
                  <p className="text-slate-300 leading-relaxed text-sm italic">{result.reasoning || "Reasoning engine unavailable."}</p>
                </div>
              </motion.div>
            )}

            {batchResult && (
              <motion.div key="batch" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
                 <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="glass p-8 rounded-3xl flex flex-col items-center justify-center border-t-4 border-indigo-500">
                       <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2">Overall Sentiment</p>
                       <h2 className="text-4xl font-black text-white uppercase">{batchResult.overall_sentiment}</h2>
                    </div>
                    <div className="glass p-8 rounded-3xl md:col-span-2">
                       <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-6">Sentiment Distribution</p>
                       <div className="flex gap-2 h-8 w-full rounded-lg overflow-hidden">
                          {Object.entries(batchResult.sentiment_distribution).map(([label, count]) => (
                             <div 
                                key={label} 
                                style={{ width: `${(count / batchResult.metadata.total_rows) * 100}%` }}
                                className={`h-full flex items-center justify-center text-[10px] font-black ${label === 'Positive' ? 'bg-emerald-500' : label === 'Negative' ? 'bg-rose-500' : 'bg-blue-500'}`}
                             >
                                {count}
                             </div>
                          ))}
                       </div>
                       <div className="flex justify-between mt-3">
                          {Object.keys(batchResult.sentiment_distribution).map(label => (
                             <div key={label} className="flex items-center gap-1.5 text-[10px] font-bold text-slate-400 uppercase">
                                <span className={`w-2 h-2 rounded-full ${label === 'Positive' ? 'bg-emerald-500' : label === 'Negative' ? 'bg-rose-500' : 'bg-blue-500'}`} />
                                {label}
                             </div>
                          ))}
                       </div>
                    </div>
                 </div>
                 <div className="glass p-8 rounded-3xl border border-indigo-500/20 shadow-2xl shadow-indigo-500/10">
                    <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                       <Sparkles className="text-indigo-400 animate-pulse" size={20} /> 
                       Batch Executive Summary
                    </h3>
                    <p className="text-slate-200 text-lg leading-relaxed italic font-medium">
                       "{batchResult.reasoning_summary}"
                    </p>
                    <div className="mt-8 pt-6 border-t border-white/5 flex justify-between items-center text-[10px] text-slate-500 font-bold uppercase tracking-widest">
                       <span>Processed {batchResult.metadata.total_rows} Reviews</span>
                       <span>Timestamp: {new_date().toLocaleTimeString()}</span>
                    </div>
                 </div>
              </motion.div>
            )}
            
            {batchLoading && !batchResult && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="p-20 flex flex-col items-center justify-center space-y-4 glass rounded-3xl">
                 <div className="w-16 h-16 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin" />
                 <p className="text-indigo-400 font-black uppercase tracking-widest animate-pulse">Running LangGraph Pipeline...</p>
                 <p className="text-slate-500 text-xs italic">Loading RoBERTa weights and requesting Gemini reasoning for {selectedProduct}...</p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};

// Helper for date
const new_date = () => new Date();

export default AnalyzePage;
