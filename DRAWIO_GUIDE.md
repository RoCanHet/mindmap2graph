# Draw.io Export Guide

Hướng dẫn export Miro mindmap sang draw.io XML để visualize và edit.

## 🎯 Tại sao export sang draw.io?

- **Visualize**: Xem graph dưới dạng diagram đẹp mắt
- **Edit**: Tùy chỉnh layout, colors, shapes
- **Share**: Export sang PNG, PDF, SVG để share với team
- **Present**: Tạo presentation từ diagram
- **Document**: Tạo documentation với diagram chất lượng cao

---

## 🚀 Quick Start

### Option 1: Web UI (Dễ nhất)

1. **Chạy web UI**:
   ```bash
   streamlit run app.py
   ```

2. **Load board data**:
   - Upload JSON hoặc
   - Connect Miro API hoặc
   - Dùng demo data

3. **Export**:
   - Scroll xuống section "🎨 Export cho draw.io"
   - Click **"📥 Export draw.io XML"**
   - Click **"⬇️ Download draw.io XML"**

4. **Import vào draw.io**:
   - Mở https://app.diagrams.net
   - File → Open from → Device
   - Chọn file XML vừa download

### Option 2: Command Line

```bash
# Export cùng với chatbot formats
python main.py --format all --export-drawio

# Chỉ export draw.io XML
python main.py --export-drawio

# Output sẽ ở: output/graph_drawio.xml
```

### Option 3: Python Code

```python
from src import MiroClient, MindmapParser, GraphConverter, DrawIOExporter

# 1. Fetch and parse
client = MiroClient(access_token="...")
board_data = client.get_board_data("board_id")

parser = MindmapParser()
nodes, edges = parser.parse(board_data)

converter = GraphConverter(directed=True)
graph = converter.convert(nodes, edges)

# 2. Export to draw.io XML
drawio_exporter = DrawIOExporter(graph)
drawio_exporter.save_to_file("output/my_graph.xml")

# Done! File saved to output/my_graph.xml
```

---

## 📖 Import vào draw.io

### Bước 1: Mở draw.io

Có 3 cách:
- **Online**: https://app.diagrams.net (khuyến nghị)
- **Desktop**: Download tại https://github.com/jgraph/drawio-desktop
- **VS Code**: Install extension "Draw.io Integration"

### Bước 2: Import file XML

**Cách 1: Menu**
1. Click **File** → **Open from** → **Device**
2. Chọn file `graph_drawio.xml`
3. Click **Open**

**Cách 2: Drag & Drop**
1. Kéo file XML vào cửa sổ draw.io
2. Drop vào canvas
3. Done!

### Bước 3: Xem graph

Graph sẽ hiển thị với:
- 🟨 **Sticky notes** - Màu vàng
- 🟦 **Cards** - Màu xanh dương
- 🟩 **Shapes** - Màu xanh lá
- ➡️ **Arrows** - Mũi tên với labels

---

## ✏️ Edit trong draw.io

### Rearrange Layout

**Auto-arrange** (Khuyến nghị):
1. Select All (Ctrl+A / Cmd+A)
2. Click **Arrange** → **Layout**
3. Chọn layout:
   - **Horizontal Flow**: Trái → Phải
   - **Vertical Flow**: Trên → Dưới
   - **Organic**: Tự động
   - **Circle**: Hình tròn

**Manual arrange**:
- Drag nodes để di chuyển
- Use grid (View → Grid) để align đẹp
- Use snap (View → Snap to) để snap vào grid

### Change Colors

**Thay đổi màu node**:
1. Select node
2. Click **Style** tab bên phải
3. Chọn:
   - **Fill**: Màu nền
   - **Line**: Màu viền
   - **Font**: Màu chữ

**Batch change**:
1. Select multiple nodes (Ctrl+Click)
2. Change style → apply cho tất cả

### Change Shapes

**Thay đổi shape**:
1. Select node
2. Right-click → **Edit Style**
3. Change `shape=` value:
   - `rectangle` - Hình chữ nhật
   - `ellipse` - Hình tròn
   - `rhombus` - Hình thoi
   - `hexagon` - Hình lục giác
   - `cloud` - Hình mây

### Add More Elements

**Add new nodes**:
- Drag từ sidebar trái
- Shapes: General, Flowchart, UML, etc.

**Add text**:
- Double-click node để edit text
- Insert → Text để add text box

**Add images**:
- Insert → Image
- Upload hoặc paste URL

### Style Connectors

**Arrow style**:
1. Select arrow
2. Style tab → Change:
   - **Line**: Straight, Curved, Orthogonal
   - **Arrow**: None, Classic, Block, Diamond
   - **Color**: Line color
   - **Width**: Line thickness

**Add waypoints**:
- Click arrow → Drag waypoint để thay đổi đường đi

---

## 📤 Export từ draw.io

### Export PNG (Cho presentations)

1. File → Export as → PNG
2. Chọn options:
   - **Zoom**: 100% - 200% (khuyến nghị 150%)
   - **Border**: 10-20px
   - **Transparent**: Tick nếu muốn background trong suốt
3. Click **Export**
4. Save file

**Use cases**: Slides, documents, website

### Export PDF (Cho printing)

1. File → Export as → PDF
2. Options:
   - **All pages**: Nếu có nhiều pages
   - **Fit to**: One page hoặc multiple pages
3. Export

**Use cases**: Documentation, reports, printing

### Export SVG (Cho web)

1. File → Export as → SVG
2. Options:
   - **Include copy of diagram**: Tick để embed source
   - **Links**: Open in same/new window
3. Export

**Use cases**: Websites, scaling graphics

### Export as XML (Backup)

1. File → Save as
2. Chọn location
3. Save

**Use cases**: Backup, version control

---

## 🎨 Styling Tips

### Color Schemes

**Professional**:
```
Background: #ffffff
Primary: #0066cc (Blue)
Secondary: #00cc66 (Green)
Accent: #ff9900 (Orange)
Text: #333333
```

**Pastel**:
```
Background: #f5f5f5
Primary: #a8dadc (Light blue)
Secondary: #f1faee (Cream)
Accent: #e63946 (Red)
Text: #1d3557 (Dark blue)
```

**Dark Mode**:
```
Background: #1e1e1e
Primary: #569cd6 (Blue)
Secondary: #4ec9b0 (Teal)
Accent: #ce9178 (Orange)
Text: #d4d4d4
```

### Font Recommendations

- **Titles**: Arial, Helvetica (14-16pt, Bold)
- **Body**: Arial, Verdana (11-12pt)
- **Labels**: Arial (10pt)

### Layout Best Practices

✅ **DO**:
- Use consistent spacing (40-60px between nodes)
- Align nodes to grid
- Use orthogonal connectors for clarity
- Group related nodes
- Use colors to distinguish types
- Add legends if needed

❌ **DON'T**:
- Overlap nodes
- Cross arrows unnecessarily
- Use too many colors (max 5)
- Make text too small (<10pt)
- Over-complicate layout

---

## 🔧 Advanced Features

### Layers

Use layers để organize complex diagrams:
1. View → Layers
2. Create new layer
3. Move objects between layers
4. Show/hide layers

### Pages

Multiple pages cho large flows:
1. Insert → Page
2. Navigate với page tabs
3. Link pages together

### Custom Libraries

Create custom shape libraries:
1. File → New Library
2. Drag shapes vào library
3. Save library
4. Share với team

### Embed Links

Add clickable links:
1. Select object
2. Right-click → Edit Link
3. Add URL
4. Links work trong PNG export (nếu tick option)

---

## 🤝 Collaboration

### Share với Team

**Option 1: Export file**
- Export XML và share file
- Team import vào draw.io của họ

**Option 2: Google Drive**
- Save to Google Drive (nếu dùng online)
- Share link với view/edit permissions

**Option 3: Export image**
- Export PNG/PDF
- Share qua email/Slack

### Version Control

**Git**:
```bash
git add output/graph_drawio.xml
git commit -m "Update chatbot flow diagram"
git push
```

**Manual**:
- Save versions với timestamp
- `graph_v1_2024-01-15.xml`
- `graph_v2_2024-01-20.xml`

---

## 🐛 Troubleshooting

### File không import được

**Giải pháp**:
1. Check file có đúng format XML không (mở bằng text editor)
2. Thử browser khác (Chrome recommended)
3. Thử desktop app thay vì online
4. Re-export từ tool

### Layout bị lỗi

**Giải pháp**:
1. Select All → Arrange → Layout
2. Manually adjust waypoints
3. Use "Clear Waypoints" nếu arrows rối
4. Reset zoom (View → Zoom → 100%)

### Mất text khi export PNG

**Giải pháp**:
1. Check font có được embed không
2. Tăng DPI khi export (150-200%)
3. Use PDF thay vì PNG
4. Check "Include text" option

### File quá lớn

**Giải pháp**:
1. Split thành multiple pages
2. Simplify diagram (remove unnecessary details)
3. Use lower resolution khi export
4. Compress với online tools

---

## 📊 Use Cases

### 1. Chatbot Flow Documentation

**Before** (Miro):
- Collaborative mindmapping
- Fast ideation
- Product team friendly

**After** (draw.io):
- Professional diagrams
- Ready cho documentation
- Export cho presentations

### 2. Technical Architecture

- Convert conversation flow → Technical diagram
- Add technical details (APIs, databases)
- Share với engineering team

### 3. Presentations

- Export beautiful diagrams
- Add to Google Slides / PowerPoint
- Present to stakeholders

### 4. User Journey Maps

- Visualize user paths
- Color-code by user type
- Export for UX documentation

---

## 💡 Pro Tips

### Tip 1: Use Templates

draw.io có nhiều templates:
- Flowcharts
- UML diagrams
- Network diagrams
- Mind maps

Apply template style lên graph của bạn.

### Tip 2: Keyboard Shortcuts

Essential shortcuts:
- `Ctrl+D`: Duplicate
- `Ctrl+G`: Group
- `Ctrl+Shift+G`: Ungroup
- `Ctrl+Z`: Undo
- `Alt+Shift+Arrow`: Move 1px

### Tip 3: Smart Connectors

- Hover over node edge → drag để tạo arrow
- Hold `Alt` khi connect → straight line
- Double-click connector → add waypoint

### Tip 4: Copy Style

1. Select node with style you want
2. Right-click → Copy Style
3. Select target nodes
4. Right-click → Paste Style

### Tip 5: Search & Replace

- Edit → Find/Replace
- Search text trong nodes
- Batch replace

---

## 🎓 Learning Resources

**Official**:
- draw.io Documentation: https://www.diagrams.net/doc/
- Video tutorials: https://www.youtube.com/c/drawio

**Community**:
- Reddit: r/drawio
- Stack Overflow: [draw.io tag]

---

## ✅ Checklist

Trước khi export sang draw.io:
- [ ] Board đã có đầy đủ nodes và connectors
- [ ] Labels đã được add vào arrows
- [ ] Node content rõ ràng và đầy đủ

Sau khi import vào draw.io:
- [ ] Tất cả nodes đã hiển thị đúng
- [ ] Arrows kết nối đúng
- [ ] Labels đã hiển thị
- [ ] Layout arrange đẹp mắt
- [ ] Colors/styles đã customize
- [ ] Export file backup (XML)
- [ ] Export PNG/PDF nếu cần

---

## 🎉 Next Steps

1. ✅ Export graph từ Miro
2. ✅ Import vào draw.io
3. ✅ Auto-arrange layout
4. ✅ Customize colors/styles
5. ✅ Add additional details
6. ✅ Export PNG/PDF
7. ✅ Share với team!

Happy diagramming! 🎨📊
