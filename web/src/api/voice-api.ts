import axios from 'axios';
import { EmotionCfg } from '../lib/WebGpuTts';

// Mặc định server Docker của Chatterbox mở cổng 8005.
// Có thể override bằng biến môi trường VITE_API_URL.
const API_BASE = (import.meta as any).env.VITE_API_URL || 'http://localhost:8005';

/**
 * Gọi OpenAI-compatible endpoint của Chatterbox-TTS-Server
 * POST /v1/audio/speech
 * Body: {
 *   input: "Text",
 *   exaggeration, cfg_weight, temperature, speed
 * }
 * Trả về audio/wav (arraybuffer)
 */
export async function generateVoiceREST(text: string, emotion: EmotionCfg): Promise<ArrayBuffer> {
  const payload = {
    input: text,
    exaggeration: emotion.exaggeration,
    cfg_weight: emotion.cfg,
    temperature: emotion.temperature,
    speed: emotion.speed
  };

  const res = await axios.post(`${API_BASE}/v1/audio/speech`, payload, {
    responseType: 'arraybuffer'
  });

  return res.data as ArrayBuffer;
} 