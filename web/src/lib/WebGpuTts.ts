/*
  WebGpuTts - wrapper util dùng transformers.js + onnxruntime-web
  Chỉ load model 1 lần, cache IndexedDB. Nếu navigator.gpu không khả dụng hoặc lỗi, hàm generate sẽ throw → UI fallback sang REST.
*/

import * as ort from 'onnxruntime-web';
import { pipeline } from '@xenova/transformers';

export interface EmotionCfg {
  exaggeration: number;
  cfg: number;
  temperature: number;
  speed: number;
}

class WebGpuTts {
  private ready: boolean = false;
  private synthesizer: any; // type any vì lib chưa có types chuẩn cho TTS

  async init() {
    if (this.ready) return;
    // Check WebGPU availability
    // @ts-ignore - navigator.gpu experimental typing
    if (!(navigator as any).gpu) {
      throw new Error('WebGPU not supported');
    }

    // Init ONNX WebGPU backend
    // @ts-ignore - experimental api
    await (ort as any).env.wasm.init();
    ort.env.logLevel = 'warning';
    ort.env.wasm.wasmPaths = 'https://cdn.jsdelivr.net/npm/onnxruntime-web@1.19.0/dist/';
    await ort.InferenceSession.create('dummy');

    // Load model via transformers.js (WebGPU)
    // @ts-ignore - extra options for transformers.js
    this.synthesizer = await pipeline('text-to-audio', 'onnx-community/Kokoro-82M-v1.0-ONNX', {
      quantized: false,
      // @ts-ignore
      device: 'webgpu'
    });
    this.ready = true;
  }

  async generate(text: string, emotion: EmotionCfg): Promise<ArrayBuffer> {
    if (!this.ready) await this.init();
    // Simple mapping of emotion parameters to kokoro options
    const options = {
      voice: 'default',
      ...emotion
    };
    const result = await this.synthesizer(text, options);
    // result.audio is Blob | ArrayBuffer depending on transformers.js version
    const buffer = result.audio instanceof Blob ? await result.audio.arrayBuffer() : result.audio;
    return buffer;
  }
}

export default new WebGpuTts(); 