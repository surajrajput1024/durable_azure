## Power BI Data Change Triggered  Analysis Pipeline (Azure)

## Objective

Automatically detect and process **Power BI dataset changes**, and run **scalable Python-based analysis** (e.g., outlier detection, etc.) using **Azure Durable Functions**. Final results are saved or delivered to a client endpoint.

---

## High-Level Architecture Overview

```mermaid
flowchart TD
    %% --- Source System ---
    A1[Power BI Dataset]:::source -->|Refresh Triggered| A2[Power BI Refresh Event]:::event

    %% --- Automation Layer ---
    A2 --> B1[Power Automate Flow]:::logic
    B1 -->|Trigger HTTP POST| C1[Azure Function: HTTP Trigger]:::azure

    %% --- Durable Function Orchestration ---
    C1 --> C2[Durable Orchestrator Function]:::azure

    %% --- Activity Functions ---
    C2 --> D1[Fetch Data from Power BI API]:::activity
    D1 --> D2[Store Raw Data in Blob Storage]:::storage

    D2 --> E1[Read Data in Chunks]:::activity
    E1 --> E2[Fan-Out: Parallel Chunk Processors]:::activity
    E2 --> E3[Each Chunk: Dask + PyOD Analysis]:::compute

    E3 --> E4[Fan-In: Aggregate Results]:::activity
    E4 --> F1[Store Results or Send via Webhook]:::output

    %% --- External Output ---
    F1 --> F2[Client Webhook or Viewer]:::client

    %% Better, Clean Color Scheme
    classDef source fill:#DCE775,stroke:#AFB42B,color:#1B1B1B
    classDef event fill:#FFF176,stroke:#FBC02D,color:#1B1B1B
    classDef logic fill:#81D4FA,stroke:#0288D1,color:#1B1B1B
    classDef azure fill:#64B5F6,stroke:#1976D2,color:#1B1B1B
    classDef activity fill:#AED581,stroke:#558B2F,color:#1B1B1B
    classDef compute fill:#4DB6AC,stroke:#00796B,color:#1B1B1B
    classDef storage fill:#FFCC80,stroke:#EF6C00,color:#1B1B1B
    classDef output fill:#B39DDB,stroke:#512DA8,color:#1B1B1B
    classDef client fill:#F06292,stroke:#C2185B,color:#1B1B1B

```

---

## Tech Stack Overview

| Layer | Component | Technology |
| --- | --- | --- |
| **Source** | Dataset | Power BI |
| **Trigger Automation** | Refresh Event | Power Automate |
| **Pipeline Entry** | HTTP Trigger | Azure Function (Python) |
| **Workflow Engine** | Durable Orchestration | Azure Durable Functions |
| **Storage** | Intermediate & Final | Azure Blob Storage |
| **Processing** | Scalable Analysis | Dask + PyOD |
| **ML Model** | Outlier Detection | IsolationForest, LOF (via PyOD) |
| **Fan-out/Fan-in** | Parallelism | Durable Fan-out Activities |
| **Client Output** | Results Delivery | Webhook or Blob Explorer |

---

## Execution Flow

1. Power BI dataset gets refreshed (scheduled or manually).
2. Power Automate listens for the dataset refresh completion.
3. Power Automate triggers Azure Function via HTTP.
4. Durable Orchestrator begins:
    - Fetches data from Power BI REST API
    - Stores raw data in Azure Blob Storage
    - Reads data in chunks
    - Processes each chunk with `Dask + PyOD`
    - Aggregates and stores/sends results

---

## Why this?

- **Scalable** for millions of rows via Dask chunking
- **Event-driven** via Power BI + Power Automate
- **Durable & Serverless**: no infrastructure maintenance
- **Flexible** to add more models/steps later

---