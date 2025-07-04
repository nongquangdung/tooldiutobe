import React, { useState } from 'react';
import VoiceStudioV2 from './components/VoiceStudioV2';
import EmotionLibraryModal from './components/EmotionLibraryModal';
import VoiceLibraryModal from './components/VoiceLibraryModal';
import styles from './styles/App.module.css';

const App: React.FC = () => {
  const [showEmotionLibrary, setShowEmotionLibrary] = useState(false);
  const [showVoiceLibrary, setShowVoiceLibrary] = useState(false);

  return (
    <div className={styles.appContainer}>
      {/* Main Content - Full Width */}
      <div className={styles.fullWidthContent}>
        <VoiceStudioV2 
          onOpenEmotionLibrary={() => setShowEmotionLibrary(true)}
          onOpenVoiceLibrary={() => setShowVoiceLibrary(true)}
        />
      </div>
      
      {/* Modals */}
      {showEmotionLibrary && (
        <EmotionLibraryModal onClose={() => setShowEmotionLibrary(false)} />
      )}
      
      {showVoiceLibrary && (
        <VoiceLibraryModal 
          onClose={() => setShowVoiceLibrary(false)}
          onSelectVoice={(voiceId) => {
            console.log('Selected voice:', voiceId);
            setShowVoiceLibrary(false);
          }}
        />
      )}
    </div>
  );
};

export default App; 