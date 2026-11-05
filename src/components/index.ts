import type React from 'react';
import type {Element} from '../types';
import {Caption, KineticText} from './text';
import {Character, ParticleBurst, Prop, Shape} from './visual';

export interface ComponentProps {
  el: Element;
  /** Component + preset params merged with registry defaults. */
  p: Record<string, any>;
}

/** Must stay in sync with engine/registry.json "components" (validator enforces the plan side). */
export const COMPONENTS: Record<string, React.FC<ComponentProps>> = {
  KineticText,
  Caption,
  Shape,
  Prop,
  Character,
  ParticleBurst,
};
