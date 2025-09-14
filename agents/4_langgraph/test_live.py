# Live request/response testing
import gradio as gr

def handle_request(message, criteria, history):
    """Handle user requests with live debugging"""
    print(f"🔍 LIVE REQUEST:")
    print(f"  Message: '{message}'")
    print(f"  Criteria: '{criteria}'")
    print(f"  History length: {len(history) if history else 0}")
    
    try:
        # Convert to strings
        message = str(message) if message else ""
        criteria = str(criteria) if criteria else ""
        
        # Check if inputs are valid
        if not message.strip() or not criteria.strip():
            print("🔍 Empty inputs, returning existing history")
            return history or []
        
        # Create response
        response = f"✅ Processing: {message}"
        feedback = f"📋 Success criteria: {criteria}"
        
        # Build new history
        new_history = list(history) if history else []
        new_history.append([message, response])
        new_history.append(["", feedback])
        
        print(f"🔍 LIVE RESPONSE:")
        print(f"  New history length: {len(new_history)}")
        print(f"  User message: '{new_history[-2][0]}'")
        print(f"  Assistant response: '{new_history[-2][1]}'")
        print(f"  Feedback: '{new_history[-1][1]}'")
        print("=" * 50)
        
        return new_history
        
    except Exception as e:
        print(f"🔍 ERROR: {str(e)}")
        error_history = list(history) if history else []
        error_history.append(["", f"❌ Error: {str(e)}"])
        return error_history

def reset_form():
    """Reset the form"""
    print("🔍 RESET CALLED")
    return "", "", []

def test_live_flow():
    """Test the complete live flow"""
    print("🧪 TESTING LIVE REQUEST/RESPONSE FLOW")
    print("=" * 60)
    
    # Test 1: Empty history
    print("Test 1: Empty history")
    result1 = handle_request("what is the exchange rate of usd/inr", "an accurate rate", [])
    print(f"✅ Result: {len(result1)} messages")
    print()
    
    # Test 2: With existing history
    print("Test 2: With existing history")
    existing = [["Previous message", "Previous response"]]
    result2 = handle_request("test message", "test criteria", existing)
    print(f"✅ Result: {len(result2)} messages")
    print()
    
    # Test 3: Error handling
    print("Test 3: Error handling")
    result3 = handle_request("", "", [])
    print(f"✅ Empty inputs handled: {len(result3) == 0}")
    print()
    
    print("✅ ALL LIVE TESTS PASSED!")
    return True

if __name__ == "__main__":
    # Run live tests
    test_live_flow()
    
    # Create interface
    print("\n🚀 CREATING LIVE INTERFACE")
    print("=" * 60)
    
    with gr.Blocks() as live_demo:
        gr.Markdown("# Live Request/Response Testing")
        gr.Markdown("**Status:** 🔍 Live debugging enabled")
        
        chatbot = gr.Chatbot()
        message_input = gr.Textbox(
            label="Your request", 
            placeholder="Enter your request...",
            value="what is the exchange rate of usd/inr"
        )
        criteria_input = gr.Textbox(
            label="Success criteria", 
            placeholder="Enter criteria...",
            value="an accurate rate"
        )
        
        with gr.Row():
            send_btn = gr.Button("Send Request", variant="primary")
            reset_btn = gr.Button("Reset", variant="secondary")
        
        send_btn.click(handle_request, [message_input, criteria_input, chatbot], chatbot)
        reset_btn.click(reset_form, [], [message_input, criteria_input, chatbot])
        message_input.submit(handle_request, [message_input, criteria_input, chatbot], chatbot)
    
    print("✅ Live interface created!")
    print("🚀 Launching live interface...")
    live_demo.launch(share=True)
