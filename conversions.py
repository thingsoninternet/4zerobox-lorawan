import math

ref_table = [329.5,247.7,188.5,144.1,111.3,86.43,67.77,53.41,42.47,33.90,27.28,22.05,17.96,14.69,12.09,10.00,8.313,
              6.940,5.827,4.911,4.160,3.536,3.020,2.588,2.228,1.924,1.668,1.451,1.266,1.108,0.9731,0.8572,0.7576]
min_temp = -50
delta_temp = 5



def acceleration_module(x, y, z):
    # convert x,y,z acceleration components to acceleration module in g (9.8 m/s^2)
    return math.sqrt(math.pow(x,2)+math.pow(y,2)+math.pow(z,2))/9.8


def float_to_2bytes(v):
    # convert a float value between 0 and 256 in 2 bytes,
    # one byte for integer part and one byte for decimal part
    if v < 0:
        return bytearray([0, 0])
    if v > 256:
        return bytearray([255,255])
    i = int(v)
    d = int((v-i)*100)
    return bytearray([i, d])


def format_payload(acc, temp, power):
    payload = bytearray(6)
    payload[0:2] = float_to_2bytes(acc)
    payload[2:4] = float_to_2bytes(temp)
    payload[4:6] = float_to_2bytes(power)
    return payload