#!/usr/bin/env python3
"""
Test script for Qwen MCP Server tools
"""

import asyncio
from qwen_mcp_server.tools import chat, analyzeFile, changeFile
import os

async def test_chat():
    """Test the chat tool"""
    print("Testing chat tool...")
    try:
        result = await chat("Hello, what can you do?")
        print(f"Chat result: {result}")
    except Exception as e:
        print(f"Chat error: {e}")

async def test_analyze_file():
    """Test the analyzeFile tool"""
    print("\nTesting analyzeFile tool...")
    try:
        # Create a test file in the project directory
        test_file = "test.txt"
        with open(test_file, "w") as f:
            f.write("This is a test file for Qwen MCP Server tool testing.")
        
        result = await analyzeFile(os.path.abspath(test_file), "What is this file about?")
        print(f"AnalyzeFile result: {result}")
        
        # Clean up
        os.remove(test_file)
    except Exception as e:
        print(f"AnalyzeFile error: {e}")

async def test_change_file():
    """Test the changeFile tool"""
    print("\nTesting changeFile tool...")
    try:
        # Create a test file in the project directory
        test_file = "test_change.txt"
        with open(test_file, "w") as f:
            f.write("This is a test file that should be modified.")
        
        result = await changeFile(os.path.abspath(test_file), "Change this text to say 'File successfully modified by Qwen MCP Server'")
        print(f"ChangeFile result: {result}")
        
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)
    except Exception as e:
        print(f"ChangeFile error: {e}")

async def main():
    """Run all tests"""
    print("Testing Qwen MCP Server tools...\n")
    
    await test_chat()
    await test_analyze_file()
    await test_change_file()
    
    print("\nAll tests completed.")

if __name__ == "__main__":
    asyncio.run(main())