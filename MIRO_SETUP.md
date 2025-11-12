# Hướng dẫn Setup Miro API (Chi tiết)

Hướng dẫn từng bước để lấy Miro API token và sử dụng tool này.

## Option 1: Sử dụng Web UI (KHÔNG cần API - Dễ nhất! ✅)

### Bước 1: Export JSON từ Miro

1. **Mở Miro board** của bạn
2. Click vào **menu "..." (3 chấm)** ở góc trên bên phải
3. Chọn **"Export this board"**
4. Trong popup export:
   - Format: Chọn **"Board backup (.rtb)"** hoặc sử dụng Miro API

**⚠️ Lưu ý**: Hiện tại Miro không hỗ trợ export JSON trực tiếp từ UI. Bạn cần dùng Option 2 (API) hoặc Option 3 (Demo data).

---

## Option 2: Sử dụng Miro API (Khuyến nghị)

### Bước 1: Tạo Miro Developer App

1. **Đăng nhập Miro**: https://miro.com
2. Truy cập **Developer Settings**: https://miro.com/app/settings/user-profile/apps
3. Click nút **"Create new app"**

   ![Create App Button](https://i.imgur.com/example1.png)

4. **Điền thông tin app**:
   ```
   App Name: Chatbot Graph Converter
   Description: Convert mindmap to chatbot graph
   ```

5. Click **"Create"**

### Bước 2: Cấu hình App Permissions

1. Sau khi tạo app, scroll xuống section **"Permissions"**

2. Bật các permissions sau:
   ```
   ✅ boards:read         - Read board content
   ✅ boards:write        - (Optional) Nếu muốn update board
   ```

3. Click **"Save"** để lưu permissions

### Bước 3: Lấy Access Token

Có 2 cách lấy token:

#### Cách A: Development Token (Dễ - Dùng cho testing)

1. Trong app settings, scroll xuống **"Access tokens"** section
2. Click **"Install app and get OAuth token"**
3. Chọn team bạn muốn cài đặt app
4. Click **"Add"** để authorize
5. Copy **Access Token** hiển thị:
   ```
   Token sẽ có dạng:
   MRo1234567890abcdefghijklmnopqrstuvwxyz...
   ```
6. ⚠️ **LƯU TOKEN NÀY AN TOÀN** - Không share với người khác!

#### Cách B: OAuth 2.0 (Production - Phức tạp hơn)

Xem docs: https://developers.miro.com/docs/getting-started-with-oauth

### Bước 4: Lấy Board ID

1. **Mở board Miro** bạn muốn convert
2. Nhìn vào URL trên browser:
   ```
   https://miro.com/app/board/uXjVKbzXYZ0=/
                              ^^^^^^^^^^^^
                              Đây là Board ID
   ```
3. Copy phần ID (bao gồm cả dấu `=` ở cuối nếu có)

### Bước 5: Test Token

Test token bằng curl:

```bash
# Thay YOUR_ACCESS_TOKEN và YOUR_BOARD_ID
curl -X GET \
  'https://api.miro.com/v2/boards/YOUR_BOARD_ID' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

Nếu thành công, bạn sẽ thấy JSON response với board info.

---

## Option 3: Sử dụng Demo Data (Không cần gì cả!)

1. Chạy web UI:
   ```bash
   streamlit run app.py
   ```

2. Chọn **"Upload JSON file từ Miro"**

3. Click button **"🎮 Sử dụng Demo Data"**

4. Done! Bạn có thể test toàn bộ tính năng với demo data

---

## Sử dụng Tool

### Cách 1: Web UI (Dễ nhất cho Product Team)

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy web app
streamlit run app.py
```

Web sẽ mở tại: http://localhost:8501

**Features:**
- ✅ Upload JSON hoặc dùng demo data
- ✅ Connect với Miro API
- ✅ Xem preview graph statistics
- ✅ Export và download JSON ngay trên web
- ✅ Không cần code!

### Cách 2: Command Line (Cho Developers)

```bash
# Setup .env file
cp .env.example .env
nano .env  # Paste token và board ID

# Run converter
python main.py --format all --export-graph
```

---

## Troubleshooting

### Lỗi 401 Unauthorized

```
Error: 401 Unauthorized
```

**Nguyên nhân**: Access token không hợp lệ

**Giải pháp**:
1. Check lại token có đúng không (không bị thừa khoảng trắng)
2. Đảm bảo token chưa expired
3. Verify app đã được install vào team
4. Thử generate token mới

### Lỗi 403 Forbidden

```
Error: 403 Forbidden
```

**Nguyên nhân**: Không có quyền truy cập board

**Giải pháp**:
1. Check app permissions có `boards:read` không
2. Đảm bảo bạn có quyền access board đó
3. Thử share board cho chính bạn với full permissions
4. Re-install app vào team

### Lỗi 404 Not Found

```
Error: 404 Not Found
```

**Nguyên nhân**: Board ID không tồn tại

**Giải pháp**:
1. Check lại Board ID từ URL
2. Đảm bảo copy đúng format (bao gồm cả `=` nếu có)
3. Try access board trực tiếp trên web trước

### Board trống / Không có data

```
Parsed 0 nodes and 0 edges
```

**Nguyên nhân**: Board không có items hoặc connectors

**Giải pháp**:
1. Thêm sticky notes/cards vào board
2. Connect các items bằng arrows (connectors)
3. Verify board không bị giới hạn permissions

### Lỗi SSL/Network

```
Error: SSL/Network connection failed
```

**Giải pháp**:
1. Check internet connection
2. Nếu dùng corporate network, check proxy settings
3. Try VPN nếu Miro bị block

---

## Security Best Practices

### ✅ DO:
- Store token trong `.env` file (gitignored)
- Use environment variables trong production
- Rotate token định kỳ (3-6 tháng)
- Limit permissions chỉ những gì cần (`boards:read`)
- Use OAuth 2.0 cho production apps

### ❌ DON'T:
- Commit token vào git repository
- Share token qua email/chat
- Dùng token của người khác
- Grant quá nhiều permissions
- Hardcode token trong code

---

## FAQ

### Q: Token có expire không?
**A**: Development token thường không expire, nhưng có thể bị revoke nếu:
- Bạn revoke manually trong app settings
- App bị delete
- Team permissions thay đổi

### Q: Có giới hạn API calls không?
**A**: Có. Miro rate limit:
- 100 requests per minute per app
- 1000 requests per hour per app

Tool này tự động handle pagination và retry.

### Q: Board cần format gì để convert được?
**A**:
- Items: Sticky notes, cards, shapes (có text content)
- Connectors: Arrows kết nối giữa các items
- Labels: Add text vào arrows để mô tả transitions

### Q: Có support board lớn không?
**A**: Có! Tool handle:
- Pagination cho board với nhiều items
- Streaming processing
- Memory efficient với graph operations

### Q: Export JSON có thể import lại vào Miro không?
**A**: Không. Tool này chỉ convert từ Miro → Chatbot format.
Để sync 2 chiều cần implement thêm write API.

### Q: Có thể tự động sync khi board update không?
**A**: Hiện tại chưa. Cần setup:
- Miro webhooks để listen board changes
- Auto re-export khi có changes
→ Feature này sẽ được add trong tương lai

---

## Resources

- 📘 **Miro API Docs**: https://developers.miro.com/docs
- 🔑 **Get Access Token**: https://miro.com/app/settings/user-profile/apps
- 💬 **Miro Community**: https://community.miro.com/
- 🐛 **Report Issues**: [GitHub Issues](https://github.com/yourusername/mindmap2graph/issues)

---

## Video Tutorial (Coming Soon)

- [ ] Video: Cách lấy Miro API token (Vietnamese)
- [ ] Video: Demo convert mindmap → chatbot graph
- [ ] Video: Deploy web app lên server

---

## Next Steps

1. ✅ Lấy Miro API token theo hướng dẫn trên
2. ✅ Chạy `streamlit run app.py` để mở web UI
3. ✅ Paste token và board ID
4. ✅ Click "Fetch Board Data"
5. ✅ Export và download JSON
6. ✅ Import vào chatbot platform của bạn

Happy converting! 🚀
