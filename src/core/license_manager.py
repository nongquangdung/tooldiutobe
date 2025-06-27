import hashlib
import platform
import subprocess
import uuid
import requests
import json
import os
from datetime import datetime, timedelta
import sqlite3
from pathlib import Path

class LicenseManager:
    """
    Quản lý License cho Voice Studio
    - Kiểm tra license từ server hoặc offline
    - Hardware fingerprinting
    - Cache license để giảm call API
    - Trial mode và premium features
    """
    
    def __init__(self):
        self.license_server_url = "https://license.voicestudio.app"  # Đổi thành domain thực của bạn
        self.local_db_path = "voice_studio_license.db"
        self.hardware_id = None
        self.current_license = None
        self.init_local_db()
        
    def init_local_db(self):
        """Khởi tạo SQLite database để cache license"""
        try:
            conn = sqlite3.connect(self.local_db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS license_cache (
                    id INTEGER PRIMARY KEY,
                    license_key TEXT,
                    hardware_id TEXT,
                    expiry_date TEXT,
                    features TEXT,
                    last_verified TEXT,
                    status TEXT
                )
            ''')
            
            # Bảng để track export count
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS export_counter (
                    id INTEGER PRIMARY KEY,
                    date TEXT,
                    count INTEGER DEFAULT 0
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"License DB init error: {e}")

    def get_hardware_id(self):
        """Tạo unique hardware fingerprint từ nhiều nguồn"""
        if self.hardware_id:
            return self.hardware_id
            
        try:
            # Thu thập thông tin hardware
            system_info = []
            
            # CPU Info
            try:
                if platform.system() == "Windows":
                    cpu_info = subprocess.check_output("wmic cpu get ProcessorId", shell=True).decode().strip()
                    system_info.append(cpu_info.replace('ProcessorId', '').strip())
                else:
                    cpu_info = subprocess.check_output("cat /proc/cpuinfo | grep 'Serial'", shell=True).decode().strip()
                    system_info.append(cpu_info)
            except:
                system_info.append(platform.processor())
            
            # Motherboard UUID
            try:
                if platform.system() == "Windows":
                    mb_uuid = subprocess.check_output("wmic csproduct get UUID", shell=True).decode().strip()
                    system_info.append(mb_uuid.replace('UUID', '').strip())
                else:
                    mb_uuid = subprocess.check_output("sudo dmidecode -s system-uuid", shell=True).decode().strip()
                    system_info.append(mb_uuid)
            except:
                system_info.append(str(uuid.getnode()))
            
            # MAC Address
            system_info.append(str(uuid.getnode()))
            
            # System info
            system_info.extend([
                platform.system(),
                platform.machine(),
                platform.node()
            ])
            
            # Tạo hash từ tất cả thông tin
            combined = "|".join(filter(None, system_info))
            self.hardware_id = hashlib.sha256(combined.encode()).hexdigest()[:16]
            
        except Exception as e:
            # Fallback nếu không lấy được hardware info
            self.hardware_id = hashlib.sha256(f"{platform.node()}-{uuid.getnode()}".encode()).hexdigest()[:16]
            
        return self.hardware_id

    def verify_license_online(self, license_key):
        """Xác thực license với server"""
        try:
            payload = {
                "license_key": license_key,
                "hardware_id": self.get_hardware_id(),
                "app_version": "1.0.0",
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.license_server_url}/api/verify",
                json=payload,
                timeout=10,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "valid":
                    # Cache license vào local DB
                    self.cache_license(license_key, result)
                    return result
                else:
                    return {"status": "invalid", "reason": result.get("reason", "Unknown error")}
            else:
                return {"status": "server_error", "reason": f"HTTP {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            # Nếu không kết nối được server, check cache
            return self.verify_license_offline(license_key)
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def verify_license_offline(self, license_key):
        """Xác thực license từ cache khi offline"""
        try:
            conn = sqlite3.connect(self.local_db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM license_cache 
                WHERE license_key = ? AND hardware_id = ?
                ORDER BY last_verified DESC LIMIT 1
            ''', (license_key, self.get_hardware_id()))
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return {"status": "invalid", "reason": "License not found in cache"}
            
            # Kiểm tra expiry
            expiry_date = datetime.fromisoformat(row[3])
            if datetime.now() > expiry_date:
                return {"status": "expired", "reason": "License expired"}
            
            # Kiểm tra last verified (cho phép offline tối đa 7 ngày)
            last_verified = datetime.fromisoformat(row[6])
            if datetime.now() > last_verified + timedelta(days=7):
                return {"status": "offline_too_long", "reason": "Please connect to internet to verify license"}
            
            return {
                "status": "valid",
                "expiry_date": row[3],
                "features": json.loads(row[4]),
                "offline_mode": True
            }
            
        except Exception as e:
            return {"status": "error", "reason": f"Cache verification error: {e}"}

    def cache_license(self, license_key, license_data):
        """Cache license vào local database"""
        try:
            conn = sqlite3.connect(self.local_db_path)
            cursor = conn.cursor()
            
            # Xóa cache cũ của license này
            cursor.execute('DELETE FROM license_cache WHERE license_key = ?', (license_key,))
            
            # Thêm cache mới
            cursor.execute('''
                INSERT INTO license_cache 
                (license_key, hardware_id, expiry_date, features, last_verified, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                license_key,
                self.get_hardware_id(),
                license_data.get("expiry_date"),
                json.dumps(license_data.get("features", {})),
                datetime.now().isoformat(),
                license_data.get("status")
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"License cache error: {e}")

    def activate_license(self, license_key):
        """Kích hoạt license key"""
        result = self.verify_license_online(license_key)
        
        if result["status"] == "valid":
            self.current_license = result
            self.save_current_license(license_key)
            return True, "License activated successfully!"
        else:
            return False, f"Activation failed: {result.get('reason', 'Unknown error')}"

    def save_current_license(self, license_key):
        """Lưu license key hiện tại"""
        try:
            with open("current_license.key", "w") as f:
                f.write(license_key)
        except Exception as e:
            print(f"Save license error: {e}")

    def load_current_license(self):
        """Load license key đã lưu"""
        try:
            if os.path.exists("current_license.key"):
                with open("current_license.key", "r") as f:
                    license_key = f.read().strip()
                if license_key:
                    result = self.verify_license_online(license_key)
                    if result["status"] == "valid":
                        self.current_license = result
                        return True
            return False
        except Exception as e:
            print(f"Load license error: {e}")
            return False

    def is_feature_enabled(self, feature_name):
        """Kiểm tra tính năng có được bật không"""
        if not self.current_license:
            # Trial mode - chỉ cho phép một số tính năng cơ bản
            trial_features = ["basic_tts", "emotion_preview", "export_limit_5"]
            return feature_name in trial_features
        
        if self.current_license.get("status") != "valid":
            return False
        
        features = self.current_license.get("features", {})
        return features.get(feature_name, False)

    def get_license_info(self):
        """Lấy thông tin license hiện tại"""
        if not self.current_license:
            return {
                "status": "trial",
                "mode": "Trial Mode",
                "expires": "Limited features",
                "features": ["Basic TTS", "5 exports/day"]
            }
        
        return {
            "status": self.current_license.get("status"),
            "mode": "Premium" if self.current_license.get("status") == "valid" else "Trial",
            "expires": self.current_license.get("expiry_date", "Unknown"),
            "features": list(self.current_license.get("features", {}).keys()),
            "offline": self.current_license.get("offline_mode", False)
        }

    def deactivate_license(self):
        """Hủy kích hoạt license"""
        try:
            if os.path.exists("current_license.key"):
                os.remove("current_license.key")
            
            # Xóa cache
            conn = sqlite3.connect(self.local_db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM license_cache')
            conn.commit()
            conn.close()
            
            self.current_license = None
            return True
        except Exception as e:
            print(f"Deactivate error: {e}")
            return False

    def can_export(self):
        """Kiểm tra có thể export không (dựa trên license và limit)"""
        if self.is_feature_enabled("export_unlimited"):
            return True
        
        # Trial mode - giới hạn 5 exports/day
        if self.get_export_count_today() < 5:
            return True
        
        return False
    
    def get_export_count_today(self):
        """Lấy số lượng exports hôm nay"""
        try:
            today = datetime.now().date().isoformat()
            conn = sqlite3.connect(self.local_db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT count FROM export_counter WHERE date = ?', (today,))
            row = cursor.fetchone()
            conn.close()
            
            return row[0] if row else 0
        except Exception as e:
            print(f"Export count error: {e}")
            return 0
    
    def increment_export_count(self):
        """Tăng export count cho hôm nay"""
        try:
            today = datetime.now().date().isoformat()
            conn = sqlite3.connect(self.local_db_path)
            cursor = conn.cursor()
            
            # Check nếu đã có record hôm nay
            cursor.execute('SELECT count FROM export_counter WHERE date = ?', (today,))
            row = cursor.fetchone()
            
            if row:
                # Update count
                cursor.execute('UPDATE export_counter SET count = count + 1 WHERE date = ?', (today,))
            else:
                # Insert new record
                cursor.execute('INSERT INTO export_counter (date, count) VALUES (?, 1)', (today,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Increment export error: {e}")
            return False

# Singleton instance
license_manager = LicenseManager() 