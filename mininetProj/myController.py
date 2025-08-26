from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Firewall(object):
    """
    A Firewall object is created for each switch that connects.
    A Connection object for that switch is passed to the __init__ function.
    """

    def __init__(self, connection):
        # Keep track of the connection to the switch so that we can send it messages.
        self.connection = connection

        # This binds our PacketIn event listener
        connection.addListeners(self)

        # Install firewall rules

        # Rule 1: Allow ARP (Flood)
        self.connection.send(of.ofp_flow_mod(
            action=of.ofp_action_output(port=of.OFPP_FLOOD),
            priority=3,
            match=of.ofp_match(dl_type=0x0806)  # ARP packets
        ))
        log.info("Rule added: Allow ARP (Flood)")

        # Rule 2: Allow UDP (Forward to destination)
        self.connection.send(of.ofp_flow_mod(
            action=of.ofp_action_output(port=of.OFPP_CONTROLLER),  # Send to controller to determine destination port
            priority=2,
            match=of.ofp_match(dl_type=0x0800, nw_proto=17)  # IPv4 + UDP
        ))
        log.info("Rule added: Allow UDP (Forward)")

        # Rule 3: Drop all other IP traffic
        self.connection.send(of.ofp_flow_mod(
            priority=1,
            match=of.ofp_match(dl_type=0x0800)  # IPv4
        ))
        log.info("Rule added: Drop all other IP traffic")

    def _handle_PacketIn(self, event):
        """
        Handle packets that match the UDP rule (sent to the controller).
        """
        packet = event.parsed  # Parsed packet
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        packet_in = event.ofp  # The actual ofp_packet_in message

        # Handle UDP packets to forward them to the correct port
        ip_packet = packet.payload
        if hasattr(ip_packet, 'protocol') and ip_packet.protocol == 17:  # UDP protocol
            udp_packet = ip_packet.payload
            destination_ip = ip_packet.dstip
            log.info(f"Handling UDP packet for destination: {destination_ip}")

            # Determine destination port based on destination IP
            dst_port = self.get_port_for_ip(destination_ip)
            if dst_port is not None:
                log.info(f"Forwarding UDP packet to port {dst_port}")
                msg = of.ofp_packet_out()
                msg.data = packet_in
                msg.actions.append(of.ofp_action_output(port=dst_port))
                msg.in_port = event.port
                self.connection.send(msg)
            else:
                log.warning(f"No port found for IP {destination_ip}, dropping packet")

    def get_port_for_ip(self, ip):
        """
        Map destination IPs to ports.
        This should match the topology defined in Mininet.
        """
        ip_to_port = {
            "10.0.0.1": 1,
            "10.0.0.2": 2,
            "10.0.0.3": 3,
            "10.0.0.4": 4,
            "10.0.0.5": 5,
        }
        return ip_to_port.get(str(ip), None)


def launch():
    """
    Starts the component
    """
    def start_switch(event):
        log.debug("Controlling %s" % (event.connection,))
        Firewall(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
