# YouTube -> Structured Technical Notes Generator

An AI-powered Streamlit application that transforms subtitle-enabled YouTube videos into structured technical documentation using large language models.

The system extracts transcripts, performs parallel summarization to reduce latency, and streams a dynamically generated, hierarchically structured final document with technical breakdown.

---

## Overview

This project demonstrates an optimized LLM processing pipeline designed for:

- Context-window safe transcript handling
- Latency-aware parallel inference
- Clean streaming user experience
- Modular service-layer architecture

---

## Core Features

- Single YouTube URL processing
- Subtitle-based transcript extraction
- Token-aware chunking
- Parallel chunk summarization (`ThreadPoolExecutor`)
- Final-stage streamed document generation
- Dynamic heading generation
- PDF export support

---

## Demo

![Demo Recording](assests/demo-recording.mp4)

## Tech Stack

- Python 3.10+
- Streamlit
- OpenAI API
- youtube-transcript-api
- tiktoken

---

## To run locally

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Malavika-Raja/AI-YouTube-Notes-System.git
```
### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```
Activate:

```bash
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Add Environment Variables

Create a .env file:

```bash
OPENAI_API_KEY=your_api_key_here
```

### 5️⃣ Run the App

```bash
streamlit run app.py
```

## Performance Strategy

The application reduces latency by parallelizing chunk-level API calls while preserving deterministic output order. Streaming is applied during the final document synthesis stage to ensure clarity and structured presentation.


