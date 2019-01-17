import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlim((0,5000))
ax.set_ylim((0,10000))
line, = ax.plot([], [],c='k',lw=1)

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
decording = True 
timer=0 #t일정 시간이 지나면 공백(" ")을 출력할 때 타이머로

def init():
    line.set_data([], [])
    return line,

def animate(i):
    global decording,timer
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    n = len(data)
    x = np.linspace(0,44100/2,n/2)
    y = np.fft.fft(data)/n
    y = np.absolute(y)
    y = y[range(int(n/2))]
    line.set_data(x, y)

    #가로, 세로 주파수들을 20Hz 범위 내로 측정함
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

    # DTMF 음이 감지되면 출력
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

    return line,

p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK,input_device_index=2)

animation = animation.FuncAnimation(fig, animate, init_func=init, interval=1, blit=True)

plt.show()
