# 🚀 HEROKU DEPLOYMENT - BƯỚC CHO BƯỚC

## Bước 1: Cài đặt Heroku CLI (5 phút)

### Tải và cài đặt:
1. Vào https://devcenter.heroku.com/articles/heroku-cli
2. Download "64-bit Installer" cho Windows
3. Chạy file .exe và install như bình thường
4. Restart PowerShell sau khi cài xong

### Kiểm tra cài đặt:
```bash
heroku --version
# Sẽ hiển thị: heroku/8.x.x win32-x64 node-v18.x.x
```

---

## Bước 2: Login Heroku (2 phút)

```bash
heroku login
# Sẽ mở browser để login, đăng ký tài khoản miễn phí nếu chưa có
```

---

## Bước 3: Chuẩn bị files (đã sẵn sàng ✅)

Files cần thiết đã có:
```
license_server/
├── server.py          ✅ 
├── requirements.txt   ✅ 
├── Procfile          ✅ 
├── runtime.txt       ✅ 
└── admin.py          ✅ 
```

---

## Bước 4: Deploy lên Heroku (10 phút)

```bash
# 1. Vào thư mục license_server
cd license_server

# 2. Khởi tạo git repository
git init

# 3. Add tất cả files
git add .

# 4. Commit files
git commit -m "Deploy Voice Studio License Server to Heroku"

# 5. Tạo Heroku app (thay "my-voice-studio" bằng tên bạn muốn)
heroku create my-voice-studio-license

# 6. Deploy!
git push heroku main

# 7. Tạo demo licenses
heroku run "python admin.py demo"

# 8. Kiểm tra app
heroku open
```

---

## Bước 5: Test deployment (5 phút)

```bash
# Lấy URL của app
heroku apps:info

# Test health check (thay URL bằng app của bạn)
curl https://my-voice-studio-license.herokuapp.com/health
```

Kết quả thành công sẽ như:
```json
{"status":"healthy","timestamp":"2025-06-25T...","version":"1.0.0"}
```

---

## Bước 6: Cập nhật client code (3 phút)

```bash
# Quay về thư mục gốc
cd ..

# Cập nhật URL trong client (thay bằng URL app của bạn)
python update_client_url.py https://my-voice-studio-license.herokuapp.com
```

---

## Bước 7: Test hoàn chỉnh (5 phút)

```bash
# Test license system
python simple_license_demo.py

# Chạy Voice Studio với cloud license
python src/main.py
```

---

## 🎉 THÀNH CÔNG!

App của bạn sẽ có URL như: `https://your-app-name.herokuapp.com`

### Demo license keys để test:
```
BASIC: VS-FDJCRLSW-DJ0NY94X-CWAJQOSY
PRO: VS-MKDERGNT-7QZ0P9LG-VLRUN2H9
ENTERPRISE: VS-58FE6CRJ-8GIK1NMF-KY7LZQAH
```

### Quản lý app:
```bash
heroku logs --tail           # Xem logs real-time
heroku ps                    # Check app status
heroku run bash              # SSH vào app
heroku restart               # Restart app
```

---

## 💰 Chi phí Heroku:

- **Free Tier:** 750 hours/month miễn phí
- **Sleep:** App ngủ sau 30 phút không dùng
- **Wake up:** Tự động thức khi có request (mất 10-30 giây)
- **Upgrade:** $7/month để không sleep

---

## 🚀 Next Steps:

1. **Test license activation** trong Voice Studio
2. **Tạo website bán license** 
3. **Setup Stripe/PayPal** cho payment
4. **Start marketing** và kiếm tiền! 💰

**🎊 Chúc mừng! Bạn đã có license server trên cloud rồi!** 