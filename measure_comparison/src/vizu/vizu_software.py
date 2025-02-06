'''VIZUALISATION SOFTWARE
This software encompasses functions from the csv_segmentation and video_segmentation module
For function descriptions, check the said modules.
The aim of this software is to display synchronized data from different measurement means
'''

##########IMPORTS#########
import time
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import cv2
import torch


###PATHS
data_path = 'C:/Users/radja/Documents/COURS/RSRC/CARDIO-visualization/data/'
cmd_path = data_path + 'cmd/'
live_path = data_path + 'LIVE test/'
electro_phi_path = data_path + 'electroPHISIO/'

###GLOBAL VARIABLES. THIS IS A TRIAL FILLED BY MYSELF FOR TESTING.
MC_FILENAME, MC_TEMP = '', '' ##including path + MC_FILENAME
CMD_FILENAME, ELECTROPHI_FILENAME = '', '../../data/electroPHISIO/OUT_17-18-19_1-2-3_09-07-2024_17-23.txt'
FILTERS, GATES = [1,2,3], [1,2,3]
gates_input = input("Please write the number of the gates which you would want to get information from in GATE-GATE-...-GATE format")
filters_input = input("Please write the filters you'd want in FILTER-FILTER-...-FILTER format")
BOUNDING_RECT_FILENAME = '../../data/bounding_rect_data/07-09-2024_22-56'
FPS=30
downsample_factor = FPS*10


####ASSOCIATED FUNCTIONS####
'''DOWNSAMPLE_DATA : 
Match data rates - 10kHz and 30FPS'''
def downsample_data(voltage, t, threshold=40):
    num_rows, num_columns = voltage.shape
    num_full_chunks = num_rows // downsample_factor
    remaining_rows = num_rows % downsample_factor
    print(num_full_chunks, remaining_rows)

    def process_chunk(chunk):
        mean_chunk = chunk.mean(axis=0)
        abs_diff = np.abs(chunk - mean_chunk)
        #check if any value in chunk > or < than the threshold
        if np.any(abs_diff > threshold):
            #if there is a large enough difference, keep the largest value (positive or negative)
            #####in the case where within one chunk of ~33333 values there are two spikes (one positive and one negative), 
            ####this implementation considers the value with the biggest difference. Further implementation should consider a flag when this happens
            result = np.max(chunk, axis=0) if (np.max(chunk) > np.abs(np.min(chunk)) and np.max(chunk) >np.min(chunk, axis=0)) else np.min(chunk, axis=0)
        else:
            # Otherwise, use the mean
            result = mean_chunk
        return result
    
    # FULL CHUNKS
    full_chunks_volt = voltage[:num_full_chunks * downsample_factor].reshape(num_full_chunks, downsample_factor, num_columns)
    downsampled_full_volt = np.apply_along_axis(process_chunk, 1, full_chunks_volt)
    
    full_chunks_time = t[:num_full_chunks * downsample_factor].reshape(num_full_chunks, downsample_factor)
    downsampled_full_time = full_chunks_time.mean(axis=1)

    # REMAINDER, if existing
    if remaining_rows > 0:
        remaining_chunk_volt = voltage[num_full_chunks * downsample_factor:]
        remaining_chunk_time = t[num_full_chunks * downsample_factor:]
        downsampled_remaining_volt = process_chunk(remaining_chunk_volt)
        downsampled_remaining_time = remaining_chunk_time.mean(keepdims=True)
        # Combine FULL and REMAINDER
        downsampled_voltages = np.vstack([downsampled_full_volt, downsampled_remaining_volt])
        downsampled_time = np.concatenate([downsampled_full_time, downsampled_remaining_time])
    else:
        downsampled_voltages = downsampled_full_volt
        downsampled_time = downsampled_full_time

    #print("Downsampled shapes:", downsampled_voltages.shape, downsampled_time.shape)
    return downsampled_time, downsampled_voltages


######DATA STRUCTURE

'''DATA STRUCTURE'''
###TENSOR CREATION
device = torch.device('cpu')
tensor = torch.tensor([1.0, 2.0, 3.0], device=device)