# Kế hoạch Phát triển Giao diện Web - Voice Studio V2

Mục tiêu là hoàn thiện các tính năng cho giao diện web hiện tại, kế thừa từ ứng dụng PC, dựa trên 5 tab chính đã có.

---

### **Thứ tự ưu tiên triển khai:**

1.  **Tab Emotions:** Hoàn thiện chức năng CRUD (Create, Read, Update, Delete) cho cảm xúc.
2.  **Tab Projects:** Triển khai lưu và tải kịch bản.
3.  **Tab License & Settings:** Hoàn thiện các chức năng phụ.

---

### **Chi tiết Kế hoạch**

#### **1. Triển khai Tab "Emotions" (Quản lý Cảm xúc)**

*   **Phân tích Backend (API đã có):**
    *   `GET /v1/emotions`: Lấy danh sách.
    *   `POST /v1/emotions`: Tạo mới.
    *   `PUT /v1/emotions/{name}`: Cập nhật.
    *   `DELETE /v1/emotions/{name}`: Xóa.
    *   `POST /v1/emotions/import` & `GET /v1/emotions/export`: Import/Export JSON.

*   **Kế hoạch Frontend (`EmotionManager.tsx`, `EmotionTable.tsx`):**
    1.  **Hiển thị danh sách:**
        *   Tạo hàm API trong `voice-api.ts` để gọi `GET /v1/emotions`.
        *   Dùng `useEffect` trong `EmotionManager.tsx` để gọi API và lưu kết quả vào state.
        *   Truyền dữ liệu vào `EmotionTable.tsx` để hiển thị dạng bảng với các nút hành động (Sửa, Xóa).
    2.  **Thêm/Sửa:**
        *   Tạo form (dạng modal) để nhập liệu.
        *   Khi "Lưu", gọi API `POST` (tạo mới) hoặc `PUT` (cập nhật).
        *   Làm mới lại bảng sau khi thành công.
    3.  **Xóa:**
        *   Hiển thị hộp thoại xác nhận trước khi gọi API `DELETE`.
        *   Làm mới lại bảng.
    4.  **Import/Export:**
        *   Tạo nút để gọi các API tương ứng và xử lý file.

---

#### **2. Triển khai Tab "Projects" (Quản lý Dự án)**

*   **Phân tích Backend (API đã có):**
    *   `GET /v1/projects`: Liệt kê.
    *   `POST /v1/projects`: Tạo mới.
    *   `GET /v1/projects/{id}`: Tải.
    *   `PUT /v1/projects/{id}`: Lưu/Cập nhật.
    *   `DELETE /v1/projects/{id}`: Xóa.

*   **Kế hoạch Frontend (`ProjectManager.tsx`):**
    1.  **Hiển thị danh sách:** Gọi `GET /v1/projects` và hiển thị.
    2.  **Lưu dự án:**
        *   Tạo nút "Save Project".
        *   Lấy dữ liệu kịch bản (`segments`, `characters`) từ state của `VoiceStudioV2.tsx`.
        *   Gọi API `POST` hoặc `PUT` để lưu dữ liệu.
    3.  **Tải dự án:**
        *   Khi người dùng chọn dự án, gọi `GET /v1/projects/{id}`.
        *   Cập nhật lại state trong `VoiceStudioV2.tsx` với dữ liệu nhận được.
    4.  **Xóa dự án:** Triển khai tương tự các tab khác.

---

#### **3. Triển khai Tab "License" & "Settings"**

*   **Phân tích Backend (API đã có):**
    *   Các endpoint `/v1/license/*` và `/v1/settings/*`.

*   **Kế hoạch Frontend (`LicenseManager.tsx`, `SettingsPanel`):**
    1.  **License:**
        *   Gọi `GET /v1/license/status` để hiển thị thông tin.
        *   Tạo ô input và nút để kích hoạt license qua `POST /v1/license/activate`.
    2.  **Settings:**
        *   Gọi `GET /v1/settings` để hiển thị.
        *   Cho phép thay đổi và lưu lại qua `POST /v1/settings`.
