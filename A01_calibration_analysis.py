# -*- coding: utf-8 -*-
"""
This code will analyse the calibration results of BusSim and plot it along side a number of uncalibrated models (timespace diagram of bus trajectories)

@author: geomlk
"""
import numpy as np
import matplotlib.pyplot as plt
import pickle
from BusSim_static_v2 import Model,run_model

#Step 1: Load calibration results

def load_calibrated_params():
    with open('C:/Users/geomlk/Dropbox/Minh_UoL/DA/ABM/BusSim/BusSim_model_calibration_reps.pkl', 'rb') as f:
    #with open('/Users/geomik/Dropbox/Minh_UoL/DA/ABM/BusSim/BusSim_model_calibration.pkl', 'rb') as f:      
        model_params, fixed_params,best_mean,Sol_archived_mean,Sol_archived_std,PI_archived = pickle.load(f)
    return best_mean    

def load_actual_params():
    #load up a model from a Pickle    
    #with open('C:/Users/geomlk/Dropbox/Minh_UoL/DA/ABM/BusSim/BusSim_data_static.pkl', 'rb') as f:
    with open('/Users/geomik/Dropbox/Minh_UoL/DA/ABM/BusSim/BusSim_data_static.pkl', 'rb') as f:      
        model_params, fixed_params, ArrivalRate, ArrivalData, DepartureRate, StateData, GroundTruth,GPSData = pickle.load(f)
    return model_params, fixed_params, ArrivalRate,DepartureRate

if __name__ == '__main__':
    
    model_params, fixed_params, ArrivalRate,DepartureRate = load_actual_params()
    best_mean = load_calibrated_params()
    
    do_reps = False #whether we should export the distribution of headways
    do_ani = False
    do_spacetime_rep_plot = True
    
    #Run the actual parameters first
    NumReps = 10
    do_spacetime_plot = True
    uncalibrated = False
    for r in range(NumReps):
        run_model(model_params,do_ani,do_spacetime_plot,do_reps,uncalibrated)                    
    
    #Now run the calibrated parameters
    do_spacetime_plot = False
    uncalibrated = True
    ArrivalRate = best_mean[0:model_params['NumberOfStop']]
    DepartureRate = best_mean[model_params['NumberOfStop']:2*model_params['NumberOfStop']]
    TrafficSpeed = best_mean[-1]
    #Initialise the model parameters
    model_params2 = {
        "dt": 10,
        "NumberOfStop": model_params['NumberOfStop'],
        "LengthBetweenStop": 2000,
        "EndTime": 6000,
        "Headway": 5 * 60,
        "BurnIn": 1 * 60,
        "AlightTime": 1,
        "BoardTime": 3,
        "StoppingTime": 3,
        "BusAcceleration": 3,  # m/s
        "TrafficSpeed": TrafficSpeed,  # m/s
        "ArrivalRate": ArrivalRate,
        "DepartureRate": DepartureRate,
        "Noise_std": 5           
    }
    for s in range(NumReps):
        run_model(model_params2,do_ani,do_spacetime_plot,do_reps,uncalibrated)                    
