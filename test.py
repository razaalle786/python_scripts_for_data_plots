import numpy as np
data = []
with open('20230815-0003.txt', 'rb') as f:
    waveform_DATA = f.readlines()
    for i in range (len(waveform_DATA)):
        waveform_data = str(waveform_DATA[i]).split('b')[1].split('\\r\\n')[0].split(',')
        # for j in range(3):
        # print(waveform_data[2])
        data.append(float(waveform_data[0][1:]))
        data.append(float(waveform_data[1]))
        data.append(float(waveform_data[2]))
print(max(data), np.min(data))
# print(np.max(waveform_data), np.min(waveform_data))

