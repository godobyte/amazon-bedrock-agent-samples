#!/usr/bin/env python3
"""
Blender MCP Server Integration with Amazon Bedrock Agents

This example demonstrates how to connect a Blender MCP server to Amazon Bedrock
using Claude 3.7 as the foundation model.
"""

import asyncio
import json
import os
import boto3
import logging
import sys
from typing import Dict, Any, List

# Import the MCP client classes
from InlineAgent.tools.mcp import MCPStdio
from mcp import StdioServerParameters

from InlineAgent.agent import InlineAgent
from InlineAgent.action_group import ActionGroup

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Bedrock client setup
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name=os.environ.get("AWS_REGION", "us-west-2")
)

async def setup_blender_mcp_server():
    """
    Set up and connect to the Blender MCP server.
    
    Returns:
        tuple: (mcp_client, function_schema, callable_tools)
    """
    # Define server parameters for Blender MCP
    server_params = StdioServerParameters(
        command="uvx",
        args=["blender-mcp"]
    )
    
    # Create the MCP client
    logger.info("Connecting to Blender MCP server...")
    mcp_client = await MCPStdio.create(
        server_params=server_params,
        tools_to_use=set()  # Use all available tools
    )
    
    logger.info(f"Connected to Blender MCP server with {len(mcp_client.callable_tools)} tools")
    
    return mcp_client, mcp_client.function_schema, mcp_client.callable_tools

async def create_bedrock_agent(mcp_client) -> InlineAgent:
    """
    Create a Bedrock Agent with the Blender MCP tools.
    
    Args:
        mcp_client: The MCP client with tools
        
    Returns:
        InlineAgent: The configured Bedrock Agent
    """
    # Create action groups with the MCP client
    action_groups = [
        ActionGroup(
            name="BlenderMCPTools",
            description="Tools for interacting with Blender through the Model Context Protocol",
            mcp_clients=[mcp_client]
        )
    ]
    
    # Create the agent with Claude 3 Sonnet
    agent = InlineAgent(
        foundation_model="us.anthropic.claude-3-5-haiku-20241022-v1:0",
        # foundation_model="us.anthropic.claude-3-7-sonnet-20240620-v1:0",
        instruction="You are an expert 3D artist assistant that helps users create and modify 3D scenes in Blender. Use the available Blender tools to help users visualize their ideas.",
        action_groups=action_groups,
        agent_name="BlenderMCPAgent"
    )
    
    logger.info(f"Created Bedrock Agent with Blender MCP tools")
    return agent

async def interactive_session(agent: InlineAgent):
    """
    Run an interactive session with the Bedrock Agent and Blender MCP.
    
    Args:
        agent: The Bedrock Agent
    """
    print("\n=== Blender MCP + Amazon Bedrock Agent Interactive Session ===")
    print("Type 'exit' to quit\n")
    
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        try:
            # Send the input to the agent
            agent_response = await agent.invoke(
                input_text=user_input,
            )
                
        except Exception as e:
            logger.error(f"Error during agent invocation: {str(e)}")
            print(f"\nError: {str(e)}")

async def invoke_session(agent: InlineAgent, inputs: list[str]):
    """
    Run an interactive session with the Bedrock Agent and Blender MCP.
    
    Args:
        agent: The Bedrock Agent
        inputs: User inputs for MCP to run
    """
    print("\n=== Blender MCP + Amazon Bedrock Agent Invoke Session ===")

    for user_input in inputs:
        try:
            print(f"\n--- Invoking with input {user_input}")
            agent_response = await agent.invoke(
                input_text=user_input,
            )
            
        except Exception as e:
            logger.error(f"Error during agent invocation: {str(e)}")
            print(f"\nError: {str(e)}")


async def main():
    """Main function to run the example."""
    try:
        # setup_blender_agent()

        # Set up the Blender MCP server
        mcp_client, function_schema, callable_tools = await setup_blender_mcp_server()
        
        # Create the Bedrock Agent
        agent = await create_bedrock_agent(mcp_client)
        
        if sys.argv[1] == "interactive":
            # Run the interactive session
            await interactive_session(agent)
        else:
            # Run invoke with cmd line args
            await invoke_session(agent, sys.argv[1:])


    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        # Clean up resources
        if 'mcp_client' in locals():
            await mcp_client.cleanup()
        logger.info("Session ended")

if __name__ == "__main__":
    asyncio.run(main())
