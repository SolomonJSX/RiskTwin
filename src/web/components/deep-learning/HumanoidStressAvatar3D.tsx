'use client';

import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Float, OrbitControls, Ring, Sphere, Cylinder } from '@react-three/drei';
import * as THREE from 'three';

interface HumanoidStressAvatarProps {
  distressScore: number; // 0.0 to 1.0
  clusterCode: string; // STABLE_DISCIPLINE, LATENT_ANXIETY, ACUTE_PANIC, CHRONIC_EXHAUSTION
  heartRateBpm?: number;
}

// Внутренняя 3D сцена аватара
function CyberHumanoidModel({
  distressScore,
  clusterCode,
}: {
  distressScore: number;
  clusterCode: string;
}) {
  const groupRef = useRef<THREE.Group>(null);
  const heartRef = useRef<THREE.Mesh>(null);
  const headRef = useRef<THREE.Mesh>(null);
  const auraRef = useRef<THREE.Mesh>(null);
  const ringRef = useRef<THREE.Mesh>(null);

  // Вычисление динамической цветовой палитры в зависимости от стресса
  const { mainColor, emissiveColor, auraColor, bpm, isPanic, isExhausted } = useMemo(() => {
    const isExh = clusterCode === 'CHRONIC_EXHAUSTION' || distressScore >= 0.75;
    const isPan = clusterCode === 'ACUTE_PANIC' || (distressScore >= 0.5 && !isExh);
    const isAnx = clusterCode === 'LATENT_ANXIETY' || (distressScore >= 0.25 && !isPan && !isExh);

    let main = '#10b981'; // Изумрудный (Stable)
    let emissive = '#059669';
    let aura = '#34d399';
    let calculatedBpm = 62 + distressScore * 30;

    if (isExh) {
      main = '#7c3aed'; // Темно-фиолетовый / истощение
      emissive = '#4c1d95';
      aura = '#a78bfa';
      calculatedBpm = 50 + (1.0 - distressScore) * 20; // Угасающий тяжелый пульс
    } else if (isPan) {
      main = '#ef4444'; // Ярко-красный / острая паника
      emissive = '#dc2626';
      aura = '#f87171';
      calculatedBpm = 110 + distressScore * 35; // Тахикардия 130-145 BPM
    } else if (isAnx) {
      main = '#f59e0b'; // Янтарно-желтый / латентная тревога
      emissive = '#d97706';
      aura = '#fbbf24';
      calculatedBpm = 82 + distressScore * 20;
    }

    return {
      mainColor: main,
      emissiveColor: emissive,
      auraColor: aura,
      bpm: calculatedBpm,
      isPanic: isPan,
      isExhausted: isExh,
    };
  }, [distressScore, clusterCode]);

  useFrame((state, delta) => {
    const t = state.clock.getElapsedTime();

    // 1. Дыхание и покачивание тела
    if (groupRef.current) {
      const breathSpeed = isPanic ? 5.0 : isExhausted ? 1.0 : 2.2;
      const breathAmp = isExhausted ? 0.02 : 0.05;
      groupRef.current.position.y = Math.sin(t * breathSpeed) * breathAmp;

      // Осанка: при хроническом истощении сгибается вперед (сутулость)
      const targetRotX = isExhausted ? 0.18 : isPanic ? Math.sin(t * 12) * 0.02 : 0.0;
      groupRef.current.rotation.x = THREE.MathUtils.lerp(groupRef.current.rotation.x, targetRotX, 0.05);

      // Легкий тремор при острой панике
      if (isPanic) {
        groupRef.current.position.x = (Math.random() - 0.5) * 0.015;
      } else {
        groupRef.current.position.x = 0;
      }
    }

    // 2. Сердечный пульс (Cardio BPM)
    if (heartRef.current) {
      const freq = (bpm / 60) * Math.PI * 2;
      const pulse = Math.pow(Math.sin(t * freq), 4);
      const scale = 1.0 + pulse * (isPanic ? 0.45 : 0.25);
      heartRef.current.scale.set(scale, scale, scale);
    }

    // 3. Вращение когнитивной ауры и кольца стресса
    if (ringRef.current) {
      ringRef.current.rotation.z += delta * (isPanic ? 3.0 : 0.8);
      ringRef.current.rotation.x = Math.sin(t * 1.5) * 0.3;
    }

    if (auraRef.current) {
      auraRef.current.rotation.y += delta * 0.6;
    }
  });

  return (
    <group ref={groupRef} position={[0, -0.6, 0]}>
      {/* 1. ГОЛОВА (Когнитивно-психологический центр) */}
      <group position={[0, 1.85, 0]}>
        <Sphere ref={headRef} args={[0.32, 32, 32]}>
          <meshStandardMaterial
            color="#0f172a"
            emissive={emissiveColor}
            emissiveIntensity={isPanic ? 0.8 : 0.4}
            roughness={0.2}
            metalness={0.8}
            wireframe={false}
          />
        </Sphere>

        {/* Нейронный шлем / визор */}
        <Cylinder args={[0.33, 0.33, 0.12, 32]} position={[0, 0.05, 0.08]} rotation={[0.2, 0, 0]}>
          <meshStandardMaterial
            color={mainColor}
            emissive={mainColor}
            emissiveIntensity={1.2}
            roughness={0.1}
            metalness={0.9}
          />
        </Cylinder>

        {/* Когнитивный ореол тревожности (Halo Ring) */}
        <Ring ref={ringRef} args={[0.42, 0.46, 32]} position={[0, 0.15, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <meshBasicMaterial color={auraColor} side={THREE.DoubleSide} transparent opacity={0.7} />
        </Ring>
      </group>

      {/* 2. ШЕЯ И КЛЮЧИЦЫ */}
      <Cylinder args={[0.12, 0.14, 0.2, 16]} position={[0, 1.48, 0]}>
        <meshStandardMaterial color="#1e293b" metalness={0.7} roughness={0.3} />
      </Cylinder>

      {/* 3. ТОРС (Грудная клетка) */}
      <group position={[0, 1.05, 0]}>
        <Cylinder args={[0.48, 0.38, 0.72, 32]}>
          <meshStandardMaterial
            color="#0f172a"
            metalness={0.85}
            roughness={0.25}
            wireframe={false}
          />
        </Cylinder>

        {/* Кардио-ядро (Сердечный ритм стресса) */}
        <Sphere ref={heartRef} args={[0.16, 24, 24]} position={[0, 0.12, 0.25]}>
          <meshStandardMaterial
            color={mainColor}
            emissive={mainColor}
            emissiveIntensity={isPanic ? 2.0 : 1.2}
            roughness={0.1}
          />
        </Sphere>

        {/* Защитные ребра каркаса */}
        {[-0.15, 0.0, 0.15].map((yOffset, idx) => (
          <Ring key={idx} args={[0.42 - idx * 0.03, 0.44 - idx * 0.03, 24]} position={[0, yOffset, 0]} rotation={[-Math.PI / 2, 0, 0]}>
            <meshBasicMaterial color={mainColor} side={THREE.DoubleSide} transparent opacity={0.4} />
          </Ring>
        ))}
      </group>

      {/* 4. ТАЗ И БАЗА КОРПУСА */}
      <Cylinder args={[0.36, 0.32, 0.28, 24]} position={[0, 0.56, 0]}>
        <meshStandardMaterial color="#1e293b" metalness={0.8} roughness={0.3} />
      </Cylinder>

      {/* 5. РУКИ (Плечи, предплечья, кисти) */}
      {[-1, 1].map((side) => (
        <group key={side} position={[side * 0.62, 1.32, 0]}>
          {/* Плечевой сустав */}
          <Sphere args={[0.13, 16, 16]}>
            <meshStandardMaterial color={mainColor} emissive={emissiveColor} emissiveIntensity={0.6} metalness={0.9} />
          </Sphere>
          {/* Плечо */}
          <Cylinder args={[0.09, 0.08, 0.42, 16]} position={[side * 0.06, -0.26, 0]} rotation={[0, 0, side * -0.15]}>
            <meshStandardMaterial color="#0f172a" metalness={0.7} />
          </Cylinder>
          {/* Локоть */}
          <Sphere args={[0.08, 12, 12]} position={[side * 0.11, -0.5, 0]}>
            <meshBasicMaterial color={mainColor} />
          </Sphere>
          {/* Предплечье */}
          <Cylinder args={[0.07, 0.06, 0.44, 16]} position={[side * 0.14, -0.74, 0.04]} rotation={[0.2, 0, side * -0.1]}>
            <meshStandardMaterial color="#1e293b" metalness={0.8} />
          </Cylinder>
        </group>
      ))}

      {/* 6. НОГИ (Стойка и стабильность) */}
      {[-1, 1].map((side) => (
        <group key={side} position={[side * 0.24, 0.4, 0]}>
          {/* Бедренный сустав */}
          <Sphere args={[0.11, 16, 16]}>
            <meshBasicMaterial color={mainColor} />
          </Sphere>
          {/* Бедро */}
          <Cylinder args={[0.12, 0.09, 0.62, 16]} position={[0, -0.34, 0]}>
            <meshStandardMaterial color="#0f172a" metalness={0.8} roughness={0.3} />
          </Cylinder>
          {/* Коленный шарнир */}
          <Sphere args={[0.09, 14, 14]} position={[0, -0.68, 0.02]}>
            <meshStandardMaterial color={mainColor} emissive={emissiveColor} emissiveIntensity={0.8} />
          </Sphere>
          {/* Голень */}
          <Cylinder args={[0.08, 0.07, 0.65, 16]} position={[0, -1.04, 0.02]}>
            <meshStandardMaterial color="#1e293b" metalness={0.7} />
          </Cylinder>
          {/* Стопа */}
          <Cylinder args={[0.09, 0.11, 0.08, 16]} position={[0, -1.38, 0.08]} rotation={[0.2, 0, 0]}>
            <meshStandardMaterial color={mainColor} metalness={0.9} />
          </Cylinder>
        </group>
      ))}

      {/* 7. ГОЛОГРАФИЧЕСКИЙ ПЬЕДЕСТАЛ / СКАНИРУЮЩИЙ ПОЛ */}
      <group position={[0, -1.45, 0]}>
        <Ring args={[0.7, 1.4, 36]} rotation={[-Math.PI / 2, 0, 0]}>
          <meshBasicMaterial color={mainColor} transparent opacity={0.25} side={THREE.DoubleSide} />
        </Ring>
        <Ring args={[1.45, 1.5, 48]} rotation={[-Math.PI / 2, 0, 0]}>
          <meshBasicMaterial color={mainColor} transparent opacity={0.6} side={THREE.DoubleSide} />
        </Ring>
      </group>
    </group>
  );
}

export const HumanoidStressAvatar3D: React.FC<HumanoidStressAvatarProps> = ({
  distressScore,
  clusterCode,
  heartRateBpm,
}) => {
  return (
    <div className="w-full h-full min-h-[460px] relative rounded-2xl overflow-hidden bg-gradient-to-b from-slate-950 via-slate-900 to-emerald-950/40 border border-emerald-500/20 shadow-2xl">
      {/* 3D WebGL Canvas */}
      <Canvas camera={{ position: [0, 0.3, 4.4], fov: 42 }}>
        <ambientLight intensity={0.8} />
        <directionalLight position={[5, 10, 7]} intensity={2.0} color="#ffffff" />
        <pointLight position={[-6, 4, -4]} intensity={2.5} color="#00ffcc" />
        <pointLight position={[6, -4, 4]} intensity={2.0} color="#f43f5e" />

        <Float speed={1.5} rotationIntensity={0.2} floatIntensity={0.3}>
          <CyberHumanoidModel distressScore={distressScore} clusterCode={clusterCode} />
        </Float>

        <OrbitControls
          enableZoom={true}
          minDistance={2.5}
          maxDistance={7.0}
          maxPolarAngle={Math.PI / 2 + 0.1}
          minPolarAngle={Math.PI / 4}
          enablePan={false}
          rotateSpeed={0.8}
        />
      </Canvas>

      {/* Бейдж состояния в углу 3D сцены */}
      <div className="absolute top-4 left-4 z-10 flex flex-col space-y-1 backdrop-blur-md bg-slate-900/80 px-3.5 py-2 rounded-xl border border-white/10 text-xs">
        <div className="flex items-center space-x-2">
          <span className="relative flex h-2.5 w-2.5">
            <span
              className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                distressScore > 0.5 ? 'bg-red-400' : distressScore > 0.25 ? 'bg-amber-400' : 'bg-emerald-400'
              }`}
            />
            <span
              className={`relative inline-flex rounded-full h-2.5 w-2.5 ${
                distressScore > 0.5 ? 'bg-red-500' : distressScore > 0.25 ? 'bg-amber-500' : 'bg-emerald-500'
              }`}
            />
          </span>
          <span className="font-mono font-bold tracking-wider uppercase text-[11px] text-white">
            {clusterCode.replace('_', ' ')}
          </span>
        </div>
        <p className="text-[11px] text-slate-300">
          Кардио-ритм: <span className="font-bold text-white">{Math.round(62 + distressScore * 65)} BPM</span>
        </p>
      </div>

      {/* Подсказка управления */}
      <div className="absolute bottom-3 right-4 z-10 text-[10px] text-slate-400 font-mono backdrop-blur-sm bg-slate-900/60 px-2.5 py-1 rounded-md border border-white/5">
        ✦ Вращайте мышью • Скролл для зума
      </div>
    </div>
  );
};
