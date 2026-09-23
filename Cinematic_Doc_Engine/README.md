# 🎬 Cinematic Doc Engine

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![AI Integration](https://img.shields.io/badge/AI-OpenAI%20%7C%20ElevenLabs-orange.svg)]()

## 📌 Overview
**Cinematic Doc Engine** is an enterprise-grade, fully automated AI media orchestration pipeline. It takes a raw topic and autonomously researches, scripts, generates voiceovers, sources B-roll footage, and renders a production-ready video documentary. 

This project demonstrates the ability to integrate multiple LLMs and AI services into a **robust, resilient system** with strict data boundaries, error handling, and idempotent processing workflows.

## 🏗️ Architecture & Data Flow

The system is built on a modular architecture, decoupling the AI generation from the rendering engine to ensure stability and cost-efficiency.

1. **Narrative Engine (`narrative_engine.py`):** Interfaces with LLMs to generate structured, strictly formatted JSON scripts. Enforces tool boundaries to prevent hallucination.
2. **Audio Engine (`elevenlabs_engine.py`):** Handles text-to-speech synthesis with automatic retry logic and fallback mechanisms.
3. **Asset Hunter (`video_broll_hunter.py`):** Scrapes and indexes contextual video assets based on the LLM's semantic tags.
4. **Render Engine (`render_longform_documentary.py`):** Assembles the final artifact. Uses idempotent file-checking (doesn't re-download or re-generate assets if a previous run failed).

## 🚀 Key Technical Features
* **Production-Ready AI Integration:** Complex prompt engineering with deterministic outputs (JSON enforcement).
* **Containerization:** Fully Dockerized environment ensuring consistent execution across development and production.
* **Resilience & Logging:** Comprehensive error handling around external API calls with exponential backoff.
* **Idempotency & State Management:** Ensures that interrupted processes can resume without duplicating API costs.

## ⚙️ Quick Start (Docker)

1. Clone the repository.
2. Add your API keys to the `.env` file.
3. Build and run the container:
```bash
docker build -t cinematic-doc-engine .
docker run --env-file .env cinematic-doc-engine
```

## 🧪 Testing Strategy
The architecture supports robust testing. External AI API calls are isolated, allowing unit tests to mock AI responses and validate the internal pipeline logic without incurring API usage costs.
