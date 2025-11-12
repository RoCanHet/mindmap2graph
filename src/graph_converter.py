"""Convert parsed mindmap to NetworkX graph."""
import networkx as nx
from typing import Dict, List, Any, Optional
import logging
from .mindmap_parser import Node, Edge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphConverter:
    """Converter for transforming mindmap to NetworkX graph."""

    def __init__(self, directed: bool = True):
        """
        Initialize graph converter.

        Args:
            directed: Whether to create a directed graph (default: True)
        """
        self.directed = directed
        self.graph = nx.DiGraph() if directed else nx.Graph()

    def convert(
        self,
        nodes: Dict[str, Node],
        edges: List[Edge],
    ) -> nx.Graph:
        """
        Convert nodes and edges to NetworkX graph.

        Args:
            nodes: Dictionary of Node objects
            edges: List of Edge objects

        Returns:
            NetworkX graph
        """
        logger.info(f"Converting to {'directed' if self.directed else 'undirected'} graph...")

        # Add nodes
        for node_id, node in nodes.items():
            self.graph.add_node(
                node_id,
                content=node.content,
                type=node.type,
                position=node.position,
                **node.metadata,
            )

        logger.info(f"Added {len(nodes)} nodes to graph")

        # Add edges
        for edge in edges:
            edge_attrs = {"label": edge.label} if edge.label else {}
            edge_attrs.update(edge.metadata)

            self.graph.add_edge(
                edge.source,
                edge.target,
                **edge_attrs,
            )

        logger.info(f"Added {len(edges)} edges to graph")

        return self.graph

    def get_graph_stats(self) -> Dict[str, Any]:
        """Get statistics about the graph."""
        stats = {
            "num_nodes": self.graph.number_of_nodes(),
            "num_edges": self.graph.number_of_edges(),
            "is_directed": self.graph.is_directed(),
            "is_connected": nx.is_weakly_connected(self.graph) if self.directed else nx.is_connected(self.graph),
        }

        # Calculate degree statistics
        if self.graph.number_of_nodes() > 0:
            degrees = dict(self.graph.degree())
            stats["avg_degree"] = sum(degrees.values()) / len(degrees)
            stats["max_degree"] = max(degrees.values())
            stats["min_degree"] = min(degrees.values())

        # Find root nodes (nodes with no incoming edges) for directed graphs
        if self.directed and self.graph.number_of_nodes() > 0:
            root_nodes = [n for n in self.graph.nodes() if self.graph.in_degree(n) == 0]
            stats["num_root_nodes"] = len(root_nodes)
            stats["root_nodes"] = root_nodes[:5]  # First 5 root nodes

            # Find leaf nodes (nodes with no outgoing edges)
            leaf_nodes = [n for n in self.graph.nodes() if self.graph.out_degree(n) == 0]
            stats["num_leaf_nodes"] = len(leaf_nodes)

        return stats

    def find_paths(
        self,
        source_id: str,
        target_id: str,
        max_paths: int = 5,
    ) -> List[List[str]]:
        """
        Find all paths between two nodes.

        Args:
            source_id: Source node ID
            target_id: Target node ID
            max_paths: Maximum number of paths to return

        Returns:
            List of paths (each path is a list of node IDs)
        """
        try:
            if self.directed:
                all_paths = list(nx.all_simple_paths(self.graph, source_id, target_id))
            else:
                all_paths = list(nx.all_simple_paths(self.graph, source_id, target_id))

            return all_paths[:max_paths]
        except (nx.NodeNotFound, nx.NetworkXNoPath) as e:
            logger.warning(f"No path found: {e}")
            return []

    def get_subgraph_from_root(self, root_id: str, max_depth: Optional[int] = None) -> nx.Graph:
        """
        Get subgraph starting from a root node.

        Args:
            root_id: Root node ID
            max_depth: Maximum depth to traverse (None for unlimited)

        Returns:
            Subgraph rooted at the specified node
        """
        if root_id not in self.graph:
            raise ValueError(f"Node {root_id} not found in graph")

        if max_depth is None:
            # Get all descendants
            descendants = nx.descendants(self.graph, root_id)
            subgraph_nodes = [root_id] + list(descendants)
        else:
            # BFS traversal with depth limit
            subgraph_nodes = {root_id}
            current_level = {root_id}

            for _ in range(max_depth):
                next_level = set()
                for node in current_level:
                    next_level.update(self.graph.successors(node))
                subgraph_nodes.update(next_level)
                current_level = next_level
                if not current_level:
                    break

        return self.graph.subgraph(subgraph_nodes).copy()

    def export_graphml(self, output_path: str):
        """
        Export graph to GraphML format.

        Args:
            output_path: Path to save GraphML file
        """
        nx.write_graphml(self.graph, output_path)
        logger.info(f"Graph exported to {output_path}")

    def export_gexf(self, output_path: str):
        """
        Export graph to GEXF format.

        Args:
            output_path: Path to save GEXF file
        """
        nx.write_gexf(self.graph, output_path)
        logger.info(f"Graph exported to {output_path}")
