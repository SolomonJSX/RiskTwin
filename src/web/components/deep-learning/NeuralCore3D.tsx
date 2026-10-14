'use client';

import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Sphere, MeshDistortMaterial, Float } from '@react-three/drei';
import * as THREE from 'three';

interface CoreSphereProps {
  stressLevel: number; // 0 to 100
}

function AnimatedCore({ stressLevel }: CoreSphereProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  
  // Цвет сферы: от спокойного изумрудного до горящего неонового коралла при стрессе
  const isStressed = stressLevel > 50;
  const coreColor = isStressed ? '#ff3366' : '#00ff88';

  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta * (isStressed ? 0.8 : 0.3);
      meshRef.current.rotation.y += delta * (isStressed ? 1.2 : 0.4);
    }
  });

  return (
    <Float speed={isStressed ? 4 : 2} rotationIntensity={1.5} floatIntensity={2}>
      <Sphere ref={meshRef} args={[1.5, 64, 64]}>
        <MeshDistortMaterial
          color={coreColor}
          emissive={coreColor}
          emissiveIntensity={isStressed ? 0.7 : 0.4}
          roughness={0.15}
          metalness={0.8}
          distort={isStressed ? 0.65 : 0.35}
          speed={isStressed ? 5 : 2}
          wireframe={false}
        />
      </Sphere>
    </Float>
  );
}

export const NeuralCore3D: React.FC<{ stressLevel: number }> = ({ stressLevel }) => {
  return (
    <div className="w-full h-full relative">
      <Canvas camera={{ position: [0, 0, 4.2], fov: 45 }}>
        <ambientLight intensity={0.7} />
        <directionalLight position={[10, 10, 5]} intensity={1.5} />
        <pointLight position={[-10, -10, -5]} color="#00ffcc" intensity={2} />
        <AnimatedCore stressLevel={stressLevel} />
      </Canvas>
    </div>
  );
};
