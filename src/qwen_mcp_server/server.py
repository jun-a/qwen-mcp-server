from typing import Any, Dict, Callable, Optional
import asyncio
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("qwen-mcp-server")

class MCPServer:
    def __init__(self, port: int = 9999):
        self.port = port
        self.tools: Dict[str, Dict[str, Any]] = {}
        
        # 組み込みツールを定義
        @mcp.tool()
        async def echo(text: str) -> Dict[str, Any]:
            """入力テキストをエコーします"""
            return {"echoedText": text}
    
    def define_tool(self, tool: Dict[str, Any], handler: Callable) -> None:
        """サーバーが処理できるツールを定義"""
        # FastMCPにツールを登録
        tool_name = tool["name"]
        tool_description = tool["description"]
        
        # デコレータを使ってツールを登録
        decorated_handler = mcp.tool(name=tool_name, description=tool_description)(handler)
        self.tools[tool_name] = {"tool": tool, "handler": decorated_handler}
    
    async def listen(self, callback: Optional[Callable] = None) -> None:
        """サーバーを起動"""
        if callback:
            # コールバックがコルーチンの場合、適切に処理する
            if asyncio.iscoroutinefunction(callback):
                await callback()
            else:
                callback()
        
        # FastMCPサーバーをSTDIOで実行（非同期版）
        await mcp.run_async(transport='stdio')
    
    def close(self) -> None:
        """サーバーを閉じる"""
        # FastMCPでは特別な終了処理は不要
        pass

# サンプルの計算ツールを定義
@mcp.tool()
async def calculate(
    operation: str, 
    a: float, 
    b: float
) -> Dict[str, Any]:
    """基本的な算術演算を実行します
    
    Args:
        operation: 実行する演算（add, subtract, multiply, divide）
        a: 最初のオペランド
        b: 2番目のオペランド
    """
    if operation == "add":
        return {"result": a + b}
    elif operation == "subtract":
        return {"result": a - b}
    elif operation == "multiply":
        return {"result": a * b}
    elif operation == "divide":
        if b == 0:
            raise ValueError("ゼロ除算")
        return {"result": a / b}
    else:
        raise ValueError(f"不明な演算: {operation}")