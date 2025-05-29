# Blender MCP + Amazon Bedrock Agent Integration

This example demonstrates how to connect the Blender MCP server to Amazon Bedrock Agents using Claude 3.7 as the foundation model.

## Overview

This integration allows you to:
- Connect to a Blender MCP server
- Register Blender tools with Amazon Bedrock Agents
- Create an interactive session where Claude can control Blender through natural language

## Prerequisites

- Python 3.10+
- Blender 3.0+ with the BlenderMCP addon installed and running
- AWS credentials configured with Bedrock access
- `uv` package manager installed

## Setup

1. Make sure Blender is running with the BlenderMCP addon enabled:
   - In Blender, go to the 3D View sidebar (press N if not visible)
   - Find the "BlenderMCP" tab
   - Click "Connect to Claude"

2. Install the required dependencies:
   ```bash
   pip install boto3 mcp-client-py
   ```

3. Set your AWS credentials and region:
   ```bash
   export AWS_REGION=us-east-1  # Change to your preferred region
   ```

## Running the Example

1. Start the example:
   ```bash
   python blender_bedrock_agent.py
   ```

2. An interactive session will start where you can type instructions for Claude to control Blender.

3. Example prompts:
   - "Create a simple scene with a cube and a sphere"
   - "Make the cube red and the sphere blue"
   - "Add a light source above the objects"
   - "Get information about the current scene"

4. Type 'exit' to quit the session.

## How It Works

1. The script connects to the Blender MCP server using the `MCPStdio` client
2. It retrieves the available tools and their schemas from the MCP server
3. These tools are registered with a Bedrock Agent using Claude 3.7
4. User inputs are sent to the agent, which may decide to use Blender tools
5. When tools are invoked, the results are sent back to the agent for further processing

## Troubleshooting

- **Connection issues**: Make sure the Blender addon server is running
- **AWS errors**: Verify your AWS credentials and Bedrock access
- **Tool invocation errors**: Check the logs for detailed error messages

## Security Note

This example allows Claude to execute arbitrary Python code in Blender through the `execute_blender_code` tool. Use with caution in production environments and always save your work before using it.
