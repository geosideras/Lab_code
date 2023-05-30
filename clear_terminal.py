import time
import msvcrt

no_of_device = 1
while True:
    if msvcrt.kbhit() and ord(msvcrt.getch()) == 27:  # Check if Esc key is pressed
        print("Esc key pressed. Exiting...")
        break
    else:
        #Start measuring a new device
        start_time = time.time()
        voltage = 0
        for i in range(6):
            voltage += 0.5
            print("Taking PNA measurements for " + str(voltage) + "V", end = "\r", flush=True)
            time.sleep(1)
        #Finished the device
        end_time = time.time()
        
        measured_time = float(end_time - start_time)
        print(f"Device with number {no_of_device} measured time: ", measured_time)
        no_of_device += 1
        print("Beginning measurement in new device!!!")
