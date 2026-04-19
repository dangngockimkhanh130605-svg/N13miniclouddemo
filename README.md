# ☁️ MyMiniCloud Project - Comprehensive Testing & Deployment Manual

Tài liệu hướng dẫn chuẩn bị và kiểm thử toàn diện hệ thống MyMiniCloud (9 Server cơ bản + 10 Tiện ích mở rộng).

---

## 🛠 PHẦN 1: CHUẨN BỊ MÔI TRƯỜNG (PREPARATION)

### 1.1. Trên Máy Local (Windows/MacOS)

1. **Khởi động Docker:** Đảm bảo Docker Desktop đã được bật.
2. **Di chuyển vào thư mục dự án:**
   ```cmd
   cd C:\Users\Myle\Documents\CloudComputing\FromGitHub\N13miniclouddemo
   ```
3. **Build và Chạy Container:**
   ```dos
   docker-compose build --no-cache
   docker-compose up -d
   ```
4. **Kiểm tra trạng thái:** `docker-compose ps` (Tất cả phải là `Up`).

---

### 1.2. Trên Môi trường AWS EC2

1. **Kết nối SSH:**
   ```dos
   ssh -i "MyKeypair.pem" ubuntu@ec2-47-129-37-143.ap-southeast-1.compute.amazonaws.com
   ```
2. **Di chuyển vào thư mục dự án trên EC2:**
   ```bash
   cd ~/N13miniclouddemo
   ```
3. **Khởi chạy hệ thống:**
   ```bash
   docker-compose up -d
   ```
4. **Kiểm tra trạng thái:** `docker-compose ps`.

---

## 🛑 PHẦN 2: KỊCH BẢN KIỂM THỬ CƠ BẢN TRÊN LOCAL (9 SERVER)

> Hoàn thành toàn bộ phần này → **5 điểm cơ bản**.

### 2.1. Kiểm thử bằng Trình duyệt (Browser)

| STT | Dịch vụ | URL Truy cập | Kỳ vọng kết quả |
|-----|---------|--------------|-----------------|
| 1 | Web Server | http://localhost:8080/ | Hiển thị trang `MyMiniCloud – Home` |
| 1 | Web Blog | http://localhost:8080/blog/ | Hiển thị trang `MyMiniCloud Blog` |
| 4 | Auth Server (Keycloak) | http://localhost:8081 | Giao diện Keycloak, đăng nhập được `admin/admin` |
| 5 | Storage (MinIO Console) | http://localhost:9001 | Giao diện MinIO, đăng nhập `minioadmin/minioadmin` |
| 7 | Monitoring (Prometheus) | http://localhost:9090 | Giao diện Prometheus, tab Status → Targets |
| 8 | Grafana Dashboard | http://localhost:3000 | Giao diện Grafana, đăng nhập `admin/admin` |

---

### 2.2. Kiểm thử bằng Dòng lệnh (Terminal)

> 💡 **Mỗi mục đều có 2 tab lệnh:** chọn đúng môi trường đang dùng.
> - **Bash** → dùng cho Git Bash / WSL / MacOS / Linux Terminal
> - **PowerShell** → dùng cho Windows PowerShell / Terminal gốc Windows

---

#### 1️⃣ Web Frontend Server (Nginx static site)

**Mục đích:** Kiểm tra khả năng phục vụ trang web tĩnh.

**Bash (Git Bash / WSL / Linux / MacOS):**
```bash
# Kiểm tra trang chủ
curl -I http://localhost:8080/

# Kiểm tra trang blog
curl -I http://localhost:8080/blog/
```

**PowerShell (Windows):**
```powershell
# Kiểm tra trang chủ
Invoke-WebRequest -Uri http://localhost:8080/ -Method HEAD | Select-Object StatusCode, StatusDescription

# Kiểm tra trang blog
Invoke-WebRequest -Uri http://localhost:8080/blog/ -Method HEAD | Select-Object StatusCode, StatusDescription
```

**Kỳ vọng:**
- Cả 2 lệnh đều trả về `200 OK`.
- Trang Home hiển thị `MyMiniCloud – Home`.
- Trang Blog hiển thị `MyMiniCloud Blog`.

---

#### 2️⃣ Application Backend Server (Flask API)

**Mục đích:** Kiểm tra API backend hoạt động và trả JSON đúng định dạng.

**Bash:**
```bash
# Gọi trực tiếp qua port 8085
curl http://localhost:8085/hello

# Gọi qua Reverse Proxy
curl http://localhost/api/hello
```

**PowerShell:**
```powershell
# Gọi trực tiếp qua port 8085
Invoke-RestMethod -Uri http://localhost:8085/hello

# Gọi qua Reverse Proxy
Invoke-RestMethod -Uri http://localhost/api/hello
```

**Kỳ vọng:**
- Cả 2 lệnh đều trả về JSON: `{"message": "Hello from App Server!"}`.
- Proxy hoạt động đúng (kết quả 2 lệnh giống nhau).

---

#### 3️⃣ Relational Database Server (MariaDB)

**Mục đích:** Kiểm tra dữ liệu khởi tạo tự động trong container DB.

**Bash:**
```bash
docker exec -it relational-database-server mysql -uroot -proot \
  -e "USE minicloud; SHOW TABLES; SELECT * FROM notes;"
```

**PowerShell:**
```powershell
docker exec -it relational-database-server mariadb -uroot -proot `
  -e "USE minicloud; SHOW TABLES; SELECT * FROM notes;"
```

> ⚠️ PowerShell dùng dấu `` ` `` (backtick) thay cho `\` (backslash) để xuống dòng.

**Kỳ vọng:**
- Bảng `notes` tồn tại.
- Có ít nhất 1 dòng dữ liệu: `Hello from MariaDB!`.

---

#### 4️⃣ Authentication Identity Server (Keycloak)

**Mục đích:** Kiểm tra dịch vụ đăng nhập OIDC hoạt động.

**Bash:**
```bash
# Kiểm tra Keycloak phản hồi qua proxy
curl -I http://localhost/auth/
```

**PowerShell:**
```powershell
# Kiểm tra Keycloak phản hồi qua proxy
# -MaximumRedirection 0 để thấy status 302 thay vì bị redirect tự động
try {
    Invoke-WebRequest -Uri http://localhost/auth/ -Method HEAD -MaximumRedirection 0
} catch {
    $_.Exception.Response.StatusCode.value__
    $_.Exception.Response.Headers["Location"]
}
```

**Kỳ vọng:**
- Trả về `302 Found` → redirect về trang login Keycloak.
- Truy cập http://localhost:8081 trên trình duyệt → đăng nhập `admin/admin` thành công.
- Giao diện Dashboard Keycloak hiển thị, tạo được user `sv01`.

---

#### 5️⃣ Object Storage Server (MinIO)

**Mục đích:** Kiểm tra lưu trữ đối tượng tương tự Amazon S3.

**Bash:**
```bash
# Kiểm tra MinIO API đang sống
curl -I http://localhost:9000/minio/health/live
```

**PowerShell:**
```powershell
# Kiểm tra MinIO API đang sống
Invoke-WebRequest -Uri http://localhost:9000/minio/health/live -Method HEAD | Select-Object StatusCode, StatusDescription
```

**Kỳ vọng:**
- API trả về `200 OK`.
- Truy cập http://localhost:9001 → đăng nhập `minioadmin/minioadmin` → tạo bucket `demo` → upload file thành công.

---

#### 6️⃣ Internal DNS Server (Bind9)

**Mục đích:** Kiểm tra phân giải tên miền nội bộ.

**Bash:**
```bash
# Truy vấn bản ghi DNS nội bộ
dig @127.0.0.1 -p 1053 web-frontend-server.cloud.local +short
```

**PowerShell:**
```powershell
# Truy vấn bản ghi DNS nội bộ qua container (không cần cài dig trên Windows)
docker exec -it internal-dns-server dig @127.0.0.1 web-frontend-server.cloud.local +short

# Hoặc dùng Resolve-DnsName nếu port 1053 được expose ra localhost
Resolve-DnsName -Name web-frontend-server.cloud.local -Server 127.0.0.1 -Port 1053 -Type A
```

**Kỳ vọng:**
- Trả về IP `10.10.10.10` (theo file cấu hình `db.cloud.local`).
- Nếu trống → kiểm tra `db.cloud.local` và restart container.

---

#### 7️⃣ Monitoring: Node Exporter + Prometheus

**Mục đích:** Xác minh hệ thống giám sát thu thập metric hoạt động.

**Bash:**
```bash
# Kiểm tra Node Exporter cung cấp metrics
curl -s http://localhost:9100/metrics | head -n 10
```

**PowerShell:**
```powershell
# Kiểm tra Node Exporter cung cấp metrics (lấy 10 dòng đầu)
(Invoke-RestMethod -Uri http://localhost:9100/metrics) -split "`n" | Select-Object -First 10
```

**Kỳ vọng:**
- Trả về danh sách metrics bắt đầu bằng `# HELP` và `# TYPE`.
- Truy cập http://localhost:9090 → **Status → Targets** → `monitoring-node-exporter-server:9100` trạng thái **UP**.
- Thử truy vấn `node_cpu_seconds_total` trong tab Graph → có dữ liệu.

---

#### 8️⃣ Monitoring Grafana Dashboard

**Mục đích:** Kiểm tra khả năng hiển thị biểu đồ giám sát.

**Bash:**
```bash
# Kiểm tra Grafana đang chạy
curl -I http://localhost:3000
```

**PowerShell:**
```powershell
# Kiểm tra Grafana đang chạy
Invoke-WebRequest -Uri http://localhost:3000 -Method HEAD | Select-Object StatusCode, StatusDescription
```

**Kỳ vọng:**
- Trả về `200 OK`.
- Truy cập http://localhost:3000 → đăng nhập `admin/admin`.
- Add datasource Prometheus với URL: `http://monitoring-prometheus-server:9090`.
- Import dashboard **"Node Exporter Full"** → Dashboard hiển thị CPU/RAM/Network metrics.

---

#### 9️⃣ API Gateway Proxy Server (Nginx Reverse Proxy)

**Mục đích:** Kiểm tra routing hợp nhất qua một cổng duy nhất.

**Bash:**
```bash
# Route / → Web server
curl -I http://localhost/

# Route /api/hello → App backend
curl -s http://localhost/api/hello

# Route /auth/ → Keycloak
curl -I http://localhost/auth/
```

**PowerShell:**
```powershell
# Route / → Web server
Invoke-WebRequest -Uri http://localhost/ -Method HEAD | Select-Object StatusCode

# Route /api/hello → App backend
Invoke-RestMethod -Uri http://localhost/api/hello

# Route /auth/ → Keycloak (bắt 302 thủ công)
try {
    Invoke-WebRequest -Uri http://localhost/auth/ -Method HEAD -MaximumRedirection 0
} catch {
    "StatusCode: " + $_.Exception.Response.StatusCode.value__
}
```

**Kỳ vọng:**
- `/` → trả `200 OK` (web tĩnh).
- `/api/hello` → JSON `{"message": "Hello from App Server!"}`.
- `/auth/` → redirect `302` đến Keycloak login page.

---

#### 🔟 Kiểm tra thông mạng nội bộ (Ping tất cả server)

**Mục đích:** Xác minh tất cả container trong cùng network `cloud-net` có thể ping nhau.

**Bash:**
```bash
docker exec -it api-gateway-proxy-server ping -c 3 web-frontend-server
docker exec -it api-gateway-proxy-server ping -c 3 application-backend-server
docker exec -it api-gateway-proxy-server ping -c 3 relational-database-server
docker exec -it api-gateway-proxy-server ping -c 3 authentication-identity-server
docker exec -it api-gateway-proxy-server ping -c 3 object-storage-server
docker exec -it api-gateway-proxy-server ping -c 3 internal-dns-server
docker exec -it api-gateway-proxy-server ping -c 3 monitoring-prometheus-server
docker exec -it api-gateway-proxy-server ping -c 3 monitoring-grafana-dashboard-server
```

**PowerShell:**
```powershell
# Ping từng container (dùng -n thay -c trên Windows container nếu cần,
# nhưng vì đây là container Linux nên vẫn dùng -c 3)
docker exec -it api-gateway-proxy-server ping -c 3 web-frontend-server
docker exec -it api-gateway-proxy-server ping -c 3 application-backend-server
docker exec -it api-gateway-proxy-server ping -c 3 relational-database-server
docker exec -it api-gateway-proxy-server ping -c 3 authentication-identity-server
docker exec -it api-gateway-proxy-server ping -c 3 object-storage-server
docker exec -it api-gateway-proxy-server ping -c 3 internal-dns-server
docker exec -it api-gateway-proxy-server ping -c 3 monitoring-prometheus-server
docker exec -it api-gateway-proxy-server ping -c 3 monitoring-grafana-dashboard-server
```

> 💡 Lệnh `docker exec` chạy bên trong container Linux nên cú pháp `-c 3` giữ nguyên cho cả Bash và PowerShell. Lệnh `ping` ở đây là của container, không phải của Windows.

**Kỳ vọng:**
- Tất cả lệnh ping trả về `0% packet loss` → các container thông mạng hoàn toàn.

> 👉 **Chú ý: Hoàn thành đến đây SV sẽ được 5 điểm cơ bản.**

---

## 🚀 PHẦN 3: KỊCH BẢN KIỂM THỬ MỞ RỘNG (10 YÊU CẦU — 5 ĐIỂM)

> Mỗi yêu cầu mở rộng = **0.5 điểm**. Trong báo cáo ghi rõ đã làm được bao nhiêu phần.

---

> 💡 **Mỗi mục đều có 2 tab lệnh:** chọn đúng môi trường đang dùng.
> - **Bash** → dùng cho Git Bash / WSL / MacOS / Linux Terminal
> - **PowerShell** → dùng cho Windows PowerShell / Terminal gốc Windows

---

### Mở rộng 1️⃣ — Web Frontend: Blog cá nhân 3 bài

**Mục tiêu:** Tạo ≥ 3 bài viết HTML trong thư mục `/blog/`, mỗi bài có ảnh và link quay về.

**Bash:**
```bash
# Kiểm tra từng bài blog trả về 200
curl -I http://localhost:8080/blog/blog1.html
curl -I http://localhost:8080/blog/blog2.html
curl -I http://localhost:8080/blog/blog3.html

# Kiểm tra trang index có hyperlink đến 3 bài
curl -s http://localhost:8080/ | grep "blog"
```

**PowerShell:**
```powershell
# Kiểm tra từng bài blog trả về 200
Invoke-WebRequest -Uri http://localhost:8080/blog/blog1.html -Method HEAD | Select-Object StatusCode
Invoke-WebRequest -Uri http://localhost:8080/blog/blog2.html -Method HEAD | Select-Object StatusCode
Invoke-WebRequest -Uri http://localhost:8080/blog/blog3.html -Method HEAD | Select-Object StatusCode

# Kiểm tra trang index có hyperlink đến 3 bài
(Invoke-WebRequest -Uri http://localhost:8080/).Content | Select-String "blog"
```

**Kỳ vọng:**
- Cả 3 URL trả về `200 OK`.
- Nội dung trang chủ chứa các đường link `/blog/blog1.html`, `/blog/blog2.html`, `/blog/blog3.html`.
- Mỗi bài viết hiển thị được ảnh minh họa và có link quay về trang chính.

---

### Mở rộng 2️⃣ — Application Backend: API `/student`

**Mục tiêu:** Thêm route `/student` trả danh sách 5 sinh viên từ file JSON.

**Bash:**
```bash
# Gọi trực tiếp qua port backend
curl http://localhost:8085/student

# Gọi qua Reverse Proxy
curl http://localhost/api/student
```

**PowerShell:**
```powershell
# Gọi trực tiếp qua port backend
Invoke-RestMethod -Uri http://localhost:8085/student

# Gọi qua Reverse Proxy
Invoke-RestMethod -Uri http://localhost/api/student
```

**Kỳ vọng:**
- Cả 2 lệnh đều trả về JSON danh sách 5 sinh viên gồm các trường `id`, `name`, `major`, `gpa`.
- Ví dụ: `[{"gpa": 3.5, "id": 1, "major": "CNTT", "name": "Nguyen Van A"}, ...]`

---

### Mở rộng 3️⃣ — Database: Tạo `studentdb` và bảng `students`

**Mục tiêu:** Tạo CSDL `studentdb`, bảng `students` với ≥ 3 bản ghi.

**Bash:**
```bash
# Kiểm tra database studentdb tồn tại
docker exec -it relational-database-server mysql -uroot -proot \
  -e "SHOW DATABASES;" | grep studentdb

# Xem cấu trúc bảng students
docker exec -it relational-database-server mysql -uroot -proot \
  -e "USE studentdb; DESCRIBE students;"

# Xem dữ liệu trong bảng
docker exec -it relational-database-server mysql -uroot -proot \
  -e "USE studentdb; SELECT * FROM students;"
```

**PowerShell:**
```powershell
# Kiểm tra database studentdb tồn tại
docker exec -it relational-database-server mysql -uroot -proot `
  -e "SHOW DATABASES;" | Select-String "studentdb"

# Xem cấu trúc bảng students
docker exec -it relational-database-server mysql -uroot -proot `
  -e "USE studentdb; DESCRIBE students;"

# Xem dữ liệu trong bảng
docker exec -it relational-database-server mysql -uroot -proot `
  -e "USE studentdb; SELECT * FROM students;"
```

> ⚠️ PowerShell dùng dấu `` ` `` (backtick) thay cho `\` (backslash) để xuống dòng.

**Kỳ vọng:**
- `SHOW DATABASES` liệt kê được `studentdb`.
- Bảng `students` có đủ 5 cột: `id`, `student_id`, `fullname`, `dob`, `major`.
- Có ít nhất 3 bản ghi dữ liệu.

---

### Mở rộng 4️⃣ — Keycloak: Realm, Client, User và test `/secure`

**Mục tiêu:** Tạo realm riêng theo MSSV, 2 user, 1 client, lấy token và truy cập `/secure`.

**Bash:**
```bash
# Bước 1: Lấy Access Token (thay realm_sv<MSSV> và <password> cho đúng)
TOKEN=$(curl -s -X POST \
  "http://localhost:8081/realms/realm_sv001/protocol/openid-connect/token" \
  -d "client_id=flask-app&username=sv01&password=<password>&grant_type=password" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# Bước 2: Dùng token gọi endpoint /secure
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8085/secure
```

**PowerShell:**
```powershell
# Bước 1: Lấy Access Token (thay realm_sv<MSSV> và <password> cho đúng)
$body = "client_id=flask-app&username=sv01&password=<password>&grant_type=password"
$response = Invoke-RestMethod -Method POST `
  -Uri "http://localhost:8081/realms/realm_sv001/protocol/openid-connect/token" `
  -Body $body `
  -ContentType "application/x-www-form-urlencoded"
$TOKEN = $response.access_token
Write-Host "Token (50 ký tự đầu): $($TOKEN.Substring(0,50))..."

# Bước 2: Dùng token gọi endpoint /secure
Invoke-RestMethod -Uri http://localhost:8085/secure `
  -Headers @{ Authorization = "Bearer $TOKEN" }
```

**Kỳ vọng:**
- Bước 1: biến `$TOKEN` chứa chuỗi JWT dài (không rỗng, không báo lỗi).
- Bước 2 trả về JSON: `{"message": "Secure resource OK", "preferred_username": "sv01"}`.
- Trên giao diện http://localhost:8081 → thấy realm `realm_sv001`, user `sv01`/`sv02`, client `flask-app`.

---

### Mở rộng 5️⃣ — MinIO: Upload avatar và file PDF

**Mục tiêu:** Tạo 2 bucket `profile-pics` và `documents`, upload file thành công.

**Bash:**
```bash
# Kiểm tra MinIO API đang sống
curl -I http://localhost:9000/minio/health/live

# (Nếu bucket được set policy public) Kiểm tra object có truy cập được không
curl -I http://localhost:9000/profile-pics/avatar.jpg
```

**PowerShell:**
```powershell
# Kiểm tra MinIO API đang sống
Invoke-WebRequest -Uri http://localhost:9000/minio/health/live -Method HEAD | Select-Object StatusCode

# (Nếu bucket được set policy public) Kiểm tra object có truy cập được không
try {
    Invoke-WebRequest -Uri http://localhost:9000/profile-pics/avatar.jpg -Method HEAD | Select-Object StatusCode
} catch {
    "StatusCode: " + $_.Exception.Response.StatusCode.value__
}
```

**Kỳ vọng:**
- http://localhost:9001 → đăng nhập được.
- Bucket `profile-pics` tồn tại và chứa file `avatar.jpg`.
- Bucket `documents` tồn tại và chứa file PDF báo cáo.
- Có thể lấy URL public object (nếu set policy public).

---

### Mở rộng 6️⃣ — DNS: Thêm bản ghi A mới

**Mục tiêu:** Thêm `app-backend`, `minio`, `keycloak` vào zone `cloud.local` và test `dig`.

**Bash:**
```bash
# Kiểm tra bản ghi app-backend
dig @127.0.0.1 -p 1053 app-backend.cloud.local +short

# Kiểm tra bản ghi minio
dig @127.0.0.1 -p 1053 minio.cloud.local +short

# Kiểm tra bản ghi keycloak
dig @127.0.0.1 -p 1053 keycloak.cloud.local +short
```

**PowerShell:**
```powershell
# Cách 1: Dùng docker exec vào container DNS (luôn hoạt động, không cần cài thêm)
docker exec -it internal-dns-server dig @127.0.0.1 app-backend.cloud.local +short
docker exec -it internal-dns-server dig @127.0.0.1 minio.cloud.local +short
docker exec -it internal-dns-server dig @127.0.0.1 keycloak.cloud.local +short

# Cách 2: Dùng Resolve-DnsName có sẵn trên Windows (port 1053 phải được expose)
Resolve-DnsName -Name app-backend.cloud.local -Server 127.0.0.1 -Port 1053 -Type A
Resolve-DnsName -Name minio.cloud.local       -Server 127.0.0.1 -Port 1053 -Type A
Resolve-DnsName -Name keycloak.cloud.local    -Server 127.0.0.1 -Port 1053 -Type A
```

**Kỳ vọng:**
- `app-backend.cloud.local` → trả về `10.10.10.20`.
- `minio.cloud.local` và `keycloak.cloud.local` → trả về IP tương ứng đã cấu hình.
- Không có lỗi `NXDOMAIN` hay `connection refused`.

---

### Mở rộng 7️⃣ — Prometheus: Thêm scrape target `web`

**Mục tiêu:** Thêm job `web` giám sát `web-frontend-server:80`, xác nhận target xuất hiện.

**Bash:**
```bash
# Kiểm tra danh sách targets qua Prometheus API
curl -s http://localhost:9090/api/v1/targets \
  | python3 -m json.tool | grep -A5 '"job":"web"'
```

**PowerShell:**
```powershell
# Kiểm tra danh sách targets qua Prometheus API
$targets = Invoke-RestMethod -Uri "http://localhost:9090/api/v1/targets"
$targets.data.activeTargets | Where-Object { $_.labels.job -eq "web" } | Select-Object scrapeUrl, health
```

**Kỳ vọng:**
- Kết quả hiển thị job tên `web` với `scrapeUrl` chứa `web-frontend-server:80`.
- Truy cập http://localhost:9090/targets → thấy job `web` xuất hiện trong danh sách.

---

### Mở rộng 8️⃣ — Grafana: Dashboard cá nhân 3 biểu đồ

**Mục tiêu:** Tạo dashboard tên `System Health of <MSSV>` với 3 panel: CPU, Memory, Network.

**Bash:**
```bash
# Liệt kê danh sách dashboard đã tạo
curl -s -u admin:admin "http://localhost:3000/api/search?type=dash-db" \
  | python3 -m json.tool | grep "title"
```

**PowerShell:**
```powershell
# Liệt kê danh sách dashboard đã tạo
$cred = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:admin"))
$dashboards = Invoke-RestMethod -Uri "http://localhost:3000/api/search?type=dash-db" `
  -Headers @{ Authorization = "Basic $cred" }
$dashboards | Select-Object title, url
```

**Kỳ vọng:**
- Kết quả liệt kê được dashboard có tên chứa `System Health of`.
- Truy cập http://localhost:3000 → Dashboard hiển thị đủ 3 panel: CPU Usage, Memory Usage, Network Traffic.
- Datasource đã kết nối tới Prometheus thành công (không báo `No data`).

---

### Mở rộng 9️⃣ — API Gateway: Route `/student/` qua proxy

**Mục tiêu:** Cấu hình `nginx.conf` thêm route `/student/` trỏ tới backend.

**Bash:**
```bash
# Test route /student/ qua proxy
curl http://localhost/student/

# Kiểm tra header phản hồi
curl -I http://localhost/student/
```

**PowerShell:**
```powershell
# Test route /student/ qua proxy — xem dữ liệu JSON
Invoke-RestMethod -Uri http://localhost/student/

# Kiểm tra header phản hồi
Invoke-WebRequest -Uri http://localhost/student/ -Method HEAD | Select-Object StatusCode, Headers
```

**Kỳ vọng:**
- Trả về JSON danh sách sinh viên (giống kết quả `/api/student`).
- Header trả về `200 OK`, `Content-Type: application/json`.

---

### Mở rộng 🔟 — Load Balancer: Round Robin giữa 2 Web Server

**Mục tiêu:** Cấu hình upstream `lb_cluster` với 2 server, kiểm thử response luân phiên.

**Bash:**
```bash
# Test Round Robin — chạy 6 lần, phải thấy luân phiên Server 1 / Server 2
for i in {1..6}; do
  echo "--- Lần $i ---"
  curl -s http://localhost/lba/ | grep "<h1>"
done

# Kiểm tra header X-LB-Test được gắn đúng
curl -I http://localhost/lba/
```

**PowerShell:**
```powershell
# Test Round Robin — chạy 6 lần, phải thấy luân phiên Server 1 / Server 2
1..6 | ForEach-Object {
    Write-Host "--- Lần $_ ---"
    (Invoke-WebRequest -Uri http://localhost/lba/).Content | Select-String "<h1>"
}

# Kiểm tra header X-LB-Test được gắn đúng
$resp = Invoke-WebRequest -Uri http://localhost/lba/
$resp.StatusCode
$resp.Headers["X-LB-Test"]
```

**Kỳ vọng:**
- Response luân phiên: `Server 1` → `Server 2` → `Server 1` → `Server 2` ...
- Header `X-LB-Test` có giá trị `Success-Node`.

---

## 🌐 PHẦN 4: KỊCH BẢN KIỂM THỬ TRÊN AWS EC2 (PUBLIC IP)

**Địa chỉ IP:** `47.129.37.143` | **IP Nội bộ:** `172.31.28.252`

### 4.1. Kiểm thử Công khai (Từ máy tính bất kỳ)

| STT | Dịch vụ / Mở rộng | URL Truy cập | Kỳ vọng kết quả |
|-----|-------------------|--------------|-----------------|
| 1 | Proxy Gateway (Web) | http://47.129.37.143/ | Trang chủ hiển thị ổn định qua Internet |
| 2 | App API qua Proxy | http://47.129.37.143/api/hello | JSON `{"message": "Hello from App Server!"}` |
| 3 | Auth (Keycloak) | http://47.129.37.143/auth/ | Redirect 302 đến Keycloak login page |
| 4 | API Student (MR #2) | http://47.129.37.143/api/student | JSON danh sách 5 sinh viên |
| 5 | Route /student/ (MR #9) | http://47.129.37.143/student/ | JSON danh sách sinh viên qua proxy |
| 6 | Monitoring Prometheus | http://47.129.37.143:9090 | Prometheus targets hiển thị **UP** |
| 7 | Grafana | http://47.129.37.143:3000 | Dashboard hiển thị biểu đồ |
| 8 | MinIO Console | http://47.129.37.143:9001 | Giao diện MinIO, thấy các bucket |
| 9 | Load Balancer (MR #10) | http://47.129.37.143/lba/ | Response luân phiên Server 1/Server 2 |

---

### 4.2. Kiểm thử Hạ tầng (Trong SSH Terminal)

> Các lệnh này bắt buộc chạy sau khi đã SSH vào EC2.

#### A. Kiểm tra DNS nội bộ (Mở rộng #6)

```bash
dig @127.0.0.1 -p 1053 web-frontend-server.cloud.local +short
# Kỳ vọng: 10.10.10.10

dig @127.0.0.1 -p 1053 app-backend.cloud.local +short
# Kỳ vọng: 10.10.10.20
```

#### B. Kiểm tra Database (Cơ bản & Mở rộng #3)

```bash
# Xem dữ liệu hệ thống (Cơ bản)
docker exec -it relational-database-server mysql -uroot -proot \
  -e "USE minicloud; SELECT * FROM notes;"

# Xem bảng sinh viên (Mở rộng #3)
docker exec -it relational-database-server mysql -uroot -proot \
  -e "USE studentdb; SELECT * FROM students;"
```

#### C. Kiểm tra Kết nối mạng nội bộ (Cơ bản #10)

```bash
docker exec -it api-gateway-proxy-server ping -c 3 web-frontend-server
docker exec -it api-gateway-proxy-server ping -c 3 application-backend-server
docker exec -it api-gateway-proxy-server ping -c 3 relational-database-server
docker exec -it api-gateway-proxy-server ping -c 3 authentication-identity-server
docker exec -it api-gateway-proxy-server ping -c 3 object-storage-server
docker exec -it api-gateway-proxy-server ping -c 3 internal-dns-server
docker exec -it api-gateway-proxy-server ping -c 3 monitoring-prometheus-server
docker exec -it api-gateway-proxy-server ping -c 3 monitoring-grafana-dashboard-server
```

#### D. Kiểm tra Log & Metrics (Cơ bản #7, Mở rộng #8)

```bash
# Kiểm tra Node Exporter cung cấp dữ liệu cho Prometheus
curl -s http://localhost:9100/metrics | head -n 10

# Kiểm tra Prometheus có job web (Mở rộng #7)
curl -s http://localhost:9090/api/v1/targets \
  | python3 -m json.tool | grep -A3 '"job":"web"'
```

#### E. Kiểm tra Load Balancer trên EC2 (Mở rộng #10)

```bash
for i in {1..6}; do
  echo "--- Lần $i ---"
  curl -s http://localhost/lba/ | grep "<h1>"
done
```

---

> **📸 Lưu ý cho Báo cáo:** Khi chụp ảnh minh chứng trên EC2, hãy đảm bảo khung hình bao gồm cả dòng chữ `ubuntu@ip-172-31-28-252:~/N13miniclouddemo$` để xác thực môi trường triển khai Cloud.

---

## ✅ PHẦN 5: BẢNG TỔNG KẾT KIỂM THỬ

### 5.1. Phần Cơ Bản (5 điểm)

| STT | Server | Lệnh / URL kiểm thử | Kỳ vọng | Kết quả |
|-----|--------|---------------------|---------|---------|
| 1 | Web Frontend | `curl -I http://localhost:8080/` | `200 OK` | ☐ |
| 1 | Web Blog | `curl -I http://localhost:8080/blog/` | `200 OK` | ☐ |
| 2 | App Server | `curl http://localhost:8085/hello` | JSON hello | ☐ |
| 3 | Database | `docker exec ... SELECT * FROM notes` | Có dữ liệu | ☐ |
| 4 | Keycloak | http://localhost:8081 | Đăng nhập được | ☐ |
| 5 | MinIO | http://localhost:9001 | Upload file OK | ☐ |
| 6 | DNS | `dig @127.0.0.1 -p 1053 web-frontend-server.cloud.local` | Trả về `10.10.10.10` | ☐ |
| 7 | Prometheus | http://localhost:9090/targets | Node Exporter **UP** | ☐ |
| 8 | Grafana | http://localhost:3000 | Dashboard hiển thị | ☐ |
| 9 | Proxy | `curl http://localhost/api/hello` | JSON qua proxy | ☐ |
| 10 | Network | `docker exec ... ping -c 3 ...` | `0% packet loss` | ☐ |

### 5.2. Phần Mở Rộng (5 điểm)

| STT | Server | Yêu cầu mở rộng | Lệnh / URL kiểm thử | Điểm | Kết quả |
|-----|--------|-----------------|---------------------|------|---------|
| 1 | Web Frontend | Blog 3 bài HTML | `curl -I http://localhost:8080/blog/blog1.html` | 0.5 | ☐ |
| 2 | Backend API | API `/student` | `curl http://localhost/api/student` | 0.5 | ☐ |
| 3 | Database | CSDL `studentdb` + bảng `students` | `docker exec ... SELECT * FROM students` | 0.5 | ☐ |
| 4 | Keycloak | Realm + Client + Token + `/secure` | `curl -H "Authorization: Bearer $TOKEN" .../secure` | 0.5 | ☐ |
| 5 | MinIO | 2 bucket + upload avatar & PDF | http://localhost:9001 → bucket `profile-pics` & `documents` | 0.5 | ☐ |
| 6 | DNS | Thêm 3 bản ghi A mới | `dig @127.0.0.1 -p 1053 app-backend.cloud.local` | 0.5 | ☐ |
| 7 | Prometheus | Thêm scrape target `web` | http://localhost:9090/targets → job `web` | 0.5 | ☐ |
| 8 | Grafana | Dashboard `System Health of <MSSV>` 3 panel | http://localhost:3000 → Dashboard cá nhân | 0.5 | ☐ |
| 9 | Proxy | Route `/student/` → backend | `curl http://localhost/student/` | 0.5 | ☐ |
| 10 | Load Balancer | Round Robin 2 web server | `for i in {1..6}; do curl -s http://localhost/lba/ \| grep "<h1>"; done` | 0.5 | ☐ |
| | | | **Tổng cộng** | **5 điểm** | |
