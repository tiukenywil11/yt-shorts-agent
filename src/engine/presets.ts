// Pure, frame-deterministic motion presets. Offsets (dx, dy) are fractions of video WIDTH so motion
// looks identical in every render mode.
import {Easing, interpolate} from 'remotion';
import type {Element} from '../types';
import {withDefaults} from './registry';

export interface Motion {
  dx: number;
  dy: number;
  scale: number;
  rotate: number;
  opacity: number;
}

const clamp01 = (v: number) => Math.min(1, Math.max(0, v));
const easeOut = Easing.out(Easing.cubic);
const TAU = Math.PI * 2;

const enter: Record<string, (t: number, p: Record<string, any>, m: Motion) => void> = {
  none: () => {},
  fade_in: (t, p, m) => {
    m.opacity *= easeOut(clamp01(t / p.inSec));
  },
  pop_in: (t, p, m) => {
    const k = clamp01(t / p.inSec);
    m.scale *= interpolate(k, [0, 1], [0, 1], {easing: Easing.out(Easing.back(p.overshoot * 15))});
    m.opacity *= clamp01(k * 3);
  },
  slide_in_left: (t, p, m) => {
    const k = clamp01(t / p.inSec);
    m.dx -= p.distance * (1 - easeOut(k));
    m.opacity *= clamp01(k * 2);
  },
  slide_in_right: (t, p, m) => {
    const k = clamp01(t / p.inSec);
    m.dx += p.distance * (1 - easeOut(k));
    m.opacity *= clamp01(k * 2);
  },
  slide_in_up: (t, p, m) => {
    const k = clamp01(t / p.inSec);
    m.dy += p.distance * (1 - easeOut(k));
    m.opacity *= clamp01(k * 2);
  },
  bounce: (t, p, m) => {
    const k = clamp01(t / p.inSec);
    m.dy -= p.height * (1 - k) * Math.abs(Math.cos(k * Math.PI * 2.5));
    m.opacity *= clamp01(k * 5);
  },
  shake: (t, p, m) => {
    const k = clamp01(t / p.inSec);
    if (k < 1) m.dx += p.amplitude * Math.sin(t * TAU * 12) * (1 - k);
  },
};

const loop: Record<string, (t: number, p: Record<string, any>, m: Motion) => void> = {
  pulse: (t, p, m) => {
    m.scale *= 1 + p.amount * 0.5 * (1 - Math.cos((TAU * t) / p.periodSec));
  },
  float_loop: (t, p, m) => {
    m.dy += p.amplitude * Math.sin((TAU * t) / p.periodSec);
  },
  wiggle: (t, p, m) => {
    m.rotate += p.degrees * Math.sin((TAU * t) / p.periodSec);
  },
};

const exit: Record<string, (remaining: number, p: Record<string, any>, m: Motion) => void> = {
  fade_out: (r, p, m) => {
    m.opacity *= clamp01(r / p.outSec);
  },
  pop_out: (r, p, m) => {
    const k = clamp01(r / p.outSec);
    m.scale *= Easing.in(Easing.cubic)(k);
    m.opacity *= k;
  },
};

/** t = seconds since element start. */
export const computeMotion = (el: Element, t: number): Motion => {
  const m: Motion = {dx: 0, dy: 0, scale: 1, rotate: 0, opacity: 1};
  if (el.preset && enter[el.preset]) enter[el.preset](t, withDefaults('presets', el.preset, el.params), m);
  if (el.loop && loop[el.loop]) loop[el.loop](t, withDefaults('presets', el.loop, el.params), m);
  if (el.exit && exit[el.exit]) exit[el.exit](el.durationSec - t, withDefaults('presets', el.exit, el.params), m);
  return m;
};
