from can_load import LoadController
import time
# CAN
port = 'can0'
id = 10
loads = LoadController(port, id)


while True:

    w1, w2, wt = loads.get_loads()

    print(f'{{"w1":{round(w1,4)}, "w2":{round(w2,4)}}}')
    time.sleep(0.1)
