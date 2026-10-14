'use client';

import React from 'react';
import { Activity, Cpu, Layers, Users, Brain } from 'lucide-react';
import { RiskTwinLogo } from './RiskTwinLogo';

interface HeaderProps {
  activeTab: 'radar' | 'simulator' | 'agent-world' | 'stress-twin' | 'client-offers';
  setActiveTab: (tab: 'radar' | 'simulator' | 'agent-world' | 'stress-twin' | 'client-offers') => void;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, setActiveTab }) => {
  return (
    <header className="sticky top-0 z-50 w-full backdrop-blur-md bg-gradient-to-r from-emerald-800 via-emerald-700 to-teal-700 text-white shadow-md border-b border-emerald-600/30">
      <div className="max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          {/* Бренд */}
          <div className="flex items-center space-x-3.5">
            <div className="flex items-center justify-center w-11 h-11 rounded-2xl bg-white shadow-md ring-2 ring-white/20 p-1">
              <RiskTwinLogo className="w-8 h-8" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-2xl font-black tracking-tight text-white">
                  Risk<span className="text-emerald-200">Twin</span>
                </span>
                <span className="px-2.5 py-0.5 text-[11px] font-bold tracking-wide bg-white/20 text-white rounded-full">
                  AI Core 2.0
                </span>
              </div>
              <p className="text-xs text-emerald-100/90 font-medium">
                Предиктивный двойник финансового поведения
              </p>
            </div>
          </div>

          {/* Навигация */}
          <nav className="flex items-center space-x-1.5 p-1 bg-emerald-900/40 rounded-2xl border border-emerald-500/30">
            <button
              onClick={() => setActiveTab('radar')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all duration-200 ${
                activeTab === 'radar'
                  ? 'bg-white text-emerald-950 shadow-sm font-bold'
                  : 'text-emerald-100 hover:text-white hover:bg-emerald-800/50'
              }`}
            >
              <Activity className="w-4 h-4 text-emerald-600" />
              <span>Радар заемщика</span>
            </button>

            <button
              onClick={() => setActiveTab('agent-world')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all duration-200 ${
                activeTab === 'agent-world'
                  ? 'bg-white text-emerald-950 shadow-sm font-bold'
                  : 'text-emerald-100 hover:text-white hover:bg-emerald-800/50'
              }`}
            >
              <Users className="w-4 h-4 text-emerald-600" />
              <span>Мир ИИ-двойника</span>
            </button>

            <button
              onClick={() => setActiveTab('stress-twin')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all duration-200 ${
                activeTab === 'stress-twin'
                  ? 'bg-white text-emerald-950 shadow-sm font-bold'
                  : 'text-emerald-100 hover:text-white hover:bg-emerald-800/50'
              }`}
            >
              <Brain className="w-4 h-4 text-emerald-600" />
              <span>Психо-двойник 3D</span>
            </button>

            <button
              onClick={() => setActiveTab('simulator')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all duration-200 ${
                activeTab === 'simulator'
                  ? 'bg-white text-emerald-950 shadow-sm font-bold'
                  : 'text-emerald-100 hover:text-white hover:bg-emerald-800/50'
              }`}
            >
              <Cpu className="w-4 h-4 text-emerald-600" />
              <span>Стресс-тестирование</span>
            </button>

            <button
              onClick={() => setActiveTab('client-offers')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all duration-200 ${
                activeTab === 'client-offers'
                  ? 'bg-white text-emerald-950 shadow-sm font-bold'
                  : 'text-emerald-100 hover:text-white hover:bg-emerald-800/50'
              }`}
            >
              <Layers className="w-4 h-4 text-emerald-600" />
              <span>Витрина решений & ДБО</span>
            </button>
          </nav>

          {/* Индикатор статуса ML */}
          <div className="hidden md:flex items-center space-x-2.5 px-3.5 py-1.5 rounded-full bg-emerald-900/40 border border-white/20 text-xs">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-300 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-300"></span>
            </span>
            <span className="text-white font-medium text-[11px]">
              PyTorch Core Active
            </span>
          </div>

        </div>
      </div>
    </header>
  );
};