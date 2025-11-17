"""Parse Mermaid flowchart to graph structure."""
import re
from typing import Dict, List, Tuple, Any


class MermaidParser:
    """Parser for Mermaid flowchart syntax."""

    def __init__(self):
        """Initialize parser."""
        self.nodes = {}
        self.edges = []

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse Mermaid file to graph structure.

        Args:
            file_path: Path to Mermaid file

        Returns:
            Dict with items and connectors
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return self.parse(content)

    def parse(self, mermaid_text: str) -> Dict[str, Any]:
        """
        Parse Mermaid text to graph structure.

        Args:
            mermaid_text: Mermaid flowchart text

        Returns:
            Dict with items and connectors (compatible with MindmapParser)
        """
        lines = mermaid_text.split('\n')

        for line in lines:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith('%%') or line.startswith('flowchart'):
                continue

            # Skip subgraph definitions
            if line.startswith('subgraph') or line.startswith('end') or line.startswith('direction'):
                continue

            # Parse node definitions and connections
            self._parse_line(line)

        # Convert to format compatible with MindmapParser
        items = []
        for node_id, node_data in self.nodes.items():
            items.append({
                "id": node_id,
                "type": node_data.get("shape", "card"),
                "data": {"content": node_data.get("label", node_id)},
                "position": {"x": 0, "y": 0}  # Will be auto-positioned
            })

        connectors = []
        for idx, edge in enumerate(self.edges):
            connector = {
                "id": f"edge_{idx}",
                "startItem": {"id": edge["from"]},
                "endItem": {"id": edge["to"]},
            }
            if edge.get("label"):
                connector["captions"] = [{"content": edge["label"]}]
            connectors.append(connector)

        return {
            "items": items,
            "connectors": connectors
        }

    def _parse_line(self, line: str):
        """Parse a single line of Mermaid syntax."""
        # Pattern for node definition: NodeID["Label"] or NodeID("Label") or NodeID{Label}
        node_pattern = r'(\w+)\s*([(\[{])\s*([^)\]}]+)\s*([)\]}])'

        # Pattern for edge: NodeA --> NodeB or NodeA -->|Label| NodeB
        edge_pattern = r'(\w+)\s*-->(?:\|([^|]+)\|)?\s*(\w+)'

        # Find all node definitions in line
        for match in re.finditer(node_pattern, line):
            node_id = match.group(1)
            open_bracket = match.group(2)
            label = match.group(3)

            # Determine shape based on brackets
            shape_map = {
                '[': 'card',
                '(': 'sticky_note',
                '{': 'shape'
            }
            shape = shape_map.get(open_bracket, 'card')

            # Clean label (remove HTML tags if any)
            label_clean = re.sub(r'<br\/?>', ' ', label)
            label_clean = label_clean.strip()

            self.nodes[node_id] = {
                "label": label_clean,
                "shape": shape
            }

        # Find edges
        for match in re.finditer(edge_pattern, line):
            from_node = match.group(1)
            edge_label = match.group(2) if match.group(2) else ""
            to_node = match.group(3)

            # Ensure nodes exist
            if from_node not in self.nodes:
                self.nodes[from_node] = {"label": from_node, "shape": "card"}
            if to_node not in self.nodes:
                self.nodes[to_node] = {"label": to_node, "shape": "card"}

            self.edges.append({
                "from": from_node,
                "to": to_node,
                "label": edge_label.strip() if edge_label else ""
            })

    def get_stats(self) -> Dict[str, Any]:
        """Get parsing statistics."""
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
        }
