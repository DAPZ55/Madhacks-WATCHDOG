# 811 Vision AR: project guide for agents

Read this first. It is the map of the repo; the code comments hold the detail.

## What it is

A hackathon prototype. An overhead picture of painted "811" utility markings goes in; an Arduino
UNO Q turns it into a metric map; iPhones show that map as AR on the real ground, with pipes drawn
below the surface.

```
picture (upload or webcam) -> UNO Q: find tags, flatten, find paint, trace lines -> candidate
candidate -> human review -> published map revision -> iPhones poll it -> AR on the floor
```

No cloud, no internet at run time. The Mac is only for writing code and pushing it.

## Safety rules (never break these)

1. Never output or imply "safe to dig" or "clear". Not in UI text, labels, API fields, or comments.
2. Depth is never measured. `depth_m` stays `null`. Pipes are drawn at a display-only depth
   (state minimum-cover rule) and must stay labeled as simulated.
3. Two evidence sources that disagree (paint vs uploaded layout) are both kept and both shown.
   Never average or merge them.
4. A `NO/<owner>` marking means that owner reports no facilities. It is not an all-clear.
5. Failures must be visible to users: lost tracking, stale map, moved tags, dead monitoring.
6. Low-confidence recognition is stored as "unread" and sent to review, never guessed.

## Hardware and network

| Thing | Detail |
|---|---|
| Edge board | Arduino UNO Q, Debian 13, aarch64, Python 3.13. Host `Madhacks16`, user `arduino` |
| Camera | Logitech Brio 105 on a USB-C hub. Skip `qcom-venus-*` video nodes (SoC codec, not a camera) |
| Address | `http://Madhacks16.local:8000` (mDNS). Plain HTTP on purpose |
| Network today | Board, Mac, phone all join the iPhone hotspot |
| Own network | Profile `811-site` (SSID `811-Vision`, board is `10.42.0.1`). Created, switch not yet proven |
| Phone | iPhone 17 Pro Max (LiDAR). Device id in the build commands below |
| Anchor tags | 4 printed ArUco tags, dictionary `ARUCO_MIP_36h12`, ids 0-3 named A1-A4, black square 0.145 m |

SSH is key-based, no sudo. Quote remote paths: `ssh arduino@Madhacks16.local '~/vision811/...'`.

## Repo layout

```
edge/                 runs on the UNO Q (and on the Mac for dev)
  server.py           FastAPI app: all HTTP endpoints, camera, modes, publishing
  vision.py           scan(): picture -> utility polylines in site meters
  tags.py             ArUco detect, survey() of tag layout, focal-length knob
  admin.html          web admin panel served at /
  vision811.service   systemd user unit (starts server at boot)
  setup_wifi.sh       one-time creation of the board's own Wi-Fi profile (interactive)
ios/                  xcodegen project, two apps, one design system
  project.yml         targets: Vision811 (AR), Vision811Admin (control panel)
  App/                AR app: Vision811App.swift, SiteMap.swift, SiteTransform.swift,
                      Jurisdiction.swift, jurisdictions.json, A1-A4.png
  Admin/AdminApp.swift  admin app, talks to the board API
  Shared/Theme.swift  design tokens and components for both apps; Shared/Fonts/
tools/                make_tags.py, make_street_scenes.py, marking_symbols.py, test_transform.sh
tests/                test_vision.py, test_streets.py, transform_check/main.swift
sample_data/          map.json (dev copy), streets/ (synthetic scenes + ground truth), tags/
deploy.sh             push code to the board over SSH and restart its service
run.sh                run the server on the Mac
```

`reports/` and `research_notes/` are the owner's notes, not code.

## Coordinate frames

- **Site frame S** (the only frame stored): meters, right-handed. A1 is the origin, +X points to A2,
  +Y lies on the ground to the left of +X seen from above, +Z up. Ground is z = 0.
- **Camera pixels**: converted to S with a homography from the 4 tag centers (`vision.py`).
- **ARKit world**: each phone fits its own transform from S (`SiteTransform.swift`). Tag positions
  used for the fit are where the camera-to-tag sight line hits the LiDAR floor, not ARKit's raw
  size-based estimate.

Tag positions in S come from `tags.survey()`. Moving a tag or the camera invalidates them: re-survey.

## Edge pipeline (`edge/vision.py`)

1. Detect tags; need all 4 or the scan is rejected.
2. Warp to a top-down raster at 200 px/m covering the tags plus 0.3 m margin.
3. HSV threshold per APWA color (ranges in `COLORS`, knobs `MIN_SAT`, `MIN_VAL`).
4. Group strokes by dilation (`GAP_M` = 0.08 m) but measure on real paint pixels.
5. Trace each group's centerline as the longest path through paint cells (handles bends; a
   branching mark keeps only its longest run).
6. Output utilities in map schema with `depth_m: null`.

Classical vision only. No ML model is integrated yet (a small symbol classifier is planned).

## Map object (schema 1.2)

`sample_data/map.json`, served at `/api/v1/maps/latest`. Key fields:

- `map_revision` (int, bumps on every publish), `published_at`, `publish_note`
- `anchors[]`: `id`, `position_m` [x, y, 0], `size_m`
- `model_scale`: 1.0 real size; 0.1 means a 1:10 scale model (phones scale depths, zones, labels)
- `utilities[]`: `utility_id`, `utility_class`, `marking_color`,
  `surface_marking.centerline_m` and/or `uploaded_layout.centerline_m`, `depth_m` (null),
  `depth_status`, `display_depth_m` + `display_depth_status: "hypothetical"`, `evidence_relationship`
- Added at reply time, not stored: `site_mode` (`scan` | `monitor`), `alerts[]`

Every publish goes through `_publish()` in `server.py`: new revision, copy into
`sample_data/history/`, atomic replace. Never write `map.json` any other way.

## Modes

- **scan** (default): aim once, `POST /api/v1/scan_site` surveys tags and scans markings from the
  same frames, operator approves, camera is then not needed. Phones check tag spacing themselves.
- **monitor**: camera stays aimed. A watchdog thread checks the tags every 2 s; `alerts` reach
  every phone with the next map poll (tag moved, view blocked, camera offline). Refuses to start
  unless all 4 tags are visible.

## API (all under `http://<board>:8000`)

Read-only, used by phones: `GET /api/v1/maps/latest`, `GET /api/v1/maps/{revision}`,
`GET /api/v1/status`, `GET /api/v1/history`.

Scan and review: `POST /api/v1/scan` (raw image body, `?model_scale=`), `POST /api/v1/capture`,
`POST /api/v1/scan_site`, `GET /api/v1/candidate`, `GET /api/v1/scan/preview`,
`POST /api/v1/publish`, `POST /api/v1/reject`, `POST /api/v1/rollback?revision=`.

Camera and tags: `GET /camera` (MJPEG with overlay, `?state=&scale=`), `GET /api/v1/snapshot`
(one JPEG), `GET /api/v1/tags`, `GET /api/v1/survey`, `POST /api/v1/survey` (saves and clears
utilities).

Board: `POST /api/v1/mode?mode=`, `GET|POST /api/v1/network`, `POST /api/v1/network/boot`,
`POST /api/v1/power?action=`, `GET /api/v1/mock` (dev helper), `GET /` (web admin).

Errors return `{"detail": "<plain explanation>"}`; clients show that text.
There is no authentication (owner's choice for the demo). Private network only.

## Phone apps

- **Vision811** (worker): polls the map every 3 s, aligns to tags, draws ground lines, merged orange
  zebra tolerance zones, pipes at simulated depth, length labels. State picker (WI, NY, CHI, TX)
  changes labels, tolerance width, and cover depth from `jurisdictions.json`. Recalibrate button.
- **Vision811Admin** (supervisor): tabs Site, Scan, Live, History, System over the API above.
- Both use `ios/Shared/Theme.swift`: dark asphalt field, square corners, hairlines, safety orange
  for actions, hazard yellow for warnings. Utility colors are data, never chrome.
- State rules live once, in `ios/App/jurisdictions.json`; the server reads the same file. Entries
  with `"verified": false` are typical practice, not confirmed regulation.

## Commands

```bash
# checks (run after any vision or transform change)
.venv/bin/python tests/test_vision.py
.venv/bin/python tests/test_streets.py
./tools/test_transform.sh

# regenerate synthetic scenes for the current tag layout
.venv/bin/python tools/make_street_scenes.py

# push to the board and restart its service (board keeps its own map and history)
./deploy.sh

# iOS: regenerate project, build, install (scheme Vision811 or Vision811Admin)
cd ios && xcodegen
xcodebuild -project Vision811.xcodeproj -scheme Vision811 \
  -destination 'id=00008150-000D05A40AE8C01C' -allowProvisioningUpdates -derivedDataPath build build
xcrun devicectl device install app --device 00008150-000D05A40AE8C01C \
  build/Build/Products/Debug-iphoneos/Vision811.app
```

On the Mac, a process started by an agent cannot open the camera (macOS permission). Camera work
is tested on the board, or by the owner from their own terminal.

## Conventions

- Smallest change that works. No new dependencies or abstractions without need.
- Deliberate shortcuts carry a `ponytail:` comment naming the ceiling and the upgrade path.
- Calibration values are named knobs at the top of their file (HSV ranges, focal length,
  thresholds). Tune them, do not hard-code new ones inline.
- Non-trivial logic leaves one runnable check in `tests/`.
- Tap targets 48 pt minimum; warnings never rely on color alone.
- Commit after each working step. Never push without being asked.

## Known limits

- Color detection is fooled by colored surfaces (the venue carpet) and road paint (double yellow).
- Scenes in `sample_data/streets/` are synthetic. `marks_*.jpg` contain symbols and text that the
  scanner currently misreads as extra lines; they are test data for the planned symbol model.
- Lens distortion is not corrected; focal length is from the camera's spec sheet (confirmed against
  one tape measurement).
- One tag decodes unreliably at steep angles; visibility is judged over 5 frames.
- Two servers can exist (Mac dev and board). Phones default to the board. Keep one source of truth.
- Layout import with discrepancy flagging exists in the schema and phone rendering, but the edge
  has no import endpoint yet.
- The UNO Q's microcontroller side is unused.

## Source documents

- Original specification: `~/Desktop/811_Vision_AR_Technical_Specification.md` (not in this repo).
  This project deviates from it only where noted above; its safety rules are binding.
