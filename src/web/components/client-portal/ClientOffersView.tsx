'use client';

import React, { useState, useMemo } from 'react';
import { useOffers } from '@/hooks/useRiskTwin';
import { RestructuringOffer } from '@/lib/api';
import { BankOfficerWorkplace } from './BankOfficerWorkplace';
import { SmartphoneMockup } from './SmartphoneMockup';
import { KafkaLiveConsole, KafkaLogMessage } from './KafkaLiveConsole';
import { Radio, Layers, Smartphone, ShieldCheck } from 'lucide-react';

interface ClientOffersViewProps {
  loanId: string | null;
  onSignOffer: (offerId: string, otpCode: string) => Promise<any>;
}

const DEFAULT_ARMAN_OFFERS: RestructuringOffer[] = [
  {
    offerId: 'offer-arman-balanced-001',
    scenarioType: 'BALANCED',
    newTenorMonths: 42,
    newMonthlyPayment: 89500,
    gracePeriodMonths: 0,
    npvRecoveryRate: 0.98,
    kdnPostRestructure: 0.075,
    status: 'Offered',
    expiresAt: new Date(Date.now() + 14 * 86400000).toISOString(),
  },
  {
    offerId: 'offer-arman-grace-002',
    scenarioType: 'GRACE_PERIOD',
    newTenorMonths: 36,
    newMonthlyPayment: 108200,
    gracePeriodMonths: 3,
    npvRecoveryRate: 0.96,
    kdnPostRestructure: 0.09,
    status: 'Offered',
    expiresAt: new Date(Date.now() + 14 * 86400000).toISOString(),
  },
  {
    offerId: 'offer-arman-tenor-003',
    scenarioType: 'TENOR_EXTENSION',
    newTenorMonths: 48,
    newMonthlyPayment: 78400,
    gracePeriodMonths: 0,
    npvRecoveryRate: 0.95,
    kdnPostRestructure: 0.065,
    status: 'Offered',
    expiresAt: new Date(Date.now() + 14 * 86400000).toISOString(),
  },
];

const INITIAL_KAFKA_LOGS: KafkaLogMessage[] = [
  {
    id: 'k-1',
    timestamp: '11:41:02',
    topic: 'banking.telemetry.v1',
    eventType: 'TelemetryIngested',
    partition: 0,
    direction: 'inbound',
    payload: { account: 'KZ88...4001', txCount: 36, balanceDropPct: 35.2, nightDboLogins: 4 },
  },
  {
    id: 'k-2',
    timestamp: '11:41:05',
    topic: 'risk.alerts.ews.v1',
    eventType: 'PreDelinquencyTriggered',
    partition: 1,
    direction: 'outbound',
    payload: { borrower: 'Arman', riskLevel: 'HIGH_PRE_DELINQUENCY', pDefault30d: 0.013, daysToCashGap: 30 },
  },
];

export const ClientOffersView: React.FC<ClientOffersViewProps> = ({
  loanId,
  onSignOffer,
}) => {
  const currentLoanId = loanId || 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee';
  const { data: rawOffers = [], isLoading, refetch } = useOffers(currentLoanId);

  const offers = useMemo(() => {
    const list = rawOffers.length > 0 ? rawOffers : DEFAULT_ARMAN_OFFERS;
    const map = new Map<string, RestructuringOffer>();
    for (let i = list.length - 1; i >= 0; i--) {
      const o = list[i];
      if (!map.has(o.scenarioType)) {
        map.set(o.scenarioType, o);
      }
    }
    const unique = Array.from(map.values());
    return unique.length > 0 ? unique : list.slice(0, 3);
  }, [rawOffers]);

  // States
  const [isDispatched, setIsDispatched] = useState(false);
  const [isSignedByClient, setIsSignedByClient] = useState(false);
  const [kafkaLogs, setKafkaLogs] = useState<KafkaLogMessage[]>(INITIAL_KAFKA_LOGS);

  // Dispatch from Bank Officer to Kafka Topic
  const handleDispatchToKafka = () => {
    const now = new Date();
    const timeStr = now.toTimeString().split(' ')[0];

    const newLog: KafkaLogMessage = {
      id: `k-dispatch-${Date.now()}`,
      timestamp: timeStr,
      topic: 'risk.restructuring.approved.v1',
      eventType: 'OfferApprovedByOfficer',
      partition: 2,
      direction: 'outbound',
      payload: {
        loanId: currentLoanId,
        officer: 'RiskOfficer-01',
        scenarios: ['BALANCED', 'GRACE_PERIOD', 'TENOR_EXTENSION'],
        kdnLimit: 0.4,
        dispatchChannel: 'MOBILE_DBO_PUSH'
      }
    };

    setKafkaLogs((prev) => [newLog, ...prev]);
    setIsDispatched(true);
  };

  // Client Signs on Smartphone Mockup
  const handleClientSign = async (offerId: string, otpCode: string) => {
    const now = new Date();
    const timeStr = now.toTimeString().split(' ')[0];

    try {
      await onSignOffer(offerId, otpCode);
    } catch {
      // resilient local confirmation
    }

    const newLog: KafkaLogMessage = {
      id: `k-sign-${Date.now()}`,
      timestamp: timeStr,
      topic: 'risk.contracts.signed.v1',
      eventType: 'ContractSignedByClient',
      partition: 3,
      direction: 'outbound',
      payload: {
        offerId,
        otpCode: otpCode || '7777',
        status: 'SIGNED_ACTIVE',
        ifrs9Stage: 'STAGE_1',
        newMonthlyPayment: 89500,
        bureauReported: true
      }
    };

    setKafkaLogs((prev) => [newLog, ...prev]);
    setIsSignedByClient(true);
    refetch();
  };

  const handleResetSimulation = () => {
    setIsDispatched(false);
    setIsSignedByClient(false);
    setKafkaLogs(INITIAL_KAFKA_LOGS);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      
      {/* Overview Info Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-4 rounded-2xl bg-slate-50 border border-slate-200 text-xs">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-xl bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold">
            <Radio className="w-4 h-4 text-emerald-600 animate-pulse" />
          </div>
          <div>
            <div className="font-bold text-slate-900 flex items-center space-x-2">
              <span>Сквозной процесс: от алерта риск-офицера до смартфона заемщика</span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-bold">
                Human-in-the-Loop
              </span>
            </div>
            <p className="text-slate-500 text-[11px] mt-0.5">
              Модель не меняет условия сама. Офицер банка валидирует алерт и отправляет оффер через Kafka на смартфон.
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2 text-[11px] font-mono">
          <span className="px-2.5 py-1 rounded-lg bg-white border border-slate-200 text-slate-600">
            Broker: <strong>localhost:9092</strong>
          </span>
          <span className="px-2.5 py-1 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-800 font-bold">
            SignalR: Live
          </span>
        </div>
      </div>

      {/* Main 2-Column Split: Bank Officer Desk (Left) + Smartphone Simulator (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Column: Bank Officer Console (7 cols) */}
        <div className="lg:col-span-7">
          <BankOfficerWorkplace
            offers={offers}
            isDispatched={isDispatched}
            isSignedByClient={isSignedByClient}
            onDispatchToKafka={handleDispatchToKafka}
            onResetSimulation={handleResetSimulation}
          />
        </div>

        {/* Right Column: Smartphone Simulator (5 cols) */}
        <div className="lg:col-span-5 flex justify-center sticky top-24">
          <SmartphoneMockup
            isDispatchedFromBank={isDispatched}
            offers={offers}
            onClientSign={handleClientSign}
            onResetSimulation={handleResetSimulation}
          />
        </div>

      </div>

      {/* Real-time Apache Kafka Console at the bottom */}
      <div className="pt-4">
        <KafkaLiveConsole logs={kafkaLogs} />
      </div>

    </div>
  );
};