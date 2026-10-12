'use client';

import React from 'react';
import { Activity, ShieldCheck, Cpu, Layers } from 'lucide-react';

interface HeaderProps {
  activeTab: 'radar' | 'simulator' | 'client-offers';
  setActiveTab: (tab: 'radar' | 'simulator' | 'client-offers') => void;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, setActiveTab }) => {
  return (
    <header className="sticky top-0 z-50 w-full backdrop-blur-md bg-gradient-to-r from-emerald-950 via-emerald-800 to-teal-700 text-white shadow-lg border-b border-emerald-500/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          {/* Бренд & Логотип */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center justify-center w-11 h-11 rounded-xl bg-gradient-to-br from-emerald-400 to-teal-200 text-emerald-950 shadow-md ring-2 ring-emerald-300/30">
              <ShieldCheck className="w-6 h-6 stroke-[2.2]" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-2xl font-bold tracking-tight text-white">
                  Risk<span className="text-emerald-300 font-extrabold">Twin</span>
                </span>
                <span className="px-2 py-0.5 text-[11px] font-semibold tracking-wide bg-emerald-400/20 text-emerald-200 rounded-full border border-emerald-400/30">
                  AI Core 2.0
                </span>
              </div>
              <p className="text-xs text-emerald-100/80 font-medium">
                Предиктивная аналитика финансового поведения
              </p>
            </div>
          </div>

          {/* Интерактивная навигация между разделами */}
          <nav className="flex items-center space-x-1.5 p-1 bg-emerald-900/60 rounded-xl border border-emerald-700/50 shadow-inner">
            <button
              onClick={() => setActiveTab('radar')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                activeTab === 'radar'
                  ? 'bg-white text-emerald-950 shadow-sm font-semibold'
                  : 'text-emerald-100/90 hover:text-white hover:bg-emerald-800/60'
              }`}
            >
              <Activity className="w-4 h-4 text-emerald-600" />
              <span>Радар наблюдения</span>
            </button>

            <button
              onClick={() => setActiveTab('simulator')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                activeTab === 'simulator'
                  ? 'bg-white text-emerald-950 shadow-sm font-semibold'
                  : 'text-emerald-100/90 hover:text-white hover:bg-emerald-800/60'
              }`}
            >
              <Cpu className="w-4 h-4 text-emerald-600" />
              <span>Стресс-моделирование</span>
            </button>

            <button
              onClick={() => setActiveTab('client-offers')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                activeTab === 'client-offers'
                  ? 'bg-white text-emerald-950 shadow-sm font-semibold'
                  : 'text-emerald-100/90 hover:text-white hover:bg-emerald-800/60'
              }`}
            >
              <Layers className="w-4 h-4 text-emerald-600" />
              <span>Витрина решений</span>
            </button>
          </nav>

          {/* Индикатор интеллектуального ядра (AI Engine Live Status) */}
          <div className="hidden md:flex items-center space-x-3 px-3.5 py-1.5 rounded-full bg-emerald-900/40 border border-emerald-400/20 text-xs">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-400"></span>
            </span>
            <span className="text-emerald-100 font-medium">
              ML-движок активен
            </span>
            <span className="text-emerald-300/40">|</span>
            <span className="text-emerald-200/80 font-mono text-[11px]">
              Latency: 14ms
            </span>
          </div>

        </div>
      </div>
    </header>
  );
};