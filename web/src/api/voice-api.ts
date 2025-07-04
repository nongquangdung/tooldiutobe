import axios from 'axios';
// Dùng kiểu đơn giản cho parameters gửi lên server
export interface TtsParams {
  exaggeration: number;
  cfg: number;
  temperature: number;
  speed: number;
  emotion?: string;
  inner?: boolean;
}

// Mặc định server Docker của Chatterbox mở cổng 8005.
// Có thể override bằng biến môi trường VITE_API_URL.
const API_BASE = (import.meta as any).env.VITE_API_URL || 'http://localhost:8000';

/**
 * Gọi OpenAI-compatible endpoint của Chatterbox-TTS-Server
 * POST /v1/audio/speech
 * Body: {
 *   input: "Text",
 *   exaggeration, cfg_weight, temperature, speed, voice_id?
 * }
 * Trả về audio/wav (arraybuffer)
 */
export async function generateVoiceREST(text: string, params: TtsParams, voiceId?: string): Promise<ArrayBuffer> {
  const payload: any = {
    input: text,
    exaggeration: params.exaggeration,
    cfg_weight: params.cfg,
    temperature: params.temperature,
    speed: params.speed,
    emotion: params.emotion,
    inner: params.inner
  };
  if (voiceId) {
    payload.voice_id = voiceId;
  }

  const res = await axios.post(`${API_BASE}/v1/audio/speech`, payload, {
    responseType: 'arraybuffer'
  });

  return res.data as ArrayBuffer;
}

export interface Voice {
  id: string;
  name: string;
  gender: string;
  description: string;
}

export async function fetchVoices(): Promise<{count: number, voices: Voice[]}> {
  const res = await axios.get(`${API_BASE}/v1/voices`);
  return res.data;
}

export async function uploadVoice(file: File, name?: string): Promise<{success: boolean, voice_id: string}> {
  const form = new FormData();
  form.append('file', file);
  if (name) {
    form.append('name', name);
  }
  
  const res = await axios.post(`${API_BASE}/v1/voices/upload`, form, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  
  return res.data;
} 