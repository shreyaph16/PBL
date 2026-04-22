import React, { useState, useEffect } from 'react';
import { LayoutDashboard, BarChart3, Search, Database, GitBranch, Terminal } from 'lucide-react';
import DashboardPage from './pages/DashboardPage';
import AnalyzePage from './pages/AnalyzePage';
import Navbar from './components/Navbar';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="flex-grow container mx-auto px-4 py-8">
        {activeTab === 'dashboard' ? <DashboardPage /> : <AnalyzePage />}
      </main>
      
      <footer className="py-6 border-t border-white/5 bg-slate-900/30">
        <div className="container mx-auto px-4 flex justify-between items-center text-slate-500 text-sm">
          <div className="flex items-center gap-2">
            <Terminal size={14} />
            <span>Sentiment-App Engine v1.0.0</span>
          </div>
          <div className="flex items-center gap-4">
            <a href="#" className="hover:text-indigo-400 transition-colors">Documentation</a>
            <a href="#" className="hover:text-indigo-400 transition-colors flex items-center gap-1">
              <GitBranch size={14} /> GitHub
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
