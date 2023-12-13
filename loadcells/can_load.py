import canopen
import os

EDS_FILE = os.path.dirname(os.path.realpath(__file__)) +\
    '/dual-loadcells.eds'


class LoadController():
    def __init__(self, port='can0', node_id=7):
        network = canopen.Network()
        network.connect(bustype='socketcan', channel=port)
        self.node = network.add_node(node_id, EDS_FILE)
      

    def get_loads(self):
        w1 = self.node.sdo[0x6500][0x1].raw
        w2 = self.node.sdo[0x6500][0x2].raw
        wt = self.node.sdo[0x6500][0x3].raw
        return w1, w2, wt