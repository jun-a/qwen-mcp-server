from typing import Any, Dict, List, Optional
import subprocess
import json
import sys
import os
from mcp.server.fastmcp import FastMCP

# Get the mcp instance from server
from qwen_mcp_server.server import mcp

@mcp.tool()
async def chat(
    prompt: str,
    model: Optional[str] = None,
    sandbox: Optional[bool] = False,
    yolo: Optional[bool] = False
) -> Dict[str, Any]:
    """Engages in a chat conversation with Qwen.
    
    Args:
        prompt: The prompt for the chat conversation.
        model: The Qwen model to use (optional).
        sandbox: Run Qwen in sandbox mode (optional).
        yolo: Automatically accept all actions (optional).
    """
    try:
        # Build the command
        cmd = ["qwen"]
        
        if model:
            cmd.extend(["-m", model])
            
        cmd.extend(["-p", prompt])
        
        if sandbox:
            cmd.append("-s")
            
        if yolo:
            cmd.append("-y")
        
        # Execute the command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            return {"response": result.stdout}
        else:
            raise Exception(f"Qwen command failed with return code {result.returncode}: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        raise Exception("Qwen command timed out")
    except Exception as e:
        raise Exception(f"Error executing Qwen command: {str(e)}")

@mcp.tool()
async def analyzeFile(
    filePath: str,
    prompt: Optional[str] = None,
    model: Optional[str] = None,
    sandbox: Optional[bool] = False,
    yolo: Optional[bool] = False
) -> Dict[str, Any]:
    """Analyzes a file using Qwen's capabilities.
    
    Args:
        filePath: The absolute path to the file to analyze.
        prompt: Additional instructions for analyzing the file (optional).
        model: The Qwen model to use (optional).
        sandbox: Run Qwen in sandbox mode (optional).
        yolo: Automatically accept all actions (optional).
    """
    try:
        # Check if file exists
        if not os.path.exists(filePath):
            raise Exception(f"File not found: {filePath}")
            
        # Build the prompt
        if prompt:
            full_prompt = f"Analyze the file '{filePath}' with these instructions: {prompt}"
        else:
            full_prompt = f"Analyze the file '{filePath}' and provide a detailed summary of its contents, purpose, and structure."
            
        # Build the command
        cmd = ["qwen"]
        
        if model:
            cmd.extend(["-m", model])
            
        cmd.extend(["-p", full_prompt])
        
        if sandbox:
            cmd.append("-s")
            
        if yolo:
            cmd.append("-y")
        
        # Execute the command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            return {"analysis": result.stdout}
        else:
            raise Exception(f"Qwen command failed with return code {result.returncode}: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        raise Exception("Qwen command timed out")
    except Exception as e:
        raise Exception(f"Error executing Qwen command: {str(e)}")

@mcp.tool()
async def changeFile(
    filePath: str,
    prompt: str,
    model: Optional[str] = None,
    sandbox: Optional[bool] = False,
    yolo: Optional[bool] = False
) -> Dict[str, Any]:
    """Modifies a file based on instructions using Qwen's capabilities.
    
    Args:
        filePath: The absolute path to the file to modify.
        prompt: Instructions for modifying the file.
        model: The Qwen model to use (optional).
        sandbox: Run Qwen in sandbox mode (optional).
        yolo: Automatically accept all actions (optional).
    """
    try:
        # Check if file exists
        if not os.path.exists(filePath):
            raise Exception(f"File not found: {filePath}")
            
        # Build the prompt
        full_prompt = f"Modify the file '{filePath}' according to these instructions: {prompt}"
            
        # Build the command
        cmd = ["qwen"]
        
        if model:
            cmd.extend(["-m", model])
            
        cmd.extend(["-p", full_prompt])
        
        if sandbox:
            cmd.append("-s")
            
        if yolo:
            cmd.append("-y")
        
        # Execute the command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            return {"result": result.stdout, "status": "File modification requested"}
        else:
            raise Exception(f"Qwen command failed with return code {result.returncode}: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        raise Exception("Qwen command timed out")
    except Exception as e:
        raise Exception(f"Error executing Qwen command: {str(e)}")