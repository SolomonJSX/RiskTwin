'use client';

import React, { useState } from 'react';
import { useOffers } from '@/hooks/useRiskTwin';
import { RestructuringOffer } from '@/lib/api';
import confetti from 'canvas-confetti';
import { Sparkles, Calendar, ArrowDownRight, ShieldCheck, CheckCircle2, Clock, X, Lock } from 'lucide-react';

interface ClientOffersViewProps {
  loanId: string | null;
  onSignOffer: (offerId: string, otpCode: string) => Promise<any>;
}

export const ClientOffersView: React.FC<ClientOffersViewProps> = ({
  loanId,
  onSignOffer,
}) => {
  const currentLoanId = loanId || 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee';
  const { data: offers = [], isLoading, refetch } = useOffers(currentLoanId);

  const [selectedOffer, setSelectedOffer] = useState<RestructuringOffer | null>(null);
  const [otpCode, setOtpCode] = useState('');
  const [isSigning, setIsSigning] = useState(false);
  const [signSuccess, setSignSuccess] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  // Запуск конфетти при успешном подписании
  const triggerConfetti = () => {
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 },
      colors: ['#10B981', '#059669', '#34D399', '#6EE7B7'],
    });
  };

  const handleConfirmSign = async () => {
    if (!selectedOffer) return;
    setIsSigning(true);
    setErrorMsg('');

    try {
      await onSignOffer(selectedOffer.offerId, otpCode || '7777');
      setSignSuccess(true);
      triggerConfetti();
      refetch();
    } catch (err: any) {
      setErrorMsg('Неверный код подтверждения (для теста введите 7777)');
    } finally {
      setIsSigning(false);
    }
  };

  const getScenarioTitle = (type: string) => {
    switch (type) {
      case '0':
      case 'BALANCED':
      case 'Balanced':
        return {
          title: 'Оптимальный баланс',
          badge: 'Рекомендовано ИИ',
          badgeColor: 'bg-emerald-100 text-emerald-800 border-emerald-300',
          desc: 'Сбалансированное снижение платежа с минимальной переплатой',
        };
      case '1':
      case 'GRACE_PERIOD':
      case 'GracePeriod':
        return {
          title: 'Период передышки',
          badge: 'Кредитные каникулы',
          badgeColor: 'bg-teal-100 text-teal-800 border-teal-300',
          desc: 'Временная пауза для восстановления семейного бюджета',
        };
      default:
        return {
          title: 'Легкий платеж',
          badge: 'Максимальный комфорт',
          badgeColor: 'bg-blue-100 text-blue-800 border-blue-300',
          desc: 'Снижение ежемесячного взноса до минимума за счет срока',
        };
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Баннер заботы о клиенте */}
      <div className="glass-card rounded-2xl p-6 bg-gradient-to-r from-emerald-900 via-emerald-800 to-teal-800 text-white shadow-lg">
        <div className="max-w-2xl">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-400/20 text-emerald-200 text-xs font-semibold mb-3 border border-emerald-400/30">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Персональная программа поддержки</span>
          </div>
          <h2 className="text-2xl font-bold tracking-tight">
            Выберите комфортный вариант оплаты кредита
          </h2>
          <p className="text-emerald-100/90 text-sm mt-2">
            Система заранее рассчитала 3 щадящих сценария без штрафов и без влияния на вашу кредитную историю.
          </p>
        </div>
      </div>

      {isLoading ? (
        <div className="glass-card rounded-2xl p-12 text-center text-slate-500">
          <div className="w-8 h-8 border-2 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <p>ИИ формирует персональные варианты...</p>
        </div>
      ) : offers.length === 0 ? (
        <div className="glass-card rounded-2xl p-12 text-center bg-white">
          <ShieldCheck className="w-12 h-12 text-emerald-600 mx-auto mb-3" />
          <h3 className="text-base font-bold text-slate-800">Кредит стабилен</h3>
          <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
            Для этого договора еще не сформированы специальные планы, либо предыдущий план уже активен. Запустите стресс-тест или оценку ИИ на вкладке «Радар».
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {offers.map((offer, idx) => {
            const meta = getScenarioTitle(offer.scenarioType || String(idx));
            const isSigned = offer.status === 'Signed' || offer.status === 'ACCEPTED';

            return (
              <div
                key={offer.offerId}
                className="glass-card glass-card-hover rounded-2xl p-6 bg-white border border-emerald-500/20 flex flex-col justify-between relative overflow-hidden"
              >
                <div>
                  {/* Бейдж сценария */}
                  <div className="flex items-center justify-between mb-3">
                    <span className={`text-[11px] font-semibold px-2.5 py-1 rounded-full border ${meta.badgeColor}`}>
                      {meta.badge}
                    </span>
                    {isSigned && (
                      <span className="text-xs font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded-full flex items-center space-x-1">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>Подписан</span>
                      </span>
                    )}
                  </div>

                  <h3 className="text-lg font-bold text-slate-800">{meta.title}</h3>
                  <p className="text-xs text-slate-500 mt-1 mb-6">{meta.desc}</p>

                  {/* Ключевые параметры на понятном языке */}
                  <div className="space-y-4">
                    <div className="p-3.5 rounded-xl bg-emerald-50/60 border border-emerald-200/50">
                      <span className="text-xs text-slate-500 flex items-center space-x-1">
                        <ArrowDownRight className="w-3.5 h-3.5 text-emerald-600" />
                        <span>Новый ежемесячный платеж:</span>
                      </span>
                      <div className="text-2xl font-extrabold text-emerald-900 mt-1">
                        ₸ {Math.round(offer.newMonthlyPayment).toLocaleString('ru-RU')}
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                        <div className="text-slate-400 flex items-center space-x-1">
                          <Calendar className="w-3 h-3" />
                          <span>Срок:</span>
                        </div>
                        <div className="font-semibold text-slate-700 mt-0.5">
                          {offer.newTenorMonths} мес.
                        </div>
                      </div>

                      <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                        <div className="text-slate-400 flex items-center space-x-1">
                          <Clock className="w-3 h-3" />
                          <span>Каникулы:</span>
                        </div>
                        <div className="font-semibold text-slate-700 mt-0.5">
                          {offer.gracePeriodMonths > 0 ? `${offer.gracePeriodMonths} мес.` : 'Без каникул'}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Кнопка подписания */}
                <div className="mt-6 pt-4 border-t border-slate-100">
                  <button
                    disabled={isSigned}
                    onClick={() => {
                      setSelectedOffer(offer);
                      setOtpCode('7777');
                      setSignSuccess(false);
                      setErrorMsg('');
                    }}
                    className={`w-full py-2.5 rounded-xl font-semibold text-xs transition-all shadow-sm ${
                      isSigned
                        ? 'bg-slate-100 text-slate-400 cursor-not-allowed'
                        : 'bg-emerald-600 hover:bg-emerald-700 text-white active:scale-95'
                    }`}
                  >
                    {isSigned ? 'Договор активирован' : 'Выбрать этот вариант'}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Модальное окно безопасного SMS OTP подтверждения */}
      {selectedOffer && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="glass-card rounded-2xl max-w-md w-full p-6 bg-white border border-emerald-500/20 shadow-2xl relative">
            <button
              onClick={() => setSelectedOffer(null)}
              className="absolute top-4 right-4 text-slate-400 hover:text-slate-600 p-1"
            >
              <X className="w-5 h-5" />
            </button>

            {!signSuccess ? (
              <div>
                <div className="flex items-center space-x-3 mb-4">
                  <div className="p-2.5 rounded-xl bg-emerald-100 text-emerald-800">
                    <Lock className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-base font-bold text-slate-800">
                      Подтверждение соглашения
                    </h3>
                    <p className="text-xs text-slate-500">
                      Безопасное подписание по коду из SMS
                    </p>
                  </div>
                </div>

                <div className="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 mb-4 text-xs text-emerald-900">
                  Новый ежемесячный платеж составит:{' '}
                  <span className="font-bold">
                    ₸ {Math.round(selectedOffer.newMonthlyPayment).toLocaleString('ru-RU')}
                  </span>
                </div>

                <div className="space-y-2 mb-4">
                  <label className="text-xs font-semibold text-slate-700">
                    Введите SMS-код (тестовый код: <span className="text-emerald-700 font-bold">7777</span>)
                  </label>
                  <input
                    type="text"
                    value={otpCode}
                    onChange={(e) => setOtpCode(e.target.value)}
                    placeholder="7777"
                    maxLength={4}
                    className="w-full text-center tracking-widest text-2xl font-mono py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 font-bold text-slate-800"
                  />
                  {errorMsg && (
                    <p className="text-xs text-rose-600 mt-1">{errorMsg}</p>
                  )}
                </div>

                <button
                  disabled={isSigning}
                  onClick={handleConfirmSign}
                  className="w-full py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs shadow-md transition-all active:scale-95 disabled:opacity-50"
                >
                  {isSigning ? 'Подписание...' : 'Подтвердить и обновить график'}
                </button>
              </div>
            ) : (
              <div className="text-center py-4">
                <div className="w-12 h-12 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto mb-3">
                  <CheckCircle2 className="w-7 h-7" />
                </div>
                <h3 className="text-base font-bold text-slate-800">
                  Соглашение успешно подписано!
                </h3>
                <p className="text-xs text-slate-500 mt-2">
                  График платежей мгновенно обновлен. Данные зарегистрированы в системе финансовой стабильности.
                </p>
                <button
                  onClick={() => setSelectedOffer(null)}
                  className="mt-6 w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-900 text-white text-xs font-semibold"
                >
                  Закрыть
                </button>
              </div>
            )}
          </div>
        </div>
      )}

    </div>
  );
};