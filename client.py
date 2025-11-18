import asyncio
import sys
from urllib.parse import urlparse
from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from mcp import StdioServerParameters

USE_STDIO = True  # True: stdio 모드 / False: SSE 모드

async def run_stdio():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server_stdio.py"]
    )
    async with stdio_client(server_params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            await interact(session)

async def run_sse(server_url: str):
    if urlparse(server_url).scheme not in ("http", "https"):
        print("Error: Server URL must start with http:// or https://")
        sys.exit(1)
    try:
        async with sse_client(server_url) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                await session.initialize()
                await interact(session)
    except Exception as e:
        print(f"Error connecting to server: {e}")
        sys.exit(1)

async def interact(session: ClientSession):
    # 도구 호출
    add_result = await session.call_tool("add", arguments={"a": 10, "b": 15})
    print("Add result:", add_result.content[0].text)
    
    subtract_result = await session.call_tool("subtract", arguments={"a": 20, "b": 8})
    print("Subtract result:", subtract_result.content[0].text)
    
    multiply_result = await session.call_tool("multiply", arguments={"a": 5, "b": 6})
    print("Multiply result:", multiply_result.content[0].text)
    
    divide_result = await session.call_tool("divide", arguments={"a": 15.0, "b": 3.0})
    print("Divide result:", divide_result.content[0].text)

if __name__ == "__main__":
    if USE_STDIO:
        asyncio.run(run_stdio())
    else:
        if len(sys.argv) != 2:
            print("Usage: python client.py <server_url>")
            sys.exit(1)
        asyncio.run(run_sse(sys.argv[1]))



