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

The application is deployed via Streamlit Community Cloud.

---

## Core Features

- Single YouTube URL processing
- Subtitle-based transcript extraction
- Token-aware chunking
- Parallel chunk summarization (`ThreadPoolExecutor`)
- Final-stage streamed document generation
- Dynamic heading generation
- Markdown export support

---

## Tech Stack

- Python 3.10+
- Streamlit
- OpenAI API
- youtube-transcript-api
- tiktoken

---

## Performance Strategy

The application reduces latency by parallelizing chunk-level API calls while preserving deterministic output order. Streaming is applied only during the final document synthesis stage to ensure clarity and structured presentation.


