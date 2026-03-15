import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run():
    server_params = StdioServerParameters(
        command=r"C:\Users\Franco\AppData\Local\Programs\Python\Python314\Scripts\notebooklm-mcp.exe",
        args=[],
        env=None
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Session initialized")
            # List tools
            tools = await session.list_tools()
            print(f"Number of tools: {len(tools.tools)}")
            # List notebooks
            result = await session.call_tool("notebook_list", {"max_results": 100})
            import json
            data = json.loads(result.content[0].text)
            if data.get("status") == "success":
                notebooks = data.get("notebooks", [])
                print(f"Total notebooks: {data.get('count')}")
                print("\nApp Notebooks found:")
                found = False
                for nb in notebooks:
                    title = nb.get("title", "")
                    if "App" in title:
                        print(f"- {title} (ID: {nb.get('notebook_id')}) (Modified: {nb.get('modified_at')})")
                        found = True
                if not found:
                    print("- No notebooks found with 'App' in the title.")
            else:
                print(f"Error: {data}")

if __name__ == "__main__":
    asyncio.run(run())
