# Chat with Wiki App

Welcome to the Chat with Wiki App repository! This interactive web application allows users to engage in a chat-based conversation with OpenAI's GPT-3.5-turbo model, leveraging information extracted from Wikipedia.

## Overview

The Chat with Wiki App combines natural language processing techniques and the power of GPT-3.5-turbo to provide a conversational experience. Users can input a Wikipedia URL, and the app extracts relevant information from the page, creating a dynamic context for the conversation.

## Features

- Extracts information from Wikipedia pages using BeautifulSoup and requests.
- Utilizes langchain for text splitting, embeddings, and conversational retrieval.
- Implements a Streamlit interface for user interaction.
- Leverages OpenAI's GPT-3.5-turbo for generating conversational responses.

## How to Use

1. Visit the [Chat with Wiki App](https://chat-wiki.streamlit.app/) web page.
2. Enter a Wikipedia URL to extract information.
3. Engage in a chat-based conversation with the GPT-3.5-turbo model.

## Files in This Repository

- `app.py`: Main application file containing the Streamlit app setup and interaction with langchain and OpenAI models.
- `get_wiki.py`: Module for extracting information from Wikipedia pages using BeautifulSoup.

## Hosting

The Chat with Wiki App is hosted at [https://chat-wiki.streamlit.app/](https://chat-wiki.streamlit.app/).


Happy chatting with Wiki!
