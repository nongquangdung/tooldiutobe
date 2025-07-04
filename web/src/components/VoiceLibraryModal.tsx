import React, { useEffect, useState, useRef } from 'react';
import styles from '../styles/VoiceStudioV2.module.css';
import { fetchVoices, uploadVoice, Voice } from '../api/voice-api';

interface Props {
  onClose: () => void;
  onSelectVoice?: (voiceId: string) => void;
}

const SearchIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="11" cy="11" r="8"></circle>
    <path d="M21 21l-4.35-4.35"></path>
  </svg>
);

const FilterIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="22,3 2,3 10,12.46 10,19 14,21 14,12.46"></polygon>
  </svg>
);

const PlayIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="5,3 19,12 5,21"></polygon>
  </svg>
);

const UploadIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
    <polyline points="17,8 12,3 7,8"></polyline>
    <line x1="12" y1="3" x2="12" y2="15"></line>
  </svg>
);

const VoiceLibraryModal: React.FC<Props> = ({ onClose, onSelectVoice }) => {
  const [voices, setVoices] = useState<Voice[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');
  const [activeTab, setActiveTab] = useState('all');
  const [uploadName, setUploadName] = useState('');
  const [uploading, setUploading] = useState(false);
  const [selectedVoice, setSelectedVoice] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    loadVoices();
  }, []);

  const loadVoices = async () => {
    setLoading(true);
    try {
      const data = await fetchVoices();
      setVoices(data.voices);
    } catch (err) {
      console.error('Failed to load voices', err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    const file = fileInputRef.current?.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      await uploadVoice(file, uploadName || undefined);
      await loadVoices();
      setUploadName('');
      if (fileInputRef.current) fileInputRef.current.value = '';
      alert('Voice uploaded successfully!');
    } catch (err: any) {
      alert(`Upload failed: ${err.message || 'Unknown error'}`);
    } finally {
      setUploading(false);
    }
  };

  const handleVoiceClick = (voiceId: string) => {
    setSelectedVoice(voiceId);
    onSelectVoice?.(voiceId);
  };

  const filteredVoices = voices.filter(voice => {
    // Filter by search term
    const matchesSearch = !filter || 
      voice.name.toLowerCase().includes(filter.toLowerCase()) ||
      voice.description.toLowerCase().includes(filter.toLowerCase());
    
    // Filter by tab
    if (activeTab === 'all') return matchesSearch;
    if (activeTab === 'male') return matchesSearch && voice.gender === 'male';
    if (activeTab === 'female') return matchesSearch && voice.gender === 'female';
    
    return matchesSearch;
  });

  return (
    <div className={styles.voiceLibraryOverlay}>
      <div className={styles.voiceLibraryModal}>
        {/* Header */}
        <div className={styles.voiceLibraryHeader}>
          <div className={styles.headerLeft}>
            <h2 className={styles.modalTitle}>Voice Library</h2>
            <p className={styles.modalSubtitle}>Chọn giọng nói hoàn hảo cho dự án của bạn</p>
          </div>
          <button className={styles.closeButton} onClick={onClose}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        {/* Search & Filter Bar */}
        <div className={styles.voiceLibraryToolbar}>
          <div className={styles.searchSection}>
            <div className={styles.searchInputWrapper}>
              <SearchIcon />
              <input
                type="text"
                placeholder="Tìm kiếm giọng nói..."
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className={styles.voiceSearchInput}
              />
            </div>
          </div>
          
          <div className={styles.filterSection}>
            <div className={styles.voiceFilterTabs}>
              <button 
                className={activeTab === 'all' ? styles.voiceTabActive : styles.voiceTab} 
                onClick={() => setActiveTab('all')}
              >
                Tất cả ({voices.length})
              </button>
              <button 
                className={activeTab === 'male' ? styles.voiceTabActive : styles.voiceTab} 
                onClick={() => setActiveTab('male')}
              >
                Nam ({voices.filter(v => v.gender === 'male').length})
              </button>
              <button 
                className={activeTab === 'female' ? styles.voiceTabActive : styles.voiceTab} 
                onClick={() => setActiveTab('female')}
              >
                Nữ ({voices.filter(v => v.gender === 'female').length})
              </button>
            </div>
            
            <button className={styles.uploadButton} onClick={() => fileInputRef.current?.click()}>
              <UploadIcon />
              Upload Voice
            </button>
          </div>
        </div>

        {/* Voice Grid */}
        <div className={styles.voiceLibraryContent}>
          {loading ? (
            <div className={styles.voiceLoadingState}>
              <div className={styles.loadingSpinner}></div>
              <p>Đang tải giọng nói...</p>
            </div>
          ) : filteredVoices.length === 0 ? (
            <div className={styles.voiceEmptyState}>
              <div className={styles.emptyStateIcon}>🎙️</div>
              <h3>Không tìm thấy giọng nói</h3>
              <p>Thử thay đổi bộ lọc hoặc từ khóa tìm kiếm</p>
            </div>
          ) : (
            <div className={styles.voiceGrid}>
              {filteredVoices.map((voice) => (
                <div 
                  key={voice.id} 
                  className={`${styles.voiceCard} ${selectedVoice === voice.id ? styles.voiceCardSelected : ''}`}
                  onClick={() => handleVoiceClick(voice.id)}
                >
                  <div className={styles.voiceCardHeader}>
                    <div className={styles.voiceAvatar}>
                      <div className={styles.voiceAvatarIcon}>
                        {voice.gender === 'male' ? '👨' : voice.gender === 'female' ? '👩' : '🎭'}
                      </div>
                      <div className={styles.voiceGenderBadge}>
                        <span className={`${styles.genderBadge} ${styles[`gender${voice.gender}`]}`}>
                          {voice.gender === 'male' ? 'Nam' : voice.gender === 'female' ? 'Nữ' : 'Khác'}
                        </span>
                      </div>
                    </div>
                    <button className={styles.voicePlayButton}>
                      <PlayIcon />
                    </button>
                  </div>
                  
                  <div className={styles.voiceCardBody}>
                    <h3 className={styles.voiceName}>{voice.name}</h3>
                    <p className={styles.voiceDescription}>{voice.description}</p>
                    
                    <div className={styles.voiceMetadata}>
                      <div className={styles.voiceQuality}>
                        <span className={styles.qualityLabel}>Chất lượng:</span>
                        <div className={styles.qualityStars}>
                          {'★'.repeat(5)}
                        </div>
                      </div>
                      <div className={styles.voiceProvider}>ChatterboxTTS</div>
                    </div>
                  </div>
                  
                  {selectedVoice === voice.id && (
                    <div className={styles.selectedIndicator}>
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3">
                        <polyline points="20,6 9,17 4,12"></polyline>
                      </svg>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Upload Form - Hidden Input */}
        <input
          type="file"
          ref={fileInputRef}
          accept=".wav"
          style={{ display: 'none' }}
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) {
              // Show upload dialog
              const name = prompt('Tên giọng nói (tùy chọn):');
              setUploadName(name || '');
              handleUpload(e as any);
            }
          }}
        />
      </div>
    </div>
  );
};

export default VoiceLibraryModal; 