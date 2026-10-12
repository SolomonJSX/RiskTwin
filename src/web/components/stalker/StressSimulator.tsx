'use client';

import React, { useState } from 'react';
import { Zap, AlertCircle, ArrowRight, CheckCircle2, ShieldAlert, Sparkles, RefreshCw } from 'lucide-react';
import { StressSimulateRequest } from '@/lib/api';

interface StressSimulatorProps {
  onSimulate: (payload: StressSimulateRequest) => Promise<any>;
  isSimulating: boolean;
  onGoToOffers: (loanId: string) => void;
}

export const StressSimulator: React.FC<StressSimulatorProps> = ({
  onSimulate,
  isSimulating,
  onGoToOffers,
}) => {
  // Тестовый токен клиента из нашего сида базы данных
  const [clientToken, setClientToken] = useState('11111111-2222-3333-4444-555555555555');
  const defaultLoanId = 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee';

  const [lastResult, setLastResult] = useState<any>(null);

  const handleRunPreset = async (eventType: string, deltaValue: number, comment: string) => {
    try {
      const res = await onSimulate({
        clientToken,
        eventType,
        deltaValue,
        comment,
      });
      setLastResult(res);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Заголовок с акцентом на предиктивную аналитику */}
      <div className="glass-card rounded-2xl p-6 bg-gradient-to-br from-white via-emerald-50/30 to-teal-50/20 border border-emerald-500/20">
        <div className="flex items-center space-x-3 mb-2">
          <div className="p-2 rounded-xl bg-emerald-600 text-white shadow-sm">
            <Zap className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-800">
              Интерактивное стресс-тестирование заемщика
            </h2>
            <p className="text-xs text-slate-500">
              Смоделируйте внезапные жизненные трудности клиента и посмотрите, как ИИ среагирует мгновенно
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Колонка с готовыми сценариями шоков */}
        <div className="lg:col-span-1 space-y-4">
          <div className="glass-card rounded-2xl p-5 border border-emerald-500/20 bg-white/90">
            <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider text-emerald-900 mb-4 flex items-center space-x-2">
              <Sparkles className="w-4 h-4 text-emerald-600" />
              <span>Выберите стресс-сценарий</span>
            </h3>

            <div className="space-y-3">
              {/* Сценарий 1: Падение дохода */}
              <button
                disabled={isSimulating}
                onClick={() =>
                  handleRunPreset(
                    'SALARY_DROP',
                    -0.4,
                    'Падение поступления заработной платы на 40% (потеря подработки)'
                  )
                }
                className="w-full text-left p-4 rounded-xl border border-emerald-500/20 bg-gradient-to-r from-emerald-50/50 to-white hover:border-emerald-500/50 hover:shadow-md transition-all group disabled:opacity-50"
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-sm text-slate-800 group-hover:text-emerald-800">
                    📉 Падение зарплаты (-40%)
                  </span>
                  <ArrowRight className="w-4 h-4 text-emerald-600 transform group-hover:translate-x-1 transition-transform" />
                </div>
                <p className="text-xs text-slate-500 mt-1">
                  У заемщика снизился ежемесячный доход, возрастает нагрузка на бюджет
                </p>
              </button>

              {/* Сценарий 2: Микрозайм */}
              <button
                disabled={isSimulating}
                onClick={() =>
                  handleRunPreset(
                    'MICROLOAN_TAKEN',
                    150000,
                    'Оформлен краткосрочный микрокредит в стороннем МФО на ₸150 000'
                  )
                }
                className="w-full text-left p-4 rounded-xl border border-amber-500/20 bg-gradient-to-r from-amber-50/40 to-white hover:border-amber-500/50 hover:shadow-md transition-all group disabled:opacity-50"
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-sm text-slate-800 group-hover:text-amber-800">
                    💳 Микрозайм на стороне (+₸150к)
                  </span>
                  <ArrowRight className="w-4 h-4 text-amber-600 transform group-hover:translate-x-1 transition-transform" />
                </div>
                <p className="text-xs text-slate-500 mt-1">
                  Паттерн кассового разрыва: клиент ищет быстрые деньги под высокий процент
                </p>
              </button>

              {/* Сценарий 3: Расходы на лечение / шок */}
              <button
                disabled={isSimulating}
                onClick={() =>
                  handleRunPreset(
                    'HIGH_EXPENSE',
                    -200000,
                    'Внезапный отток средств: оплата медицинских услуг или ремонт авто'
                  )
                }
                className="w-full text-left p-4 rounded-xl border border-rose-500/20 bg-gradient-to-r from-rose-50/40 to-white hover:border-rose-500/50 hover:shadow-md transition-all group disabled:opacity-50"
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-sm text-slate-800 group-hover:text-rose-800">
                    🏥 Непредвиденные траты (₸200к)
                  </span>
                  <ArrowRight className="w-4 h-4 text-rose-600 transform group-hover:translate-x-1 transition-transform" />
                </div>
                <p className="text-xs text-slate-500 mt-1">
                  Обнуление подушки безопасности перед датой списания кредита
                </p>
              </button>
            </div>
          </div>
        </div>

        {/* Колонка результатов реакции ИИ в реальном времени */}
        <div className="lg:col-span-2">
          <div className="glass-card rounded-2xl p-6 border border-emerald-500/20 bg-white/95 h-full flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between border-b border-emerald-500/10 pb-4 mb-4">
                <span className="text-sm font-bold text-slate-800 flex items-center space-x-2">
                  <ShieldAlert className="w-4 h-4 text-emerald-600" />
                  <span>Реакция предиктивного ядра ИИ</span>
                </span>
                {isSimulating && (
                  <span className="flex items-center space-x-2 text-xs text-emerald-700 font-medium">
                    <RefreshCw className="w-3.5 h-3.5 animate-spin text-emerald-600" />
                    <span>Анализируем риск...</span>
                  </span>
                )}
              </div>

              {!lastResult ? (
                <div className="py-16 text-center text-slate-400">
                  <div className="w-14 h-14 mx-auto mb-3 rounded-2xl bg-emerald-50 flex items-center justify-center text-emerald-600 border border-emerald-200">
                    <Zap className="w-7 h-7" />
                  </div>
                  <p className="font-medium text-slate-600">Система ожидает входящих сигналов</p>
                  <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
                    Нажмите любой сценарий слева, чтобы протестировать реакцию предиктивного алгоритма
                  </p>
                </div>
              ) : (
                <div className="space-y-4 animate-in fade-in duration-300">
                  {/* Статус обнаружения */}
                  <div className="p-4 rounded-xl bg-amber-50/80 border border-amber-300/60 flex items-start space-x-3">
                    <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <div className="text-sm font-bold text-amber-900">
                        Обнаружен скрытый риск до наступления просрочки!
                      </div>
                      <div className="text-xs text-amber-800 mt-1">
                        {lastResult.analysis?.TriggerReason || lastResult.Message || 'Зафиксировано стресс-событие в поведении клиента'}
                      </div>
                    </div>
                  </div>

                  {/* Сравнение показателей Было / Стало */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                      <div className="text-xs text-slate-500">Вероятность риска (было)</div>
                      <div className="text-xl font-bold text-slate-700 mt-1">12% (Норма)</div>
                    </div>
                    <div className="p-4 rounded-xl bg-amber-50 border border-amber-200">
                      <div className="text-xs text-amber-800">Вероятность риска (стало)</div>
                      <div className="text-xl font-bold text-amber-700 mt-1">
                        {lastResult.analysis?.NewProbability 
                          ? `${Math.round(lastResult.analysis.NewProbability * 100)}%`
                          : '68% (Критично)'}
                      </div>
                    </div>
                  </div>

                  {/* Действие ИИ */}
                  <div className="p-4 rounded-xl bg-emerald-50/70 border border-emerald-300/60 flex items-start space-x-3">
                    <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <div className="text-sm font-bold text-emerald-950">
                        Автоматически сформированы 3 щадящих плана
                      </div>
                      <div className="text-xs text-emerald-800 mt-1">
                        Математический алгоритм оптимизировал график платежей, чтобы клиент мог комфортно платить без ухудшения кредитной истории.
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Футер с переходом к витрине офферов */}
            {lastResult && (
              <div className="pt-4 border-t border-emerald-500/10 flex justify-end">
                <button
                  onClick={() => onGoToOffers(defaultLoanId)}
                  className="flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white font-medium text-xs shadow-md transition-all active:scale-95"
                >
                  <span>Посмотреть сформированные сценарии для клиента</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            )}

          </div>
        </div>

      </div>

    </div>
  );
};