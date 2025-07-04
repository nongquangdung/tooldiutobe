import axios from 'axios';

const API_BASE = (import.meta as any).env.VITE_API_URL || 'http://localhost:8000';

export interface Emotion {
  id: string;
  name: string;
  exaggeration: number;
  cfg_weight: number;
  temperature: number;
  speed: number;
  category?: string;
}

export async function fetchEmotions(): Promise<Record<string, Emotion>> {
  const res = await axios.get(`${API_BASE}/v1/emotions`);
  return res.data;
}

export async function createEmotion(data: Omit<Emotion, 'id'>): Promise<string> {
  const res = await axios.post(`${API_BASE}/v1/emotions`, data);
  return res.data.id;
}

export async function updateEmotion(id: string, data: Emotion) {
  await axios.put(`${API_BASE}/v1/emotions/${id}`, data);
}

export async function deleteEmotion(id: string) {
  await axios.delete(`${API_BASE}/v1/emotions/${id}`);
}

export async function deleteAllEmotions() {
  await axios.delete(`${API_BASE}/v1/emotions/all`);
}

export async function importEmotionFile(file: File) {
  const form = new FormData();
  form.append('file', file);
  await axios.post(`${API_BASE}/v1/emotions/import`, form, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
}

export async function exportEmotions(): Promise<Blob> {
  const res = await axios.get(`${API_BASE}/v1/emotions/export`, { responseType: 'blob' });
  return res.data;
} 