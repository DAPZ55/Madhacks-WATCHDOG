#!/bin/sh
# Push code to the UNO Q and restart its service. Usage: ./deploy.sh [user@host]
# The board's own published map and scan outputs are left alone (they are the board's data).
HOST="${1:-arduino@Madhacks16.local}"
cd "$(dirname "$0")" || exit 1
COPYFILE_DISABLE=1 tar czf - --no-xattrs --no-mac-metadata \
  --exclude .git --exclude .venv --exclude ios/build --exclude 'ios/*.xcodeproj' --exclude __pycache__ \
  --exclude .impeccable --exclude reports --exclude research_notes --exclude .DS_Store \
  --exclude sample_data/map.json --exclude 'sample_data/scan*' --exclude sample_data/history \
  . | ssh "$HOST" 'mkdir -p ~/vision811 && tar xzf - -C ~/vision811' || exit 1
# First deploy only: seed the board's map from the Mac's.
ssh "$HOST" 'test -f ~/vision811/sample_data/map.json' || scp -q sample_data/map.json "$HOST:vision811/sample_data/map.json"
ssh "$HOST" 'systemctl --user restart vision811 2>/dev/null && echo "service restarted" || echo "service not installed yet"'
