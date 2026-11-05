import React from 'react';
import {Composition} from 'remotion';
import {modeSpec} from './engine/registry';
import {Short} from './Short';
import type {ShortProps} from './types';

const defaultProps: ShortProps = {
  mode: 'preview',
  plan: {
    schemaVersion: '1.0',
    video: {id: 'placeholder', width: 1080, height: 1920, fps: 30, durationSec: 2},
    audio: {voiceover: null, music: null},
    scenes: [
      {
        id: 'scene-01',
        startSec: 0,
        durationSec: 2,
        background: {type: 'gradient'},
        elements: [
          {
            id: 'hello',
            type: 'text',
            component: 'KineticText',
            startSec: 0,
            durationSec: 2,
            content: 'Pass --props to preview a project',
            preset: 'pop_in',
            transform: {x: 0.5, y: 0.5},
          },
        ],
      },
    ],
  },
};

export const Root: React.FC = () => (
  <Composition
    id="Short"
    component={Short}
    defaultProps={defaultProps}
    width={1080}
    height={1920}
    fps={30}
    durationInFrames={60}
    calculateMetadata={({props}) => {
      // Render mode decides resolution + fps; the plan's timeline (seconds) is identical in every mode.
      const m = modeSpec(props.mode);
      return {
        width: m.width,
        height: m.height,
        fps: m.fps,
        durationInFrames: Math.max(1, Math.round(props.plan.video.durationSec * m.fps)),
      };
    }}
  />
);
