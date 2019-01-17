import pyaudio
import numpy as np

CHUNK = 1000
RATE = 44100

rows_freq = []
rows_freq.append(697)
rows_freq.append(770)
rows_freq.append(852)
rows_freq.append(941)
cols_freq = []
cols_freq.append(1209)
cols_freq.append(1336)
cols_freq.append(1477)
cols_freq.append(1633)
rows = [False]*4
cols = [False]*4
timer = 0
rows_id = -1
cols_id = -1
decording = False

print("DTMF decorder")
p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK,input_device_index=2)

while True:
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    n = len(data)
    y = np.fft.fft(data)/n
    y = np.absolute(y)
    y = y[range(int(n/2))]

    for i in range(4):
        for j in range(20):
            if(y[int((rows_freq[i]+10-j)*CHUNK/RATE)]>500):
                rows[i] = True
                break
            else:rows[i] = False

        for j in range(20):
            if(y[int((cols_freq[i]+10-j)*CHUNK/RATE)]>500):
                cols[i] = True
                break
            else:cols[i] = False

    # 가로 세로 모두 한개씩만 있다면
    if(rows.count(True) == 1 and cols.count(True) == 1):
        timer = 1
        if(decording == False):
            decording = True
            rows_id = rows.index(True)
            cols_id = cols.index(True)
            if(rows_id==3):
                if(cols_id==0): print('*',end="",flush=True)
                if(cols_id==1): print('0',end="",flush=True)
                if(cols_id==2): print('#',end="",flush=True)
            else:print(rows_id*3+cols_id+1,end="",flush=True)

    else :
        decording = False
        if(timer!=0):
            if(timer<20):
                timer+=1
            else:
                print(" ",end="",flush=True)
                timer=0
