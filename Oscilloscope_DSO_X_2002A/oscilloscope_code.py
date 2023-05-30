import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import os

rm = pyvisa.ResourceManager()
print(rm.list_resources())
oscil = rm.open_resource('USB0::0x0957::0x179B::MY55392242::0::INSTR')
print(oscil.query("*IDN?"))
# Clear status and load the default setup.
oscil.write("*CLS")
# oscil.write("*RST")
oscil.timeout = 10000  # ms

def get_measurement(path, file_name, fig_flag):
    
    # Specify the directory path
    # path = r'C:\Users\LAB\Documents\Keysight_oscil_2002A'

    if fig_flag == 1:
        # Download the screen image.
        # --------------------------------------------------------
        oscil.write(":HARDcopy:INKSaver OFF")
        screen_display = oscil.query_binary_values(":DISPlay:DATA? PNG, COLor", datatype='B')   #it works
        # screen_display = get_definite_length_block_data(sDisplay)

        #Save display data values to file.
        image_file_name = 'screen_image.png'
        with open(os.path.join(path, image_file_name), 'wb') as fp:
            fp.write(bytearray(screen_display))

        print("Screen image was succesfully written to :\t", os.path.join(path, file_name))
        #--------------------------------------------------------------

    # # Use auto-scale to automatically set up oscilloscope.
    # print("Autoscale.")
    # oscil.write(":AUToscale")

    # Set trigger mode.
    oscil.write(":TRIG:MODE EDGE")
    qresult = oscil.query(":TRIG:MODE?")
    print("Trigger mode: %s" % qresult)

    # Set EDGE trigger parameters.
    oscil.write(":TRIGger:EDGE:SOURce CHANnel2")
    qresult = oscil.query(":TRIGger:EDGE:SOURce?")
    print("Trigger edge source: %s" % qresult)

    # Set the waveform source channel mode.
    oscil.write(":WAV:SOURce CHANnel2")
    qresult = oscil.query(":WAV:SOUR?")
    print("Waveform source channel is: %s" % qresult)

    # Set the waveform points mode.
    oscil.write(":WAVeform:POINts:MODE RAW")
    qresult = oscil.query(":WAVeform:POINts:MODE?")
    print("Waveform points mode: %s" % qresult)

    # Get the number of waveform points available.
    oscil.write(":WAVeform:POINts 10240")
    qresult = oscil.query(":WAVeform:POINts?")
    print("Waveform points available: %s" % qresult)

    oscil.write(":MEASure:SOURce CHANnel2")
    qresult = oscil.query(":MEASure:SOURce?")
    print("Measure source: %s" % qresult)

    # Choose the format of the data returned:
    oscil.write(":WAVeform:FORMat BYTE")
    print("Waveform format: %s" % oscil.query(":WAVeform:FORMat?"))

    # Get numeric values for later calculations.
    x_increment = float(oscil.query(":WAVeform:XINCrement?"))
    x_origin = float(oscil.query(":WAVeform:XORigin?"))
    y_increment = float(oscil.query(":WAVeform:YINCrement?"))
    y_origin = float(oscil.query(":WAVeform:YORigin?"))
    y_reference = float(oscil.query(":WAVeform:YREFerence?"))

    # Get the waveform data.
    data_bytes = oscil.query_binary_values(":WAVeform:DATA?", datatype='B')
    nLength = len(data_bytes)
    print("Number of data values: %d" % nLength)

    #Save wave data values to file.
    # file_name = 'wave_data.csv'
    with open(os.path.join(path, file_name), 'w+') as f:
        x_points = []
        y_points = []
        for i in range(0, nLength - 1):
            time_val = x_origin + (i * x_increment)
            x_points.append(time_val)
            voltage = (data_bytes[i] - y_reference) * y_increment + y_origin
            y_points.append(voltage)
            f.write("%E, %f\n" % (time_val, voltage))
    print("\nWave data was successfully written to :\t", os.path.join(path, file_name))
    if fig_flag == 1:
        #Ploting the output
        plt.plot(x_points,y_points)
        plt.grid()
        plt.xlabel("Time")
        plt.ylabel("Voltage")
        plot_file_name = 'figure.png'
        plt.savefig(os.path.join(path, plot_file_name), dpi=200)
        print("Plot figure was successfully written to :\t", os.path.join(path, plot_file_name))
        # plt.show()

def get_rise_t(times):

    oscil.write(":MEASure:SOURce CHANnel2")

    rise_time_list = []
    for i in range(times):
        rise_time = oscil.query(":MEAS:RIS?")
        x, y = rise_time.split("-")
        x = x.replace('+', '')
        x = x.replace('E','')
        rise_time = float(float(x) * 10**-float(y))
        rise_time = round(rise_time, 10)
        print("Iteration ", i, "------ Fall time is: ", rise_time)
        rise_time_list.append(rise_time)
    rise_time_avg = sum(rise_time_list) / len(rise_time_list)
    print("The fall time is: " + format(rise_time_avg, '.10f') + ' seconds')
    return rise_time_avg

def get_fall_t(times):

    oscil.write(":MEASure:SOURce CHANnel2")
    fall_time_list = []
    for i in range(times):
        fall_time = oscil.query(":MEAS:FALL?")
        x, y = fall_time.split("-")
        x = x.replace('+', '')
        x = x.replace('E','')
        fall_time = float(float(x) * 10**-float(y))
        fall_time = round(fall_time, 10)
        print("Iteration ", i, "------ Fall time is: ", fall_time)
        fall_time_list.append(fall_time)
    fall_time_avg = sum(fall_time_list) / len(fall_time_list)
    print("The fall time is: " + format(fall_time_avg, '.10f') + ' seconds')
    return fall_time_avg


print("Main program began")
path = r'C:\Users\LAB\Documents\Keysight_DSO_X_2002A'
file_name = 'wave_data.csv'
get_measurement(path, file_name, 0)

times = 5 #times taking the measurement for averaging
f_t = get_fall_t(times)
r_t = get_rise_t(times)

oscil.close()
print("\nOscilloscope closed normally!")
