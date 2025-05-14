#!/usr/bin/env bash
set -euo pipefail

# ── Configurable variables ─────────────────────────────────────────────────────
MCAST_SENDER_PREFIX="${MCAST_SENDER_PREFIX:-234.0.0}"    # original multicast group network
MCAST_REWRITE_PREFIX="${MCAST_REWRITE_PREFIX:-238.0.0}"  # rewritten source-network (for reference)
THROUGHPUT="${THROUGHPUT:-10M}"                          # e.g. 10M, 100M
PORT_BASE="${PORT_BASE:-5001}"                           # starting port for streams
INTERVAL="${INTERVAL:-1}"                                # iperf reporting interval (s)

# ── Helpers ───────────────────────────────────────────────────────────────────
get_ip() {
  docker exec "$1" sh -c "ip -4 addr show dev eth1 \
    | awk '/inet /{print \$2}' | cut -d'/' -f1"
}

cleanup() {
  pkill -P $$ || true
  exit
}
trap cleanup INT TERM

# ── Start receivers on iperf3 ──────────────────────────────────────────────────
for i in 1 2; do
  GROUP="${MCAST_SENDER_PREFIX}.${i}"
  PORT=$((PORT_BASE + i - 1))
  docker exec iperf3 \
    iperf -s -u -B "$GROUP" -p "$PORT" -i "$INTERVAL" &
done

# ── Start senders on iperf1 & iperf2 ───────────────────────────────────────────
for i in 1 2; do
  GROUP="${MCAST_SENDER_PREFIX}.${i}"
  PORT=$((PORT_BASE + i - 1))
  SRC_IP=$(get_ip "iperf${i}")
  docker exec "iperf${i}" \
    iperf -u -c "$GROUP" -B "$SRC_IP" -p "$PORT" \
          -b "$THROUGHPUT" -i "$INTERVAL" &
done

wait
