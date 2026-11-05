#!/usr/bin/env node
// Render adapter: npm run render:short -- --project projects/<id> --mode stills|draft|preview|final
//   [--scenes scene-01,scene-03] [--overwrite] [--concurrency N]
// Validates first, bundles with the project folder as publicDir, renders into <project>/output/,
// then runs scripts/check_video.py (videos) or make_contact_sheet.py (stills).
import {bundle} from '@remotion/bundler';
import {renderMedia, renderStill, selectComposition} from '@remotion/renderer';
import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PY = process.env.PYTHON || (process.platform === 'win32' ? 'python' : 'python3');
const registry = JSON.parse(fs.readFileSync(path.join(ROOT, 'engine/registry.json'), 'utf8'));

const die = (msg) => {
  console.error(`RENDER FAILED: ${msg}`);
  process.exit(1);
};

const parseArgs = (argv) => {
  const out = {mode: 'preview', scenes: null, overwrite: false, concurrency: null};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--project') out.project = argv[++i];
    else if (a === '--mode') out.mode = argv[++i];
    else if (a === '--scenes') out.scenes = argv[++i].split(',').map((s) => s.trim()).filter(Boolean);
    else if (a === '--overwrite') out.overwrite = true;
    else if (a === '--concurrency') out.concurrency = Number(argv[++i]);
    else die(`Unknown argument ${a}`);
  }
  if (!out.project) die('Missing --project projects/<id>');
  if (!registry.modes[out.mode]) die(`--mode must be one of ${Object.keys(registry.modes).join(', ')}`);
  return out;
};

const py = (args) => spawnSync(PY, args, {cwd: ROOT, stdio: 'inherit'}).status;

const main = async () => {
  const args = parseArgs(process.argv.slice(2));
  const projectDir = path.resolve(ROOT, args.project);
  const planPath = path.join(projectDir, 'animation.json');
  if (!fs.existsSync(planPath)) die(`No animation.json in ${projectDir}`);

  if (py([path.join('scripts', 'validate_project.py'), projectDir]) !== 0) die('validation errors (see above).');
  const plan = JSON.parse(fs.readFileSync(planPath, 'utf8').replace(/^﻿/, ''));
  const outDir = path.join(projectDir, 'output');
  fs.mkdirSync(outDir, {recursive: true});
  fs.mkdirSync(path.join(projectDir, 'cache'), {recursive: true});
  const inputProps = {plan, mode: args.mode};
  fs.writeFileSync(path.join(projectDir, 'cache', 'props.json'), JSON.stringify(inputProps));

  if (args.mode === 'final' && !args.scenes && fs.existsSync(path.join(outDir, 'final.mp4')) && !args.overwrite) {
    die('output/final.mp4 already exists. Pass --overwrite only if you intend to replace it.');
  }

  const t0 = Date.now();
  const serveUrl = await bundle({
    entryPoint: path.join(ROOT, 'src', 'index.ts'),
    publicDir: projectDir,
    onProgress: () => {},
  });
  console.log(`Bundled in ${((Date.now() - t0) / 1000).toFixed(1)}s`);
  const composition = await selectComposition({serveUrl, id: 'Short', inputProps});
  const {fps} = composition;
  const spec = registry.modes[args.mode];
  const common = {composition, serveUrl, inputProps, logLevel: 'warn'};
  const toF = (s) => Math.round(s * fps);

  if (args.mode === 'stills') {
    const stillsDir = path.join(outDir, 'stills');
    fs.rmSync(stillsDir, {recursive: true, force: true});
    fs.mkdirSync(stillsDir, {recursive: true});
    const selected = plan.scenes.filter((s) => !args.scenes || args.scenes.includes(s.id));
    const t1 = Date.now();
    for (const s of selected) {
      const times = [s.startSec + s.durationSec * 0.5, s.startSec + Math.max(s.durationSec * 0.85, s.durationSec - 0.2)];
      for (const t of times) {
        const frame = Math.min(composition.durationInFrames - 1, toF(t));
        const file = path.join(stillsDir, `${s.id}_${(frame / fps).toFixed(2)}s.png`);
        await renderStill({...common, frame, output: file, imageFormat: 'png'});
      }
    }
    console.log(`Rendered ${selected.length * 2} stills in ${((Date.now() - t1) / 1000).toFixed(1)}s`);
    if (py([path.join('scripts', 'make_contact_sheet.py'), '--images', stillsDir]) !== 0) die('contact sheet failed');
    return;
  }

  const media = {
    ...common,
    codec: 'h264',
    audioCodec: 'aac',
    crf: spec.crf,
    pixelFormat: 'yuv420p',
    colorSpace: 'bt709', // limited-range BT.709: what YouTube expects (avoids full-range yuvj420p)
    enforceAudioTrack: true,
    ...(args.concurrency ? {concurrency: args.concurrency} : {}),
  };

  const jobs = [];
  if (args.scenes) {
    for (const id of args.scenes) {
      const idx = plan.scenes.findIndex((s) => s.id === id);
      if (idx < 0) die(`Scene ${id} not found in animation.json`);
      const s = plan.scenes[idx];
      const tr = s.transitionOut;
      const tail = plan.scenes[idx + 1] && tr && tr.preset !== 'cut' ? tr.durationSec || 0 : 0;
      const start = toF(s.startSec);
      const end = Math.min(composition.durationInFrames - 1, toF(s.startSec + s.durationSec + tail) - 1);
      jobs.push({file: path.join(outDir, `${id}-${args.mode}.mp4`), frameRange: [start, end], partial: true});
    }
  } else {
    jobs.push({file: path.join(outDir, `${args.mode}.mp4`), frameRange: null, partial: false});
  }

  let failed = false;
  for (const job of jobs) {
    const t1 = Date.now();
    await renderMedia({...media, outputLocation: job.file, ...(job.frameRange ? {frameRange: job.frameRange} : {})});
    const secs = (Date.now() - t1) / 1000;
    console.log(`Rendered ${path.relative(ROOT, job.file)} in ${secs.toFixed(1)}s`);
    const check = [path.join('scripts', 'check_video.py'), job.file, '--expect', args.mode, '--project', projectDir];
    if (job.partial) check.push('--partial');
    if (py(check) !== 0) failed = true;
  }
  if (failed) die('technical check failed (see FAIL lines).');
};

main().catch((err) => die(err?.stack || String(err)));
