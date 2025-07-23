# 🔐 HƯỚNG DẪN QUẢN LÝ LICENSE VOICE STUDIO

## 📋 TỔNG QUAN HỆ THỐNG

Voice Studio sử dụng hệ thống license management với:
- **Hardware binding** - Mỗi license gắn với thiết bị cụ thể
- **Trial mode** - Miễn phí với giới hạn 5 exports/ngày
- **Multiple plans** - Basic, Pro, Enterprise
- **Offline support** - Hoạt động offline tối đa 7 ngày
- **Admin API** - Quản lý license qua REST API

---

## 🚀 KHỞI ĐỘNG HỆ THỐNG

### 1. Start License Server
```bash
# Chuyển vào thư mục license server
cd license_server

# Khởi động server
python start_server.py

# Hoặc chạy trực tiếp
python server.py
```

**Server sẽ chạy tại**: `http://localhost:5000`

### 2. Kiểm tra Server Health
```bash
python admin.py health
```

**Kết quả thành công**:
```
✅ Server is healthy: running at 2024-06-25T10:30:00
```

---

## 👤 QUẢN LÝ TÀI KHOẢN

### 1. TẠO LICENSE MỚI

#### Tạo License Pro (Khuyến nghị)
```bash
python admin.py create \
  --email customer@example.com \
  --plan pro \
  --days 30 \
  --devices 2
```

#### Tạo License Enterprise
```bash
python admin.py create \
  --email enterprise@company.com \
  --plan enterprise \
  --days 365 \
  --devices 5
```

#### Tạo License Trial Extension
```bash
python admin.py create \
  --email trial@example.com \
  --plan basic \
  --days 7 \
  --devices 1
```

**Kết quả tạo thành công**:
```
✅ License created successfully!
   License Key: VS-8F7A2B9C-1E4D5F6G-7H8I9J0K
   Customer: customer@example.com
   Plan: pro
   Expires: 2024-07-25T10:30:00
   Max Devices: 2
   Features: ['export_unlimited', 'inner_voice', 'emotion_config', 'batch_processing']
```

### 2. XEM THÔNG TIN LICENSE

```bash
python admin.py status --key VS-8F7A2B9C-1E4D5F6G-7H8I9J0K
```

**Kết quả**:
```
✅ License Status:
   Key: VS-8F7A2B9C-1E4D5F6G-7H8I9J0K
   Customer: customer@example.com
   Plan: pro
   Status: active
   Created: 2024-06-25T10:30:00
   Expires: 2024-07-25T10:30:00
   Activations: 1/2
   Active Devices:
     1. Hardware: A1B2C3D4E5F6G7H8
        Activated: 2024-06-25T11:00:00
        Last Seen: 2024-06-25T14:30:00
   Features: ['export_unlimited', 'inner_voice', 'emotion_config', 'batch_processing']
```

### 3. TEST VERIFY LICENSE

```bash
python admin.py verify --key VS-8F7A2B9C-1E4D5F6G-7H8I9J0K
```

---

## ⏰ QUẢN LÝ THỜI GIAN

### 1. GIA HẠN LICENSE (Extend Days)

**Cách 1: Tạo license mới với thời gian dài hơn**
```bash
# Tạo license mới thay thế license cũ
python admin.py create \
  --email existing-customer@example.com \
  --plan pro \
  --days 60 \
  --devices 2
```

**Cách 2: Sử dụng Database trực tiếp**
```bash
# Kết nối database và update expiry_date
sqlite3 license_server/license_server.db

# Update expiry date (thêm 30 ngày)
UPDATE licenses 
SET expiry_date = datetime(expiry_date, '+30 days') 
WHERE license_key = 'VS-8F7A2B9C-1E4D5F6G-7H8I9J0K';

# Kiểm tra kết quả
SELECT license_key, expiry_date FROM licenses 
WHERE license_key = 'VS-8F7A2B9C-1E4D5F6G-7H8I9J0K';
```

### 2. SET NGÀY HẾT HẠN CỤ THỂ

```sql
-- Kết nối database
sqlite3 license_server/license_server.db

-- Set ngày hết hạn cụ thể (format: YYYY-MM-DDTHH:MM:SS)
UPDATE licenses 
SET expiry_date = '2024-12-31T23:59:59' 
WHERE license_key = 'VS-8F7A2B9C-1E4D5F6G-7H8I9J0K';
```

### 3. GIA HẠN HÀNG LOẠT

```sql
-- Gia hạn tất cả license Pro thêm 30 ngày
UPDATE licenses 
SET expiry_date = datetime(expiry_date, '+30 days') 
WHERE plan_type = 'pro' AND status = 'active';

-- Gia hạn theo email domain
UPDATE licenses 
SET expiry_date = datetime(expiry_date, '+90 days') 
WHERE customer_email LIKE '%@company.com' AND status = 'active';
```

---

## 🔄 RESET VÀ DEACTIVATE

### 1. RESET HARDWARE ACTIVATIONS

```sql
-- Kết nối database
sqlite3 license_server/license_server.db

-- Xóa tất cả activations của 1 license (cho phép activate lại)
DELETE FROM activations 
WHERE license_key = 'VS-8F7A2B9C-1E4D5F6G-7H8I9J0K';

-- Reset activation count
UPDATE licenses 
SET current_activations = 0 
WHERE license_key = 'VS-8F7A2B9C-1E4D5F6G-7H8I9J0K';
```

### 2. DEACTIVATE DEVICE CỤ THỂ

```sql
-- Deactivate 1 hardware ID cụ thể
UPDATE activations 
SET status = 'deactivated' 
WHERE license_key = 'VS-8F7A2B9C-1E4D5F6G-7H8I9J0K' 
  AND hardware_id = 'A1B2C3D4E5F6G7H8';

-- Giảm activation count
UPDATE licenses 
SET current_activations = current_activations - 1 
WHERE license_key = 'VS-8F7A2B9C-1E4D5F6G-7H8I9J0K';
```

### 3. SUSPEND LICENSE

```sql
-- Tạm dừng license (có thể kích hoạt lại)
UPDATE licenses 
SET status = 'suspended' 
WHERE license_key = 'VS-8F7A2B9C-1E4D5F6G-7H8I9J0K';

-- Kích hoạt lại
UPDATE licenses 
SET status = 'active' 
WHERE license_key = 'VS-8F7A2B9C-1E4D5F6G-7H8I9J0K';
```

---

## 🔑 QUẢN LÝ LICENSE KEY

### 1. TẠO DEMO LICENSES

```bash
# Tạo bộ demo licenses cho testing
python admin.py demo
```

**Kết quả**:
```
🎯 Creating demo licenses...

📝 Creating basic license...
✅ License created successfully!

📝 Creating pro license...
✅ License created successfully!

📝 Creating enterprise license...
✅ License created successfully!

🎉 Successfully created 3 demo licenses!

🔑 DEMO LICENSE KEYS:
   BASIC: VS-12345678-12345678-12345678
   PRO: VS-87654321-87654321-87654321
   ENTERPRISE: VS-ABCDEF01-ABCDEF01-ABCDEF01
```

### 2. TÌM KIẾM LICENSE

```sql
-- Tìm license theo email
SELECT * FROM licenses 
WHERE customer_email = 'customer@example.com';

-- Tìm license hết hạn
SELECT * FROM licenses 
WHERE datetime(expiry_date) < datetime('now');

-- Tìm license theo plan
SELECT * FROM licenses 
WHERE plan_type = 'pro' AND status = 'active';

-- Tìm license với nhiều activations
SELECT * FROM licenses 
WHERE current_activations >= max_activations;
```

### 3. THỐNG KÊ LICENSE

```sql
-- Thống kê theo plan
SELECT plan_type, COUNT(*) as count, 
       SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active
FROM licenses 
GROUP BY plan_type;

-- Thống kê activations
SELECT 
    l.plan_type,
    AVG(l.current_activations) as avg_activations,
    MAX(l.current_activations) as max_activations,
    COUNT(a.id) as total_devices
FROM licenses l 
LEFT JOIN activations a ON l.license_key = a.license_key 
GROUP BY l.plan_type;
```

---

## 🛠️ COMMANDS NÂNG CAO

### 1. BATCH OPERATIONS

#### Script tạo nhiều license
```bash
#!/bin/bash
# create_bulk_licenses.sh

emails=(
    "user1@company.com"
    "user2@company.com" 
    "user3@company.com"
)

for email in "${emails[@]}"; do
    echo "Creating license for $email..."
    python admin.py create \
        --email "$email" \
        --plan pro \
        --days 30 \
        --devices 2
    sleep 1
done
```

#### Script gia hạn hàng loạt
```python
# extend_licenses.py
import sqlite3
from datetime import datetime, timedelta

def extend_all_active_licenses(days=30):
    conn = sqlite3.connect('license_server/license_server.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE licenses 
        SET expiry_date = datetime(expiry_date, '+{} days')
        WHERE status = 'active'
    """.format(days))
    
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    print(f"✅ Extended {affected} active licenses by {days} days")

if __name__ == "__main__":
    extend_all_active_licenses(30)
```

### 2. MONITORING & ALERTS

#### Script kiểm tra license sắp hết hạn
```python
# check_expiring.py
import sqlite3
from datetime import datetime, timedelta

def check_expiring_licenses(days_warning=7):
    conn = sqlite3.connect('license_server/license_server.db')
    cursor = conn.cursor()
    
    warning_date = (datetime.now() + timedelta(days=days_warning)).isoformat()
    
    cursor.execute("""
        SELECT license_key, customer_email, plan_type, expiry_date
        FROM licenses 
        WHERE datetime(expiry_date) BETWEEN datetime('now') AND datetime(?)
        AND status = 'active'
        ORDER BY expiry_date
    """, (warning_date,))
    
    expiring = cursor.fetchall()
    conn.close()
    
    if expiring:
        print(f"⚠️  {len(expiring)} licenses expiring in next {days_warning} days:")
        for license_key, email, plan, expiry in expiring:
            print(f"   {email} ({plan}) - {license_key} expires {expiry}")
    else:
        print(f"✅ No licenses expiring in next {days_warning} days")

if __name__ == "__main__":
    check_expiring_licenses(7)
```

### 3. BACKUP & RESTORE

#### Backup Database
```bash
# Backup license database
cp license_server/license_server.db "license_backup_$(date +%Y%m%d_%H%M%S).db"

# Export to SQL
sqlite3 license_server/license_server.db .dump > license_backup.sql
```

#### Restore Database
```bash
# Restore from backup
cp license_backup_20240625_103000.db license_server/license_server.db

# Restore from SQL
sqlite3 license_server/license_server.db < license_backup.sql
```

---

## 📊 REPORTS & ANALYTICS

### 1. License Usage Report
```sql
-- Report tổng quan
SELECT 
    plan_type,
    COUNT(*) as total_licenses,
    SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active,
    SUM(CASE WHEN datetime(expiry_date) < datetime('now') THEN 1 ELSE 0 END) as expired,
    SUM(current_activations) as total_activations
FROM licenses 
GROUP BY plan_type;
```

### 2. Device Activity Report
```sql
-- Thiết bị hoạt động gần đây
SELECT 
    l.customer_email,
    l.plan_type,
    a.hardware_id,
    a.last_verified,
    datetime('now') - datetime(a.last_verified) as days_inactive
FROM licenses l
JOIN activations a ON l.license_key = a.license_key
WHERE a.status = 'active'
ORDER BY a.last_verified DESC;
```

---

## 🚨 XỬ LÝ SỰ CỐ

### 1. Customer mất License Key
```bash
# Tìm license theo email
sqlite3 license_server/license_server.db
SELECT license_key, plan_type, expiry_date 
FROM licenses 
WHERE customer_email = 'customer@example.com' 
AND status = 'active';
```

### 2. License không activate được
```bash
# Kiểm tra activations hiện tại
python admin.py status --key VS-XXXXXXXX-XXXXXXXX-XXXXXXXX

# Reset activations nếu cần
sqlite3 license_server/license_server.db
DELETE FROM activations WHERE license_key = 'VS-XXXXXXXX-XXXXXXXX-XXXXXXXX';
UPDATE licenses SET current_activations = 0 WHERE license_key = 'VS-XXXXXXXX-XXXXXXXX-XXXXXXXX';
```

### 3. Server không hoạt động
```bash
# Kiểm tra logs
tail -f license_server.log

# Restart server
cd license_server
python start_server.py

# Kiểm tra port
netstat -tulpn | grep :5000
```

---

## 📞 LIÊN HỆ HỖ TRỢ

Khi có vấn đề với license system:
1. **Kiểm tra server health**: `python admin.py health`
2. **Check database**: Verify data integrity
3. **Review logs**: Check verification_logs table
4. **Test với demo license**: `python admin.py demo`

**Emergency Commands**:
```bash
# Tạo license khẩn cấp
python admin.py create --email emergency@support.com --plan pro --days 7 --devices 1

# Backup database ngay lập tức
cp license_server/license_server.db emergency_backup.db
``` 