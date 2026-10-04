# Vendored wheel provenance

- Upstream: `kaggle-environments` 1.32.7, (c) Kaggle Inc, Apache License 2.0
  - PyPI: https://pypi.org/project/kaggle-environments/1.32.7/
  - Source: https://github.com/Kaggle/kaggle-environments
- Local file: `kaggle_environments-1.32.7+nodeps-py3-none-any.whl` (787 KB)
- Repackaging (engine code untouched):
  1. Removed all `Requires-Dist` lines from METADATA. Rationale: the full
     upstream dependency set (pygame, jax, open_spiel, transformers, litellm,
     pettingzoo, ...) is not required to run headless kaggriculture episodes
     and several members fail to build from source on modern CPython (e.g.
     pygame on 3.14). Only the four runtime deps actually imported by the
     headless core are installed (see ../requirements.txt).
  2. Stripped non-code assets (visualizer HTML bundles, bundled JS, game
     data files, ~136 MB uncompressed). The kaggriculture `html_renderer`
     degrades gracefully (returns an empty string) when the visualizer file
     is missing; episode dynamics are unaffected.
  3. Added `+nodeps` local version tag per PEP 440 so the build is clearly
     distinguishable from the official release.
- Rebuild: the archive is a plain zip round-trip of the official wheel with
  the edits above; RECORD hashes were regenerated for the kept files.
- License compliance: Apache-2.0 permits redistribution with attribution;
  this notice plus the LICENSE file inside the wheel provide it.
