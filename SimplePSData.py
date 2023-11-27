import numpy as np


with open('20230717-0001.psdata', 'rb') as f:
    waveform_data = np.fromfile(f, np.float32)

print("Max:", max(waveform_data))
print("Min:", np.min(waveform_data))