#!/usr/bin/env python3
import os

voices_dir = "voices"
test_voice = "layla"

print(" CASE SENSITIVITY ISSUE ANALYSIS")
print("="*50)

# Test current logic
voice_lower = os.path.join(voices_dir, f"{test_voice}.wav")
voice_capital = os.path.join(voices_dir, f"{test_voice.capitalize()}.wav")

print(f" User chọn: {test_voice}")
print(f" Tìm: {voice_lower}  {' if os.path.exists(voice_lower) else '}")
print(f" Tìm: {voice_capital}  {' if os.path.exists(voice_capital) else '}")

print(f"\n Files có chứa layla:")
files = os.listdir(voices_dir) 
for f in files:
    if "layla" in f.lower():
        print(f"   - {f}")

print(f"\n FIX: Code cần thử file với tên: {test_voice.capitalize()}.wav")
