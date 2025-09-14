from playwright.async_api import async_playwright
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from dotenv import load_dotenv
import os
import requests
from langchain.agents import Tool
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_experimental.tools import PythonREPLTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper



load_dotenv(override=True)
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_user = os.getenv("PUSHOVER_USER")
pushover_url = "https://api.pushover.net/1/messages.json"
serper = GoogleSerperAPIWrapper()

async def playwright_tools():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    return toolkit.get_tools(), browser, playwright


def push(text: str):
    """Send a push notification to the user"""
    print(f"🔔 [PUSH] Sending push notification: {text[:50]}...")
    try:
        response = requests.post(pushover_url, data = {"token": pushover_token, "user": pushover_user, "message": text})
        if response.status_code == 200:
            print(f"✅ [PUSH] Notification sent successfully")
            return "Push notification sent successfully"
        else:
            print(f"❌ [PUSH] Failed to send notification: {response.status_code}")
            return f"Failed to send push notification: {response.status_code}"
    except Exception as e:
        print(f"❌ [PUSH] Error sending notification: {e}")
        return f"Error sending push notification: {e}"


def get_file_tools():
    toolkit = FileManagementToolkit(root_dir="sandbox")
    return toolkit.get_tools()


def search_with_progress(query: str):
    """Search the web with progress logging"""
    print(f"🔍 [SEARCH] Searching for: {query}")
    try:
        result = serper.run(query)
        print(f"✅ [SEARCH] Found {len(result)} results")
        return result
    except Exception as e:
        print(f"❌ [SEARCH] Error: {e}")
        return f"Search error: {e}"

def python_repl_with_progress(code: str):
    """Run Python code with progress logging"""
    print(f"🐍 [PYTHON] Executing code: {code[:100]}...")
    try:
        from langchain_experimental.tools import PythonREPLTool
        repl = PythonREPLTool()
        result = repl.run(code)
        print(f"✅ [PYTHON] Code executed successfully")
        return result
    except Exception as e:
        print(f"❌ [PYTHON] Error: {e}")
        return f"Python execution error: {e}"

def wiki_search_with_progress(query: str):
    """Search Wikipedia with progress logging"""
    print(f"📚 [WIKIPEDIA] Searching for: {query}")
    try:
        wikipedia = WikipediaAPIWrapper()
        wiki_tool = WikipediaQueryRun(api_wrapper=wikipedia)
        result = wiki_tool.run(query)
        print(f"✅ [WIKIPEDIA] Found Wikipedia information")
        return result
    except Exception as e:
        print(f"❌ [WIKIPEDIA] Error: {e}")
        return f"Wikipedia search error: {e}"

async def other_tools():
    push_tool = Tool(name="send_push_notification", func=push, description="Use this tool when you want to send a push notification")
    file_tools = get_file_tools()

    tool_search = Tool(
        name="search",
        func=search_with_progress,
        description="Use this tool when you want to get the results of an online web search"
    )

    python_repl = Tool(
        name="python_repl",
        func=python_repl_with_progress,
        description="Use this tool when you want to run Python code"
    )

    wiki_tool = Tool(
        name="wikipedia",
        func=wiki_search_with_progress,
        description="Use this tool when you want to search Wikipedia for information"
    )
    
    return file_tools + [push_tool, tool_search, python_repl, wiki_tool]

