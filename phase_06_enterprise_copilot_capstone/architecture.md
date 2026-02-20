# Enterprise Copilot - Architecture

## System Architecture

### High-Level Overview

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│      API Gateway (Azure APIM)       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   FastAPI Backend (Container Apps)  │
│  ┌──────────────────────────────┐   │
│  │   Supervisor Agent           │   │
│  │  ┌────────┐  ┌────────┐     │   │
│  │  │Research│  │  Code  │     │   │
│  │  │ Agent  │  │ Agent  │ ... │   │
│  │  └────────┘  └────────┘     │   │
│  └──────────────────────────────┘   │
└─────────────┬───────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
    ▼                   ▼
┌──────────┐    ┌──────────────┐
│  Azure   │    │ Azure AI     │
│  OpenAI  │    │   Search     │
└──────────┘    └──────────────┘
```

## Component Details

### 1. API Layer
- FastAPI REST endpoints
- Authentication & authorization
- Rate limiting
- Request validation

### 2. Agent Orchestration Layer
- Supervisor agent for routing
- Specialized agents:
  - Research Agent (RAG-based)
  - Code Agent (code generation/analysis)
  - Analysis Agent (data analysis)
- State management with LangGraph

### 3. Retrieval Layer
- Vector store (Azure AI Search)
- Hybrid search (vector + BM25)
- Re-ranking with cross-encoders
- Query optimization

### 4. LLM Layer
- Azure OpenAI Service
- Model routing (GPT-4 vs GPT-3.5)
- Token optimization
- Response caching

### 5. Monitoring Layer
- Prometheus metrics
- OpenTelemetry tracing
- Cost tracking
- Performance metrics

### 6. Storage Layer
- Azure AI Search (vector store)
- Redis (caching)
- Azure Storage (documents)

## Data Flow

1. **User Request** → API Gateway
2. **API Gateway** → FastAPI Backend
3. **Supervisor Agent** analyzes intent
4. **Route to Specialized Agent**:
   - Research queries → Research Agent → RAG System
   - Code queries → Code Agent → Direct LLM
   - Analysis queries → Analysis Agent → Tools + LLM
5. **Execute**:
   - Retrieve context (if needed)
   - Call Azure OpenAI
   - Process response
6. **Return** → User

## Scalability

- Horizontal scaling with Container Apps
- Caching for frequent queries
- Async processing for long-running tasks
- Load balancing across instances

## Security

- Managed Identity for Azure services
- KeyVault for secrets
- API key authentication
- Input validation and sanitization

## Cost Optimization

- Semantic caching
- Smart model routing
- Token optimization
- Batch processing where applicable

## Monitoring & Observability

- Request/response logging
- Token usage tracking
- Error rate monitoring
- Latency metrics
- Cost per request tracking
