import React from 'react';
import {AbsoluteFill, Freeze, Html5Audio, Sequence, interpolate, staticFile, useVideoConfig} from 'remotion';
import {SceneView, toFrames} from './engine/Scene';
import type {ShortProps} from './types';

/**
 * Timeline: scenes play back-to-back at their exact startSec, so narration sync never shifts.
 * A non-cut transitionOut holds the outgoing scene's last frame for durationSec while the next
 * scene enters on top (crossfade / slide_up).
 */
export const Short: React.FC<ShortProps> = ({plan}) => {
  const {fps, durationInFrames} = useVideoConfig();
  const scenes = plan.scenes;
  const audio = plan.audio ?? {};
  const musicVolume = audio.musicVolume ?? 0.15;
  const fadeFrames = Math.round(fps * 1.0);

  return (
    <AbsoluteFill style={{background: '#000'}}>
      {scenes.map((scene, i) => {
        const tr = scene.transitionOut;
        if (!scenes[i + 1] || !tr || tr.preset === 'cut' || !tr.durationSec) return null;
        const len = toFrames(scene.durationSec, fps);
        return (
          <Sequence
            key={`${scene.id}-hold`}
            name={`${scene.id} (transition hold)`}
            from={toFrames(scene.startSec, fps) + len}
            durationInFrames={Math.max(1, toFrames(tr.durationSec, fps))}
          >
            <Freeze frame={len - 1}>
              <SceneView scene={scene} />
            </Freeze>
          </Sequence>
        );
      })}
      {scenes.map((scene, i) => (
        <Sequence
          key={scene.id}
          name={scene.id}
          from={toFrames(scene.startSec, fps)}
          durationInFrames={Math.max(1, toFrames(scene.durationSec, fps))}
        >
          <SceneView scene={scene} transitionIn={i > 0 ? scenes[i - 1].transitionOut : undefined} />
        </Sequence>
      ))}
      {audio.voiceover ? <Html5Audio src={staticFile(audio.voiceover)} volume={audio.voiceVolume ?? 1} /> : null}
      {audio.music ? (
        <Html5Audio
          src={staticFile(audio.music)}
          loop
          volume={(f) =>
            musicVolume *
            interpolate(f, [durationInFrames - fadeFrames, durationInFrames], [1, 0], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            })
          }
        />
      ) : null}
    </AbsoluteFill>
  );
};
