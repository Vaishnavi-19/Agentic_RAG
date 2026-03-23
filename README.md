# Agentic RAG

This project demonstrates an Agentic Retrieval-Augmented Generation (RAG) workflow.

## What is RAG?

RAG (Retrieval-Augmented Generation) combines two steps:

1. Retrieve relevant knowledge from an external source (vector database, search index, web, docs).
2. Generate an answer with an LLM using the retrieved context.

Instead of asking the model to answer from parametric memory alone, RAG grounds responses in fresh, source-based context.

## Why Use RAG?

- Reduces hallucinations by grounding answers in retrieved evidence.
- Supports private or domain-specific knowledge not present in model training data.
- Improves freshness because new documents can be indexed without retraining the LLM.
- Makes responses more auditable because context can be inspected.

## Typical RAG Flow

1. User asks a question.
2. Question is embedded and matched against indexed chunks.
3. Top relevant chunks are retrieved.
4. LLM answers using question + retrieved context.
5. Optional post-checks validate quality and route to retries, web search, or clarification.

## What is Agentic RAG?

Agentic RAG adds decision-making steps around retrieval and generation.
Instead of a fixed pipeline, the system can choose actions such as:

- Rewriting the query when retrieval quality is low.
- Running web search when internal documents are insufficient.
- Grading retrieved chunks before generation.
- Iterating until confidence or quality criteria are met.

This project follows that pattern by using graph nodes for retrieval, grading, optional web search, and final generation.

## Corrective vs Self vs Adaptive RAG

These three patterns are related but solve different control problems.

| Pattern | Core Idea | Trigger | Main Action | Strength | Trade-off |
|---|---|---|---|---|---|
| Corrective RAG | Fix low-quality retrieval before final answer | Retrieval relevance is poor | Correct retrieval set (filter, re-rank, re-query, fallback search) | Better grounding and factuality | Extra latency and orchestration complexity |
| Self-RAG | Model critiques and improves its own output process | Internal self-evaluation signals uncertainty or gaps | Generate, critique, revise (possibly retrieve again) | Better answer quality and reasoning transparency | More tokens and longer inference chains |
| Adaptive RAG | Dynamically choose strategy based on query type/difficulty | Router detects simple vs complex or known vs unknown query | Skip retrieval, use lightweight retrieval, or use multi-step retrieval/search | Cost and latency optimization with better task fit | Requires robust routing logic and evaluation |

## Simple Intuition

- Corrective RAG asks: Are my retrieved documents good enough?
- Self-RAG asks: Is my current answer good enough?
- Adaptive RAG asks: Which workflow should I run for this question?

## When to Prefer Each

1. Use Corrective RAG when retrieval quality is the main bottleneck.
2. Use Self-RAG when answer faithfulness and completeness need extra verification.
3. Use Adaptive RAG when query diversity is high and you need cost-aware routing.

## Practical Evaluation Metrics for RAG

- Retrieval Precision at k: fraction of retrieved chunks that are relevant.
- Retrieval Recall at k: how much of needed evidence appears in top k chunks.
- Groundedness/Faithfulness: answer claims supported by provided context.
- Answer Relevance: how directly the response addresses the user query.
- Latency: end-to-end response time.
- Cost: token and tool usage per query.

## Common Failure Modes

- Bad chunking: important facts split across chunks.
- Poor embeddings: semantic mismatch for your domain.
- Weak prompts: model ignores or underuses context.
- No fallback path: retrieval miss leads to hallucinated answer.
- Missing evaluation loop: quality degrades unnoticed over time.

## Next Improvements You Can Add

1. Add query rewriting before retrieval.
2. Add document re-ranking after first-pass retrieval.
3. Add citation extraction for each generated claim.
4. Add confidence scoring and abstain behavior.
5. Add offline evaluation datasets and automated regressions.