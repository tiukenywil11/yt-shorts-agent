import registry from '../../engine/registry.json';
import type {Mode, Params} from '../types';

type ParamSpec = {type: string; default?: unknown};
type SpecMap = Record<string, ParamSpec>;

const specGroups: Record<string, Record<string, {params: SpecMap}>> = {
  components: registry.components as Record<string, {params: SpecMap}>,
  presets: registry.presets as Record<string, {params: SpecMap}>,
  cameras: registry.cameras as Record<string, {params: SpecMap}>,
  backgrounds: registry.backgrounds as Record<string, {params: SpecMap}>,
};

export const modeSpec = (mode: Mode) =>
  (registry.modes as Record<Mode, {width: number; height: number; fps: number; crf: number}>)[mode];

/** Merge registry defaults with the plan's params. Unknown entries were rejected by the validator. */
export const withDefaults = (
  group: keyof typeof specGroups,
  name: string | null | undefined,
  params: Params | undefined,
): Record<string, any> => {
  const spec = name ? specGroups[group][name]?.params ?? {} : {};
  const out: Record<string, unknown> = {};
  for (const [key, s] of Object.entries(spec)) out[key] = s.default;
  for (const [key, v] of Object.entries(params ?? {})) if (key in spec) out[key] = v;
  return out;
};
