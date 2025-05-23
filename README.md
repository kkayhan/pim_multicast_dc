![mcast1](./mcast1.png)

# mcjoin

`mcjoin` is a minimal CLI utility for simulating multicast sources and receivers.

### Supported Flags

- `-d` — Run as a background daemon  
- `-s` — Run the tool as the multicast source , if not set it acts as client 
- `-t` — Set the TTL value  
- `-i` — Specify the network interface

> **Note:** Tested on Linux Kernel **6.8.0-59-generic**. Known IGMP-join issues with Kernel **5.x**.

## Examples

### 1. Start as a Source

```bash
mcjoin -s -t 20 -i eth1 234.0.0.1
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

Joins multicast group `234.0.0.1` on `eth1`, from specific source `192.168.100.2`.
