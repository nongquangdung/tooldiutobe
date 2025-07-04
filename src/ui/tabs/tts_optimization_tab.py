"""
TTS Optimization Settings Tab
Provides UI controls for ChatterboxTTS optimization parameters
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, 
    QComboBox, QCheckBox, QSlider, QPushButton, QSpinBox,
    QDoubleSpinBox, QTextEdit, QTabWidget, QGridLayout,
    QProgressBar, QMessageBox, QSplitter, QFormLayout,
    QButtonGroup, QRadioButton, QFrame, QScrollArea
)
from PySide6.QtCore import Qt, Signal, QTimer, QThread
from PySide6.QtGui import QFont, QPalette
import json
import os
import torch

from ..styles import COLORS, BUTTON_STYLE, LABEL_STYLE

class TtsOptimizationTab(QWidget):
    """🚀 TTS Optimization Settings Tab"""
    
    optimization_changed = Signal(dict)  # Emit when settings change
    
    def __init__(self):
        super().__init__()
        self.current_settings = self._load_default_settings()
        self.auto_apply = True
        self.setup_ui()
        self._load_saved_settings()
        self._update_gpu_info()
        
    def setup_ui(self):
        """Setup the optimization UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Header with GPU info
        header_group = self._create_header_section()
        layout.addWidget(header_group)
        
        # Main splitter for left/right panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel: Core optimization settings
        left_panel = self._create_optimization_panel()
        splitter.addWidget(left_panel)
        
        # Right panel: Advanced settings & monitoring
        right_panel = self._create_advanced_panel()
        splitter.addWidget(right_panel)
        
        splitter.setStretchFactor(0, 2)  # Left panel wider
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter)
        
        # Bottom: Apply/Reset controls
        controls_group = self._create_controls_section()
        layout.addWidget(controls_group)
        
    def _create_header_section(self):
        """Create header with GPU info and optimization status"""
        group = QGroupBox("🚀 TTS Optimization Status")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                font-size: 14px;
                border: 2px solid {COLORS['primary']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: {COLORS['surface']};
            }}
        """)
        
        layout = QGridLayout(group)
        
        # GPU Status
        self.gpu_status_label = QLabel("🔍 Detecting GPU...")
        self.gpu_status_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px;")
        layout.addWidget(QLabel("Hardware:"), 0, 0)
        layout.addWidget(self.gpu_status_label, 0, 1, 1, 2)
        
        # Optimization Status
        self.opt_status_label = QLabel("⚠️ Not optimized")
        self.opt_status_label.setStyleSheet("color: #FF6B35; font-weight: bold;")
        layout.addWidget(QLabel("Status:"), 1, 0)
        layout.addWidget(self.opt_status_label, 1, 1, 1, 2)
        
        # Performance Estimate
        self.perf_estimate_label = QLabel("📊 Calculate performance...")
        layout.addWidget(QLabel("Expected:"), 2, 0)
        layout.addWidget(self.perf_estimate_label, 2, 1, 1, 2)
        
        return group
    
    def _create_optimization_panel(self):
        """Create main optimization settings panel"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # === 1. Core Optimization Settings ===
        core_group = QGroupBox("⚡ Core Optimization")
        core_layout = QFormLayout(core_group)
        
        # Enable/Disable optimization
        self.enable_optimization_cb = QCheckBox("Enable TTS Optimization")
        self.enable_optimization_cb.setChecked(True)
        self.enable_optimization_cb.toggled.connect(self._on_optimization_toggled)
        core_layout.addRow(self.enable_optimization_cb)
        
        # Optimization preset
        preset_layout = QHBoxLayout()
        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            "🚀 Maximum Performance (RTX 40xx)",
            "⚡ High Performance (RTX 30xx)", 
            "🔋 Balanced (RTX 20xx/GTX 16xx)",
            "💾 Memory Optimized (GTX 10xx)",
            "🛡️ Conservative (Older GPUs)",
            "🎛️ Custom"
        ])
        self.preset_combo.currentTextChanged.connect(self._on_preset_changed)
        preset_layout.addWidget(self.preset_combo)
        
        self.auto_detect_btn = QPushButton("🔍 Auto")
        self.auto_detect_btn.setMaximumWidth(60)
        self.auto_detect_btn.clicked.connect(self._auto_detect_preset)
        preset_layout.addWidget(self.auto_detect_btn)
        
        core_layout.addRow("Optimization Preset:", preset_layout)
        layout.addWidget(core_group)
        
        # === 2. Precision Settings ===
        precision_group = QGroupBox("🎯 Precision & Data Type")
        precision_layout = QFormLayout(precision_group)
        
        # Data type selection
        dtype_layout = QHBoxLayout()
        self.dtype_combo = QComboBox()
        self.dtype_combo.addItems(["float32 (Stable)", "float16 (Fast)", "bfloat16 (Experimental)"])
        self.dtype_combo.currentTextChanged.connect(self._on_dtype_changed)
        dtype_layout.addWidget(self.dtype_combo)
        
        # Dtype info button
        self.dtype_info_btn = QPushButton("ℹ️")
        self.dtype_info_btn.setMaximumWidth(30)
        self.dtype_info_btn.clicked.connect(self._show_dtype_info)
        dtype_layout.addWidget(self.dtype_info_btn)
        
        precision_layout.addRow("Data Type:", dtype_layout)
        
        # Mixed precision controls
        self.mixed_precision_cb = QCheckBox("Enable Mixed Precision")
        self.mixed_precision_cb.setToolTip("Use FP16 for non-critical operations while keeping FP32 for stability")
        precision_layout.addRow(self.mixed_precision_cb)
        
        layout.addWidget(precision_group)
        
        # === 3. Compilation Settings ===
        compile_group = QGroupBox("🔧 Torch Compilation")
        compile_layout = QFormLayout(compile_group)
        
        # Enable compilation
        self.enable_compilation_cb = QCheckBox("Enable Torch Compilation")
        self.enable_compilation_cb.toggled.connect(self._on_compilation_toggled)
        compile_layout.addRow(self.enable_compilation_cb)
        
        # Compilation backend
        self.backend_combo = QComboBox()
        self.backend_combo.addItems(["cudagraphs", "inductor", "aot_autograd"])
        compile_layout.addRow("Backend:", self.backend_combo)
        
        # Fullgraph mode
        self.fullgraph_cb = QCheckBox("Fullgraph Mode")
        self.fullgraph_cb.setToolTip("More aggressive optimization, may fail on some models")
        compile_layout.addRow(self.fullgraph_cb)
        
        layout.addWidget(compile_group)
        
        # === 4. Memory Management ===
        memory_group = QGroupBox("💾 Memory Management")
        memory_layout = QFormLayout(memory_group)
        
        # CPU Offloading
        self.cpu_offload_cb = QCheckBox("Enable CPU Offloading")
        self.cpu_offload_cb.setToolTip("Move model to CPU when not in use to save VRAM")
        memory_layout.addRow(self.cpu_offload_cb)
        
        # Voice caching
        cache_layout = QHBoxLayout()
        self.voice_cache_cb = QCheckBox("Voice Cache")
        cache_layout.addWidget(self.voice_cache_cb)
        
        self.cache_size_spin = QSpinBox()
        self.cache_size_spin.setRange(1, 50)
        self.cache_size_spin.setValue(10)
        self.cache_size_spin.setSuffix(" voices")
        cache_layout.addWidget(self.cache_size_spin)
        
        memory_layout.addRow("Caching:", cache_layout)
        
        # Chunked processing
        chunk_layout = QHBoxLayout()
        self.chunked_processing_cb = QCheckBox("Chunked Processing")
        chunk_layout.addWidget(self.chunked_processing_cb)
        
        self.chunk_size_spin = QSpinBox()
        self.chunk_size_spin.setRange(50, 500)
        self.chunk_size_spin.setValue(200)
        self.chunk_size_spin.setSuffix(" chars")
        chunk_layout.addWidget(self.chunk_size_spin)
        
        memory_layout.addRow("Text Chunking:", chunk_layout)
        
        layout.addWidget(memory_group)
        
        # === 5. Generation Settings ===
        gen_group = QGroupBox("🎤 Generation Optimization")
        gen_layout = QFormLayout(gen_group)
        
        # Lazy loading
        self.lazy_load_cb = QCheckBox("Lazy Model Loading")
        self.lazy_load_cb.setToolTip("Load model only when needed for faster startup")
        gen_layout.addRow(self.lazy_load_cb)
        
        # Streaming generation
        self.streaming_cb = QCheckBox("Streaming Generation")
        self.streaming_cb.setToolTip("Generate audio in real-time chunks")
        gen_layout.addRow(self.streaming_cb)
        
        # Warmup iterations
        warmup_layout = QHBoxLayout()
        self.warmup_spin = QSpinBox()
        self.warmup_spin.setRange(0, 10)
        self.warmup_spin.setValue(2)
        self.warmup_spin.setSuffix(" iterations")
        warmup_layout.addWidget(self.warmup_spin)
        
        gen_layout.addRow("Compilation Warmup:", warmup_layout)
        
        layout.addWidget(gen_group)
        
        scroll.setWidget(widget)
        return scroll
    
    def _create_advanced_panel(self):
        """Create advanced settings and monitoring panel"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # === Advanced Tabs ===
        tab_widget = QTabWidget()
        
        # Environment Variables Tab
        env_tab = self._create_env_tab()
        tab_widget.addTab(env_tab, "🌍 Environment")
        
        # Monitoring Tab
        monitor_tab = self._create_monitoring_tab()
        tab_widget.addTab(monitor_tab, "📊 Monitor")
        
        # Benchmarks Tab
        benchmark_tab = self._create_benchmark_tab()
        tab_widget.addTab(benchmark_tab, "⚡ Benchmark")
        
        layout.addWidget(tab_widget)
        
        return widget
    
    def _create_env_tab(self):
        """Create environment variables configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Environment variables
        env_group = QGroupBox("🌍 Environment Variables")
        env_layout = QVBoxLayout(env_group)
        
        # Generate env vars button
        self.generate_env_btn = QPushButton("📋 Generate Environment Variables")
        self.generate_env_btn.clicked.connect(self._generate_env_vars)
        env_layout.addWidget(self.generate_env_btn)
        
        # Environment variables display
        self.env_text = QTextEdit()
        self.env_text.setPlaceholderText("Environment variables will appear here...")
        self.env_text.setMaximumHeight(150)
        env_layout.addWidget(self.env_text)
        
        # Copy to clipboard
        self.copy_env_btn = QPushButton("📋 Copy to Clipboard")
        self.copy_env_btn.clicked.connect(self._copy_env_vars)
        env_layout.addWidget(self.copy_env_btn)
        
        layout.addWidget(env_group)
        
        # Save/Load presets
        preset_group = QGroupBox("💾 Optimization Presets")
        preset_layout = QVBoxLayout(preset_group)
        
        preset_buttons_layout = QHBoxLayout()
        self.save_preset_btn = QPushButton("💾 Save Preset")
        self.save_preset_btn.clicked.connect(self._save_preset)
        preset_buttons_layout.addWidget(self.save_preset_btn)
        
        self.load_preset_btn = QPushButton("📂 Load Preset")
        self.load_preset_btn.clicked.connect(self._load_preset)
        preset_buttons_layout.addWidget(self.load_preset_btn)
        
        preset_layout.addLayout(preset_buttons_layout)
        layout.addWidget(preset_group)
        
        layout.addStretch()
        return widget
    
    def _create_monitoring_tab(self):
        """Create real-time monitoring tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # GPU Monitoring
        gpu_group = QGroupBox("🖥️ GPU Monitoring")
        gpu_layout = QFormLayout(gpu_group)
        
        # Memory usage
        self.memory_usage_bar = QProgressBar()
        self.memory_usage_bar.setRange(0, 100)
        gpu_layout.addRow("VRAM Usage:", self.memory_usage_bar)
        
        # GPU utilization
        self.gpu_util_bar = QProgressBar()
        self.gpu_util_bar.setRange(0, 100)
        gpu_layout.addRow("GPU Utilization:", self.gpu_util_bar)
        
        # Temperature
        self.temp_label = QLabel("-- °C")
        gpu_layout.addRow("Temperature:", self.temp_label)
        
        layout.addWidget(gpu_group)
        
        # Performance Metrics
        perf_group = QGroupBox("📈 Performance Metrics")
        perf_layout = QFormLayout(perf_group)
        
        self.avg_generation_time = QLabel("-- seconds")
        perf_layout.addRow("Avg Generation Time:", self.avg_generation_time)
        
        self.real_time_factor = QLabel("--x real-time")
        perf_layout.addRow("Real-time Factor:", self.real_time_factor)
        
        self.total_generations = QLabel("0")
        perf_layout.addRow("Total Generations:", self.total_generations)
        
        layout.addWidget(perf_group)
        
        # Auto-refresh monitoring
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self._update_monitoring)
        self.monitor_timer.start(2000)  # Update every 2 seconds
        
        layout.addStretch()
        return widget
    
    def _create_benchmark_tab(self):
        """Create benchmarking tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Benchmark controls
        bench_group = QGroupBox("⚡ Performance Benchmark")
        bench_layout = QVBoxLayout(bench_group)
        
        # Test settings
        test_layout = QFormLayout()
        
        self.test_text_combo = QComboBox()
        self.test_text_combo.addItems([
            "Short (10 words)",
            "Medium (50 words)", 
            "Long (200 words)",
            "Very Long (500 words)"
        ])
        test_layout.addRow("Test Text Length:", self.test_text_combo)
        
        self.test_iterations_spin = QSpinBox()
        self.test_iterations_spin.setRange(1, 10)
        self.test_iterations_spin.setValue(3)
        test_layout.addRow("Iterations:", self.test_iterations_spin)
        
        bench_layout.addLayout(test_layout)
        
        # Run benchmark
        self.run_benchmark_btn = QPushButton("🚀 Run Benchmark")
        self.run_benchmark_btn.clicked.connect(self._run_benchmark)
        bench_layout.addWidget(self.run_benchmark_btn)
        
        # Benchmark progress
        self.benchmark_progress = QProgressBar()
        self.benchmark_progress.setVisible(False)
        bench_layout.addWidget(self.benchmark_progress)
        
        # Results
        self.benchmark_results = QTextEdit()
        self.benchmark_results.setPlaceholderText("Benchmark results will appear here...")
        self.benchmark_results.setMaximumHeight(200)
        bench_layout.addWidget(self.benchmark_results)
        
        layout.addWidget(bench_group)
        layout.addStretch()
        return widget
    
    def _create_controls_section(self):
        """Create apply/reset controls"""
        group = QGroupBox()
        layout = QHBoxLayout(group)
        
        # Auto-apply checkbox
        self.auto_apply_cb = QCheckBox("Auto-apply changes")
        self.auto_apply_cb.setChecked(True)
        self.auto_apply_cb.toggled.connect(self._on_auto_apply_toggled)
        layout.addWidget(self.auto_apply_cb)
        
        layout.addStretch()
        
        # Control buttons
        self.reset_btn = QPushButton("🔄 Reset to Default")
        self.reset_btn.clicked.connect(self._reset_to_default)
        layout.addWidget(self.reset_btn)
        
        self.apply_btn = QPushButton("✅ Apply Settings")
        self.apply_btn.setStyleSheet(BUTTON_STYLE.replace('#5856D6', '#28CD41'))
        self.apply_btn.clicked.connect(self._apply_settings)
        self.apply_btn.setEnabled(not self.auto_apply)
        layout.addWidget(self.apply_btn)
        
        return group
    
    def _load_default_settings(self):
        """Load default optimization settings"""
        return {
            'enabled': True,
            'preset': 'balanced',
            'dtype': 'float16',
            'mixed_precision': True,
            'compilation': True,
            'backend': 'cudagraphs',
            'fullgraph': True,
            'cpu_offload': False,
            'voice_cache': True,
            'cache_size': 10,
            'chunked_processing': True,
            'chunk_size': 200,
            'lazy_load': True,
            'streaming': False,
            'warmup_iterations': 2
        }
    
    def _update_gpu_info(self):
        """Update GPU information display"""
        try:
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                memory_total = torch.cuda.get_device_properties(0).total_memory // (1024**3)
                memory_used = torch.cuda.memory_allocated(0) // (1024**3)
                
                self.gpu_status_label.setText(f"🖥️ {gpu_name} ({memory_total}GB)")
                self.gpu_status_label.setStyleSheet(f"color: {COLORS['success']}; font-weight: bold;")
                
                # Update optimization status
                if self.current_settings['enabled']:
                    self.opt_status_label.setText("✅ Optimized")
                    self.opt_status_label.setStyleSheet("color: #28CD41; font-weight: bold;")
                    
                    # Calculate performance estimate
                    gpu_score = self._calculate_gpu_score(gpu_name)
                    speedup = self._estimate_speedup(gpu_score)
                    self.perf_estimate_label.setText(f"🚀 ~{speedup:.1f}x faster")
                    
            else:
                self.gpu_status_label.setText("❌ CUDA not available")
                self.gpu_status_label.setStyleSheet("color: #FF6B35;")
                
        except Exception as e:
            self.gpu_status_label.setText(f"⚠️ Error: {str(e)}")
    
    def _calculate_gpu_score(self, gpu_name):
        """Calculate GPU performance score"""
        gpu_scores = {
            'RTX 4090': 100,
            'RTX 4080': 85,
            'RTX 4070': 70,
            'RTX 3090': 90,
            'RTX 3080': 80,
            'RTX 3070': 65,
            'RTX 3060': 50,
            'RTX 2080': 60,
            'RTX 2070': 45,
            'GTX 1080': 35,
            'GTX 1070': 25
        }
        
        for gpu, score in gpu_scores.items():
            if gpu in gpu_name:
                return score
        return 20  # Default for unknown GPUs
    
    def _estimate_speedup(self, gpu_score):
        """Estimate speedup based on GPU score and settings"""
        base_speedup = 1.0
        
        if self.current_settings['compilation']:
            base_speedup += 0.5 + (gpu_score / 100) * 2.0
        
        if self.current_settings['dtype'] == 'float16' and gpu_score > 40:
            base_speedup += 0.3 + (gpu_score / 100) * 1.0
        
        if self.current_settings['voice_cache']:
            base_speedup += 0.2
        
        return min(base_speedup, 6.0)  # Cap at 6x
    
    def _on_optimization_toggled(self, enabled):
        """Handle optimization enable/disable"""
        self.current_settings['enabled'] = enabled
        if self.auto_apply:
            self._apply_settings()
        self._update_gpu_info()
    
    def _on_preset_changed(self, preset_text):
        """Handle preset selection change"""
        preset_map = {
            "🚀 Maximum Performance (RTX 40xx)": "maximum",
            "⚡ High Performance (RTX 30xx)": "high", 
            "🔋 Balanced (RTX 20xx/GTX 16xx)": "balanced",
            "💾 Memory Optimized (GTX 10xx)": "memory_optimized",
            "🛡️ Conservative (Older GPUs)": "conservative",
            "🎛️ Custom": "custom"
        }
        
        preset = preset_map.get(preset_text, "balanced")
        self._apply_preset(preset)
    
    def _apply_preset(self, preset):
        """Apply optimization preset"""
        presets = {
            "maximum": {
                'dtype': 'float16',
                'compilation': True,
                'backend': 'cudagraphs',
                'fullgraph': True,
                'cpu_offload': False,
                'voice_cache': True,
                'cache_size': 20,
                'chunked_processing': True,
                'chunk_size': 150,
                'streaming': True
            },
            "high": {
                'dtype': 'float16',
                'compilation': True,
                'backend': 'cudagraphs',
                'fullgraph': True,
                'cpu_offload': False,
                'voice_cache': True,
                'cache_size': 15,
                'chunked_processing': True,
                'chunk_size': 180
            },
            "balanced": {
                'dtype': 'float16',
                'compilation': True,
                'backend': 'cudagraphs',
                'fullgraph': False,
                'cpu_offload': False,
                'voice_cache': True,
                'cache_size': 10,
                'chunked_processing': True,
                'chunk_size': 200
            },
            "memory_optimized": {
                'dtype': 'float32',
                'compilation': False,
                'cpu_offload': True,
                'voice_cache': True,
                'cache_size': 5,
                'chunked_processing': True,
                'chunk_size': 250
            },
            "conservative": {
                'dtype': 'float32',
                'compilation': False,
                'cpu_offload': False,
                'voice_cache': False,
                'chunked_processing': False
            }
        }
        
        if preset != "custom" and preset in presets:
            self.current_settings.update(presets[preset])
            self._update_ui_from_settings()
            if self.auto_apply:
                self._apply_settings()
    
    def _update_ui_from_settings(self):
        """Update UI controls from current settings"""
        # Update data type combo
        dtype_map = {"float32": 0, "float16": 1, "bfloat16": 2}
        self.dtype_combo.setCurrentIndex(dtype_map.get(self.current_settings.get('dtype', 'float16'), 1))
        
        # Update checkboxes
        self.enable_compilation_cb.setChecked(self.current_settings.get('compilation', True))
        self.fullgraph_cb.setChecked(self.current_settings.get('fullgraph', False))
        self.cpu_offload_cb.setChecked(self.current_settings.get('cpu_offload', False))
        self.voice_cache_cb.setChecked(self.current_settings.get('voice_cache', True))
        self.chunked_processing_cb.setChecked(self.current_settings.get('chunked_processing', True))
        self.lazy_load_cb.setChecked(self.current_settings.get('lazy_load', True))
        self.streaming_cb.setChecked(self.current_settings.get('streaming', False))
        
        # Update spinboxes
        self.cache_size_spin.setValue(self.current_settings.get('cache_size', 10))
        self.chunk_size_spin.setValue(self.current_settings.get('chunk_size', 200))
        self.warmup_spin.setValue(self.current_settings.get('warmup_iterations', 2))
        
        # Update backend combo
        backend_map = {"cudagraphs": 0, "inductor": 1, "aot_autograd": 2}
        self.backend_combo.setCurrentIndex(backend_map.get(self.current_settings.get('backend', 'cudagraphs'), 0))
    
    def _auto_detect_preset(self):
        """Auto-detect optimal preset based on GPU"""
        try:
            if not torch.cuda.is_available():
                self.preset_combo.setCurrentText("🛡️ Conservative (Older GPUs)")
                return
            
            gpu_name = torch.cuda.get_device_name(0)
            memory_gb = torch.cuda.get_device_properties(0).total_memory // (1024**3)
            
            if "RTX 40" in gpu_name or "RTX 4090" in gpu_name:
                self.preset_combo.setCurrentText("🚀 Maximum Performance (RTX 40xx)")
            elif "RTX 30" in gpu_name or "RTX 3080" in gpu_name or "RTX 3090" in gpu_name:
                self.preset_combo.setCurrentText("⚡ High Performance (RTX 30xx)")
            elif "RTX 20" in gpu_name or "GTX 16" in gpu_name:
                self.preset_combo.setCurrentText("🔋 Balanced (RTX 20xx/GTX 16xx)")
            elif "GTX 10" in gpu_name or memory_gb <= 8:
                self.preset_combo.setCurrentText("💾 Memory Optimized (GTX 10xx)")
            else:
                self.preset_combo.setCurrentText("🛡️ Conservative (Older GPUs)")
                
            QMessageBox.information(self, "Auto-Detection Complete", 
                                  f"Detected {gpu_name} with {memory_gb}GB VRAM\n"
                                  f"Recommended preset: {self.preset_combo.currentText()}")
        except Exception as e:
            QMessageBox.warning(self, "Auto-Detection Failed", f"Could not detect GPU: {str(e)}")
    
    def _generate_env_vars(self):
        """Generate environment variables from current settings"""
        env_vars = []
        
        if self.current_settings.get('enabled', True):
            env_vars.append(f"DISABLE_OPTIMIZATION=false")
        else:
            env_vars.append(f"DISABLE_OPTIMIZATION=true")
            
        env_vars.append(f"CHATTERBOX_DTYPE={self.current_settings.get('dtype', 'float16')}")
        env_vars.append(f"CHATTERBOX_COMPILATION={'true' if self.current_settings.get('compilation', True) else 'false'}")
        env_vars.append(f"CHATTERBOX_CPU_OFFLOAD={'true' if self.current_settings.get('cpu_offload', False) else 'false'}")
        env_vars.append(f"CHATTERBOX_LAZY_LOAD={'true' if self.current_settings.get('lazy_load', True) else 'false'}")
        
        if self.current_settings.get('chunked_processing', True):
            env_vars.append(f"CHATTERBOX_CHUNKED=true")
            env_vars.append(f"CHATTERBOX_CHUNK_SIZE={self.current_settings.get('chunk_size', 200)}")
        
        env_text = "\n".join(env_vars)
        self.env_text.setPlainText(env_text)
        
        # Show additional instructions
        instructions = "\n\n# To use these settings:\n"
        instructions += "# 1. Copy the above variables\n"
        instructions += "# 2. Add them to your .env file, or\n"
        instructions += "# 3. Set them in your shell before running:\n"
        instructions += "#    export VARIABLE_NAME=value  (Linux/macOS)\n"
        instructions += "#    $env:VARIABLE_NAME=\"value\"  (PowerShell)\n"
        
        self.env_text.setPlainText(env_text + instructions)
    
    def _copy_env_vars(self):
        """Copy environment variables to clipboard"""
        try:
            from PySide6.QtGui import QClipboard
            clipboard = QClipboard()
            text = self.env_text.toPlainText()
            # Extract only the actual env vars (before the comments)
            env_lines = [line for line in text.split('\n') if line and not line.startswith('#')]
            clipboard.setText('\n'.join(env_lines))
            QMessageBox.information(self, "Copied", "Environment variables copied to clipboard!")
        except Exception as e:
            QMessageBox.warning(self, "Copy Failed", f"Could not copy to clipboard: {str(e)}")
    
    def _update_monitoring(self):
        """Update real-time monitoring data"""
        try:
            if torch.cuda.is_available():
                # Memory usage
                memory_used = torch.cuda.memory_allocated(0)
                memory_total = torch.cuda.get_device_properties(0).total_memory
                memory_percent = int((memory_used / memory_total) * 100)
                self.memory_usage_bar.setValue(memory_percent)
                
                # GPU utilization (simplified)
                try:
                    utilization = torch.cuda.utilization(0) if hasattr(torch.cuda, 'utilization') else 0
                    self.gpu_util_bar.setValue(utilization)
                except:
                    self.gpu_util_bar.setValue(0)
                
                # Temperature (if available)
                try:
                    import pynvml
                    pynvml.nvmlInit()
                    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                    temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                    self.temp_label.setText(f"{temp}°C")
                except:
                    self.temp_label.setText("-- °C")
        except:
            pass
    
    def _run_benchmark(self):
        """Run performance benchmark"""
        self.run_benchmark_btn.setEnabled(False)
        self.benchmark_progress.setVisible(True)
        self.benchmark_progress.setValue(0)
        
        # TODO: Implement actual benchmarking
        # For now, show placeholder
        QMessageBox.information(self, "Benchmark", "Benchmark feature will be implemented in next update!")
        
        self.run_benchmark_btn.setEnabled(True)
        self.benchmark_progress.setVisible(False)
    
    def _on_auto_apply_toggled(self, enabled):
        """Handle auto-apply toggle"""
        self.auto_apply = enabled
        self.apply_btn.setEnabled(not enabled)
    
    def _apply_settings(self):
        """Apply current settings"""
        # Collect all current settings from UI
        self.current_settings.update({
            'dtype': ['float32', 'float16', 'bfloat16'][self.dtype_combo.currentIndex()],
            'compilation': self.enable_compilation_cb.isChecked(),
            'backend': ['cudagraphs', 'inductor', 'aot_autograd'][self.backend_combo.currentIndex()],
            'fullgraph': self.fullgraph_cb.isChecked(),
            'cpu_offload': self.cpu_offload_cb.isChecked(),
            'voice_cache': self.voice_cache_cb.isChecked(),
            'cache_size': self.cache_size_spin.value(),
            'chunked_processing': self.chunked_processing_cb.isChecked(),
            'chunk_size': self.chunk_size_spin.value(),
            'lazy_load': self.lazy_load_cb.isChecked(),
            'streaming': self.streaming_cb.isChecked(),
            'warmup_iterations': self.warmup_spin.value()
        })
        
        # Save settings
        self._save_settings()
        
        # Emit signal for other components
        self.optimization_changed.emit(self.current_settings)
        
        # Update status
        self._update_gpu_info()
        
        QMessageBox.information(self, "Settings Applied", 
                              "Optimization settings have been applied!\n"
                              "Restart the application for full effect.")
    
    def _reset_to_default(self):
        """Reset all settings to default"""
        self.current_settings = self._load_default_settings()
        self._update_ui_from_settings()
        if self.auto_apply:
            self._apply_settings()
    
    def _save_settings(self):
        """Save settings to file"""
        try:
            settings_file = os.path.join(os.getcwd(), "configs", "tts_optimization.json")
            os.makedirs(os.path.dirname(settings_file), exist_ok=True)
            
            with open(settings_file, 'w') as f:
                json.dump(self.current_settings, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save optimization settings: {e}")
    
    def _load_saved_settings(self):
        """Load saved settings from file"""
        try:
            settings_file = os.path.join(os.getcwd(), "configs", "tts_optimization.json")
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    saved_settings = json.load(f)
                    self.current_settings.update(saved_settings)
                    self._update_ui_from_settings()
        except Exception as e:
            print(f"Warning: Could not load optimization settings: {e}")
    
    def _save_preset(self):
        """Save current settings as named preset"""
        # TODO: Implement preset saving dialog
        QMessageBox.information(self, "Save Preset", "Preset saving will be implemented in next update!")
    
    def _load_preset(self):
        """Load a saved preset"""
        # TODO: Implement preset loading dialog
        QMessageBox.information(self, "Load Preset", "Preset loading will be implemented in next update!")
    
    def _show_dtype_info(self):
        """Show information about data types"""
        info = """
<h3>Data Type Information:</h3>
<p><b>float32 (Stable):</b><br/>
• Full precision, most stable<br/>
• Best compatibility with all GPUs<br/>
• Highest memory usage<br/>
• Recommended for GTX 10xx and older</p>

<p><b>float16 (Fast):</b><br/>
• Half precision, ~2x faster on modern GPUs<br/>
• Requires Tensor Cores (RTX series)<br/>
• 50% memory usage<br/>
• May have slight quality impact</p>

<p><b>bfloat16 (Experimental):</b><br/>
• Brain float format<br/>
• Better numerical stability than float16<br/>
• Limited GPU support<br/>
• Experimental support only</p>
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Data Type Information")
        msg.setTextFormat(Qt.RichText)
        msg.setText(info)
        msg.exec()
    
    def _on_dtype_changed(self):
        """Handle data type change"""
        dtype_text = self.dtype_combo.currentText()
        if "float16" in dtype_text:
            self.current_settings['dtype'] = 'float16'
        elif "bfloat16" in dtype_text:
            self.current_settings['dtype'] = 'bfloat16'
        else:
            self.current_settings['dtype'] = 'float32'
        
        if self.auto_apply:
            self._apply_settings()
    
    def _on_compilation_toggled(self, enabled):
        """Handle compilation toggle"""
        self.current_settings['compilation'] = enabled
        # Enable/disable related controls
        self.backend_combo.setEnabled(enabled)
        self.fullgraph_cb.setEnabled(enabled)
        
        if self.auto_apply:
            self._apply_settings()
    
    def get_optimization_settings(self):
        """Get current optimization settings for external use"""
        return self.current_settings.copy()
    
    def apply_external_settings(self, settings):
        """Apply settings from external source"""
        self.current_settings.update(settings)
        self._update_ui_from_settings()
        if self.auto_apply:
            self._apply_settings()
