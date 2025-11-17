# Graph to draw.io XML Converter

Convert graph data (nodes and edges) to draw.io XML format for visualization.

## 🎯 What it does

Takes JSON data with graph structure → Converts to draw.io XML → Import vào draw.io để visualize

## 🚀 Quick Start

### Install

```bash
pip install -r requirements.txt
```

### Usage

```bash
# Convert JSON file to draw.io XML
python convert_to_drawio.py input.json -o output.xml

# Then import output.xml into draw.io
```

## 📖 Input Format

Your JSON file should have this structure:

```json
{
  "items": [
    {
      "id": "node_1",
      "type": "sticky_note",
      "data": {"content": "Node text"},
      "position": {"x": 0, "y": 0}
    },
    {
      "id": "node_2",
      "type": "card",
      "data": {"title": "Another node"},
      "position": {"x": 200, "y": 100}
    }
  ],
  "connectors": [
    {
      "id": "edge_1",
      "startItem": {"id": "node_1"},
      "endItem": {"id": "node_2"},
      "captions": [{"content": "Edge label"}]
    }
  ]
}
```

### Node Types & Colors

- **sticky_note** → 🟨 Yellow (#fff2cc)
- **card** → 🟦 Blue (#dae8fc)
- **shape** → 🟩 Green (#d5e8d4)
- **unknown** → ⬜ Gray (#f5f5f5)

## 📝 Example

See `examples/export_drawio.py` for a complete example with demo data:

```bash
python examples/export_drawio.py
```

This will create `output/chatbot_graph_drawio.xml`

## 🎨 Import to draw.io

1. Open https://app.diagrams.net
2. **File** → **Open from** → **Device**
3. Select your `.xml` file
4. Graph displays with colored nodes and arrows
5. Edit, rearrange, export to PNG/PDF/SVG

**Tip**: Use **Arrange** → **Layout** → **Horizontal Flow** to auto-arrange nodes

## 🔧 Advanced Usage

### Python API

```python
from src import MindmapParser, GraphConverter, DrawIOExporter
import json

# Load your data
with open('input.json') as f:
    data = json.load(f)

# Parse
parser = MindmapParser()
nodes, edges = parser.parse(data)

# Convert to graph
converter = GraphConverter(directed=True)
graph = converter.convert(nodes, edges)

# Export to draw.io XML
exporter = DrawIOExporter(graph)
exporter.save_to_file('output.xml')
```

### Customize Node Colors

Edit `src/drawio_exporter.py`:

```python
def _get_node_color(self, node_type: str) -> tuple:
    color_map = {
        "my_type": ("#custom_fill", "#custom_stroke"),
    }
    return color_map.get(node_type, ("#ffffff", "#000000"))
```

## 📚 Documentation

- **[README.md](README.md)** - This file
- **[DRAWIO_GUIDE.md](DRAWIO_GUIDE.md)** - Complete draw.io usage guide

## 🛠️ Code Structure

```
.
├── convert_to_drawio.py       # Main converter script
├── src/
│   ├── mindmap_parser.py      # Parse JSON to nodes/edges
│   ├── graph_converter.py     # Convert to NetworkX graph
│   └── drawio_exporter.py     # Export to draw.io XML
└── examples/
    └── export_drawio.py       # Example with demo data
```

## ⚙️ How it works

```
JSON Input
   ↓
Parse nodes & edges (MindmapParser)
   ↓
Create NetworkX graph (GraphConverter)
   ↓
Generate draw.io XML (DrawIOExporter)
   ↓
XML Output
```

## 🎨 draw.io Features

The generated XML includes:

- ✅ Nodes with proper positioning
- ✅ Color-coded by type
- ✅ Edge labels
- ✅ Orthogonal connectors
- ✅ Proper sizing based on content
- ✅ Compatible with draw.io online & desktop

## 🐛 Troubleshooting

### File won't import to draw.io

- Check XML is valid: `cat output.xml`
- Try different browser (Chrome recommended)
- Use draw.io desktop app

### Nodes overlap

- Use draw.io's **Arrange** → **Layout**
- Manually drag to reposition

### Missing labels

- Check your input JSON has `captions` in connectors
- Labels might be hidden if too long

## 📦 Requirements

- Python 3.8+
- networkx (for graph operations)

## 🤝 Contributing

Feel free to submit issues or pull requests.
