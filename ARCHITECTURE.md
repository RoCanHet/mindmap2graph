# Architecture Documentation

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Miro Mindmap Board                        │
│  ┌─────┐      ┌─────┐      ┌─────┐      ┌─────┐           │
│  │Node1├─────►│Node2├─────►│Node3├─────►│Node4│           │
│  └─────┘      └─────┘      └─────┘      └─────┘           │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   MiroClient (API)     │
              │  - fetch board items   │
              │  - fetch connectors    │
              └────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   MindmapParser        │
              │  - extract nodes       │
              │  - extract edges       │
              │  - parse content       │
              └────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   GraphConverter       │
              │  - NetworkX graph      │
              │  - topology analysis   │
              │  - path finding        │
              └────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   ChatbotExporter      │
              │  - dialogue_flow       │
              │  - intent_tree         │
              │  - scenario_paths      │
              └────────────────────────┘
                           │
                           ▼
        ┌─────────────────┴─────────────────┐
        │                                    │
        ▼                                    ▼
┌──────────────┐                    ┌──────────────┐
│   JSON Files │                    │ GraphML File │
│ - dialogue   │                    │ - visualize  │
│ - intents    │                    │ - analysis   │
│ - scenarios  │                    │              │
└──────────────┘                    └──────────────┘
        │                                    │
        ▼                                    ▼
┌──────────────┐                    ┌──────────────┐
│   Chatbot    │                    │    Gephi     │
│  Platform    │                    │  Cytoscape   │
└──────────────┘                    └──────────────┘
```

## Component Details

### 1. MiroClient

**Purpose**: Interact with Miro REST API

**Key Methods**:
- `get_board_items(board_id)` - Fetch all items (nodes)
- `get_board_connectors(board_id)` - Fetch all connectors (edges)
- `get_board_data(board_id)` - Fetch complete board data

**API Endpoints Used**:
- `GET /v2/boards/{board_id}/items`
- `GET /v2/boards/{board_id}/connectors`

**Error Handling**:
- Network errors
- Authentication errors (401)
- Rate limiting
- Invalid board ID (404)

### 2. MindmapParser

**Purpose**: Parse raw Miro data into structured format

**Data Classes**:

```python
Node
├── id: str
├── content: str
├── type: str
├── position: (x, y)
└── metadata: dict

Edge
├── id: str
├── source: str
├── target: str
├── label: str
└── metadata: dict
```

**Parsing Logic**:
1. Extract text content from different item types:
   - sticky_note: data.content or data.title
   - card: data.title
   - shape: data.content
2. Extract position coordinates
3. Store additional metadata (style, geometry)
4. Build edge connections from connectors

### 3. GraphConverter

**Purpose**: Convert to NetworkX graph structure

**Graph Types**:
- **Directed Graph** (DiGraph): Default, for conversation flows
- **Undirected Graph** (Graph): Optional, for topic relationships

**Features**:

```python
# Graph Statistics
- num_nodes, num_edges
- is_connected
- avg_degree, max_degree, min_degree
- num_root_nodes, num_leaf_nodes

# Graph Operations
- find_paths(source, target)
- get_subgraph_from_root(root_id, max_depth)
- export_graphml() / export_gexf()
```

**Algorithms Used**:
- BFS for subgraph extraction
- Simple path finding (NetworkX)
- Connected component analysis
- Degree centrality

### 4. ChatbotExporter

**Purpose**: Export to chatbot-friendly formats

#### Format 1: Dialogue Flow

**Structure**:
```json
{
  "states": [
    {
      "state_id": "node_1",
      "message": "Hello!",
      "transitions": [
        {
          "target_state": "node_2",
          "condition": "user_input",
          "label": "Continue"
        }
      ]
    }
  ]
}
```

**Use Case**:
- Conversation flow definition
- State machine implementation
- Chatbot platform integration (Dialogflow, Rasa, Botpress)

#### Format 2: Intent Tree

**Structure**:
```json
{
  "intent_trees": [
    {
      "intent_id": "root",
      "intent_name": "Main Intent",
      "children": [
        {
          "intent_id": "child_1",
          "intent_name": "Sub Intent",
          "children": []
        }
      ]
    }
  ]
}
```

**Use Case**:
- Intent hierarchy design
- NLU training data organization
- Multi-level intent classification

#### Format 3: Scenario Paths

**Structure**:
```json
{
  "scenarios": [
    {
      "scenario_id": "scenario_1",
      "steps": [
        {
          "step_number": 1,
          "node_id": "node_1",
          "message": "Start",
          "transition": "next"
        }
      ]
    }
  ]
}
```

**Use Case**:
- Test case generation
- User journey mapping
- Conversation training data

## Data Flow

### Step-by-Step Process

```
1. User creates mindmap in Miro
   ↓
2. MiroClient fetches via API
   ↓
3. MindmapParser extracts structure
   ├─> Nodes (items)
   └─> Edges (connectors)
   ↓
4. GraphConverter builds NetworkX graph
   ├─> Add nodes with attributes
   ├─> Add edges with labels
   └─> Calculate statistics
   ↓
5. ChatbotExporter generates formats
   ├─> Dialogue Flow (state machine)
   ├─> Intent Tree (hierarchy)
   └─> Scenario Paths (test cases)
   ↓
6. Export to JSON/GraphML files
   ↓
7. Import to chatbot platform
```

## Configuration

### Environment Variables

```bash
MIRO_ACCESS_TOKEN=<token>      # Required: Miro API token
MIRO_BOARD_ID=<board_id>       # Required: Target board ID
MIRO_API_BASE_URL=<url>        # Optional: API endpoint
```

### Settings (Pydantic)

```python
class Settings(BaseSettings):
    miro_access_token: str
    miro_board_id: str
    miro_api_base_url: str = "https://api.miro.com/v2"
```

## Performance Considerations

### API Calls
- **Pagination**: Handles large boards with cursor-based pagination
- **Rate Limiting**: Respects Miro API rate limits
- **Batch Processing**: Fetches all items/connectors in batches

### Memory Usage
- **Nodes**: O(N) where N = number of items
- **Edges**: O(E) where E = number of connectors
- **Graph**: O(N + E) for NetworkX storage

### Optimization Tips
1. Filter by item type to reduce data
2. Use max_depth in subgraph extraction
3. Limit scenario path generation with max_depth
4. Cache board data for multiple exports

## Error Handling

### API Errors
```python
try:
    board_data = client.get_board_data(board_id)
except requests.HTTPError as e:
    if e.response.status_code == 401:
        # Invalid token
    elif e.response.status_code == 404:
        # Board not found
```

### Parsing Errors
- Missing content: Use type or ID as fallback
- Invalid position: Set to None
- Missing connectors: Skip invalid edges

### Graph Errors
- Disconnected graph: Handle with subgraph analysis
- Cyclic dependencies: Use simple_paths with cutoff
- Missing nodes: Filter out invalid edges

## Extension Points

### 1. Custom Exporters

```python
class MyCustomExporter(ChatbotExporter):
    def export_my_format(self):
        # Custom logic here
        return {...}
```

### 2. Custom Parsers

```python
class EnhancedParser(MindmapParser):
    def _extract_text_content(self, item):
        # Enhanced extraction logic
        return super()._extract_text_content(item)
```

### 3. Graph Algorithms

```python
# Add custom graph analysis
def find_critical_paths(graph):
    # Identify most important conversation paths
    pass

def calculate_conversation_complexity(graph):
    # Measure chatbot complexity
    pass
```

## Testing Strategy

### Unit Tests
- Test each component independently
- Mock Miro API responses
- Verify data transformations

### Integration Tests
- Test full pipeline with mock data
- Verify output formats
- Check graph properties

### Example Test

```python
def test_dialogue_flow_export():
    # Setup
    board_data = create_mock_board_data()
    parser = MindmapParser()
    nodes, edges = parser.parse(board_data)

    # Execute
    converter = GraphConverter()
    graph = converter.convert(nodes, edges)
    exporter = ChatbotExporter(graph)
    result = exporter.export_dialogue_flow()

    # Assert
    assert result['format'] == 'dialogue_flow'
    assert len(result['states']) > 0
```

## Security Considerations

### API Token Security
- Store in `.env` file (never commit)
- Use environment variables in production
- Rotate tokens regularly

### Data Privacy
- Board data may contain sensitive info
- Sanitize before sharing exports
- Respect data access permissions

### Input Validation
- Validate board_id format
- Sanitize node content
- Check graph size limits

## Deployment

### Local Development
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Production
- Use secrets management for tokens
- Set up monitoring/logging
- Handle API rate limits
- Cache results when possible

## Troubleshooting Guide

### Common Issues

1. **401 Unauthorized**
   - Check MIRO_ACCESS_TOKEN
   - Verify token permissions

2. **Empty graph**
   - Verify board has items and connectors
   - Check item types are supported

3. **Disconnected graph**
   - Review board structure
   - Ensure all nodes are connected

4. **Large export files**
   - Use max_depth to limit scenarios
   - Filter by specific intent trees
   - Export subgraphs only

## Future Enhancements

- [ ] Support for Miro frames (grouping)
- [ ] Image/icon extraction from items
- [ ] Real-time board sync
- [ ] Bidirectional sync (edit → Miro)
- [ ] Webhook support for auto-update
- [ ] Visual graph preview in CLI
- [ ] Support for other mindmap tools (XMind, MindMeister)
- [ ] Direct integration with chatbot platforms
- [ ] AI-powered intent suggestion
- [ ] Conversation flow validation
