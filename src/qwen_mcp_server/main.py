# src/qwen_mcp_server/main.py
#!/usr/bin/env python3
"""
Qwen MCP Server entry point
"""

import argparse
import asyncio
import sys
import os

# Add the parent directory to the path so we can import server
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from qwen_mcp_server.server import MCPServer, calculate, mcp

async def on_start(server, port):
    """Callback function called when server starts"""
    print(f"Qwen MCPサーバーがポート{port}で実行中です", file=sys.stderr)
    print("定義されたツール:", file=sys.stderr)
    # FastMCPからツールリストを取得
    tools = await mcp.list_tools()
    for tool in tools:
        print(f"- {tool.name}: {tool.description}", file=sys.stderr)

def main():
    """Main entry point for the MCP server"""
    parser = argparse.ArgumentParser(description="Qwen MCP Server")
    parser.add_argument("--port", type=int, default=9999, help="Port to listen on")
    args = parser.parse_args()
    
    # 新しいMCPサーバーインスタンスを作成
    server = MCPServer(args.port)
    
    async def start_callback():
        await on_start(server, args.port)
    
    print(f"Qwen MCPサーバーをポート{args.port}で起動します...", file=sys.stderr)
    asyncio.run(server.listen(start_callback))

if __name__ == "__main__":
    main()