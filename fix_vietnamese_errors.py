#!/usr/bin/env python3
"""
Fix Vietnamese error messages that cause Unicode encoding issues
"""

import os
import re

# Vietnamese error message replacements
VIETNAMESE_REPLACEMENTS = {
    'Lỗi': 'Error',
    'Lỗi tải project': 'Error loading project',
    'Lỗi lưu project': 'Error saving project', 
    'Lỗi xóa project': 'Error deleting project',
    'Lỗi tạo ảnh': 'Error creating image',
    'Lỗi tải ảnh': 'Error loading image',
    'Lỗi resize ảnh': 'Error resizing image',
    'Lỗi kiểm tra ảnh': 'Error checking image',
    'Lỗi OpenAI': 'OpenAI error',
    'Lỗi Claude': 'Claude error',
    'Lỗi DeepSeek': 'DeepSeek error',
    'Lỗi ElevenLabs TTS': 'ElevenLabs TTS error',
    'Lỗi Google TTS': 'Google TTS error',
    'Lỗi Google TTS Free': 'Google TTS Free error',
    'Lỗi lấy danh sách giọng': 'Error getting voice list',
    'Lỗi tạo audio': 'Error creating audio',
    'Lỗi ghép audio': 'Error merging audio',
    'Lỗi ghép segment': 'Error merging segment',
    'Lỗi tạo file audio cuối cùng': 'Error creating final audio file',
    'Lỗi tạo audio cho': 'Error creating audio for',
    'Lỗi tạo audio chunk': 'Error creating audio chunk',
    'Lỗi preview': 'Preview error',
    'Lỗi cập nhật': 'Update error',
    'Lỗi xử lý preview': 'Preview processing error',
    'Lỗi tạo preview thật cho': 'Error creating real preview for',
    'Lỗi xóa emotion': 'Error deleting emotion',
    'Lỗi export': 'Export error',
    'Lỗi import': 'Import error',
    'Lỗi thống kê': 'Statistics error',
    'Lỗi reset': 'Reset error',
    'Lỗi reset all': 'Reset all error',
    'Lỗi Export': 'Export Error',
    'Lỗi Import': 'Import Error',
    'Lỗi Reset': 'Reset Error',
    'Lỗi Reset All': 'Reset All Error',
    'Lỗi xử lý param change cho': 'Error processing param change for',
    'Lỗi tạo ảnh đoạn': 'Error creating segment image',
    'Lỗi tạo giọng đoạn': 'Error creating segment voice',
    'Lỗi tạo video đoạn': 'Error creating segment video',
    'Lỗi ghép video': 'Error merging video',
    'Lỗi pipeline': 'Pipeline error',
    'Lỗi tạo lại segment': 'Error recreating segment',
    'Lỗi thêm nhạc nền': 'Error adding background music',
    'Lỗi xử lý ảnh đoạn': 'Error processing segment image',
    'Lỗi pipeline với ảnh thủ công': 'Pipeline error with manual images',
    'Lỗi tạo video segment': 'Error creating video segment',
    'Lỗi ghép với transitions': 'Error merging with transitions',
    'Lỗi dọn dẹp': 'Cleanup error',
    'Lỗi khi import files': 'Error importing files',
    'Lỗi load Emotion Config': 'Error loading Emotion Config',
    'Lỗi load License tab': 'Error loading License tab',
    'Lỗi": "Vui lòng nhập prompt': 'Error": "Please enter prompt',
    'Lỗi": "Vui lòng chọn thư mục chứa ảnh': 'Error": "Please select image folder',
    'Lỗi": "Vui lòng chọn project': 'Error": "Please select project',
    'Lỗi": "Không thể tạo video': 'Error": "Cannot create video',
    'Lỗi": "Không thể xóa': 'Error": "Cannot delete',
    'Lỗi": "Không thể lưu cài đặt': 'Error": "Cannot save settings',
    'Lỗi load cài đặt': 'Error loading settings',
    'Lỗi": "Không thể tạo câu chuyện': 'Error": "Cannot create story',
    'Lỗi tạo câu chuyện': 'Story creation error',
    'Lỗi": "Lỗi không xác định': 'Error": "Unknown error',
    'Lỗi": "Không thể copy': 'Error": "Cannot copy',
    'Lỗi": "Không thể lưu file': 'Error": "Cannot save file',
    'Lỗi": "Lỗi tạo audio': 'Error": "Audio creation error',
    'Lỗi tạo audio': 'Audio creation error',
    'Lỗi": "Không thể lấy thông tin device': 'Error": "Cannot get device info',
    'Lỗi": "Không thể xóa cache': 'Error": "Cannot clear cache',
    'Lỗi": "File JSON không đúng format': 'Error": "JSON file wrong format',
    'Lỗi": "Không thể đọc file': 'Error": "Cannot read file',
    'Lỗi": "JSON script không đúng format': 'Error": "JSON script wrong format',
    'Lỗi JSON': 'JSON Error',
    'Lỗi": "JSON không hợp lệ': 'Error": "Invalid JSON',
    'Lỗi": "Không thể parse script': 'Error": "Cannot parse script',
    'Lỗi": "Không thể cập nhật overview': 'Error": "Cannot update overview',
    'Lỗi Preview': 'Preview Error',
    'Lỗi Critical': 'Critical Error',
    'Lỗi": "Không thể tạo preview Chatterbox TTS': 'Error": "Cannot create Chatterbox TTS preview',
    'Lỗi preview voice': 'Voice preview error',
    'Lỗi": "Lỗi tạo voice': 'Error": "Voice creation error',
    'Lỗi tạo voice': 'Voice creation error',
    'Lỗi": "Force merge thất bại': 'Error": "Force merge failed',
    'Lỗi": "Lỗi khi force merge': 'Error": "Error during force merge',
    'Lỗi": "Không thể force merge files': 'Error": "Cannot force merge files',
    'Lỗi force merge': 'Force merge error',
    'Lỗi": "Lỗi force merge': 'Error": "Force merge error',
    'Lỗi": "Không thể tạo preview': 'Error": "Cannot create preview',
    'Lỗi Voice Clone Setup': 'Voice Clone Setup Error',
    'Lỗi": "Chunk size phải là số': 'Error": "Chunk size must be number',
    'Lỗi": "Không thể chia đoạn nội dung': 'Error": "Cannot split content',
}

def fix_vietnamese_in_file(file_path):
    """Fix Vietnamese error messages in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        replacements_made = 0
        
        # Replace Vietnamese error messages
        for vietnamese, english in VIETNAMESE_REPLACEMENTS.items():
            if vietnamese in content:
                content = content.replace(vietnamese, english)
                replacements_made += 1
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return replacements_made
        
        return 0
        
    except Exception as e:
        print(f"[ERROR] Failed to process {file_path}: {e}")
        return 0

def main():
    """Main fix function"""
    print("VIETNAMESE ERROR MESSAGES FIX - Starting...")
    
    src_dir = os.path.join(os.getcwd(), 'src')
    if not os.path.exists(src_dir):
        print(f"[ERROR] Source directory not found: {src_dir}")
        return
    
    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"[INFO] Found {len(python_files)} Python files to check")
    
    total_replacements = 0
    files_modified = 0
    
    # Process each file
    for file_path in python_files:
        rel_path = os.path.relpath(file_path, src_dir)
        replacements = fix_vietnamese_in_file(file_path)
        
        if replacements > 0:
            print(f"[FIXED] {rel_path}: {replacements} replacements")
            total_replacements += replacements
            files_modified += 1
        else:
            print(f"[OK] {rel_path}: no changes needed")
    
    print(f"\n[SUMMARY]")
    print(f"Files processed: {len(python_files)}")
    print(f"Files modified: {files_modified}")
    print(f"Total replacements: {total_replacements}")
    
    if files_modified > 0:
        print(f"\n[SUCCESS] Vietnamese error messages fixed!")
    else:
        print(f"\n[INFO] No Vietnamese error messages found.")

if __name__ == "__main__":
    main()