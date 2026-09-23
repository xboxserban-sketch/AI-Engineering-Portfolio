# 👨‍💻 Software & AI Engineer Portfolio

Welcome to my engineering portfolio. This repository showcases my ability to design and build **robust, production-ready AI systems, automated data pipelines, and responsive frontend dashboards**.

My engineering philosophy focuses on architectural best practices: **containerization (Docker), idempotent data flows, strict AI tool boundaries, and comprehensive error handling.**

---

## 🚀 Featured Systems

### 1. [AI Visual Workflow Builder](./AI_Visual_Workflow_Builder) 🔗
*A visual drag-and-drop AI workflow builder (Zapier/Make.com for AI).*
* **Tech Stack:** React 18 + TypeScript (React Flow), Python/FastAPI, Docker Compose
* **Demonstrates:** Topological DAG Execution, Idempotent Processing, Fault-Tolerant Node Execution, Real-time Monitoring
* **Tests:** 4/4 Passed ✅

### 2. [Autonomous AI Swarm](./Autonomous_AI_Swarm) 🤖
*Multi-agent AI system with real-time WebSocket communication and a live Command Center dashboard.*
* **Tech Stack:** React 18 + TypeScript (Framer Motion), Python/FastAPI + WebSockets, Docker Compose
* **Demonstrates:** Multi-Agent Architecture, Strict Permission Matrix (Tool Boundaries), Fault-Tolerant Consensus Protocol, Live Observation Dashboard
* **Tests:** 5/5 Passed ✅

### 3. [Cinematic Doc Engine](./Cinematic_Doc_Engine) 🎬
*Enterprise-grade AI media orchestration pipeline for automated documentary generation.*
* **Tech Stack:** Python 3.11, OpenAI / ElevenLabs APIs, Docker
* **Demonstrates:** Multi-LLM Orchestration, Idempotent Processing, Fallback Mechanisms, Strict Data Boundaries (JSON Validation)
* **Tests:** 3/3 Passed ✅

### 4. [Enterprise Lead Gen](./Enterprise_Lead_Gen) 🏢
*High-throughput automated B2B data pipeline with intelligent web crawling.*
* **Tech Stack:** Python, SQLite, Google Maps API, Docker
* **Demonstrates:** Relational Databases (ACID), API Integration, Rate-Limiting, Resilient Data Flow Architecture
* **Tests:** 2/2 Passed ✅

### 5. [Autopilot AI Dashboard](./Autopilot_AI) 🚗
*Smart, asynchronous vehicle telematics UI with real-time data visualization.*
* **Tech Stack:** JavaScript (ES6+), HTML/CSS, NGINX (Docker)
* **Demonstrates:** UI State Management, Component-Based Architecture, Asynchronous Rendering

---

## 🧪 Quality Engineering & Testing

All backend systems include isolated unit test suites. External API dependencies are mocked to ensure reliable CI/CD pipelines without incurring API costs.

```
Total Tests: 14/14 Passed ✅
├── AI_Visual_Workflow_Builder  → 4 tests (topological sort, cycle detection, execution, idempotency)
├── Autonomous_AI_Swarm         → 5 tests (boundaries, lifecycle, routing, WebSocket format, rejection flow)
├── Cinematic_Doc_Engine        → 3 tests (idempotency, JSON validation, fallback mechanism)
└── Enterprise_Lead_Gen         → 2 tests (database insertion, rate limiting)
```

## 🐳 Containerization

Every project is fully containerized with production-ready Dockerfiles. Multi-service projects use `docker-compose.yml` for orchestration.

## 📬 Contact

Open to remote opportunities in AI/ML engineering and full-stack development. Feel free to explore the code and reach out.
