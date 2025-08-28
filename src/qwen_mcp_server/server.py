import asyncio
import json
import argparse
from typing import Dict, Any, Callable, Optional
from websockets.server import serve
from websockets.exceptions import ConnectionClosed

class MCPServer:
    def __init__(self, port: int = 9999):
        self.port = port
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.servers = set()
        
        # 組み込みツールを定義
        self.define_tool({
            "name": "echo",
            "description": "入力テキストをエコーします",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "エコーするテキスト"}
                },
                "required": ["text"]
            }
        }, self._echo_handler)
    
    async def _echo_handler(self, input: Dict[str, Any]) -> Dict[str, Any]:
        return {"echoedText": input["text"]}
    
    def define_tool(self, tool: Dict[str, Any], handler: Callable) -> None:
        """サーバーが処理できるツールを定義"""
        self.tools[tool["name"]] = {"tool": tool, "handler": handler}
    
    async def listen(self, callback: Optional[Callable] = None) -> None:
        """サーバーを起動"""
        async def handler(websocket, path):
            print("新しいクライアントが接続されました")
            
            try:
                async for message in websocket:
                    try:
                        request = json.loads(message)
                        response = await self.handle_request(request)
                        await websocket.send(json.dumps(response))
                    except Exception as error:
                        print(f"メッセージ処理中のエラー: {error}")
                        await websocket.send(json.dumps({
                            "jsonrpc": "2.0",
                            "error": {
                                "code": -32603,
                                "message": "内部エラー",
                                "data": str(error)
                            },
                            "id": None
                        }))
            except ConnectionClosed:
                print("クライアントが切断されました")
        
        server = await serve(handler, "localhost", self.port)
        self.servers.add(server)
        print(f"Qwen MCPサーバーがポート{self.port}で実行中です")
        
        if callback:
            # コールバックがコルーチンの場合、適切に処理する
            if asyncio.iscoroutinefunction(callback):
                await callback()
            else:
                callback()
        
        await server.wait_closed()
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """受信したリクエストを処理"""
        # リクエストを検証
        if not request.get("jsonrpc") or request["jsonrpc"] != "2.0":
            return self._create_error_response(
                request.get("id"), 
                -32600, 
                "無効なリクエスト", 
                "送信されたJSONは有効なリクエストオブジェクトではありません。"
            )
        
        # 異なるメソッドを処理
        method = request.get("method")
        if method == "initialize":
            return await self._handle_initialize(request)
        elif method == "tools/list":
            return self._handle_list_tools(request)
        elif method == "tools/call":
            return await self._handle_call_tool(request)
        else:
            return self._create_error_response(
                request.get("id"), 
                -32601, 
                "メソッドが見つかりません", 
                f"メソッド '{method}' が見つかりません。"
            )
    
    def _handle_list_tools(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """tools/listリクエストを処理"""
        tools = [tool_info["tool"] for tool_info in self.tools.values()]
        return {
            "jsonrpc": "2.0",
            "result": {"tools": tools},
            "id": request.get("id")
        }
    
    async def _handle_initialize(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """initializeリクエストを処理"""
        import sys
        print("Initialize request received", file=sys.stderr)
        
        response = {
            "protocolVersion": "2025-06-18",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "qwen-mcp-server",
                "version": "1.0.0"
            }
        }
        
        print(f"Sending response: {response}", file=sys.stderr)
        return {
            "jsonrpc": "2.0",
            "result": response,
            "id": request.get("id")
        }
    
    async def _handle_call_tool(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """tools/callリクエストを処理"""
        params = request.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        
        # ツールが存在するかチェック
        if name not in self.tools:
            return self._create_error_response(
                request.get("id"), 
                -32601, 
                "メソッドが見つかりません", 
                f"ツール '{name}' が見つかりません。"
            )
        
        try:
            # ツールハンドラーを呼び出す
            handler = self.tools[name]["handler"]
            result = await handler(args)
            
            return {
                "jsonrpc": "2.0",
                "result": {"content": result},
                "id": request.get("id")
            }
        except Exception as error:
            return self._create_error_response(
                request.get("id"), 
                -32603, 
                "内部エラー", 
                str(error)
            )
    
    async def _handle_initialize(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """initializeリクエストを処理"""
        import sys
        print("Initialize request received", file=sys.stderr)
        
        response = {
            "protocolVersion": "2025-06-18",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "qwen-mcp-server",
                "version": "1.0.0"
            }
        }
        
        print(f"Sending response: {response}", file=sys.stderr)
        return {
            "jsonrpc": "2.0",
            "result": response,
            "id": request.get("id")
        }
    
    def close(self) -> None:
        """サーバーを閉じる"""
        for server in self.servers:
            server.close()

# サンプルの計算ツールを定義
async def calculate_handler(input: Dict[str, Any]) -> Dict[str, Any]:
    operation = input["operation"]
    a = input["a"]
    b = input["b"]
    
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

def main():
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
    async def on_start():
        print(f"Qwen MCPサーバーがポート{args.port}で実行中です")
        print("定義されたツール:")
        for name, tool_info in server.tools.items():
            print(f"- {name}: {tool_info['tool']['description']}")
    
    asyncio.run(server.listen(on_start))

if __name__ == "__main__":
    main()