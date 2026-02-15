
# 🚀 RAG API with Deterministic CI/CD Pipeline

## 📌 Overview

This project implements a Retrieval-Augmented Generation (RAG) API with automated CI/CD validation using GitHub Actions.

It goes beyond basic RAG implementation by solving a critical real-world problem:

> LLM outputs are non-deterministic, making automated testing unreliable.

To address this, I implemented **Mock LLM mode**, enabling deterministic retrieval testing inside CI pipelines.

This mirrors production-grade AI system design.

---

## 🛠 Tech Stack

* API Framework: FastAPI
* Vector Database: ChromaDB
* LLM: Ollama (TinyLlama)
* CI/CD: GitHub Actions
* Testing: Semantic validation script
* Embeddings: Custom embed pipeline

---

## 🏗 Architecture

```
User Query
    ↓
FastAPI
    ↓
ChromaDB (Vector Search)
    ↓
Retrieved Context
    ↓
Production Mode → Ollama (LLM)
Mock Mode → Return Context Directly
```

---

# 🔍 The Core Problem: LLM Non-Determinism

To test retrieval quality, I intentionally removed the keyword **“orchestration”** from the knowledge base.

After rebuilding embeddings and querying the API multiple times:

* Sometimes the answer included “orchestration”
* Sometimes it did not
* The output changed for the same query

Why?

Because the LLM was trained associating:

```
Kubernetes ↔ Orchestration
```

Even though the knowledge base no longer contained the word.

This exposed a serious issue:

> Automated tests become unreliable when generation is probabilistic.

---

# 🧠 Why This Matters

In CI/CD:

* Tests must be deterministic
* Builds must be reliable
* Failures must reflect real issues

If LLM output varies randomly:

* Tests pass when they shouldn’t
* Tests fail when nothing changed
* Engineers lose trust in CI
* Real regressions get ignored

This is unacceptable in production systems.

---

# ✅ The Solution: Mock LLM Mode

I implemented an environment-variable-driven mode:

```python
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "0") == "1"
```

### Production Mode

* Uses Ollama for natural language responses.

### Mock Mode

* Returns retrieved context directly.
* Skips LLM generation.
* Produces deterministic output.

---

## 🎯 Why Mock Mode is Critical

* Deterministic CI validation
* No dependency on Ollama in CI
* Faster test execution
* Retrieval-focused testing
* Production-safe pipelines

This separates:

**Retrieval Quality** from
**LLM Generation Variability**

---

# 🧪 Semantic Testing Strategy

Instead of testing exact responses, I implemented:

* Meaning-focused validation
* Required keyword checks
* Retrieval correctness testing

Example:

```python
assert "orchestration" in response
assert "container" in response
```

This ensures knowledge quality, not phrasing style.

---

# ⚙️ CI/CD Automation (GitHub Actions)

Workflow triggers when:

* k8s.txt changes
* app.py changes
* embed.py changes

Pipeline Steps:

1. Checkout code
2. Install dependencies
3. Rebuild embeddings
4. Start API in Mock Mode
5. Run semantic tests
6. Pass/Fail build

If keywords are missing:

❌ Build fails
✅ Deployment blocked

---

# 🔴 Demonstration of CI Catching Data Degradation

When I pushed the modified `k8s.txt` (missing "orchestration"):

* CI rebuilt embeddings
* Mock mode returned deterministic context
* Semantic test failed
* GitHub Actions blocked the build

This prevented degraded knowledge from reaching production.
# Note
 The Ci workflow completed successfully while the k8s.txt files contains all keywords. 

---

# 🚀 What This Project Demonstrates

* RAG system implementation
* Embedding lifecycle management
* LLM non-determinism handling
* Deterministic CI design
* Mock-based testing strategy
* Production-grade AI validation
* GitHub Actions automation
* Separation of concerns in AI systems

---

# 🧠 Engineering Insight

LLMs are probabilistic systems.

CI pipelines are deterministic systems.

Bridging them requires architectural separation between:

* Retrieval validation
* Generation behavior

Mock mode enables that separation.

This is how real companies maintain AI system quality at scale.

---

# 📈 Future Improvements

* Multi-document knowledge base


---

# 🎯 Final Takeaway

This project evolved from a simple RAG API into a fully automated, production-aware AI system with deterministic validation.

It reflects how modern AI engineering teams:

* Protect data quality
* Enforce CI trust
* Separate retrieval from generation
* Prevent silent knowledge degradation



