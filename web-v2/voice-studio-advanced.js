// Voice Studio Advanced Features
// Tích hợp emotion system, character mapping, inner voice từ app PC

class VoiceStudioAdvanced {
    constructor() {
        this.config = window.VOICE_STUDIO_CONFIG;
        this.currentEmotion = 'Neutral';
        this.characters = new Map();
        this.currentProject = null;
        this.analytics = {
            sessionsGenerated: 0,
            totalDuration: 0,
            voiceUsage: {}
        };
        
        this.init();
    }
    
    init() {
        this.createEmotionSystem();
        this.createCharacterMapping();
        this.createInnerVoiceControls();
        this.createAnalyticsPanel();
        this.createProjectManager();
        this.setupEventListeners();
    }
    
    // ===== EMOTION SYSTEM =====
    createEmotionSystem() {
        const emotionSection = document.createElement('div');
        emotionSection.id = 'emotion-system';
        emotionSection.className = 'mb-6';
        emotionSection.innerHTML = `
            <details class="group" open>
                <summary class="list-none flex cursor-pointer items-center group">
                    <h3 class="text-lg font-semibold text-slate-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                        🎭 Emotion Configuration
                    </h3>
                    <span class="ml-2 text-slate-500 dark:text-slate-400 group-hover:text-indigo-500 transition-colors">
                        <svg class="w-5 h-5 transform group-open:rotate-90 transition-transform" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 111.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                        </svg>
                    </span>
                </summary>
                <div class="mt-4 space-y-4">
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                        ${this.createEmotionPresets()}
                    </div>
                    <div class="emotion-controls grid grid-cols-2 md:grid-cols-4 gap-4">
                        ${this.createEmotionSliders()}
                    </div>
                    <div class="flex gap-2">
                        <button id="emotion-preview-btn" class="btn-secondary">
                            🎧 Preview Emotion
                        </button>
                        <button id="emotion-reset-btn" class="btn-secondary">
                            🔄 Reset
                        </button>
                    </div>
                </div>
            </details>
        `;
        
        // Insert after existing controls
        const existingControls = document.querySelector('.mb-6');
        existingControls.parentNode.insertBefore(emotionSection, existingControls.nextSibling);
    }
    
    createEmotionPresets() {
        return Object.keys(this.config.emotions.presets).map(emotion => 
            `<button class="emotion-preset-btn" data-emotion="${emotion}">
                ${this.getEmotionIcon(emotion)} ${emotion}
            </button>`
        ).join('');
    }
    
    createEmotionSliders() {
        return `
            <div>
                <label class="label-base text-sm">Exaggeration</label>
                <input type="range" id="emotion-exaggeration" min="0.1" max="2.0" step="0.1" value="1.0" class="slider-base">
                <span id="emotion-exaggeration-value" class="text-sm">1.0</span>
            </div>
            <div>
                <label class="label-base text-sm">CFG Weight</label>
                <input type="range" id="emotion-cfg" min="0.1" max="1.0" step="0.1" value="0.5" class="slider-base">
                <span id="emotion-cfg-value" class="text-sm">0.5</span>
            </div>
            <div>
                <label class="label-base text-sm">Temperature</label>
                <input type="range" id="emotion-temperature" min="0.1" max="1.5" step="0.1" value="0.8" class="slider-base">
                <span id="emotion-temperature-value" class="text-sm">0.8</span>
            </div>
            <div>
                <label class="label-base text-sm">Speed</label>
                <input type="range" id="emotion-speed" min="0.5" max="2.0" step="0.1" value="1.0" class="slider-base">
                <span id="emotion-speed-value" class="text-sm">1.0</span>
            </div>
        `;
    }
    
    getEmotionIcon(emotion) {
        const icons = {
            'Neutral': '😐', 'Happy': '😊', 'Sad': '😢', 'Excited': '🤩',
            'Calm': '😌', 'Angry': '😠', 'Whisper': '🤫', 'Commanding': '👑'
        };
        return icons[emotion] || '🎭';
    }
    
    // ===== CHARACTER MAPPING =====
    createCharacterMapping() {
        const characterSection = document.createElement('div');
        characterSection.id = 'character-mapping';
        characterSection.className = 'mb-6';
        characterSection.innerHTML = `
            <details class="group">
                <summary class="list-none flex cursor-pointer items-center group">
                    <h3 class="text-lg font-semibold text-slate-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                        👥 Character Mapping
                    </h3>
                    <span class="ml-2 text-slate-500 dark:text-slate-400 group-hover:text-indigo-500 transition-colors">
                        <svg class="w-5 h-5 transform group-open:rotate-90 transition-transform" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 111.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                        </svg>
                    </span>
                </summary>
                <div class="mt-4">
                    <div class="flex gap-2 mb-4">
                        <button id="add-character-btn" class="btn-primary text-sm">
                            ➕ Add Character
                        </button>
                        <button id="auto-detect-characters-btn" class="btn-secondary text-sm">
                            🔍 Auto Detect
                        </button>
                        <button id="reset-characters-btn" class="btn-secondary text-sm">
                            🔄 Reset All
                        </button>
                    </div>
                    <div class="character-table-container">
                        <table id="character-table" class="w-full text-sm">
                            <thead>
                                <tr class="border-b dark:border-slate-600">
                                    <th class="text-left p-2">Character</th>
                                    <th class="text-left p-2">Voice</th>
                                    <th class="text-left p-2">Emotion</th>
                                    <th class="text-left p-2">Speed</th>
                                    <th class="text-left p-2">Actions</th>
                                </tr>
                            </thead>
                            <tbody id="character-table-body">
                                <!-- Characters will be populated here -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </details>
        `;
        
        const emotionSection = document.getElementById('emotion-system');
        emotionSection.parentNode.insertBefore(characterSection, emotionSection.nextSibling);
    }
    
    // ===== INNER VOICE =====
    createInnerVoiceControls() {
        const innerVoiceSection = document.createElement('div');
        innerVoiceSection.id = 'inner-voice-system';
        innerVoiceSection.className = 'mb-6';
        innerVoiceSection.innerHTML = `
            <details class="group">
                <summary class="list-none flex cursor-pointer items-center group">
                    <h3 class="text-lg font-semibold text-slate-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                        🧠 Inner Voice Effects
                    </h3>
                    <span class="ml-2 text-slate-500 dark:text-slate-400 group-hover:text-indigo-500 transition-colors">
                        <svg class="w-5 h-5 transform group-open:rotate-90 transition-transform" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 111.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                        </svg>
                    </span>
                </summary>
                <div class="mt-4">
                    <div class="mb-4">
                        <label class="flex items-center cursor-pointer">
                            <input type="checkbox" id="inner-voice-enabled" class="mr-2">
                            <span class="text-sm">Enable Inner Voice Effects</span>
                        </label>
                    </div>
                    <div id="inner-voice-controls" class="hidden space-y-4">
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                            ${this.createInnerVoiceEffects()}
                        </div>
                        <div class="flex gap-2">
                            <button id="inner-voice-preview-btn" class="btn-secondary text-sm">
                                🎧 Preview Effect
                            </button>
                            <button id="inner-voice-reset-btn" class="btn-secondary text-sm">
                                🔄 Reset
                            </button>
                        </div>
                    </div>
                </div>
            </details>
        `;
        
        const characterSection = document.getElementById('character-mapping');
        characterSection.parentNode.insertBefore(innerVoiceSection, characterSection.nextSibling);
    }
    
    createInnerVoiceEffects() {
        return Object.entries(this.config.innerVoice.effects).map(([effect, params]) => 
            `<div class="inner-voice-effect p-3 border rounded-lg cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-700" data-effect="${effect}">
                <div class="font-medium">${effect}</div>
                <div class="text-xs text-slate-500 dark:text-slate-400 mt-1">
                    ${params.description}
                </div>
            </div>`
        ).join('');
    }
    
    // ===== ANALYTICS PANEL =====
    createAnalyticsPanel() {
        const analyticsSection = document.createElement('div');
        analyticsSection.id = 'analytics-panel';
        analyticsSection.className = 'mb-6';
        analyticsSection.innerHTML = `
            <details class="group">
                <summary class="list-none flex cursor-pointer items-center group">
                    <h3 class="text-lg font-semibold text-slate-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                        📊 Analytics & Statistics
                    </h3>
                    <span class="ml-2 text-slate-500 dark:text-slate-400 group-hover:text-indigo-500 transition-colors">
                        <svg class="w-5 h-5 transform group-open:rotate-90 transition-transform" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 111.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                        </svg>
                    </span>
                </summary>
                <div class="mt-4">
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                        <div class="analytics-card p-4 bg-slate-50 dark:bg-slate-700 rounded-lg">
                            <div class="text-sm text-slate-500 dark:text-slate-400">Sessions Generated</div>
                            <div class="text-2xl font-bold" id="analytics-sessions">0</div>
                        </div>
                        <div class="analytics-card p-4 bg-slate-50 dark:bg-slate-700 rounded-lg">
                            <div class="text-sm text-slate-500 dark:text-slate-400">Total Duration</div>
                            <div class="text-2xl font-bold" id="analytics-duration">0:00</div>
                        </div>
                        <div class="analytics-card p-4 bg-slate-50 dark:bg-slate-700 rounded-lg">
                            <div class="text-sm text-slate-500 dark:text-slate-400">Quality Score</div>
                            <div class="text-2xl font-bold" id="analytics-quality">-</div>
                        </div>
                    </div>
                    <div class="flex gap-2">
                        <button id="analytics-export-btn" class="btn-secondary text-sm">
                            📥 Export Data
                        </button>
                        <button id="analytics-reset-btn" class="btn-secondary text-sm">
                            🔄 Reset Stats
                        </button>
                    </div>
                </div>
            </details>
        `;
        
        const innerVoiceSection = document.getElementById('inner-voice-system');
        innerVoiceSection.parentNode.insertBefore(analyticsSection, innerVoiceSection.nextSibling);
    }
    
    // ===== PROJECT MANAGER =====
    createProjectManager() {
        const projectSection = document.createElement('div');
        projectSection.id = 'project-manager';
        projectSection.className = 'mb-6';
        projectSection.innerHTML = `
            <details class="group">
                <summary class="list-none flex cursor-pointer items-center group">
                    <h3 class="text-lg font-semibold text-slate-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                        📁 Project Manager
                    </h3>
                    <span class="ml-2 text-slate-500 dark:text-slate-400 group-hover:text-indigo-500 transition-colors">
                        <svg class="w-5 h-5 transform group-open:rotate-90 transition-transform" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 111.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                        </svg>
                    </span>
                </summary>
                <div class="mt-4">
                    <div class="flex gap-2 mb-4">
                        <button id="new-project-btn" class="btn-primary text-sm">
                            ➕ New Project
                        </button>
                        <button id="save-project-btn" class="btn-secondary text-sm">
                            💾 Save Current
                        </button>
                        <button id="load-project-btn" class="btn-secondary text-sm">
                            📂 Load Project
                        </button>
                    </div>
                    <div id="project-list" class="space-y-2">
                        <!-- Projects will be listed here -->
                    </div>
                </div>
            </details>
        `;
        
        const analyticsSection = document.getElementById('analytics-panel');
        analyticsSection.parentNode.insertBefore(projectSection, analyticsSection.nextSibling);
    }
    
    // ===== EVENT LISTENERS =====
    setupEventListeners() {
        this.setupEmotionEvents();
        this.setupCharacterEvents();
        this.setupInnerVoiceEvents();
        this.setupAnalyticsEvents();
        this.setupProjectEvents();
    }
    
    setupEmotionEvents() {
        // Emotion preset buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('emotion-preset-btn')) {
                const emotion = e.target.dataset.emotion;
                this.applyEmotionPreset(emotion);
            }
        });
        
        // Emotion sliders
        ['exaggeration', 'cfg', 'temperature', 'speed'].forEach(param => {
            const slider = document.getElementById(`emotion-${param}`);
            const value = document.getElementById(`emotion-${param}-value`);
            if (slider && value) {
                slider.addEventListener('input', (e) => {
                    value.textContent = e.target.value;
                    this.updateEmotionParams();
                });
            }
        });
        
        // Preview button
        const previewBtn = document.getElementById('emotion-preview-btn');
        if (previewBtn) {
            previewBtn.addEventListener('click', () => this.previewEmotion());
        }
    }
    
    setupCharacterEvents() {
        // Add character button
        const addBtn = document.getElementById('add-character-btn');
        if (addBtn) {
            addBtn.addEventListener('click', () => this.addCharacter());
        }
        
        // Auto detect button
        const autoBtn = document.getElementById('auto-detect-characters-btn');
        if (autoBtn) {
            autoBtn.addEventListener('click', () => this.autoDetectCharacters());
        }
    }
    
    setupInnerVoiceEvents() {
        // Enable checkbox
        const checkbox = document.getElementById('inner-voice-enabled');
        const controls = document.getElementById('inner-voice-controls');
        if (checkbox && controls) {
            checkbox.addEventListener('change', (e) => {
                controls.classList.toggle('hidden', !e.target.checked);
            });
        }
        
        // Effect selection
        document.addEventListener('click', (e) => {
            if (e.target.closest('.inner-voice-effect')) {
                const effect = e.target.closest('.inner-voice-effect').dataset.effect;
                this.selectInnerVoiceEffect(effect);
            }
        });
    }
    
    setupAnalyticsEvents() {
        // Export button
        const exportBtn = document.getElementById('analytics-export-btn');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportAnalytics());
        }
    }
    
    setupProjectEvents() {
        // New project button
        const newBtn = document.getElementById('new-project-btn');
        if (newBtn) {
            newBtn.addEventListener('click', () => this.createNewProject());
        }
        
        // Save project button
        const saveBtn = document.getElementById('save-project-btn');
        if (saveBtn) {
            saveBtn.addEventListener('click', () => this.saveCurrentProject());
        }
    }
    
    // ===== METHODS =====
    applyEmotionPreset(emotion) {
        const preset = this.config.emotions.presets[emotion];
        if (!preset) return;
        
        this.currentEmotion = emotion;
        
        // Update UI sliders
        document.getElementById('emotion-exaggeration').value = preset.exaggeration;
        document.getElementById('emotion-exaggeration-value').textContent = preset.exaggeration;
        document.getElementById('emotion-cfg').value = preset.cfg;
        document.getElementById('emotion-cfg-value').textContent = preset.cfg;
        document.getElementById('emotion-temperature').value = preset.temperature;
        document.getElementById('emotion-temperature-value').textContent = preset.temperature;
        document.getElementById('emotion-speed').value = preset.speed;
        document.getElementById('emotion-speed-value').textContent = preset.speed;
        
        // Visual feedback
        document.querySelectorAll('.emotion-preset-btn').forEach(btn => {
            btn.classList.remove('bg-indigo-600', 'text-white');
            btn.classList.add('bg-slate-200', 'dark:bg-slate-600');
        });
        
        const selectedBtn = document.querySelector(`[data-emotion="${emotion}"]`);
        if (selectedBtn) {
            selectedBtn.classList.remove('bg-slate-200', 'dark:bg-slate-600');
            selectedBtn.classList.add('bg-indigo-600', 'text-white');
        }
    }
    
    updateEmotionParams() {
        // Update parameters for next generation
        this.currentEmotionParams = {
            exaggeration: parseFloat(document.getElementById('emotion-exaggeration').value),
            cfg: parseFloat(document.getElementById('emotion-cfg').value),
            temperature: parseFloat(document.getElementById('emotion-temperature').value),
            speed: parseFloat(document.getElementById('emotion-speed').value)
        };
    }
    
    addCharacter() {
        const name = prompt('Enter character name:');
        if (name) {
            this.characters.set(name, {
                name,
                voice: 'Auto',
                emotion: 'Neutral',
                speed: 1.0
            });
            this.updateCharacterTable();
        }
    }
    
    updateCharacterTable() {
        const tbody = document.getElementById('character-table-body');
        if (!tbody) return;
        
        tbody.innerHTML = Array.from(this.characters.values()).map(char => `
            <tr>
                <td class="p-2">${char.name}</td>
                <td class="p-2">
                    <select class="select-base text-sm" onchange="voiceStudio.updateCharacterVoice('${char.name}', this.value)">
                        <option value="Auto">Auto</option>
                        ${this.config.predefinedVoices.map(voice => 
                            `<option value="${voice}" ${char.voice === voice ? 'selected' : ''}>${voice}</option>`
                        ).join('')}
                    </select>
                </td>
                <td class="p-2">
                    <select class="select-base text-sm" onchange="voiceStudio.updateCharacterEmotion('${char.name}', this.value)">
                        ${Object.keys(this.config.emotions.presets).map(emotion => 
                            `<option value="${emotion}" ${char.emotion === emotion ? 'selected' : ''}>${emotion}</option>`
                        ).join('')}
                    </select>
                </td>
                <td class="p-2">
                    <input type="range" min="0.5" max="2.0" step="0.1" value="${char.speed}" 
                           class="slider-base" onchange="voiceStudio.updateCharacterSpeed('${char.name}', this.value)">
                </td>
                <td class="p-2">
                    <button class="btn-secondary text-xs" onclick="voiceStudio.removeCharacter('${char.name}')">
                        🗑️
                    </button>
                </td>
            </tr>
        `).join('');
    }
    
    selectInnerVoiceEffect(effect) {
        // Remove previous selection
        document.querySelectorAll('.inner-voice-effect').forEach(el => {
            el.classList.remove('bg-indigo-100', 'dark:bg-indigo-900', 'border-indigo-500');
        });
        
        // Add selection to current effect
        const selectedEffect = document.querySelector(`[data-effect="${effect}"]`);
        if (selectedEffect) {
            selectedEffect.classList.add('bg-indigo-100', 'dark:bg-indigo-900', 'border-indigo-500');
        }
        
        this.currentInnerVoiceEffect = effect;
    }
    
    updateAnalytics(data) {
        this.analytics.sessionsGenerated++;
        this.analytics.totalDuration += data.duration || 0;
        
        document.getElementById('analytics-sessions').textContent = this.analytics.sessionsGenerated;
        document.getElementById('analytics-duration').textContent = this.formatDuration(this.analytics.totalDuration);
        
        // Save analytics to localStorage
        localStorage.setItem('voiceStudioAnalytics', JSON.stringify(this.analytics));
    }
    
    formatDuration(seconds) {
        const minutes = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
    
    exportAnalytics() {
        const data = {
            analytics: this.analytics,
            timestamp: new Date().toISOString(),
            version: 'Voice Studio Web v2.0'
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `voice-studio-analytics-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }
    
    // Public methods for external access
    updateCharacterVoice(name, voice) {
        if (this.characters.has(name)) {
            this.characters.get(name).voice = voice;
        }
    }
    
    updateCharacterEmotion(name, emotion) {
        if (this.characters.has(name)) {
            this.characters.get(name).emotion = emotion;
        }
    }
    
    updateCharacterSpeed(name, speed) {
        if (this.characters.has(name)) {
            this.characters.get(name).speed = parseFloat(speed);
        }
    }
    
    removeCharacter(name) {
        this.characters.delete(name);
        this.updateCharacterTable();
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.voiceStudio = new VoiceStudioAdvanced();
}); 