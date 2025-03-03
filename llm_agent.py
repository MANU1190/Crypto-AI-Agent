import requests
import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LLMAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.together.xyz/inference"  # As confirmed working
        self.conversation_history = []

    def call_llm(self, user_input, price=None, step=1, coin=None):
        """Call the LLaMA 3.8B chat model via Together AI API, with separate prompts for each ReACT step."""

        # Step 1: Extract Cryptocurrency Name
        if step == 1:
            system_prompt = (
                "You are a helpful AI agent. Your task is to extract the cryptocurrency name from the user's query.\n"
                "If the query contains a cryptocurrency name, respond *only* with the name.\n"
                "If the query does not contain a cryptocurrency name, respond *only* with 'NO_CRYPTO'."
                "Example:\n"
                "User: What is the price of Bitcoin?\n"
                "AI: Bitcoin"
            )
            payload = self._prepare_payload(system_prompt, user_input)
            return self._make_api_call(payload)

        # Step 2: Validate Cryptocurrency Name and Direct to Tool
        elif step == 2:
            system_prompt = (
                f"You are a helpful AI agent. Your task is to validate the cryptocurrency name: '{coin}'.\n"
                "If '{coin}' is a valid cryptocurrency (e.g., Bitcoin, Ethereum, Dogecoin), respond *only* with 'VALID_COIN:{coin}'.\n"
                "If '{coin}' is not a valid cryptocurrency, respond *only* with 'INVALID_COIN'."
                "Example:\n"
                "User: Bitcoin\n"
                "AI: VALID_COIN:bitcoin"
            )
            payload = self._prepare_payload(system_prompt, user_input)
            return self._make_api_call(payload)

        # Step 3: Generate Output with Few-Shot Prompting
        elif step == 3:
            system_prompt = (
                "You are a helpful AI agent. Your task is to generate a concise, natural-language response with the cryptocurrency price.\n"
                "Use the following examples as a guide:\n"
                "User: Price query for bitcoin in usd. Price: $96,262.14\n"
                "AI: The current price of Bitcoin is $96,262.14 USD."
                "User: Price query for ethereum in eur. Price: €2,500\n"
                "AI: The current price of Ethereum is €2,500 EUR."
                f"Now generate the response for the following:\n"
                f"User: Price query for {coin} in usd. Price: {price}\n"
                f"AI:"
            )
            payload = self._prepare_payload(system_prompt, user_input, price)
            return self._make_api_call(payload)

        else:
            return "Invalid step."

    def _prepare_payload(self, system_prompt, user_input, price=None):
        """Prepare the payload for the Together AI API call."""
        messages = [{"role": "system", "content": system_prompt}]
        messages.append({"role": "user", "content": user_input})
        if price:
            messages.append({"role": "system", "content": f"Price: {price}"})
        payload = {
            "model": "meta-llama/Llama-3-8b-chat-hf",  # As confirmed working
            "messages": messages,
            "max_tokens": 200,
            "temperature": 0.1,
        }
        return payload

    def _make_api_call(self, payload):
        """Make the API call to the Together AI API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            logging.info(f"Calling URL: {self.url}")  # Debug logging
            logging.debug(f"Payload: {payload}")  # Debug logging
            response = requests.post(self.url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            logging.debug(f"Response: {result}")  # Debug logging

            # Updated response parsing for inference
            assistant_response = result.get("output", {}).get("choices", [{}])[0].get("text", "").strip()
            return assistant_response

        except requests.RequestException as e:
            if e.response is not None:
                if e.response.status_code == 401:
                    error_message = "Error: Unauthorized (401). Please check your Together AI API key."
                elif e.response.status_code == 429:
                    error_message = "Error: Too Many Requests (429). You might be rate limited. Please try again later."
                else:
                    error_message = f"Error calling LLM: {e.response.status_code} - {e}"
            else:
                error_message = f"Error calling LLM: {e}. Could not connect to the API."

            logging.error(error_message)
            return error_message
        except ValueError as e:
            logging.error(f"Value error: {e}")
            return f"Value error: {e}"
        except Exception as e:
            logging.exception("An unexpected error occurred")  # Logs the full traceback
            return f"Sorry, I couldn’t process your request: {str(e)}"

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
