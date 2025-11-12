"""Basic usage example for Miro to Graph converter."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import MiroClient, MindmapParser, GraphConverter, ChatbotExporter


def main():
    """Basic usage example."""
    # Step 1: Initialize Miro client
    print("Step 1: Connecting to Miro...")
    miro_client = MiroClient(
        access_token="YOUR_ACCESS_TOKEN_HERE",
        api_base_url="https://api.miro.com/v2"
    )

    # Step 2: Fetch board data
    print("Step 2: Fetching board data...")
    board_id = "YOUR_BOARD_ID_HERE"
    board_data = miro_client.get_board_data(board_id)
    print(f"  Found {len(board_data['items'])} items and {len(board_data['connectors'])} connectors")

    # Step 3: Parse mindmap
    print("\nStep 3: Parsing mindmap...")
    parser = MindmapParser()
    nodes, edges = parser.parse(board_data)
    print(f"  Parsed {len(nodes)} nodes and {len(edges)} edges")

    # Print summary
    summary = parser.get_summary()
    print(f"  Node types: {summary['node_types']}")

    # Step 4: Convert to graph
    print("\nStep 4: Converting to graph...")
    converter = GraphConverter(directed=True)
    graph = converter.convert(nodes, edges)
    stats = converter.get_graph_stats()
    print(f"  Graph has {stats['num_nodes']} nodes and {stats['num_edges']} edges")

    # Step 5: Export to chatbot format
    print("\nStep 5: Exporting to chatbot format...")
    exporter = ChatbotExporter(graph)

    # Export dialogue flow
    dialogue_flow = exporter.export_dialogue_flow()
    print(f"  Dialogue flow has {dialogue_flow['total_states']} states")
    print(f"  Entry points: {dialogue_flow['entry_points']}")

    # Export intent tree
    intent_tree = exporter.export_intent_tree()
    print(f"  Intent tree has {intent_tree['num_root_intents']} root intents")

    # Export scenario paths
    scenarios = exporter.export_scenario_paths()
    print(f"  Generated {scenarios['total_scenarios']} conversation scenarios")

    # Save to files
    print("\nStep 6: Saving to files...")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    exporter.export_to_json(str(output_dir / "dialogue_flow.json"), "dialogue_flow")
    exporter.export_to_json(str(output_dir / "intent_tree.json"), "intent_tree")
    exporter.export_to_json(str(output_dir / "scenario_paths.json"), "scenario_paths")

    print(f"  All files saved to {output_dir}/")
    print("\n✓ Done!")


if __name__ == "__main__":
    main()
