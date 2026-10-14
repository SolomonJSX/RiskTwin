'use client';

import React from 'react';
import { Radio, Clock } from 'lucide-react';
import { motion } from 'framer-motion';

export interface SignalEvent {
  id: string;
  timestamp: string;
  clientAccount: string;
  source: string;
  severity: 'high' | 'medium' | 'info';
  description: string;
  prediction: string;
}

interface LiveSignalFeedProps {
  signals: SignalEvent[];
  onSelectClient?: (accountNumber: string) => void;
}

export const LiveSignalFeed: React.FC<LiveSignalFeedProps> = ({
  signals,
  onSelectClient,
}) => {
  return (
    <div className="glass-card rounded-2xl p-5 bg-white border border-slate-200/80 shadow-sm space-y-4">
      
      {/* Аккуратная шапка без вырвиглазных овалов */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-100">
        <div className="flex items-center space-x-2">
          <span className="relative flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
          </span>
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800 flex items-center space-x-1.5">
            <Radio className="w-3.5 h-3.5 text-emerald-600" />
            <span>Живой перехват сигналов</span>
          </h3>
        </div>
        <span className="text-[11px] text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200 font-medium">
          Стрим активен
        </span>
      </div>

      <div className="space-y-2.5 max-h-[380px] overflow-y-auto pr-1">
        {signals.map((sig, idx) => (
          <motion.div
            key={sig.id}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.05 }}
            onClick={() => onSelectClient && onSelectClient(sig.clientAccount)}
            className="p-3 rounded-xl border border-slate-100 hover:border-emerald-300 bg-slate-50/60 hover:bg-emerald-50/20 transition-all cursor-pointer group"
          >
            <div className="flex items-center justify-between text-[11px] mb-1">
              <span className="font-semibold text-slate-700 flex items-center space-x-1.5">
                <span className={`w-2 h-2 rounded-full ${
                  sig.severity === 'high'
                    ? 'bg-rose-500'
                    : sig.severity === 'medium'
                    ? 'bg-amber-500'
                    : 'bg-emerald-500'
                }`} />
                <span className="font-mono text-xs">{sig.clientAccount}</span>
                <span className="text-slate-400">({sig.source})</span>
              </span>
              <span className="text-slate-400 font-mono text-[10px] flex items-center space-x-1">
                <Clock className="w-3 h-3" />
                <span>{sig.timestamp}</span>
              </span>
            </div>

            <p className="text-xs text-slate-800 font-medium group-hover:text-emerald-950 transition-colors">
              {sig.description}
            </p>

            <div className="mt-1.5 text-[11px] text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-lg border border-emerald-200/60">
              💡 {sig.prediction}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};
