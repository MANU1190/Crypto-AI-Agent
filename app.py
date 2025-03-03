import streamlit as st
import os
import time
from crypto_tool import CryptoTool
from llm_agent import LLMAgent

def main():
    # Set page configuration
    st.set_page_config(page_title="Crypto Price AI Agent", page_icon="💰", layout="centered")

    # Title and description
    st.title("Crypto Price AI Agent")
    st.write("Ask me about the price of any cryptocurrency, and I’ll fetch the latest price for you!")

    # Initialize tools and agent
    crypto_tool = CryptoTool()
    together_api_key = "tgp_v1__RIq1Lo4_SEpcnMnCLOhbQv8Uajg_7X3dUaM2fXrHUY"
    if not together_api_key:
        st.error("TOGETHER_AI_API_KEY not found in environment variables. Please set it.")
        return
    agent = LLMAgent(together_api_key)

    # Initialize chat history in session state
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    # Display chat history
    st.subheader("Chat History")
    for i, message in enumerate(st.session_state.conversation_history):
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        else:
            st.write(f"**AI Agent:** {message['content']}")

    # User input (using a form to manage state better)
    with st.form(key="chat_form"):
        user_input = st.text_input("You: ", key="user_input")
        submit_button = st.form_submit_button("Send")

    # Process user input when submitted
    if submit_button and user_input:
        if user_input.lower() in ["exit", "quit"]:
            st.session_state.conversation_history = []
            st.write("**AI Agent:** Goodbye.")
            st.rerun()  # Force a rerun to update the UI
        else:
            # Step 1: Extract Cryptocurrency Name (Reasoning)
            print("AI Agent: Calling LLM to extract cryptocurrency name...")  # Terminal log
            llm_response = agent.call_llm(user_input, step=1)
            time.sleep(1)  # Add a 1-second delay between API calls

            # Update conversation history with user input
            st.session_state.conversation_history.append({"role": "user", "content": user_input})

            # Step 2: Validate Cryptocurrency Name
            if "NO_CRYPTO" in llm_response:
                final_response = "Sorry, I couldn’t understand your request. Please provide a clear cryptocurrency name."
            else:
                coin = llm_response.strip()
                print(f"AI Agent: LLM extracted cryptocurrency name: {coin}")  # Terminal log
                print("AI Agent: Calling LLM to validate cryptocurrency name...")  # Terminal log
                llm_response = agent.call_llm(user_input, step=2, coin=coin)
                time.sleep(1)  # Add a 1-second delay between API calls

                if "INVALID_COIN" in llm_response:
                    final_response = f"I’m not sure if '{coin}' is a cryptocurrency. Did you mean Bitcoin, Ethereum, or something else?"
                else:
                    # Step 3: Get the Cryptocurrency Price (Acting)
                    currency = "usd"  # Default to USD
                    print("AI Agent: Calling CryptoTool to get the price...")  # Terminal log
                    price = crypto_tool.get_price(coin, currency)
                    time.sleep(1)  # Add a 1-second delay between API calls

                    if isinstance(price, str) and "Error" in price:
                        final_response = price
                    else:
                        print(f"AI Agent: CryptoTool obtained the price: {price}")  # Terminal log
                        # Step 4: Generate Output with Few-Shot Prompting (Reasoning)
                        print("AI Agent: Calling LLM for precise output...")  # Terminal log
                        final_response = agent.call_llm(user_input, step=3, price=price, coin=coin)
                        time.sleep(1)  # Add a 1-second delay between API calls

            # Update conversation history with the final response
            if final_response:
                st.session_state.conversation_history.append({"role": "assistant", "content": final_response})

            # Display the agent's final response in the chat
            st.write(f"**AI Agent:** {final_response}")

    # Add a button to clear chat history (optional)
    if st.button("Clear Chat"):
        st.session_state.conversation_history = []
        st.rerun()  # Force a rerun to update the UI

if __name__ == "__main__":
    main()