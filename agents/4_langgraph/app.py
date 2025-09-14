import gradio as gr
from sidekick import Sidekick
import asyncio
import os
from dotenv import load_dotenv
import io
import sys
from contextlib import redirect_stdout, redirect_stderr

# Load environment variables
load_dotenv(override=True)

# Pushover credentials
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_USER = os.getenv("PUSHOVER_USER")

# Global log storage
log_messages = []

def log_print(*args, **kwargs):
    """Custom print function that captures logs for the web interface"""
    message = ' '.join(str(arg) for arg in args)
    print(message)  # Still print to console
    log_messages.append(message)
    # Keep only last 100 messages to prevent memory issues
    if len(log_messages) > 100:
        log_messages.pop(0) 

def clear_logs():
    """Clear log messages"""
    global log_messages
    log_messages = []
    return "Logs cleared"

async def setup():
    log_print(f"🔧 [SETUP] Initializing Sidekick...")
    sidekick = Sidekick()
    log_print(f"⚙️ [SETUP] Setting up Sidekick with tools...")
    await sidekick.setup()
    log_print(f"✅ [SETUP] Sidekick setup completed successfully")
    return sidekick

def get_logs():
    """Get current log messages for display"""
    return "\n".join(log_messages[-50:])  # Show last 50 messages

def process_message_sync(sidekick, message, success_criteria, history):
    """Synchronous wrapper for async process_message"""
    log_print(f"🔄 [APP] Processing message: {message[:50]}...")
    log_print(f"🎯 [APP] Success criteria: {success_criteria}")
    log_print(f"📚 [APP] Current history length: {len(history) if history else 0}")
    
    try:
        # Run the async function
        log_print(f"⚙️ [APP] Creating new event loop for async execution")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        log_print(f"🚀 [APP] Starting async superstep execution")
        
        # Temporarily redirect stdout to capture sidekick logs
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        result = loop.run_until_complete(sidekick.run_superstep(message, success_criteria, history))
        
        # Capture any output from sidekick
        captured_output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        # Add captured output to logs
        if captured_output.strip():
            for line in captured_output.strip().split('\n'):
                if line.strip():
                    log_messages.append(line.strip())
        
        log_print(f"✅ [APP] Async execution completed successfully")
        log_print(f"📊 [APP] Result length: {len(result) if result else 0}")
        
        loop.close()
        return result, sidekick, get_logs()
    except Exception as e:
        log_print(f"❌ [APP] Error in process_message_sync: {e}")
        log_print(f"🔍 [APP] Error type: {type(e).__name__}")
        import traceback
        log_print(f"📋 [APP] Traceback: {traceback.format_exc()}")
        
        # Return error in history in correct Gradio format
        error_history = list(history) if history else []
        error_history.append([None, f"❌ Error: {str(e)}"])
        return error_history, sidekick, get_logs()

def reset_sync():
    """Synchronous reset function"""
    log_print(f"🔄 [RESET] Resetting interface")
    return "", "", [], get_logs()

def free_resources(sidekick):
    print(f"🧹 [CLEANUP] Cleaning up resources")
    try:
        if sidekick:
            print(f"🔧 [CLEANUP] Cleaning up Sidekick instance")
            sidekick.cleanup()
            print(f"✅ [CLEANUP] Cleanup completed successfully")
    except Exception as e:
        print(f"❌ [CLEANUP] Exception during cleanup: {e}")

# Create the interface
with gr.Blocks(title="Sidekick", theme=gr.themes.Default(primary_hue="emerald")) as ui:
    gr.Markdown("## Lalit Personal Co-Worker")
    gr.Markdown("**Features:** 🔍 Web Search | 📝 File Writing | 🔔 Push Notifications")
    
    sidekick = gr.State()

    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(label="Sidekick", height=300)
        with gr.Column(scale=1):
            log_display = gr.Textbox(
                label="📊 Live Progress Log", 
                max_lines=20,
                interactive=False,
                value="Waiting for activity..."
            )
    
    with gr.Group():
        with gr.Row():
            message = gr.Textbox(
                show_label=False, 
                placeholder="Your request to the Sidekick (e.g., 'Find a French restaurant in Dubai and send me a push notification')",
                value="I'd like to go for dinner tomorrow in a French restaurant in DUBAI. Please find a great French restaurant and write a report in markdown to dinner.md including the name, address, menu, reviews. Send me a push notification with the restaurant name and phone."
            )
        with gr.Row():
            success_criteria = gr.Textbox(
                show_label=False, 
                placeholder="What are your success criteria?",
                value="Find a French restaurant in Dubai, create a markdown report with all details, and send push notification"
            )
    
    with gr.Row():
        reset_button = gr.Button("Reset", variant="stop")
        go_button = gr.Button("Go!", variant="primary")
        refresh_logs_button = gr.Button("🔄 Refresh Logs", variant="secondary")
        clear_logs_button = gr.Button("🗑️ Clear Logs", variant="secondary")

    # Event handlers
    ui.load(setup, [], [sidekick])
    
    message.submit(
        process_message_sync, 
        [sidekick, message, success_criteria, chatbot], 
        [chatbot, sidekick, log_display]
    )
    
    success_criteria.submit(
        process_message_sync, 
        [sidekick, message, success_criteria, chatbot], 
        [chatbot, sidekick, log_display]
    )
    
    go_button.click(
        process_message_sync, 
        [sidekick, message, success_criteria, chatbot], 
        [chatbot, sidekick, log_display]
    )
    
    reset_button.click(
        reset_sync, 
        [], 
        [message, success_criteria, chatbot, log_display]
    )
    
    refresh_logs_button.click(
        get_logs,
        [],
        [log_display]
    )
    
    clear_logs_button.click(
        clear_logs,
        [],
        [log_display]
    )

print("🚀 Starting Sidekick with Push Notifications...")
print(f"🔔 Pushover Token: {PUSHOVER_TOKEN[:10] if PUSHOVER_TOKEN else 'None'}...")
print(f"👤 Pushover User: {PUSHOVER_USER[:10] if PUSHOVER_USER else 'None'}...")
print(f"🌐 Launching Gradio interface...")
ui.launch(inbrowser=True, share=True)
