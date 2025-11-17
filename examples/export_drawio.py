"""Example: Export Miro mindmap to draw.io XML format."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import MiroClient, MindmapParser, GraphConverter, DrawIOExporter


def create_demo_board_data():
    """Create demo Miro board data."""
    return {
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
                "data": {"content": "Cảm ơn! Còn gì khác tôi có thể giúp không?"},
                "position": {"x": 800, "y": 0},
            },
        ],
        "connectors": [
            {
                "id": "conn_1",
                "startItem": {"id": "node_1"},
                "endItem": {"id": "node_2"},
                "captions": [{"content": "Muốn đặt hàng"}],
            },
            {
                "id": "conn_2",
                "startItem": {"id": "node_1"},
                "endItem": {"id": "node_3"},
                "captions": [{"content": "Hỏi về sản phẩm"}],
            },
            {
                "id": "conn_3",
                "startItem": {"id": "node_2"},
                "endItem": {"id": "node_4"},
                "captions": [{"content": "Tiếp tục"}],
            },
            {
                "id": "conn_4",
                "startItem": {"id": "node_3"},
                "endItem": {"id": "node_5"},
                "captions": [{"content": "Xem chi tiết"}],
            },
            {
                "id": "conn_5",
                "startItem": {"id": "node_4"},
                "endItem": {"id": "node_6"},
                "captions": [{"content": "Xác nhận"}],
            },
            {
                "id": "conn_6",
                "startItem": {"id": "node_6"},
                "endItem": {"id": "node_7"},
                "captions": [{"content": "Hoàn thành"}],
            },
            {
                "id": "conn_7",
                "startItem": {"id": "node_5"},
                "endItem": {"id": "node_7"},
                "captions": [{"content": "Kết thúc"}],
            },
        ]
    }


def main():
    """Main function to export draw.io XML."""
    print("=" * 70)
    print("Export Miro Mindmap to draw.io XML")
    print("=" * 70)

    # Step 1: Create demo board data
    print("\n[1/4] Creating demo board data...")
    board_data = create_demo_board_data()
    print(f"  ✓ Created board with {len(board_data['items'])} items")

    # Step 2: Parse mindmap
    print("\n[2/4] Parsing mindmap...")
    parser = MindmapParser()
    nodes, edges = parser.parse(board_data)
    print(f"  ✓ Parsed {len(nodes)} nodes and {len(edges)} edges")

    # Step 3: Convert to graph
    print("\n[3/4] Converting to graph...")
    converter = GraphConverter(directed=True)
    graph = converter.convert(nodes, edges)
    stats = converter.get_graph_stats()
    print(f"  ✓ Created graph with {stats['num_nodes']} nodes and {stats['num_edges']} edges")

    # Step 4: Export to draw.io XML
    print("\n[4/4] Exporting to draw.io XML...")
    drawio_exporter = DrawIOExporter(graph)

    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Save to file
    output_path = output_dir / "chatbot_graph_drawio.xml"
    drawio_exporter.save_to_file(str(output_path))

    # Get stats
    export_stats = drawio_exporter.get_export_stats()
    print(f"  ✓ Exported to {output_path}")
    print(f"    - Total nodes: {export_stats['total_nodes']}")
    print(f"    - Total edges: {export_stats['total_edges']}")
    print(f"    - Total cells: {export_stats['total_cells']}")
    print(f"    - Node types: {export_stats['node_types']}")

    print("\n" + "=" * 70)
    print("✓ Export completed!")
    print("=" * 70)

    print("\nNhững gì có thể làm tiếp:")
    print("1. Mở file XML trong draw.io:")
    print("   - Truy cập: https://app.diagrams.net")
    print("   - File → Open from → Device")
    print("   - Chọn file: output/chatbot_graph_drawio.xml")
    print("")
    print("2. Edit và customize:")
    print("   - Rearrange nodes")
    print("   - Change colors")
    print("   - Add more shapes")
    print("   - Export to PNG/PDF/SVG")
    print("")
    print("3. Auto-arrange:")
    print("   - Arrange → Layout → Horizontal/Vertical Flow")
    print("")


if __name__ == "__main__":
    main()
