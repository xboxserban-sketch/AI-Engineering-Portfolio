# AI Visual Workflow Builder

![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

A modern, robust visual drag-and-drop AI workflow builder (like Zapier/Make.com but for AI). Users create workflows by dragging AI nodes onto a canvas and connecting them.

## Architecture & Features

- **Topological DAG Execution**: Built a custom execution engine that resolves node dependencies and executes workflows using topological sorting. Ensures data flows correctly from source nodes to terminal nodes.
- **Idempotent Processing**: Safely retry failed workflows. The engine persists state and skips already-completed nodes (ExecutionStatus.SUCCESS), only resuming from the point of failure.
- **Fault-Tolerant Node Execution**: Built for resilience. If a single node fails, the failure is caught, logged, and isolated. Downstream dependencies are skipped, while independent branches continue executing.
- **Real-time Execution Monitoring**: Includes execution status tracking.
- **Structured JSON Logging**: Observability out-of-the-box with full JSON structured logs for the backend.

## Tech Stack
- **Backend**: Python, FastAPI, Pydantic, topological graph traversal
- **Frontend**: React, TypeScript, React Flow
- **Infra**: Docker, Docker Compose

## Quick Start
1. Copy `.env.example` to `.env`
2. Run `docker-compose up --build`
3. Access UI on `http://localhost` and API on `http://localhost:8000/docs`
