from can_jd import *
import time
# CAN
port = 'can1'
id = 10
can_jd = CANJD(port, id)

#restore parameters
can_jd.restore_parameters()

print("Parameters restored!, you can reboot now")