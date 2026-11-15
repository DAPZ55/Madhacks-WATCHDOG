#!/bin/sh
# One-time setup of the UNO Q's own Wi-Fi network ("811-Vision"), for running with no phone hotspot
# and no internet. Run ON THE BOARD, interactively, so the password is typed by you and never stored
# in the repo:
#     ssh -t arduino@Madhacks16.local ~/vision811/edge/setup_wifi.sh
# Creates the network profile only. It does NOT switch to it: use the admin panel's Network section.
set -e
NAME=811-site
SSID=811-Vision

printf "Password for Wi-Fi network %s (8-63 characters): " "$SSID"
stty -echo; read -r PASS; stty echo; echo
[ ${#PASS} -ge 8 ] && [ ${#PASS} -le 63 ] || { echo "Password must be 8-63 characters. Nothing changed."; exit 1; }

nmcli connection delete "$NAME" >/dev/null 2>&1 || true
# 2.4 GHz (band bg): longest range, every phone supports it. "shared" = board hands out addresses
# and is always 10.42.0.1. autoconnect off: joining the hotspot stays the default at boot.
nmcli connection add type wifi ifname wlan0 con-name "$NAME" autoconnect no ssid "$SSID" \
  802-11-wireless.mode ap 802-11-wireless.band bg \
  ipv4.method shared ipv4.addresses 10.42.0.1/24 ipv6.method disabled \
  wifi-sec.key-mgmt wpa-psk wifi-sec.psk "$PASS" >/dev/null
echo "Created network profile '$NAME' (SSID $SSID). Board address on it: 10.42.0.1"
echo "Switch to it from the admin panel: Network > Switch to own network."
