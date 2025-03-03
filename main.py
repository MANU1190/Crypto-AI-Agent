import os
import logging
import time  # Import the time module
from crypto_tool import CryptoTool
from llm_agent import LLMAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Use your Together AI API key
    together_api_key = os.environ.get("TOGETHER_AI_API_KEY")
    if not together_api_key:
        raise ValueError("TOGETHER_AI_API_KEY not found in environment variables. Please set it.")

    # Initialize tools and agent
    crypto_tool = CryptoTool()
    agent = LLMAgent(together_api_key)

    print("AI Agent: Hello! I can fetch cryptocurrency prices for you. How can I help?")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("AI Agent: Goodbye.")
            break

        try:
            # Step 1: Extract Cryptocurrency Name
            print("AI Agent: Calling LLM to extract cryptocurrency name...")
            llm_response = agent.call_llm(user_input, step=1)
            time.sleep(1)  # Add a 1-second delay between API calls

            if "NO_CRYPTO" in llm_response:
                final_response = "Sorry, I couldn’t understand your request. Please provide a clear cryptocurrency name."
                print(f"AI Agent: {final_response}")
                continue

            coin = llm_response.strip()
            print("AI Agent: LLM extracted cryptocurrency name:", coin)

            # Step 2: Validate Cryptocurrency Name
            print("AI Agent: Calling LLM to validate cryptocurrency name...")
            llm_response = agent.call_llm(user_input, step=2, coin=coin)
            time.sleep(1)  # Add a 1-second delay between API calls

            if "INVALID_COIN" in llm_response:
                final_response = f"I’m not sure if '{coin}' is a cryptocurrency. Did you mean Bitcoin, Ethereum, or something else?"
                print(f"AI Agent: {final_response}")
                continue

            # Step 3: Get the Cryptocurrency Price
            currency = "usd"  # Default to USD
            print("AI Agent: Calling CryptoTool to get the price...")
            price = crypto_tool.get_price(coin, currency)
            time.sleep(1) # Add a 1-second delay

            if isinstance(price, str) and "Error" in price:
                final_response = price
                print(f"AI Agent: {final_response}")
                continue

            print("AI Agent: CryptoTool obtained the price:", price)

            # Step 4: Generate Output with Few-Shot Prompting
            print("AI Agent: Calling LLM for precise output...")
            llm_response = agent.call_llm(user_input, step=3, price=price, coin=coin)
            time.sleep(1)  # Add a 1-second delay between API calls
            final_response = llm_response

            print(f"AI Agent: {final_response}")

        except Exception as e:
            logging.exception("An unexpected error occurred")
            final_response = f"Sorry, I couldn’t process your request: {str(e)}"
            print(f"AI Agent: {final_response}")

if __name__ == "__main__":
    main()
