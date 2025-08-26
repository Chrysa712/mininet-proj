# Firewall Implementation with Mininet and POX Controller

## Project Overview

This project implements a simple firewall using Software-Defined Networking (SDN) principles with Mininet network emulator and POX Controller. The assignment is part of the "Internet Technologies and Services" course at Athens University of Economics and Business.

## Network Topology

- **1 Switch** (S1)
- **5 Hosts** (H1-H5) with IP addresses 10.0.0.1/24 to 10.0.0.5/24
- **Remote POX Controller** managing the switch

## Firewall Rules

The firewall implements the following traffic control rules:

| Source IP | Destination IP | Protocol | Action |
|-----------|----------------|----------|--------|
| any ipv4  | any ipv4       | UDP      | Accept (forward to destination port) |
| any       | any            | ARP      | Accept (flooding) |
| any ipv4  | any ipv4       | other    | Drop |

## Project Structure

```
├── Topo5hosts.py      # Network topology definition
├── myController.py    # POX controller with firewall logic
└── README.md          # This file
```

## Requirements

- Mininet
- POX Controller
- Python 2.7 or 3.x
- OpenFlow 1.3 support

## Usage

1. **Start POX Controller** (in separate terminal):
   ```bash
   ./pox.py myController
   ```

2. **Run Mininet with topology**:
   ```bash
   sudo python Topo5hosts.py
   ```

3. **Test the network** (in Mininet CLI):
   ```
   mininet> dump
   mininet> net
   mininet> pingall
   mininet> dpctl dump-flows -O Openflow13 s1
   mininet> iperfudp
   ```

## Expected Behavior

- **ARP packets**: Allowed and flooded to all ports
- **UDP packets**: Forwarded to correct destination based on IP header
- **ICMP/TCP packets**: Dropped by firewall rules

## Assignment Details

- **Course**: Internet Technologies and Services
- **Instructor**: Anna Kefala
- **Academic Year**: 2024-2025
- **Due Date**: June 27, 2025
- **Submission**: Individual work via e-class

## Documentation

The complete project documentation includes:
- System architecture explanation
- Firewall rules implementation details
- Test results with screenshots
- Troubleshooting notes
