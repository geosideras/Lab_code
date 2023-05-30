import pyvisa as visa
import time

def instr_init(port_name='USB0::0x09C4::0x0400::DG1D170200037::0::INSTR'):
    rm = visa.ResourceManager()
    # print(rm.list_resources())
    DG1022 = rm.open_resource('USB0::0x09C4::0x0400::DG1D170200037::0::INSTR')
    DG1022.write('*IDN?')
    time.sleep(0.01)
    print(DG1022.read())
    return DG1022


# type of signal = 1: SIN, 2: SQUARE, 3: RAMP, 4: PULSE, 5: NOISE
# parameters = freq(Hz), amplitude(Vpp) and offset(Vdc)
def set_params(handle, type=1, freq=1000, ampl=1.0, offset=-1.5):
    if type == 1:
        type = 'SIN'
    elif type == 2:
        type = 'SQU'
    elif type == 3:
        type = 'RAMP'
    elif type == 4:
        type = 'PULS'
    elif type == 5:
        type = 'NOIS'
    else :
        print('Wrong input for type!!!')

    command = 'FREQ ' + str(freq)
    handle.write(command)
    time.sleep(0.5)
    command = 'VOLT ' + str(ampl)
    handle.write(command)
    time.sleep(0.5)
    command = 'VOLT:OFFS ' + str(offset)
    handle.write(command)
    time.sleep(0.5)
    command = 'FUNC ' + type
    handle.write(command)


handle = instr_init()
# type of signal = 1: SIN, 2: SQUARE, 3: RAMP, 4: PULSE, 5: NOISE
# parameters = freq(Hz), amplitude(Vpp) and offset(Vdc)
set_params(handle, 1, 10000, 2, 0.5)
