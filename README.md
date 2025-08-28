# Qwen MCP Server

Python implementation of the Qwen MCP Server that can be installed as a package and run from anywhere.

## Installation

```bash
cd qwen-mcp-server
uv build
pip install dist/*.whl
```

## Usage

```bash
qwen-mcp-server [--port PORT]
```

By default, the server will run on port 9999. You can specify a different port using the `--port` option.

## Integration
To use this server with Claude Desktop, add the following to your `mcp.json`:

```json
{
  "mcpServers": {
    "qwen": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/jun-a/qwen-mcp-server",
        "qwen-mcp-server"
      ]
    }
  }
}
```
