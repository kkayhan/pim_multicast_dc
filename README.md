# pim_multicast_dc

mcjoin is used for multicast source and receiver.
Had issues with igmp-joins with Linux Kernel 5.x
Currently using 6.8.0-59-generic


Examples for mcjoin

Start sourcing (-s) multicast traffic
|| mcjoin -s -i eth1 234.0.0.1

Join to a specific group without specific source
|| mcjoin -i eth1 234.0.0.1

Join to a specific group with specific source
|| mcjoin -i eth1 192.168.100.2,234.0.0.1