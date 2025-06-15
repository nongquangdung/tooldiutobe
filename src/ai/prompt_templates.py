class PromptTemplates:
    """Gợi ý prompt mẫu cho các thể loại video"""
    
    @staticmethod
    def get_all_categories():
        """Lấy tất cả danh mục prompt"""
        return {
            "travel": PromptTemplates.travel_prompts(),
            "education": PromptTemplates.education_prompts(),
            "business": PromptTemplates.business_prompts(),
            "lifestyle": PromptTemplates.lifestyle_prompts(),
            "technology": PromptTemplates.technology_prompts(),
            "food": PromptTemplates.food_prompts(),
            "story": PromptTemplates.story_prompts()
        }
    
    @staticmethod
    def travel_prompts():
        """Prompt mẫu cho video du lịch"""
        return {
            "category": "Du lịch",
            "prompts": [
                "Tạo video giới thiệu 5 điểm đến đẹp nhất Việt Nam với cảnh quan thiên nhiên tuyệt vời",
                "Hướng dẫn du lịch bụi Đà Lạt trong 3 ngày với ngân sách tiết kiệm",
                "Khám phá ẩm thực đường phố Sài Gòn qua 5 món ăn đặc trưng",
                "Top 10 bãi biển đẹp nhất miền Trung Việt Nam cho kỳ nghỉ hè",
                "Trải nghiệm văn hóa dân tộc thiểu số ở Sapa và Mù Cang Chải"
            ]
        }
    
    @staticmethod
    def education_prompts():
        """Prompt mẫu cho video giáo dục"""
        return {
            "category": "Giáo dục",
            "prompts": [
                "Giải thích cách hoạt động của trí tuệ nhân tạo một cách đơn giản cho người mới bắt đầu",
                "Hướng dẫn học tiếng Anh hiệu quả với 5 phương pháp khoa học",
                "Lịch sử hình thành và phát triển của Internet từ 1960 đến nay",
                "Cách quản lý thời gian hiệu quả cho học sinh, sinh viên",
                "Giới thiệu 7 kỳ quan thế giới cổ đại và câu chuyện lịch sử"
            ]
        }
    
    @staticmethod
    def business_prompts():
        """Prompt mẫu cho video kinh doanh"""
        return {
            "category": "Kinh doanh",
            "prompts": [
                "5 bước khởi nghiệp thành công cho người trẻ với vốn ít",
                "Cách xây dựng thương hiệu cá nhân trên mạng xã hội",
                "Chiến lược marketing online hiệu quả cho doanh nghiệp nhỏ",
                "Kỹ năng đàm phán và thuyết phục trong kinh doanh",
                "Xu hướng công nghệ sẽ thay đổi thế giới kinh doanh trong 5 năm tới"
            ]
        }
    
    @staticmethod
    def lifestyle_prompts():
        """Prompt mẫu cho video lối sống"""
        return {
            "category": "Lối sống",
            "prompts": [
                "Thói quen buổi sáng của những người thành công",
                "Cách trang trí phòng ngủ nhỏ trở nên rộng rãi và đẹp mắt",
                "5 bài tập yoga đơn giản giúp giảm stress sau ngày làm việc",
                "Hướng dẫn nấu 3 món ăn healthy cho người bận rộn",
                "Cách sống tối giản và tìm thấy hạnh phúc trong cuộc sống đơn giản"
            ]
        }
    
    @staticmethod
    def technology_prompts():
        """Prompt mẫu cho video công nghệ"""
        return {
            "category": "Công nghệ",
            "prompts": [
                "So sánh iPhone 15 vs Samsung Galaxy S24: Nên chọn máy nào?",
                "Cách bảo mật thông tin cá nhân trên Internet an toàn",
                "Giới thiệu ChatGPT và cách sử dụng AI trong công việc hàng ngày",
                "Xu hướng công nghệ 2024: VR, AR, và Metaverse",
                "Hướng dẫn chọn laptop phù hợp cho học tập và làm việc"
            ]
        }
    
    @staticmethod
    def food_prompts():
        """Prompt mẫu cho video ẩm thực"""
        return {
            "category": "Ẩm thực",
            "prompts": [
                "Cách làm bánh mì Việt Nam chuẩn vị tại nhà",
                "5 món ăn vặt Hàn Quốc dễ làm cho bạn trẻ",
                "Bí quyết nấu phở bò ngon như hàng quán",
                "Hướng dẫn làm bánh ngọt không cần lò nướng",
                "Top 10 món ăn đặc sản miền Bắc phải thử một lần"
            ]
        }
    
    @staticmethod
    def story_prompts():
        """Prompt mẫu cho video kể chuyện"""
        return {
            "category": "Kể chuyện",
            "prompts": [
                "Câu chuyện cảm động về tình mẫu tử qua bức thư của người mẹ",
                "Hành trình vượt khó của một sinh viên nghèo trở thành CEO",
                "Truyền thuyết về hồ Gươm và câu chuyện lịch sử Việt Nam",
                "Câu chuyện tình yêu xuyên thời gian qua 4 thế hệ",
                "Những bài học cuộc sống từ câu chuyện của người thành công"
            ]
        }
    
    @staticmethod
    def get_random_prompt(category=None):
        """Lấy prompt ngẫu nhiên từ danh mục"""
        import random
        categories = PromptTemplates.get_all_categories()
        
        if category and category in categories:
            return random.choice(categories[category]["prompts"])
        else:
            # Lấy ngẫu nhiên từ tất cả danh mục
            all_prompts = []
            for cat_data in categories.values():
                all_prompts.extend(cat_data["prompts"])
            return random.choice(all_prompts)
    
    @staticmethod
    def search_prompts(keyword):
        """Tìm kiếm prompt theo từ khóa"""
        results = []
        categories = PromptTemplates.get_all_categories()
        
        for cat_name, cat_data in categories.items():
            for prompt in cat_data["prompts"]:
                if keyword.lower() in prompt.lower():
                    results.append({
                        "category": cat_data["category"],
                        "prompt": prompt
                    })
        
        return results 