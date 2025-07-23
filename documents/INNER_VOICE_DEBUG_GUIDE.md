# 🎭 INNER VOICE DEBUG GUIDE

## Vấn đề cần debug:

### 1. **Auto-save không thực sự lưu vào file JSON**
- Console show "💾 Saved" nhưng file không thay đổi
- Real-time changes không persist

### 2. **Reset chỉ về hard-coded defaults**
- Thay vì reset về user's original values
- Không linh hoạt theo config file

---

## 🔧 Đã thực hiện những gì:

### 1. **Enhanced save_inner_voice_config_to_file():**
```python
# Thêm debug logging chi tiết
print(f"🔍 DEBUGGING SAVE: Starting save to {config_path}")
print(f"📊 {type_name}: delay={current_values['delay']}, filter='{current_values['filter']}'")

# File verification sau khi save
with open(config_path, 'r', encoding='utf-8') as f:
    verify_config = json.load(f)
if "inner_voice_config" in verify_config:
    print(f"✅ SAVE VERIFIED: File updated successfully")
```

### 2. **Original Values System:**
```python
# Store original values for reset
self.inner_voice_original_values = {}

# Load và lưu original values từ file
self.inner_voice_original_values[type_name] = {
    "delay": preset.get("delay", 500),
    "decay": preset.get("decay", 0.3),
    "gain": preset.get("gain", 0.5),
    "filter": preset.get("filter", "aecho=0.6:0.5:500:0.3")
}
```

### 3. **Smart Reset Logic:**
```python
def reset_inner_voice_type(self, type_name: str):
    # Reset về ORIGINAL values thay vì hard-coded
    if type_name in self.inner_voice_original_values:
        original_vals = self.inner_voice_original_values[type_name]
        # Reset về user's saved values
```

---

## 🧪 Cách test debug:

### **Step 1: Mở Voice Studio**
```bash
python src/main.py
```

### **Step 2: Mở tab "🎭 Cấu hình Cảm xúc"**
- Tìm group "Inner Voice (Thoại nội tâm)"
- ✅ Bật checkbox

### **Step 3: Test Auto-Save**
1. Thay đổi delay light từ 50 → 999
2. **Kiểm tra console** - sẽ thấy debug messages:
   ```
   🔍 DEBUGGING SAVE: Starting save to configs/emotions/unified_emotions.json
   🎭 Inner Voice enabled: True
   📊 light: delay=999.0, decay=0.3, gain=0.5, filter='aecho=0.6:0.5:500:0.3'
   ✅ SAVE VERIFIED: File updated successfully
   ```

3. **Kiểm tra file JSON** - mở `configs/emotions/unified_emotions.json`:
   ```json
   "inner_voice_config": {
     "presets": {
       "light": {
         "delay": 999.0,  // ← Should change to 999
         "filter": "aecho=0.6:0.5:500:0.3"
       }
     }
   }
   ```

### **Step 4: Test Reset to Original**
1. Thay đổi light delay về 50, deep delay về 150 (như hiện tại)
2. Đặt light delay = 888 (test value)
3. Click nút "↻ Reset" của light
4. **Expected:** Light delay reset về 50 (original), KHÔNG phải 500 (hard-coded)

### **Step 5: Debug Console Output**
Nếu auto-save không work, sẽ thấy:
```
❌ SAVE FAILED: Missing inner_voice_group or inner_voice_type_widgets
❌ FILE WRITE ERROR: [具体错误]
❌ CRITICAL SAVE ERROR: [具体错误]
```

---

## 🔍 Potential Issues:

### 1. **Signals not connected properly**
```python
# Check in connect_inner_voice_signals()
widgets["delay"].valueChanged.connect(lambda v, t=type_name: self.on_inner_voice_param_changed(t))
```

### 2. **File permissions**
- Windows có thể block write vào configs/emotions/
- Thử chạy as Administrator

### 3. **Timing issues**
```python
# blockSignals() có thể block auto-save
widgets["delay"].blockSignals(True)  # ← During reset
# Auto-save chỉ trigger khi unblock
```

### 4. **Lambda closure bug**
```python
# Lambda có thể capture wrong type_name
lambda v, t=type_name: self.on_inner_voice_param_changed(t)
#          ↑ Ensure proper closure
```

---

## 💡 Quick Fix Test:

### Test manual trigger save:
1. Thay đổi inner voice values
2. Mở Python Console trong app (nếu có) hoặc add button:
   ```python
   self.save_inner_voice_config_to_file()  # Manual trigger
   ```

### Test file write permissions:
```python
# Tạo test file
with open("configs/emotions/test_write.json", 'w') as f:
    f.write('{"test": true}')
# Nếu fail = permission issue
```

---

## 📋 Expected Console Output (Success):
```
📥 Loaded light: delay=50.0, filter='aecho=0.6:0.5:500:0.3'
📥 Loaded deep: delay=150.0, filter='aecho=0.8:0.6:800:0.6,lowpass=f=3000'
📥 Loaded dreamy: delay=300.0, filter='aecho=0.9:0.8:1200:0.8,chorus=0.5:0.9:50:0.4:0.25:2'
✅ Loaded inner voice config from configs/emotions/unified_emotions.json
🔗 Connected inner voice signals for auto-save

[User changes delay to 888]
🔍 DEBUGGING SAVE: Starting save to configs/emotions/unified_emotions.json
✅ Successfully read existing config file
🎭 Inner Voice enabled: True
📊 light: delay=888.0, decay=0.3, gain=0.5, filter='aecho=0.6:0.5:500:0.3'
✅ SAVE VERIFIED: File updated successfully
   📝 Saved light: delay=888.0, filter='aecho=0.6:0.5:500:0.3'
💾 SAVE COMPLETED: configs/emotions/unified_emotions.json

[User clicks Reset light]
🔄 RESETTING light to ORIGINAL values:
   delay: 50.0
   decay: 0.3
   gain: 0.5
   filter: 'aecho=0.6:0.5:500:0.3'
✅ Reset completed for light
```

---

**🎯 Mục tiêu:** Auto-save hoạt động real-time và reset về user's original values thay vì hard-coded defaults. 