# LangChain Multi-Agent Research System

A production-style research assistant built with LangChain, Streamlit, and AI-powered tooling for web research, content extraction, report generation, and critical evaluation.

This project showcases a multi-agent workflow where a search agent gathers sources, a reader agent extracts relevant information from the best candidate pages, a writer chain compiles a structured research report, and a critic chain reviews the quality of the final output.

## Overview

The system is designed to automate the research process by combining:

- intelligent web search,
- content extraction from live web pages,
- structured narrative generation,
- quality review and feedback scoring.

It is a practical template for building research copilots, agentic AI tools, and AI-assisted knowledge workflows.

## Key Features

- Multi-agent design for research orchestration
- Tavily-powered web search for up-to-date information
- Deep content extraction using BeautifulSoup, readability, and trafilatura
- Structured report writing with prompt-based generation
- Automated critique and evaluation layer
- User-friendly Streamlit interface
- Easy-to-extend architecture for additional agents or tools

## Tech Stack

- Python 3.11+
- LangChain
- LangChain Core and Community integrations
- Tavily API
- Google Gemini / OpenAI-compatible LLM integration
- Streamlit
- BeautifulSoup, readability-lxml, trafilatura, requests
- python-dotenv

## Architecture

The project follows a simple but effective research pipeline:

1. Search Agent
   - Queries the web for recent and relevant information on a topic.

2. Reader Agent
   - Selects a promising source and extracts readable content from the page.

3. Writer Chain
   - Combines search results and scraped content into a structured report.

4. Critic Chain
   - Reviews the output, identifies strengths, highlights improvements, and scores the report.

5. Streamlit Frontend
   - Exposes the workflow in a clean interactive web app.

```text
User Input
   ↓
Search Agent
   ↓
Reader Agent
   ↓
Writer Chain
   ↓
Critic Chain
   ↓
Final Research Output
```

## Repository Structure

```bash
LangChain-Multi-Agent-Research-System/
├── app.py                # Streamlit web interface
├── main.py               # Terminal-based pipeline execution
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
├── LICENSE               # License file
├── src/
│   ├── agents/
│   │   └── agents.py     # Search, reader, writer, and critic logic
│   ├── pipelines/
│   │   └── pipeline.py   # Research workflow orchestration
│   ├── tools/
│   │   └── tools.py      # Web search and scraping tools
│   └── __init__.py
└── .env                  # Local environment variables (create manually)
```

## Prerequisites

Before running the project, ensure you have:

- Python 3.11 or later
- A Tavily API key
- A Gemini or OpenAI-compatible API key
- A terminal or IDE with access to the project directory

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/200ritik/LangChain-Multi-Agent-Research-System.git
cd LangChain-Multi-Agent-Research-System
```

### 2. Create a virtual environment

Using conda:

```bash
conda create -n langagent python=3.11 -y
conda activate langagent
```

Using venv:

```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the project root and add your API keys:

```env
TAVILY_API_KEY=your_tavily_api_key
GEMINI_API_KEY=your_gemini_api_key
```

If you use a different provider or model, update the configuration in the relevant source files accordingly.

## Running the Project

### Start the Streamlit app

```bash
streamlit run app.py
```

This launches the research interface where you can enter a topic and generate a report.

### Run the pipeline in terminal mode

```bash
python main.py
```

This executes the end-to-end research flow and prints the search results, extracted content, report, and critic feedback.

## Example Usage

Try searching for topics such as:

- "Latest trends in generative AI"
- "Climate technology investment outlook"
- "AI agent architecture best practices"

The workflow will search the web, extract useful information, write a report, and provide a quality review.

## Notes

- This project is intended as a learning and experimentation platform for agentic AI workflows.
- Scraping may be affected by website protections, rate limits, and anti-bot restrictions.
- For production deployment, consider caching, rate limiting, improved source ranking, and more robust error handling.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Acknowledgements

This project builds on the following tools and frameworks:

- LangChain
- Tavily
- Streamlit
- BeautifulSoup
- trafilatura
- readability-lxml
