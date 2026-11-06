// TypeScript mirror of the Animation DSL v1. Allowed values live in engine/registry.json and are
// enforced by scripts/validate_project.py before every render.
export type Mode = 'draft' | 'preview' | 'final' | 'stills';

export type Params = Record<string, unknown>;

export interface Transform {
  x?: number;
  y?: number;
  scale?: number;
  rotation?: number;
  opacity?: number;
  layer?: number;
  /** Screen-fixed (HUD): ignores the scene camera. Fixed elements draw above all camera elements. */
  fixed?: boolean;
}

export interface Element {
  id: string;
  type: string;
  component: string;
  asset?: string | null;
  startSec: number;
  durationSec: number;
  transform?: Transform;
  content?: string | null;
  preset?: string | null;
  loop?: string | null;
  exit?: string | null;
  params?: Params;
}

export interface Background {
  type: 'solid' | 'gradient' | 'image';
  asset?: string;
  [key: string]: unknown;
}

export interface Transition {
  preset: string;
  durationSec?: number;
}

export interface Sfx {
  asset: string;
  atSec: number;
  volume?: number;
}

export interface Scene {
  id: string;
  startSec: number;
  durationSec: number;
  background?: Background;
  camera?: {preset: string; params?: Params};
  elements?: Element[];
  sfx?: Sfx[];
  transitionOut?: Transition;
}

export interface AnimationPlan {
  schemaVersion: '1.0';
  video: {id: string; title?: string; width: number; height: number; fps: number; durationSec: number};
  audio?: {voiceover?: string | null; music?: string | null; voiceVolume?: number; musicVolume?: number};
  scenes: Scene[];
}

export type ShortProps = {
  plan: AnimationPlan;
  mode: Mode;
};
