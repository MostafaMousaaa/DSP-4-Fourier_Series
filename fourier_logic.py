import numpy as np
from typing import Callable, Tuple, Dict, List
import json

class FourierSeriesAnalyzer:
    """Enhanced Fourier Series analyzer for educational purposes"""
    
    def __init__(self, period: float = 2*np.pi):
        self.period = period
        self.omega0 = 2*np.pi / period
        self.predefined_functions = self._load_function_library()
        
    def _load_function_library(self) -> Dict:
        """Library of educational function examples"""
        return {
            'square': {
                'name': 'Square Wave',
                'formula': 'A if (t%T) < T/2 else -A',
                'description': 'Classic square wave with odd harmonics only',
                'func': lambda t, A=1, T=None: np.where((t % (T or self.period)) < (T or self.period)/2, A, -A)
            },
            'sawtooth': {
                'name': 'Sawtooth Wave',
                'formula': '2A((t%T)/T) - A',
                'description': 'Linear ramp with all harmonics',
                'func': lambda t, A=1, T=None: A * (2*((t % (T or self.period))/(T or self.period)) - 1)
            },
            'triangle': {
                'name': 'Triangle Wave',
                'formula': '2A|2((t%T)/T - 0.5)| - A',
                'description': 'Triangle wave with odd harmonics only',
                'func': lambda t, A=1, T=None: A * (2*np.abs(2*((t % (T or self.period))/(T or self.period) - 0.5)) - 1)
            },
            'half_wave': {
                'name': 'Half-Wave Rectified Sine',
                'formula': 'max(0, A*sin(2πt/T))',
                'description': 'Rectified sine wave with DC component',
                'func': lambda t, A=1, T=None: np.maximum(0, A * np.sin(2*np.pi*t/(T or self.period)))
            },
            'pulse_train': {
                'name': 'Pulse Train',
                'formula': 'A if (t%T) < duty*T else 0',
                'description': 'Periodic pulses with adjustable duty cycle',
                'func': lambda t, A=1, T=None, duty=0.2: np.where((t % (T or self.period)) < duty*(T or self.period), A, 0)
            }
        }
    
    def compute_coefficients(self, func: Callable, n_harmonics: int, n_points: int = 2000) -> Tuple[float, np.ndarray, np.ndarray]:
        """Compute Fourier coefficients with educational metrics"""
        t = np.linspace(0, self.period, n_points, endpoint=False)
        f_samples = func(t)
        
        # DC component
        a0 = (2/self.period) * np.trapz(f_samples, t)
        
        # Initialize arrays
        an = np.zeros(n_harmonics)
        bn = np.zeros(n_harmonics)
        
        # Compute harmonics
        for n in range(1, n_harmonics + 1):
            cos_n = np.cos(n * self.omega0 * t)
            sin_n = np.sin(n * self.omega0 * t)
            an[n-1] = (2/self.period) * np.trapz(f_samples * cos_n, t)
            bn[n-1] = (2/self.period) * np.trapz(f_samples * sin_n, t)
        
        return a0, an, bn
    
    def synthesize_progressive(self, a0: float, an: np.ndarray, bn: np.ndarray, t: np.ndarray) -> List[np.ndarray]:
        """Generate progressive reconstruction for animation"""
        reconstructions = []
        signal = a0/2 * np.ones_like(t)
        reconstructions.append(signal.copy())
        
        for n in range(len(an)):
            signal += an[n] * np.cos((n+1) * self.omega0 * t)
            signal += bn[n] * np.sin((n+1) * self.omega0 * t)
            reconstructions.append(signal.copy())
        
        return reconstructions
    
    def synthesize_selective(self, a0: float, an: np.ndarray, bn: np.ndarray, t: np.ndarray, 
                           enabled_harmonics: List[bool]) -> np.ndarray:
        """Synthesize with selective harmonics enabled"""
        signal = a0/2 * np.ones_like(t)
        
        for n, enabled in enumerate(enabled_harmonics):
            if enabled and n < len(an):
                signal += an[n] * np.cos((n+1) * self.omega0 * t)
                signal += bn[n] * np.sin((n+1) * self.omega0 * t)
        
        return signal
    
    def compute_metrics(self, original: np.ndarray, reconstructed: np.ndarray) -> Dict:
        """Compute educational metrics"""
        rms_error = np.sqrt(np.mean((original - reconstructed)**2))
        max_error = np.max(np.abs(original - reconstructed))
        snr = 20 * np.log10(np.std(original) / (rms_error + 1e-12))
        
        return {
            'rms_error': rms_error,
            'max_error': max_error,
            'snr_db': snr,
            'relative_error': rms_error / (np.std(original) + 1e-12)
        }
    
    def get_harmonic_analysis(self, an: np.ndarray, bn: np.ndarray) -> Dict:
        """Analyze harmonic content for educational insights"""
        magnitude = np.sqrt(an**2 + bn**2)
        phase = np.arctan2(bn, an)
        power = magnitude**2
        total_power = np.sum(power)
        
        # Find dominant harmonics
        dominant_indices = np.argsort(magnitude)[-5:][::-1]
        
        return {
            'magnitude': magnitude,
            'phase': phase,
            'power': power,
            'total_power': total_power,
            'power_percentage': (power / (total_power + 1e-12)) * 100,
            'dominant_harmonics': dominant_indices + 1,  # 1-indexed
            'fundamental_power': power[0] if len(power) > 0 else 0,
            'thd': np.sqrt(np.sum(power[1:]) / (power[0] + 1e-12)) * 100 if len(power) > 0 else 0
        }
    
    def export_data(self, t: np.ndarray, original: np.ndarray, reconstructed: np.ndarray, 
                   a0: float, an: np.ndarray, bn: np.ndarray) -> Dict:
        """Export analysis data for educational use"""
        return {
            'time': t.tolist(),
            'original_signal': original.tolist(),
            'reconstructed_signal': reconstructed.tolist(),
            'coefficients': {
                'a0': float(a0),
                'an': an.tolist(),
                'bn': bn.tolist()
            },
            'analysis': self.get_harmonic_analysis(an, bn),
            'metrics': self.compute_metrics(original, reconstructed)
        }
