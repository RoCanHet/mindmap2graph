"""Demo with mock Miro data (no API key required)."""
import sys
from pathlib import Path
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import MindmapParser, GraphConverter, ChatbotExporter


def create_mock_board_data():
    """Create mock Miro board data for demonstration."""
    return {
        "board_id": "demo_board",
        "items": [
            {
                "id": "node_1",
                "type": "sticky_note",
                "data": {"content": "Chào mừng! Tôi có thể giúp gì cho bạn?"},
                "position": {"x": 0, "y": 0},
                "style": {"fillColor": "light_yellow"}
            },
            {
                "id": "node_2",
                "type": "card",
                "data": {"title": "Đặt hàng online"},
                "position": {"x": 200, "y": 100},
                "style": {"fillColor": "light_blue"}
            },
            {
                "id": "node_3",
                "type": "card",
                "data": {"title": "Hỏi thông tin sản phẩm"},
                "position": {"x": 200, "y": -100},
                "style": {"fillColor": "light_green"}
            },
            {
                "id": "node_4",
                "type": "sticky_note",
                "data": {"content": "Chọn sản phẩm từ danh mục"},
                "position": {"x": 400, "y": 100},
                "style": {"fillColor": "light_yellow"}
            },
            {
                "id": "node_5",
                "type": "sticky_note",
                "data": {"content": "Cung cấp thông tin chi tiết sản phẩm"},
                "position": {"x": 400, "y": -100},
                "style": {"fillColor": "light_yellow"}
            },
            {
                "id": "node_6",
                "type": "card",
                "data": {"title": "Xác nhận đơn hàng"},
                "position": {"x": 600, "y": 100},
                "style": {"fillColor": "light_blue"}
            },
            {
                "id": "node_7",
                "type": "sticky_note",
                "data": {"content": "Cảm ơn! Còn gì khác tôi có thể giúp không?"},
                "position": {"x": 800, "y": 0},
                "style": {"fillColor": "light_pink"}
            },
        ],
        "connectors": [
            {
                "id": "conn_1",
                "startItem": {"id": "node_1"},
                "endItem": {"id": "node_2"},
                "captions": [{"content": "Muốn đặt hàng"}],
                "style": {"strokeColor": "blue"}
            },
            {
                "id": "conn_2",
                "startItem": {"id": "node_1"},
                "endItem": {"id": "node_3"},
                "captions": [{"content": "Hỏi về sản phẩm"}],
                "style": {"strokeColor": "green"}
            },
            {
                "id": "conn_3",
                "startItem": {"id": "node_2"},
                "endItem": {"id": "node_4"},
                "captions": [{"content": "Tiếp tục"}],
                "style": {"strokeColor": "blue"}
            },
            {
                "id": "conn_4",
                "startItem": {"id": "node_3"},
                "endItem": {"id": "node_5"},
                "captions": [{"content": "Xem chi tiết"}],
                "style": {"strokeColor": "green"}
            },
            {
                "id": "conn_5",
                "startItem": {"id": "node_4"},
                "endItem": {"id": "node_6"},
                "captions": [{"content": "Xác nhận"}],
                "style": {"strokeColor": "blue"}
            },
            {
                "id": "conn_6",
                "startItem": {"id": "node_6"},
                "endItem": {"id": "node_7"},
                "captions": [{"content": "Hoàn thành"}],
                "style": {"strokeColor": "blue"}
            },
            {
                "id": "conn_7",
                "startItem": {"id": "node_5"},
                "endItem": {"id": "node_7"},
                "captions": [{"content": "Kết thúc"}],
                "style": {"strokeColor": "green"}
            },
        ]
    }


def main():
    """Run demo with mock data."""
    print("=" * 70)
    print("DEMO: Miro Mindmap to Chatbot Graph Converter")
    print("(Using mock data - no API key required)")
    print("=" * 70)

    # Create mock data
    print("\n[1/5] Creating mock Miro board data...")
    board_data = create_mock_board_data()
    print(f"  ✓ Created mock board with {len(board_data['items'])} items")
    print(f"    and {len(board_data['connectors'])} connectors")

    # Parse mindmap
    print("\n[2/5] Parsing mindmap structure...")
    parser = MindmapParser()
    nodes, edges = parser.parse(board_data)
    summary = parser.get_summary()
    print(f"  ✓ Parsed {summary['total_nodes']} nodes and {summary['total_edges']} edges")
    print(f"    Node types: {summary['node_types']}")

    # Print nodes
    print("\n  Nodes:")
    for node_id, node in list(nodes.items())[:3]:
        print(f"    - {node_id}: {node.content[:50]}")
    if len(nodes) > 3:
        print(f"    ... and {len(nodes) - 3} more")

    # Convert to graph
    print("\n[3/5] Converting to graph structure...")
    converter = GraphConverter(directed=True)
    graph = converter.convert(nodes, edges)
    stats = converter.get_graph_stats()
    print(f"  ✓ Created directed graph:")
    print(f"    - Nodes: {stats['num_nodes']}")
    print(f"    - Edges: {stats['num_edges']}")
    print(f"    - Root nodes: {stats.get('num_root_nodes', 0)}")
    print(f"    - Leaf nodes: {stats.get('num_leaf_nodes', 0)}")
    print(f"    - Connected: {stats['is_connected']}")
    print(f"    - Avg degree: {stats.get('avg_degree', 0):.2f}")

    # Export to chatbot formats
    print("\n[4/5] Exporting to chatbot formats...")
    exporter = ChatbotExporter(graph)

    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Export dialogue flow
    print("\n  Exporting Dialogue Flow format...")
    dialogue_flow = exporter.export_dialogue_flow()
    output_path = output_dir / "demo_dialogue_flow.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dialogue_flow, f, indent=2, ensure_ascii=False)
    print(f"    ✓ Saved to {output_path}")
    print(f"      - Total states: {dialogue_flow['total_states']}")
    print(f"      - Entry points: {dialogue_flow['entry_points']}")

    # Export intent tree
    print("\n  Exporting Intent Tree format...")
    intent_tree = exporter.export_intent_tree()
    output_path = output_dir / "demo_intent_tree.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(intent_tree, f, indent=2, ensure_ascii=False)
    print(f"    ✓ Saved to {output_path}")
    print(f"      - Root intents: {intent_tree['num_root_intents']}")

    # Export scenario paths
    print("\n  Exporting Scenario Paths format...")
    scenarios = exporter.export_scenario_paths(max_depth=10)
    output_path = output_dir / "demo_scenario_paths.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(scenarios, f, indent=2, ensure_ascii=False)
    print(f"    ✓ Saved to {output_path}")
    print(f"      - Total scenarios: {scenarios['total_scenarios']}")

    # Show sample scenario
    if scenarios['total_scenarios'] > 0:
        sample = scenarios['scenarios'][0]
        print(f"\n  Sample Scenario #{sample['scenario_id']}:")
        print(f"    Length: {sample['length']} steps")
        print(f"    Path: {sample['start_node']} → {sample['end_node']}")
        for step in sample['steps'][:3]:
            print(f"      {step['step_number']}. {step['message'][:50]}...")

    # Export graph
    print("\n  Exporting graph file...")
    converter.export_graphml(str(output_dir / "demo_graph.graphml"))
    print(f"    ✓ Saved to {output_dir / 'demo_graph.graphml'}")

    # Generate summary
    print("\n[5/5] Summary...")
    summary = exporter.export_summary()
    print(f"  ✓ Chatbot Scenario Summary:")
    print(f"    - Total nodes: {summary['total_nodes']}")
    print(f"    - Total edges: {summary['total_edges']}")
    print(f"    - Entry points: {summary['entry_points']}")
    print(f"    - End points: {summary['end_points']}")
    print(f"    - Avg branching factor: {summary['avg_branching_factor']:.2f}")
    print(f"    - Node types: {summary['node_types']}")

    print("\n" + "=" * 70)
    print("✓ Demo completed successfully!")
    print(f"All files saved to: {output_dir.absolute()}/")
    print("=" * 70)

    print("\nNext steps:")
    print("1. Review the generated JSON files in output/")
    print("2. Set up your Miro API token in .env file")
    print("3. Run: python main.py --format all")


if __name__ == "__main__":
    main()
