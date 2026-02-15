# AURA TRIAGE 🏥

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-1.0-orange)
![Status](https://img.shields.io/badge/Status-Live-success)

## 🌐 Live Demo
🔗 https://aura-triage.onrender.com

---

## 📌 Overview

**AURA (Automated Urgency Risk Assessment) TRIAGE** is an AI-powered clinical triage system designed to evaluate patient severity using vital parameters, symptom analysis, and a structured risk scoring model.

The system assists in prioritizing patients based on clinical urgency, enabling faster and smarter medical decision-making.

---

## 🔥 Core Features

- 🧠 Severity Index Calculation
- 🚦 Risk Classification (Stable / Moderate / Critical)
- 🏥 Department Recommendation
- 📊 Interactive Dashboard Analytics
- 📄 Automated PDF Report Generation
- 🆔 Unique Patient ID Generation
- 🌍 Fully Deployed Web Application

---

## 🛠️ Tech Stack

### 💻 Frontend
- HTML
- CSS
- JavaScript

### ⚙️ Backend
- Python
- Flask Framework

### 🗄️ Database
- SQLite

### 📄 Reporting
- ReportLab (PDF Generation)

### 🚀 Deployment
- Render (Gunicorn Production Server)

---

## 📊 Severity Index Model

The system evaluates patients based on:

- Age
- Blood Pressure
- Heart Rate
- Temperature
- Symptoms
- Existing Medical Conditions

### Risk Categories:

- 🟢 **Stable** → Low priority
- 🟡 **Moderate Attention** → Requires monitoring
- 🔴 **Critical Priority** → Immediate medical intervention

The output includes:
- Severity Index
- Risk Level
- Department Allocation
- Confidence Score
- Estimated Wait Time

---

## 🚀 Installation & Local Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/AURA-TRIAGE.git
cd AURA-TRIAGE
