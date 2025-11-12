"""Parser for Miro mindmap data."""
from typing import Dict, List, Any, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Node:
    """Represents a node in the mindmap."""

    def __init__(
        self,
        node_id: str,
        content: str,
        node_type: str,
        position: Optional[Tuple[float, float]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a Node.

        Args:
            node_id: Unique identifier
            content: Text content of the node
            node_type: Type of node (e.g., 'shape', 'sticky_note', 'card')
            position: (x, y) position on board
            metadata: Additional metadata
        """
        self.id = node_id
        self.content = content
        self.type = node_type
        self.position = position
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary."""
        return {
            "id": self.id,
            "content": self.content,
            "type": self.type,
            "position": self.position,
            "metadata": self.metadata,
        }

    def __repr__(self) -> str:
        return f"Node(id={self.id}, content={self.content[:30]}...)"


class Edge:
    """Represents an edge (connection) between nodes."""

    def __init__(
        self,
        edge_id: str,
        source_id: str,
        target_id: str,
        label: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize an Edge.

        Args:
            edge_id: Unique identifier
            source_id: Source node ID
            target_id: Target node ID
            label: Optional label for the edge
            metadata: Additional metadata
        """
        self.id = edge_id
        self.source = source_id
        self.target = target_id
        self.label = label
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert edge to dictionary."""
        return {
            "id": self.id,
            "source": self.source,
            "target": self.target,
            "label": self.label,
            "metadata": self.metadata,
        }

    def __repr__(self) -> str:
        return f"Edge(source={self.source}, target={self.target}, label={self.label})"


class MindmapParser:
    """Parser for converting Miro board data to structured mindmap."""

    def __init__(self):
        """Initialize parser."""
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []

    def _extract_text_content(self, item: Dict[str, Any]) -> str:
        """
        Extract text content from Miro item.

        Args:
            item: Miro item data

        Returns:
            Extracted text content
        """
        # Try different content fields based on item type
        if "data" in item:
            data = item["data"]
            # For shapes and cards
            if "content" in data:
                return data["content"]
            # For sticky notes
            if "title" in data:
                return data["title"]
            # For text items
            if "text" in data:
                return data["text"]

        # Fallback to type or id
        return item.get("type", item.get("id", "Unknown"))

    def _extract_position(self, item: Dict[str, Any]) -> Optional[Tuple[float, float]]:
        """
        Extract position from Miro item.

        Args:
            item: Miro item data

        Returns:
            (x, y) position or None
        """
        if "position" in item:
            pos = item["position"]
            return (pos.get("x", 0), pos.get("y", 0))
        return None

    def parse(self, board_data: Dict[str, Any]) -> Tuple[Dict[str, Node], List[Edge]]:
        """
        Parse Miro board data into nodes and edges.

        Args:
            board_data: Board data from MiroClient

        Returns:
            Tuple of (nodes_dict, edges_list)
        """
        logger.info("Parsing board data...")

        # Parse items as nodes
        items = board_data.get("items", [])
        for item in items:
            node_id = item.get("id")
            if not node_id:
                continue

            content = self._extract_text_content(item)
            node_type = item.get("type", "unknown")
            position = self._extract_position(item)

            # Store additional metadata
            metadata = {
                "style": item.get("style", {}),
                "geometry": item.get("geometry", {}),
            }

            node = Node(
                node_id=node_id,
                content=content,
                node_type=node_type,
                position=position,
                metadata=metadata,
            )
            self.nodes[node_id] = node

        logger.info(f"Parsed {len(self.nodes)} nodes")

        # Parse connectors as edges
        connectors = board_data.get("connectors", [])
        for connector in connectors:
            edge_id = connector.get("id")
            if not edge_id:
                continue

            start_item = connector.get("startItem", {})
            end_item = connector.get("endItem", {})

            source_id = start_item.get("id")
            target_id = end_item.get("id")

            if not source_id or not target_id:
                continue

            # Extract label if available
            label = None
            if "captions" in connector:
                captions = connector["captions"]
                if captions and len(captions) > 0:
                    label = captions[0].get("content", "")

            # Store additional metadata
            metadata = {
                "style": connector.get("style", {}),
                "shape": connector.get("shape", ""),
            }

            edge = Edge(
                edge_id=edge_id,
                source_id=source_id,
                target_id=target_id,
                label=label,
                metadata=metadata,
            )
            self.edges.append(edge)

        logger.info(f"Parsed {len(self.edges)} edges")

        return self.nodes, self.edges

    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics of parsed mindmap."""
        node_types = {}
        for node in self.nodes.values():
            node_types[node.type] = node_types.get(node.type, 0) + 1

        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "node_types": node_types,
        }
