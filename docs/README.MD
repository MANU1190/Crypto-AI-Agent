# Crypto Price AI Agent

A ReACT-style AI agent built with Python that fetches real-time cryptocurrency prices using the Together AI API (LLaMA 3.8B model) and the CoinGecko API. The agent processes user queries in a conversational manner, validates cryptocurrency names, and generates concise, natural-language responses. It supports both a console-based interface (`main.py`) and a web-based interface using Streamlit (`app.py`).

## Overview

This project implements an agentic application that follows the ReACT (Reasoning and Acting) pattern:
1. Extracts and validates cryptocurrency names from user queries using an LLM.
2. Fetches real-time prices from CoinGecko using a custom `CryptoTool`.
3. Generates polished, user-friendly responses using the LLM.

The agent maintains context, handles errors gracefully, and includes rate limiting to prevent API overuse.

## Features

- **ReACT Flow**: Processes user queries in a reasoning-acting loop to extract, validate, fetch, and respond with cryptocurrency prices.
- **Dynamic Cryptocurrency Validation**: Uses CoinGecko to dynamically validate any cryptocurrency, not just a static list.
- **Real-Time Pricing**: Fetches current prices for cryptocurrencies (e.g., Bitcoin, Ethereum, Dogecoin) in USD, EUR, INR, or GBP.
- **Conversational Interface**: Supports natural language queries in a console or web UI.
- **Error Handling**: Includes robust error handling for API failures, invalid inputs, and rate limits.
- **Rate Limiting**: Implements 1-second delays between API calls to avoid rate limiting issues.
- **Web Interface**: Provides a user-friendly Streamlit app for interactive queries.

## Prerequisites

- Python 3.8 or higher
- An active Together AI API key (for the LLaMA 3.8B model)
- Internet connection (for API calls to Together AI and CoinGecko)

## Installation

1.  **Clone the repository:**

    ```
    git clone : https://github.com/MANU1190/Crypto-AI-Agent.git
    cd : https://github.com/MANU1190/Crypto-AI-Agent.git
    ```

2.  **Create a virtual environment:**

    ```
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    *   On Windows:

        ```
        .\venv\Scripts\activate
        ```

    *   On macOS and Linux:

        ```
        source venv/bin/activate
        ```

4.  **Install the dependencies:**

    ```
    pip install -r requirements.txt
    ```

## Configuration

1.  **Set the Together AI API key:**

    *   Obtain an API key from [Together AI](https://api.together.xyz/).
    *   Set the API key as an environment variable named `TOGETHER_AI_API_KEY`. You can do this in your `.env` file or directly in your system's environment variables.

    *   **Create a `.env` file (recommended):**

        ```
        touch .env
        ```

    *   Add the following line to your `.env` file, replacing `your_api_key` with your actual API key:

        ```
        TOGETHER_AI_API_KEY=your_api_key
        ```

## Usage

1.  **Run the Streamlit application:**

    ```
    streamlit run app.py
    ```

2.  **Interact with the AI agent:**

    *   Open the Streamlit application in your web browser (usually at `http://localhost:8501`).
    *   Enter your query in the text input field and press "Send".
    *   The AI agent will respond with the current price of the cryptocurrency.

## Code Structure

The project consists of the following main files:

-   `app.py`: Streamlit application that provides a user interface for interacting with the AI agent.
-   `crypto_tool.py`: Class for fetching cryptocurrency prices from the CoinGecko API.
-   `llm_agent.py`: Class for interacting with the Together AI API for natural language processing.
-   `main.py`: Main script that orchestrates the entire process.
-   `requirements.txt`: Lists the project's dependencies.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to suggest improvements or report bugs.
