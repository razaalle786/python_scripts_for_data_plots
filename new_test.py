import numpy as np

data = []

with open('20230815-0003.txt', 'r') as f:
    waveform_DATA = f.readlines()
    for line in waveform_DATA:
        waveform_data = line.strip().split('\t')
        data.append(float(waveform_data[0]))
        data.append(float(waveform_data[1]))
        data.append(float(waveform_data[2]))

print("Max:", max(data))
print("Min:", np.min(data))
