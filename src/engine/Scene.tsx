import React from 'react';
import {AbsoluteFill, Easing, Html5Audio, Img, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {COMPONENTS} from '../components';
import type {Background, Element, Scene, Transition} from '../types';
import {computeMotion} from './presets';
import {withDefaults} from './registry';

export const toFrames = (sec: number, fps: number) => Math.round(sec * fps);

const BackgroundView: React.FC<{bg?: Background}> = ({bg}) => {
  const type = bg?.type ?? 'solid';
  const p = withDefaults('backgrounds', type, bg as Record<string, unknown>);
  if (type === 'image' && bg?.asset) {
    return (
      <AbsoluteFill>
        <Img src={staticFile(bg.asset)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
    );
  }
  if (type === 'gradient') {
    return <AbsoluteFill style={{background: `linear-gradient(${p.angle}deg, ${p.from}, ${p.to})`}} />;
  }
  return <AbsoluteFill style={{background: p.color}} />;
};

const ElementBody: React.FC<{el: Element}> = ({el}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const Comp = COMPONENTS[el.component];
  if (!Comp) throw new Error(`Element ${el.id}: component '${el.component}' is not implemented.`);
  const tr = el.transform ?? {};
  const m = computeMotion(el, frame / fps);
  const p = {
    ...withDefaults('presets', el.preset, el.params),
    ...withDefaults('presets', el.loop, el.params),
    ...withDefaults('presets', el.exit, el.params),
    ...withDefaults('components', el.component, el.params),
  };
  return (
    <div
      style={{
        position: 'absolute',
        left: (tr.x ?? 0.5) * width,
        top: (tr.y ?? 0.5) * height,
        zIndex: tr.layer ?? 0,
        opacity: (tr.opacity ?? 1) * m.opacity,
        transform: `translate(-50%, -50%) translate(${m.dx * width}px, ${m.dy * width}px) rotate(${
          (tr.rotation ?? 0) + m.rotate
        }deg) scale(${(tr.scale ?? 1) * m.scale})`,
      }}
    >
      <Comp el={el} p={p} />
    </div>
  );
};

const cameraStyle = (scene: Scene, frame: number, sceneFrames: number, width: number): React.CSSProperties => {
  const preset = scene.camera?.preset ?? 'static';
  const p = withDefaults('cameras', preset, scene.camera?.params);
  const k = interpolate(frame, [0, Math.max(1, sceneFrames - 1)], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.ease),
  });
  if (preset === 'camera_push') return {transform: `scale(${1 + p.amount * k})`};
  if (preset === 'camera_pan') {
    const overscan = 1 + 2 * Math.max(Math.abs(p.dx), Math.abs(p.dy));
    return {transform: `scale(${overscan}) translate(${-p.dx * width * k}px, ${-p.dy * width * k}px)`};
  }
  return {};
};

/** One scene in local time (frame 0 = scene start). transitionIn = previous scene's transitionOut. */
export const SceneView: React.FC<{scene: Scene; transitionIn?: Transition}> = ({scene, transitionIn}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const sceneFrames = toFrames(scene.durationSec, fps);

  let enter: React.CSSProperties = {};
  const tIn = transitionIn && transitionIn.preset !== 'cut' ? toFrames(transitionIn.durationSec ?? 0, fps) : 0;
  if (tIn > 0) {
    const k = interpolate(frame, [0, tIn], [0, 1], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
    enter = transitionIn!.preset === 'slide_up' ? {transform: `translateY(${(1 - k) * height}px)`} : {opacity: k};
  }

  return (
    <AbsoluteFill style={{overflow: 'hidden', ...enter}}>
      <AbsoluteFill style={cameraStyle(scene, frame, sceneFrames, width)}>
        <BackgroundView bg={scene.background} />
        {(scene.elements ?? []).map((el) => (
          <Sequence
            key={el.id}
            name={el.id}
            from={toFrames(el.startSec, fps)}
            durationInFrames={Math.max(1, toFrames(el.durationSec, fps))}
            layout="none"
          >
            <ElementBody el={el} />
          </Sequence>
        ))}
      </AbsoluteFill>
      {(scene.sfx ?? []).map((fx, i) => (
        <Sequence key={`sfx-${i}`} from={toFrames(fx.atSec, fps)} layout="none">
          <Html5Audio src={staticFile(fx.asset)} volume={fx.volume ?? 1} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
