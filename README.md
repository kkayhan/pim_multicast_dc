# mcjoin

`mcjoin` is a lightweight CLI tool for IPv4 multicast source and receiver management.

> **Note:** Tested on Linux Kernel **6.8.0-59-generic**. Known IGMP-join issues with Kernel **5.x**.

## Features

* Source (`-s`) multicast traffic
* Join multicast groups with or without specific sources

## Prerequisites

* Linux system with kernel **6.8.0-59-generic** or newer
* `mcjoin` installed and in your `$PATH`

## Usage

```bash
mcjoin [options] <interface> <group>
```

### Options

* `-s`
  Start sourcing multicast traffic.
* `-i <interface>`
  Network interface to use (e.g., `eth1`).

## Examples

### 1. Start as a Source

```bash
mcjoin -s -i eth1 234.0.0.1
```

Starts sourcing multicast traffic to group `234.0.0.1` on `eth1`.

### 2. Join a Group (Any Source)

```bash
mcjoin -i eth1 234.0.0.1
```

Joins multicast group `234.0.0.1` on `eth1` (accepts traffic from any source).

### 3. Join a Group (Specific Source)

```bash
mcjoin -i eth1 192.168.100.2,234.0.0.1
```

Joins multicast group `234.0.0.1` on `eth1`, filtering traffic from source `192.168.100.2`.
