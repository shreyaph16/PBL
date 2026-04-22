import React from 'react';
import { Layout, Search, Zap } from 'lucide-react';

const Navbar = ({ activeTab, setActiveTab }) => {
  return (
    <nav className="sticky top-0 z-50 glass border-b border-white/5 mb-2">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <Zap size={18} className="text-white fill-white" />
          </div>
          <span className="text-xl font-bold tracking-tight text-white">Sentiment<span className="text-indigo-400">App</span></span>
        </div>
        
        <div className="flex items-center gap-1 bg-slate-800/50 p-1 rounded-xl border border-white/5">
          <button 
            onClick={() => setActiveTab('dashboard')}
            className={`flex items-center gap-2 px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === 'dashboard' 
                ? 'bg-indigo-500 text-white shadow-lg shadow-indigo-500/20' 
                : 'text-slate-400 hover:text-slate-100'
            }`}
          >
            <Layout size={16} />
            Dashboard
          </button>
          <button 
            onClick={() => setActiveTab('analyze')}
            className={`flex items-center gap-2 px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === 'analyze' 
                ? 'bg-indigo-500 text-white shadow-lg shadow-indigo-500/20' 
                : 'text-slate-400 hover:text-slate-100'
            }`}
          >
            <Search size={16} />
            Analyze
          </button>
        </div>
        
        <div className="hidden md:block">
          <span className="text-xs bg-indigo-500/10 text-indigo-400 px-3 py-1 rounded-full border border-indigo-500/20 font-medium">
            Project Gemini Ready
          </span>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
