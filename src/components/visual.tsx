import React from 'react';
import {Img, random, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {ComponentProps} from './index';

export const Shape: React.FC<ComponentProps> = ({p}) => {
  const {width} = useVideoConfig();
  const k = width / 1080;
  const w = p.width * width;
  const h = p.height * width;
  const stroke = p.strokeWidth * k;
  if (p.shape === 'triangle') {
    return (
      <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} style={{overflow: 'visible', display: 'block'}}>
        <polygon points={`${w / 2},0 ${w},${h} 0,${h}`} fill={p.color} stroke={p.strokeColor} strokeWidth={stroke} />
      </svg>
    );
  }
  return (
    <div
      style={{
        width: w,
        height: p.shape === 'line' ? Math.max(stroke, 2 * k) : h,
        background: p.color,
        borderRadius: p.shape === 'circle' ? '50%' : p.radius * width,
        border: stroke > 0 && p.shape !== 'line' ? `${stroke}px solid ${p.strokeColor}` : undefined,
        boxSizing: 'border-box',
      }}
    />
  );
};

export const Prop: React.FC<ComponentProps> = ({el, p}) => {
  const {width} = useVideoConfig();
  return (
    <Img
      src={staticFile(el.asset as string)}
      style={{width: p.width * width, display: 'block', transform: p.flipX ? 'scaleX(-1)' : undefined}}
    />
  );
};

/** Pose-swap character: params.poses = [{atSec, asset}] relative to the element start. */
export const Character: React.FC<ComponentProps> = ({el, p}) => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const t = frame / fps;
  let asset = el.asset as string;
  for (const pose of (p.poses as {atSec: number; asset: string}[]) ?? []) {
    if (pose.atSec <= t) asset = pose.asset;
  }
  const squash = p.talking ? 1 + 0.025 * Math.sin(t * Math.PI * 2 * 4) : 1;
  return (
    <Img
      src={staticFile(asset)}
      style={{
        width: p.width * width,
        display: 'block',
        transformOrigin: '50% 100%',
        transform: `scaleX(${p.flipX ? -1 : 1}) scaleY(${squash})`,
      }}
    />
  );
};

/** Seeded particle burst: identical output for the same seed on every render. */
export const ParticleBurst: React.FC<ComponentProps> = ({el, p}) => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const k = Math.min(1, frame / fps / el.durationSec);
  const eased = 1 - Math.pow(1 - k, 3);
  const size = p.size * width;
  const count = Math.max(1, Math.round(p.count));
  return (
    <div style={{position: 'relative', width: 0, height: 0}}>
      {Array.from({length: count}, (_, i) => {
        const angle = random(`${p.seed}-a-${i}`) * Math.PI * 2;
        const speed = 0.45 + random(`${p.seed}-s-${i}`) * 0.55;
        const dist = p.spread * width * speed * eased;
        const x = Math.cos(angle) * dist;
        const y = Math.sin(angle) * dist + k * k * 0.08 * width;
        const s = size * (0.6 + random(`${p.seed}-z-${i}`) * 0.8);
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: x - s / 2,
              top: y - s / 2,
              width: s,
              height: s,
              borderRadius: '50%',
              background: p.color,
              opacity: 1 - k,
            }}
          />
        );
      })}
    </div>
  );
};
