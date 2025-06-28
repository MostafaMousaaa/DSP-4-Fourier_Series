# Interactive Fourier Series Demonstrator

An educational desktop application for visualizing and understanding Fourier series decomposition of periodic signals.

## Features

- **Real-time Fourier Analysis**: Interactive parameter adjustment with instant visualization
- **Multiple Signal Types**: Square, triangle, sawtooth, half-wave rectified, pulse train, and custom functions
- **Progressive Animation**: Watch harmonic buildup step-by-step
- **3D Visualization**: Waterfall plot showing harmonic contributions
- **Convergence Analysis**: Track reconstruction error and power capture
- **Educational Interface**: Professional UI optimized for learning

## Technical Concepts

### Fourier Series Fundamentals
- **Periodic Signal Decomposition**: Any periodic function can be expressed as a sum of sine and cosine terms
- **Harmonic Analysis**: Understanding frequency content through magnitude and phase spectra
- **Convergence Behavior**: How reconstruction accuracy improves with more harmonics
- **Gibbs Phenomenon**: Overshoot behavior near discontinuities

### Mathematical Implementation
- **Coefficient Calculation**: Numerical integration using trapezoidal rule
- **Synthesis**: Real-time reconstruction from Fourier coefficients
- **Error Metrics**: RMS error, SNR, and Total Harmonic Distortion (THD)

## Installation

### Requirements
```bash
pip install PySide6 matplotlib numpy scipy
```

### File Structure
```
fourier_logic.py    # Core mathematical operations
fourier_ui.py       # PySide6 user interface
```

## Quick Start

1. **Launch Application**
   ```bash
   python fourier_ui.py
   ```

2. **Select a Function**
   - Click preset buttons (Square, Triangle, etc.)
   - Or enter custom function using variable `t`

3. **Adjust Parameters**
   - **Period**: Signal repetition interval
   - **Harmonics**: Number of frequency components (1-50)
   - **Amplitude**: Signal scaling factor

4. **Explore Visualizations**
   - **Time Domain**: Original vs reconstructed signal
   - **Frequency Domain**: Magnitude and phase spectra
   - **3D View**: Harmonic buildup visualization
   - **Convergence**: Error analysis and power capture

## Educational Workflow

### Basic Analysis
1. Start with **Square Wave** (demonstrates odd harmonics only)
2. Observe **Gibbs phenomenon** near edges
3. Increase harmonics to see improved reconstruction
4. Check **Convergence tab** for quantitative metrics

### Advanced Exploration
1. Compare different waveforms:
   - **Triangle**: Faster convergence than square wave
   - **Sawtooth**: Contains all harmonics
   - **Pulse Train**: Adjustable duty cycle effects

2. Custom functions:
   ```python
   np.sin(2*np.pi*t) + 0.3*np.sin(6*np.pi*t)  # Fundamental + 3rd harmonic
   np.abs(np.sin(2*np.pi*t))                   # Full-wave rectified sine
   ```

3. Use **Animation** to visualize progressive reconstruction

### Key Observations
- **Square waves** require many harmonics due to sharp transitions
- **Smooth functions** converge faster (fewer harmonics needed)
- **Symmetry properties** determine which harmonics are present
- **95% power capture** often achieved with relatively few harmonics

## Interface Guide

### Control Panel
- **Function Selection**: Preset waveforms with mathematical descriptions
- **Parameter Sliders**: Real-time adjustment with visual feedback
- **Animation Controls**: Play/pause/reset progressive buildup
- **Harmonic Toggles**: Enable/disable individual frequency components

### Visualization Tabs
- **📈 Time Domain**: Signal comparison with enhanced styling
- **📊 Frequency Domain**: Dual-plot magnitude/phase spectra
- **🎬 3D Visualization**: Interactive waterfall display
- **📉 Convergence**: Multi-metric error analysis

### Analysis Metrics
- **RMS Error**: Root-mean-square reconstruction error
- **SNR**: Signal-to-noise ratio in decibels
- **THD**: Total harmonic distortion percentage
- **Power Capture**: Cumulative energy in first N harmonics

## Technical Notes

### Performance Optimization
- 3D plots use downsampled data for smooth interaction
- Animation uses cached progressive reconstructions
- Coefficient computation optimized with vectorized operations

### Educational Design
- Color-coded visualizations for intuitive understanding
- Progressive disclosure of complexity
- Quantitative metrics alongside visual feedback
- Professional styling optimized for presentation

## Example Use Cases

### Signal Processing Course
- Demonstrate frequency domain representation
- Illustrate sampling and reconstruction concepts
- Show practical filter design implications

### Mathematics Education
- Visualize infinite series convergence
- Connect abstract formulas to intuitive graphics
- Explore symmetry and periodicity concepts

### Research Applications
- Analyze periodic measurement data
- Understand spectral content of experimental signals
- Validate theoretical predictions

## Tips for Effective Learning

1. **Start Simple**: Begin with basic waveforms before custom functions
2. **Observe Patterns**: Note which signals require more/fewer harmonics
3. **Use Animation**: Step-through mode reveals reconstruction process
4. **Check Convergence**: Quantitative analysis supplements visual understanding
5. **Experiment**: Try unusual functions to test intuition

## System Requirements

- **OS**: Windows 10+, macOS 10.14+, Linux
- **Python**: 3.8+
- **RAM**: 4GB minimum, 8GB recommended
- **Display**: 1400x900 minimum resolution

---

**Educational Focus**: This tool emphasizes conceptual understanding through interactive visualization rather than computational efficiency. Ideal for classroom demonstrations, self-study, and research exploration.
