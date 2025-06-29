/*
  LocalTts.ts
  Wrapper sinh giọng nói cục bộ bằng kokoro-js.
  Thứ tự ưu tiên backend: WebGPU ➜ WASM (CPU).
*/

// @ts-ignore – thư viện chưa có khai báo types chuẩn
import { KokoroTTS } from 'kokoro-js';

export type BackendMode = 'webgpu' | 'wasm';

export interface EmotionCfg {
  exaggeration: number;
  cfg: number;
  temperature: number;
  speed: number;
}

class LocalTts {
  private ready = false;
  private backend: BackendMode | null = null;
  private tts: any;

  private detectBackend(): BackendMode {
    return (navigator as any).gpu ? 'webgpu' : 'wasm';
  }

  async init() {
    if (this.ready) return;

    this.backend = this.detectBackend();
    const dtype = this.backend === 'webgpu' ? 'fp32' : 'q8';

    // Load model (cached sau lần đầu)
    this.tts = await KokoroTTS.from_pretrained('onnx-community/Kokoro-82M-v1.0-ONNX', {
      // @ts-ignore – device option do kokoro-js định nghĩa
      device: this.backend,
      dtype
    });

    this.ready = true;
  }

  async generate(text: string, emotion: EmotionCfg): Promise<ArrayBuffer> {
    if (!this.ready) {
      await this.init();
    }

    // Map emotion.speed → speed, các thông số khác để TODO sau
    const options: any = {
      voice: 'af_heart', // default voice
      speed: emotion.speed ?? 1.0
    };

    const audio = await this.tts.generate(text, options);

    // toWav() trả về Uint8Array; chuyển sang ArrayBuffer
    const wavData: Uint8Array = await audio.toWav();
    return wavData.buffer as ArrayBuffer;
  }
}

export default new LocalTts(); 