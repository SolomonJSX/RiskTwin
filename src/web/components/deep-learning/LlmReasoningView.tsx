'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Brain, 
  Sparkles, 
  Cpu, 
  TrendingUp, 
  TrendingDown, 
  ShieldCheck, 
  FileText, 
  Copy, 
  Check, 
  RefreshCw, 
  Languages, 
  AlertCircle 
} from 'lucide-react';
import { AttentionToken } from './DeepLearningExplainer';

interface LlmReasoningViewProps {
  name: string;
  role: string;
  accountNumber: string;
  riskProbability: number;
  tokens: AttentionToken[];
  passport360?: Record<string, any>;
}

interface ReasoningResult {
  modelUsed: string;
  latencyMs: number;
  fullText: string;
  sections: {
    learned: string;
    why: string;
    counterfactual: string;
  };
}

export const LlmReasoningView: React.FC<LlmReasoningViewProps> = ({
  name,
  role,
  accountNumber,
  riskProbability,
  tokens,
  passport360,
}) => {
  const [language, setLanguage] = useState<'ru' | 'kz'>('ru');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ReasoningResult | null>(null);
  const [copied, setCopied] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/llm-reasoning', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name,
          role,
          accountNumber,
          riskProbability,
          tokens,
          passport360,
          language,
        }),
      });

      if (!res.ok) {
        throw new Error('Ошибка генерации');
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error('Failed to generate LLM reasoning:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (!result) return;
    const textToCopy = `[RiskTwin XAI Вердикт: ${name} (${accountNumber})]\nМодель: ${result.modelUsed}\n\n1. Чему обучилась сеть:\n${result.sections.learned}\n\n2. Почему изменился риск:\n${result.sections.why}\n\n3. Контрфактический план:\n${result.sections.counterfactual}`;
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const isHighRisk = riskProbability > 50;

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm space-y-6">
      {/* Шапка компонента */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-100 pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-emerald-50 text-emerald-700 rounded-lg border border-emerald-100">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-base font-bold text-slate-900">
                LLM Neuro-Symbolic Вердикт Модели
              </h3>
              <span className="text-[11px] font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200 flex items-center gap-1">
                <Cpu className="w-3 h-3 text-emerald-600" />
                Ollama: mistral-nemo:12b
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Синтез математических весов Cross-Attention PyTorch в объяснимый аналитический отчет
            </p>
          </div>
        </div>

        {/* Переключатель языка и кнопка генерации */}
        <div className="flex items-center gap-2 self-start sm:self-auto">
          <div className="flex items-center bg-slate-100 p-0.5 rounded-lg border border-slate-200 text-xs">
            <button
              onClick={() => setLanguage('ru')}
              className={`px-2.5 py-1 rounded-md font-medium transition-colors ${
                language === 'ru'
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-500 hover:text-slate-900'
              }`}
            >
              RU
            </button>
            <button
              onClick={() => setLanguage('kz')}
              className={`px-2.5 py-1 rounded-md font-medium transition-colors ${
                language === 'kz'
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-500 hover:text-slate-900'
              }`}
            >
              KZ
            </button>
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-semibold shadow-sm transition-all disabled:opacity-50"
          >
            {loading ? (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                <span>Генерация вердикта...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-3.5 h-3.5" />
                <span>Запустить анализ LLM</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Индикатор 360° Кредитного паспорта заемщика */}
      {passport360 && (
        <div className="flex flex-wrap items-center gap-2 px-3.5 py-2 bg-emerald-50/80 border border-emerald-200 rounded-xl text-xs text-emerald-950 shadow-2xs">
          <ShieldCheck className="w-4 h-4 text-emerald-700 shrink-0" />
          <span className="font-bold text-emerald-900">360° Кредитный паспорт (Home Credit):</span>
          <span className="bg-white px-2 py-0.5 rounded-md border border-emerald-200 text-emerald-800 font-mono text-[11px] font-semibold">DTI: {(passport360.dti_ratio * 100).toFixed(1)}%</span>
          <span className="bg-white px-2 py-0.5 rounded-md border border-emerald-200 text-emerald-800 font-mono text-[11px] font-semibold">Опережение: {Math.abs(passport360.inst_avg_delay_days || 5.4)} дн.</span>
          <span className="bg-white px-2 py-0.5 rounded-md border border-emerald-200 text-emerald-800 font-mono text-[11px] font-semibold">Отказы: {passport360.prev_refused_count || 0}</span>
          <span className="bg-white px-2 py-0.5 rounded-md border border-emerald-200 text-emerald-800 font-mono text-[11px] font-semibold">Долги ПКБ: 0 ₸</span>
          <span className="bg-white px-2 py-0.5 rounded-md border border-emerald-200 text-emerald-800 font-mono text-[11px] font-semibold">Класс: {passport360.ext_source || '0.88 (AAA)'}</span>
        </div>
      )}

      {/* Состояние: еще не запущено */}
      {!result && !loading && (
        <div className="bg-slate-50 border border-dashed border-slate-200 rounded-xl p-8 text-center space-y-3">
          <div className="w-12 h-12 mx-auto rounded-full bg-white border border-slate-200 flex items-center justify-center text-emerald-600 shadow-sm">
            <Brain className="w-6 h-6" />
          </div>
          <div className="max-w-md mx-auto">
            <h4 className="text-sm font-semibold text-slate-800">
              Готов к генерации мотивированного заключения
            </h4>
            <p className="text-xs text-slate-500 mt-1">
              Нажмите кнопку выше, чтобы локальная модель <code className="text-emerald-700 font-mono">mistral-nemo:12b</code> через Ollama проанализировала веса внимания <span className="font-mono text-slate-700">α</span> и сформировала вердикт для заемщика <strong className="text-slate-800">{name}</strong>.
            </p>
          </div>
        </div>
      )}

      {/* Индикатор загрузки */}
      {loading && (
        <div className="py-12 flex flex-col items-center justify-center space-y-4">
          <div className="relative">
            <div className="w-12 h-12 rounded-full border-2 border-emerald-200 border-t-emerald-600 animate-spin" />
            <Brain className="w-5 h-5 text-emerald-600 absolute inset-0 m-auto" />
          </div>
          <div className="text-center">
            <p className="text-xs font-semibold text-slate-800">
              Локальная модель Ollama анализирует матрицу внимания PyTorch...
            </p>
            <p className="text-[11px] text-slate-500 mt-0.5">
              Извлечение скрытых связей между 16 признаками Feature Store
            </p>
          </div>
        </div>
      )}

      {/* Результат генерации */}
      {result && !loading && (
        <AnimatePresence mode="wait">
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-4"
          >
            {/* Статус-панель инференса */}
            <div className="flex items-center justify-between text-[11px] bg-slate-50 px-3.5 py-2 rounded-lg border border-slate-200 text-slate-600">
              <div className="flex items-center gap-3">
                <span>Движок: <strong className="text-slate-800">{result.modelUsed}</strong></span>
                <span>•</span>
                <span>Время вывода: <strong className="text-emerald-700 font-mono">{result.latencyMs} мс</strong></span>
                <span>•</span>
                <span>Заемщик: <strong className="text-slate-800">{name}</strong></span>
              </div>
              <button
                onClick={handleCopy}
                className="flex items-center gap-1 text-slate-700 hover:text-emerald-700 font-medium transition-colors"
              >
                {copied ? (
                  <>
                    <Check className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Скопировано!</span>
                  </>
                ) : (
                  <>
                    <Copy className="w-3.5 h-3.5" />
                    <span>Копировать отчет</span>
                  </>
                )}
              </button>
            </div>

            {/* Карточка 1: Чему обучилась сеть */}
            <div className="p-4 rounded-xl border border-blue-100 bg-blue-50/40 space-y-2">
              <div className="flex items-center gap-2">
                <span className="w-6 h-6 rounded-md bg-blue-100 text-blue-700 text-xs font-bold flex items-center justify-center">
                  1
                </span>
                <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wide">
                  {language === 'kz' ? 'Желі нені үйренді (Жасырын паттерн)' : 'Чему обучилась нейросеть (Выявленный скрытый паттерн)'}
                </h4>
              </div>
              <p className="text-xs text-slate-700 leading-relaxed pl-8">
                {result.sections.learned}
              </p>
            </div>

            {/* Карточка 2: Почему изменился риск */}
            <div className={`p-4 rounded-xl border space-y-2 ${
              isHighRisk 
                ? 'border-amber-200 bg-amber-50/40' 
                : 'border-emerald-200 bg-emerald-50/40'
            }`}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className={`w-6 h-6 rounded-md text-xs font-bold flex items-center justify-center ${
                    isHighRisk ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'
                  }`}>
                    2
                  </span>
                  <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wide">
                    {language === 'kz' ? 'Тәуекел неліктен өзгерді (Басты триггерлер)' : 'Почему изменился риск (Драйверы и веса внимания α)'}
                  </h4>
                </div>
                <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full ${
                  isHighRisk ? 'bg-rose-100 text-rose-800' : 'bg-emerald-100 text-emerald-800'
                }`}>
                  PD: {riskProbability}%
                </span>
              </div>
              <p className="text-xs text-slate-700 leading-relaxed pl-8">
                {result.sections.why}
              </p>
            </div>

            {/* Карточка 3: Контрфактический план */}
            <div className="p-4 rounded-xl border border-emerald-200 bg-emerald-50/40 space-y-2">
              <div className="flex items-center gap-2">
                <span className="w-6 h-6 rounded-md bg-emerald-100 text-emerald-800 text-xs font-bold flex items-center justify-center">
                  3
                </span>
                <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wide">
                  {language === 'kz' ? 'Контрфактикалық жоспар (Тәуекелді төмендету)' : 'Контрфактический прогноз (Что снизит вероятность дефолта)'}
                </h4>
              </div>
              <p className="text-xs text-slate-700 leading-relaxed pl-8">
                {result.sections.counterfactual}
              </p>
            </div>
          </motion.div>
        </AnimatePresence>
      )}
    </div>
  );
};
