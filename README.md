# 🏗️ Agentic AI for Safety Monitoring with Construction Risk Analytics

An AI-powered construction safety and risk monitoring platform designed to continuously analyze construction-site conditions and worker safety data.

The system uses specialized AI agents to identify hazards, assess risk, monitor PPE compliance, detect unsafe worker behavior, generate safety alerts, and provide actionable recommendations through an interactive dashboard.

---

## 📌 Project Overview

Construction sites involve multiple risks such as:

- Unsafe environmental conditions
- Poor visibility
- Wet or unsafe floor conditions
- Faulty equipment
- Worker PPE violations
- Unsafe worker behavior
- High-risk construction zones

Traditional monitoring methods can be manual and reactive.

This project aims to build an **agent-based construction risk intelligence platform** that analyzes monitoring data and provides automated risk assessment and safety insights.

---

# 🎯 Project Objectives

The main objectives of this project are:

- Detect construction-site hazards
- Calculate site risk scores
- Monitor worker safety
- Detect PPE violations
- Identify unsafe worker behavior
- Generate safety alerts
- Provide safety recommendations
- Analyze worker safety by construction zone
- Generate structured safety reports
- Provide an interactive Streamlit dashboard

---

# 🧠 System Architecture

The project follows a modular agent-based architecture.

```text
                    Construction Risk Intelligence
                              Platform
                                  │
                ┌─────────────────┴─────────────────┐
                │                                   │
        Site Risk Agent                       Safety Agent
                │                                   │
        Site Monitoring Data                 Worker Safety Data
                │                                   │
        Hazard Detection                    PPE Detection
                │                            Behavior Analysis
        Risk Scoring                              │
                │                            Safety Scoring
                │                                   │
        Site Risk Report                    Safety Alerts
                │                                   │
                └─────────────────┬─────────────────┘
                                  │
                           Processed Results
                                  │
                                  ▼
                         Streamlit Dashboard