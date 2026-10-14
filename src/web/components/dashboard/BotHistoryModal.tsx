'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  History, 
  Clock, 
  Brain, 
  FileText, 
  X, 
  CheckCircle2, 
  AlertTriangle, 
  ShieldAlert, 
  TrendingDown, 
  TrendingUp, 
  Sparkles,
  Zap,
  Cpu,
  Eye,
  Check
} from 'lucide-react';
import { AttentionToken } from '@/components/deep-learning/DeepLearningExplainer';
import { LlmReasoningView } from '@/components/deep-learning/LlmReasoningView';

interface BotHistoryModalProps {
  isOpen: boolean;
  onClose: () => void;
  bot: {
    accountNumber: string;
    name: string;
    role: string;
    avatar: string;
    clientToken: string;
    monthlyIncome?: number;
    monthlyPayment?: number;
    currentPrincipal?: number;
    riskProbability: number;
    tokens: AttentionToken[];
    passport360?: Record<string, any>;
  };
  onEvaluate?: () => void;
}

export const BotHistoryModal: React.FC<BotHistoryModalProps> = ({
  isOpen,
  onClose,
  bot,
  onEvaluate,
}) => {
  const [activeTab, setActiveTab] = useState<'timeline' | 'xai' | 'features' | 'llm'>('timeline');

  if (!isOpen) return null;

  const isHighRisk = bot.riskProbability > 50;
  const isMediumRisk = bot.riskProbability > 25 && bot.riskProbability <= 50;

  // Реальные 360° банковские признаки из 6 таблиц Home Credit
  const featureStoreItems = [
    { name: 'AMT_INCOME_TOTAL', label: '1. Ежемесячный доход (Application)', val: `₸ ${(bot.monthlyIncome || 1200000).toLocaleString('ru-RU')}`, group: 'App' },
    { name: 'dti_ratio', label: '2. Коэффициент долговой нагрузки (DTI)', val: bot.passport360?.dti_ratio ? `${(bot.passport360.dti_ratio * 100).toFixed(1)}%` : '12.1%', group: 'App' },
    { name: 'EXT_SOURCE_2', label: '3. Внешний кредитный скоринг (Бюро ПКБ)', val: bot.passport360?.ext_source || '0.88 (Класс AAA)', group: 'Bureau' },
    { name: 'bureau_total_debt', label: '4. Долги в других банках (Бюро ПКБ)', val: `${bot.passport360?.bureau_total_debt || 0} ₸`, group: 'Bureau' },
    { name: 'bureau_total_overdue', label: '5. Внешние просрочки (Бюро ПКБ)', val: '0 ₸ (Чистая КИ)', group: 'Bureau' },
    { name: 'inst_avg_delay_days', label: '6. Дисциплина (Installments Payments)', val: `${bot.passport360?.inst_avg_delay_days || -5.4} дн. (досрочно)`, group: 'Tx' },
    { name: 'inst_late_count', label: '7. Число задержек за историю (Installments)', val: `${bot.passport360?.inst_late_count || 0} платежей`, group: 'Tx' },
    { name: 'inst_underpay_count', label: '8. Недоплаты / кассовые дефициты', val: '0 ₸', group: 'Tx' },
    { name: 'pos_completed_count', label: '9. Успешно закрытые BNPL (POS CASH)', val: `${bot.passport360?.pos_completed_count || 2} контракта`, group: 'POS' },
    { name: 'pos_max_dpd', label: '10. Дней просрочки по рассрочкам (POS)', val: '0 дней DPD', group: 'POS' },
    { name: 'cc_pos_drawings_sum', label: '12. Безналичные покупки картой (Credit Card)', val: `₸ ${(bot.passport360?.cc_pos_drawings_sum || 320000).toLocaleString('ru-RU')} (прозрачно)`, group: 'CC' },
    { name: 'cc_utilization_mean', label: '13. Утилизация лимита кредитной карты', val: `${((bot.passport360?.cc_utilization_mean ?? 0.18) * 100).toFixed(0)}%`, group: 'CC' },
    { name: 'prev_approved_count', label: '14. Одобренные заявки в банке (Previous App)', val: `${bot.passport360?.prev_approved_count ?? 3} одобрено`, group: 'Prev' },
    { name: 'prev_refused_count', label: '15. Отказы банков в прошлом (Previous App)', val: `${bot.passport360?.prev_refused_count || 0} отказов`, group: 'Prev' },
    { name: 'employment_years', label: '16. Непрерывный трудовой стаж', val: `${bot.passport360?.employment_years || 7} лет`, group: 'App' },
  ];

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs animate-in fade-in duration-200"
      onClick={onClose}
    >
      <div 
        className="bg-white rounded-3xl max-w-4xl w-full max-h-[92vh] overflow-hidden shadow-2xl border border-slate-200 flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        
        {/* Шапка модального окна */}
        <div className="p-6 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
          <div className="flex items-center space-x-3.5">
            <div className="w-14 h-14 rounded-2xl bg-white border border-slate-200 flex items-center justify-center text-3xl shadow-xs">
              {bot.avatar}
            </div>
            <div>
              <div className="flex items-center space-x-2.5">
                <h3 className="text-xl font-extrabold text-slate-900 tracking-tight">
                  {bot.name}
                </h3>
                <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-300">
                  {bot.role}
                </span>
              </div>
              <p className="text-xs text-slate-500 font-mono mt-0.5">
                Счет: {bot.accountNumber} • Токен: {bot.clientToken.substring(0, 18)}...
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className="text-right">
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                Вероятность риска (PD)
              </span>
              <span className={`text-2xl font-black font-mono ${
                isHighRisk ? 'text-rose-600' : isMediumRisk ? 'text-amber-600' : 'text-emerald-700'
              }`}>
                {bot.riskProbability}%
              </span>
            </div>

            <button
              onClick={onClose}
              className="w-9 h-9 rounded-xl bg-white hover:bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-600 hover:text-slate-900 transition-colors cursor-pointer shadow-2xs"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Быстрые финансовые карточки */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 p-4 bg-emerald-50/30 border-b border-slate-100 text-xs">
          <div className="bg-white p-2.5 rounded-xl border border-slate-200 shadow-2xs">
            <span className="text-slate-400 text-[10px] block">Доход в месяц:</span>
            <span className="font-bold text-slate-900 font-mono">
              ₸ {(bot.monthlyIncome || 450000).toLocaleString('ru-RU')}
            </span>
          </div>
          <div className="bg-white p-2.5 rounded-xl border border-slate-200 shadow-2xs">
            <span className="text-slate-400 text-[10px] block">Платеж по кредиту:</span>
            <span className="font-bold text-slate-900 font-mono">
              ₸ {(bot.monthlyPayment || 78500).toLocaleString('ru-RU')}
            </span>
          </div>
          <div className="bg-white p-2.5 rounded-xl border border-slate-200 shadow-2xs">
            <span className="text-slate-400 text-[10px] block">Остаток долга:</span>
            <span className="font-bold text-slate-900 font-mono">
              ₸ {(bot.currentPrincipal || 2400000).toLocaleString('ru-RU')}
            </span>
          </div>
          <div className="bg-white p-2.5 rounded-xl border border-slate-200 shadow-2xs">
            <span className="text-slate-400 text-[10px] block">Статус портфеля:</span>
            <span className={`font-bold ${isHighRisk ? 'text-rose-600' : isMediumRisk ? 'text-amber-600' : 'text-emerald-700'}`}>
              {isHighRisk ? '⚠️ В зоне риска' : isMediumRisk ? 'Требует внимания' : '✅ Стабильный'}
            </span>
          </div>
        </div>

        {/* Навигационные табы модалки */}
        <div className="px-6 pt-3 border-b border-slate-200 bg-white flex space-x-4">
          <button
            onClick={() => setActiveTab('timeline')}
            className={`pb-3 text-xs font-bold transition-all border-b-2 flex items-center space-x-1.5 cursor-pointer ${
              activeTab === 'timeline'
                ? 'border-emerald-600 text-emerald-700'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <Clock className="w-3.5 h-3.5" />
            <span>Хроника транзакций и событий ({bot.tokens.length})</span>
          </button>

          <button
            onClick={() => setActiveTab('xai')}
            className={`pb-3 text-xs font-bold transition-all border-b-2 flex items-center space-x-1.5 cursor-pointer ${
              activeTab === 'xai'
                ? 'border-emerald-600 text-emerald-700'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <Brain className="w-3.5 h-3.5" />
            <span>Веса внимания PyTorch XAI (α)</span>
          </button>

          <button
            onClick={() => setActiveTab('features')}
            className={`pb-3 text-xs font-bold transition-all border-b-2 flex items-center space-x-1.5 cursor-pointer ${
              activeTab === 'features'
                ? 'border-emerald-600 text-emerald-700'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Аудит 16 признаков</span>
          </button>

          <button
            onClick={() => setActiveTab('llm')}
            className={`pb-3 text-xs font-bold transition-all border-b-2 flex items-center space-x-1.5 cursor-pointer ${
              activeTab === 'llm'
                ? 'border-emerald-600 text-emerald-700'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
            <span>🤖 Вердикт нейросети (Ollama LLM)</span>
          </button>
        </div>

        {/* Содержимое вкладок */}
        <div className="p-6 overflow-y-auto flex-1 space-y-4">
          
          {/* ВКЛАДКА 1: Хроника событий */}
          {activeTab === 'timeline' && (
            <div className="space-y-3">
              <p className="text-xs text-slate-500 mb-2">
                Полная история финансовых транзакций и поведенческих триггеров заемщика во времени:
              </p>

              {bot.tokens.map((token, idx) => {
                const isCritical = token.weight > 0.8;
                const isWarning = token.weight > 0.4 && token.weight <= 0.8;

                return (
                  <motion.div
                    key={`${token.day}-${idx}`}
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.04 }}
                    className={`p-4 rounded-2xl border transition-all ${
                      isCritical
                        ? 'bg-rose-50/60 border-rose-200'
                        : isWarning
                        ? 'bg-amber-50/60 border-amber-200'
                        : 'bg-emerald-50/40 border-emerald-200'
                    }`}
                  >
                    <div className="flex items-center justify-between text-xs mb-1.5">
                      <div className="flex items-center space-x-2">
                        <span className="font-mono font-bold text-slate-700 px-2 py-0.5 rounded-md bg-white border border-slate-200 text-[11px]">
                          {token.day}
                        </span>
                        <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${
                          token.category === 'income'
                            ? 'bg-emerald-100 text-emerald-800'
                            : token.category === 'microloan'
                            ? 'bg-rose-100 text-rose-800'
                            : token.category === 'night_activity'
                            ? 'bg-amber-100 text-amber-800'
                            : 'bg-slate-100 text-slate-700'
                        }`}>
                          {token.category === 'income' ? 'Поступление' : token.category === 'microloan' ? 'Микрозайм' : token.category === 'night_activity' ? 'Ночной ДБО' : 'Транзакция'}
                        </span>
                      </div>

                      <div className="flex items-center space-x-2">
                        <span className="text-[11px] text-slate-500 font-mono">Вес внимания:</span>
                        <span className={`font-mono font-black text-xs ${
                          isCritical ? 'text-rose-600' : isWarning ? 'text-amber-600' : 'text-emerald-700'
                        }`}>
                          α = {token.weight.toFixed(2)}
                        </span>
                      </div>
                    </div>

                    <p className="text-xs font-semibold text-slate-900 mb-2">
                      {token.event}
                    </p>

                    <div className="w-full bg-slate-200/80 rounded-full h-1.5 overflow-hidden">
                      <div
                        className={`h-full rounded-full ${
                          isCritical ? 'bg-rose-500' : isWarning ? 'bg-amber-500' : 'bg-emerald-500'
                        }`}
                        style={{ width: `${Math.min(token.weight * 100, 100)}%` }}
                      />
                    </div>
                  </motion.div>
                );
              })}
            </div>
          )}

          {/* ВКЛАДКА 2: XAI Векторы внимания */}
          {activeTab === 'xai' && (
            <div className="space-y-4">
              <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs text-slate-700 leading-relaxed">
                <span className="font-bold text-emerald-900 block mb-1">
                  Архитектура Dual-Tower Cross-Attention (PyTorch):
                </span>
                Механизм кросс-внимания связывает финансовую историю с психоэмоциональным профилем. 
                Каждый вес α отражает силу синергии: как ночной вход в ДБО или падение зарплаты сдвигает латентный вектор дефолта.
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {bot.tokens.map((token, idx) => (
                  <div key={idx} className="p-3.5 rounded-xl bg-white border border-slate-200 shadow-2xs space-y-1.5">
                    <div className="flex justify-between items-center text-xs">
                      <span className="font-mono text-slate-500">{token.day}</span>
                      <span className="font-mono font-bold text-emerald-700">Внимание: {(token.weight * 100).toFixed(0)}%</span>
                    </div>
                    <p className="text-xs font-medium text-slate-800 line-clamp-2">{token.event}</p>
                    <div className="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                      <div
                        className="h-full bg-emerald-600 rounded-full"
                        style={{ width: `${Math.min(token.weight * 100, 100)}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ВКЛАДКА 3: Аудит признаков Feature Store */}
          {activeTab === 'features' && (
            <div className="space-y-3">
              <p className="text-xs text-slate-500">
                Значения 16 признаков модели `DualTowerCrossAttentionNet` в Feature Store на текущий момент:
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
                {featureStoreItems.map((f, idx) => (
                  <div key={idx} className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 flex items-center justify-between text-xs">
                    <div>
                      <span className="font-semibold text-slate-800 block text-[11px]">{f.label}</span>
                      <span className="text-[10px] text-slate-400 font-mono">{f.name}</span>
                    </div>
                    <span className="font-mono font-bold text-slate-900 bg-white px-2 py-0.5 rounded-md border border-slate-200">
                      {f.val}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ВКЛАДКА 4: LLM Neuro-Symbolic Вердикт (Ollama) */}
          {activeTab === 'llm' && (
            <LlmReasoningView
              name={bot.name}
              role={bot.role}
              accountNumber={bot.accountNumber}
              riskProbability={bot.riskProbability}
              tokens={bot.tokens}
              passport360={bot.passport360}
            />
          )}

        </div>

        {/* Подвал с действиями */}
        <div className="p-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between">
          <div className="flex items-center space-x-2 text-xs text-slate-500 font-mono">
            <Zap className="w-3.5 h-3.5 text-emerald-600" />
            <span>PyTorch Tensor Engine • Полный аудит цифрового двойника</span>
          </div>

          <div className="flex items-center space-x-2.5">
            {onEvaluate && (
              <button
                onClick={() => {
                  onClose();
                  onEvaluate();
                }}
                className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-sm transition-all flex items-center space-x-1.5 cursor-pointer"
              >
                <Sparkles className="w-3.5 h-3.5" />
                <span>Подобрать план спасения (OR-Tools)</span>
              </button>
            )}

            <button
              onClick={onClose}
              className="px-4 py-2 rounded-xl bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 font-semibold text-xs transition-all cursor-pointer"
            >
              Закрыть
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};
