#!/bin/sh
# Runs the site-transform check on the Mac (no phone needed).
cd "$(dirname "$0")/.." || exit 1
swiftc ios/App/SiteTransform.swift tests/transform_check/main.swift -o "${TMPDIR:-/tmp}/transform_check" && "${TMPDIR:-/tmp}/transform_check"
