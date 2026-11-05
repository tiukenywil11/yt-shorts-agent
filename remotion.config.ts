// Used by `npm run studio` only. scripts/render.mjs passes its own options to the Node APIs.
// Studio preview of a project: set SHORT_PROJECT=projects/<id> and pass --props=projects/<id>/cache/props.json
import {Config} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
if (process.env.SHORT_PROJECT) {
  Config.setPublicDir(process.env.SHORT_PROJECT);
}
