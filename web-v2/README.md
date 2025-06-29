# 🎙️ Voice Studio Web V2.0 - Professional TTS Platform

## 🌟 **Tổng quan**

Voice Studio Web V2.0 là phiên bản web nâng cao được tích hợp từ **Chatterbox TTS Server** và **Voice Studio Desktop App**, mang đến trải nghiệm TTS chuyên nghiệp với đầy đủ tính năng từ cả hai nền tảng.

## ✨ **Tính năng chính**

### 🎭 **Emotion System (từ Desktop App)**
- **8 emotion presets**: Neutral, Happy, Sad, Excited, Calm, Angry, Whisper, Commanding
- **Real-time adjustment**: Exaggeration, CFG Weight, Temperature, Speed
- **Emotion preview**: Test từng emotion trước khi generate
- **Reset functionality**: Quay về default settings

### 👥 **Character Mapping (từ Desktop App)**
- **Multi-character support**: Tối đa 10 nhân vật
- **Voice assignment**: Gán voice riêng cho từng nhân vật
- **Individual settings**: Emotion, speed riêng cho mỗi character
- **Auto-detection**: Tự động phát hiện nhân vật từ text

### 🧠 **Inner Voice Effects (từ Desktop App)**
- **3 effect types**: Light, Deep, Dreamy
- **Audio processing**: Lowpass filter, echo, reverb
- **Context-aware**: Phù hợp cho tư duy, nội tâm
- **Real-time preview**: Test effects ngay lập tức

### 🎤 **28 Predefined Voices (từ Chatterbox)**
- **Female voices (10)**: Abigail, Alice, Cora, Elena, Emily, Gianna, Jade, Layla, Olivia, Taylor
- **Male voices (18)**: Adrian, Alexander, Austin, Axel, Connor, Eli, Everett, Gabriel, Henry, Ian, và nhiều hơn
- **High quality**: Professional voice models
- **Voice cloning**: Upload reference audio để clone voice

### 📊 **Analytics & Statistics (từ Desktop App)**
- **Session tracking**: Theo dõi số lần generate
- **Duration monitoring**: Tổng thời lượng audio tạo ra
- **Quality metrics**: Đánh giá chất lượng voice
- **Export data**: Xuất analytics ra JSON/CSV

### 📁 **Project Management (từ Desktop App)**
- **Project creation**: Tạo và quản lý projects
- **Settings save**: Lưu cấu hình cho từng project
- **Project history**: Lịch sử các projects đã tạo
- **Auto-save**: Tự động lưu state

### 🌊 **Waveform Visualization (từ Chatterbox)**
- **WaveSurfer.js integration**: Hiển thị waveform chuyên nghiệp
- **Audio controls**: Play, pause, seek, volume
- **Visual feedback**: Real-time audio visualization
- **Export options**: Download audio với nhiều format

### 🎨 **Professional UI/UX**
- **Dark/Light theme**: Toggle theme system
- **Responsive design**: Mobile-friendly interface
- **Smooth animations**: Professional transitions
- **Status indicators**: Real-time system status

## 🚀 **Installation & Setup**

### **Prerequisites**
```bash
# Chatterbox TTS Server (Backend)
git clone https://github.com/devnen/Chatterbox-TTS-Server.git
cd Chatterbox-TTS-Server

# Install dependencies
pip install -r requirements.txt

# Start server
python server.py
```

### **Voice Studio Web V2.0**
```bash
# Copy files to web server
cp -r web-v2/* /your/web/server/path/

# Or serve locally
cd web-v2
python -m http.server 8080

# Access at http://localhost:8080
```

## ⚙️ **Configuration**

### **API Endpoints**
```javascript
// voice-studio-config.js
api: {
    baseUrl: 'http://localhost:8005', // Chatterbox backend
    voiceStudio: 'http://localhost:8000', // Voice Studio backend
    endpoints: {
        speech: '/v1/audio/speech',
        voices: '/v1/voices',
        emotions: '/api/emotions',
        characters: '/api/characters'
    }
}
```

### **Feature Flags**
```javascript
features: {
    emotionSystem: true,        // Enable emotion configuration
    characterMapping: true,     // Enable character mapping
    innerVoiceEffects: true,    // Enable inner voice effects
    analytics: true,            // Enable analytics tracking
    projectManagement: true     // Enable project management
}
```

## 🎯 **Usage Guide**

### **1. Basic Voice Generation**
1. Enter text trong textarea
2. Select voice từ dropdown (28 predefined voices)
3. Click "Generate Speech" button
4. Audio sẽ play tự động với waveform visualization

### **2. Emotion Configuration**
1. Mở "🎭 Emotion Configuration" section
2. Click emotion preset button (Happy, Sad, Excited, etc.)
3. Fine-tune với sliders (Exaggeration, CFG, Temperature, Speed)
4. Click "🎧 Preview Emotion" để test
5. Generate với emotion đã chọn

### **3. Character Mapping**
1. Mở "👥 Character Mapping" section
2. Click "➕ Add Character" để thêm nhân vật
3. Hoặc "🔍 Auto Detect" để tự động phát hiện
4. Assign voice và emotion cho từng character
5. Generate multi-character conversations

### **4. Inner Voice Effects**
1. Mở "🧠 Inner Voice Effects" section
2. Enable checkbox "Enable Inner Voice Effects"
3. Select effect: Light, Deep, hoặc Dreamy
4. Click "🎧 Preview Effect" để test
5. Generate với inner voice effect

### **5. Analytics Tracking**
1. Mở "📊 Analytics & Statistics" section
2. Xem real-time metrics: Sessions, Duration, Quality
3. Click "📥 Export Data" để xuất analytics
4. Track usage patterns và performance

### **6. Project Management**
1. Mở "📁 Project Manager" section
2. Click "➕ New Project" để tạo project mới
3. "💾 Save Current" để lưu settings hiện tại
4. "📂 Load Project" để load project đã lưu

## 🔧 **Advanced Features**

### **Voice Cloning**
```javascript
// Upload reference audio
const formData = new FormData();
formData.append('audio', audioFile);
await fetch('/v1/clone', { method: 'POST', body: formData });
```

### **Batch Processing**
```javascript
// Process multiple texts
const texts = ['Text 1', 'Text 2', 'Text 3'];
const results = await Promise.all(
    texts.map(text => generateVoice(text, emotionConfig))
);
```

### **Custom Presets**
```javascript
// Create custom emotion preset
const customEmotion = {
    name: 'Mysterious',
    exaggeration: 0.8,
    cfg: 0.3,
    temperature: 0.6,
    speed: 0.9
};
```

## 📱 **Mobile Support**

Voice Studio Web V2.0 hoàn toàn responsive và hoạt động tốt trên mobile:
- **Touch-friendly**: Optimized cho touch interface
- **Responsive grids**: Auto-adjust layout
- **Mobile audio**: Native mobile audio support
- **Gesture support**: Swipe, pinch, tap gestures

## 🎨 **Theming**

### **Dark Mode**
- Auto-detect system preference
- Manual toggle button
- Persistent theme selection
- Smooth transitions

### **Custom Styling**
```css
/* Override default colors */
:root {
    --primary-color: #your-brand-color;
    --secondary-color: #your-accent-color;
}
```

## 🔒 **Security**

- **CORS configured**: Safe cross-origin requests
- **Input validation**: Prevent XSS attacks
- **File upload limits**: Secure file handling
- **API rate limiting**: Prevent abuse

## 🚀 **Performance**

- **Lazy loading**: Load components on demand
- **Caching**: Cache frequently used data
- **Compression**: Optimized assets
- **CDN ready**: Static assets optimization

## 🤝 **Contributing**

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 **License**

MIT License - Free for personal and commercial use

## 🙏 **Credits**

- **Chatterbox TTS**: Core TTS engine by Resemble AI
- **Voice Studio Desktop**: Advanced features integration
- **WaveSurfer.js**: Audio visualization
- **Tailwind CSS**: UI framework

## 📞 **Support**

- **Documentation**: Full API documentation available
- **Issues**: Report bugs via GitHub Issues
- **Discord**: Join community for support
- **Email**: Professional support available

---

## 🎉 **What's New in V2.0**

### ✅ **From Desktop App Integration**
- ✅ Complete emotion system với 8 presets
- ✅ Character mapping với voice assignment
- ✅ Inner voice effects (Light/Deep/Dreamy)
- ✅ Analytics & statistics tracking
- ✅ Project management system

### ✅ **From Chatterbox Integration**
- ✅ 28 predefined voices (female + male)
- ✅ Voice cloning capabilities
- ✅ Professional waveform visualization
- ✅ Dark/Light theme system
- ✅ File upload & management

### ✅ **New Web-Specific Features**
- ✅ Mobile-responsive design
- ✅ Touch-friendly interface
- ✅ Progressive Web App ready
- ✅ Offline functionality
- ✅ Real-time collaboration ready

---

**Voice Studio Web V2.0** - Bringing desktop-grade TTS capabilities to the web! 🚀 