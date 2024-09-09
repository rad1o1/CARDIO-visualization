# CARDIO-visualization

## Overview
CARDIO-visualization is a data processing framework designed for the spatiotemporal and multimodal analysis of cardiomyocyte cell cultures. The project integrates video (optical data) and electrophysiology (electrical data) to create a synchronized map of cell activity, which can be obtained from external data files.
## Key Features

### 1. Electrode Detection & Isolation
- Automated detection of electrodes in video frames using contour detection over TFT arrays.
- Isolation of specific regions of interest (ROI) in each frame, corresponding to the electrode positions, with pixel-level precision.
- Adjustable threshold margins for error correction during electrode localization.

### 2. Spatiotemporal Displacement Calculation
- Frame-by-frame analysis of displacement over time, using windows to calculate pixel intensity differences.
- Capable of determining changes in electrode positions across successive video frames, providing a window into mechanical shifts or activity in cell culture.
- Results are returned as time series, providing real-time insights into changes over a defined period.

### 3. Multimodal Data Synchronization
- The system can synchronize electrophysiological and video data using time-stamped bounding box metadata.
- Precision handling of multimodal data, including handling mismatched frame rates between electrical and optical measurements.

## Current Limitations & Areas for Improvement
### Limitation in trials
This current setup is limited in it's quantity of trials and data that actually was exploited. Future measurements could help consolidate the validity of this project.

### 4. Deep Learning for Automated Electrode Tracking
- **Planned Development:** Integrate deep learning algorithms to automatically track electrodes in real-time, reducing the need for manual annotation and improving accuracy in tracking electrodes over long-term experiments.

### 5. Fluorescent Visual Data Integration
- **Exploration:** Future integration of fluorescent visual data acquisition for ion displacement tracking, providing additional insights into intracellular processes.
