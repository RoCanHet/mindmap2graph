# Quick Start Guide

Hướng dẫn nhanh để bắt đầu sử dụng Miro Mindmap to Chatbot Graph Converter.

## Bước 1: Cài đặt

```bash
# Clone repository
git clone https://github.com/yourusername/mindmap2graph.git
cd mindmap2graph

# Cài đặt dependencies
pip install -r requirements.txt
```

## Bước 2: Chạy Demo (Không cần API key)

Để test tool mà không cần Miro API key, chạy demo với mock data:

```bash
python examples/demo_with_mock_data.py
```

Output sẽ được lưu vào folder `output/`:
- `demo_dialogue_flow.json` - Dialogue flow format
- `demo_intent_tree.json` - Intent tree format
- `demo_scenario_paths.json` - Scenario paths format
- `demo_graph.graphml` - Graph file (có thể mở bằng Gephi)

## Bước 3: Cấu hình Miro API

### Lấy Access Token:

1. Truy cập: https://miro.com/app/settings/user-profile/apps
2. Click "Create new app" hoặc chọn app có sẵn
3. Copy **Access Token**

### Lấy Board ID:

1. Mở board Miro của bạn
2. Copy ID từ URL: `https://miro.com/app/board/{BOARD_ID}/`

### Tạo file .env:

```bash
cp .env.example .env
```

Edit `.env`:

```env
MIRO_ACCESS_TOKEN=your_access_token_here
MIRO_BOARD_ID=your_board_id_here
```

## Bước 4: Chạy với Miro Board của bạn

```bash
# Export tất cả formats
python main.py

# Export format cụ thể
python main.py --format dialogue_flow

# Export với graph visualization
python main.py --export-graph
```

## Bước 5: Xem kết quả

Mở file JSON trong `output/` để xem kết quả:

```bash
# Linux/Mac
cat output/chatbot_scenario_dialogue_flow.json

# Windows
type output\chatbot_scenario_dialogue_flow.json
```

## Use Case Examples

### 1. Chatbot Flow Design

**Miro Setup:**
```
[Welcome] --"start"--> [Ask Need]
                          |
              +-----------+-----------+
              |                       |
         "order"                  "info"
              |                       |
              v                       v
        [Process Order]         [Show Info]
              |                       |
              v                       v
         [Confirm]                [Thanks]
```

**Command:**
```bash
python main.py --format dialogue_flow
```

**Result:** File JSON với states và transitions cho chatbot platform

### 2. Intent Hierarchy

**Miro Setup:**
```
[Main Intent]
    ├─> [Sub Intent 1]
    │       ├─> [Action 1.1]
    │       └─> [Action 1.2]
    └─> [Sub Intent 2]
            └─> [Action 2.1]
```

**Command:**
```bash
python main.py --format intent_tree
```

**Result:** Cây phân cấp intents cho NLU training

### 3. Test Scenarios

**Miro Setup:**
Vẽ tất cả các conversation paths có thể

**Command:**
```bash
python main.py --format scenario_paths
```

**Result:** List các test scenarios cho automated testing

## Tips cho Miro Board

✅ **DO:**
- Sử dụng Sticky Notes hoặc Cards cho dialogue states
- Connect bằng Connectors (arrows)
- Thêm labels vào connectors để mô tả conditions
- Tổ chức từ trái sang phải hoặc trên xuống dưới
- Group related intents bằng Frames

❌ **DON'T:**
- Để orphan nodes (không có connector)
- Tạo circular loops phức tạp
- Quá nhiều branches từ 1 node (>5)
- Labels quá dài hoặc phức tạp

## Troubleshooting

### Lỗi: Module not found

```bash
pip install -r requirements.txt
```

### Lỗi: 401 Unauthorized

Check lại `MIRO_ACCESS_TOKEN` trong `.env`

### Lỗi: No nodes found

Board có thể trống hoặc không có items phù hợp. Thử:
1. Thêm sticky notes hoặc cards vào board
2. Verify BOARD_ID đúng

### Graph không connected

Một số nodes có thể isolated. Check lại connectors trên Miro.

## Advanced Usage

### Sử dụng trong Python code

```python
from src import MiroClient, MindmapParser, GraphConverter, ChatbotExporter

# Load từ Miro
client = MiroClient(access_token="...")
board_data = client.get_board_data("board_id")

# Parse và convert
parser = MindmapParser()
nodes, edges = parser.parse(board_data)

converter = GraphConverter(directed=True)
graph = converter.convert(nodes, edges)

# Export
exporter = ChatbotExporter(graph)
exporter.export_to_json("output.json", "dialogue_flow")
```

### Custom export format

Extend `ChatbotExporter` class:

```python
class MyExporter(ChatbotExporter):
    def export_my_format(self):
        # Your custom logic
        return {"format": "my_custom_format", ...}
```

## Next Steps

1. ✅ Chạy demo để hiểu workflow
2. ✅ Setup Miro API credentials
3. ✅ Tạo mindmap trên Miro
4. ✅ Chạy converter
5. ✅ Import vào chatbot platform của bạn

## Support

- 📖 Docs: [README.md](README.md)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/mindmap2graph/issues)
- 💡 Examples: Xem folder `examples/`

Happy chatbot building! 🤖
