"""Streamlit Web UI for Miro to Chatbot Graph Converter.

Product team có thể sử dụng web interface này mà không cần code.
"""
import streamlit as st
import json
import sys
from pathlib import Path
import io

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src import MiroClient, MindmapParser, GraphConverter, ChatbotExporter, DrawIOExporter

# Page config
st.set_page_config(
    page_title="Miro to Chatbot Graph",
    page_icon="🤖",
    layout="wide",
)

# Title
st.title("🤖 Miro Mindmap → Chatbot Graph Converter")
st.markdown("Chuyển đổi Miro mindmap thành graph cho chatbot scenario design")

# Sidebar
st.sidebar.header("⚙️ Configuration")

# Method selection
method = st.sidebar.radio(
    "Chọn phương thức:",
    ["📁 Upload JSON file từ Miro", "🔗 Connect qua Miro API"],
    help="JSON file: Export từ Miro board | API: Kết nối trực tiếp"
)

st.sidebar.markdown("---")

board_data = None

# Method 1: Upload JSON file
if method == "📁 Upload JSON file từ Miro":
    st.header("📁 Upload Miro Board JSON")

    st.info("""
    **Cách export JSON từ Miro:**
    1. Mở board Miro của bạn
    2. Click "..." menu → "Export"
    3. Chọn "JSON" format
    4. Download file và upload ở đây

    **Hoặc sử dụng demo data bằng cách bỏ qua bước này**
    """)

    uploaded_file = st.file_uploader(
        "Upload Miro board JSON file",
        type=['json'],
        help="File JSON export từ Miro board"
    )

    if uploaded_file is not None:
        try:
            board_data = json.load(uploaded_file)
            st.success(f"✅ Đã load file: {uploaded_file.name}")
        except Exception as e:
            st.error(f"❌ Lỗi đọc file: {e}")
    else:
        # Use demo data
        if st.button("🎮 Sử dụng Demo Data (không cần upload)"):
            st.session_state['use_demo'] = True

    if 'use_demo' in st.session_state and st.session_state['use_demo']:
        # Create demo data
        board_data = {
            "board_id": "demo_board",
            "items": [
                {
                    "id": "node_1",
                    "type": "sticky_note",
                    "data": {"content": "Chào mừng! Tôi có thể giúp gì cho bạn?"},
                    "position": {"x": 0, "y": 0},
                },
                {
                    "id": "node_2",
                    "type": "card",
                    "data": {"title": "Đặt hàng online"},
                    "position": {"x": 200, "y": 100},
                },
                {
                    "id": "node_3",
                    "type": "card",
                    "data": {"title": "Hỏi thông tin sản phẩm"},
                    "position": {"x": 200, "y": -100},
                },
                {
                    "id": "node_4",
                    "type": "sticky_note",
                    "data": {"content": "Chọn sản phẩm từ danh mục"},
                    "position": {"x": 400, "y": 100},
                },
                {
                    "id": "node_5",
                    "type": "sticky_note",
                    "data": {"content": "Cung cấp thông tin chi tiết sản phẩm"},
                    "position": {"x": 400, "y": -100},
                },
                {
                    "id": "node_6",
                    "type": "card",
                    "data": {"title": "Xác nhận đơn hàng"},
                    "position": {"x": 600, "y": 100},
                },
                {
                    "id": "node_7",
                    "type": "sticky_note",
                    "data": {"content": "Cảm ơn! Còn gì khác không?"},
                    "position": {"x": 800, "y": 0},
                },
            ],
            "connectors": [
                {"id": "c1", "startItem": {"id": "node_1"}, "endItem": {"id": "node_2"}, "captions": [{"content": "Muốn đặt hàng"}]},
                {"id": "c2", "startItem": {"id": "node_1"}, "endItem": {"id": "node_3"}, "captions": [{"content": "Hỏi sản phẩm"}]},
                {"id": "c3", "startItem": {"id": "node_2"}, "endItem": {"id": "node_4"}, "captions": [{"content": "Tiếp tục"}]},
                {"id": "c4", "startItem": {"id": "node_3"}, "endItem": {"id": "node_5"}, "captions": [{"content": "Chi tiết"}]},
                {"id": "c5", "startItem": {"id": "node_4"}, "endItem": {"id": "node_6"}, "captions": [{"content": "Xác nhận"}]},
                {"id": "c6", "startItem": {"id": "node_6"}, "endItem": {"id": "node_7"}, "captions": [{"content": "Hoàn thành"}]},
                {"id": "c7", "startItem": {"id": "node_5"}, "endItem": {"id": "node_7"}, "captions": [{"content": "Kết thúc"}]},
            ]
        }
        st.success("✅ Đang sử dụng Demo Data")

# Method 2: Miro API
else:
    st.header("🔗 Kết nối với Miro API")

    with st.expander("📖 Hướng dẫn lấy Miro API Token", expanded=False):
        st.markdown("""
        ### Bước 1: Tạo Miro App
        1. Truy cập: https://miro.com/app/settings/user-profile/apps
        2. Click **"Create new app"**
        3. Nhập tên app (ví dụ: "Chatbot Converter")
        4. Click **"Create"**

        ### Bước 2: Lấy Access Token
        1. Trong app vừa tạo, scroll xuống phần **"OAuth scopes"**
        2. Enable các permissions:
           - `boards:read` (đọc board data)
        3. Click **"Install app and get OAuth token"**
        4. Copy **Access Token** (token dài bắt đầu bằng `M...`)

        ### Bước 3: Lấy Board ID
        1. Mở board Miro bạn muốn convert
        2. Copy ID từ URL: `https://miro.com/app/board/{BOARD_ID}/`
        3. Ví dụ: `uXjVKbzXYZ0=` là board ID
        """)

    col1, col2 = st.columns(2)

    with col1:
        access_token = st.text_input(
            "Miro Access Token",
            type="password",
            help="Token từ Miro app settings"
        )

    with col2:
        board_id = st.text_input(
            "Board ID",
            help="ID từ URL của Miro board"
        )

    if st.button("🔄 Fetch Board Data"):
        if not access_token or not board_id:
            st.error("❌ Vui lòng nhập cả Access Token và Board ID")
        else:
            with st.spinner("Đang kết nối với Miro..."):
                try:
                    client = MiroClient(access_token=access_token)
                    board_data = client.get_board_data(board_id)
                    st.success(f"✅ Đã fetch {len(board_data['items'])} items và {len(board_data['connectors'])} connectors")
                except Exception as e:
                    st.error(f"❌ Lỗi kết nối Miro: {e}")
                    st.info("Kiểm tra lại token và board ID. Đảm bảo app có quyền truy cập board.")

# Process data if available
if board_data:
    st.markdown("---")
    st.header("🔄 Processing")

    # Parse mindmap
    with st.spinner("Parsing mindmap..."):
        parser = MindmapParser()
        nodes, edges = parser.parse(board_data)
        summary = parser.get_summary()

    # Show summary
    col1, col2, col3 = st.columns(3)
    col1.metric("📍 Nodes", summary['total_nodes'])
    col2.metric("🔗 Edges", summary['total_edges'])
    col3.metric("📊 Node Types", len(summary['node_types']))

    with st.expander("📋 Chi tiết Nodes", expanded=False):
        for node_id, node in list(nodes.items())[:10]:
            st.markdown(f"- **{node_id}**: {node.content}")
        if len(nodes) > 10:
            st.markdown(f"_... và {len(nodes) - 10} nodes khác_")

    # Convert to graph
    with st.spinner("Converting to graph..."):
        converter = GraphConverter(directed=True)
        graph = converter.convert(nodes, edges)
        stats = converter.get_graph_stats()

    # Show graph stats
    st.subheader("📊 Graph Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎯 Root Nodes", stats.get('num_root_nodes', 0))
    col2.metric("🏁 Leaf Nodes", stats.get('num_leaf_nodes', 0))
    col3.metric("🔗 Avg Degree", f"{stats.get('avg_degree', 0):.2f}")
    col4.metric("✅ Connected", "Yes" if stats.get('is_connected') else "No")

    # Export options
    st.markdown("---")
    st.header("📤 Export")

    export_format = st.selectbox(
        "Chọn format export:",
        ["dialogue_flow", "intent_tree", "scenario_paths", "all"],
        format_func=lambda x: {
            "dialogue_flow": "💬 Dialogue Flow (state machine)",
            "intent_tree": "🌳 Intent Tree (hierarchy)",
            "scenario_paths": "🛤️ Scenario Paths (test cases)",
            "all": "📦 All Formats"
        }[x]
    )

    # Export button
    if st.button("📥 Generate & Download"):
        with st.spinner("Exporting..."):
            exporter = ChatbotExporter(graph)

            # Generate data
            if export_format == "dialogue_flow":
                data = exporter.export_dialogue_flow()
            elif export_format == "intent_tree":
                data = exporter.export_intent_tree()
            elif export_format == "scenario_paths":
                data = exporter.export_scenario_paths()
            else:  # all
                data = {
                    "dialogue_flow": exporter.export_dialogue_flow(),
                    "intent_tree": exporter.export_intent_tree(),
                    "scenario_paths": exporter.export_scenario_paths(),
                }

            # Convert to JSON
            json_str = json.dumps(data, indent=2, ensure_ascii=False)

            # Download button
            st.download_button(
                label="⬇️ Download JSON",
                data=json_str,
                file_name=f"chatbot_scenario_{export_format}.json",
                mime="application/json",
            )

            st.success("✅ Export hoàn thành!")

            # Show preview
            with st.expander("👀 Preview JSON", expanded=False):
                st.json(data)

            # Show summary
            st.subheader("📊 Export Summary")
            export_summary = exporter.export_summary()
            col1, col2, col3 = st.columns(3)
            col1.metric("Total States", export_summary['total_nodes'])
            col2.metric("Entry Points", export_summary['entry_points'])
            col3.metric("End Points", export_summary['end_points'])

    # Draw.io XML export
    st.markdown("---")
    st.subheader("🎨 Export cho draw.io")
    st.info("Export graph sang định dạng XML để import vào draw.io và visualize")

    if st.button("📥 Export draw.io XML"):
        with st.spinner("Generating draw.io XML..."):
            drawio_exporter = DrawIOExporter(graph)
            xml_content = drawio_exporter.export_to_drawio_xml()

            # Download button
            st.download_button(
                label="⬇️ Download draw.io XML",
                data=xml_content,
                file_name="chatbot_graph_drawio.xml",
                mime="application/xml",
            )

            st.success("✅ Draw.io XML export hoàn thành!")

            # Show stats
            stats = drawio_exporter.get_export_stats()
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Nodes", stats['total_nodes'])
            col2.metric("Total Edges", stats['total_edges'])
            col3.metric("Total Cells", stats['total_cells'])

            # Show instructions
            with st.expander("📖 Hướng dẫn import vào draw.io", expanded=True):
                st.markdown("""
                ### Cách import file XML vào draw.io:

                1. **Mở draw.io**: Truy cập https://app.diagrams.net hoặc https://draw.io
                2. **Import file**:
                   - Click **File** → **Open from** → **Device**
                   - Chọn file XML vừa download
                   - Hoặc kéo thả file XML vào draw.io
                3. **Xem graph**: Graph sẽ hiển thị với:
                   - 🟨 Sticky notes (màu vàng)
                   - 🟦 Cards (màu xanh)
                   - 🟩 Shapes (màu xanh lá)
                   - Mũi tên kết nối với labels
                4. **Edit**: Bạn có thể edit, rearrange, export sang PNG/PDF/SVG

                **Tip**: Dùng **Arrange** → **Layout** để auto-arrange nodes đẹp hơn!
                """)

            # Show preview
            with st.expander("👀 Preview XML", expanded=False):
                st.code(xml_content[:2000] + "\n...(truncated)", language="xml")

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Tips")
st.sidebar.markdown("""
**Best Practices:**
- Sử dụng Sticky Notes cho dialogue states
- Connect bằng arrows
- Thêm labels vào arrows
- Tổ chức từ trái → phải hoặc trên → dưới
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Documentation")
st.sidebar.markdown("""
- [README](README.md)
- [Quick Start](QUICKSTART.md)
- [Architecture](ARCHITECTURE.md)
""")
