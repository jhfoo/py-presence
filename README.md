# Purpose
This app scans the immediate network for host presence, defined by mac address.

# Implementation
2 methods of scan available:
1. ~~nmap (to be implemented)~~
2. scapy (implementing)

nmap should be a little faster

# Requirements
1. scapy: Sudo installed and configured to be executable to the user.
2. ~~nmap: nmap installed. No sudo required. Slightly faster.~~

# Strategy
## scapy runs authoritative sweeps of the network
1. GOOD: authoritative
3. BAD: slow - scans entire network

## ping polls for device status changes
1. GOOD: fast - monitor only addresses of interest
2. BAD: less authoritative - MAC can be assigned new IP