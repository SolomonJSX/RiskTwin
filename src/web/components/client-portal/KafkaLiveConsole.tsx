'use client';

import React from 'react';
import { Terminal, Radio, CheckCircle, Database } from 'lucide-react';

export interface KafkaLogMessage {
  id: string;
  timestamp: string;
  topic: string;
  eventType: string;
  partition: number;
  payload: Record<string, any>;
  direction: 'inbound' | 'outbound';
}

interface KafkaLiveConsoleProps {
  logs: KafkaLogMessage[];
}

export const KafkaLiveConsole: React.FC<KafkaLiveConsoleProps> = ({ logs }) => {
  return (
    <div className="rounded-2xl bg-slate-950 text-slate-100 border border-slate-800 shadow-xl overflow-hidden font-mono text-xs">
      {/* Top Console Bar */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-slate-900 border-b border-slate-800">
        <div className="flex items-center space-x-2.5">
          <Terminal className="w-4 h-4 text-emerald-400" />
          <span className="font-bold text-slate-200">
            Apache Kafka Event Bus <span className="text-slate-400 font-normal">(Redpanda Engine)</span>
          </span>
          <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-700/50 flex items-center space-x-1">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span>broker: localhost:9092</span>
          </span>
        </div>

        <div className="flex items-center space-x-3 text-[11px] text-slate-400">
          <span className="flex items-center space-x-1">
            <Radio className="w-3.5 h-3.5 text-emerald-400" />
            <span>EDA Active</span>
          </span>
          <span className="text-slate-600">|</span>
          <span className="flex items-center space-x-1">
            <Database className="w-3.5 h-3.5 text-teal-400" />
            <span>4 Topics</span>
          </span>
        </div>
      </div>

      {/* Topics Summary Chips */}
      <div className="px-4 py-2 bg-slate-900/60 border-b border-slate-800/80 flex flex-wrap items-center gap-2 text-[10px]">
        <span className="text-slate-400 font-semibold">Active Topics:</span>
        <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
          banking.telemetry.v1
        </span>
        <span className="px-2 py-0.5 rounded bg-rose-950/60 text-rose-300 border border-rose-800/50">
          risk.alerts.ews.v1
        </span>
        <span className="px-2 py-0.5 rounded bg-amber-950/60 text-amber-300 border border-amber-800/50">
          risk.restructuring.approved.v1
        </span>
        <span className="px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-800/50">
          risk.contracts.signed.v1
        </span>
      </div>

      {/* Stream Messages */}
      <div className="p-3 max-h-48 overflow-y-auto space-y-2 select-text font-mono text-[11px]">
        {logs.length === 0 ? (
          <div className="text-slate-500 py-2 text-center">Ожидание событий брокера Kafka...</div>
        ) : (
          logs.map((log) => (
            <div
              key={log.id}
              className="p-2 rounded-lg bg-slate-900/90 border border-slate-800 hover:border-slate-700 transition-colors flex items-start space-x-3"
            >
              <span className="text-slate-500 shrink-0 font-medium">{log.timestamp}</span>
              
              <span
                className={`text-[10px] px-1.5 py-0.5 rounded font-bold uppercase shrink-0 ${
                  log.direction === 'inbound'
                    ? 'bg-blue-950 text-blue-300 border border-blue-800'
                    : 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                }`}
              >
                {log.direction === 'inbound' ? 'CONSUME' : 'PRODUCE'}
              </span>

              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2">
                  <span className="text-emerald-400 font-semibold">{log.topic}</span>
                  <span className="text-slate-600">•</span>
                  <span className="text-amber-300 font-medium">{log.eventType}</span>
                  <span className="text-slate-500 text-[10px]">part:{log.partition}</span>
                </div>
                <div className="text-slate-400 text-[10px] mt-0.5 truncate">
                  {JSON.stringify(log.payload)}
                </div>
              </div>

              <CheckCircle className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" />
            </div>
          ))
        )}
      </div>
    </div>
  );
};
