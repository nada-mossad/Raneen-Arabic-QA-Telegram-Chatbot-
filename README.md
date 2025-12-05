# 🛍️ Raneen Arabic QA Chatbot

A smart **Arabic question-answering chatbot** built using **FastAPI**,
**Haystack**, and the **Telegram Bot API**.\
All product data used by the chatbot is **web-scraped from the Raneen
website**, then indexed for semantic retrieval and answer extraction.

## Project Overview

This system provides an intelligent product assistant that answers
Arabic questions about items listed on **Raneen.com**.\
It integrates: 
- FastAPI backend
- Haystack QA pipeline
- Telegram chatbot
- Web-scraped Arabic product dataset

## Objectives

-   Build a natural Arabic conversational QA system
-   Retrieve the best-matching product description using semantic
    similarity
-   Extract accurate answers using a transformer reader
-   Provide results via Telegram interface

## Dataset (Web-Scraped From Raneen)

Dataset scraped from Raneen website stored in CSV and converted to Haystack Documents.

## System Architecture

### 1. Telegram Bot (Frontend)

-   Sends user queries to backend
-   Displays answers and product links

### 2. FastAPI Backend

-   Hosts `/ask` endpoint
-   Runs QA inference

### 3. Haystack QA Pipeline

#### Retriever

Model: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

#### Reader

Model: `deepset/xlm-roberta-large-squad2`

## API Endpoint

### POST /ask

Example:

``` json
{ "query": "عايزة اعرف سعر طقم الحلل" }
```

## Features

-   Arabic language support
-   Real‑time Telegram interaction
-   Semantic retrieval + transformer reader
-   Easy to extend

## Limitations

-   In‑memory document store
-   Local hosting
-   Minimal error handling

