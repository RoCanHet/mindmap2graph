"""Main script for converting Miro mindmap to chatbot graph."""
import argparse
import logging
import sys
from pathlib import Path

from config import get_settings
from src import MiroClient, MindmapParser, GraphConverter, ChatbotExporter, DrawIOExporter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Convert Miro mindmap to chatbot scenario graph"
    )
    parser.add_argument(
        "--board-id",
        type=str,
        help="Miro board ID (overrides .env)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Output directory for generated files",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["dialogue_flow", "intent_tree", "scenario_paths", "all"],
        default="all",
        help="Export format for chatbot scenario",
    )
    parser.add_argument(
        "--export-graph",
        action="store_true",
        help="Also export graph in GraphML format",
    )
    parser.add_argument(
        "--export-drawio",
        action="store_true",
        help="Also export graph in draw.io XML format",
    )

    args = parser.parse_args()

    # Load settings
    try:
        settings = get_settings()
    except Exception as e:
        logger.error(f"Failed to load settings: {e}")
        logger.error("Please create a .env file with MIRO_ACCESS_TOKEN and MIRO_BOARD_ID")
        sys.exit(1)

    # Override board ID if provided
    board_id = args.board_id or settings.miro_board_id

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    logger.info("=" * 60)
    logger.info("Miro to Chatbot Graph Converter")
    logger.info("=" * 60)
    logger.info(f"Board ID: {board_id}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Export format: {args.format}")
    logger.info("=" * 60)

    # Step 1: Fetch data from Miro
    logger.info("\n[1/5] Fetching data from Miro...")
    try:
        miro_client = MiroClient(
            access_token=settings.miro_access_token,
            api_base_url=settings.miro_api_base_url,
        )
        board_data = miro_client.get_board_data(board_id)
        logger.info(f"✓ Fetched {len(board_data['items'])} items and {len(board_data['connectors'])} connectors")
    except Exception as e:
        logger.error(f"✗ Failed to fetch Miro data: {e}")
        sys.exit(1)

    # Step 2: Parse mindmap
    logger.info("\n[2/5] Parsing mindmap structure...")
    try:
        parser = MindmapParser()
        nodes, edges = parser.parse(board_data)
        summary = parser.get_summary()
        logger.info(f"✓ Parsed {summary['total_nodes']} nodes and {summary['total_edges']} edges")
        logger.info(f"  Node types: {summary['node_types']}")
    except Exception as e:
        logger.error(f"✗ Failed to parse mindmap: {e}")
        sys.exit(1)

    # Step 3: Convert to graph
    logger.info("\n[3/5] Converting to graph structure...")
    try:
        converter = GraphConverter(directed=True)
        graph = converter.convert(nodes, edges)
        stats = converter.get_graph_stats()
        logger.info(f"✓ Created graph with {stats['num_nodes']} nodes and {stats['num_edges']} edges")
        logger.info(f"  Root nodes: {stats.get('num_root_nodes', 0)}")
        logger.info(f"  Leaf nodes: {stats.get('num_leaf_nodes', 0)}")
        logger.info(f"  Connected: {stats['is_connected']}")

        # Export graph if requested
        if args.export_graph:
            graph_path = output_dir / "graph.graphml"
            converter.export_graphml(str(graph_path))
            logger.info(f"  Exported graph to {graph_path}")

        # Export draw.io XML if requested
        if args.export_drawio:
            drawio_exporter = DrawIOExporter(graph)
            drawio_path = output_dir / "graph_drawio.xml"
            drawio_exporter.save_to_file(str(drawio_path))
            logger.info(f"  Exported draw.io XML to {drawio_path}")
    except Exception as e:
        logger.error(f"✗ Failed to convert to graph: {e}")
        sys.exit(1)

    # Step 4: Export to chatbot format
    logger.info("\n[4/5] Exporting chatbot scenarios...")
    try:
        exporter = ChatbotExporter(graph)

        # Export in requested format
        output_path = output_dir / f"chatbot_scenario_{args.format}.json"
        exporter.export_to_json(str(output_path), export_format=args.format)
        logger.info(f"✓ Exported chatbot scenario to {output_path}")

        # Generate summary
        summary = exporter.export_summary()
        logger.info(f"  Total states: {summary['total_nodes']}")
        logger.info(f"  Entry points: {summary['entry_points']}")
        logger.info(f"  End points: {summary['end_points']}")
        logger.info(f"  Avg branching factor: {summary['avg_branching_factor']:.2f}")
    except Exception as e:
        logger.error(f"✗ Failed to export chatbot scenarios: {e}")
        sys.exit(1)

    # Step 5: Done
    logger.info("\n[5/5] Conversion complete!")
    logger.info("=" * 60)
    logger.info(f"✓ All files saved to: {output_dir}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
