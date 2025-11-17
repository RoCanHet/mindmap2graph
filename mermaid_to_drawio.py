"""Convert Mermaid flowchart to draw.io XML."""
import argparse
import logging
import sys
from pathlib import Path

from src import MermaidParser, MindmapParser, GraphConverter, DrawIOExporter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Convert Mermaid flowchart to draw.io XML format"
    )
    parser.add_argument(
        "input_file",
        type=str,
        nargs='?',
        default="OTS",
        help="Input Mermaid file (default: OTS)",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="output/flowchart.xml",
        help="Output XML file path (default: output/flowchart.xml)",
    )

    args = parser.parse_args()

    # Check input file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        logger.error(f"Input file not found: {args.input_file}")
        sys.exit(1)

    # Create output directory
    output_path = Path(args.output)
    output_path.parent.mkdir(exist_ok=True, parents=True)

    logger.info("=" * 70)
    logger.info("Mermaid Flowchart → draw.io XML Converter")
    logger.info("=" * 70)
    logger.info(f"Input: {args.input_file}")
    logger.info(f"Output: {args.output}")
    logger.info("=" * 70)

    # Step 1: Parse Mermaid file
    logger.info("\n[1/4] Parsing Mermaid flowchart...")
    try:
        mermaid_parser = MermaidParser()
        graph_data = mermaid_parser.parse_file(args.input_file)
        stats = mermaid_parser.get_stats()
        logger.info(f"✓ Parsed Mermaid file")
        logger.info(f"  - Total nodes: {stats['total_nodes']}")
        logger.info(f"  - Total edges: {stats['total_edges']}")
    except Exception as e:
        logger.error(f"✗ Failed to parse Mermaid: {e}")
        sys.exit(1)

    # Step 2: Convert to graph structure
    logger.info("\n[2/4] Converting to graph structure...")
    try:
        parser = MindmapParser()
        nodes, edges = parser.parse(graph_data)
        logger.info(f"✓ Parsed {len(nodes)} nodes and {len(edges)} edges")
    except Exception as e:
        logger.error(f"✗ Failed to parse graph: {e}")
        sys.exit(1)

    # Step 3: Build NetworkX graph
    logger.info("\n[3/4] Building graph...")
    try:
        converter = GraphConverter(directed=True)
        graph = converter.convert(nodes, edges)
        graph_stats = converter.get_graph_stats()
        logger.info(f"✓ Created graph with {graph_stats['num_nodes']} nodes and {graph_stats['num_edges']} edges")
    except Exception as e:
        logger.error(f"✗ Failed to build graph: {e}")
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

    logger.info("\n" + "=" * 70)
    logger.info("✓ Conversion complete!")
    logger.info("=" * 70)
    logger.info(f"\nNext steps:")
    logger.info(f"1. Open https://app.diagrams.net")
    logger.info(f"2. File → Open from → Device")
    logger.info(f"3. Select {args.output}")
    logger.info(f"4. Use Arrange → Layout → Vertical/Horizontal Flow")
    logger.info(f"5. Edit colors, export to PNG/PDF")


if __name__ == "__main__":
    main()
