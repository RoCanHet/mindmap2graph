# Miro Mindmap to Chatbot Graph Converter

Chuyển đổi mindmap từ Miro thành graph structure phục vụ thiết kế kịch bản chatbot.

## 🌟 Tính năng

- ✅ **Web UI** - Giao diện web đơn giản cho Product team (không cần code!)
- ✅ Kết nối Miro API để lấy dữ liệu mindmap
- ✅ Parse cấu trúc mindmap (nodes và connections)
- ✅ Chuyển đổi sang NetworkX graph
- ✅ Export nhiều format cho chatbot:
  - **Dialogue Flow**: Luồng hội thoại với states và transitions
  - **Intent Tree**: Cây phân cấp intents
  - **Scenario Paths**: Các kịch bản hội thoại hoàn chỉnh
- ✅ Export graph sang GraphML/GEXF để visualize
- ✅ **Export sang draw.io XML** - Visualize và edit diagram đẹp mắt! 🎨
- ✅ Demo data (test ngay không cần Miro API)
- ✅ Docker support - Deploy dễ dàng

## 🚀 Quick Start

### Option 1: Web UI (Khuyến nghị cho Product Team)

```bash
# Clone và chạy
git clone https://github.com/yourusername/mindmap2graph.git
cd mindmap2graph
chmod +x run.sh
./run.sh
# Chọn option 1 (Web UI)
```

Web sẽ mở tại: http://localhost:8501

**Features Web UI:**
- ✅ Upload JSON hoặc dùng demo data
- ✅ Connect với Miro API
- ✅ Xem preview graph statistics
- ✅ Export và download JSON ngay trên web
- ✅ Export draw.io XML để visualize diagram
- ✅ Không cần code!

👉 **Xem thêm**: [PRODUCT_TEAM_GUIDE.md](PRODUCT_TEAM_GUIDE.md) - Hướng dẫn cho Product team

### Option 2: Command Line (Cho Developers)

```bash
# Setup
pip install -r requirements.txt
cp .env.example .env
# Edit .env với token

# Run
python main.py --format all
```

### Option 3: Docker

```bash
docker-compose up
```

👉 **Xem thêm**: [DEPLOY.md](DEPLOY.md) - Hướng dẫn deploy lên cloud

## Cài đặt

### 1. Clone repository

```bash
git clone https://github.com/yourusername/mindmap2graph.git
cd mindmap2graph
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình Miro API

#### Lấy Access Token từ Miro:

1. Truy cập https://miro.com/app/settings/user-profile/apps
2. Tạo app mới hoặc chọn app có sẵn
3. Copy **Access Token**

#### Lấy Board ID:

1. Mở board Miro của bạn
2. Board ID nằm trong URL: `https://miro.com/app/board/{BOARD_ID}/`

#### Tạo file `.env`:

```bash
cp .env.example .env
```

Chỉnh sửa `.env` với thông tin của bạn:

```env
MIRO_ACCESS_TOKEN=your_miro_access_token_here
MIRO_BOARD_ID=your_board_id_here
```

## Sử dụng

### Cách 1: Web UI (Dễ nhất - Cho Product Team)

```bash
streamlit run app.py
```

Hoặc dùng script tự động:
```bash
./run.sh
# Chọn option 1
```

**Trong Web UI:**
1. Chọn phương thức: Upload JSON hoặc Connect Miro API
2. Load data (hoặc dùng demo data)
3. Xem preview statistics
4. Chọn format export
5. Click "Generate & Download"
6. Done!

👉 **Chi tiết**: [PRODUCT_TEAM_GUIDE.md](PRODUCT_TEAM_GUIDE.md)

### Cách 2: Command Line (Cho Developers)

```bash
# Export tất cả formats
python main.py

# Export format cụ thể
python main.py --format dialogue_flow
python main.py --format intent_tree
python main.py --format scenario_paths

# Export với graph file
python main.py --format all --export-graph

# Export draw.io XML (NEW!)
python main.py --export-drawio

# Export tất cả formats + draw.io
python main.py --format all --export-graph --export-drawio

# Chỉ định board ID khác
python main.py --board-id uXjVKbzXYZ0=

# Chỉ định output directory
python main.py --output-dir my_output
```

### Cách 3: Python Code

```python
from src import MiroClient, MindmapParser, GraphConverter, ChatbotExporter

# 1. Kết nối Miro
client = MiroClient(
    access_token="your_token",
    api_base_url="https://api.miro.com/v2"
)

# 2. Lấy dữ liệu board
board_data = client.get_board_data("your_board_id")

# 3. Parse mindmap
parser = MindmapParser()
nodes, edges = parser.parse(board_data)

# 4. Chuyển đổi sang graph
converter = GraphConverter(directed=True)
graph = converter.convert(nodes, edges)

# 5. Export cho chatbot
exporter = ChatbotExporter(graph)
exporter.export_to_json("output/chatbot_scenario.json", "dialogue_flow")
```

## Output Formats

### 1. Dialogue Flow Format

Format này biểu diễn luồng hội thoại với các states và transitions:

```json
{
  "format": "dialogue_flow",
  "version": "1.0",
  "entry_points": ["node_1"],
  "total_states": 5,
  "states": [
    {
      "state_id": "node_1",
      "message": "Xin chào! Tôi có thể giúp gì cho bạn?",
      "type": "sticky_note",
      "transitions": [
        {
          "target_state": "node_2",
          "condition": "Đặt hàng",
          "label": "Đặt hàng"
        },
        {
          "target_state": "node_3",
          "condition": "Hỏi thông tin",
          "label": "Hỏi thông tin"
        }
      ],
      "is_entry_point": true
    }
  ]
}
```

**Ứng dụng**: Phù hợp cho chatbot platform như Dialogflow, Rasa, hoặc custom chatbot framework.

### 2. Intent Tree Format

Format này biểu diễn cấu trúc phân cấp intents:

```json
{
  "format": "intent_tree",
  "version": "1.0",
  "num_root_intents": 1,
  "intent_trees": [
    {
      "intent_id": "root_1",
      "intent_name": "Chào hỏi",
      "type": "shape",
      "children": [
        {
          "intent_id": "child_1",
          "intent_name": "Hỏi tên",
          "transition_label": "Giới thiệu",
          "children": []
        }
      ]
    }
  ]
}
```

**Ứng dụng**: Thiết kế intent hierarchy cho NLU engines.

### 3. Scenario Paths Format

Format này chứa tất cả các kịch bản hội thoại có thể:

```json
{
  "format": "scenario_paths",
  "version": "1.0",
  "total_scenarios": 10,
  "scenarios": [
    {
      "scenario_id": "scenario_1",
      "length": 4,
      "start_node": "node_1",
      "end_node": "node_5",
      "steps": [
        {
          "step_number": 1,
          "node_id": "node_1",
          "message": "Xin chào",
          "type": "sticky_note",
          "transition": "Bắt đầu"
        }
      ]
    }
  ]
}
```

**Ứng dụng**: Testing chatbot, training conversation AI, generating test cases.

## Cấu trúc Project

```
mindmap2graph/
├── config.py              # Configuration management
├── main.py                # Main execution script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
│
├── src/
│   ├── __init__.py
│   ├── miro_client.py         # Miro API client
│   ├── mindmap_parser.py      # Mindmap parser
│   ├── graph_converter.py     # Graph converter
│   └── chatbot_exporter.py    # Chatbot scenario exporter
│
├── examples/
│   └── basic_usage.py         # Example usage
│
└── output/                    # Generated output files
    ├── chatbot_scenario_*.json
    └── graph.graphml
```

## API Classes

### MiroClient

Kết nối với Miro API để lấy dữ liệu board.

```python
client = MiroClient(access_token="...", api_base_url="...")

# Lấy tất cả items
items = client.get_board_items(board_id)

# Lấy connectors
connectors = client.get_board_connectors(board_id)

# Lấy toàn bộ board data
board_data = client.get_board_data(board_id)
```

### MindmapParser

Parse dữ liệu Miro thành nodes và edges.

```python
parser = MindmapParser()
nodes, edges = parser.parse(board_data)
summary = parser.get_summary()
```

### GraphConverter

Chuyển đổi nodes/edges thành NetworkX graph.

```python
converter = GraphConverter(directed=True)
graph = converter.convert(nodes, edges)

# Thống kê graph
stats = converter.get_graph_stats()

# Tìm paths giữa 2 nodes
paths = converter.find_paths(source_id, target_id)

# Lấy subgraph từ root
subgraph = converter.get_subgraph_from_root(root_id, max_depth=3)

# Export graph
converter.export_graphml("output/graph.graphml")
```

### ChatbotExporter

Export graph sang format phù hợp cho chatbot.

```python
exporter = ChatbotExporter(graph)

# Export dialogue flow
dialogue = exporter.export_dialogue_flow()

# Export intent tree
intents = exporter.export_intent_tree()

# Export scenarios
scenarios = exporter.export_scenario_paths(max_depth=10)

# Lưu file JSON
exporter.export_to_json("output.json", format="dialogue_flow")

# Tạo summary
summary = exporter.export_summary()
```

## Use Cases

### 1. Thiết kế Chatbot Flow

Product team vẽ mindmap conversation flow trên Miro → Export sang dialogue flow → Import vào chatbot platform.

### 2. Intent Mapping

Vẽ intent hierarchy trên Miro → Export intent tree → Training NLU model.

### 3. Test Scenario Generation

Mindmap các conversation paths → Export scenarios → Automated testing chatbot.

### 4. Documentation

Mindmap chatbot logic → Export graph + JSON → Documentation cho team.

## Miro Board Best Practices

Để có kết quả tốt nhất:

1. **Sử dụng Sticky Notes hoặc Cards** cho các dialogue states
2. **Sử dụng Connectors** (mũi tên) để kết nối các nodes
3. **Thêm labels vào connectors** để mô tả điều kiện chuyển state
4. **Tổ chức rõ ràng**: Entry points ở trên/trái, end points ở dưới/phải
5. **Nhóm theo intent**: Sử dụng frames để nhóm các intent liên quan

### Example Miro Structure:

```
[Chào hỏi] --"Bắt đầu"--> [Hỏi nhu cầu]
                              |
                   +----------+-----------+
                   |                      |
              "Đặt hàng"            "Hỏi thông tin"
                   |                      |
                   v                      v
           [Xử lý đơn hàng]        [Cung cấp info]
                   |                      |
                   v                      v
              [Xác nhận]              [Kết thúc]
```

## Troubleshooting

### Lỗi Authentication

```
Failed to fetch Miro data: 401 Unauthorized
```

**Giải pháp**: Kiểm tra lại `MIRO_ACCESS_TOKEN` trong file `.env`

### Lỗi Board ID không tồn tại

```
Failed to fetch Miro data: 404 Not Found
```

**Giải pháp**:
- Kiểm tra `MIRO_BOARD_ID` có đúng không
- Đảm bảo access token có quyền truy cập board này

### Graph không connected

```
is_connected: false
```

**Giải pháp**:
- Kiểm tra lại mindmap trên Miro có kết nối đầy đủ không
- Một số nodes có thể bị isolated (không có connector)

## Phát triển thêm

### Thêm export format mới

Tạo method mới trong `ChatbotExporter`:

```python
def export_custom_format(self) -> Dict[str, Any]:
    # Your custom logic here
    return {
        "format": "custom",
        "data": ...
    }
```

### Tích hợp với chatbot platform khác

Modify `chatbot_exporter.py` để support format của platform của bạn (Botpress, Landbot, etc.)

### Visualize graph

Sử dụng output GraphML với tools như:
- Gephi
- Cytoscape
- NetworkX visualization

```python
import matplotlib.pyplot as plt
import networkx as nx

# Visualize
pos = nx.spring_layout(graph)
nx.draw(graph, pos, with_labels=True)
plt.savefig("graph.png")
```

## Requirements

- Python 3.8+
- requests
- networkx
- python-dotenv
- pydantic

## License

MIT License

## 📚 Documentation

- **[README.md](README.md)** - Bạn đang đọc file này
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[PRODUCT_TEAM_GUIDE.md](PRODUCT_TEAM_GUIDE.md)** - Hướng dẫn cho Product team (không cần code)
- **[MIRO_SETUP.md](MIRO_SETUP.md)** - Chi tiết setup Miro API
- **[DRAWIO_GUIDE.md](DRAWIO_GUIDE.md)** - 🎨 Hướng dẫn export sang draw.io (NEW!)
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[DEPLOY.md](DEPLOY.md)** - Deployment guide (Docker, Cloud, etc.)

## 🐳 Deployment

### Local

```bash
./run.sh
```

### Docker

```bash
docker-compose up
```

### Cloud (Streamlit Cloud - Free!)

1. Push code lên GitHub
2. Go to https://streamlit.io/cloud
3. Connect repo và deploy
4. Done! Có URL public cho cả team dùng

👉 **Chi tiết**: [DEPLOY.md](DEPLOY.md)

## Đóng góp

Contributions are welcome! Please feel free to submit a Pull Request.

## Tác giả

Tạo cho use case: Chuyển đổi Miro mindmap sang graph structure phục vụ thiết kế kịch bản chatbot.

## Liên hệ

- Issues: [GitHub Issues](https://github.com/yourusername/mindmap2graph/issues)
- Miro API Docs: https://developers.miro.com/docs
- Streamlit Docs: https://docs.streamlit.io
