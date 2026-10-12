'use client';

import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { 
  History, 
  AlertTriangle, 
  TrendingUp, 
  Clock, 
  ShieldAlert, 
  CheckCircle2, 
  HelpCircle, 
  Activity, 
  RefreshCw,
  Zap,
  ArrowUpRight,
  Brain,
  Info
} from 'lucide-react';

interface ClientHistoryModalProps {
  clientToken: string;
  accountNumber: string;
  currentRiskProb: number;
  lastScoring?: {
    pDefault30d: number;
    pDefault60d: number;
    triggeredAt: string;
    shapFactorsJson?: string;
    featureSnapshotJson?: string;
  };
  onClose: () => void;
  onEvaluate: () => void;
}

export const ClientHistoryModal: React.FC<ClientHistoryModalProps> = ({
  clientToken,
  accountNumber,
  currentRiskProb,
  lastScoring,
  onClose,
  onEvaluate,
}) => {
  const [activeTab, setActiveTab] = useState<'timeline' | 'cross_attention' | 'features'>('timeline');

  // Запрос хроники изменений через API Сталкера
  const { data: timelineData, isLoading: isTimelineLoading, refetch } = useQuery({
    queryKey: ['timeline', clientToken],
    queryFn: () => api.getTimeline(clientToken),
    refetchInterval: 5000,
  });

  // Парсинг XAI факторов внимания / SHAP
  let shapDrivers: any[] = [];
  if (lastScoring?.shapFactorsJson) {
    try {
      shapDrivers = JSON.parse(lastScoring.shapFactorsJson);
    } catch {
      shapDrivers = [];
    }
  }

  // Парсинг слепка признаков из Feature Store
  let featuresSnapshot: Record<string, any> = {};
  if (lastScoring?.featureSnapshotJson) {
    try {
      featuresSnapshot = JSON.parse(lastScoring.featureSnapshotJson);
    } catch {
      featuresSnapshot = {};
    }
  }

  const timelineItems = timelineData || [];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
      <div 
        className="glass-card bg-white rounded-3xl max-w-4xl w-full max-h-[90vh] overflow-hidden shadow-2xl border border-emerald-500/20 flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Шапка модального окна */}
        <div className="p-6 bg-gradient-to-r from-emerald-950 via-emerald-900 to-teal-800 text-white flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-2xl bg-emerald-500/20 border border-emerald-400/30 text-emerald-300">
              <History className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="text-xl font-bold">Хроника изменений и динамика риска</h3>
                <span className="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-400/20 text-emerald-200 border border-emerald-400/30 font-mono">
                  {accountNumber}
                </span>
              </div>
              <p className="text-xs text-emerald-200/80 mt-0.5 font-mono">
                Токен: {clientToken}
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <div className="text-right">
              <p className="text-[11px] text-emerald-200/80 font-medium">Текущий риск дефолта</p>
              <div className="flex items-center space-x-1.5 justify-end">
                <span className={`text-2xl font-black ${currentRiskProb > 40 ? 'text-rose-300' : 'text-emerald-300'}`}>
                  {currentRiskProb}%
                </span>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-sm transition-colors"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Вкладки переключения вида */}
        <div className="px-6 pt-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div className="flex space-x-2">
            <button
              onClick={() => setActiveTab('timeline')}
              className={`pb-3 px-3 text-xs font-bold transition-all border-b-2 flex items-center space-x-1.5 ${
                activeTab === 'timeline'
                  ? 'border-emerald-600 text-emerald-700'
                  : 'border-transparent text-slate-500 hover:text-slate-800'
              }`}
            >
              <Clock className="w-3.5 h-3.5" />
              <span>Лента событий (Timeline)</span>
              {timelineItems.length > 0 && (
                <span className="ml-1 px-1.5 py-0.2 text-[10px] bg-emerald-100 text-emerald-800 rounded-full">
                  {timelineItems.length}
                </span>
              )}
            </button>

            <button
              onClick={() => setActiveTab('cross_attention')}
              className={`pb-3 px-3 text-xs font-bold transition-all border-b-2 flex items-center space-x-1.5 ${
                activeTab === 'cross_attention'
                  ? 'border-emerald-600 text-emerald-700'
                  : 'border-transparent text-slate-500 hover:text-slate-800'
              }`}
            >
              <Brain className="w-3.5 h-3.5" />
              <span>Интерпретация ИИ (Cross-Attention)</span>
            </button>

            <button
              onClick={() => setActiveTab('features')}
              className={`pb-3 px-3 text-xs font-bold transition-all border-b-2 flex items-center space-x-1.5 ${
                activeTab === 'features'
                  ? 'border-emerald-600 text-emerald-700'
                  : 'border-transparent text-slate-500 hover:text-slate-800'
              }`}
            >
              <Activity className="w-3.5 h-3.5" />
              <span>Слепок признаков (Feature Store)</span>
            </button>
          </div>

          <button
            onClick={() => refetch()}
            className="p-1.5 text-xs text-slate-500 hover:text-emerald-600 transition-colors flex items-center space-x-1"
            title="Обновить данные"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span className="text-[11px]">Обновить</span>
          </button>
        </div>

        {/* Тело модального окна со скроллом */}
        <div className="p-6 overflow-y-auto flex-1 space-y-6">
          
          {/* ВКЛАДКА 1: TIMELINE */}
          {activeTab === 'timeline' && (
            <div className="space-y-4">
              <div className="bg-emerald-50/50 border border-emerald-200/60 rounded-2xl p-4 flex items-start space-x-3">
                <Info className="w-5 h-5 text-emerald-700 mt-0.5 flex-shrink-0" />
                <div className="text-xs text-slate-600 leading-relaxed">
                  <p className="font-semibold text-slate-800">
                    Автоматическая фиксация изменений поведения клиента
                  </p>
                  Каждое новое событие (задержка зарплаты, платеж в МФО, ночная тревожность в ДБО) мгновенно анализируется модулем <span className="font-bold text-emerald-700">«Сталкер»</span> и обновляет вероятность дефолта.
                </div>
              </div>

              {isTimelineLoading ? (
                <div className="py-12 text-center text-slate-400">
                  <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2 text-emerald-600" />
                  <p className="text-xs">Загрузка хроники клиента...</p>
                </div>
              ) : timelineItems.length === 0 ? (
                <div className="text-center py-10 bg-slate-50 rounded-2xl border border-dashed border-slate-200">
                  <CheckCircle2 className="w-8 h-8 text-emerald-500 mx-auto mb-2" />
                  <p className="text-sm font-bold text-slate-700">Аномалий и резких изменений не зафиксировано</p>
                  <p className="text-xs text-slate-500 mt-1">Клиент совершает стандартные транзакции в рамках финансового профиля</p>
                </div>
              ) : (
                <div className="relative pl-6 border-l-2 border-emerald-200 space-y-6 my-2">
                  {timelineItems.map((item: any, idx: number) => {
                    const isSevere = item.severity === 'CRITICAL' || item.deltaPd > 0.15;
                    const dateFormatted = new Date(item.timestamp).toLocaleString('ru-RU', {
                      day: '2-digit',
                      month: 'short',
                      hour: '2-digit',
                      minute: '2-digit',
                    });

                    return (
                      <div key={item.snapshotId || idx} className="relative group">
                        {/* Точка на таймлайне */}
                        <div className={`absolute -left-[31px] top-1 w-4 h-4 rounded-full border-2 border-white shadow-sm flex items-center justify-center ${
                          isSevere ? 'bg-rose-500 ring-4 ring-rose-100' : 'bg-emerald-500 ring-4 ring-emerald-100'
                        }`} />

                        <div className={`p-4 rounded-2xl border transition-all ${
                          isSevere
                            ? 'bg-rose-50/40 border-rose-200 hover:bg-rose-50/70'
                            : 'bg-white border-slate-200 hover:border-emerald-300'
                        }`}>
                          <div className="flex items-center justify-between mb-1.5">
                            <span className="text-[11px] font-bold text-slate-500 flex items-center space-x-1.5">
                              <Clock className="w-3 h-3" />
                              <span>{dateFormatted}</span>
                            </span>

                            <div className="flex items-center space-x-2">
                              <span className={`text-xs font-black px-2 py-0.5 rounded-lg flex items-center space-x-1 ${
                                item.deltaPd > 0 
                                  ? 'bg-rose-100 text-rose-700' 
                                  : 'bg-emerald-100 text-emerald-700'
                              }`}>
                                <ArrowUpRight className="w-3 h-3" />
                                <span>{(item.deltaPd > 0 ? '+' : '') + Math.round(item.deltaPd * 100)}% к риску</span>
                              </span>
                              <span className="text-xs font-bold text-slate-700">
                                Итог PD: {Math.round(item.riskScore * 100)}%
                              </span>
                            </div>
                          </div>

                          <p className="text-xs font-semibold text-slate-800 mt-1">
                            {item.eventDescriptionRu}
                          </p>

                          <div className="mt-2 pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
                            <span>Баланс на день: {item.dailyBalance?.toLocaleString('ru-RU')} KZT</span>
                            <span>DTI: {Math.round(item.dti * 100)}%</span>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}

          {/* ВКЛАДКА 2: CROSS-ATTENTION & XAI */}
          {activeTab === 'cross_attention' && (
            <div className="space-y-4">
              <div className="bg-teal-50/50 border border-teal-200/60 rounded-2xl p-4 flex items-start space-x-3">
                <Brain className="w-5 h-5 text-teal-700 mt-0.5 flex-shrink-0" />
                <div className="text-xs text-slate-600 leading-relaxed">
                  <p className="font-semibold text-slate-800">
                    Нейросетевая матрица синергии факторов (FT-Transformer)
                  </p>
                  Нейросеть связывает финансовые маркеры заемщика с его психоэмоциональным поведением через механизм <span className="font-bold text-teal-700">Cross-Attention [7×9]</span>, определяя первопричину риска.
                </div>
              </div>

              {shapDrivers.length === 0 ? (
                <div className="text-center py-10 bg-slate-50 rounded-2xl border border-dashed border-slate-200">
                  <AlertTriangle className="w-8 h-8 text-amber-500 mx-auto mb-2" />
                  <p className="text-sm font-bold text-slate-700">Глубокий скоринг еще не запускался</p>
                  <p className="text-xs text-slate-500 mt-1">Нажмите «Подобрать план ИИ» для полного инференса нейросети</p>
                </div>
              ) : (
                <div className="space-y-3">
                  <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                    Ключевые драйверы риска (Веса взаимного внимания):
                  </h4>

                  <div className="grid grid-cols-1 gap-2.5">
                    {shapDrivers.map((driver: any, i: number) => {
                      const weightPct = Math.round(driver.impactWeight * 100);

                      return (
                        <div 
                          key={i} 
                          className="p-3.5 rounded-2xl bg-white border border-slate-200 hover:border-emerald-300 transition-all shadow-xs flex items-center justify-between"
                        >
                          <div className="flex items-center space-x-3">
                            <span className="w-6 h-6 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold flex items-center justify-center">
                              {i + 1}
                            </span>
                            <div>
                              <p className="text-xs font-bold text-slate-800">
                                {driver.humanReadableReason || driver.featureName}
                              </p>
                              <p className="text-[10px] text-slate-400 font-mono">
                                Фича: {driver.featureName}
                              </p>
                            </div>
                          </div>

                          <div className="text-right">
                            <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                              Сила влияния: {weightPct}%
                            </span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* ВКЛАДКА 3: ОНЛАЙН СЛЕПОК FEATURE STORE */}
          {activeTab === 'features' && (
            <div className="space-y-4">
              <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4 text-xs text-slate-600">
                <p className="font-semibold text-slate-800 mb-1">
                  Онлайн скользящие окна (Redis Feature Store)
                </p>
                Текущие актуальные агрегаты расходов, остатков и поведенческих маркеров ДБО, используемые моделью.
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {Object.entries(featuresSnapshot).length > 0 ? (
                  Object.entries(featuresSnapshot).map(([key, val]) => (
                    <div key={key} className="p-3 bg-white border border-slate-200 rounded-xl">
                      <p className="text-[10px] text-slate-400 font-mono truncate" title={key}>{key}</p>
                      <p className="text-sm font-bold text-slate-800 mt-0.5">
                        {typeof val === 'number' ? (val % 1 !== 0 ? val.toFixed(2) : val.toLocaleString('ru-RU')) : String(val)}
                      </p>
                    </div>
                  ))
                ) : (
                  <div className="col-span-3 text-center py-8 text-slate-400 text-xs">
                    Слепок признаков появится после первого запуска скоринга
                  </div>
                )}
              </div>
            </div>
          )}

        </div>

        {/* Подвал модального окна */}
        <div className="p-5 border-t border-slate-200 bg-slate-50 flex items-center justify-between">
          <p className="text-xs text-slate-500">
            Система непрерывно пересчитывает риск при обнаружении транзакционных аномалий
          </p>
          <div className="flex space-x-3">
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-200 transition-colors"
            >
              Закрыть
            </button>
            <button
              onClick={() => {
                onClose();
                onEvaluate();
              }}
              className="px-5 py-2 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 shadow-sm transition-all"
            >
              Сформировать превентивный оффер
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
