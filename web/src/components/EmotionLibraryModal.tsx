import React, { useEffect, useState } from 'react';
import styles from '../styles/VoiceStudioV2.module.css'; // Re-use same design tokens
import {
  fetchEmotions,
  createEmotion,
  updateEmotion,
  deleteEmotion,
  importEmotionFile,
  exportEmotions,
  Emotion
} from '../api/emotion-api';

interface Props {
  onClose: () => void;
}

const emptyRow = (): Emotion => ({
  id: '',
  name: '',
  exaggeration: 1.0,
  cfg_weight: 0.5,
  temperature: 0.8,
  speed: 1.0,
  category: ''
});

const EmotionLibraryModal: React.FC<Props> = ({ onClose }) => {
  const [emotions, setEmotions] = useState<Record<string, Emotion>>({});
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    fetchEmotions().then((raw) => {
      const data = (raw as any).emotions ? (raw as any).emotions : raw;
      // Ensure numeric properties are numbers
      const normalized: Record<string, Emotion> = {};
      Object.entries(data).forEach(([id, raw]) => {
        const emo: any = raw;
        if (!emo || typeof emo !== 'object') return;
        const makeNumber = (v: any, def: number) => {
          const n = parseFloat(v);
          return Number.isFinite(n) ? n : def;
        };
        const params = (emo as any).parameters || emo;
        normalized[id] = {
          id,
          name: emo.name || id,
          exaggeration: makeNumber(params.exaggeration, 1.0),
          cfg_weight: makeNumber(params.cfg_weight, 0.5),
          temperature: makeNumber(params.temperature, 0.8),
          speed: makeNumber(params.speed, 1.0),
          category: params.category ?? emo.category ?? ''
        } as Emotion;
      });
      setEmotions(normalized);
    });
  }, []);

  const handleAdd = () => {
    const newRow = emptyRow();
    // Temporary negative key before saving
    const tempId = `temp-${Date.now()}`;
    setEmotions({ ...emotions, [tempId]: newRow });
  };

  const handleChange = (id: string, field: keyof Emotion, value: string | number) => {
    setEmotions({
      ...emotions,
      [id]: {
        ...emotions[id],
        [field]: value
      }
    });
  };

  const handleDelete = async (id: string) => {
    if (id.startsWith('temp-')) {
      const copy = { ...emotions };
      delete copy[id];
      setEmotions(copy);
      return;
    }
    try {
      await deleteEmotion(id);
    } catch (e) {
      console.warn('Backend delete failed, will remove locally', e);
    }
    const copy = { ...emotions };
    delete copy[id];
    setEmotions(copy);
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      let working: Record<string, Emotion> = { ...emotions };

      // 1. Create new emotions (temp-)
      for (const [id, emo] of Object.entries(emotions)) {
        if (!id.startsWith('temp-')) continue;
        const { id: _omit, ...payload } = emo as any;
        try {
          const newId = await createEmotion(payload);
          delete working[id];
          working[newId] = { ...payload, id: newId } as Emotion;
        } catch (e) {
          console.error('Create failed', e);
        }
      }

      // 2. Update existing emotions
      for (const emo of Object.values(working)) {
        if (!emo.id || emo.id.startsWith('temp-')) continue;
        try {
          await updateEmotion(emo.id, emo);
        } catch (e) {
          console.warn('Update fail id', emo.id, e);
        }
      }

      const updated = await fetchEmotions();
      setEmotions(updated);
      alert('Emotion library saved!');
    } catch (e: any) {
      console.error(e);
      alert('Save failed: ' + (e?.message || 'Unknown error'));
    } finally {
      setIsSaving(false);
    }
  };

  const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      try {
        await importEmotionFile(file);
        const raw = await fetchEmotions();
        const data = (raw as any).emotions ? (raw as any).emotions : raw;
        // Preserve original categories from import
        const normalized: Record<string, Emotion> = {};
        Object.entries(data).forEach(([id, raw]) => {
          const emo: any = raw;
          if (!emo || typeof emo !== 'object') return;
          const makeNumber = (v: any, def: number) => {
            const n = parseFloat(v);
            return Number.isFinite(n) ? n : def;
          };
          const params = (emo as any).parameters || emo;
          normalized[id] = {
            id,
            name: emo.name || id,
            exaggeration: makeNumber(params.exaggeration, 1.0),
            cfg_weight: makeNumber(params.cfg_weight, 0.5),
            temperature: makeNumber(params.temperature, 0.8),
            speed: makeNumber(params.speed, 1.0),
            // Keep original category, don't default to 'general'
            category: params.category ?? emo.category ?? ''
          } as Emotion;
        });
        setEmotions(normalized);
        alert('Import successful!');
      } catch (e: any) {
        alert('Import failed: ' + (e?.message || 'Unknown error'));
      }
    }
  };

  const handleExport = async () => {
    const blob = await exportEmotions();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'emotion_library.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modalContentLarge}>
        <div className={styles.modalHeader}>Emotion Library
          <button className={styles.iconBtn} onClick={onClose}>×</button>
        </div>

        <div className={styles.modalBody} style={{ maxHeight: '60vh', overflow: 'auto' }}>
          <table className={styles.basicTable} style={{ width: '100%' }}>
            <thead>
              <tr>
                <th>Name</th>
                <th>Exa</th>
                <th>CFG</th>
                <th>Temp</th>
                <th>Speed</th>
                <th>Category</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(emotions).map(([id, emo]) => (
                <tr key={id}>
                  <td>
                    <input type="text" value={emo.name} onChange={e => handleChange(id, 'name', e.target.value)} />
                  </td>
                  <td>
                    <input type="number" step={0.1} min={0} max={3} value={emo.exaggeration ?? ''} onChange={e => handleChange(id, 'exaggeration', parseFloat(e.target.value))} />
                  </td>
                  <td>
                    <input type="number" step={0.1} min={0.1} max={1} value={emo.cfg_weight ?? ''} onChange={e => handleChange(id, 'cfg_weight', parseFloat(e.target.value))} />
                  </td>
                  <td>
                    <input type="number" step={0.1} min={0} max={2} value={emo.temperature ?? ''} onChange={e => handleChange(id, 'temperature', parseFloat(e.target.value))} />
                  </td>
                  <td>
                    <input type="number" step={0.1} min={0.5} max={3} value={emo.speed ?? ''} onChange={e => handleChange(id, 'speed', parseFloat(e.target.value))} />
                  </td>
                  <td>
                    <input type="text" value={emo.category ?? ''} onChange={e => handleChange(id, 'category', e.target.value)} />
                  </td>
                  <td>
                    <button className={styles.iconBtn} onClick={() => handleDelete(id)}>🗑</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className={styles.modalFooter}>
          <input type="file" accept="application/json" style={{ display: 'none' }} id="emotionImport" onChange={handleImport} />
          <button className={styles.secondaryBtn} onClick={handleAdd}>+ Add</button>
          <label htmlFor="emotionImport" className={styles.secondaryBtn}>Import</label>
          <button className={styles.secondaryBtn} onClick={handleExport}>Export</button>
          <button className={styles.primaryBtn} disabled={isSaving} onClick={handleSave}>{isSaving ? 'Saving…' : 'Save'}</button>
        </div>
      </div>
    </div>
  );
};

export default EmotionLibraryModal; 