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

## Available Tools

The Qwen MCP Server provides the following tools:

1. **calculate** - Performs basic arithmetic operations (add, subtract, multiply, divide)
2. **echo** - Echoes input text
3. **chat** - Engages in a chat conversation with Qwen
4. **analyzeFile** - Analyzes a file using Qwen's capabilities
5. **changeFile** - Modifies a file based on instructions using Qwen's capabilities

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
