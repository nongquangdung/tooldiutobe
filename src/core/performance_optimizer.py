import os
import psutil
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class PerformanceOptimizer:
    """Tối ưu hóa hiệu suất cho việc xử lý video"""
    
    def __init__(self):
        self.cpu_count = os.cpu_count()
        self.memory_gb = psutil.virtual_memory().total / (1024**3)
        self.optimal_threads = self._calculate_optimal_threads()
    
    def _calculate_optimal_threads(self):
        """Tính số thread tối ưu dựa trên phần cứng"""
        # Sử dụng 70% CPU cores để tránh quá tải
        optimal = max(1, int(self.cpu_count * 0.7))
        
        # Giới hạn dựa trên RAM (mỗi thread cần ~500MB)
        max_by_memory = max(1, int(self.memory_gb / 0.5))
        
        return min(optimal, max_by_memory, 8)  # Tối đa 8 threads
    
    def get_system_info(self):
        """Lấy thông tin hệ thống"""
        return {
            "cpu_cores": self.cpu_count,
            "memory_gb": round(self.memory_gb, 1),
            "optimal_threads": self.optimal_threads,
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent
        }
    
    def parallel_image_generation(self, prompts, image_generator, progress_callback=None):
        """Tạo ảnh song song để tăng tốc"""
        results = []
        total = len(prompts)
        
        with ThreadPoolExecutor(max_workers=min(self.optimal_threads, total)) as executor:
            # Submit all tasks
            future_to_prompt = {
                executor.submit(image_generator.generate_image, prompt): prompt 
                for prompt in prompts
            }
            
            # Collect results
            for i, future in enumerate(as_completed(future_to_prompt)):
                prompt = future_to_prompt[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    if progress_callback:
                        progress_callback(int((i + 1) / total * 100), 
                                        f"Đã tạo ảnh {i + 1}/{total}")
                except Exception as e:
                    results.append({"success": False, "error": str(e)})
        
        return results
    
    def parallel_tts_generation(self, texts, tts_generator, progress_callback=None):
        """Tạo TTS song song để tăng tốc"""
        results = []
        total = len(texts)
        
        with ThreadPoolExecutor(max_workers=min(self.optimal_threads, total)) as executor:
            # Submit all tasks
            future_to_text = {
                executor.submit(tts_generator.generate_speech, text): text 
                for text in texts
            }
            
            # Collect results
            for i, future in enumerate(as_completed(future_to_text)):
                text = future_to_text[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    if progress_callback:
                        progress_callback(int((i + 1) / total * 100), 
                                        f"Đã tạo audio {i + 1}/{total}")
                except Exception as e:
                    results.append({"success": False, "error": str(e)})
        
        return results
    
    def optimize_video_settings(self, target_quality="medium"):
        """Tối ưu cài đặt video dựa trên phần cứng"""
        settings = {
            "low": {
                "resolution": "1280x720",
                "fps": 20,
                "bitrate": "1M",
                "preset": "fast"
            },
            "medium": {
                "resolution": "1920x1080", 
                "fps": 25,
                "bitrate": "2M",
                "preset": "medium"
            },
            "high": {
                "resolution": "1920x1080",
                "fps": 30,
                "bitrate": "4M", 
                "preset": "slow"
            }
        }
        
        # Điều chỉnh dựa trên phần cứng
        if self.memory_gb < 4:
            target_quality = "low"
        elif self.memory_gb < 8:
            target_quality = "medium"
        
        return settings.get(target_quality, settings["medium"])
    
    def monitor_resources(self, duration=60):
        """Giám sát tài nguyên hệ thống"""
        start_time = time.time()
        stats = {
            "cpu_usage": [],
            "memory_usage": [],
            "timestamps": []
        }
        
        while time.time() - start_time < duration:
            stats["cpu_usage"].append(psutil.cpu_percent(interval=1))
            stats["memory_usage"].append(psutil.virtual_memory().percent)
            stats["timestamps"].append(time.time() - start_time)
            time.sleep(1)
        
        return {
            "avg_cpu": sum(stats["cpu_usage"]) / len(stats["cpu_usage"]),
            "max_cpu": max(stats["cpu_usage"]),
            "avg_memory": sum(stats["memory_usage"]) / len(stats["memory_usage"]),
            "max_memory": max(stats["memory_usage"]),
            "stats": stats
        }
    
    def cleanup_temp_files(self, directories):
        """Dọn dẹp file tạm để giải phóng dung lượng"""
        cleaned_size = 0
        cleaned_files = 0
        
        for directory in directories:
            if os.path.exists(directory):
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            file_size = os.path.getsize(file_path)
                            os.remove(file_path)
                            cleaned_size += file_size
                            cleaned_files += 1
                        except Exception:
                            continue
        
        return {
            "cleaned_files": cleaned_files,
            "cleaned_size_mb": round(cleaned_size / (1024*1024), 2)
        }
    
    def estimate_processing_time(self, num_images, num_audio_segments, video_length_minutes):
        """Ước tính thời gian xử lý"""
        # Thời gian ước tính dựa trên phần cứng (giây)
        base_times = {
            "image_generation": 10,  # 10s per image
            "tts_generation": 5,     # 5s per audio segment  
            "video_composition": 30  # 30s per minute of video
        }
        
        # Điều chỉnh dựa trên số thread
        thread_factor = max(0.3, 1 / self.optimal_threads)
        
        estimated_time = (
            (num_images * base_times["image_generation"] * thread_factor) +
            (num_audio_segments * base_times["tts_generation"] * thread_factor) +
            (video_length_minutes * base_times["video_composition"])
        )
        
        return {
            "estimated_seconds": int(estimated_time),
            "estimated_minutes": round(estimated_time / 60, 1),
            "thread_factor": thread_factor,
            "system_performance": "high" if self.optimal_threads >= 4 else "medium" if self.optimal_threads >= 2 else "low"
        } 