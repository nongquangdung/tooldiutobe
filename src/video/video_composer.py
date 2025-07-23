<<<<<<< Updated upstream
import ffmpeg
import os
import subprocess
from pathlib import Path

class VideoComposer:
    def __init__(self):
        self.temp_dir = "temp_video"
        Path(self.temp_dir).mkdir(exist_ok=True)
    
    def create_segment_video(self, image_path, audio_path, output_path, effects=None):
        """Tạo video từ 1 ảnh + 1 audio với hiệu ứng"""
        try:
            # Lấy độ dài audio
            probe = ffmpeg.probe(audio_path)
            duration = float(probe['streams'][0]['duration'])
            
            # Tạo input streams
            image_input = ffmpeg.input(image_path, loop=1, t=duration)
            audio_input = ffmpeg.input(audio_path)
            
            # Áp dụng hiệu ứng cho ảnh
            if effects and effects.get('zoom', False):
                # Hiệu ứng zoom in/out
                zoom_factor = effects.get('zoom_factor', 1.1)
                image_input = image_input.filter('zoompan', 
                    z=f'min(zoom+0.0015,{zoom_factor})', 
                    d=int(duration * 25),  # 25 fps
                    x='iw/2-(iw/zoom/2)', 
                    y='ih/2-(ih/zoom/2)'
                )
            
            # Resize về 1920x1080
            image_input = image_input.filter('scale', 1920, 1080)
            
            # Ghép video
            output = ffmpeg.output(
                image_input, audio_input,
                output_path,
                vcodec='libx264',
                acodec='aac',
                pix_fmt='yuv420p',
                r=25  # 25 fps
            )
            
            ffmpeg.run(output, overwrite_output=True, quiet=True)
            return {"success": True, "path": output_path, "duration": duration}
            
        except Exception as e:
            return {"success": False, "error": f"Lỗi tạo video segment: {str(e)}"}
    
    def merge_segments(self, segment_paths, output_path, transitions=None):
        """Ghép nhiều segment thành video hoàn chỉnh"""
        try:
            # Tạo file list cho ffmpeg concat
            list_file = os.path.join(self.temp_dir, "segments_list.txt")
            with open(list_file, 'w') as f:
                for path in segment_paths:
                    f.write(f"file '{os.path.abspath(path)}'\n")
            
            # Ghép video
            if transitions and transitions.get('crossfade', False):
                # Ghép với hiệu ứng chuyển cảnh (phức tạp hơn)
                return self._merge_with_transitions(segment_paths, output_path, transitions)
            else:
                # Ghép đơn giản
                cmd = [
                    'ffmpeg', '-f', 'concat', '-safe', '0', 
                    '-i', list_file, '-c', 'copy', 
                    '-y', output_path
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    return {"success": True, "path": output_path}
                else:
                    return {"success": False, "error": f"FFmpeg error: {result.stderr}"}
                    
        except Exception as e:
            return {"success": False, "error": f"Lỗi ghép video: {str(e)}"}
    
    def _merge_with_transitions(self, segment_paths, output_path, transitions):
        """Ghép video với hiệu ứng chuyển cảnh"""
        try:
            # Tạo filter complex cho crossfade
            inputs = []
            for path in segment_paths:
                inputs.append(ffmpeg.input(path))
            
            # Áp dụng crossfade giữa các segment
            current = inputs[0]
            for i in range(1, len(inputs)):
                fade_duration = transitions.get('fade_duration', 0.5)
                current = ffmpeg.filter([current, inputs[i]], 'xfade', 
                                      transition='fade', duration=fade_duration)
            
            output = ffmpeg.output(current, output_path, vcodec='libx264', acodec='aac')
            ffmpeg.run(output, overwrite_output=True, quiet=True)
            
            return {"success": True, "path": output_path}
        except Exception as e:
            return {"success": False, "error": f"Lỗi ghép với transitions: {str(e)}"}
    
    def add_background_music(self, video_path, music_path, output_path, music_volume=0.3):
        """Thêm nhạc nền vào video"""
        try:
            video_input = ffmpeg.input(video_path)
            music_input = ffmpeg.input(music_path)
            
            # Mix audio với volume thấp cho nhạc nền
            audio_mixed = ffmpeg.filter([video_input['a'], music_input], 'amix', 
                                      inputs=2, duration='first', 
                                      weights=f'1 {music_volume}')
            
            output = ffmpeg.output(video_input['v'], audio_mixed, output_path,
                                 vcodec='copy', acodec='aac')
            
            ffmpeg.run(output, overwrite_output=True, quiet=True)
            return {"success": True, "path": output_path}
        except Exception as e:
            return {"success": False, "error": f"Lỗi thêm nhạc nền: {str(e)}"}
    
    def cleanup_temp_files(self):
        """Dọn dẹp file tạm"""
        try:
            import shutil
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": f"Lỗi dọn dẹp: {str(e)}"} 
=======
import ffmpeg
import os
import subprocess
from pathlib import Path

class VideoComposer:
    def __init__(self):
        self.temp_dir = "temp_video"
        Path(self.temp_dir).mkdir(exist_ok=True)
    
    def create_segment_video(self, image_path, audio_path, output_path, effects=None):
        """Tạo video từ 1 ảnh + 1 audio với hiệu ứng"""
        try:
            # Lấy độ dài audio
            probe = ffmpeg.probe(audio_path)
            duration = float(probe['streams'][0]['duration'])
            
            # Tạo input streams
            image_input = ffmpeg.input(image_path, loop=1, t=duration)
            audio_input = ffmpeg.input(audio_path)
            
            # Áp dụng hiệu ứng cho ảnh
            if effects and effects.get('zoom', False):
                # Hiệu ứng zoom in/out
                zoom_factor = effects.get('zoom_factor', 1.1)
                image_input = image_input.filter('zoompan', 
                    z=f'min(zoom+0.0015,{zoom_factor})', 
                    d=int(duration * 25),  # 25 fps
                    x='iw/2-(iw/zoom/2)', 
                    y='ih/2-(ih/zoom/2)'
                )
            
            # Resize về 1920x1080
            image_input = image_input.filter('scale', 1920, 1080)
            
            # Ghép video
            output = ffmpeg.output(
                image_input, audio_input,
                output_path,
                vcodec='libx264',
                acodec='aac',
                pix_fmt='yuv420p',
                r=25  # 25 fps
            )
            
            ffmpeg.run(output, overwrite_output=True, quiet=True)
            return {"success": True, "path": output_path, "duration": duration}
            
        except Exception as e:
            return {"success": False, "error": f"Error tạo video segment: {str(e)}"}
    
    def merge_segments(self, segment_paths, output_path, transitions=None):
        """Ghép nhiều segment thành video hoàn chỉnh"""
        try:
            # Tạo file list cho ffmpeg concat
            list_file = os.path.join(self.temp_dir, "segments_list.txt")
            with open(list_file, 'w') as f:
                for path in segment_paths:
                    f.write(f"file '{os.path.abspath(path)}'\n")
            
            # Ghép video
            if transitions and transitions.get('crossfade', False):
                # Ghép với hiệu ứng chuyển cảnh (phức tạp hơn)
                return self._merge_with_transitions(segment_paths, output_path, transitions)
            else:
                # Ghép đơn giản
                cmd = [
                    'ffmpeg', '-f', 'concat', '-safe', '0', 
                    '-i', list_file, '-c', 'copy', 
                    '-y', output_path
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True,
                                       stderr=subprocess.DEVNULL)  # Suppress FFmpeg stderr
                if result.returncode == 0:
                    return {"success": True, "path": output_path}
                else:
                    return {"success": False, "error": f"FFmpeg error (code: {result.returncode})"}
                    
        except Exception as e:
            return {"success": False, "error": f"Error ghép video: {str(e)}"}
    
    def _merge_with_transitions(self, segment_paths, output_path, transitions):
        """Ghép video với hiệu ứng chuyển cảnh"""
        try:
            # Tạo filter complex cho crossfade
            inputs = []
            for path in segment_paths:
                inputs.append(ffmpeg.input(path))
            
            # Áp dụng crossfade giữa các segment
            current = inputs[0]
            for i in range(1, len(inputs)):
                fade_duration = transitions.get('fade_duration', 0.5)
                current = ffmpeg.filter([current, inputs[i]], 'xfade', 
                                      transition='fade', duration=fade_duration)
            
            output = ffmpeg.output(current, output_path, vcodec='libx264', acodec='aac')
            ffmpeg.run(output, overwrite_output=True, quiet=True)
            
            return {"success": True, "path": output_path}
        except Exception as e:
            return {"success": False, "error": f"Error ghép với transitions: {str(e)}"}
    
    def add_background_music(self, video_path, music_path, output_path, music_volume=0.3):
        """Thêm nhạc nền vào video"""
        try:
            video_input = ffmpeg.input(video_path)
            music_input = ffmpeg.input(music_path)
            
            # Mix audio với volume thấp cho nhạc nền
            audio_mixed = ffmpeg.filter([video_input['a'], music_input], 'amix', 
                                      inputs=2, duration='first', 
                                      weights=f'1 {music_volume}')
            
            output = ffmpeg.output(video_input['v'], audio_mixed, output_path,
                                 vcodec='copy', acodec='aac')
            
            ffmpeg.run(output, overwrite_output=True, quiet=True)
            return {"success": True, "path": output_path}
        except Exception as e:
            return {"success": False, "error": f"Error thêm nhạc nền: {str(e)}"}
    
    def cleanup_temp_files(self):
        """Dọn dẹp file tạm"""
        try:
            import shutil
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": f"Error dọn dẹp: {str(e)}"} 
>>>>>>> Stashed changes
