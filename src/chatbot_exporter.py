"""Export graph data to chatbot scenario format."""
import json
import networkx as nx
from typing import Dict, List, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatbotExporter:
    """Exporter for converting graph to chatbot scenario format."""

    def __init__(self, graph: nx.Graph):
        """
        Initialize chatbot exporter.

        Args:
            graph: NetworkX graph to export
        """
        self.graph = graph

    def _get_node_data(self, node_id: str) -> Dict[str, Any]:
        """
        Get formatted node data.

        Args:
            node_id: Node identifier

        Returns:
            Dictionary with node data
        """
        node_attrs = self.graph.nodes[node_id]
        return {
            "id": node_id,
            "content": node_attrs.get("content", ""),
            "type": node_attrs.get("type", "unknown"),
            "position": node_attrs.get("position"),
        }

    def _get_edge_data(self, source: str, target: str) -> Dict[str, Any]:
        """
        Get formatted edge data.

        Args:
            source: Source node ID
            target: Target node ID

        Returns:
            Dictionary with edge data
        """
        edge_attrs = self.graph.get_edge_data(source, target) or {}
        return {
            "from": source,
            "to": target,
            "label": edge_attrs.get("label"),
        }

    def export_dialogue_flow(self) -> Dict[str, Any]:
        """
        Export graph as dialogue flow format.

        This format represents the chatbot conversation flow where:
        - Each node is a dialogue state/message
        - Edges represent transitions between states
        - Root nodes are entry points
        - Leaf nodes are endpoints

        Returns:
            Dictionary in dialogue flow format
        """
        logger.info("Exporting dialogue flow format...")

        # Find root nodes (entry points)
        if self.graph.is_directed():
            root_nodes = [n for n in self.graph.nodes() if self.graph.in_degree(n) == 0]
        else:
            # For undirected graphs, use nodes with only 1 connection as potential roots
            root_nodes = [n for n in self.graph.nodes() if self.graph.degree(n) == 1]

        # Build dialogue states
        states = []
        for node_id in self.graph.nodes():
            node_data = self._get_node_data(node_id)

            # Get transitions (outgoing edges)
            transitions = []
            if self.graph.is_directed():
                for successor in self.graph.successors(node_id):
                    edge_data = self._get_edge_data(node_id, successor)
                    transitions.append({
                        "target_state": successor,
                        "condition": edge_data.get("label"),
                        "label": edge_data.get("label"),
                    })
            else:
                for neighbor in self.graph.neighbors(node_id):
                    edge_data = self._get_edge_data(node_id, neighbor)
                    transitions.append({
                        "target_state": neighbor,
                        "condition": edge_data.get("label"),
                        "label": edge_data.get("label"),
                    })

            states.append({
                "state_id": node_id,
                "message": node_data["content"],
                "type": node_data["type"],
                "transitions": transitions,
                "is_entry_point": node_id in root_nodes,
            })

        return {
            "format": "dialogue_flow",
            "version": "1.0",
            "entry_points": root_nodes,
            "total_states": len(states),
            "states": states,
        }

    def export_intent_tree(self) -> Dict[str, Any]:
        """
        Export graph as intent tree format.

        This format represents a hierarchical intent structure:
        - Root nodes are main intents
        - Child nodes are sub-intents or responses
        - Useful for intent-based chatbots

        Returns:
            Dictionary in intent tree format
        """
        logger.info("Exporting intent tree format...")

        # Find root nodes
        if self.graph.is_directed():
            root_nodes = [n for n in self.graph.nodes() if self.graph.in_degree(n) == 0]
        else:
            root_nodes = list(self.graph.nodes())[:1]  # Use first node as root for undirected

        def build_tree(node_id: str, visited: set) -> Dict[str, Any]:
            """Recursively build intent tree."""
            if node_id in visited:
                return None

            visited.add(node_id)
            node_data = self._get_node_data(node_id)

            children = []
            if self.graph.is_directed():
                successors = list(self.graph.successors(node_id))
            else:
                successors = [n for n in self.graph.neighbors(node_id) if n not in visited]

            for child_id in successors:
                edge_data = self._get_edge_data(node_id, child_id)
                child_tree = build_tree(child_id, visited)
                if child_tree:
                    child_tree["transition_label"] = edge_data.get("label")
                    children.append(child_tree)

            return {
                "intent_id": node_id,
                "intent_name": node_data["content"],
                "type": node_data["type"],
                "children": children,
            }

        # Build tree for each root
        intent_trees = []
        for root_id in root_nodes:
            tree = build_tree(root_id, set())
            if tree:
                intent_trees.append(tree)

        return {
            "format": "intent_tree",
            "version": "1.0",
            "num_root_intents": len(intent_trees),
            "intent_trees": intent_trees,
        }

    def export_scenario_paths(self, max_depth: int = 10) -> Dict[str, Any]:
        """
        Export all possible conversation paths as scenarios.

        Args:
            max_depth: Maximum path depth to explore

        Returns:
            Dictionary with all conversation scenarios
        """
        logger.info("Exporting scenario paths...")

        # Find root nodes
        if self.graph.is_directed():
            root_nodes = [n for n in self.graph.nodes() if self.graph.in_degree(n) == 0]
            leaf_nodes = [n for n in self.graph.nodes() if self.graph.out_degree(n) == 0]
        else:
            root_nodes = list(self.graph.nodes())[:1]
            leaf_nodes = [n for n in self.graph.nodes() if self.graph.degree(n) == 1]

        # Generate all paths from roots to leaves
        scenarios = []
        scenario_id = 1

        for root in root_nodes:
            for leaf in leaf_nodes:
                if root == leaf:
                    continue

                try:
                    # Find all simple paths
                    paths = list(nx.all_simple_paths(self.graph, root, leaf, cutoff=max_depth))

                    for path in paths:
                        # Build scenario from path
                        steps = []
                        for i, node_id in enumerate(path):
                            node_data = self._get_node_data(node_id)

                            step = {
                                "step_number": i + 1,
                                "node_id": node_id,
                                "message": node_data["content"],
                                "type": node_data["type"],
                            }

                            # Add transition info
                            if i < len(path) - 1:
                                next_node = path[i + 1]
                                edge_data = self._get_edge_data(node_id, next_node)
                                step["transition"] = edge_data.get("label")

                            steps.append(step)

                        scenarios.append({
                            "scenario_id": f"scenario_{scenario_id}",
                            "length": len(steps),
                            "start_node": root,
                            "end_node": leaf,
                            "steps": steps,
                        })
                        scenario_id += 1

                except nx.NetworkXNoPath:
                    continue

        return {
            "format": "scenario_paths",
            "version": "1.0",
            "total_scenarios": len(scenarios),
            "scenarios": scenarios,
        }

    def export_to_json(self, output_path: str, export_format: str = "dialogue_flow"):
        """
        Export graph to JSON file in specified format.

        Args:
            output_path: Path to save JSON file
            export_format: Export format ('dialogue_flow', 'intent_tree', 'scenario_paths', 'all')
        """
        if export_format == "dialogue_flow":
            data = self.export_dialogue_flow()
        elif export_format == "intent_tree":
            data = self.export_intent_tree()
        elif export_format == "scenario_paths":
            data = self.export_scenario_paths()
        elif export_format == "all":
            data = {
                "dialogue_flow": self.export_dialogue_flow(),
                "intent_tree": self.export_intent_tree(),
                "scenario_paths": self.export_scenario_paths(),
            }
        else:
            raise ValueError(f"Unknown export format: {export_format}")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"Exported {export_format} format to {output_path}")

    def export_summary(self) -> Dict[str, Any]:
        """
        Generate a summary of the chatbot scenario.

        Returns:
            Dictionary with summary information
        """
        # Calculate statistics
        num_nodes = self.graph.number_of_nodes()
        num_edges = self.graph.number_of_edges()

        if self.graph.is_directed():
            root_nodes = [n for n in self.graph.nodes() if self.graph.in_degree(n) == 0]
            leaf_nodes = [n for n in self.graph.nodes() if self.graph.out_degree(n) == 0]
        else:
            root_nodes = []
            leaf_nodes = []

        # Get node types distribution
        node_types = {}
        for node_id in self.graph.nodes():
            node_type = self.graph.nodes[node_id].get("type", "unknown")
            node_types[node_type] = node_types.get(node_type, 0) + 1

        return {
            "total_nodes": num_nodes,
            "total_edges": num_edges,
            "entry_points": len(root_nodes),
            "end_points": len(leaf_nodes),
            "node_types": node_types,
            "avg_branching_factor": num_edges / num_nodes if num_nodes > 0 else 0,
        }
