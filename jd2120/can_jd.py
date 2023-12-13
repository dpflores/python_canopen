import canopen
import os

EDS_FILE = os.path.dirname(os.path.realpath(__file__)) +\
    '/JD2xxx_v1.0.eds'
# Cargar archivo de configuración de dispositivo CANopen
g = 9.81

accel_resolution = g/1000
gyro_resolution = 0.1       # degrees/s

slope_resolutions = {"10": 0.01, "100": 0.1, "1000": 1}


class CANJD():
    def __init__(self, port='can1', node_id=10, speed0=0):
        network = canopen.Network()
        network.connect(bustype='socketcan', channel=port)
        self.node = network.add_node(node_id, EDS_FILE)
        self.slope_resolution = slope_resolutions[str(
            self.node.sdo[0x6000].raw)]
        
        self.speed = speed0
        self.slope_x = 0
        self.slope_y = 0

    def get_prop_accel(self):
        x = self.node.sdo[0x3403].raw * accel_resolution
        y = self.node.sdo[0x3404].raw * accel_resolution
        z = self.node.sdo[0x3405].raw * accel_resolution
        return x, y, z

    def get_gyro(self):
        x = self.node.sdo[0x3400].raw * gyro_resolution
        y = self.node.sdo[0x3401].raw * gyro_resolution
        z = self.node.sdo[0x3402].raw * gyro_resolution
        return x, y, z

    def get_slopes(self):
        # angle = (value - offeset)*resolution
        x = (self.node.sdo[0x6010].raw  - self.node.sdo[0x6012].raw) * self.slope_resolution
        y = (self.node.sdo[0x6020].raw  - self.node.sdo[0x6022].raw) * self.slope_resolution
        return x, y
    
    def calibrate_xy(self, samples = 10):
        sumx = 0
        sumy = 0
        for i in range(samples):
            sumx += self.node.sdo[0x6010].raw 
            sumy += self.node.sdo[0x6020].raw

        avgx = int(sumx/samples)
        avgy = int(sumy/samples)

        
        # Setting the preseting
        self.node.sdo[0x6012].raw = avgx
        self.node.sdo[0x6022].raw = avgy

        return avgx* self.slope_resolution, avgy* self.slope_resolution
    
    def save_parameters(self):
        # string 'save' converted to hexadecimal following ascii
        self.node.sdo[0x1010][0x3].raw = 0x65766173
    

    def restore_parameters(self):
        # string 'load' converted to hexadecimal following ascii
        self.node.sdo[0x1011][0x3].raw = 0x64616f6c
        
   