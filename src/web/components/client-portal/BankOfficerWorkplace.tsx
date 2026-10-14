'use client';

import React from 'react';
import {
  ShieldAlert,
  Cpu,
  Send,
  CheckCircle2,
  AlertTriangle,
  Scale,
  Sparkles,
  User,
  ArrowDownRight,
  TrendingDown,
  Layers,
  RotateCcw
} from 'lucide-react';
import { RestructuringOffer } from '@/lib/api';

interface BankOfficerWorkplaceProps {
  offers: RestructuringOffer[];
  isDispatched: boolean;
  isSignedByClient: boolean;
  onDispatchToKafka: () => void;
  onResetSimulation: () => void;
}

export const BankOfficerWorkplace: React.FC<BankOfficerWorkplaceProps> = ({
  offers,
  isDispatched,
  isSignedByClient,
  onDispatchToKafka,
  onResetSimulation
}) => {
  return (
    <div className="space-y-6">
      
      {/* 1. Header Banner: Bank Officer Control Panel */}
      <div className="rounded-3xl p-6 bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white shadow-xl border border-slate-700/60">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold border border-emerald-500/40 mb-2">
              <Scale className="w-3.5 h-3.5" />
              <span>Контур риск-офицера • Human-in-the-Loop</span>
            </div>
            <h2 className="text-xl font-black text-white">
              Рабочее место кредитного риск-офицера
            </h2>
            <p className="text-xs text-slate-300 mt-1 max-w-xl">
              Предиктивная верификация сигналов EWS и санкционирование превентивной реструктуризации до передачи в ДБО заемщика.
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <span className="px-3 py-1.5 rounded-xl bg-slate-800 text-slate-300 text-xs font-mono border border-slate-700 flex items-center space-x-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>Kafka Producer: Ready</span>
            </span>
            {isDispatched && (
              <button
                onClick={onResetSimulation}
                className="px-3 py-1.5 rounded-xl bg-slate-700/80 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center space-x-1"
                title="Сбросить симуляцию"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Сброс</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* 2. Urgent EWS Alert Card (From Kafka Topic: risk.alerts.ews.v1) */}
      <div className="rounded-2xl p-5 bg-rose-50 border-2 border-rose-200 shadow-sm relative overflow-hidden">
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-rose-600 text-white flex items-center justify-center shadow-md">
              <ShieldAlert className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-black uppercase tracking-wider text-rose-700">
                  АЛЕРТ СИСТЕМЫ РАННЕГО ОПОВЕЩЕНИЯ (EWS)
                </span>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-rose-200 text-rose-900 font-mono font-bold">
                  Topic: risk.alerts.ews.v1
                </span>
              </div>
              <h3 className="text-base font-bold text-slate-900 mt-0.5">
                Заемщик Арман С. вошел в зону скрытого стресса
              </h3>
            </div>
          </div>

          <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-rose-100 text-rose-800 border border-rose-300">
            Импульс дефолта: 30 дней
          </span>
        </div>

        {/* Client Details Strip */}
        <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
          <div className="p-2.5 rounded-xl bg-white border border-rose-100">
            <div className="text-slate-500 font-medium text-[11px]">Кредитный договор:</div>
            <div className="font-bold text-slate-900 mt-0.5 font-mono">KZ88...4001</div>
          </div>
          <div className="p-2.5 rounded-xl bg-white border border-rose-100">
            <div className="text-slate-500 font-medium text-[11px]">Текущий долг:</div>
            <div className="font-bold text-slate-900 mt-0.5 font-mono">₸ 4 200 000</div>
          </div>
          <div className="p-2.5 rounded-xl bg-white border border-rose-100">
            <div className="text-slate-500 font-medium text-[11px]">Ежемесячный взнос:</div>
            <div className="font-bold text-slate-900 mt-0.5 font-mono">₸ 145 000</div>
          </div>
          <div className="p-2.5 rounded-xl bg-white border border-rose-100">
            <div className="text-slate-500 font-medium text-[11px]">Текущий статус МСФО:</div>
            <div className="font-bold text-emerald-700 mt-0.5 flex items-center space-x-1">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Stage 1 (Угроза Stage 2)</span>
            </div>
          </div>
        </div>

        {/* Diagnostic stress markers */}
        <div className="mt-3 flex flex-wrap items-center gap-2 text-[11px]">
          <span className="text-slate-600 font-semibold">Триггеры внимания модели:</span>
          <span className="px-2.5 py-1 rounded-lg bg-white text-rose-700 font-medium border border-rose-200">
            Задержка зарплаты: +14 дней
          </span>
          <span className="px-2.5 py-1 rounded-lg bg-white text-rose-700 font-medium border border-rose-200">
            Падение остатка подушки: -35%
          </span>
          <span className="px-2.5 py-1 rounded-lg bg-white text-rose-700 font-medium border border-rose-200">
            Аномальные ночные сессии ДБО: 4 за 7 дней
          </span>
        </div>
      </div>

      {/* 3. Decision Support: Google OR-Tools Optimization Scenarios */}
      <div className="glass-card rounded-2xl p-5 bg-white border border-slate-200 shadow-xs space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Cpu className="w-5 h-5 text-emerald-600" />
            <h3 className="text-sm font-bold text-slate-900">
              Сценарии оптимизатора Google OR-Tools (MILP)
            </h3>
          </div>
          <div className="text-xs font-semibold text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200 flex items-center space-x-1">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
            <span>Комплаенс АРРФР соблюден (КДН ≤ 40%, штрафы ₸0)</span>
          </div>
        </div>

        {/* 3 Options Table / Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {offers.map((offer, idx) => {
            const isBalanced = idx === 0 || offer.scenarioType === 'BALANCED' || offer.scenarioType === '0';
            return (
              <div
                key={offer.offerId}
                className={`p-3.5 rounded-xl border transition-all ${
                  isBalanced
                    ? 'bg-emerald-50/70 border-emerald-300 ring-1 ring-emerald-400/40'
                    : 'bg-slate-50 border-slate-200'
                }`}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-600">
                    {isBalanced ? 'Сценарий 1 (Реком.)' : idx === 1 ? 'Сценарий 2 (Каникулы)' : 'Сценарий 3 (Срок)'}
                  </span>
                  {isBalanced && (
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-200 text-emerald-900">
                      NPV 98%
                    </span>
                  )}
                </div>

                <div className="text-xs font-bold text-slate-900">
                  {isBalanced ? 'Оптимальный баланс' : idx === 1 ? 'Период передышки' : 'Легкий платеж'}
                </div>

                <div className="mt-2 text-xl font-extrabold text-emerald-950 font-mono">
                  ₸ {Math.round(offer.newMonthlyPayment).toLocaleString('ru-RU')}
                  <span className="text-xs font-normal text-slate-500"> /мес</span>
                </div>

                <div className="text-[11px] text-slate-600 mt-1 space-y-0.5">
                  <div>Срок: <strong>{offer.newTenorMonths} мес.</strong></div>
                  <div>Каникулы: <strong>{offer.gracePeriodMonths > 0 ? `${offer.gracePeriodMonths} мес.` : '0 мес.'}</strong></div>
                  <div>Расчетный КДН: <strong className="text-emerald-700">{(offer.kdnPostRestructure * 100).toFixed(1)}%</strong></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 4. Action Banner: Dispatch to Kafka */}
      <div className="rounded-2xl p-5 bg-slate-50 border border-slate-200 space-y-3">
        {!isDispatched ? (
          <div>
            <div className="flex items-center space-x-2 text-slate-900 font-bold text-sm mb-1">
              <Layers className="w-4 h-4 text-emerald-600" />
              <span>Решение риск-офицера банка</span>
            </div>
            <p className="text-xs text-slate-600 mb-4 leading-relaxed">
              Вы подтверждаете отправку сформированного пакета реструктуризации заемщику. После нажатия кнопки событие поступит в брокер Kafka (топик: <code>risk.restructuring.approved.v1</code>), а клиент получит Push-нотификацию на свой смартфон.
            </p>

            <button
              onClick={onDispatchToKafka}
              className="w-full py-3.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm shadow-md hover:shadow-lg transition-all flex items-center justify-center space-x-2 active:scale-95"
            >
              <Send className="w-4 h-4" />
              <span>Одобрить сценарии и отправить в ДБО (Kafka Dispatch)</span>
            </button>
          </div>
        ) : !isSignedByClient ? (
          <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-300 flex items-start space-x-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
            <div>
              <div className="text-xs font-bold text-emerald-950">
                Сценарии успешно одобрены риск-офицером!
              </div>
              <p className="text-[11px] text-emerald-800 mt-0.5 leading-relaxed">
                Событие опубликовано в Kafka topic <code>risk.restructuring.approved.v1</code>. На смартфоне клиента (справа) всплыло Push-уведомление. Ожидается выбор опции и ввод SMS-кода 7777 клиентом.
              </p>
            </div>
          </div>
        ) : (
          <div className="p-4 rounded-xl bg-emerald-100/80 border border-emerald-400 flex items-start space-x-3">
            <CheckCircle2 className="w-6 h-6 text-emerald-700 shrink-0 mt-0.5" />
            <div>
              <div className="text-xs font-black uppercase tracking-wider text-emerald-950">
                ДОГОВОР УСПЕШНО РЕСТРУКТУРИРОВАН И АКТИВИРОВАН
              </div>
              <p className="text-xs text-emerald-900 mt-1 leading-relaxed font-medium">
                Заемщик подписал соглашение по SMS-коду 7777. Событие зафиксировано в Kafka: <code>risk.contracts.signed.v1</code>. Кредит удержан в Stage 1 (МСФО 9), банк спас капитал от 100% провизий!
              </p>
            </div>
          </div>
        )}
      </div>

    </div>
  );
};
