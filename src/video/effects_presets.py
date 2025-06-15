class EffectsPresets:
    """Các preset hiệu ứng có sẵn cho video"""
    
    @staticmethod
    def get_all_presets():
        """Lấy tất cả preset hiệu ứng"""
        return {
            "minimal": EffectsPresets.minimal(),
            "dynamic": EffectsPresets.dynamic(),
            "cinematic": EffectsPresets.cinematic(),
            "social_media": EffectsPresets.social_media(),
            "educational": EffectsPresets.educational()
        }
    
    @staticmethod
    def minimal():
        """Preset tối giản - không hiệu ứng"""
        return {
            "name": "Tối giản",
            "description": "Không hiệu ứng, chỉ hiển thị ảnh tĩnh",
            "zoom": False,
            "transitions": None,
            "zoom_factor": 1.0,
            "fade_duration": 0
        }
    
    @staticmethod
    def dynamic():
        """Preset năng động - zoom và chuyển cảnh"""
        return {
            "name": "Năng động",
            "description": "Zoom nhẹ và chuyển cảnh mượt mà",
            "zoom": True,
            "transitions": {"crossfade": True, "fade_duration": 0.5},
            "zoom_factor": 1.1,
            "fade_duration": 0.5
        }
    
    @staticmethod
    def cinematic():
        """Preset điện ảnh - zoom chậm, chuyển cảnh dài"""
        return {
            "name": "Điện ảnh",
            "description": "Zoom chậm, chuyển cảnh dài tạo cảm giác điện ảnh",
            "zoom": True,
            "transitions": {"crossfade": True, "fade_duration": 1.0},
            "zoom_factor": 1.2,
            "fade_duration": 1.0
        }
    
    @staticmethod
    def social_media():
        """Preset mạng xã hội - nhanh, bắt mắt"""
        return {
            "name": "Mạng xã hội",
            "description": "Hiệu ứng nhanh, bắt mắt cho TikTok, Instagram",
            "zoom": True,
            "transitions": {"crossfade": True, "fade_duration": 0.3},
            "zoom_factor": 1.15,
            "fade_duration": 0.3
        }
    
    @staticmethod
    def educational():
        """Preset giáo dục - ổn định, dễ theo dõi"""
        return {
            "name": "Giáo dục",
            "description": "Hiệu ứng nhẹ, ổn định, dễ theo dõi nội dung",
            "zoom": True,
            "transitions": {"crossfade": True, "fade_duration": 0.7},
            "zoom_factor": 1.05,
            "fade_duration": 0.7
        }
    
    @staticmethod
    def get_preset_by_name(name):
        """Lấy preset theo tên"""
        presets = EffectsPresets.get_all_presets()
        return presets.get(name, presets["dynamic"])  # Default to dynamic 