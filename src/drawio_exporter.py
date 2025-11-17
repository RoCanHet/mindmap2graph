"""Export graph to draw.io XML format."""
import xml.etree.ElementTree as ET
from xml.dom import minidom
import networkx as nx
from typing import Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DrawIOExporter:
    """Exporter for converting graph to draw.io XML format."""

    def __init__(self, graph: nx.Graph):
        """
        Initialize draw.io exporter.

        Args:
            graph: NetworkX graph to export
        """
        self.graph = graph
        self.cell_id_counter = 2  # Start from 2 (0 and 1 are reserved)
        self.node_id_map = {}  # Map node_id to cell_id

    def _create_style(
        self,
        shape: str = "rounded=1",
        fill_color: str = "#dae8fc",
        stroke_color: str = "#6c8ebf",
        font_size: int = 12,
        **kwargs
    ) -> str:
        """
        Create style string for draw.io cell.

        Args:
            shape: Shape style
            fill_color: Fill color
            stroke_color: Stroke color
            font_size: Font size
            **kwargs: Additional style attributes

        Returns:
            Style string
        """
        style_parts = [
            shape,
            f"whiteSpace=wrap",
            f"html=1",
            f"fillColor={fill_color}",
            f"strokeColor={stroke_color}",
            f"fontSize={font_size}",
        ]

        for key, value in kwargs.items():
            style_parts.append(f"{key}={value}")

        return ";".join(style_parts) + ";"

    def _get_node_color(self, node_type: str) -> tuple:
        """
        Get color for node based on type.

        Args:
            node_type: Type of node

        Returns:
            Tuple of (fill_color, stroke_color)
        """
        color_map = {
            "sticky_note": ("#fff2cc", "#d6b656"),  # Yellow
            "card": ("#dae8fc", "#6c8ebf"),          # Blue
            "shape": ("#d5e8d4", "#82b366"),         # Green
            "unknown": ("#f5f5f5", "#666666"),       # Gray
        }
        return color_map.get(node_type, color_map["unknown"])

    def _create_node_cell(
        self,
        node_id: str,
        node_attrs: Dict[str, Any],
        parent_id: str = "1"
    ) -> ET.Element:
        """
        Create mxCell element for a node.

        Args:
            node_id: Node identifier
            node_attrs: Node attributes from graph
            parent_id: Parent cell ID

        Returns:
            mxCell Element
        """
        cell_id = str(self.cell_id_counter)
        self.cell_id_counter += 1
        self.node_id_map[node_id] = cell_id

        # Get node properties
        content = node_attrs.get("content", node_id)
        node_type = node_attrs.get("type", "unknown")
        position = node_attrs.get("position", (0, 0))

        # Limit content length for display
        if len(content) > 100:
            display_content = content[:97] + "..."
        else:
            display_content = content

        # Get colors based on type
        fill_color, stroke_color = self._get_node_color(node_type)

        # Create style
        style = self._create_style(
            shape="rounded=1",
            fill_color=fill_color,
            stroke_color=stroke_color,
            font_size=12,
        )

        # Create cell element
        cell = ET.Element("mxCell")
        cell.set("id", cell_id)
        cell.set("value", display_content)
        cell.set("style", style)
        cell.set("vertex", "1")
        cell.set("parent", parent_id)

        # Create geometry
        geometry = ET.SubElement(cell, "mxGeometry")

        # Position from Miro (scale down by 2 for better fit)
        if position:
            x = position[0] / 2
            y = position[1] / 2
        else:
            # Auto-layout if no position
            x = 100 + (self.cell_id_counter * 150) % 800
            y = 100 + ((self.cell_id_counter // 6) * 150)

        # Width based on content length (min 120, max 300)
        width = min(max(120, len(display_content) * 8), 300)
        height = 60

        geometry.set("x", str(int(x)))
        geometry.set("y", str(int(y)))
        geometry.set("width", str(width))
        geometry.set("height", str(height))
        geometry.set("as", "geometry")

        return cell

    def _create_edge_cell(
        self,
        source_id: str,
        target_id: str,
        edge_attrs: Dict[str, Any],
        parent_id: str = "1"
    ) -> ET.Element:
        """
        Create mxCell element for an edge.

        Args:
            source_id: Source node ID (original)
            target_id: Target node ID (original)
            edge_attrs: Edge attributes from graph
            parent_id: Parent cell ID

        Returns:
            mxCell Element
        """
        cell_id = str(self.cell_id_counter)
        self.cell_id_counter += 1

        # Get mapped cell IDs
        source_cell_id = self.node_id_map.get(source_id)
        target_cell_id = self.node_id_map.get(target_id)

        if not source_cell_id or not target_cell_id:
            logger.warning(f"Edge source or target not found: {source_id} -> {target_id}")
            return None

        # Get edge label
        label = edge_attrs.get("label", "")

        # Create edge style
        style = self._create_style(
            shape="edgeStyle=orthogonalEdgeStyle",
            fill_color="none",
            stroke_color="#000000",
            font_size=11,
            endArrow="classic",
            rounded=0,
        )

        # Create cell element
        cell = ET.Element("mxCell")
        cell.set("id", cell_id)
        cell.set("value", label if label else "")
        cell.set("style", style)
        cell.set("edge", "1")
        cell.set("parent", parent_id)
        cell.set("source", source_cell_id)
        cell.set("target", target_cell_id)

        # Create geometry
        geometry = ET.SubElement(cell, "mxGeometry")
        geometry.set("relative", "1")
        geometry.set("as", "geometry")

        return cell

    def export_to_drawio_xml(self) -> str:
        """
        Export graph to draw.io XML format.

        Returns:
            XML string in draw.io format
        """
        logger.info("Exporting to draw.io XML format...")

        # Create root mxGraphModel
        diagram = ET.Element("mxGraphModel")
        diagram.set("dx", "1434")
        diagram.set("dy", "780")
        diagram.set("grid", "1")
        diagram.set("gridSize", "10")
        diagram.set("guides", "1")
        diagram.set("tooltips", "1")
        diagram.set("connect", "1")
        diagram.set("arrows", "1")
        diagram.set("fold", "1")
        diagram.set("page", "1")
        diagram.set("pageScale", "1")
        diagram.set("pageWidth", "1169")
        diagram.set("pageHeight", "827")
        diagram.set("math", "0")
        diagram.set("shadow", "0")

        # Create root element
        root = ET.SubElement(diagram, "root")

        # Add default cells (required by draw.io)
        cell_0 = ET.SubElement(root, "mxCell")
        cell_0.set("id", "0")

        cell_1 = ET.SubElement(root, "mxCell")
        cell_1.set("id", "1")
        cell_1.set("parent", "0")

        # Add nodes
        for node_id in self.graph.nodes():
            node_attrs = self.graph.nodes[node_id]
            node_cell = self._create_node_cell(node_id, node_attrs)
            root.append(node_cell)

        logger.info(f"Added {len(self.graph.nodes())} nodes to XML")

        # Add edges
        edge_count = 0
        for source_id, target_id in self.graph.edges():
            edge_attrs = self.graph.get_edge_data(source_id, target_id) or {}
            edge_cell = self._create_edge_cell(source_id, target_id, edge_attrs)
            if edge_cell is not None:
                root.append(edge_cell)
                edge_count += 1

        logger.info(f"Added {edge_count} edges to XML")

        # Convert to string with pretty printing
        xml_string = ET.tostring(diagram, encoding="unicode")

        # Pretty print
        dom = minidom.parseString(xml_string)
        pretty_xml = dom.toprettyxml(indent="  ")

        # Remove extra blank lines
        lines = [line for line in pretty_xml.split('\n') if line.strip()]
        pretty_xml = '\n'.join(lines)

        logger.info("Draw.io XML export complete")

        return pretty_xml

    def save_to_file(self, output_path: str):
        """
        Save draw.io XML to file.

        Args:
            output_path: Path to save XML file
        """
        xml_content = self.export_to_drawio_xml()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(xml_content)

        logger.info(f"Draw.io XML saved to {output_path}")

    def get_export_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the export.

        Returns:
            Dictionary with export statistics
        """
        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "total_cells": self.cell_id_counter - 2,  # Exclude cells 0 and 1
            "node_types": self._get_node_type_counts(),
        }

    def _get_node_type_counts(self) -> Dict[str, int]:
        """Get count of nodes by type."""
        type_counts = {}
        for node_id in self.graph.nodes():
            node_type = self.graph.nodes[node_id].get("type", "unknown")
            type_counts[node_type] = type_counts.get(node_type, 0) + 1
        return type_counts
