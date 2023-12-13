from can_jd import *
import time
# CAN
port = 'can1'
id = 10
can_jd = CANJD(port, id)


SAMPLES = 100 

print("Calibrating...")

avgx, avgy = can_jd.calibrate_xy(SAMPLES)
print(avgx, avgy)

# save parameters
can_jd.save_parameters()

print("Calibration done!")
