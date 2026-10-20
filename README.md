# AI-Powered OpenAPI Compliance Tester Agent 🤖🚩

A highly dynamic, automated command-line tool built in Python that evaluates live REST API implementations against **OpenAPI/Swagger contract schemas**. It leverages advanced cloud LLM reasoning to intelligently generate contextual test payloads at runtime and documents structural mismatches inside a polished, responsive **HTML dashboard report**.

## 🌟 Core Features
- **Dynamic Schema Traversal:** Recursively loops through all endpoints, HTTP methods, and parameter structures inside any given local Swagger YAML file.
- **AI-Driven Edge Case Generation:** Uses the `openai/gpt-oss-120b` reasoning engine via Groq API to dynamically synthesize data configurations.
- **Zero Hardcoding Architecture:** Operates completely as a reusable CLI tool by accepting file paths and target base URLs via system arguments.
- **Automated Dashboard Compilation:** Programmatically records execution metrics and structural type violations inside time-stamped HTML logs.

## 🛠️ The Tech Stack
- **Core Engine:** Python 3.8+
- **Validation Layer:** `jsonschema`, `pyyaml`
- **Network Interface:** `requests`, `fastapi`, `uvicorn`
- **Inference Platform:** Groq Cloud SDK (`openai/gpt-oss-120b`)

---

## 🚀 Getting Started

### 1. Prerequisites & Installation
Ensure you have Python 3.8+ installed. Secure your local workspace environment by setting up an isolated virtual environment:

```bash
# Clone the repository
git clone https://github.com
cd api-contract-tester-agent

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install all required package dependencies
pip install groq requests jsonschema pyyaml fastapi uvicorn
```

### 2. Configure Environment Variables
Acquire a free API key from the [Groq Cloud Console](https://groq.com) and export it to your active terminal terminal session:

```bash
# Mac / Linux
export GROQ_API_KEY="your_actual_groq_api_key_here"

# Windows (Command Prompt)
set GROQ_API_KEY=your_actual_groq_api_key_here
```

---

## 💻 Running the Test Pipeline

To experience the automated contract error-catching in action, open two concurrent terminal windows.

### Step 1: Launch the Target API Server (Terminal 1)
Run the provided dummy FastAPI server which hosts intentional contract type mismatches:
```bash
source venv/bin/activate
python3 app.py
```
*Keep this terminal window running. The server will mount at `http://127.0.0.1:8000`.*

### Step 2: Trigger the Auditor Tool (Terminal 2)
Execute the dynamic script framework passing your local schema file path and target network base URL as parameters:
```bash
source venv/bin/activate
python3 api_auditor.py my_swagger.yaml http://127.0.0.1:8000
```

---

## 📊 Evaluation Reports
Upon execution, the terminal will print out a high-level console summary graph. Concurrently, a time-stamped visual asset named `compliance_report_YYYY-MM-DD_HH-MM-SS.html` is compiled right into your workspace.

Open this HTML file in any browser to review the diagnostic ledger mapping layout mismatches, undocumented code returns, or explicit format breaks.

## 🔒 Security & Sandbox Isolation
This tool is configured to operate in a safe developer sandbox layer. No actual application databases or user identities are mapped, making the dynamic test generation cycles entirely private and compliant with data boundaries.
