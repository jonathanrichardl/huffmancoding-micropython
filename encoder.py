from generator import TableGenerator
import machine
from GY85 import GY85
from math import atan,sqrt
from utime import ticks_diff, ticks_ms,sleep
from array import array
from gc import collect
def encode(uncompressed,table,filema):
    machine.Pin(25).on()
    result = []
    compressed = 0
    pos = 7
    for a in uncompressed:
        for a in table[a]:
            if pos<0:
                result.append(compressed)
                pos = 7
                compressed = 0
            if a:
                compressed |= 1 << pos
            pos -= 1
    result.append(compressed)
    file.write(bytearray(result))
    machine.Pin(25).off()

def init():
    machine.freq(200000000) 
    sclPin = 1
    sdaPin = 0
    i2cid = 0
    gy85 = GY85(scl = sclPin, sda = sdaPin, i2cid = i2cid, gyro = True) # enable all measurements
    return gy85

if __name__ == "__main__":
    LED = machine.Pin(25,machine.Pin.OUT)
    gy85 = init()
    total = 0
    i = 0
    try:
        table = TableGenerator()
    except:
        machine.Pin(25).on()
        print('T-able doesnt exist')
        print('Generating Table')
        a = 0
        text = []
        buffer = array('f',[0,0,0])
        buffer2 = array('f',[0,0])
        buffer3 = array('f',[0,0,0,0])
        while(a <4):
            gy85.readAcc(buffer)
            try:
                buffer2[0] = atan(buffer[1]/buffer[2]) * 57.3
                buffer2[1] = atan((- buffer[0]) / sqrt(buffer[1] * buffer[1] + buffer[2] * buffer[2])) * 57.3
            except:
                buffer2[0] = 0
                buffer2[1] = 0
            gy85.readGyro(buffer3)
            text += [('%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2fx'%(buffer[0],buffer[1],buffer[2],
                                                                       buffer2[0],buffer2[1],buffer3[0],
                                                                       buffer3[1],buffer3[2],buffer3[3]))]
            a+= 0.2
            sleep(0.5)
            pass
        text = ''.join(text)
        table = TableGenerator(text)
        table.writeFile()
        text = None #clear
        machine.Pin(25).off()
    collect()
    file = open('compressed.bin','wb')
    buffer = array('f',[0,0,0])
    buffer2 = array('f',[0,0])
    buffer3 = array('f',[0,0,0,0])
    print("Reading and Compressing")
    while True:
        try:
            gy85.readAcc(buffer)
            try:
                buffer2[0] = atan(buffer[1]/buffer[2]) * 57.3
                buffer2[1] = atan((- buffer[0]) / sqrt(buffer[1] * buffer[1] + buffer[2] * buffer[2])) * 57.3
            except:
                buffer2[0] = 0
                buffer2[1] = 0
            gy85.readGyro(buffer3)
            start = ticks_ms()
            encode('%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2fx'%(buffer[0],buffer[1],buffer[2],
                                                                   buffer2[0],buffer[1],buffer3[0],
                                                                   buffer3[1],buffer3[2],buffer3[3]),table.table,file)
            total += ticks_diff(ticks_ms(),start)
            i += 1
            sleep(0.1)
        except KeyboardInterrupt:
            break
    file.close
    print("Total data read and compressed : " + str(i))
    print("Average Compression Time : " + str(total/i) + 'ms')
    
    



