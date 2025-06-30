import React, { useState, useRef, useEffect } from 'react';
import styles from '../styles/VoiceStudioV2.module.css';

// Icons components
const PlusIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="12" y1="5" x2="12" y2="19"></line>
    <line x1="5" y1="12" x2="19" y2="12"></line>
  </svg>
);

const PlayIcon = () => (
  <svg viewBox="0 0 24 24">
    <path d="M8 5v14l11-7z"/>
  </svg>
);

const PauseIcon = () => (
  <svg viewBox="0 0 24 24">
    <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
  </svg>
);

const SettingsIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="3"></circle>
    <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
  </svg>
);

const UploadIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
    <polyline points="17,8 12,3 7,8"></polyline>
    <line x1="12" y1="3" x2="12" y2="15"></line>
  </svg>
);

const SunIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="5"></circle>
    <line x1="12" y1="1" x2="12" y2="3"></line>
    <line x1="12" y1="21" x2="12" y2="23"></line>
    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
    <line x1="1" y1="12" x2="3" y2="12"></line>
    <line x1="21" y1="12" x2="23" y2="12"></line>
    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
  </svg>
);

const MoonIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
  </svg>
);

const DownloadIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
    <polyline points="7,10 12,15 17,10"></polyline>
    <line x1="12" y1="15" x2="12" y2="3"></line>
  </svg>
);

const ShareIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="18" cy="5" r="3"></circle>
    <circle cx="6" cy="12" r="3"></circle>
    <circle cx="18" cy="19" r="3"></circle>
    <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
    <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
  </svg>
);

const CloseIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="18" y1="6" x2="6" y2="18"></line>
    <line x1="6" y1="6" x2="18" y2="18"></line>
  </svg>
);

const TrashIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="3,6 5,6 21,6"></polyline>
    <path d="M19,6v14a2,2 0,0,1-2,2H7a2,2 0,0,1-2-2V6m3,0V4a2,2 0,0,1,2-2h4a2,2 0,0,1,2,2v2"></path>
  </svg>
);

const MagicIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path>
  </svg>
);

// Enhanced Interfaces for ChatterboxTTS integration
interface Dialogue {
  speaker: string;
  text: string;
  emotion: string;
  inner_voice?: boolean;
  inner_voice_type?: 'light' | 'deep' | 'dreamy';
}

interface Segment {
  id: number;
  dialogues: Dialogue[];
}

interface Character {
  id: string;
  name: string;
  gender: 'male' | 'female' | 'neutral';
  voice?: string; // ChatterboxTTS voice assignment
}

interface ProjectData {
  segments: Segment[];
  characters: Character[];
}

// ChatterboxTTS Available Voices (from the app)
const CHATTERBOX_VOICES = [
  'Aaron', 'Abigail', 'Adrian', 'Alexander', 'Alice', 'Aria', 'Austin',
  'Bella', 'Brian', 'Caroline', 'Connor', 'David', 'Emily', 'Emma',
  'Grace', 'Henry', 'James', 'Jordan', 'Kate', 'Kevin', 'Liam',
  'Madison', 'Michael', 'Natalie', 'Oliver', 'Rachel', 'Ryan', 'Sophia'
];

// Available Emotions (93 emotions from the app)
const EMOTIONS = [
  'admiration', 'adoration', 'aesthetic_appreciation', 'amusement', 'anger', 'anxiety',
  'awe', 'awkwardness', 'boredom', 'calmness', 'concentration', 'confusion',
  'contemplation', 'contempt', 'contentment', 'craving', 'curiosity', 'desire',
  'determination', 'disappointment', 'disgust', 'distress', 'doubt', 'ecstasy',
  'embarrassment', 'empathic_pain', 'enthusiasm', 'entrancement', 'envy', 'excitement',
  'fear', 'guilt', 'happiness', 'horror', 'interest', 'joy', 'love',
  'nostalgia', 'pain', 'pride', 'realization', 'relief', 'romance', 'sadness',
  'satisfaction', 'serenity', 'shame', 'surprise', 'sympathy', 'triumph',
  // Extended emotions
  'dramatic', 'melancholic', 'serious', 'determined', 'frustrated', 'pleading',
  'gentle', 'soft', 'commanding', 'mysterious', 'playful', 'tender',
  'sorrowful', 'hopeful', 'confident', 'nervous', 'excited', 'calm',
  'angry', 'peaceful', 'worried', 'cheerful', 'thoughtful', 'passionate',
  'humble', 'proud', 'lonely', 'grateful', 'suspicious', 'innocent',
  'wise', 'childlike', 'mature', 'energetic', 'tired', 'refreshed',
  'overwhelmed', 'focused', 'distracted', 'alert', 'sleepy', 'awake',
  'neutral'
];

const VoiceStudioV2: React.FC = () => {
  const [textInput, setTextInput] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isDarkTheme, setIsDarkTheme] = useState(false);
  const [isVoiceConfigOpen, setIsVoiceConfigOpen] = useState(false);
  const [progress, setProgress] = useState(30);
  
  // Enhanced project data for ChatterboxTTS
  const [projectData, setProjectData] = useState<ProjectData>({
    segments: [
      {
        id: 1,
        dialogues: [
          {
            speaker: 'narrator',
            text: '',
            emotion: 'neutral'
          }
        ]
      }
    ],
    characters: [
      {
        id: 'narrator',
        name: 'Narrator',
        gender: 'neutral',
        voice: 'Alice' // Default ChatterboxTTS voice
      }
    ]
  });
  
  // Voice settings with ChatterboxTTS parameters
  const [voiceSettings, setVoiceSettings] = useState({
    temperature: 0.7,
    cfg: 2.5,
    exaggeration: 1.0,
    speed: 1.0,
    singleEmotion: 'neutral', // For single speaker mode
    autoAssignVoices: true, // AI auto-assign voices based on gender/name
  });

  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isDarkTheme) {
      document.body.classList.add('dark-theme');
    } else {
      document.body.classList.remove('dark-theme');
    }
  }, [isDarkTheme]);

  const autoResizeTextarea = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  };

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setTextInput(e.target.value);
    // Update single dialogue text
    if (projectData.segments.length === 1 && projectData.segments[0].dialogues.length === 1) {
      setProjectData(prev => ({
        ...prev,
        segments: [{
          ...prev.segments[0],
          dialogues: [{
            ...prev.segments[0].dialogues[0],
            text: e.target.value
          }]
        }]
      }));
    }
    autoResizeTextarea();
  };

  // Auto-assign ChatterboxTTS voices based on gender and name
  const autoAssignVoice = (character: Character): string => {
    const maleVoices = CHATTERBOX_VOICES.filter(voice => 
      ['Aaron', 'Adrian', 'Alexander', 'Austin', 'Brian', 'Connor', 'David', 'Henry', 'James', 'Jordan', 'Kevin', 'Liam', 'Michael', 'Oliver', 'Ryan'].includes(voice)
    );
    const femaleVoices = CHATTERBOX_VOICES.filter(voice => 
      ['Abigail', 'Alice', 'Aria', 'Bella', 'Caroline', 'Emily', 'Emma', 'Grace', 'Kate', 'Madison', 'Natalie', 'Rachel', 'Sophia'].includes(voice)
    );
    
    if (character.gender === 'male') {
      return maleVoices[Math.floor(Math.random() * maleVoices.length)];
    } else if (character.gender === 'female') {
      return femaleVoices[Math.floor(Math.random() * femaleVoices.length)];
    } else {
      return CHATTERBOX_VOICES[Math.floor(Math.random() * CHATTERBOX_VOICES.length)];
    }
  };

  const handleJsonUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'application/json') {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const jsonData: ProjectData = JSON.parse(e.target?.result as string);
          
          // Auto-assign voices if enabled
          if (voiceSettings.autoAssignVoices) {
            jsonData.characters = jsonData.characters.map(char => ({
              ...char,
              voice: char.voice || autoAssignVoice(char)
            }));
          }
          
          setProjectData(jsonData);
          setTextInput(''); // Clear single text input when loading multi-character
        } catch (error) {
          alert('File JSON không hợp lệ! Vui lòng kiểm tra định dạng.');
        }
      };
      reader.readAsText(file);
    }
  };

  const addSegment = () => {
    const newSegment: Segment = {
      id: Math.max(...projectData.segments.map(s => s.id)) + 1,
      dialogues: [
        {
          speaker: projectData.characters[0]?.id || 'narrator',
          text: '',
          emotion: 'neutral'
        }
      ]
    };
    setProjectData(prev => ({
      ...prev,
      segments: [...prev.segments, newSegment]
    }));
  };

  const addDialogue = (segmentId: number) => {
    const newDialogue: Dialogue = {
      speaker: projectData.characters[0]?.id || 'narrator',
      text: '',
      emotion: 'neutral'
    };
    
    setProjectData(prev => ({
      ...prev,
      segments: prev.segments.map(segment =>
        segment.id === segmentId
          ? { ...segment, dialogues: [...segment.dialogues, newDialogue] }
          : segment
      )
    }));
  };

  const updateDialogue = (segmentId: number, dialogueIndex: number, field: keyof Dialogue, value: string | boolean) => {
    setProjectData(prev => ({
      ...prev,
      segments: prev.segments.map(segment =>
        segment.id === segmentId
          ? {
              ...segment,
              dialogues: segment.dialogues.map((dialogue, index) =>
                index === dialogueIndex ? { ...dialogue, [field]: value } : dialogue
              )
            }
          : segment
      )
    }));
  };

  const deleteDialogue = (segmentId: number, dialogueIndex: number) => {
    setProjectData(prev => ({
      ...prev,
      segments: prev.segments.map(segment =>
        segment.id === segmentId && segment.dialogues.length > 1
          ? {
              ...segment,
              dialogues: segment.dialogues.filter((_, index) => index !== dialogueIndex)
            }
          : segment
      )
    }));
  };

  const deleteSegment = (segmentId: number) => {
    if (projectData.segments.length > 1) {
      setProjectData(prev => ({
        ...prev,
        segments: prev.segments.filter(segment => segment.id !== segmentId)
      }));
    }
  };

  const addCharacter = () => {
    const newCharacter: Character = {
      id: `character${projectData.characters.length + 1}`,
      name: `Character ${projectData.characters.length + 1}`,
      gender: 'neutral',
      voice: voiceSettings.autoAssignVoices ? autoAssignVoice({ 
        id: '', name: '', gender: 'neutral' 
      }) : 'Alice'
    };
    setProjectData(prev => ({
      ...prev,
      characters: [...prev.characters, newCharacter]
    }));
  };

  const updateCharacter = (characterId: string, field: keyof Character, value: string) => {
    setProjectData(prev => ({
      ...prev,
      characters: prev.characters.map(character =>
        character.id === characterId 
          ? { 
              ...character, 
              [field]: value,
              // Auto-assign voice when gender changes
              ...(field === 'gender' && voiceSettings.autoAssignVoices ? {
                voice: autoAssignVoice({ ...character, gender: value as 'male' | 'female' | 'neutral' })
              } : {})
            } 
          : character
      )
    }));
  };

  const handleGenerate = async () => {
    const hasText = projectData.segments.some(segment => 
      segment.dialogues.some(dialogue => dialogue.text.trim())
    );
    
    if (!hasText) {
      alert('Vui lòng nhập nội dung để tạo giọng nói');
      return;
    }

    setIsGenerating(true);
    
    try {
      // Simulate ChatterboxTTS API call
      console.log('Generating audio with ChatterboxTTS:', {
        projectData,
        voiceSettings
      });
      
      // Here would be the actual API call to ChatterboxTTS
      await new Promise(resolve => setTimeout(resolve, 2000));
      
    } catch (error) {
      alert('Tạo thất bại: ' + (error as Error).message);
    } finally {
      setIsGenerating(false);
    }
  };

  const togglePlay = () => {
    setIsPlaying(!isPlaying);
  };

  const handleSeek = (event: React.MouseEvent<HTMLDivElement>) => {
    const rect = event.currentTarget.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const percent = x / rect.width;
    setProgress(percent * 100);
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const recentProjects = [
    { name: 'Drama Romance', duration: '8:42', active: true },
    { name: 'Podcast tập 1', duration: '5:18', active: false },
    { name: 'Audiobook Chapter 1', duration: '12:05', active: false }
  ];

  const features = [
    { name: 'ChatterboxTTS Engine', isPro: false },
    { name: '93 Emotions', isPro: false },
    { name: 'Voice Cloning', isPro: true },
    { name: 'Batch Export', isPro: true }
  ];

  const isMultiCharacter = projectData.characters.length > 1 || 
    projectData.segments.some(segment => segment.dialogues.length > 1) ||
    projectData.segments.length > 1;

  const totalDialogues = projectData.segments.reduce((total, segment) => 
    total + segment.dialogues.length, 0
  );

  return (
    <div className={styles.appContainer}>
      {/* Theme Toggle */}
      <div className={styles.themeToggle} onClick={() => setIsDarkTheme(!isDarkTheme)}>
        {isDarkTheme ? <MoonIcon /> : <SunIcon />}
      </div>

      {/* Hidden file input for JSON upload */}
      <input
        type="file"
        ref={fileInputRef}
        accept=".json"
        style={{ display: 'none' }}
        onChange={handleJsonUpload}
      />

      {/* Sidebar */}
      <div className={styles.sidebar}>
        <div className={styles.sidebarHeader}>
          <div className={styles.logo}>VOICE STUDIO</div>
          <button className={styles.newSessionBtn}>
            <PlusIcon />
            Tạo mới
          </button>
        </div>

        {/* Recent Projects */}
        <div className={styles.menuSection}>
          <div className={styles.menuTitle}>Dự án gần đây</div>
          {recentProjects.map((project, index) => (
            <div key={index} className={`${styles.menuItem} ${project.active ? styles.active : ''}`}>
              <span>{project.name}</span>
              <span>{project.duration}</span>
            </div>
          ))}
        </div>

        {/* Features */}
        <div className={styles.menuSection}>
          <div className={styles.menuTitle}>Tính năng</div>
          {features.map((feature, index) => (
            <div key={index} className={feature.isPro ? styles.menuItemPro : styles.menuItem}>
              <span>{feature.name}</span>
              {feature.isPro && <span className={styles.proBadge}>PRO</span>}
            </div>
          ))}
        </div>

        {/* Upgrade Section */}
        <div className={styles.upgradeSection}>
          <div className={styles.upgradeTitle}>Nâng cấp lên Pro</div>
          <div className={styles.upgradeDesc}>Voice cloning & batch export</div>
          <button className={styles.upgradeBtn}>Nâng cấp ngay</button>
        </div>

        <div className={styles.sidebarFooter}>
          <div className={styles.userProfile}>
            <div className={styles.userAvatar}>U</div>
            <div>
              <div style={{ fontSize: '14px', fontWeight: 500, color: 'var(--sidebar-text)' }}>User</div>
              <div style={{ fontSize: '12px', color: 'var(--sidebar-text)', opacity: 0.7 }}>ChatterboxTTS</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className={styles.mainContent}>
        <div className={styles.contentArea}>
          <div className={styles.voiceStudioGrid}>
            {/* Text Input - Dynamic based on complexity */}
            {!isMultiCharacter ? (
              /* Single Character Mode */
              <div className={styles.textInputContainer}>
                <textarea
                  ref={textareaRef}
                  className={styles.textInput}
                  placeholder="Nhập nội dung văn bản..."
                  value={textInput}
                  onChange={handleTextChange}
                  rows={1}
                />
                <div className={styles.inputFooter}>
                  <div className={styles.charCounter}>
                    <span>{textInput.length}</span> ký tự
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <div 
                      className={styles.toolsBtn} 
                      onClick={() => fileInputRef.current?.click()}
                      title="Upload JSON Script"
                    >
                      <UploadIcon />
                    </div>
                    <div 
                      className={styles.toolsBtn} 
                      onClick={() => setIsVoiceConfigOpen(!isVoiceConfigOpen)}
                    >
                      <SettingsIcon />
                    </div>
                    <button className={styles.generateBtn} onClick={handleGenerate}>
                      <PlayIcon />
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              /* Multi Character Mode */
              <div className={styles.multiCharacterContainer}>
                {/* Characters Section */}
                <div className={styles.characterSection}>
                  <div className={styles.sectionHeader}>
                    <h3>Nhân vật ({projectData.characters.length})</h3>
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <button 
                        className={styles.autoBtn}
                        onClick={() => setVoiceSettings({...voiceSettings, autoAssignVoices: !voiceSettings.autoAssignVoices})}
                        title="Auto-assign voices"
                      >
                        <MagicIcon /> {voiceSettings.autoAssignVoices ? 'Auto ON' : 'Auto OFF'}
                      </button>
                      <button className={styles.addBtn} onClick={addCharacter}>
                        <PlusIcon /> Thêm nhân vật
                      </button>
                    </div>
                  </div>
                  {projectData.characters.map((character) => (
                    <div key={character.id} className={styles.characterCard}>
                      <div className={styles.characterHeader}>
                        <input
                          className={styles.characterName}
                          value={character.name}
                          onChange={(e) => updateCharacter(character.id, 'name', e.target.value)}
                          placeholder="Tên nhân vật"
                        />
                        <select
                          value={character.gender}
                          onChange={(e) => updateCharacter(character.id, 'gender', e.target.value)}
                          className={styles.genderSelect}
                        >
                          <option value="neutral">Neutral</option>
                          <option value="male">Nam</option>
                          <option value="female">Nữ</option>
                        </select>
                      </div>
                      <div className={styles.voiceSelection}>
                        <select
                          value={character.voice || 'Alice'}
                          onChange={(e) => updateCharacter(character.id, 'voice', e.target.value)}
                          className={styles.voiceSelect}
                          disabled={voiceSettings.autoAssignVoices}
                        >
                          {CHATTERBOX_VOICES.map(voice => (
                            <option key={voice} value={voice}>{voice}</option>
                          ))}
                        </select>
                        {voiceSettings.autoAssignVoices && (
                          <span className={styles.autoLabel}>Auto</span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Segments Section */}
                <div className={styles.segmentSection}>
                  <div className={styles.sectionHeader}>
                    <h3>Segments ({projectData.segments.length}) - {totalDialogues} dialogues</h3>
                    <button className={styles.addBtn} onClick={addSegment}>
                      <PlusIcon /> Thêm segment
                    </button>
                  </div>
                  
                  {projectData.segments.map((segment) => (
                    <div key={segment.id} className={styles.segmentCard}>
                      <div className={styles.segmentHeader}>
                        <span className={styles.segmentNumber}>Segment #{segment.id}</span>
                        <div style={{ display: 'flex', gap: '8px' }}>
                          <button 
                            className={styles.addDialogueBtn}
                            onClick={() => addDialogue(segment.id)}
                          >
                            <PlusIcon /> Dialogue
                          </button>
                          {projectData.segments.length > 1 && (
                            <button 
                              className={styles.deleteBtn} 
                              onClick={() => deleteSegment(segment.id)}
                            >
                              <TrashIcon />
                            </button>
                          )}
                        </div>
                      </div>

                      {segment.dialogues.map((dialogue, dialogueIndex) => (
                        <div key={dialogueIndex} className={styles.dialogueCard}>
                          <div className={styles.dialogueHeader}>
                            <span className={styles.dialogueNumber}>#{dialogueIndex + 1}</span>
                            <select
                              value={dialogue.speaker}
                              onChange={(e) => updateDialogue(segment.id, dialogueIndex, 'speaker', e.target.value)}
                              className={styles.speakerSelect}
                            >
                              {projectData.characters.map(character => (
                                <option key={character.id} value={character.id}>{character.name}</option>
                              ))}
                            </select>
                            <select
                              value={dialogue.emotion}
                              onChange={(e) => updateDialogue(segment.id, dialogueIndex, 'emotion', e.target.value)}
                              className={styles.emotionSelect}
                            >
                              {EMOTIONS.map(emotion => (
                                <option key={emotion} value={emotion}>{emotion}</option>
                              ))}
                            </select>
                            
                            <div className={styles.innerVoiceControls}>
                              <label className={styles.checkboxLabel}>
                                <input
                                  type="checkbox"
                                  checked={dialogue.inner_voice || false}
                                  onChange={(e) => updateDialogue(segment.id, dialogueIndex, 'inner_voice', e.target.checked)}
                                />
                                Inner Voice
                              </label>
                              {dialogue.inner_voice && (
                                <select
                                  value={dialogue.inner_voice_type || 'light'}
                                  onChange={(e) => updateDialogue(segment.id, dialogueIndex, 'inner_voice_type', e.target.value)}
                                  className={styles.innerVoiceSelect}
                                >
                                  <option value="light">Light</option>
                                  <option value="deep">Deep</option>
                                  <option value="dreamy">Dreamy</option>
                                </select>
                              )}
                            </div>

                            {segment.dialogues.length > 1 && (
                              <button 
                                className={styles.deleteBtn}
                                onClick={() => deleteDialogue(segment.id, dialogueIndex)}
                              >
                                <TrashIcon />
                              </button>
                            )}
                          </div>
                          <textarea
                            className={styles.dialogueText}
                            value={dialogue.text}
                            onChange={(e) => updateDialogue(segment.id, dialogueIndex, 'text', e.target.value)}
                            placeholder="Nhập nội dung dialogue..."
                            rows={2}
                          />
                        </div>
                      ))}
                    </div>
                  ))}
                </div>

                <div className={styles.multiCharacterFooter}>
                  <div className={styles.charCounter}>
                    Tổng: {projectData.segments.reduce((total, segment) => 
                      total + segment.dialogues.reduce((segTotal, dialogue) => 
                        segTotal + dialogue.text.length, 0), 0
                    )} ký tự
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <div 
                      className={styles.toolsBtn} 
                      onClick={() => fileInputRef.current?.click()}
                      title="Upload JSON Script"
                    >
                      <UploadIcon />
                    </div>
                    <div 
                      className={styles.toolsBtn} 
                      onClick={() => setIsVoiceConfigOpen(!isVoiceConfigOpen)}
                    >
                      <SettingsIcon />
                    </div>
                    <button className={styles.generateBtn} onClick={handleGenerate}>
                      <PlayIcon />
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Voice Config - Enhanced for ChatterboxTTS */}
            <div className={`${styles.voiceConfig} ${isVoiceConfigOpen ? styles.show : ''}`}>
              <div className={styles.configTitle}>
                ChatterboxTTS Settings
                <div className={styles.configClose} onClick={() => setIsVoiceConfigOpen(false)}>
                  <CloseIcon />
                </div>
              </div>

              {/* Single character emotion (only for single mode) */}
              {!isMultiCharacter && (
                <div className={styles.settingGroup}>
                  <label className={styles.settingLabel}>Emotion (Single Mode)</label>
                  <select 
                    className={styles.settingControl}
                    value={voiceSettings.singleEmotion}
                    onChange={(e) => setVoiceSettings({...voiceSettings, singleEmotion: e.target.value})}
                  >
                    {EMOTIONS.map(emotion => (
                      <option key={emotion} value={emotion}>{emotion}</option>
                    ))}
                  </select>
                </div>
              )}

              <div className={styles.settingGroup}>
                <label className={styles.settingLabel}>Temperature</label>
                <div className={styles.sliderControl}>
                  <input 
                    type="range" 
                    min="0.1" 
                    max="1.0" 
                    step="0.1" 
                    value={voiceSettings.temperature}
                    onChange={(e) => setVoiceSettings({...voiceSettings, temperature: parseFloat(e.target.value)})}
                  />
                  <span className={styles.sliderValue}>{voiceSettings.temperature.toFixed(1)}</span>
                </div>
              </div>

              <div className={styles.settingGroup}>
                <label className={styles.settingLabel}>CFG Scale</label>
                <div className={styles.sliderControl}>
                  <input 
                    type="range" 
                    min="1.0" 
                    max="5.0" 
                    step="0.5" 
                    value={voiceSettings.cfg}
                    onChange={(e) => setVoiceSettings({...voiceSettings, cfg: parseFloat(e.target.value)})}
                  />
                  <span className={styles.sliderValue}>{voiceSettings.cfg.toFixed(1)}</span>
                </div>
              </div>

              <div className={styles.settingGroup}>
                <label className={styles.settingLabel}>Exaggeration</label>
                <div className={styles.sliderControl}>
                  <input 
                    type="range" 
                    min="0.1" 
                    max="2.0" 
                    step="0.1" 
                    value={voiceSettings.exaggeration}
                    onChange={(e) => setVoiceSettings({...voiceSettings, exaggeration: parseFloat(e.target.value)})}
                  />
                  <span className={styles.sliderValue}>{voiceSettings.exaggeration.toFixed(1)}</span>
                </div>
              </div>

              <div className={styles.settingGroup}>
                <label className={styles.settingLabel}>Speed</label>
                <div className={styles.sliderControl}>
                  <input 
                    type="range" 
                    min="0.5" 
                    max="2.0" 
                    step="0.1" 
                    value={voiceSettings.speed}
                    onChange={(e) => setVoiceSettings({...voiceSettings, speed: parseFloat(e.target.value)})}
                  />
                  <span className={styles.sliderValue}>{voiceSettings.speed.toFixed(1)}x</span>
                </div>
              </div>

              <div className={styles.settingGroup}>
                <label className={styles.checkboxLabel}>
                  <input
                    type="checkbox"
                    checked={voiceSettings.autoAssignVoices}
                    onChange={(e) => setVoiceSettings({...voiceSettings, autoAssignVoices: e.target.checked})}
                  />
                  Auto-assign voices by gender
                </label>
              </div>
            </div>
          </div>

          {/* Progress Indicator */}
          {isGenerating && (
            <div className={styles.progressIndicator}>
              <div className={styles.progressSpinner}></div>
              <div className={styles.progressText}>Generating with ChatterboxTTS...</div>
            </div>
          )}
        </div>

        {/* Audio Player Bar */}
        <div className={styles.audioPlayerBar}>
          <div className={styles.playerControls}>
            <div className={styles.playBtn} onClick={togglePlay}>
              {isPlaying ? <PauseIcon /> : <PlayIcon />}
            </div>
            <div className={styles.progressTrack} onClick={handleSeek}>
              <div 
                className={styles.progressBarFill} 
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <div className={styles.timeDisplay}>
              <span>{formatTime(Math.floor(progress * 83 / 100))}</span> / <span>1:23</span>
            </div>
          </div>
          <div className={styles.audioActions}>
            <div className={styles.actionBtn} onClick={() => alert('Tải xuống dưới dạng MP3')}>
              <DownloadIcon />
            </div>
            <div className={styles.actionBtn} onClick={() => alert('Chia sẻ project!')}>
              <ShareIcon />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VoiceStudioV2; 