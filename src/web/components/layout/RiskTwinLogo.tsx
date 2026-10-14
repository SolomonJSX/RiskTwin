import React from 'react';

export const RiskTwinLogo: React.FC<{ className?: string }> = ({ className = "w-full h-full" }) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="140 80 744 740"
      className={className}
      fill="none"
    >
      <defs>
        <linearGradient id="emeraldDark" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#064E3B" />
          <stop offset="100%" stopColor="#047857" />
        </linearGradient>

        <linearGradient id="emeraldMain" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#059669" />
          <stop offset="100%" stopColor="#10B981" />
        </linearGradient>

        <linearGradient id="tealAccent" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#0D9488" />
          <stop offset="100%" stopColor="#06B6D4" />
        </linearGradient>

        <linearGradient id="goldAccent" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#F59E0B" />
          <stop offset="100%" stopColor="#FBBF24" />
        </linearGradient>

        <filter id="rhombusShadow" x="-20%" y="-20%" width="140%" height="140%" filterUnits="userSpaceOnUse">
          <feDropShadow dx="0" dy="16" stdDeviation="20" floodColor="#064E3B" floodOpacity="0.25" />
        </filter>

        <filter id="innerGlow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="4" stdDeviation="6" floodColor="#000000" floodOpacity="0.15" />
        </filter>
      </defs>

      {/* Концентрическая геометрия / Радарные линии */}
      <circle cx="512" cy="450" r="340" fill="none" stroke="#CBD5E1" strokeWidth="2.5" strokeDasharray="8,6" opacity="0.75" />
      <circle cx="512" cy="450" r="260" fill="none" stroke="#94A3B8" strokeWidth="2.5" opacity="0.65" />
      <circle cx="512" cy="450" r="180" fill="none" stroke="#CBD5E1" strokeWidth="2.5" strokeDasharray="5,5" opacity="0.75" />

      {/* Основная композиция ромбов и шевронов (Digital Twin + Radar) БЕЗ ТЕКСТА */}
      <g filter="url(#rhombusShadow)">
        {/* 1. Внешний изумрудный ромб */}
        <polygon points="512,160 792,440 512,720 232,440" fill="url(#emeraldDark)" stroke="#A7F3D0" strokeWidth="6" />

        {/* 2. Вложенный второй ромб (Цифровой двойник / Twin offset) */}
        <polygon points="512,205 747,440 512,675 277,440" fill="url(#emeraldMain)" opacity="0.95" />

        {/* 3. Ступенчатые крылья-шевроны (Казахстанский орнамент / Финансовые потоки) */}
        {/* Левое белое крыло */}
        <path
          d="M 512 250 L 400 362 L 440 402 L 360 482 L 400 522 L 512 634 L 512 584 L 440 512 L 480 472 L 400 392 L 440 352 L 512 280 Z"
          fill="#FFFFFF"
          opacity="0.95"
          filter="url(#innerGlow)"
        />

        {/* Правое бирюзовое крыло (Поведенческий поток) */}
        <path
          d="M 512 250 L 624 362 L 584 402 L 664 482 L 624 522 L 512 634 L 512 584 L 584 512 L 544 472 L 624 392 L 584 352 L 512 280 Z"
          fill="url(#tealAccent)"
          opacity="0.95"
          filter="url(#innerGlow)"
        />

        {/* 4. Центральное ядро-алмаз */}
        <polygon points="512,380 572,440 512,500 452,440" fill="#FFFFFF" stroke="#059669" strokeWidth="4" />
        <polygon points="512,398 554,440 512,482 470,440" fill="url(#goldAccent)" />
        <polygon points="512,416 536,440 512,464 488,440" fill="#FFFFFF" />

        {/* 5. Направляющие технологические маркеры */}
        <polygon points="512,125 528,150 496,150" fill="#10B981" />
        <polygon points="512,755 528,730 496,730" fill="#0D9488" />
        <polygon points="197,440 222,424 222,456" fill="#10B981" />
        <polygon points="827,440 802,424 802,456" fill="#0D9488" />
      </g>
    </svg>
  );
};
