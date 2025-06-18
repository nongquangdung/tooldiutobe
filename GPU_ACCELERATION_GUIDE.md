# 🚀 GPU Acceleration Guide for ChatterboxTTS

## 🎯 Vấn đề hiện tại

✅ **GPU có sẵn:** NVIDIA GeForce GTX 1080 (8GB VRAM)  
❌ **PyTorch:** CPU-only version (2.6.0+cpu)  
❌ **ChatterboxTTS:** Chạy trên CPU thay vì GPU  

**Kết quả:** TTS generation chậm hơn 3-10x so với GPU!

## 🚀 Giải pháp nhanh (5 phút)

### Phương án A: Tự động (Khuyến nghị)

```bash
# Chạy script tự động
./install_pytorch_cuda.bat
```

### Phương án B: Thủ công

```bash
# 1. Gỡ PyTorch CPU-only
pip uninstall torch torchvision torchaudio -y

# 2. Cài PyTorch CUDA 11.8 (tương thích tốt)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 3. Kiểm tra
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

## ⚡ Hiệu quả mong đợi

| Metric | CPU (Hiện tại) | GPU (Sau cài) | Cải thiện |
|--------|----------------|---------------|-----------|
| Generation Speed | ~4.5it/s | ~15-30it/s | **3-7x nhanh hơn** |
| Memory Usage | RAM | VRAM | Giải phóng RAM |
| Quality | ✅ | ✅ | Không đổi |
| Voice Cloning | ✅ Chậm | ✅ Nhanh | **5-10x nhanh hơn** |

## 🧪 Test sau cài đặt

```python
# Test GPU detection
python test_cuda_detection.py

# Test voice generation
python test_voice_modes.py
```

**Expected output:**
```
🎯 Real Chatterbox detected device: GPU (NVIDIA GeForce GTX 1080) - Real Chatterbox
   🚀 GPU Memory: 8GB
   ⚡ CUDA Version: 11.8
```

## 🔧 Voice Mode Logic (Đã sửa)

### 1. **Voice Selection Mode** 🗣️
- Sử dụng giọng có sẵn từ ChatterboxTTS
- Parameters: emotion, speed, cfg_weight
- **Fastest generation**

### 2. **Voice Clone Mode** 🎤  
- Clone giọng từ reference audio (3-30s)
- Upload file .wav/.mp3
- **High quality, personalized**

### 3. **~~Voice Prompt Mode~~** ❌
- **Đã loại bỏ** - ChatterboxTTS không hỗ trợ text prompt
- Previous implementation không hoạt động đúng

## 📊 UI Changes Summary

| Component | Before | After |
|-----------|--------|-------|
| Mode Selector | 3 options | 2 options (Voice + Clone) |
| Voice Prompt | Input field | **Removed** |
| Quick Actions | Prompt examples | Voice optimization |
| Status Display | 3 modes | 2 modes |
| Priority Logic | Prompt > Clone > Voice | **Clone > Voice** |

## 🎮 Recommended Workflow

1. **Install GPU PyTorch** (one time)
2. **Choose Voice Mode:**
   - 🗣️ **Voice Selection** for quick generation
   - 🎤 **Voice Clone** for personalized voices
3. **Optimize parameters** using Quick Actions
4. **Generate** with GPU acceleration!

## 🛠️ Troubleshooting

### CUDA Not Available After Install
```bash
# Check installation
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"

# If still CPU-only, try CUDA 12.1
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### GPU Memory Issues
- Close other GPU applications
- Use smaller batch sizes
- Consider voice cloning with shorter reference audio

### Still Using CPU
- Restart application after PyTorch installation
- Check `device_name` in logs should show "GPU (NVIDIA...)"
- Verify no CUDA errors in console

## 📈 Performance Monitoring

```python
# Monitor GPU usage during generation
import torch
print(f"GPU Memory: {torch.cuda.memory_allocated(0) / 1024**2:.1f}MB")
print(f"GPU Utilization: {torch.cuda.utilization(0)}%")
```

## 🎉 Expected Results

**Before (CPU):**
```
💻 Real Chatterbox detected device: CPU - Real Chatterbox
Sampling: 20%|████████| 203/1000 [00:45<02:59, 4.44it/s]
```

**After (GPU):**
```
🎯 Real Chatterbox detected device: GPU (NVIDIA GeForce GTX 1080) - Real Chatterbox
Sampling: 20%|████████| 203/1000 [00:12<00:45, 17.8it/s]
```

**Improvement: ~4x faster generation! 🚀** 