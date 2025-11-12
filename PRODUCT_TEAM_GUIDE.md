# Hướng dẫn cho Product Team 👥

Guide đơn giản cho Product Team để sử dụng tool mà **KHÔNG cần biết code**.

---

## 🎯 Mục đích

Tool này giúp bạn chuyển đổi **Miro mindmap** (vẽ conversation flow) thành **JSON file** để:
- Import vào chatbot platform (Dialogflow, Rasa, Botpress...)
- Tạo test scenarios tự động
- Document conversation flows
- Training chatbot AI

---

## 🚀 Quick Start (3 phút)

### Bước 1: Mở Web UI

**Option A: Đã có developer setup sẵn**

Developer sẽ cho bạn link, ví dụ:
- Local: `http://localhost:8501`
- Cloud: `https://your-company-mindmap2graph.streamlit.app`

Click vào link và bạn sẽ thấy giao diện web.

**Option B: Tự chạy trên máy (cần Python)**

```bash
# Mở Terminal/Command Prompt
cd mindmap2graph
./run.sh
# Chọn option 1 (Web UI)
```

### Bước 2: Chọn phương thức

Bạn có 2 cách:

#### 🎮 Cách 1: Dùng Demo Data (Dễ nhất - Test ngay!)

1. Chọn radio button: **"📁 Upload JSON file từ Miro"**
2. Click button **"🎮 Sử dụng Demo Data"**
3. Bạn sẽ thấy demo conversation flow
4. Skip xuống Bước 3

#### 🔗 Cách 2: Connect với Miro Board của bạn

1. Chọn radio button: **"🔗 Connect qua Miro API"**
2. Bạn cần 2 thứ:
   - **Miro Access Token** (xem [MIRO_SETUP.md](MIRO_SETUP.md) để lấy)
   - **Board ID** (copy từ URL board)

3. Paste vào 2 ô input
4. Click **"🔄 Fetch Board Data"**
5. Chờ 5-10 giây để load data

### Bước 3: Xem Preview

Sau khi có data, bạn sẽ thấy:
- 📊 **Statistics**: Số nodes, edges, node types
- 📋 **Nodes list**: Danh sách các conversation states
- 📈 **Graph stats**: Root nodes, leaf nodes, connectivity

### Bước 4: Export

1. **Chọn format** muốn export:
   - **💬 Dialogue Flow**: Cho chatbot platforms (khuyến nghị)
   - **🌳 Intent Tree**: Cho intent hierarchy
   - **🛤️ Scenario Paths**: Cho test cases
   - **📦 All Formats**: Export cả 3

2. Click **"📥 Generate & Download"**

3. File JSON sẽ tự động download về máy

4. ✅ Done! Giờ bạn có file JSON để import vào chatbot platform

---

## 📝 Vẽ Mindmap trên Miro như thế nào?

### Best Practices

#### ✅ DO (Nên làm):

1. **Sử dụng Sticky Notes hoặc Cards** cho mỗi dialogue state
   ```
   [Sticky Note] "Xin chào! Tôi có thể giúp gì?"
   ```

2. **Connect bằng Arrows** (Connectors)
   ```
   [State A] ----arrow----> [State B]
   ```

3. **Add labels vào arrows** để mô tả điều kiện/hành động
   ```
   [Welcome] --"user says hi"--> [Ask Name]
   ```

4. **Tổ chức flow rõ ràng**:
   - Entry points (bắt đầu) ở **bên trái hoặc trên**
   - End points (kết thúc) ở **bên phải hoặc dưới**
   ```
   [Start] --> [Middle] --> [End]
   ```

5. **Group related nodes** bằng Frames
   ```
   ┌─────────────────────┐
   │ Frame: Order Flow   │
   │ [Select] [Confirm]  │
   └─────────────────────┘
   ```

#### ❌ DON'T (Tránh):

- ❌ Để nodes không connect (orphan nodes)
- ❌ Quá nhiều arrows từ 1 node (>5 branches)
- ❌ Circular loops phức tạp không có exit
- ❌ Text quá dài trong 1 node (>200 chars)
- ❌ Không có root node (entry point)

### Example Flow

```
                    [Chào mừng]
                         │
        ┌────────────────┴────────────────┐
        │                                  │
  "Đặt hàng"                          "Hỏi info"
        │                                  │
        ▼                                  ▼
  [Chọn sản phẩm]                   [Cung cấp info]
        │                                  │
   "Xác nhận"                          "Kết thúc"
        │                                  │
        ▼                                  ▼
  [Xác nhận đơn]                      [Cảm ơn]
        │                                  │
        └────────────┬────────────────────┘
                     ▼
                 [End]
```

---

## 📤 Output Format Giải thích

### 1. Dialogue Flow Format 💬

**Dùng cho**: Import vào chatbot platform

**Structure**:
```json
{
  "states": [
    {
      "state_id": "node_1",
      "message": "Xin chào!",
      "transitions": [
        {
          "target_state": "node_2",
          "condition": "Người dùng nói gì đó",
          "label": "Continue"
        }
      ]
    }
  ]
}
```

**Cách dùng**:
- Import vào Dialogflow/Rasa/Botpress
- Mỗi `state` là 1 dialogue node
- `transitions` là các nhánh conversation có thể đi tiếp

### 2. Intent Tree Format 🌳

**Dùng cho**: Design intent hierarchy

**Structure**:
```json
{
  "intent_trees": [
    {
      "intent_id": "main_greeting",
      "intent_name": "Greeting",
      "children": [
        {
          "intent_id": "ask_name",
          "intent_name": "Ask Name"
        }
      ]
    }
  ]
}
```

**Cách dùng**:
- Training NLU model
- Organize intents theo hierarchy
- Document intent structure

### 3. Scenario Paths Format 🛤️

**Dùng cho**: Test cases, user journeys

**Structure**:
```json
{
  "scenarios": [
    {
      "scenario_id": "scenario_1",
      "steps": [
        {"step_number": 1, "message": "Start"},
        {"step_number": 2, "message": "Middle"},
        {"step_number": 3, "message": "End"}
      ]
    }
  ]
}
```

**Cách dùng**:
- Generate test cases tự động
- Document user journeys
- Training conversation AI

---

## 🎓 Examples & Use Cases

### Use Case 1: E-commerce Chatbot

**Miro Board Setup**:
```
[Welcome]
    ├─> [Browse Products]
    │       └─> [Add to Cart]
    │               └─> [Checkout]
    │                       └─> [Payment]
    │                               └─> [Confirmation]
    └─> [Track Order]
            └─> [Show Status]
                    └─> [End]
```

**Export**: Dialogue Flow → Import vào Dialogflow

**Result**: Chatbot tự động handle order flow

### Use Case 2: Support Bot

**Miro Board Setup**:
```
[Greeting]
    ├─> [Technical Issue]
    │       ├─> [Network Problem]
    │       ├─> [Software Bug]
    │       └─> [Hardware Issue]
    └─> [Billing Question]
            ├─> [Invoice]
            └─> [Payment]
```

**Export**: Intent Tree → Train NLU

**Result**: Bot phân loại support requests

### Use Case 3: Onboarding Bot

**Miro Board Setup**:
```
[Start Onboarding]
    └─> [Collect Info]
            └─> [Verify Email]
                    └─> [Setup Profile]
                            └─> [Tour Features]
                                    └─> [Complete]
```

**Export**: Scenario Paths → Test cases

**Result**: Automated testing onboarding flow

---

## ❓ FAQ

### Q: Tôi không biết code, có dùng được không?
**A**: Có! Tool có web UI, chỉ cần:
1. Mở web
2. Upload file hoặc connect Miro
3. Click export
4. Download JSON

### Q: Miro board cần format đặc biệt không?
**A**: Không. Chỉ cần:
- Có sticky notes/cards (nodes)
- Connect bằng arrows (edges)
- Add labels vào arrows nếu muốn

### Q: Tôi không có Miro API token?
**A**: Dùng demo data để test! Hoặc nhờ developer lấy token giúp (xem [MIRO_SETUP.md](MIRO_SETUP.md))

### Q: Export JSON làm gì tiếp?
**A**:
1. Import vào chatbot platform của bạn
2. Hoặc gửi cho developer để implement
3. Hoặc dùng làm documentation

### Q: Board lớn có convert được không?
**A**: Có! Tool handle boards với hàng trăm nodes

### Q: Có giới hạn số nodes không?
**A**: Không có hard limit, nhưng khuyến nghị:
- < 100 nodes: Tốt
- 100-500 nodes: OK
- > 500 nodes: Nên chia nhỏ board

### Q: Có thể edit JSON sau khi export không?
**A**: Có, file JSON có thể edit bằng text editor bất kỳ

### Q: Export rồi có import lại vào Miro được không?
**A**: Hiện tại chưa. Tool chỉ support Miro → JSON (1 chiều)

---

## 🆘 Troubleshooting

### Web không load được

**Giải pháp**:
1. Check internet connection
2. Thử browser khác (Chrome recommended)
3. Clear browser cache
4. Liên hệ developer

### Không fetch được board data

**Check list**:
- ✅ Token có đúng không?
- ✅ Board ID có đúng không?
- ✅ Bạn có quyền access board không?
- ✅ Board có items và connectors không?

### Export file bị lỗi

**Giải pháp**:
1. Thử export format khác
2. Check board có data không
3. Thử với demo data xem có lỗi không
4. Screenshot error gửi developer

### File JSON không import được vào chatbot platform

**Check**:
- ✅ Format có đúng với platform không?
- ✅ Try validate JSON online: jsonlint.com
- ✅ Check platform docs về import format

---

## 📞 Support

### Cần help?

1. **Docs**: Đọc [README.md](README.md) và [QUICKSTART.md](QUICKSTART.md)
2. **Demo**: Thử demo data trước để hiểu flow
3. **Developer**: Nhờ developer trong team support
4. **Issues**: Report bug tại GitHub Issues

### Training Session

Nếu team cần training:
- Schedule 30-minute demo session
- Hands-on practice với Miro board thật
- Q&A session

---

## ✅ Checklist

Trước khi bắt đầu:

- [ ] Đã có Miro board với conversation flow
- [ ] Board có sticky notes/cards (nodes)
- [ ] Các nodes đã được connect bằng arrows
- [ ] (Optional) Đã add labels vào arrows
- [ ] Đã có access token hoặc dùng demo data
- [ ] Web UI đã được mở
- [ ] Đã đọc hướng dẫn này

Sau khi export:

- [ ] File JSON đã download
- [ ] Đã verify JSON format
- [ ] Ready để import vào chatbot platform
- [ ] Đã backup file JSON

---

## 🎉 Tips & Tricks

### Tip 1: Start Small
Bắt đầu với flow đơn giản (5-10 nodes) để làm quen tool

### Tip 2: Use Frames
Group related nodes bằng Frames để organize tốt hơn

### Tip 3: Naming Convention
Đặt tên nodes theo pattern: `[Category] Action`
```
[Order] Select Product
[Order] Confirm Purchase
[Support] Technical Issue
```

### Tip 4: Version Control
Save multiple versions của Miro board để track changes

### Tip 5: Collaborate
Share board với team để review flow trước khi export

---

## 📚 Next Steps

1. ✅ Đọc guide này
2. ✅ Thử demo data
3. ✅ Vẽ mindmap trên Miro
4. ✅ Export & download JSON
5. ✅ Import vào chatbot platform
6. ✅ Test chatbot
7. ✅ Iterate và improve

Happy chatbot building! 🤖🚀
