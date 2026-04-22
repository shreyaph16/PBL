import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { Database, AlertCircle, RotateCw, CheckCircle2 } from 'lucide-react';

const DashboardPage = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      const result = await api.getReviews();
      setData(result);
      setError(null);
    } catch (err) {
      console.error(err);
      setError("Waiting for backend connection...");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-8 p-4">
      <header>
        <h1 className="text-3xl font-bold text-white">Sentiment Dashboard</h1>
        <p className="text-slate-400">Total analysis throughput across all products.</p>
      </header>

      <div className="bg-slate-900/50 p-6 rounded-2xl border border-white/10">
        <h3 className="text-xl font-bold text-white mb-4">System Status</h3>
        {loading && !data.length ? (
          <div className="flex items-center gap-2 text-indigo-400">
            <RotateCw className="animate-spin" size={20} />
            <span>Establishing link to backend...</span>
          </div>
        ) : error && !data.length ? (
          <div className="flex items-center gap-2 text-rose-400">
            <AlertCircle size={20} />
            <span>{error}</span>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
             <div className="bg-slate-800/50 p-6 rounded-xl border border-white/5">
               <p className="text-slate-400 text-sm font-bold uppercase tracking-widest mb-1">Total Analyzed</p>
               <p className="text-4xl font-black text-white">{data.length}</p>
             </div>
             <div className="bg-slate-800/50 p-6 rounded-xl border border-white/5">
               <p className="text-slate-400 text-sm font-bold uppercase tracking-widest mb-1">Engine Status</p>
               <div className="flex items-center gap-2">
                 <CheckCircle2 className="text-emerald-400" size={24} />
                 <p className="text-2xl font-bold text-emerald-400">Online</p>
               </div>
             </div>
             <div className="bg-slate-800/50 p-6 rounded-xl border border-white/5">
               <p className="text-slate-400 text-sm font-bold uppercase tracking-widest mb-1">Confidence Avg</p>
               <p className="text-2xl font-bold text-indigo-400">
                {data.length > 0 ? (data.reduce((acc, curr) => acc + curr.confidence, 0) / data.length * 100).toFixed(1) : "0.0"}%
               </p>
             </div>
          </div>
        )}
      </div>

      <div className="bg-slate-900/50 p-6 rounded-2xl border border-white/10">
        <h3 className="text-xl font-bold text-white mb-4">Recent Live Analysis</h3>
        <div className="space-y-3">
          {data.length === 0 ? (
            <div className="p-8 text-center border-2 border-dashed border-white/5 rounded-xl">
               <p className="text-slate-500 italic">No records found. Use the Analyze tab to run your first evaluation!</p>
            </div>
          ) : (
            data.slice(0, 8).map((r, i) => (
              <div key={i} className="p-4 bg-white/5 hover:bg-white/10 rounded-xl flex justify-between items-center group transition-all">
                <div className="flex-1 pr-8">
                   <p className="text-slate-300 text-sm line-clamp-1 group-hover:line-clamp-none transition-all">{r.review_text}</p>
                   <p className="text-[10px] text-slate-500 mt-1 uppercase tracking-tighter hover:text-indigo-400 transition-colors cursor-default">Product: {r.product_name}</p>
                </div>
                <div className={`px-3 py-1 rounded-lg font-black text-xs uppercase ${
                  r.sentiment === 'positive' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' :
                  r.sentiment === 'negative' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' :
                  'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                }`}>
                  {r.sentiment}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
