import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import type {ComponentProps} from './index';

const textStroke = (color: string, widthPx: number): React.CSSProperties =>
  widthPx > 0 ? {WebkitTextStroke: `${widthPx * 2}px ${color}`, paintOrder: 'stroke fill'} : {};

export const KineticText: React.FC<ComponentProps> = ({el, p}) => {
  const {width} = useVideoConfig();
  const k = width / 1080;
  const text = String(el.content ?? '');
  return (
    <div
      style={{
        width: p.maxWidth * width,
        textAlign: p.align,
        fontFamily: p.fontFamily,
        fontWeight: p.fontWeight,
        fontSize: p.fontSize * k,
        lineHeight: 1.1,
        color: p.color,
        whiteSpace: 'pre-wrap',
        textTransform: p.uppercase ? 'uppercase' : 'none',
        ...textStroke(p.strokeColor, p.strokeWidth * k),
      }}
    >
      {text}
    </div>
  );
};

/** Word-by-word captions. Words are timed across the element duration, weighted by length, so set the
 * element's startSec/durationSec to the narration segment timing from script.json. */
export const Caption: React.FC<ComponentProps> = ({el, p}) => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const k = width / 1080;
  const words = String(el.content ?? '').split(/\s+/).filter(Boolean);
  if (!words.length) return null;

  const weights = words.map((w) => w.length + 2);
  const total = weights.reduce((a, b) => a + b, 0);
  const progress = Math.min(0.9999, Math.max(0, frame / fps / el.durationSec)) * total;
  let acc = 0;
  let active = 0;
  for (let i = 0; i < words.length; i++) {
    acc += weights[i];
    if (progress < acc) {
      active = i;
      break;
    }
  }
  const per = Math.max(1, Math.round(p.wordsPerChunk));
  const chunkStart = Math.floor(active / per) * per;
  const chunk = words.slice(chunkStart, chunkStart + per);

  return (
    <div
      style={{
        width: 0.9 * width,
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        columnGap: '0.38em',
        fontFamily: p.fontFamily,
        fontWeight: 900,
        fontSize: p.fontSize * k,
        lineHeight: 1.15,
        textTransform: p.uppercase ? 'uppercase' : 'none',
        ...textStroke(p.strokeColor, p.strokeWidth * k),
      }}
    >
      {chunk.map((w, i) => {
        const isActive = chunkStart + i === active;
        return (
          <span
            key={chunkStart + i}
            style={{
              display: 'inline-block',
              color: isActive ? p.highlightColor : p.color,
              transform: `scale(${isActive ? 1.08 : 1})`,
            }}
          >
            {w}
          </span>
        );
      })}
    </div>
  );
};
