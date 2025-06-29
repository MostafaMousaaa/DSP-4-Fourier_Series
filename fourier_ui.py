import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QGroupBox, QSlider, QSpinBox, QDoubleSpinBox,
    QPushButton, QLabel, QComboBox, QCheckBox, QTableWidget, 
    QTableWidgetItem, QTextEdit, QTabWidget, QProgressBar,
    QSplitter, QFrame, QLineEdit
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QPalette, QColor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import matplotlib.cm as cm
import numpy as np
from fourier_logic import FourierSeriesAnalyzer
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

class PlotCanvas(FigureCanvas):
    """Enhanced matplotlib canvas for educational visualization"""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#1a1a1a')
        super().__init__(self.fig)
        self.setParent(parent)
        self.setStyleSheet("background-color: #1a1a1a; border: 2px solid #0066cc; border-radius: 8px;")
        
        # Set matplotlib style for blue/black theme
        plt.style.use('dark_background')
        
    def clear_plots(self):
        self.fig.clear()
        self.draw()

class FourierSeriesMainWindow(QMainWindow):
    """Main application window for Fourier Series educational tool"""
    
    def __init__(self):
        super().__init__()
        self.analyzer = FourierSeriesAnalyzer()
        self.current_function = None
        self.animation_timer = QTimer()
        self.animation_step = 0
        self.progressive_data = []
        
        self.setup_ui()
        self.setup_connections()
        self.load_default_function()
        # Initialize harmonic checkboxes with default value
        self.update_harmonic_checkboxes(15)  # Default harmonics value
        
    def setup_ui(self):
        """Setup the complete user interface"""
        self.setWindowTitle("Interactive Fourier Series Demonstrator")
        self.setGeometry(100, 100, 1500, 1000)
        
        # Enhanced blue/black theme
        self.setStyleSheet("""
            QMainWindow { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1a1a1a, stop:1 #0d1117); 
                color: #e6f3ff; 
            }
            QGroupBox { 
                font-weight: bold; 
                font-size: 12px;
                border: 2px solid #0066cc; 
                border-radius: 8px; 
                margin-top: 12px; 
                padding-top: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1e2328, stop:1 #161b22);
            }
            QGroupBox::title { 
                subcontrol-origin: margin; 
                left: 15px; 
                padding: 0 8px 0 8px; 
                color: #58a6ff;
                font-size: 13px;
            }
            QPushButton { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #0066cc, stop:1 #004499); 
                border: 1px solid #0088ff; 
                padding: 8px 15px; 
                border-radius: 6px; 
                color: white;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #0088ff, stop:1 #0066cc); 
                border: 1px solid #00aaff;
            }
            QPushButton:pressed { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #004499, stop:1 #003366); 
            }
            QSlider::groove:horizontal {
                border: 1px solid #0066cc;
                height: 8px;
                background: #161b22;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #58a6ff, stop:1 #0066cc);
                border: 1px solid #0088ff;
                width: 18px;
                border-radius: 9px;
                margin: -5px 0;
            }
            QSlider::handle:horizontal:hover {
                background: #79c0ff;
            }
            QLabel {
                color: #e6f3ff;
                font-size: 11px;
            }
            QLineEdit {
                background: #161b22;
                border: 2px solid #0066cc;
                border-radius: 4px;
                padding: 5px;
                color: #e6f3ff;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 2px solid #58a6ff;
            }
            QCheckBox {
                color: #e6f3ff;
                font-size: 10px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #0066cc;
                border-radius: 3px;
                background: #161b22;
            }
            QCheckBox::indicator:checked {
                background: #0066cc;
                border: 2px solid #58a6ff;
            }
            QTableWidget {
                background: #161b22;
                border: 2px solid #0066cc;
                border-radius: 6px;
                color: #e6f3ff;
                gridline-color: #30363d;
                font-size: 10px;
            }
            QHeaderView::section {
                background: #0066cc;
                color: white;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
            QTabWidget::pane {
                border: 2px solid #0066cc;
                border-radius: 8px;
                background: #1a1a1a;
            }
            QTabBar::tab {
                background: #161b22;
                color: #e6f3ff;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                border: 1px solid #30363d;
            }
            QTabBar::tab:selected {
                background: #0066cc;
                color: white;
                border: 1px solid #58a6ff;
            }
            QTabBar::tab:hover {
                background: #21262d;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main splitter
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        layout = QHBoxLayout(central_widget)
        layout.addWidget(main_splitter)
        
        # Left panel for controls
        left_panel = self.create_control_panel()
        main_splitter.addWidget(left_panel)
        
        # Right panel for plots
        right_panel = self.create_plot_panel()
        main_splitter.addWidget(right_panel)
        
        main_splitter.setSizes([400, 1000])
        
    def create_control_panel(self) -> QWidget:
        """Create the control panel with all interactive elements"""
        panel = QWidget()
        panel.setMaximumWidth(450)
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Function Selection Group with enhanced styling
        func_group = QGroupBox("📊 Function Selection")
        func_layout = QGridLayout(func_group)
        func_layout.setSpacing(8)
        
        # Enhanced predefined function buttons
        function_data = {
            'square': ('🔲 Square Wave', '#ff6b6b'),
            'triangle': ('📐 Triangle', '#4ecdc4'), 
            'sawtooth': ('🔪 Sawtooth', '#45b7d1'),
            'half_wave': ('🌊 Half Wave', '#96ceb4'),
            'pulse_train': ('⚡ Pulse Train', '#ffeaa7')
        }
        
        for i, (func_key, (label, color)) in enumerate(function_data.items()):
            btn = QPushButton(label)
            btn.setStyleSheet(f"""
                QPushButton {{ 
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 {color}, stop:1 {self.darken_color(color)}); 
                    border: 2px solid {color};
                    font-size: 10px;
                    font-weight: bold;
                    min-height: 35px;
                    min-width: 150px;
                }}
                QPushButton:hover {{ 
                    background: {color};
                }}
            """)
            btn.clicked.connect(lambda checked, key=func_key: self.load_predefined_function(key))
            func_layout.addWidget(btn, i//2, i%2)
        
        # Enhanced custom function input
        self.custom_func_input = QLineEdit("np.sin(2*np.pi*t)")
        self.custom_func_input.setPlaceholderText("Enter function using 't' variable...")
        custom_btn = QPushButton("🔧 Apply Custom Function")
        custom_btn.clicked.connect(self.apply_custom_function)
        
        func_layout.addWidget(QLabel("✏️ Custom Function:"), 3, 0)
        func_layout.addWidget(self.custom_func_input, 3, 1)
        func_layout.addWidget(custom_btn, 4, 0, 1, 2)
        
        layout.addWidget(func_group)
        
        # Enhanced Parameters Group
        params_group = QGroupBox("⚙️ Signal Parameters")
        params_layout = QGridLayout(params_group)
        params_layout.setSpacing(10)
        
        # Period slider with enhanced styling
        period_label = QLabel("🔄 Period:")
        period_label.setStyleSheet("color: #58a6ff; font-weight: bold;")
        self.period_slider = QSlider(Qt.Orientation.Horizontal)
        self.period_slider.setRange(100, 2000)
        self.period_slider.setValue(int(2*np.pi*100))
        self.period_value = QLabel("6.28")
        self.period_value.setStyleSheet("color: #79c0ff; font-weight: bold; font-size: 12px;")
        
        params_layout.addWidget(period_label, 0, 0)
        params_layout.addWidget(self.period_slider, 0, 1)
        params_layout.addWidget(self.period_value, 0, 2)
        
        # Harmonics slider
        harmonics_label = QLabel("🎵 Harmonics:")
        harmonics_label.setStyleSheet("color: #58a6ff; font-weight: bold;")
        self.harmonics_slider = QSlider(Qt.Orientation.Horizontal)
        self.harmonics_slider.setRange(1, 50)
        self.harmonics_slider.setValue(15)
        self.harmonics_value = QLabel("15")
        self.harmonics_value.setStyleSheet("color: #79c0ff; font-weight: bold; font-size: 12px;")
        
        params_layout.addWidget(harmonics_label, 1, 0)
        params_layout.addWidget(self.harmonics_slider, 1, 1)
        params_layout.addWidget(self.harmonics_value, 1, 2)
        
        # Amplitude slider
        amplitude_label = QLabel("📏 Amplitude:")
        amplitude_label.setStyleSheet("color: #58a6ff; font-weight: bold;")
        self.amplitude_slider = QSlider(Qt.Orientation.Horizontal)
        self.amplitude_slider.setRange(10, 500)
        self.amplitude_slider.setValue(100)
        self.amplitude_value = QLabel("1.0")
        self.amplitude_value.setStyleSheet("color: #79c0ff; font-weight: bold; font-size: 12px;")
        
        params_layout.addWidget(amplitude_label, 2, 0)
        params_layout.addWidget(self.amplitude_slider, 2, 1)
        params_layout.addWidget(self.amplitude_value, 2, 2)
        
        layout.addWidget(params_group)
        
        # Enhanced Animation Controls
        anim_group = QGroupBox("🎬 Animation Controls")
        anim_layout = QHBoxLayout(anim_group)
        
        self.play_btn = QPushButton("▶️ Play")
        self.pause_btn = QPushButton("⏸️ Pause") 
        self.reset_btn = QPushButton("⏹️ Reset")
        
        for btn in [self.play_btn, self.pause_btn, self.reset_btn]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet(btn.styleSheet() + "font-size: 12px;")
        
        anim_layout.addWidget(self.play_btn)
        anim_layout.addWidget(self.pause_btn)
        anim_layout.addWidget(self.reset_btn)
        
        layout.addWidget(anim_group)
        
        # Harmonic Selection
        harmonics_group = QGroupBox("Harmonic Selection")
        harmonics_layout = QVBoxLayout(harmonics_group)
        
        self.harmonic_checkboxes = []
        checkbox_widget = QWidget()
        checkbox_layout = QGridLayout(checkbox_widget)
        
        for i in range(20):  # Show first 20 harmonics
            cb = QCheckBox(f"H{i+1}")
            cb.setChecked(True)
            cb.stateChanged.connect(self.update_selective_synthesis)
            self.harmonic_checkboxes.append(cb)
            checkbox_layout.addWidget(cb, i//4, i%4)
        
        harmonics_layout.addWidget(checkbox_widget)
        layout.addWidget(harmonics_group)
        
        # Coefficient Table
        coeff_group = QGroupBox("Fourier Coefficients")
        coeff_layout = QVBoxLayout(coeff_group)
        
        self.coeff_table = QTableWidget(0, 4)
        self.coeff_table.setHorizontalHeaderLabels(['n', 'an', 'bn', '|An|'])
        self.coeff_table.setMaximumHeight(200)
        
        coeff_layout.addWidget(self.coeff_table)
        layout.addWidget(coeff_group)
        
        # Metrics Display
        metrics_group = QGroupBox("Analysis Metrics")
        metrics_layout = QGridLayout(metrics_group)
        
        self.rms_error_label = QLabel("RMS Error: --")
        self.snr_label = QLabel("SNR: -- dB")
        self.thd_label = QLabel("THD: -- %")
        
        metrics_layout.addWidget(self.rms_error_label, 0, 0)
        metrics_layout.addWidget(self.snr_label, 0, 1)
        metrics_layout.addWidget(self.thd_label, 1, 0)
        
        layout.addWidget(metrics_group)
        
        layout.addStretch()
        return panel
    
    def darken_color(self, color):
        """Helper function to darken a color for gradients"""
        color_map = {
            '#ff6b6b': '#e55555',
            '#4ecdc4': '#3eb8b0', 
            '#45b7d1': '#3a9bc1',
            '#96ceb4': '#7bb89f',
            '#ffeaa7': '#e6d396'
        }
        return color_map.get(color, color)
    
    def create_plot_panel(self) -> QWidget:
        """Create the plotting panel with multiple visualization tabs"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Create enhanced tab widget
        self.plot_tabs = QTabWidget()
        self.plot_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 3px solid #0066cc;
                border-radius: 10px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1a1a1a, stop:1 #0d1117);
            }
        """)
        
        # Enhanced plot canvases
        self.time_plot = PlotCanvas(panel, width=10, height=7)
        self.plot_tabs.addTab(self.time_plot, "📈 Time Domain")
        
        self.freq_plot = PlotCanvas(panel, width=10, height=7)
        self.plot_tabs.addTab(self.freq_plot, "📊 Frequency Domain")
        
        # 3D visualization
        self.plot_3d = PlotCanvas(panel, width=8, height=6)
        self.plot_tabs.addTab(self.plot_3d, "3D Visualization")
        
        # Convergence analysis
        self.convergence_plot = PlotCanvas(panel, width=8, height=6)
        self.plot_tabs.addTab(self.convergence_plot, "Convergence")
        
        layout.addWidget(self.plot_tabs)
        return panel
    
    def setup_connections(self):
        """Setup signal-slot connections"""
        self.period_slider.valueChanged.connect(self.update_period)
        self.harmonics_slider.valueChanged.connect(self.update_harmonics)
        self.amplitude_slider.valueChanged.connect(self.update_amplitude)
        
        self.play_btn.clicked.connect(self.start_animation)
        self.pause_btn.clicked.connect(self.pause_animation)
        self.reset_btn.clicked.connect(self.reset_animation)
        
        self.animation_timer.timeout.connect(self.animate_step)
    
    def load_predefined_function(self, func_key: str):
        """Load a predefined function from the library"""
        func_info = self.analyzer.predefined_functions[func_key]
        self.current_function = func_info['func']
        self.update_analysis()
    
    def apply_custom_function(self):
        """Apply user-defined custom function"""
        try:
            expr = self.custom_func_input.text()
            # Create safe function from expression
            def custom_func(t):
                return eval(expr, {"__builtins__": {}, "np": np, "sin": np.sin, "cos": np.cos, 
                                 "pi": np.pi, "t": t, "abs": np.abs, "exp": np.exp})
            self.current_function = custom_func
            self.update_analysis()
        except Exception as e:
            print(f"Error in custom function: {e}")
    
    def load_default_function(self):
        """Load default square wave function"""
        self.load_predefined_function('square')
    
    def update_period(self, value):
        """Update period value"""
        period = value / 100.0
        self.period_value.setText(f"{period:.2f}")
        self.analyzer.period = period
        self.analyzer.omega0 = 2*np.pi / period
        self.update_analysis()
    
    def update_harmonics(self, value):
        """Update number of harmonics"""
        self.harmonics_value.setText(str(value))
        self.update_harmonic_checkboxes(value)
        self.update_analysis()
    
    def update_harmonic_checkboxes(self, n_harmonics):
        """Update harmonic checkboxes based on number of harmonics"""
        # Update checkbox labels and visibility
        for i, cb in enumerate(self.harmonic_checkboxes):
            if i < n_harmonics:
                cb.setText(f"H{i+1}")
                cb.setVisible(True)
                cb.setChecked(True)  # Default to checked
            else:
                cb.setVisible(False)
                cb.setChecked(False)
    
    def update_amplitude(self, value):
        """Update amplitude value"""
        amplitude = value / 100.0
        self.amplitude_value.setText(f"{amplitude:.1f}")
        self.update_analysis()
    
    def update_analysis(self):
        """Perform complete Fourier analysis and update all displays"""
        if self.current_function is None:
            return
        
        # Get current parameters
        period = float(self.period_value.text())
        n_harmonics = int(self.harmonics_value.text())
        amplitude = float(self.amplitude_value.text())
        
        # Generate time vector
        t = np.linspace(0, 2*period, 2000)
        
        # Generate original signal
        try:
            if self.current_function is not None:
                original = self.current_function(t) * amplitude
            else:
                return
        except:
            return
        
        # Compute Fourier coefficients
        if self.current_function is not None:
            def wrapped_function(tt):
                return self.current_function(tt) * amplitude
            a0, an, bn = self.analyzer.compute_coefficients(wrapped_function, n_harmonics)
        else:
            return
        
        # Store coefficients for selective synthesis
        self.current_coefficients = (a0, an, bn)
        
        # Generate reconstruction
        reconstructed = self.analyzer.synthesize_progressive(a0, an, bn, t)[-1]
        
        # Update all displays
        self.update_plots(t, original, reconstructed, a0, an, bn)
        self.update_coefficient_table(a0, an, bn)
        self.update_metrics(original, reconstructed, an, bn)
        
        # Store for animation
        self.progressive_data = self.analyzer.synthesize_progressive(a0, an, bn, t)
        self.t_data = t
        self.original_data = original
    
        # Store convergence data for animation
        if hasattr(self, 'original_data') and hasattr(self, 't_data'):
            harmonic_range = np.arange(1, len(an) + 1)
            rms_errors = []
            
            for h in harmonic_range:
                reconstruction = a0/2 * np.ones_like(self.t_data)
                for n in range(h):
                    reconstruction += an[n] * np.cos((n+1) * self.analyzer.omega0 * self.t_data)
                    reconstruction += bn[n] * np.sin((n+1) * self.analyzer.omega0 * self.t_data)
                rms_error = np.sqrt(np.mean((self.original_data - reconstruction)**2))
                rms_errors.append(rms_error)
            
            self.convergence_data = {'rms_errors': rms_errors}
    
    def update_plots(self, t, original, reconstructed, a0, an, bn):
        """Update all plot displays with enhanced styling"""
        # Enhanced Time domain plot
        self.time_plot.fig.clear()
        ax1 = self.time_plot.fig.add_subplot(111, facecolor='#0d1117')
        
        # Plot with enhanced styling
        line1 = ax1.plot(t, original, color='#58a6ff', linewidth=3, label='Original Function', alpha=0.9)
        line2 = ax1.plot(t, reconstructed, color='#ff6b6b', linewidth=2.5, linestyle='--', 
                        label='Fourier Series Approximation', alpha=0.8)
        
        # Enhanced axes styling
        ax1.set_xlabel('Time (s)', color='#e6f3ff', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Amplitude', color='#e6f3ff', fontsize=12, fontweight='bold')
        ax1.set_title('Fourier Series Reconstruction', color='#58a6ff', fontsize=14, fontweight='bold', pad=20)
        
        # Enhanced legend
        legend = ax1.legend(loc='upper right', frameon=True, fancybox=True, shadow=True,
                           facecolor='#161b22', edgecolor='#0066cc', framealpha=0.9)
        legend.get_frame().set_linewidth(2)
        for text in legend.get_texts():
            text.set_color('#e6f3ff')
            text.set_fontsize(11)
            text.set_fontweight('bold')
        
        # Enhanced grid
        ax1.grid(True, alpha=0.3, color='#30363d', linestyle='-', linewidth=0.8)
        ax1.set_facecolor('#0d1117')
        
        # Enhanced tick styling
        ax1.tick_params(colors='#e6f3ff', labelsize=10, width=1.5)
        for spine in ax1.spines.values():
            spine.set_color('#0066cc')
            spine.set_linewidth(2)
        
        self.time_plot.fig.patch.set_facecolor('#1a1a1a')
        self.time_plot.fig.tight_layout(pad=2.0)
        self.time_plot.draw()
        
        # Enhanced Frequency domain plot
        self.freq_plot.fig.clear()
        
        # Magnitude spectrum
        ax2 = self.freq_plot.fig.add_subplot(211, facecolor='#0d1117')
        harmonics = np.arange(1, len(an) + 1)
        magnitude = np.sqrt(an**2 + bn**2)
        
        # Enhanced DC component
        markerline, stemlines, baseline = ax2.stem([0], [a0/2], linefmt='none', markerfmt='o',
                                                  basefmt=' ' )
        markerline.set_markerfacecolor('#58a6ff')
        markerline.set_markeredgecolor('#79c0ff')
        markerline.set_markersize(10)
        stemlines.set_color('#58a6ff')
        stemlines.set_linewidth(3)
        
        # Enhanced harmonics with selective coloring
        markerline, stemlines, baseline = ax2.stem(harmonics, magnitude, linefmt='none', markerfmt='o',
                                                  basefmt=' ' )
        
        # Set colors individually for each harmonic
        # Simplified approach - set colors for the entire plot
        markerline.set_markerfacecolor('#4ecdc4')
        markerline.set_markeredgecolor('#5dd9d1')
        stemlines.set_color('#4ecdc4')
        
        ax2.set_xlabel('Harmonic Number', color='#e6f3ff', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Magnitude', color='#e6f3ff', fontsize=11, fontweight='bold')
        ax2.set_title('Magnitude Spectrum', color='#58a6ff', fontsize=13, fontweight='bold')
        ax2.tick_params(colors='#e6f3ff', labelsize=9)
        ax2.grid(True, alpha=0.3, color='#30363d')
        for spine in ax2.spines.values():
            spine.set_color('#0066cc')
            spine.set_linewidth(1.5)
        
        # Enhanced Phase spectrum
        ax3 = self.freq_plot.fig.add_subplot(212, facecolor='#0d1117')
        phase = np.arctan2(bn, an)
        markerline, stemlines, baseline = ax3.stem(harmonics, phase, linefmt='none', markerfmt='s',
                                                  basefmt=' ' )
        
        # Set colors individually for each harmonic
        # Simplified approach - set colors for the entire plot
        markerline.set_markerfacecolor('#4ecdc4')
        markerline.set_markeredgecolor('#5dd9d1')
        stemlines.set_color('#4ecdc4')
        
        ax3.set_xlabel('Harmonic Number', color='#e6f3ff', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Phase (rad)', color='#e6f3ff', fontsize=11, fontweight='bold')
        ax3.set_title('Phase Spectrum', color='#58a6ff', fontsize=13, fontweight='bold')
        ax3.tick_params(colors='#e6f3ff', labelsize=9)
        ax3.grid(True, alpha=0.3, color='#30363d')
        for spine in ax3.spines.values():
            spine.set_color('#0066cc')
            spine.set_linewidth(1.5)
        
        self.freq_plot.fig.patch.set_facecolor('#1a1a1a')
        self.freq_plot.fig.tight_layout(pad=2.0)
        self.freq_plot.draw()
        
        # 3D Visualization
        self.update_3d_plot(t, original, a0, an, bn)
        
        # Convergence Analysis
        self.update_convergence_plot(t, original, a0, an, bn)
    
    def update_3d_plot(self, t, original, a0, an, bn):
        """Create 3D waterfall plot showing harmonic buildup"""
        self.plot_3d.fig.clear()
        ax = self.plot_3d.fig.add_subplot(111, projection='3d', facecolor='#0d1117')
        
        # Generate progressive reconstructions for 3D display
        n_harmonics = len(an)
        max_display_harmonics = min(20, n_harmonics)  # Limit for performance
        
        # Sample fewer time points for 3D performance
        t_3d = t[::10]  # Every 10th point
        original_3d = original[::10]
        
        # Plot original signal at the back
        ax.plot(t_3d, [0] * len(t_3d), original_3d, 
               color='#58a6ff', linewidth=3, alpha=0.8, label='Original')
        
        # Plot progressive reconstructions
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7', 
                 '#ff7675', '#74b9ff', '#fd79a8', '#fdcb6e', '#6c5ce7']
        # Repeat colors if needed
        while len(colors) < max_display_harmonics:
            colors.extend(colors)
        colors = colors[:max_display_harmonics]
        
        for h in range(1, max_display_harmonics + 1, 2):  # Every other harmonic for clarity
            # Reconstruct with h harmonics
            reconstruction = a0/2 * np.ones_like(t_3d)
            for n in range(h):
                if n < len(an):
                    reconstruction += an[n] * np.cos((n+1) * self.analyzer.omega0 * t_3d)
                    reconstruction += bn[n] * np.sin((n+1) * self.analyzer.omega0 * t_3d)
            
            ax.plot(t_3d, [h] * len(t_3d), reconstruction,
                   color=colors[h-1], linewidth=2, alpha=0.7)
        
        # Styling for 3D plot
        ax.set_xlabel('Time (s)', color='#e6f3ff', fontsize=11, fontweight='bold')
        ax.set_ylabel('Harmonics', color='#e6f3ff', fontsize=11, fontweight='bold') 
        
        # Handle 3D-specific attributes safely
        try:
            ax.set_zlabel('Amplitude', color='#e6f3ff', fontsize=11, fontweight='bold')  # type: ignore
        except AttributeError:
            pass  # Not a 3D axes
            
        ax.set_title('3D Harmonic Buildup Visualization', color='#58a6ff', 
                    fontsize=13, fontweight='bold', pad=20)
        
        # Set background and grid colors for 3D
        try:
            ax.xaxis.pane.fill = False  # type: ignore
            ax.xaxis.pane.set_edgecolor('#30363d')  # type: ignore
            ax.yaxis.pane.fill = False  # type: ignore
            ax.yaxis.pane.set_edgecolor('#30363d')  # type: ignore
            ax.zaxis.pane.fill = False  # type: ignore
            ax.zaxis.pane.set_edgecolor('#30363d')  # type: ignore
        except AttributeError:
            pass  # Not a 3D axes or missing pane attributes
            
        ax.grid(True, alpha=0.3, color='#30363d')
        
        # Tick colors
        ax.tick_params(colors='#e6f3ff', labelsize=9)
        
        self.plot_3d.fig.patch.set_facecolor('#1a1a1a')
        self.plot_3d.draw()
    
    def update_convergence_plot(self, t, original, a0, an, bn):
        """Create convergence analysis showing error vs harmonics"""
        self.convergence_plot.fig.clear()
        
        # Calculate progressive reconstructions and errors
        n_harmonics = len(an)
        harmonic_range = np.arange(1, n_harmonics + 1)
        rms_errors = []
        max_errors = []
        snr_values = []
        power_ratios = []
        
        for h in harmonic_range:
            # Reconstruct with h harmonics
            reconstruction = a0/2 * np.ones_like(t)
            for n in range(h):
                reconstruction += an[n] * np.cos((n+1) * self.analyzer.omega0 * t)
                reconstruction += bn[n] * np.sin((n+1) * self.analyzer.omega0 * t)
            
            # Calculate metrics
            rms_error = np.sqrt(np.mean((original - reconstruction)**2))
            max_error = np.max(np.abs(original - reconstruction))
            
            # Signal-to-noise ratio
            signal_power = np.mean(original**2)
            noise_power = np.mean((original - reconstruction)**2)
            snr = 10 * np.log10(signal_power / (noise_power + 1e-12))
            
            # Power captured by first h harmonics
            total_power = np.sum(an**2 + bn**2)
            captured_power = np.sum(an[:h]**2 + bn[:h]**2)
            power_ratio = captured_power / (total_power + 1e-12) * 100
            
            rms_errors.append(rms_error)
            max_errors.append(max_error)
            snr_values.append(snr)
            power_ratios.append(power_ratio)
        
        # Create subplots for convergence analysis
        ax1 = self.convergence_plot.fig.add_subplot(221, facecolor='#0d1117')
        ax2 = self.convergence_plot.fig.add_subplot(222, facecolor='#0d1117')
        ax3 = self.convergence_plot.fig.add_subplot(223, facecolor='#0d1117')
        ax4 = self.convergence_plot.fig.add_subplot(224, facecolor='#0d1117')
        
        # RMS Error vs Harmonics
        ax1.semilogy(harmonic_range, rms_errors, color='#ff6b6b', linewidth=2.5, 
                    marker='o', markersize=4, markerfacecolor='#ff7f7f')
        ax1.set_xlabel('Number of Harmonics', color='#e6f3ff', fontweight='bold')
        ax1.set_ylabel('RMS Error', color='#e6f3ff', fontweight='bold')
        ax1.set_title('RMS Error Convergence', color='#58a6ff', fontweight='bold')
        ax1.grid(True, alpha=0.3, color='#30363d')
        ax1.tick_params(colors='#e6f3ff', labelsize=9)
        for spine in ax1.spines.values():
            spine.set_color('#0066cc')
        
        # Maximum Error vs Harmonics
        ax2.semilogy(harmonic_range, max_errors, color='#4ecdc4', linewidth=2.5,
                    marker='s', markersize=4, markerfacecolor='#5dd9d1')
        ax2.set_xlabel('Number of Harmonics', color='#e6f3ff', fontweight='bold')
        ax2.set_ylabel('Maximum Error', color='#e6f3ff', fontweight='bold')
        ax2.set_title('Maximum Error Convergence', color='#58a6ff', fontweight='bold')
        ax2.grid(True, alpha=0.3, color='#30363d')
        ax2.tick_params(colors='#e6f3ff', labelsize=9)
        for spine in ax2.spines.values():
            spine.set_color('#0066cc')
        
        # SNR vs Harmonics
        ax3.plot(harmonic_range, snr_values, color='#ffd93d', linewidth=2.5,
                marker='^', markersize=4, markerfacecolor='#ffe066')
        ax3.set_xlabel('Number of Harmonics', color='#e6f3ff', fontweight='bold')
        ax3.set_ylabel('SNR (dB)', color='#e6f3ff', fontweight='bold')
        ax3.set_title('Signal-to-Noise Ratio', color='#58a6ff', fontweight='bold')
        ax3.grid(True, alpha=0.3, color='#30363d')
        ax3.tick_params(colors='#e6f3ff', labelsize=9)
        for spine in ax3.spines.values():
            spine.set_color('#0066cc')
        
        # Power Capture vs Harmonics
        ax4.plot(harmonic_range, power_ratios, color='#a8e6cf', linewidth=2.5,
                marker='d', markersize=4, markerfacecolor='#b8f0df')
        ax4.axhline(y=95, color='#ff6b6b', linestyle='--', alpha=0.7, linewidth=2)
        ax4.axhline(y=99, color='#58a6ff', linestyle='--', alpha=0.7, linewidth=2)
        ax4.set_xlabel('Number of Harmonics', color='#e6f3ff', fontweight='bold')
        ax4.set_ylabel('Power Captured (%)', color='#e6f3ff', fontweight='bold')
        ax4.set_title('Cumulative Power Capture', color='#58a6ff', fontweight='bold')
        ax4.set_ylim(0, 105)
        ax4.grid(True, alpha=0.3, color='#30363d')
        ax4.tick_params(colors='#e6f3ff', labelsize=9)
        for spine in ax4.spines.values():
            spine.set_color('#0066cc')
        
        # Add text annotations for key metrics
        final_rms = rms_errors[-1]
        final_snr = snr_values[-1]
        final_power = power_ratios[-1]
        
        ax1.text(0.05, 0.95, f'Final RMS: {final_rms:.4f}', transform=ax1.transAxes,
                color='#e6f3ff', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='#161b22', alpha=0.8))
        
        ax3.text(0.05, 0.95, f'Final SNR: {final_snr:.1f} dB', transform=ax3.transAxes,
                color='#e6f3ff', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='#161b22', alpha=0.8))
        
        ax4.text(0.05, 0.05, f'Power: {final_power:.1f}%', transform=ax4.transAxes,
                color='#e6f3ff', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='#161b22', alpha=0.8))
        
        # Find 95% and 99% power points
        power_95_idx = np.argmax(np.array(power_ratios) >= 95)
        power_99_idx = np.argmax(np.array(power_ratios) >= 99)
        
        if power_95_idx > 0:
            ax4.annotate(f'95% at H{power_95_idx+1}', 
                        xy=(float(power_95_idx+1), 95.0), xytext=(float(power_95_idx+5), 85.0),
                        arrowprops=dict(arrowstyle='->', color='#ff6b6b', alpha=0.7),
                        color='#ff6b6b', fontweight='bold', fontsize=9)
        
        if power_99_idx > 0:
            ax4.annotate(f'99% at H{power_99_idx+1}', 
                        xy=(float(power_99_idx+1), 99.0), xytext=(float(power_99_idx+5), 102.0),
                        arrowprops=dict(arrowstyle='->', color='#58a6ff', alpha=0.7),
                        color='#58a6ff', fontweight='bold', fontsize=9)
        
        self.convergence_plot.fig.patch.set_facecolor('#1a1a1a')
        self.convergence_plot.fig.tight_layout(pad=2.0)
        self.convergence_plot.draw()
    
    def update_coefficient_table(self, a0, an, bn):
        """Update the coefficient table"""
        self.coeff_table.setRowCount(len(an) + 1)
        
        # DC component
        self.coeff_table.setItem(0, 0, QTableWidgetItem("0 (DC)"))
        self.coeff_table.setItem(0, 1, QTableWidgetItem(f"{a0:.4f}"))
        self.coeff_table.setItem(0, 2, QTableWidgetItem("0"))
        self.coeff_table.setItem(0, 3, QTableWidgetItem(f"{a0/2:.4f}"))
        
        # Harmonics
        for i, (a, b) in enumerate(zip(an, bn)):
            magnitude = np.sqrt(a**2 + b**2)
            self.coeff_table.setItem(i+1, 0, QTableWidgetItem(str(i+1)))
            self.coeff_table.setItem(i+1, 1, QTableWidgetItem(f"{a:.4f}"))
            self.coeff_table.setItem(i+1, 2, QTableWidgetItem(f"{b:.4f}"))
            self.coeff_table.setItem(i+1, 3, QTableWidgetItem(f"{magnitude:.4f}"))
    
    def update_metrics(self, original, reconstructed, an, bn):
        """Update analysis metrics display"""
        metrics = self.analyzer.compute_metrics(original, reconstructed)
        harmonic_analysis = self.analyzer.get_harmonic_analysis(an, bn)
        
        self.rms_error_label.setText(f"RMS Error: {metrics['rms_error']:.4f}")
        self.snr_label.setText(f"SNR: {metrics['snr_db']:.2f} dB")
        self.thd_label.setText(f"THD: {harmonic_analysis['thd']:.2f} %")
    
    def update_selective_synthesis(self):
        """Update reconstruction based on selected harmonics"""
        if not hasattr(self, 'progressive_data') or not self.progressive_data:
            return
        
        # Get enabled harmonics (first 20 checkboxes)
        enabled = [cb.isChecked() for cb in self.harmonic_checkboxes]
        
        # Ensure we have the necessary data
        if not hasattr(self, 't_data') or not hasattr(self, 'original_data') or not hasattr(self, 'current_coefficients'):
            return
        
        # Extract stored coefficients
        a0, an, bn = self.current_coefficients
        
        # Perform selective synthesis using the analyzer's method
        selective_reconstructed = self.analyzer.synthesize_selective(a0, an, bn, self.t_data, enabled)
        
        # Update ALL plot tabs with selective reconstruction
        self.update_selective_plots(self.t_data, self.original_data, selective_reconstructed, a0, an, bn, enabled)
        
        # Update metrics for selective reconstruction
        self.update_metrics(self.original_data, selective_reconstructed, an, bn)
    
    def update_selective_plots(self, t, original, reconstructed, a0, an, bn, enabled_harmonics):
        """Update all plot displays with selective harmonic reconstruction"""
        # Update time domain plot
        self.update_selective_time_plot(t, original, reconstructed, a0, an, bn, enabled_harmonics)
        
        # Update frequency domain plot with selective harmonics
        self.update_selective_freq_plot(t, original, reconstructed, a0, an, bn, enabled_harmonics)
        
        # Update 3D visualization with selective harmonics
        self.update_selective_3d_plot(t, original, a0, an, bn, enabled_harmonics)
        
        # Update convergence analysis with selective harmonics
        self.update_selective_convergence_plot(t, original, a0, an, bn, enabled_harmonics)
    
    def update_selective_time_plot(self, t, original, reconstructed, a0, an, bn, enabled_harmonics):
        """Update time domain plot with selective harmonic reconstruction"""
        self.time_plot.fig.clear()
        ax = self.time_plot.fig.add_subplot(111, facecolor='#0d1117')
        
        # Plot original signal
        ax.plot(t, original, color='#58a6ff', linewidth=3, label='Original Function', alpha=0.9)
        
        # Plot selective reconstruction
        ax.plot(t, reconstructed, color='#ff6b6b', linewidth=2.5, linestyle='--', 
               label='Selective Reconstruction', alpha=0.8)
        
        # Count enabled harmonics for display
        enabled_count = sum(enabled_harmonics)
        total_harmonics = len(enabled_harmonics)
        
        # Enhanced axes styling
        ax.set_xlabel('Time (s)', color='#e6f3ff', fontsize=12, fontweight='bold')
        ax.set_ylabel('Amplitude', color='#e6f3ff', fontsize=12, fontweight='bold')
        ax.set_title(f'Selective Harmonic Reconstruction ({enabled_count}/{total_harmonics} harmonics)', 
                    color='#58a6ff', fontsize=14, fontweight='bold', pad=20)
        
        # Enhanced legend
        legend = ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True,
                          facecolor='#161b22', edgecolor='#0066cc', framealpha=0.9)
        legend.get_frame().set_linewidth(2)
        for text in legend.get_texts():
            text.set_color('#e6f3ff')
            text.set_fontsize(11)
            text.set_fontweight('bold')
        
        # Enhanced grid
        ax.grid(True, alpha=0.3, color='#30363d', linestyle='-', linewidth=0.8)
        ax.set_facecolor('#0d1117')
        
        # Enhanced tick styling
        ax.tick_params(colors='#e6f3ff', labelsize=10, width=1.5)
        for spine in ax.spines.values():
            spine.set_color('#0066cc')
            spine.set_linewidth(2)
        
        # Add harmonic selection info
        enabled_list = [i+1 for i, enabled in enumerate(enabled_harmonics) if enabled]
        if enabled_list:
            enabled_text = f"Enabled: H{', H'.join(map(str, enabled_list[:10]))}"
            if len(enabled_list) > 10:
                enabled_text += f" ... (+{len(enabled_list)-10} more)"
        else:
            enabled_text = "No harmonics enabled"
        
        ax.text(0.02, 0.98, enabled_text, transform=ax.transAxes, 
               color='#e6f3ff', fontsize=10, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='#161b22', alpha=0.8),
               verticalalignment='top')
        
        self.time_plot.fig.patch.set_facecolor('#1a1a1a')
        self.time_plot.fig.tight_layout(pad=2.0)
        self.time_plot.draw()
    
    def update_selective_freq_plot(self, t, original, reconstructed, a0, an, bn, enabled_harmonics):
        """Update frequency domain plot with selective harmonics"""
        self.freq_plot.fig.clear()
        
        # Create selective coefficients (zero out disabled harmonics)
        selective_an = an.copy()
        selective_bn = bn.copy()
        for i, enabled in enumerate(enabled_harmonics):
            if not enabled and i < len(selective_an):
                selective_an[i] = 0
                selective_bn[i] = 0
        
        # Magnitude spectrum
        ax2 = self.freq_plot.fig.add_subplot(211, facecolor='#0d1117')
        harmonics = np.arange(1, len(an) + 1)
        magnitude = np.sqrt(selective_an**2 + selective_bn**2)
        
        # Enhanced DC component
        markerline, stemlines, baseline = ax2.stem([0], [a0/2], linefmt='none', markerfmt='o',
                                                  basefmt=' ' )
        markerline.set_markerfacecolor('#58a6ff')
        markerline.set_markeredgecolor('#79c0ff')
        markerline.set_markersize(10)
        stemlines.set_color('#58a6ff')
        stemlines.set_linewidth(3)
        
        # Enhanced harmonics with selective coloring
        markerline, stemlines, baseline = ax2.stem(harmonics, magnitude, linefmt='none', markerfmt='o',
                                                  basefmt=' ' )
        
        # Use a single color for all markers (simplified approach)
        markerline.set_markerfacecolor('#ff6b6b')
        markerline.set_markeredgecolor('#ff7f7f')
        markerline.set_markersize(8)
        stemlines.set_color('#ff6b6b')
        stemlines.set_linewidth(2.5)
        
        ax2.set_xlabel('Harmonic Number', color='#e6f3ff', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Magnitude', color='#e6f3ff', fontsize=11, fontweight='bold')
        ax2.set_title('Selective Magnitude Spectrum', color='#58a6ff', fontsize=13, fontweight='bold')
        ax2.tick_params(colors='#e6f3ff', labelsize=9)
        ax2.grid(True, alpha=0.3, color='#30363d')
        for spine in ax2.spines.values():
            spine.set_color('#0066cc')
            spine.set_linewidth(1.5)
        
        # Enhanced Phase spectrum
        ax3 = self.freq_plot.fig.add_subplot(212, facecolor='#0d1117')
        phase = np.arctan2(selective_bn, selective_an)
        markerline, stemlines, baseline = ax3.stem(harmonics, phase, linefmt='none', markerfmt='s',
                                                  basefmt=' ' )
        
        # Use a single color for all markers (simplified approach)
        markerline.set_markerfacecolor('#4ecdc4')
        markerline.set_markeredgecolor('#5dd9d1')
        markerline.set_markersize(7)
        stemlines.set_color('#4ecdc4')
        stemlines.set_linewidth(2)
        
        ax3.set_xlabel('Harmonic Number', color='#e6f3ff', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Phase (rad)', color='#e6f3ff', fontsize=11, fontweight='bold')
        ax3.set_title('Selective Phase Spectrum', color='#58a6ff', fontsize=13, fontweight='bold')
        ax3.tick_params(colors='#e6f3ff', labelsize=9)
        ax3.grid(True, alpha=0.3, color='#30363d')
        for spine in ax3.spines.values():
            spine.set_color('#0066cc')
            spine.set_linewidth(1.5)
        
        self.freq_plot.fig.patch.set_facecolor('#1a1a1a')
        self.freq_plot.fig.tight_layout(pad=2.0)
        self.freq_plot.draw()
    
    def update_selective_3d_plot(self, t, original, a0, an, bn, enabled_harmonics):
        """Create 3D waterfall plot showing selective harmonic buildup"""
        self.plot_3d.fig.clear()
        ax = self.plot_3d.fig.add_subplot(111, projection='3d', facecolor='#0d1117')
        
        # Generate selective reconstructions for 3D display
        n_harmonics = len(an)
        max_display_harmonics = min(20, n_harmonics)  # Limit for performance
        
        # Sample fewer time points for 3D performance
        t_3d = t[::10]  # Every 10th point
        original_3d = original[::10]
        
        # Plot original signal at the back
        ax.plot(t_3d, [0] * len(t_3d), original_3d, 
               color='#58a6ff', linewidth=3, alpha=0.8, label='Original')
        
        # Plot selective reconstructions
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7', 
                 '#ff7675', '#74b9ff', '#fd79a8', '#fdcb6e', '#6c5ce7']
        # Repeat colors if needed
        while len(colors) < max_display_harmonics:
            colors.extend(colors)
        colors = colors[:max_display_harmonics]
        
        for h in range(1, max_display_harmonics + 1, 2):  # Every other harmonic for clarity
            # Reconstruct with selective harmonics up to h
            reconstruction = a0/2 * np.ones_like(t_3d)
            for n in range(h):
                if n < len(an) and enabled_harmonics[n]:  # Only include enabled harmonics
                    reconstruction += an[n] * np.cos((n+1) * self.analyzer.omega0 * t_3d)
                    reconstruction += bn[n] * np.sin((n+1) * self.analyzer.omega0 * t_3d)
            
            ax.plot(t_3d, [h] * len(t_3d), reconstruction,
                   color=colors[h-1], linewidth=2, alpha=0.7)
        
        # Styling for 3D plot
        ax.set_xlabel('Time (s)', color='#e6f3ff', fontsize=11, fontweight='bold')
        ax.set_ylabel('Harmonics', color='#e6f3ff', fontsize=11, fontweight='bold') 
        
        # Handle 3D-specific attributes safely
        try:
            ax.set_zlabel('Amplitude', color='#e6f3ff', fontsize=11, fontweight='bold')  # type: ignore
        except AttributeError:
            pass  # Not a 3D axes
            
        ax.set_title('Selective 3D Harmonic Buildup', color='#58a6ff', 
                    fontsize=13, fontweight='bold', pad=20)
        
        # Set background and grid colors for 3D
        try:
            ax.xaxis.pane.fill = False  # type: ignore
            ax.xaxis.pane.set_edgecolor('#30363d')  # type: ignore
            ax.yaxis.pane.fill = False  # type: ignore
            ax.yaxis.pane.set_edgecolor('#30363d')  # type: ignore
            ax.zaxis.pane.fill = False  # type: ignore
            ax.zaxis.pane.set_edgecolor('#30363d')  # type: ignore
        except AttributeError:
            pass  # Not a 3D axes or missing pane attributes
            
        ax.grid(True, alpha=0.3, color='#30363d')
        
        # Tick colors
        ax.tick_params(colors='#e6f3ff', labelsize=9)
        
        self.plot_3d.fig.patch.set_facecolor('#1a1a1a')
        self.plot_3d.draw()
    
    def update_selective_convergence_plot(self, t, original, a0, an, bn, enabled_harmonics):
        """Create convergence analysis showing error vs selective harmonics"""
        self.convergence_plot.fig.clear()
        
        # Calculate selective reconstructions and errors
        n_harmonics = len(an)
        harmonic_range = np.arange(1, n_harmonics + 1)
        rms_errors = []
        max_errors = []
        snr_values = []
        power_ratios = []
        
        for h in harmonic_range:
            # Reconstruct with selective harmonics up to h
            reconstruction = a0/2 * np.ones_like(t)
            for n in range(h):
                if n < len(an) and enabled_harmonics[n]:  # Only include enabled harmonics
                    reconstruction += an[n] * np.cos((n+1) * self.analyzer.omega0 * t)
                    reconstruction += bn[n] * np.sin((n+1) * self.analyzer.omega0 * t)
            
            # Calculate metrics
            rms_error = np.sqrt(np.mean((original - reconstruction)**2))
            max_error = np.max(np.abs(original - reconstruction))
            
            # Signal-to-noise ratio
            signal_power = np.mean(original**2)
            noise_power = np.mean((original - reconstruction)**2)
            snr = 10 * np.log10(signal_power / (noise_power + 1e-12))
            
            # Power captured by selective harmonics
            total_power = np.sum(an**2 + bn**2)
            captured_power = np.sum([an[i]**2 + bn[i]**2 for i in range(h) if enabled_harmonics[i]])
            power_ratio = captured_power / (total_power + 1e-12) * 100
            
            rms_errors.append(rms_error)
            max_errors.append(max_error)
            snr_values.append(snr)
            power_ratios.append(power_ratio)
        
        # Create subplots for convergence analysis
        ax1 = self.convergence_plot.fig.add_subplot(221, facecolor='#0d1117')
        ax2 = self.convergence_plot.fig.add_subplot(222, facecolor='#0d1117')
        ax3 = self.convergence_plot.fig.add_subplot(223, facecolor='#0d1117')
        ax4 = self.convergence_plot.fig.add_subplot(224, facecolor='#0d1117')
        
        # RMS Error vs Harmonics
        ax1.semilogy(harmonic_range, rms_errors, color='#ff6b6b', linewidth=2.5, 
                    marker='o', markersize=4, markerfacecolor='#ff7f7f')
        ax1.set_xlabel('Number of Harmonics', color='#e6f3ff', fontweight='bold')
        ax1.set_ylabel('RMS Error', color='#e6f3ff', fontweight='bold')
        ax1.set_title('Selective RMS Error Convergence', color='#58a6ff', fontweight='bold')
        ax1.grid(True, alpha=0.3, color='#30363d')
        ax1.tick_params(colors='#e6f3ff', labelsize=9)
        for spine in ax1.spines.values():
            spine.set_color('#0066cc')
        
        # Maximum Error vs Harmonics
        ax2.semilogy(harmonic_range, max_errors, color='#4ecdc4', linewidth=2.5,
                    marker='s', markersize=4, markerfacecolor='#5dd9d1')
        ax2.set_xlabel('Number of Harmonics', color='#e6f3ff', fontweight='bold')
        ax2.set_ylabel('Maximum Error', color='#e6f3ff', fontweight='bold')
        ax2.set_title('Selective Maximum Error Convergence', color='#58a6ff', fontweight='bold')
        ax2.grid(True, alpha=0.3, color='#30363d')
        ax2.tick_params(colors='#e6f3ff', labelsize=9)
        for spine in ax2.spines.values():
            spine.set_color('#0066cc')
        
        # SNR vs Harmonics
        ax3.plot(harmonic_range, snr_values, color='#ffd93d', linewidth=2.5,
                marker='^', markersize=4, markerfacecolor='#ffe066')
        ax3.set_xlabel('Number of Harmonics', color='#e6f3ff', fontweight='bold')
        ax3.set_ylabel('SNR (dB)', color='#e6f3ff', fontweight='bold')
        ax3.set_title('Selective Signal-to-Noise Ratio', color='#58a6ff', fontweight='bold')
        ax3.grid(True, alpha=0.3, color='#30363d')
        ax3.tick_params(colors='#e6f3ff', labelsize=9)
        for spine in ax3.spines.values():
            spine.set_color('#0066cc')
        
        # Power Capture vs Harmonics
        ax4.plot(harmonic_range, power_ratios, color='#a8e6cf', linewidth=2.5,
                marker='d', markersize=4, markerfacecolor='#b8f0df')
        ax4.axhline(y=95, color='#ff6b6b', linestyle='--', alpha=0.7, linewidth=2)
        ax4.axhline(y=99, color='#58a6ff', linestyle='--', alpha=0.7, linewidth=2)
        ax4.set_xlabel('Number of Harmonics', color='#e6f3ff', fontweight='bold')
        ax4.set_ylabel('Power Captured (%)', color='#e6f3ff', fontweight='bold')
        ax4.set_title('Selective Cumulative Power Capture', color='#58a6ff', fontweight='bold')
        ax4.set_ylim(0, 105)
        ax4.grid(True, alpha=0.3, color='#30363d')
        ax4.tick_params(colors='#e6f3ff', labelsize=9)
        for spine in ax4.spines.values():
            spine.set_color('#0066cc')
        
        # Add text annotations for key metrics
        final_rms = rms_errors[-1]
        final_snr = snr_values[-1]
        final_power = power_ratios[-1]
        
        ax1.text(0.05, 0.95, f'Final RMS: {final_rms:.4f}', transform=ax1.transAxes,
                color='#e6f3ff', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='#161b22', alpha=0.8))
        
        ax3.text(0.05, 0.95, f'Final SNR: {final_snr:.1f} dB', transform=ax3.transAxes,
                color='#e6f3ff', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='#161b22', alpha=0.8))
        
        ax4.text(0.05, 0.05, f'Power: {final_power:.1f}%', transform=ax4.transAxes,
                color='#e6f3ff', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='#161b22', alpha=0.8))
        
        # Find 95% and 99% power points
        power_95_idx = np.argmax(np.array(power_ratios) >= 95)
        power_99_idx = np.argmax(np.array(power_ratios) >= 99)
        
        if power_95_idx > 0:
            ax4.annotate(f'95% at H{power_95_idx+1}', 
                        xy=(float(power_95_idx+1), 95.0), xytext=(float(power_95_idx+5), 85.0),
                        arrowprops=dict(arrowstyle='->', color='#ff6b6b', alpha=0.7),
                        color='#ff6b6b', fontweight='bold', fontsize=9)
        
        if power_99_idx > 0:
            ax4.annotate(f'99% at H{power_99_idx+1}', 
                        xy=(float(power_99_idx+1), 99.0), xytext=(float(power_99_idx+5), 102.0),
                        arrowprops=dict(arrowstyle='->', color='#58a6ff', alpha=0.7),
                        color='#58a6ff', fontweight='bold', fontsize=9)
        
        self.convergence_plot.fig.patch.set_facecolor('#1a1a1a')
        self.convergence_plot.fig.tight_layout(pad=2.0)
        self.convergence_plot.draw()
    
    def start_animation(self):
        """Start the progressive reconstruction animation"""
        self.animation_step = 0
        self.animation_timer.start(200)  # 200ms intervals
    
    def pause_animation(self):
        """Pause the animation"""
        self.animation_timer.stop()
    
    def reset_animation(self):
        """Reset animation to beginning"""
        self.animation_timer.stop()
        self.animation_step = 0
    
    def animate_step(self):
        """Single step of the animation with enhanced styling"""
        if not hasattr(self, 'progressive_data') or self.animation_step >= len(self.progressive_data):
            self.animation_timer.stop()
            return
        
        # Enhanced animation plot
        self.time_plot.fig.clear()
        ax = self.time_plot.fig.add_subplot(111, facecolor='#0d1117')
        
        # Progressive build-up with color transition
        progress_ratio = self.animation_step / max(1, len(self.progressive_data) - 1)
        
        ax.plot(self.t_data, self.original_data, color='#58a6ff', linewidth=3, 
               label='Original Function', alpha=0.9)
        ax.plot(self.t_data, self.progressive_data[self.animation_step], 
               color='#ff6b6b', linewidth=3, linestyle='--',
               label=f'Harmonics: {self.animation_step}', alpha=0.9)
        
        # Add convergence info to animation
        if hasattr(self, 'convergence_data'):
            current_error = self.convergence_data['rms_errors'][min(self.animation_step, 
                                                                   len(self.convergence_data['rms_errors'])-1)]
            ax.text(0.02, 0.98, f'RMS Error: {current_error:.4f}', 
                   transform=ax.transAxes, color='#e6f3ff', fontsize=11, fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='#161b22', alpha=0.8),
                   verticalalignment='top')
        
        # Enhanced animation styling
        ax.set_xlabel('Time (s)', color='#e6f3ff', fontsize=12, fontweight='bold')
        ax.set_ylabel('Amplitude', color='#e6f3ff', fontsize=12, fontweight='bold')
        ax.set_title(f'Progressive Reconstruction - Harmonics: {self.animation_step}', 
                    color='#58a6ff', fontsize=14, fontweight='bold', pad=20)
        
        legend = ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True,
                          facecolor='#161b22', edgecolor='#0066cc', framealpha=0.9)
        for text in legend.get_texts():
            text.set_color('#e6f3ff')
            text.set_fontweight('bold')
        
        ax.grid(True, alpha=0.3, color='#30363d')
        ax.tick_params(colors='#e6f3ff', labelsize=10)
        for spine in ax.spines.values():
            spine.set_color('#0066cc')
            spine.set_linewidth(2)
        
        # Progress bar effect at bottom
        progress_width = progress_ratio * 0.9
        ax.axhspan(-0.02, -0.01, xmin=0.05, xmax=0.05 + progress_width, 
                  transform=ax.transAxes, color='#58a6ff', alpha=0.7)
        
        self.time_plot.fig.patch.set_facecolor('#1a1a1a')
        self.time_plot.draw()
        
        self.animation_step += 1

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for better dark theme
    
    # Set dark palette
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    window = FourierSeriesMainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
