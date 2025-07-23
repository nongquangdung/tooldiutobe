#!/usr/bin/env python3
"""
🧹 PROJECT CLEANUP SCRIPT
========================

Script tự động dọn dẹp project để giảm dung lượng từ 20GB xuống dưới 500MB:
1. Xóa virtual environments (GIỮ LẠI .venv_clean)
2. Xóa __pycache__ folders và .pyc files  
3. Xóa test scripts không cần thiết
4. Xóa output files và temporary files
5. Xóa node_modules
6. Dọn dẹp các file logs và debug files

CẢNH BÁO: Script này sẽ xóa nhiều file! Hãy backup trước khi chạy.
"""

import os
import shutil
import glob
from pathlib import Path

def get_folder_size(path):
    """Tính dung lượng folder (MB)"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total_size += os.path.getsize(fp)
    except:
        pass
    return total_size / (1024 * 1024)  # Convert to MB

def safe_remove(path):
    """Xóa file/folder an toàn"""
    try:
        if os.path.isfile(path):
            os.remove(path)
            return True
        elif os.path.isdir(path):
            shutil.rmtree(path)
            return True
    except Exception as e:
        print(f"❌ Không thể xóa {path}: {e}")
        return False
    return False

def cleanup_virtual_environments():
    """Xóa virtual environments - Chiếm nhiều dung lượng nhất"""
    print("\n🎯 BƯỚC 1: Dọn dẹp Virtual Environments")
    print("ℹ️  GIỮ LẠI .venv_clean trong thư mục tooldiutobe")
    
    venv_folders = [
        ".venv",
        "backend/.venv", 
        "venv",
        "__pycache__"
    ]
    
    total_saved = 0
    for venv in venv_folders:
        if os.path.exists(venv):
            size_mb = get_folder_size(venv)
            if safe_remove(venv):
                print(f"✅ Đã xóa {venv} (tiết kiệm {size_mb:.1f}MB)")
                total_saved += size_mb
            else:
                print(f"❌ Không thể xóa {venv}")
    
    # Thông báo về .venv_clean được giữ lại
    if os.path.exists(".venv_clean"):
        size_mb = get_folder_size(".venv_clean")
        print(f"💾 GIỮ LẠI .venv_clean ({size_mb:.1f}MB)")
    
    print(f"💾 Tổng tiết kiệm từ virtual envs: {total_saved:.1f}MB")
    return total_saved

def cleanup_pycache():
    """Xóa tất cả __pycache__ folders (trừ trong .venv_clean)"""
    print("\n🎯 BƯỚC 2: Dọn dẹp __pycache__ folders")
    
    count = 0
    total_saved = 0
    
    # Tìm tất cả __pycache__ folders trong project
    for root, dirs, files in os.walk("."):
        # Skip .venv_clean và các virtual environments khác
        if any(venv in root for venv in [".venv_clean", ".venv", "venv", "node_modules"]):
            continue
            
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            size_mb = get_folder_size(pycache_path)
            if safe_remove(pycache_path):
                count += 1
                total_saved += size_mb
    
    # Xóa .pyc files riêng lẻ (trừ trong .venv_clean)
    pyc_files = glob.glob("**/*.pyc", recursive=True)
    for pyc_file in pyc_files:
        if ".venv_clean" not in pyc_file:
            if safe_remove(pyc_file):
                count += 1
    
    print(f"✅ Đã xóa {count} __pycache__ folders và .pyc files (tiết kiệm {total_saved:.1f}MB)")
    return total_saved

def cleanup_test_files():
    """Xóa test scripts không cần thiết"""
    print("\n🎯 BƯỚC 3: Dọn dẹp Test Scripts")
    
    test_patterns = [
        "test_*.py",
        "debug_*.py", 
        "demo_*.py",
        "*_test.py",
        "ultimate_*.py",
        "improved_*.py",
        "final_*.py",
        "quick_*.py"
    ]
    
    # Exceptions - keep important files
    keep_files = [
        "test_script_inner_voice.py",  # Important test for inner voice
    ]
    
    count = 0
    total_saved = 0
    
    for pattern in test_patterns:
        files = glob.glob(pattern)
        for file in files:
            if file not in keep_files:
                if os.path.exists(file):
                    size_mb = os.path.getsize(file) / (1024 * 1024)
                    if safe_remove(file):
                        count += 1
                        total_saved += size_mb
    
    print(f"✅ Đã xóa {count} test scripts (tiết kiệm {total_saved:.1f}MB)")
    return total_saved

def cleanup_output_files():
    """Xóa output files và temporary files"""
    print("\n🎯 BƯỚC 4: Dọn dẹp Output Files")
    
    output_folders = [
        "voice_studio_output",
        "backend/voice_studio_output", 
        "test_output",
        "test_extended_output",
        "test_script_output",
        "outputs",
        "temp_video"
    ]
    
    output_patterns = [
        "*.mp3",
        "*.wav", 
        "*.mp4",
        "*.avi"
    ]
    
    # Log files to remove
    log_patterns = [
        "*.log",
        "debug_*.txt",
        "generate_log.txt",
        "run.log",
        "backend.log",
        "ffmpeg_errors.log"
    ]
    
    total_saved = 0
    count = 0
    
    # Xóa output folders
    for folder in output_folders:
        if os.path.exists(folder):
            size_mb = get_folder_size(folder)
            if safe_remove(folder):
                print(f"✅ Đã xóa folder {folder} (tiết kiệm {size_mb:.1f}MB)")
                total_saved += size_mb
                count += 1
    
    # Xóa scattered output files ở root
    for pattern in output_patterns + log_patterns:
        files = glob.glob(pattern)
        for file in files:
            # Skip important files
            if file in ["requirements.txt", "README.md", "config.env"]:
                continue
            if os.path.exists(file):
                size_mb = os.path.getsize(file) / (1024 * 1024)
                if safe_remove(file):
                    count += 1
                    total_saved += size_mb
    
    print(f"✅ Đã xóa {count} output files (tiết kiệm {total_saved:.1f}MB)")
    return total_saved

def cleanup_node_modules():
    """Xóa node_modules folders"""
    print("\n🎯 BƯỚC 5: Dọn dẹp Node Modules")
    
    total_saved = 0
    count = 0
    
    # Tìm tất cả node_modules
    for root, dirs, files in os.walk("."):
        # Skip .venv_clean
        if ".venv_clean" in root:
            continue
            
        if "node_modules" in dirs:
            node_modules_path = os.path.join(root, "node_modules")
            size_mb = get_folder_size(node_modules_path)
            if safe_remove(node_modules_path):
                print(f"✅ Đã xóa {node_modules_path} (tiết kiệm {size_mb:.1f}MB)")
                total_saved += size_mb
                count += 1
    
    print(f"✅ Đã xóa {count} node_modules folders (tiết kiệm {total_saved:.1f}MB)")
    return total_saved

def cleanup_documentation_files():
    """Xóa các file documentation thừa thãi"""
    print("\n🎯 BƯỚC 6: Dọn dẹp Documentation Files")
    
    # Patterns cho documentation files thừa thãi
    doc_patterns = [
        "*_SUMMARY.md",
        "*_GUIDE.md", 
        "*_REPORT.md",
        "*_ANALYSIS.md",
        "BÁO_CÁO_*.md",
        "HƯỚNG_DẪN_*.md",
        "*_ROADMAP.md",
        "*_TROUBLESHOOTING.md",
        "*_IMPLEMENTATION_*.md",
        "*_INTEGRATION_*.md"
    ]
    
    # Keep important docs
    keep_docs = [
        "README.md",
        "CLAUDE.md",  # Project instructions
        "ROADMAP.md"   # Main roadmap
    ]
    
    count = 0
    total_saved = 0
    
    for pattern in doc_patterns:
        files = glob.glob(pattern)
        for file in files:
            if file not in keep_docs and os.path.exists(file):
                size_mb = os.path.getsize(file) / (1024 * 1024)
                if safe_remove(file):
                    count += 1
                    total_saved += size_mb
    
    print(f"✅ Đã xóa {count} documentation files (tiết kiệm {total_saved:.1f}MB)")
    return total_saved

def cleanup_config_backups():
    """Xóa config backups và temporary configs"""
    print("\n🎯 BƯỚC 7: Dọn dẹp Config Backups")
    
    backup_patterns = [
        "*.backup",
        "*.bak",
        "*_backup_*.json",
        "*.json.backup",
        "*emotion_integration_test_results_*.json",
        "*chatterbox_integration_test_report_*.json",
        "*phase*_achievements_report_*.json",
        "emotion_config_*.json",
        "unified_emotion_migration_report.json"
    ]
    
    count = 0
    total_saved = 0
    
    for pattern in backup_patterns:
        files = glob.glob(pattern, recursive=True)
        for file in files:
            if os.path.exists(file):
                size_mb = os.path.getsize(file) / (1024 * 1024)
                if safe_remove(file):
                    count += 1
                    total_saved += size_mb
    
    print(f"✅ Đã xóa {count} backup files (tiết kiệm {total_saved:.1f}MB)")
    return total_saved

def cleanup_database_files():
    """Xóa database files thừa thãi"""
    print("\n🎯 BƯỚC 8: Dọn dẹp Database Files")
    
    db_files = [
        "voice_studio_analytics.db",
        "voice_studio_license.db", 
        "backend/voice_studio_analytics.db",
        "backend/voice_studio_license.db"
    ]
    
    count = 0
    total_saved = 0
    
    for db_file in db_files:
        if os.path.exists(db_file):
            size_mb = os.path.getsize(db_file) / (1024 * 1024)
            if safe_remove(db_file):
                print(f"✅ Đã xóa {db_file} (tiết kiệm {size_mb:.1f}MB)")
                count += 1
                total_saved += size_mb
    
    print(f"✅ Đã xóa {count} database files (tiết kiệm {total_saved:.1f}MB)")
    return total_saved

def main():
    """Main cleanup function"""
    print("🧹 BẮT ĐẦU DỌN DẸP PROJECT")
    print("=" * 50)
    print("ℹ️  GIỮ LẠI .venv_clean trong thư mục tooldiutobe")
    
    # Tính dung lượng trước khi cleanup
    initial_size = get_folder_size(".")
    print(f"📊 Dung lượng hiện tại: {initial_size:.1f}MB")
    
    total_saved = 0
    
    # Thực hiện cleanup theo thứ tự ưu tiên
    total_saved += cleanup_virtual_environments()  # Lớn nhất (trừ .venv_clean)
    total_saved += cleanup_node_modules()          # Lớn thứ 2
    total_saved += cleanup_output_files()          # Audio/video files
    total_saved += cleanup_pycache()               # Nhiều files nhỏ
    total_saved += cleanup_test_files()            # Test scripts
    total_saved += cleanup_documentation_files()   # Docs thừa
    total_saved += cleanup_config_backups()        # Backup files
    total_saved += cleanup_database_files()        # DB files
    
    # Tính dung lượng sau cleanup
    final_size = get_folder_size(".")
    actual_saved = initial_size - final_size
    
    print("\n" + "=" * 50)
    print("🎉 HOÀN THÀNH DỌN DẸP!")
    print(f"📊 Dung lượng trước: {initial_size:.1f}MB")
    print(f"📊 Dung lượng sau: {final_size:.1f}MB")
    print(f"💾 Tiết kiệm thực tế: {actual_saved:.1f}MB")
    print(f"📉 Giảm {(actual_saved/initial_size)*100:.1f}% dung lượng")
    
    if final_size < 500:
        print("✅ Thành công! Dung lượng đã xuống dưới 500MB")
    else:
        print("⚠️  Cần dọn dẹp thêm để đạt mục tiêu dưới 500MB")
    
    print("\n📝 GHI CHÚ:")
    print("- .venv_clean đã được giữ lại")
    print("- Chạy 'npm install' trong folder web/ để cài lại node modules")
    print("- Các model AI sẽ được tải về lại khi cần thiết")

if __name__ == "__main__":
    # Confirm before cleanup
    print("⚠️  CẢNH BÁO: Script này sẽ xóa nhiều file để giảm dung lượng!")
    print("✅ .venv_clean sẽ được GIỮ LẠI")
    print("Hãy backup project trước khi tiếp tục.")
    
    confirm = input("Bạn có muốn tiếp tục? (y/N): ").lower()
    if confirm in ['y', 'yes']:
        main()
    else:
        print("❌ Hủy bỏ cleanup.")