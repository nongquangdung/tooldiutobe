// Voice Studio Web V2.0 Configuration
// Tích hợp features từ app PC và Chatterbox backend

const VOICE_STUDIO_CONFIG = {
    api: {
        baseUrl: 'http://localhost:8005', // Chatterbox backend
        voiceStudio: 'http://localhost:8000', // Voice Studio backend
        endpoints: {
            // Chatterbox endpoints
            speech: '/v1/audio/speech',
            voices: '/v1/voices',
            clone: '/v1/clone',
            
            // Voice Studio endpoints
            emotions: '/api/emotions',
            characters: '/api/characters',
            analytics: '/api/analytics',
            projects: '/api/projects',
            innerVoice: '/api/inner-voice'
        }
    },
    
    features: {
        // Từ app PC
        emotionSystem: true,
        characterMapping: true,
        innerVoiceEffects: true,
        voiceCloning: true,
        analytics: true,
        projectManagement: true,
        
        // Từ Chatterbox
        predefinedVoices: true,
        waveformVisualization: true,
        presetSystem: true,
        themeSwitch: true
    },
    
    // Emotion configuration từ app PC
    emotions: {
        categories: ['Narrative', 'Dialogue', 'Descriptive', 'Action', 'Emotional'],
        presets: {
            'Neutral': { exaggeration: 1.0, cfg: 0.5, temperature: 0.8, speed: 1.0 },
            'Happy': { exaggeration: 1.2, cfg: 0.6, temperature: 0.9, speed: 1.1 },
            'Sad': { exaggeration: 0.8, cfg: 0.4, temperature: 0.7, speed: 0.9 },
            'Excited': { exaggeration: 1.5, cfg: 0.7, temperature: 1.0, speed: 1.2 },
            'Calm': { exaggeration: 0.7, cfg: 0.3, temperature: 0.6, speed: 0.8 },
            'Angry': { exaggeration: 1.4, cfg: 0.8, temperature: 1.1, speed: 1.3 },
            'Whisper': { exaggeration: 0.5, cfg: 0.2, temperature: 0.5, speed: 0.7 },
            'Commanding': { exaggeration: 1.3, cfg: 0.9, temperature: 0.8, speed: 1.0 }
        }
    },
    
    // Inner voice effects từ app PC
    innerVoice: {
        effects: {
            'Light': { 
                lowpass: 8000, 
                echo: 0.3, 
                reverb: 0.2,
                description: 'Nhẹ nhàng, tư duy bình thường'
            },
            'Deep': { 
                lowpass: 4000, 
                echo: 0.6, 
                reverb: 0.4,
                description: 'Sâu sắc, tư duy sâu'
            },
            'Dreamy': { 
                lowpass: 6000, 
                echo: 0.8, 
                reverb: 0.6,
                description: 'Mơ màng, tư duy mơ mộng'
            }
        }
    },
    
    // Predefined voices từ Chatterbox (28 voices)
    predefinedVoices: [
        // Female voices
        'Abigail', 'Alice', 'Cora', 'Elena', 'Emily', 'Gianna', 'Jade', 'Layla', 'Olivia', 'Taylor',
        // Male voices
        'Adrian', 'Alexander', 'Austin', 'Axel', 'Connor', 'Eli', 'Everett', 'Gabriel', 'Henry', 'Ian',
        'Jeremiah', 'Jordan', 'Julian', 'Leonardo', 'Michael', 'Miles', 'Ryan', 'Thomas'
    ],
    
    // Character mapping system từ app PC
    characterMapping: {
        maxCharacters: 10,
        defaultSettings: {
            emotion: 'Neutral',
            voice: 'Auto',
            speed: 1.0,
            exaggeration: 1.0,
            cfg_weight: 0.5
        }
    },
    
    // Analytics system từ app PC
    analytics: {
        trackUsage: true,
        metrics: ['generation_time', 'voice_quality', 'user_satisfaction'],
        exportFormats: ['json', 'csv']
    },
    
    ui: {
        theme: 'dark', // default theme
        language: 'vi', // Vietnamese
        features: {
            emotionTable: true,
            characterTable: true,
            voicePreview: true,
            waveformDisplay: true,
            projectManager: true,
            analyticsPanel: true
        }
    }
};

// Export config
window.VOICE_STUDIO_CONFIG = VOICE_STUDIO_CONFIG; 