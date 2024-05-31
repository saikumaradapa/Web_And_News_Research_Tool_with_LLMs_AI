# TeckyBot: Web Research Tool 📈

TeckyBot is a News/ Web Research Tool designed to assist users in extracting information and generating answers from provided URLs.

Developed by [Sai Kumar Adapa](https://www.linkedin.com/in/sai-kumar-adapa-5a16b2228/)

## Overview

TeckyBot is a web-based application built using Python and Streamlit framework. It leverages various natural language processing (NLP) techniques to extract text from provided URLs, create a vector database, and generate answers to user queries based on the extracted content.

## Features

- **Data Extraction:** TeckyBot fetches content from specified URLs using the `requests` library and extracts text using `BeautifulSoup`.
- **Vector Database Creation:** It creates a vector database using the extracted text and saves it locally using `FAISS`.
- **Question Answering:** Users can input queries, and TeckyBot generates answers based on the provided content using a pre-trained language model (GooglePalm) and a retrieval-based question answering system.
- **User Interface:** The application interface is built using Streamlit, providing an intuitive and interactive experience for users.

## Usage

1. Input URLs of news articles or web pages in the sidebar.
2. Click the "Process URLs" button to extract text and create the vector database.
3. Enter your query in the text area provided.
4. Click the "Get Answer" button to generate an answer based on your query.

## Installation

Clone the repository:

```bash
git clone https://github.com/saikumaradapa/TeckyBot.git
```

## Dependencies:

--> requests: For fetching web content. <br>
--> BeautifulSoup: For HTML parsing.<br>
--> Streamlit: For building the web interface.<br>
--> langchain: For natural language processing tasks such as embeddings, text splitting, and question answering.<br>
--> dotenv: For loading environment variables.<br>
