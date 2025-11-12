"""Miro API client for fetching board data."""
import requests
from typing import Dict, List, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MiroClient:
    """Client for interacting with Miro API."""

    def __init__(self, access_token: str, api_base_url: str = "https://api.miro.com/v2"):
        """
        Initialize Miro client.

        Args:
            access_token: Miro API access token
            api_base_url: Base URL for Miro API
        """
        self.access_token = access_token
        self.api_base_url = api_base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _make_request(self, endpoint: str, method: str = "GET", **kwargs) -> Dict[str, Any]:
        """
        Make HTTP request to Miro API.

        Args:
            endpoint: API endpoint
            method: HTTP method
            **kwargs: Additional request parameters

        Returns:
            JSON response data
        """
        url = f"{self.api_base_url}/{endpoint.lstrip('/')}"
        logger.info(f"Making {method} request to {url}")

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    def get_board_items(self, board_id: str, item_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all items from a Miro board.

        Args:
            board_id: Miro board ID
            item_type: Filter by item type (e.g., 'shape', 'sticky_note', 'card')

        Returns:
            List of board items
        """
        endpoint = f"boards/{board_id}/items"
        params = {}
        if item_type:
            params["type"] = item_type

        all_items = []
        cursor = None

        while True:
            if cursor:
                params["cursor"] = cursor

            response = self._make_request(endpoint, params=params)
            items = response.get("data", [])
            all_items.extend(items)

            logger.info(f"Retrieved {len(items)} items (total: {len(all_items)})")

            # Check for pagination
            cursor = response.get("cursor")
            if not cursor:
                break

        return all_items

    def get_board_connectors(self, board_id: str) -> List[Dict[str, Any]]:
        """
        Get all connectors (connections) from a Miro board.

        Args:
            board_id: Miro board ID

        Returns:
            List of connectors
        """
        endpoint = f"boards/{board_id}/connectors"
        all_connectors = []
        cursor = None

        while True:
            params = {}
            if cursor:
                params["cursor"] = cursor

            response = self._make_request(endpoint, params=params)
            connectors = response.get("data", [])
            all_connectors.extend(connectors)

            logger.info(f"Retrieved {len(connectors)} connectors (total: {len(all_connectors)})")

            cursor = response.get("cursor")
            if not cursor:
                break

        return all_connectors

    def get_board_data(self, board_id: str) -> Dict[str, Any]:
        """
        Get complete board data including items and connectors.

        Args:
            board_id: Miro board ID

        Returns:
            Dictionary with items and connectors
        """
        logger.info(f"Fetching data from board {board_id}")

        items = self.get_board_items(board_id)
        connectors = self.get_board_connectors(board_id)

        return {
            "board_id": board_id,
            "items": items,
            "connectors": connectors,
        }
