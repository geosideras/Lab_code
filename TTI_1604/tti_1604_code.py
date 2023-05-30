import serial

ser=serial.Serial()
ser.port='COM4'                              # Enter the name of the serial port
ser.baudrate = 9600
ser.timeout = 1                              #Set the timeout to 1 sec
ser.setRTS(0)                                # Give the correct value to connection lines RTS and DTR
ser.setDTR(1)
ser.dsrdtr = True                            # Enable DTR/DSR Handshake
ser.open()                                   # Open the Serial port
print("Serial details parameters:", ser)     # Print the serial port parameters

# Create a dictionary based on TTI 1604 manual
keys = ['0', '0,', '1', '1,', '2', '2,', '3', '3,', '4', '4,', '5', '5,', '6', '6,', '7', '7,', '8', '8,', '9', '9,']
values = [252, 253, 96, 97, 218, 219, 242, 243, 102, 103, 182, 183, 190, 191, 224, 225, 254, 255, 230, 231]
dictionary = dict(zip(values, keys))

#function to calculated the reading
def read_measurement(unit):

    # Empty Lists
    dec_list = []
    buffer = []

    # Loop to find the first byte with \r and read the next 9 bytes
    while 1:
        found = False
        x = ser.read(1)
        if x == b'\r':
            buffer.append(x)
            for i in range(9):
                x = ser.read(1)
                buffer.append(x)
            break

    # Translate the buffer to decimal
    for item in buffer:
        dec_list.append(ord(item))

    # Get only the display digits, meaning char(4), char(5), char(6), char(7), char(8) based on manual
    dis_digits = dec_list[4:9]

    # Check the dictionary and make the translation based on the manual
    for i in range(0, 19):
        for j in range(0, 5):
            if dis_digits[j] == values[i]:
                dis_digits[j] = keys[i]
            elif dis_digits[j] == values[i + 1]:
                dis_digits[j] = keys[i + 1]

    #Debug output
    # print("Buffer output:\t", buffer)
    # print('Output in decimal:\t' + str(dec_list))
    # print("Display digits are:\t" + str(dis_digits))

    #Output measurement
    dis_digits_string = (str(dis_digits[0]) + str(dis_digits[1]) + str(dis_digits[2]) + str(dis_digits[3]) + str(dis_digits[4]))
    measurement = float(dis_digits_string.replace(',', '.'))

    if unit == 'f':
        unit_word = 'Volts'
    elif unit == 'd':
        unit_word = 'Ampere'
    elif unit == 'e':
        unit_word = 'mAmpere'
    elif unit == 'i':
        unit_word = 'Ohm'
    elif unit == 'j':
        unit_word = 'Hz'
    print('Measured = ' + str(measurement) + ' ' + unit_word)
    return measurement

flag_stop = False
print("Pick unit measurement based on number :\n1 for Volt\n2 for Ampere\n3 for mApere\n4 for Ohm\n5 for Hz\n0 Exit")
while not flag_stop:
    input_val = input('Enter option: ')
    if input_val == '0':
        flag_stop=True
    elif input_val == '1':
        command = 'f'
        ser.write(command.encode())     # Set the display screen to Volts
        ser.reset_input_buffer()        # Reset the input buffer
        ser.read(20)                    # Get rid of potential false readings
        measurement = read_measurement(command)
    elif input_val == '2':
        command = 'd'
        ser.write(command.encode())     # Set the display screen to Amperes
        ser.reset_input_buffer()
        ser.read(20)
        measurement = read_measurement(command)
    elif input_val == '3':
        command = 'e'
        ser.write(command.encode())     # Set the display screen to mAmperes
        ser.reset_input_buffer()
        ser.read(40)
        measurement = read_measurement(command)
    elif input_val == '4':
        command = 'i'
        ser.write(command.encode())     # Set the display screen to Ohms
        ser.reset_input_buffer()
        ser.read(20)
        measurement = read_measurement(command)
    elif input_val == '5':
        command = 'j'
        ser.write(command.encode())     # Set the display screen to Hz
        ser.reset_input_buffer()
        ser.read(20)
        measurement = read_measurement(command)
    else:
        print('Wrong input')

ser.close()
