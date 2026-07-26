# Financial Risk Signal Aggregator

An AI-powered prototype that consolidates structured financial data and unstructured intelligence to generate prioritized customer risk assessments for compliance teams.

---

## Overview

Financial institutions receive risk signals from multiple independent sources, including transaction histories, customer profiles, compliance alerts, and external news feeds. Analysts typically investigate these sources manually, making the review process slow and inconsistent.

This project demonstrates an end-to-end AI-powered workflow that:

- Ingests structured and unstructured financial data
- Engineers customer-level risk features
- Applies explainable rule-based risk scoring
- Uses semantic retrieval to identify relevant external news
- Generates AI-powered investigation summaries using a local Large Language Model (Llama 3.2 via Ollama)
- Produces a consolidated executive risk summary for compliance analysts

---

# Features

- Multi-source financial data ingestion
- Customer-level feature engineering
- Rule-based explainable risk scoring
- Interactive Streamlit dashboard
- Risk ranking and visualization
- Retrieval-Augmented Generation (RAG) using financial news
- AI-generated customer investigations
- Executive compliance summary
- Local LLM execution using Ollama (no paid APIs)

---

# System Architecture

```
                    +-------------------+
                    |   Customers CSV   |
                    +-------------------+
                              |
                    +-------------------+
                    | Transactions CSV  |
                    +-------------------+
                              |
                    +-------------------+
                    |   Alerts JSON     |
                    +-------------------+
                              |
                    +-------------------+
                    |    News TXT       |
                    +-------------------+
                              |
                              ▼
                  Data Ingestion & Validation
                              |
                              ▼
                  Feature Engineering Layer
                              |
                              ▼
                Rule-Based Risk Scoring Engine
                              |
                              ▼
                 Ranked Customer Risk Scores
                              |
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
         Interactive Dashboard      AI Investigation
                                            |
                              Semantic News Retrieval
                                            |
                                            ▼
                             Prompt Construction
                                            |
                                            ▼
                               Ollama (Llama 3.2)
                                            |
                                            ▼
                       Customer Investigation Reports
                                            |
                                            ▼
                           Executive Risk Summary
```

---

# Project Structure

```
Financial-Risk-Signal-Aggregator/

│
├── app.py
├── requirements.txt
├── scripts/
│   └── generate_data.py
│
├── data/
│   └── sample/
│
└── src/
    ├── ingestion/
    │   ├── loader.py
    │   ├── validator.py
    │   └── schemas.py
    │
    ├── features/
    │   ├── engineer.py
    │   ├── rules.py
    │   └── scorer.py
    │
    └── llm/
        ├── retriever.py
        ├── prompt_builder.py
        ├── ollama_client.py
        ├── summarizer.py
        └── executive_summary.py
```

---

# Technology Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Scikit-learn
- SentenceTransformers
- Ollama
- Llama 3.2
- Requests

---

# AI Workflow

The AI reasoning pipeline follows a Retrieval-Augmented Generation (RAG) approach.

1. Top high-risk customers are selected.
2. Customer signals are converted into a semantic query.
3. Relevant news articles are retrieved using sentence embeddings and cosine similarity.
4. Customer profile, alerts, risk signals, and retrieved news are combined into a structured prompt.
5. Llama 3.2 generates a detailed investigation report.
6. Individual reports are summarized into an executive compliance report.

---

# Risk Scoring Logic

Customer risk scores are computed using transparent business rules.

Examples include:

- High average transaction value
- Frequent transactions involving high-risk countries
- Heavy cryptocurrency activity
- Multiple failed transactions
- Multiple device usage
- Politically Exposed Person (PEP)
- Sanction list match
- AML investigation alerts
- Dormant account reactivation
- Structuring patterns

Scores are normalized to a maximum of 100 and classified into:

- Low
- Medium
- High
- Critical

---

# Synthetic Dataset

The project includes a synthetic dataset generator that creates realistic financial scenarios.

Generated files:

- customers.csv
- transactions.csv
- alerts.json
- news.txt

Special injected scenarios include:

- Sanctioned customer
- Politically Exposed Person
- High-risk crypto transfers
- Structuring transactions
- Card fraud attempts
- Dormant account reactivation

---

# Design Considerations

Several design decisions were made while building the prototype.

### Explainability over Black-Box Models

A transparent rule-based scoring engine was chosen so that compliance analysts can understand why each customer received a particular risk score.

### Local AI Inference

The application uses Ollama with Llama 3.2, allowing all AI reasoning to run locally without relying on external APIs or transmitting sensitive financial data.

### Retrieval-Augmented Generation

Instead of providing the entire news corpus to the language model, only semantically relevant articles are retrieved. This improves response quality while reducing prompt size.

### Modular Architecture

The project separates data ingestion, feature engineering, scoring, retrieval, prompt construction, and LLM interaction into independent modules, making the system easier to maintain and extend.

### Human-Centric Outputs

The final output is designed for compliance analysts rather than data scientists, combining quantitative risk scores with AI-generated explanations and actionable recommendations.

---

# Data Assumptions

The prototype assumes:

- Customer IDs are consistent across all datasets.
- Uploaded datasets follow the expected schema.
- Transaction timestamps are valid.
- Alerts reference existing customers.
- News articles are provided as plain text separated by article delimiters.
- Risk rules are illustrative and not intended to replace production AML models.

---

# Installation

## Clone repository

```bash
git clone <https://github.com/abhaysinghiit/Financial-Risk-Signal-Aggregator>

cd Financial-Risk-Signal-Aggregator
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Install Ollama

Download:

https://ollama.com

Pull the model:

```bash
ollama pull llama3.2
```

Start Ollama:

```bash
ollama serve
```

---

# Running the Application

Generate sample data (optional):

```bash
python generate_data.py
```

Launch Streamlit:

```bash
streamlit run app.py
```

Upload:

- customers.csv
- transactions.csv
- alerts.json
- news.txt

Click **Generate AI Risk Report** to produce customer investigations and the executive summary.

---

# Example Input

Input:

- 100 customers
- 1,000+ transactions
- Compliance alerts
- External financial news

Output:

- Customer risk ranking
- Risk scores
- Triggered risk signals
- AI-generated investigation summaries
- Executive compliance summary

---

# Future Enhancements

Given additional development time, the following enhancements could be explored:

- Machine learning–based anomaly detection
- Real-time transaction ingestion
- Analyst feedback loop for continuous improvement
- PDF report generation
- Natural language query interface

---

# Author

Abhay Singh

M.Tech Data Science

Indian Institute of Technology Roorkee
