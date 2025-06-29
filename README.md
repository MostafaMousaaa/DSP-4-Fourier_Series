# Interactive Fourier Series Demonstrator

A powerful educational desktop application for visualizing and understanding Fourier series decomposition of periodic signals with real-time interactive controls.

## 🎬 Demo Video

<div align="center">

**Watch the DSP Fourier Series Visualization in action:**

https://github.com/user-attachments/assets/849c85e9-35b6-4b2e-a5ad-d7223df6b5fa


*Click the image above to watch the full demonstration video for the fourier Series 

</div>
## 🚀 Quick Start

### Installation
```bash
pip install PySide6 matplotlib numpy scipy
python fourier_ui.py
```

### Basic Demo
1. **Launch** the application
2. **Select** a waveform (Square, Triangle, Sawtooth, etc.)
3. **Adjust** harmonics slider (1-50) to see reconstruction improve
4. **Explore** the 4 visualization tabs
5. **Use** harmonic checkboxes for selective synthesis

## 🎯 Key Features

### Interactive Controls
- **Real-time parameter adjustment** with instant visualization
- **Progressive animation** showing harmonic buildup
- **Selective harmonic synthesis** via checkboxes
- **Custom function input** for advanced exploration

### Multi-Tab Visualization
- **📈 Time Domain**: Original vs reconstructed signal comparison
- **📊 Frequency Domain**: Magnitude and phase spectra
- **🎬 3D Visualization**: Waterfall plot of harmonic contributions  
- **📉 Convergence**: Error analysis and power capture metrics

### Signal Types
- **Preset waveforms**: Square, Triangle, Sawtooth, Half-wave, Pulse Train
- **Custom functions**: Enter any mathematical expression using variable `t`

## 🎓 Educational Demonstrations

### 1. Square Wave Analysis
- Shows **odd harmonics only** (1st, 3rd, 5th, ...)
- Demonstrates **Gibbs phenomenon** near discontinuities
- Requires **many harmonics** for accurate reconstruction

### 2. Triangle Wave Comparison
- **Faster convergence** than square wave
- **Smoother reconstruction** with fewer harmonics
- Illustrates **symmetry properties**

### 3. Harmonic Selection
- **Check/uncheck** individual harmonics
- **Observe** how each contributes to reconstruction
- **Understand** frequency domain representation

### 4. Custom Function Examples
```python
np.sin(2*np.pi*t)                    # Pure sine wave
np.sin(2*np.pi*t) + 0.5*np.sin(6*np.pi*t)  # Fundamental + 3rd harmonic
np.abs(np.sin(2*np.pi*t))            # Full-wave rectified
np.sign(np.sin(2*np.pi*t))           # Square wave alternative
```

## 📊 Understanding the Visualizations

<div align="center">

### Time Domain Tab
<img src="time_domain_tab.png" width="400" alt="Time Domain Visualization">

**Blue line**: Original signal  
**Red dashed line**: Fourier series reconstruction  
**Animation**: Progressive harmonic buildup  
**Harmonic count**: Shows enabled/disabled components

### Frequency Domain Tab
<img src="frequency_domain_tab.png" width="400" alt="Frequency Domain Visualization">

**Magnitude spectrum**: Amplitude of each harmonic  
**Phase spectrum**: Phase relationships  
**DC component**: Average value (a₀/2)  
**Selective display**: Only enabled harmonics shown

### 3D Visualization Tab
<img src="3d_visualization_tab.png" width="400" alt="3D Visualization">

**Waterfall plot**: Each layer shows reconstruction with N harmonics  
**Original signal**: Plotted at back for reference  
**Color progression**: Shows harmonic contribution buildup  
**Interactive rotation**: Explore from different angles

### Convergence Tab
<img src="convergence_tab.png" width="400" alt="Convergence Analysis">

**RMS Error**: Reconstruction accuracy vs harmonics  
**SNR**: Signal-to-noise ratio improvement  
**Power Capture**: Percentage of signal energy captured  
**95%/99% lines**: Key convergence benchmarks

</div>

## ⚙️ Advanced Features

### Animation Controls
- **Play**: Start progressive reconstruction
- **Pause**: Freeze current state
- **Reset**: Return to beginning

### Parameter Adjustment
- **Period**: Signal repetition interval (0.1-20 seconds)
- **Harmonics**: Number of frequency components (1-50)
- **Amplitude**: Signal scaling factor (0.1-5.0)

### Analysis Metrics
- **RMS Error**: Root-mean-square reconstruction error
- **SNR**: Signal-to-noise ratio in decibels
- **THD**: Total harmonic distortion percentage

## 🎯 Learning Objectives

### Signal Processing Concepts
- **Frequency domain representation** of periodic signals
- **Harmonic content** and its relationship to signal shape
- **Convergence behavior** of Fourier series
- **Filtering effects** through harmonic selection

### Mathematical Understanding
- **Fourier coefficients** calculation and interpretation
- **Orthogonality** of sine and cosine functions
- **Periodicity** and symmetry properties
- **Infinite series** convergence

## 💡 Pro Tips

1. **Start with square wave** to see Gibbs phenomenon
2. **Compare waveforms** to understand convergence differences
3. **Use animation** to visualize reconstruction process
4. **Experiment with custom functions** to test understanding
5. **Check convergence tab** for quantitative analysis
6. **Toggle harmonics** to see individual contributions

## 🤝 Contributing

Enhance this educational resource by adding:
1. **🎛️ New System Examples** (high-pass filters, differentiators, etc.)
2. **🎮 Interactive Features** for enhanced learning
3. **📊 Analysis Tools** for system characterization
4. **🌍 Real-World Applications** of convolution

## 📄 License

This project is for educational purposes. Feel free to use and modify for learning DSP concepts.

---

**Digital Signal Processing: Linear-Time-Invariant Systems**  
**Author**: DSP Student  
**Date**: June 29, 2025  
**Course**: Digital Signal Processing Fundamentals  
**Textbook Reference**: Sections 2.4-2.5 (Proakis and Manolakis, 4th ed.)