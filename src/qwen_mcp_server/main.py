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

from qwen_mcp_server.server import MCPServer, calculate_handler

async def on_start(server, port):
    """Callback function called when server starts"""
    print(f"Qwen MCPサーバーがポート{port}で実行中です")
    print("定義されたツール:")
    for name, tool_info in server.tools.items():
        print(f"- {name}: {tool_info['tool']['description']}")

def main():
    """Main entry point for the MCP server"""
    parser = argparse.ArgumentParser(description="Qwen MCP Server")
    parser.add_argument("--port", type=int, default=9999, help="Port to listen on")
    args = parser.parse_args()
    
    # 新しいMCPサーバーインスタンスを作成
    server = MCPServer(args.port)
    
    # カスタムツールを定義
    server.define_tool({
        "name": "calculate",
        "description": "基本的な算術演算を実行します",
        "inputSchema": {
            "type": "object",
            "properties": {
                "operation": { 
                    "type": "string", 
                    "description": "実行する演算（add, subtract, multiply, divide）",
                    "enum": ["add", "subtract", "multiply", "divide"]
                },
                "a": {"type": "number", "description": "最初のオペランド"},
                "b": {"type": "number", "description": "2番目のオペランド"}
            },
            "required": ["operation", "a", "b"]
        }
    }, calculate_handler)
    
    # サーバーを起動
    async def start_callback():
        await on_start(server, args.port)
    
    print(f"Qwen MCPサーバーをポート{args.port}で起動します...")
    asyncio.run(server.listen(start_callback))

if __name__ == "__main__":
    main()