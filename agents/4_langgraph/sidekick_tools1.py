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
pushover_token = os.getenv("PUSHOVER_TOKEN") or "a2k3z2e88z9fhyutq1pweqcdkus4cc"
pushover_user = os.getenv("PUSHOVER_USER") or "uqokrzf6ufdu6qjmbst9dcyz4191qh"
pushover_url = "https://api.pushover.net/1/messages.json"
serper = GoogleSerperAPIWrapper()

async def playwright_tools():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    return toolkit.get_tools(), browser, playwright


def push(text: str):
    """Send a push notification to the user"""
    try:
        print(f"🔔 Sending push notification: {text}")
        print(f"🔔 Using token: {pushover_token}")
        print(f"🔔 Using user: {pushover_user}")
        
        if not pushover_token or not pushover_user:
            error_msg = "❌ Pushover credentials not configured properly"
            print(error_msg)
            return error_msg
        
        response = requests.post(pushover_url, data={
            "token": pushover_token, 
            "user": pushover_user, 
            "message": text,
            "title": "Sidekick Notification"
        })
        
        print(f"🔔 Pushover response status: {response.status_code}")
        print(f"🔔 Pushover response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == 1:
                print("✅ Push notification sent successfully!")
                return "✅ Push notification sent successfully!"
            else:
                error_msg = f"❌ Pushover API error: {result.get('errors', 'Unknown error')}"
                print(error_msg)
                return error_msg
        else:
            error_msg = f"❌ HTTP error {response.status_code}: {response.text}"
            print(error_msg)
            return error_msg
            
    except Exception as e:
        error_msg = f"❌ Error sending push notification: {str(e)}"
        print(error_msg)
        return error_msg


def get_file_tools():
    toolkit = FileManagementToolkit(root_dir="sandbox")
    return toolkit.get_tools()


async def other_tools():
    push_tool = Tool(name="send_push_notification", func=push, description="Use this tool when you want to send a push notification")
    file_tools = get_file_tools()

    tool_search =Tool(
        name="search",
        func=serper.run,
        description="Use this tool when you want to get the results of an online web search"
    )

    wikipedia = WikipediaAPIWrapper()
    wiki_tool = WikipediaQueryRun(api_wrapper=wikipedia)

    python_repl = PythonREPLTool()
    
    return file_tools + [push_tool, tool_search, python_repl,  wiki_tool]

