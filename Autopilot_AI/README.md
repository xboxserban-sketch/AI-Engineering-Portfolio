# 🚗 Autopilot AI Dashboard

[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)]()
[![Frontend](https://img.shields.io/badge/Frontend-Vanilla_JS-blue.svg)]()
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)]()

## 📌 Overview
The **Autopilot AI Dashboard** is a smart vehicle management interface. It acts as the frontend layer for an AI-driven vehicle analytics system, processing telematics data (fuel levels, maintenance predictions, GPS coordinates) and rendering them in a highly responsive, real-time UI.

This project demonstrates strong frontend architecture, data visualization, and asynchronous state management, ticking the boxes for full-stack capability and robust interface design.

## 🏗️ Technical Highlights
* **State Management:** Uses local storage and memory states to persist telematic data (e.g., fuel settings, parking location) across sessions.
* **Component-Based Logic:** Although written in Vanilla JS/ES6, the architecture mimics React's component lifecycles (modular functions for rendering maintenance lists, modals, and charts).
* **Asynchronous Integration:** Built to connect seamlessly with backend Python/FastAPI microservices.
* **Containerized Deployment:** Fully dockerized via Nginx for lightning-fast delivery in production environments.

## 🚀 How to Run (Docker)
To spin up the dashboard in an isolated container:
```bash
docker build -t autopilot-ai .
docker run -p 8080:80 autopilot-ai
```
Then navigate to `http://localhost:8080` in your browser.

## 🧪 Quality Engineering
The UI logic is separated from the DOM manipulation layer, making the system fully compatible with modern E2E testing frameworks like Cypress or Playwright.
