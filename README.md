# Multi-Agent Research System 

This project implements an execution-driven, agentic research system using LangGraph. The user inputs a topic/area he wishes to research and the system fetches information and displays potential research areas along with reference sources.  

The focus is on **control flow, state management, tool isolation, and memory separation**, rather than prompt chaining. The system is intentionally designed as a stateless execution graph with explicit state transitions and defined failure boundaries.

Install requirements using requirements.txt
---

## Architecture Overview
```
research_agent/
│
├── tools/        <- Agentic tools
│   ├── fetch_web.py
│   └── call_llm.py
│
├── memory/        <- Persistent Memory
│   ├── vector_memory.py
│   └── graph_memory.py
│   └── chunker.py
│
├── agents/        <- Agents 
│   ├── researcher.py
│   ├── memory_agent.py
│   ├── analyst.py
│   └── summarizer.py
│   └── memory_agent.py
│   └── context_builder.py
│
├── orchestration/
│   └── graph.py   <- LangGraph DAG
│   └── state.py
│
└── main.py        <- Entry Point
```
<img width="489" height="447" alt="image" src="https://github.com/user-attachments/assets/8706cd06-b394-4843-baf6-d186be9dace8" />

## Design Principles

- **Execution-first orchestration**
- **Explicit state passed between nodes**
- **Tool failures surfaced into state**
- **Supervisor-controlled decision flow**
- **Memory separated from execution**
- **LLMs treated as interchangeable components**

## State Model

All agents operate on a shared `ResearchState`:

```python
class ResearchState(TypedDict):
    query: str
    fetched_docs: list
    vector_results: list
    graph_results: List
    final_context: str
    next_step: str
    analysis_decision: str
    sources: Dict   
```
## Tools

### Web Fetching Tool
- Using DDGS tool to fetch URLs using DuckDuckGo's utility
- Parsing each URL using Beautiful Soup

### LLM
- Calling Gemimi using Gemini's API

## Memory Subsystems

### Vector Memory
- Used FAISS for storing into vector DB
- Used for semantic retrieval
- Info fetched from the internet is stored in vector memory
  
### Graph Memory
- Persistent entity co-occurrence graph
- Optimized for auditability and traceability
- Used networkx for creating the graph and using Spacy to create tokens
Note: Install Spacy's "en_core_web_trf" transformer using the steps below: 
```python
pip install spacy
python -m spacy download en_core_web_trf
```
## Failure Handling
- Tool calls are isolated per agent
- Failures do not crash the graph
- Supervisor node decides whether to continue or abort
- System supports deterministic re-runs
- LLM does not hallucinate random stuff when the memory retrieved is garbage, as it is grounded by some context and user query.

## Running the system
```python
python main.py
```

## Sample Output
```python
=== Multi-Agent Research System ===

Enter your Research Area> Financial Technology
[supervisor] Bootstrapping → research

Sources fetched:
- https://techtesy.com/an-effective-guide-about-finance-related-research-topics/
- https://aikotradingstore.com/top-notch-features-of-the-best-financial-research-services/
- https://armgpublishing.com/journals/fmir/volume-7-issue-4/article-6/
- https://www.calltutors.com/blog/research-topics-in-finance/
- https://www.port.ac.uk/research/research-areas/finance
- https://jfin-swufe.springeropen.com/articles/10.1186/s40854-021-00285-7
- https://guides.loc.gov/fintech/21st-century
- https://jfin-swufe.springeropen.com/articles/10.1186/s40854-023-00524-z
- https://www.imperial.ac.uk/business-school/faculty-research/research-centres/centre-financial-technology/
- https://ftrc.co/
[research] Skipped non-text or binary document
[research] Skipped non-text or binary document
[research] Skipped non-text or binary document
[research] Skipped non-text or binary document
[research] Skipped non-text or binary document
[research] Skipped non-text or binary document
[research] Skipped non-text or binary document
[research] Skipped non-text or binary document
[research] Skipped non-text or binary document
[research] Skipped non-text or binary document
[memory] Storing fetched documents into memory...
[memory] Storing into vector and graph memory...
[supervisor] Analysis ready → summarize

FINAL ANSWER:

Based on the provided context, here are potential research areas in Financial Technology (FinTech), categorized by theme:

**1. Artificial Intelligence and Fraud Detection**
*   **Generative Adversarial Networks (GANs) in Fraud Prevention:** Researching the use of GANs and graph-based GAN solutions to identify financial fraud risk and mitigate class imbalance in banking transactions.
*   **Machine Learning Applications:** Investigating the general application of machine learning and AI within financial services to improve efficiency and security.

**2. Cryptocurrencies, Blockchain, and Digital Assets**
*   **Cross-Chain Stablecoins:** Designing and analyzing stablecoin services specifically tailored for cross-chain transactions.
*   **Central Bank Digital Currencies (CBDCs):** Analyzing the development, proliferation, and economic impact of CBDCs, e-money, and public vs. private digital money assets.
*   **Smart Contracts:** Evaluating the implementation and regulatory implications of smart contracts in financial agreements.

**3. Consumer Behavior and Adoption**
*   **P2P Lending Adoption:** Using models like the DeLone and McLean approach to understand investors' intentions to use Peer-to-Peer (P2P) lending platforms.
*   **User Engagement Drivers:** Unveiling the drivers of FinTech adoption and continuance (user engagement), particularly in specific regions (e.g., Italy, as mentioned in the text).  
*   **Robo-Advice:** Analyzing consumer trust and reliance on automated robo-advice compared to traditional financial counseling.

**4. Financial Inclusion and Social Impact**
*   **Serving the Unbanked:** Researching how emerging alternative financial models can impact the unbanked and populations in the developing world by making services more accessible and affordable.
*   **Green Innovation in SMEs:** Exploring how digital financial literacy and green knowledge capabilities can catalyze ambidextrous green innovation in Small and Medium Enterprises (SMEs).
*   **Financial Literacy:** Measuring the impact of digital technology on financial competence and literacy networks.

**5. Regulation, Risk, and Banking Performance**
*   **Impact on Traditional Banks:** Assessing the impact of financial technology on the performance of traditional financial banks (e.g., specific case studies like the Indonesia Stock Exchange).
*   **Regulatory Frameworks:** Developing regulatory and supervisory frameworks that balance the promotion of innovation with the containment of FinTech risks (security, trust, and systemic risk).
*   **Nonbank Financial Players:** Analyzing the rise of nonbank players since the 2008 financial crisis and their competition with traditional institutions.

**6. Corporate Management and Strategy**
*   **Overcoming Managerial Myopia:** Investigating how digital technology innovation impacts or helps overcome managerial myopia in enterprises.
*   **Business Reimagining:** Rethinking how businesses are designed, motivated, and organized in the "Tech Era."

**7. Interdisciplinary FinTech Applications**
*   **Expansion into New Fields:** Exploring the novel incorporation of FinTech issues into non-financial fields such as Dentistry, Nursing, and Veterinary practices.
```
