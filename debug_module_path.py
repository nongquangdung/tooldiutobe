#!/usr/bin/env python3
import importlib, inspect, sys, os
sys.path.insert(0, 'src')
mod = importlib.import_module('ui.emotion_config_tab')
print('Loaded module file:', mod.__file__)
print('Module mtime:', os.path.getmtime(mod.__file__))
print('Classes:', [cls for cls in dir(mod) if cls.endswith('Thread')])
IV = mod.InnerVoicePreviewThread
print('InnerVoicePreviewThread qualname', IV.__qualname__)
print('Module of IV', IV.__module__)

print('run lines first 120:')
print(inspect.getsource(IV.run)[:500])
print('[IV_THREAD_VERSION] in source?', 'IV_THREAD_VERSION' in inspect.getsource(IV.run)) 