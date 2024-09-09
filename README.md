# CARDIO-visualization

## Overview
CARDIO-visualization is a data processing framework designed for the spatiotemporal and multimodal analysis of cardiomyocyte cell cultures. The project integrates video (optical data) and electrophysiology (electrical data) to create a synchronized map of cell activity, visualized in real-time. This toolkit provides researchers with a streamlined way to combine and analyze multimodal datasets in the context of cardiac cell behavior, offering the potential for insights into electrophysiological activity and cellular dynamics.

## Key Features

### 1. Electrode Detection & Isolation
- Automated detection of electrodes in video frames using bounding box data.
- Isolation of specific regions of interest (ROI) in each frame, corresponding to the electrode positions, with pixel-level precision.
- Adjustable threshold margins for error correction during electrode localization.

### 2. Spatiotemporal Displacement Calculation
- Frame-by-frame analysis of displacement over time, using windows to calculate pixel intensity differences.
- Capable of determining changes in electrode positions across successive video frames, providing a window into mechanical shifts or activity in cell culture.
- Results are returned as time series, providing real-time insights into changes over a defined period.

### 3. Multimodal Data Synchronization
- The system can synchronize electrophysiological and video data using time-stamped bounding box metadata.
- Precision handling of multimodal data, including handling mismatched frame rates between electrical and optical measurements.

### 4. Real-Time Data Assembly & Visualization
- The framework can output visualizations of synchronized data, displaying voltage signals alongside the video in near real-time.
- Users can generate displacement heatmaps to track dynamic changes in cellular activity.

## Current Limitations & Areas for Improvement

### 1. Precision Time Protocol (PTP) Implementation
- **Improvement Needed:** Reimplementation of a fully functional PTP protocol for highly precise synchronization between video frames and electrophysiological data. This is crucial for ensuring data is temporally aligned down to the millisecond scale.

### 2. Camera Precision and Synchronization
- **Future Upgrades:** Replace the Raspberry Pi camera with a higher frame rate camera to improve the precision of video capture. The current camera’s limitations affect synchronization accuracy and image quality.
- **Potential Fix:** Explore industrial-grade cameras that don’t rely on Raspberry Pi for connectivity, which could enhance overall synchronization and ease of data capture.

### 3. Long-Term Environmental Control
- **Current Setup:** The current setup may cause cells to cool and deteriorate over long periods. Developing an environmental control system to maintain ideal conditions for cell cultures during extended recording sessions would enable longer, more accurate experiments.

### 4. Deep Learning for Automated Electrode Tracking
- **Planned Development:** Integrate deep learning algorithms to automatically track electrodes in real-time, reducing the need for manual annotation and improving accuracy in tracking electrodes over long-term experiments.

### 5. Fluorescent Visual Data Integration
- **Exploration:** Future integration of fluorescent visual data acquisition for ion displacement tracking, providing additional insights into intracellular processes.
