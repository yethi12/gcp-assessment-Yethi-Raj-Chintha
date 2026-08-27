# NorthStar Retail — GCP Assessment

## 1. Overview

This project implements a retail data and document question-answering assistant for NorthStar Retail.

The application supports two primary types of questions:

1. **Sales analytics questions**
   - Answered using SQL queries over cleaned sales data.
   - The current implementation uses DuckDB for local/offline execution.

2. **Policy/document questions**
   - Answered using Retrieval-Augmented Generation (RAG).
   - Assessment documents are loaded, chunked, embedded using Gemini embeddings, semantically retrieved, and passed to Gemini for grounded answer generation.

A routing layer determines whether a question should be handled by the sales analytics pipeline or the document/RAG pipeline.

---

## 2. Current Architecture

```text
                         User Question
                              |
                              v
                           Router
                         /        \
                        /          \
                       v            v
                    SALES        POLICY
                      |             |
                      v             v
                  DuckDB       Semantic Search
                      |             |
                      |             v
                      |        Document Chunks
                      |             |
                      |             v
                      |           Gemini
                      |             |
                      v             v
                    Answer        Answer
Sales FlowPlaintextsales.csv
    |
    v
Data Cleaning
    |
    v
clean_sales.csv
    |
    v
DuckDB
    |
    v
SQL Analytics
    |
    v
Sales Answer
Document/RAG FlowPlaintextAssessment Documents
        |
        v
Document Loader
        |
        v
Chunking
        |
        v
Gemini Embeddings
        |
        v
Semantic Similarity Search
        |
        v
Relevant Document Chunks
        |
        v
Gemini
        |
        v
Grounded Answer + Source
3. Project StructurePlaintextgcp-assessment-Yethi-Raj-Chintha/
│
├── data/
│   ├── sales.csv
│   └── product_docs/
│       ├── loyalty.json
│       ├── promotions.pdf
│       ├── returns.pdf
│       ├── shipping.json
│       ├── sizing.txt
│       ├── stationery-faq.csv
│       ├── support.pdf
│       └── warranty.pdf
│
├── src/
│   ├── __init__.py
│   ├── inspect_data.py
│   ├── check_quality.py
│   ├── clean_sales.py
│   ├── database.py
│   ├── test_database.py
│   ├── sales_queries.py
│   ├── list_documents.py
│   ├── document_loader.py
│   ├── chunker.py
│   ├── retrieval.py
│   ├── test_embeddings.py
│   ├── build_index.py
│   ├── semantic_search.py
│   ├── answer_generator.py
│   ├── router.py
│   └── main.py
│
├── tests/
│   ├── test_cleaning.py
│   ├── test_retrieval.py
│   ├── test_router.py
│   └── test_sales_queries.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
4. Data ProcessingThe supplied sales dataset contains 5,132 rows and 9 columns.The sales data contains fields including:order_idorder_datestore_idproduct_idproduct_namecategoryquantityunit_priceregionThe initial data inspection identified:Missing product namesMissing quantitiesMissing unit pricesDuplicate order IDsNegative quantities requiring validationThe cleaning pipeline removes exact duplicates and invalid/incomplete records according to the implemented cleaning logic.Cleaning ResultsOriginal rows: 5,132After removing exact duplicates: 5,124Final rows: 5,084The cleaned data is written to data/clean_sales.csv (excluded from Git).5. Sales AnalyticsThe cleaned data is loaded into DuckDB at data/northstar.duckdb.The database contains the sales table, validated at 5,084 rows.The sales analytics layer currently supports:Top 5 Products by Total RevenueProductRevenue ($)Running Shoes10,196.60Bluetooth Speaker9,046.38Denim Jacket7,652.81Rain Jacket6,893.37Wireless Earbuds6,083.21Revenue by RegionRegionRevenue ($)East26,365.67South23,860.66North21,772.03West19,697.54Central17,703.47Category Revenue (7 Days Before Latest Order Date)CategoryRevenue ($)Electronics1,329.996. Document ProcessingThe project processes eight supplied documents:loyalty.jsonpromotions.pdfreturns.pdfshipping.jsonsizing.txtstationery-faq.csvsupport.pdfwarranty.pdfThe document loader successfully loads all eight documents.Pipeline OutputDocuments processed: 8Total chunks: 1937. Semantic RetrievalModel: gemini-embedding-001Embedding Dimension: 3072Generated Local Index: data/document_index.json (excluded from Git)Semantic search uses cosine similarity to identify the most relevant document chunks.Example: Querying "What are the shipping delivery times?" retrieves shipping.json as the highest-ranked source.8. RAG Answer GenerationThe application uses retrieved document chunks as grounded context for Gemini with strict guardrails:Use only the supplied document context.Avoid outside knowledge.Explicitly state when the supplied documents do not contain enough information.Identify the source document.Example Q&AQuestion: What are the shipping delivery times?Expected Answer:Standard Delivery (Same Region): 3 to 5 business daysStandard Delivery (Cross Region): 7 to 10 business daysExpress Delivery: 1 to 2 business daysSource: shipping.jsonUnanswerable Query Handling:Question: What is the employee vacation policy?Response: States clearly that the requested information is not available in the supplied documents.9. Question RouterThe router determines whether a query belongs to SALES or POLICY. It applies deterministic classification logic first, falling back to Gemini for ambiguous cases.QuestionRouteWhat is the revenue by region?SALESWhich products generated the most revenue?SALESWhich area performed best?SALESWhat are the shipping delivery times?POLICYWhat is the return policy?POLICYCan I get my money back for an item?POLICYHow quickly will my package arrive?POLICY10. End-to-End ApplicationThe main entry point is src/main.py.Bashpython -u "src/main.py"
Interactive CLI OutputPlaintext============================================================
NorthStar Retail Assistant
============================================================

Ask a sales or policy question.
Type 'exit' to quit.

Question: Which products generated the most revenue?

Route selected: SALES

=== ANSWER ===
Top 5 products by total revenue:

- Running Shoes (SKU-AP-002): 10196.60
- Bluetooth Speaker (SKU-EL-003): 9046.38
- Denim Jacket (SKU-AP-003): 7652.81
- Rain Jacket (SKU-AP-005): 6893.37
- Wireless Earbuds (SKU-EL-001): 6083.21
11. ConfigurationCreate a local .env file based on .env.example:Code snippetGOOGLE_API_KEY=your-api-key
GEMINI_MODEL=gemini-3.6-flash
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
USE_GEMINI=true
USE_GCP=false
Security Note: Never commit .env, API keys, passwords, access tokens, or service account credentials.12. Offline / Mock ModeRun without Gemini generation calls for offline testing or retrieval debugging:Bash# Windows Command Prompt
set USE_GEMINI=false

# Bash / Linux / macOS
export USE_GEMINI=false

python -u "src/main.py"
In mock mode:Sales questions continue to run over local DuckDB.Policy questions perform local semantic retrieval and return raw context.Gemini LLM generation is disabled.To re-enable:Bashset USE_GEMINI=true
13. Installation & SetupBash# 1. Create a virtual environment
python -m venv .venv

# 2. Activate the virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
14. Build the Local Data PipelineBash# Step 1: Inspect raw sales data
python -u "src/inspect_data.py"

# Step 2: Clean sales data (writes data/clean_sales.csv)
python -u "src/clean_sales.py"

# Step 3: Create DuckDB database (writes data/northstar.duckdb)
python -u "src/database.py"

# Step 4: Validate database (Expected: 5084 rows)
python -u "src/test_database.py"
15. Build the Document PipelineBash# Step 1: Verify documents
python -u "src/list_documents.py"

# Step 2: Load document content
python -u "src/document_loader.py"

# Step 3: Generate text chunks (Expected: 193 chunks)
python -u "src/chunker.py"

# Step 4: Test embedding connection (Requires GOOGLE_API_KEY)
python -u "src/test_embeddings.py"

# Step 5: Build local vector index (writes data/document_index.json)
python -u "src/build_index.py"
16. Verification & TestingPipeline-Specific TestsBash# Test Semantic Retrieval
python -u "src/semantic_search.py"

# Test RAG Generation
python -u "src/answer_generator.py"

# Test Question Router
python -u "src/router.py"
Automated Pytest SuiteBashpytest -v
Current Status: 15 passedTest coverage covers data cleaning, invalid quantity checks, revenue calculation, DuckDB tables, sales query aggregations, semantic retrieval ranking, and deterministic/fallback router handling.17. Security & Generated FilesExcluded from Git (.gitignore).env.venv/.pytest_cache/__pycache__/data/clean_sales.csvdata/northstar.duckdbdata/document_index.jsonRepository Assetsdata/sales.csvdata/product_docs/*18. Current LimitationsStorage & Engine: Sales analytics currently use local DuckDB rather than GCP BigQuery.Index: Vector embeddings are stored in a flat local JSON file.Infrastructure: Google Cloud Platform services (Cloud Run, Cloud Storage, BigQuery, IAM) are pending integration.Chunking Strategy: Fixed-size chunking can be improved with document structure/section-aware strategies.19. Planned GCP IntegrationPlaintext                         User
                          |
                          v
                       Router
                      /      \
                     /        \
                 SALES        POLICY
                   |             |
                   v             v
               BigQuery       RAG Pipeline
                   |             |
                   |             v
                   |           Gemini
                   |             |
                   v             v
                 Answer        Answer
Target GCP Components: BigQuery, Cloud Storage, IAM, Infrastructure as Code (Terraform).Fallback Strategy: DuckDB will remain as an offline local fallback mechanism.20. Development StatusComponentStatusData inspection[x]Data cleaning[x]DuckDB database[x]SQL analytics[x]Document loading[x]Document chunking[x]Gemini embeddings[x]Semantic retrieval[x]Gemini RAG generation[x]Question routing[x]Offline / mock mode[x]Automated tests (15/15)[x]GCP & BigQuery integration[ ]GCP IaC configuration[ ]Cloud deployment[ ]21. Git Workflow & Final SubmissionBranching StrategyActive branch: initial-implementationDirect commits to main are restricted.Development flow: Feature Branch $\rightarrow$ Implementation $\rightarrow$ Commit $\rightarrow$ Pull Request $\rightarrow$ Review $\rightarrow$ Merge to main.Submission Metadata TemplatePlaintextCandidate Name:
Candidate Email ID:
Assigned Slot:
Repository URL:
Final Pull Request URL:
Final Commit ID:
Primary Technology Used: Python, DuckDB, Gemini Embeddings, Gemini Flash, Pytest
Solution Summary:
Setup Considerations:
Known Limitations:
Reviewer Access Granted: Yes/No
22. Step-by-Step Reproducibility GuideBash# Setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Data Pipeline
python -u "src/inspect_data.py"
python -u "src/clean_sales.py"
python -u "src/database.py"

# Document Pipeline
python -u "src/list_documents.py"
python -u "src/document_loader.py"
python -u "src/chunker.py"
python -u "src/build_index.py"

# Validation & Execution
pytest -v
python -u "src/main.py"
```
