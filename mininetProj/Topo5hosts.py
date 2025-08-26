#!/usr/bin/python3
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.topo import Topo


class Topo5hosts(Topo):
    def __init__(self):
        # Initialize the topology
        Topo.__init__(self)

        # Add switch
        s1 = self.addSwitch('s1')

        # Add hosts
        h1 = self.addHost("h1", mac="00:00:00:00:00:01", ip="10.0.0.1/24")
        h2 = self.addHost("h2", mac="00:00:00:00:00:02", ip="10.0.0.2/24")
        h3 = self.addHost("h3", mac="00:00:00:00:00:03", ip="10.0.0.3/24")
        h4 = self.addHost("h4", mac="00:00:00:00:00:04", ip="10.0.0.4/24")
        h5 = self.addHost("h5", mac="00:00:00:00:00:05", ip="10.0.0.5/24")

        # Connect hosts to the switch
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s1)
        self.addLink(h5, s1)

# Topology registration for Mininet CLI
topos = {'topo5hosts': Topo5hosts}

def configure():
    topo = Topo5hosts()
    net = Mininet(topo=topo, controller=RemoteController)
    net.start()

    CLI(net)

    net.stop()


if __name__ == "__main__":  # block code is executed when the script is run directly, not through sudo mininet
	configure()
