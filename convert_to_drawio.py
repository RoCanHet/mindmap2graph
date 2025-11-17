"""Convert mindmap/graph data to draw.io XML format."""
import argparse
import json
import logging
import sys
from pathlib import Path

from src import MindmapParser, GraphConverter, DrawIOExporter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_json_data(file_path: str) -> dict:
    """Load JSON data from file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Convert graph data to draw.io XML format"
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Input JSON file with graph data (nodes and edges)",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="output.xml",
        help="Output XML file path (default: output.xml)",
    )

    args = parser.parse_args()

    # Check input file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        logger.error(f"Input file not found: {args.input_file}")
        sys.exit(1)

    logger.info("=" * 60)
    logger.info("Graph to draw.io XML Converter")
    logger.info("=" * 60)
    logger.info(f"Input: {args.input_file}")
    logger.info(f"Output: {args.output}")
    logger.info("=" * 60)

    # Step 1: Load JSON data
    logger.info("\n[1/4] Loading JSON data...")
    try:
        data = load_json_data(args.input_file)
        logger.info(f"✓ Loaded data from {args.input_file}")
    except Exception as e:
        logger.error(f"✗ Failed to load JSON: {e}")
        sys.exit(1)

    # Step 2: Parse graph structure
    logger.info("\n[2/4] Parsing graph structure...")
    try:
        parser = MindmapParser()
        nodes, edges = parser.parse(data)
        summary = parser.get_summary()
        logger.info(f"✓ Parsed {summary['total_nodes']} nodes and {summary['total_edges']} edges")
    except Exception as e:
        logger.error(f"✗ Failed to parse graph: {e}")
        sys.exit(1)

    # Step 3: Convert to NetworkX graph
    logger.info("\n[3/4] Converting to graph...")
    try:
        converter = GraphConverter(directed=True)
        graph = converter.convert(nodes, edges)
        stats = converter.get_graph_stats()
        logger.info(f"✓ Created graph with {stats['num_nodes']} nodes and {stats['num_edges']} edges")
    except Exception as e:
        logger.error(f"✗ Failed to convert to graph: {e}")
        sys.exit(1)

    # Step 4: Export to draw.io XML
    logger.info("\n[4/4] Exporting to draw.io XML...")
    try:
        drawio_exporter = DrawIOExporter(graph)
        drawio_exporter.save_to_file(args.output)

        export_stats = drawio_exporter.get_export_stats()
        logger.info(f"✓ Exported to {args.output}")
        logger.info(f"  - Total nodes: {export_stats['total_nodes']}")
        logger.info(f"  - Total edges: {export_stats['total_edges']}")
        logger.info(f"  - Total cells: {export_stats['total_cells']}")
    except Exception as e:
        logger.error(f"✗ Failed to export XML: {e}")
        sys.exit(1)

    logger.info("\n" + "=" * 60)
    logger.info("✓ Conversion complete!")
    logger.info("=" * 60)
    logger.info(f"\nNext steps:")
    logger.info(f"1. Open https://app.diagrams.net")
    logger.info(f"2. File → Open from → Device")
    logger.info(f"3. Select {args.output}")
    logger.info(f"4. Edit and export as PNG/PDF/SVG")


if __name__ == "__main__":
    main()
