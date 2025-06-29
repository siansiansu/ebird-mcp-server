# eBird MCP Server

**Combine eBird with AI: Build Your Personal Bird Observation Assistant**

This project integrates the eBird API with an MCP (Model Context Protocol) Server, enabling you to query bird observation data via natural language directly inside Claude's chat window.

## Getting Started

### Prerequisites

- [eBird API Key](https://ebird.org/api/keygen): Create an eBird account and request an API key.
- [Claude Desktop App](https://claude.ai/download): Download and install the Claude Desktop application.
- Install [Python](https://www.python.org/downloads/) (See this [tutorial](https://pythontest.com/python/installing-python-3-11/)).

### Installation

**Clone the repository**

```bash
 git clone git@github.com:siansiansu/ebird-mcp-server.git
 cd ebird-mcp-server
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

### Configuration

**Configure Claude Desktop**

1. Open Claude Desktop.
2. Navigate to Settings > Developer > Edit Config > Edit `claude_desktop_config.json` File.
3. Replace the configuration with your paths and API key:

```json
{
  "mcpServers": {
    "ebird-api": {
      "command": "/absolute/path/to/python",
      "args": [
        "/absolute/path/to/ebird-mcp-server/server.py"
      ],
      "env": {
        "EBIRD_API_KEY": "your-ebird-api-key"
      }
    }
  }
}
```

Important:
- `command`: Absolute path to your Python executable.
- `args`: Absolute path to `server.py`.
- `EBIRD_API_KEY`: Your eBird API key.

**Restart Claude**

After saving the configuration, restart the Claude Desktop app. It will automatically launch and manage the MCP server.

## Usage

Open a chat in Claude and use any of the example prompts (or your own) to query eBird data.

## Features

Here are example prompts you can use to query data. The AI will decide when to call the eBird MCP Server, or you can explicitly instruct it to do so.

### Observations

**Query recent observations in a location**

```
What birds have been seen recently in Budai, Chiayi?
```

**Query recent observations of a species**

```
Are there any recent records of Black-faced Spoonbill in Tainan?
```

**Query notable (rare) observations**

```
What rare birds have been reported recently in Hsinchu?
```

### Checklists

**Top contributors**

```
List the top 100 eBird contributors in Taipei on June 26, 2025.
```

**All checklists on a date**

```
Show all checklists submitted in Kaohsiung on June 15, 2024.
```

**Recent checklists**

```
Provide the latest checklists submitted in Tainan.
```

**Summary statistics**

```
Summarize all observation checklists in New Taipei on June 20, 2024.
```

**Checklist details**

```
Show details for checklist ID S12345678.
```

### Hotspots

**List hotspots in a location**

```
List all eBird hotspots in Tainan.
```

**Nearby hotspots**

```
List birding hotspots within 5 km of my current location.
```

### Taxonomy

**Official taxonomy**

```
Provide the eBird taxonomy data for Black-faced Spoonbill.
```

**List subspecies**

```
List all subspecies of White-breasted Waterhen.
```

## License

This project is licensed under the MIT License.
