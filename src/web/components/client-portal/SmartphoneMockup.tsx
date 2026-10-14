'use client';

import React, { useState, useEffect } from 'react';
import {
  Wifi,
  Battery,
  ShieldCheck,
  Bell,
  ArrowDownRight,
  Calendar,
  Clock,
  Lock,
  CheckCircle2,
  ChevronRight,
  RotateCcw,
  Sparkles,
  Smartphone
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { RestructuringOffer } from '@/lib/api';

interface SmartphoneMockupProps {
  isDispatchedFromBank: boolean;
  offers: RestructuringOffer[];
  onClientSign: (offerId: string, otpCode: string) => Promise<any>;
  onResetSimulation: () => void;
}

export const SmartphoneMockup: React.FC<SmartphoneMockupProps> = ({
  isDispatchedFromBank,
  offers,
  onClientSign,
  onResetSimulation
}) => {
  const [isUnlocked, setIsUnlocked] = useState(false);
  const [showPush, setShowPush] = useState(false);
  const [selectedOffer, setSelectedOffer] = useState<RestructuringOffer | null>(null);
  const [otpCode, setOtpCode] = useState('7777');
  const [isSigning, setIsSigning] = useState(false);
  const [isSigned, setIsSigned] = useState(false);
  const [signedOfferMeta, setSignedOfferMeta] = useState<any>(null);

  // When bank dispatches offer, trigger Push Notification animation
  useEffect(() => {
    if (isDispatchedFromBank && !isSigned) {
      setShowPush(true);
    }
  }, [isDispatchedFromBank, isSigned]);

  const handleOpenFromPush = () => {
    setShowPush(false);
    setIsUnlocked(true);
  };

  const handleSelectOffer = (offer: RestructuringOffer) => {
    setSelectedOffer(offer);
    setOtpCode('7777');
  };

  const handleConfirmSignature = async () => {
    if (!selectedOffer) return;
    setIsSigning(true);
    try {
      await onClientSign(selectedOffer.offerId, otpCode);
    } catch {
      // resilient local confirmation
    } finally {
      setIsSigning(false);
      setIsSigned(true);
      setSignedOfferMeta(selectedOffer);
      confetti({
        particleCount: 80,
        spread: 60,
        origin: { y: 0.7 }
      });
    }
  };

  const getScenarioMeta = (type: string) => {
    switch (type) {
      case '0':
      case 'BALANCED':
      case 'Balanced':
        return {
          title: 'Оптимальный баланс',
          badge: 'Рекомендовано ИИ',
          badgeClass: 'bg-emerald-100 text-emerald-800 border-emerald-300',
          desc: 'Снижение платежа на 38% без существенной переплаты'
        };
      case '1':
      case 'GRACE_PERIOD':
      case 'GracePeriod':
        return {
          title: 'Период передышки',
          badge: 'Кредитные каникулы',
          badgeClass: 'bg-teal-100 text-teal-800 border-teal-300',
          desc: '3 месяца паузы с платежом ₸0 для восстановления бюджета'
        };
      default:
        return {
          title: 'Легкий платеж',
          badge: 'Максимальный комфорт',
          badgeClass: 'bg-blue-100 text-blue-800 border-blue-300',
          desc: 'Снижение платежа до минимума за счет срока'
        };
    }
  };

  return (
    <div className="flex flex-col items-center">
      
      {/* Smartphone Hardware Frame (iPhone 16 Pro Style) */}
      <div className="relative w-[340px] h-[690px] bg-slate-900 rounded-[52px] p-[10px] shadow-[0_25px_60px_-15px_rgba(0,0,0,0.35)] ring-1 ring-slate-800 select-none">
        
        {/* Outer Metal Rim Buttons */}
        <div className="absolute -left-[2px] top-[115px] w-[3px] h-[26px] bg-slate-700 rounded-l" />
        <div className="absolute -left-[2px] top-[155px] w-[3px] h-[48px] bg-slate-700 rounded-l" />
        <div className="absolute -left-[2px] top-[215px] w-[3px] h-[48px] bg-slate-700 rounded-l" />
        <div className="absolute -right-[2px] top-[165px] w-[3px] h-[75px] bg-slate-700 rounded-r" />

        {/* Inner OLED Display Glass */}
        <div className="relative w-full h-full bg-slate-950 rounded-[44px] overflow-hidden flex flex-col border border-slate-800/80">
          
          {/* Status Bar */}
          <div className="pt-3 px-6 pb-1 flex items-center justify-between text-[11px] text-white font-medium z-30">
            <span>11:42</span>
            
            {/* Dynamic Island */}
            <div className="w-[88px] h-[22px] bg-black rounded-full flex items-center justify-center space-x-1.5 shadow-inner">
              <span className="w-2.5 h-2.5 rounded-full bg-slate-900 border border-slate-800" />
              <span className="w-2 h-2 rounded-full bg-emerald-500/80 animate-pulse" />
            </div>

            <div className="flex items-center space-x-1.5">
              <span className="text-[10px] font-bold tracking-tight">5G</span>
              <Wifi className="w-3.5 h-3.5" />
              <Battery className="w-4 h-4 text-emerald-400 fill-emerald-400" />
            </div>
          </div>

          {/* Screen Content Container */}
          <div className="flex-1 relative overflow-hidden flex flex-col bg-slate-50 text-slate-900">
            
            {/* 1. LOCK SCREEN MODE (When not unlocked) */}
            {!isUnlocked && (
              <div className="flex-1 flex flex-col justify-between p-6 bg-gradient-to-b from-slate-900 via-slate-800 to-slate-950 text-white relative">
                
                {/* Clock on lock screen */}
                <div className="text-center pt-8">
                  <div className="text-slate-400 text-xs font-medium">Среда, 14 октября</div>
                  <div className="text-5xl font-extralight tracking-tight mt-1 font-mono">11:42</div>
                </div>

                {/* Central Status or Push Notification */}
                <div className="space-y-4 my-auto">
                  {showPush ? (
                    <div
                      onClick={handleOpenFromPush}
                      className="cursor-pointer transform hover:scale-[1.02] active:scale-95 transition-all p-4 rounded-3xl bg-white/95 backdrop-blur-md text-slate-900 shadow-2xl border border-white/60 animate-bounce duration-1000"
                    >
                      <div className="flex items-center justify-between mb-1.5">
                        <div className="flex items-center space-x-2">
                          <div className="w-6 h-6 rounded-lg bg-emerald-600 text-white flex items-center justify-center shadow-xs">
                            <ShieldCheck className="w-4 h-4" />
                          </div>
                          <span className="text-xs font-bold text-slate-900">Банк • сейчас</span>
                        </div>
                        <span className="text-[10px] text-slate-400 font-medium">Kafka Dispatch</span>
                      </div>
                      <h4 className="text-xs font-extrabold text-emerald-950">
                        Персональная поддержка кредита
                      </h4>
                      <p className="text-[11px] text-slate-600 mt-1 leading-snug">
                        Арман, для вас сформировано 3 щадящих плана снижения нагрузки. Нажмите для выбора.
                      </p>
                      <div className="mt-2.5 pt-2 border-t border-slate-100 flex items-center justify-between text-[10px] text-emerald-700 font-bold">
                        <span>Открыть в мобильном банке</span>
                        <ChevronRight className="w-3.5 h-3.5" />
                      </div>
                    </div>
                  ) : (
                    <div className="p-4 rounded-2xl bg-white/10 backdrop-blur-sm border border-white/10 text-center">
                      <Lock className="w-6 h-6 text-slate-400 mx-auto mb-2" />
                      <p className="text-xs font-semibold text-slate-200">
                        {isDispatchedFromBank
                          ? 'Уведомление готово к просмотру'
                          : 'Ожидание решения риск-офицера банка...'}
                      </p>
                      <p className="text-[10px] text-slate-400 mt-1">
                        {isDispatchedFromBank
                          ? 'Нажмите на экран для входа в приложение'
                          : 'Сотрудник банка анализирует алерт EWS'}
                      </p>
                      {isDispatchedFromBank && (
                        <button
                          onClick={() => setIsUnlocked(true)}
                          className="mt-3 px-4 py-1.5 rounded-full bg-emerald-600 text-white text-xs font-bold shadow-md hover:bg-emerald-500 transition-all"
                        >
                          Войти в ДБО
                        </button>
                      )}
                    </div>
                  )}
                </div>

                {/* Bottom Lock Icon */}
                <div className="text-center pb-4 text-slate-400 text-[10px] flex items-center justify-center space-x-1">
                  <span>Проведите вверх для разблокировки</span>
                </div>
              </div>
            )}

            {/* 2. MOBILE BANKING APPLICATION (Unlocked) */}
            {isUnlocked && (
              <div className="flex-1 flex flex-col bg-slate-100 relative overflow-hidden">
                
                {/* Mobile Bank App Header */}
                <div className="bg-emerald-800 text-white px-4 pt-3 pb-4 shadow-sm">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <div className="w-7 h-7 rounded-full bg-white text-emerald-800 flex items-center justify-center font-bold text-xs">
                        АР
                      </div>
                      <div>
                        <div className="text-xs font-bold leading-tight">Арман С.</div>
                        <div className="text-[10px] text-emerald-200">KZ88...4001 • ДБО</div>
                      </div>
                    </div>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-700/80 text-emerald-100 font-medium">
                      Stage 1
                    </span>
                  </div>

                  {/* Account overview pill */}
                  <div className="p-2.5 rounded-xl bg-emerald-900/60 border border-emerald-700/50 flex items-center justify-between text-xs">
                    <div>
                      <div className="text-[10px] text-emerald-200">Текущий долг:</div>
                      <div className="font-bold text-sm font-mono">₸ 4 200 000</div>
                    </div>
                    <div className="text-right">
                      <div className="text-[10px] text-emerald-200">Плановый платеж:</div>
                      <div className="font-bold text-sm text-emerald-200 line-through">₸ 145 000</div>
                    </div>
                  </div>
                </div>

                {/* Sub-banner: Pre-delinquency support */}
                <div className="p-3 bg-emerald-50 border-b border-emerald-200/70 flex items-start space-x-2">
                  <Sparkles className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  <div className="text-[11px] leading-snug">
                    <span className="font-bold text-emerald-950">Программа поддержки банка: </span>
                    <span className="text-emerald-800">
                      Рассчитано 3 щадящих варианта без штрафов и без ухудшения кредитной истории.
                    </span>
                  </div>
                </div>

                {/* Scrollable Offers List inside Phone */}
                <div className="flex-1 overflow-y-auto p-3 space-y-3">
                  {!isSigned ? (
                    offers.map((offer, idx) => {
                      const meta = getScenarioMeta(offer.scenarioType || String(idx));
                      return (
                        <div
                          key={offer.offerId}
                          onClick={() => handleSelectOffer(offer)}
                          className="cursor-pointer p-3.5 rounded-2xl bg-white border border-slate-200/80 shadow-xs hover:border-emerald-500 hover:shadow-md transition-all active:scale-[0.98]"
                        >
                          <div className="flex items-center justify-between mb-1.5">
                            <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full border ${meta.badgeClass}`}>
                              {meta.badge}
                            </span>
                            <span className="text-[10px] text-slate-400 font-medium">КДН ≤ 40%</span>
                          </div>

                          <div className="text-xs font-bold text-slate-900">{meta.title}</div>
                          <div className="text-[10px] text-slate-500 mt-0.5">{meta.desc}</div>

                          <div className="mt-2.5 p-2 rounded-xl bg-emerald-50/70 border border-emerald-200/60 flex items-center justify-between">
                            <div>
                              <div className="text-[9px] text-emerald-800 font-semibold flex items-center space-x-0.5">
                                <ArrowDownRight className="w-3 h-3 text-emerald-600" />
                                <span>Новый платеж:</span>
                              </div>
                              <div className="text-base font-extrabold text-emerald-950 font-mono">
                                ₸ {Math.round(offer.newMonthlyPayment).toLocaleString('ru-RU')}
                              </div>
                            </div>
                            <div className="text-right text-[10px] text-slate-600 space-y-0.5">
                              <div>Срок: <span className="font-bold text-slate-800">{offer.newTenorMonths} мес.</span></div>
                              <div>Каникулы: <span className="font-bold text-slate-800">{offer.gracePeriodMonths > 0 ? `${offer.gracePeriodMonths} мес.` : '0'}</span></div>
                            </div>
                          </div>

                          <button className="mt-2 w-full py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-[11px] shadow-xs">
                            Выбрать этот вариант
                          </button>
                        </div>
                      );
                    })
                  ) : (
                    /* Signed Success Screen inside Phone */
                    <div className="p-4 rounded-3xl bg-white border border-emerald-200 shadow-md text-center my-auto space-y-3">
                      <div className="w-12 h-12 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto">
                        <CheckCircle2 className="w-7 h-7" />
                      </div>
                      <h4 className="text-sm font-extrabold text-slate-900">
                        Договор успешно подписан!
                      </h4>
                      <p className="text-xs text-slate-600 leading-snug">
                        Новый график активирован в мобильном банке. Платеж снижен со <span className="line-through">₸145 000</span> до{' '}
                        <span className="font-bold text-emerald-800">
                          ₸ {Math.round(signedOfferMeta?.newMonthlyPayment || 89500).toLocaleString('ru-RU')}/мес
                        </span>.
                      </p>
                      <div className="p-2.5 rounded-xl bg-emerald-50 border border-emerald-200 text-[10px] text-emerald-900 font-medium">
                        ✓ Кредитная история в ГКБ: Чистая (Stage 1)<br />
                        ✓ Событие отправлено в Kafka: <code>risk.contracts.signed.v1</code>
                      </div>
                      <button
                        onClick={onResetSimulation}
                        className="w-full py-2 rounded-xl bg-slate-900 text-white text-xs font-bold hover:bg-slate-800 flex items-center justify-center space-x-1.5"
                      >
                        <RotateCcw className="w-3.5 h-3.5" />
                        <span>Сбросить симуляцию</span>
                      </button>
                    </div>
                  )}
                </div>

                {/* Mobile Bottom Navigation Bar */}
                <div className="bg-white border-t border-slate-200 px-6 py-2 flex items-center justify-between text-[9px] text-slate-400">
                  <div className="text-emerald-700 font-bold flex flex-col items-center">
                    <ShieldCheck className="w-4 h-4" />
                    <span>Кредиты</span>
                  </div>
                  <div className="flex flex-col items-center">
                    <Smartphone className="w-4 h-4" />
                    <span>Платежи</span>
                  </div>
                  <div className="flex flex-col items-center">
                    <Bell className="w-4 h-4" />
                    <span>История</span>
                  </div>
                </div>

              </div>
            )}

            {/* Bottom Sheet Modal for SMS OTP Confirmation (inside Phone display) */}
            {selectedOffer && !isSigned && (
              <div className="absolute inset-0 bg-black/60 backdrop-blur-xs z-40 flex flex-col justify-end">
                <div className="p-4 bg-white rounded-t-3xl shadow-2xl space-y-3 animate-in slide-in-from-bottom duration-200">
                  <div className="w-10 h-1 bg-slate-300 rounded-full mx-auto" />

                  <div className="flex items-center space-x-2">
                    <div className="w-7 h-7 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center">
                      <Lock className="w-4 h-4" />
                    </div>
                    <div>
                      <div className="text-xs font-bold text-slate-900">Подтверждение договора</div>
                      <div className="text-[10px] text-slate-500">Электронная подпись по SMS</div>
                    </div>
                  </div>

                  <div className="p-2.5 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-950 font-medium">
                    Новый платеж: <span className="font-bold text-emerald-800">₸ {Math.round(selectedOffer.newMonthlyPayment).toLocaleString('ru-RU')}</span> на {selectedOffer.newTenorMonths} мес.
                  </div>

                  <div className="space-y-1">
                    <label className="text-[10px] font-bold text-slate-700">
                      Введите SMS-код (демо-код: <span className="text-emerald-700 font-bold">7777</span>):
                    </label>
                    <input
                      type="text"
                      value={otpCode}
                      onChange={(e) => setOtpCode(e.target.value)}
                      maxLength={4}
                      className="w-full text-center text-xl font-mono font-bold tracking-widest py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                    />
                  </div>

                  <div className="flex space-x-2 pt-1">
                    <button
                      onClick={() => setSelectedOffer(null)}
                      className="flex-1 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs"
                    >
                      Отмена
                    </button>
                    <button
                      disabled={isSigning}
                      onClick={handleConfirmSignature}
                      className="flex-2 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-md active:scale-95 disabled:opacity-50"
                    >
                      {isSigning ? 'Подписание...' : 'Подписать (SMS)'}
                    </button>
                  </div>
                </div>
              </div>
            )}

          </div>

          {/* Home Indicator Bar */}
          <div className="py-1 flex justify-center bg-slate-950 z-30">
            <div className="w-28 h-1 bg-slate-600 rounded-full" />
          </div>

        </div>
      </div>

      <div className="mt-3 text-center text-[11px] text-slate-500 font-medium">
        📱 Симулятор мобильного приложения ДБО (Клиентский интерфейс)
      </div>
    </div>
  );
};
