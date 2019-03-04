import streams
import gpio
import conversions as cnv
from toi.fourzerobox import fourzerobox
from microchip.rn2483 import rn2483
import sfw
# uncomment the following line if you want to use the 10 DoF Click
# from bosch.bno055 import bno055

# insert OTAA credentials here
deveui = ''
appeui = ''
appkey = ''

# relays init status
status1 = LOW
status2 = LOW

# define a function to set relay status on downlink messages
def set_relays(payload):
    global status1, status2
    
    if payload[0] and status1 == LOW:
        print(" + switching relay 1 ON")
        status1 = HIGH
        fzbox.relay_on(1)
    elif not payload[0] and status1 == HIGH:
        print(" + switching relay 1 OFF")
        status1 = LOW
        fzbox.relay_off(1)
    else:
        print(" + relay 1 already in the correct state")
    
    if payload[1] and status2 == LOW:
        print(" + switching relay 2 ON")
        status2 = HIGH
        fzbox.relay_on(2)
    elif not payload[1] and status2 == HIGH:
        print(" + switching relay 2 OFF")
        status2 = LOW
        fzbox.relay_off(1)
    else:
        print(" + relay 2 already in the correct state")

# configure watchdog in normal mode with a 60 seconds timeout
sfw.watchdog(0, 60000)

# open the default serial port, the output will be visible in the serial console
streams.serial()

try:
    
    # create FourZeroBox instance
    fzbox = fourzerobox.FourZeroBox(i2c_clk=100000)
    
    # set magenta led on
    fzbox.set_led('M')
    
    # set relays status
    if status1 == LOW:
        fzbox.relay_off(1)
    else:
        fzbox.relay_on(1)

    if status2 == LOW:
        fzbox.relay_off(2)
    else:
        fzbox.relay_on(1)
    
    
    
    # init LoRa click (Mikrobus Slot 1)
    # switch SW1 pins 3, 5 and 11 shall be set in ON position
    rn2483.init(SERIAL2, None, None, D42, join_lora=False)
    rn2483.config(appeui, appkey, deveui)
    
    ################
    ## init sensors
    # ntc temperature sensor on channel "Sens1"
    fzbox.config_adc_resistive(1, 2, 0)
    fzbox.set_conversion_resistive(1, cnv.min_temp, cnv.ref_table, cnv.delta_temp, 0, -100)
    
    # current probe on channel "Cur1"
    fzbox.config_adc_current(1, 2, 7)
    fzbox.set_conversion_current(1, 100, 5, 2000, 220)
    
    # uncomment the following lines if you want to use a 10 DoF Click
    # # 10 DoF click (Mikrobus Slot 2)
    # bno = bno055.BNO055(I2C0, clk=100000)
    # bno.start()
    # bno.init('imu')
    
    # set blue led on
    fzbox.set_led('B')
    # 
except Exception as e:
    print(e)


while True:
    try:
        print("join LoRa network...")
        if rn2483.join():
            print("...succeded!")
            # set green led on
            fzbox.set_led('G')
            break
        else:
            print("...failed :(")
    except Exception as e:
        print(e)
        print("...failed :(")
    
    sfw.kick()
    sleep(5000)

while True:
    try:
        
        acc_m = 0

        # # uncomment the following lines if you want to use a 10 DoF Click
        # x, y, z = bno.get_acc()
        # acc_m = cnv.acceleration_module(x, y, z)

        temperature = fzbox.read_resistive(1)
        power = fzbox.read_power(1)
        
        print('-'*30)
        print("acceleration: %.2f [g]"% acc_m)
        print("temperature: %.2f [C]"% temperature)
        print("power: %.2f [W]"% power)
        
        payload = cnv.format_payload(acc_m, temperature, power)
        res = rn2483.tx_uncnf(payload)

        # handle downlink messages
        if type(res) == PTUPLE:
            dl_msg = res[1]
            print("received a downlink message:",[e for e in dl_msg])
            
            if len(dl_msg) == 2:
                set_relays(dl_msg)
            else:
                print("invalid message, expecting 2 bytes")
        print('-'*30)
        
        fzbox.reverse_pulse('G',100)
        
    except rn2483Exception as e:
        print(e)
        fzbox.reverse_pulse('Y',100)
    
    # kick watchdog and sleep for 10 seconds
    sfw.kick()
    sleep(10000) 
    