import { useState } from 'react';
import { Box, Button, HStack, Textarea, useToast } from '@chakra-ui/react';
import EmotionTable from '../components/EmotionTable';
import { generateVoiceREST } from '../api/voice-api';

const defaultEmotion = {
  exaggeration: 1.0,
  cfg: 0.5,
  temperature: 0.8,
  speed: 1.0
};

const VoiceStudio = () => {
  const [text, setText] = useState('Hello, this is Voice Studio Web!');
  const [emotion, setEmotion] = useState(defaultEmotion);
  const [loading, setLoading] = useState(false);
  const toast = useToast();

  const generateVoice = async () => {
    if (!text.trim()) {
      toast({ title: 'Nhập nội dung trước khi generate', status: 'warning' });
      return;
    }
    setLoading(true);
    try {
      const buffer: ArrayBuffer = await generateVoiceREST(text, emotion);
      const blob = new Blob([buffer], { type: 'audio/wav' });
      const url = URL.createObjectURL(blob);
      const audio = new Audio(url);
      await audio.play();
      toast({ title: 'Đã generate thành công', status: 'success' });
    } catch (err) {
      toast({ title: 'Lỗi generate', status: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box borderWidth="1px" borderRadius="md" p={4}>
      <Textarea
        placeholder="Nhập đoạn văn bản..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={4}
        mb={4}
      />
      <EmotionTable value={emotion} onChange={setEmotion} />
      <HStack mt={4}>
        <Button colorScheme="blue" onClick={generateVoice} isLoading={loading}>
          Generate Voice
        </Button>
      </HStack>
    </Box>
  );
};

export default VoiceStudio; 