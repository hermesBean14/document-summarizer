# document-summarizer

A command-line tool that reads a `.txt` or `.pdf` document, summarizes it using an LLM (Anthropic API), and returns a structured summary with a title, key points, and a conclusion.

## Requirements

- Python 3
- An Anthropic API key

## Installation

```bash
git clone <repo-url>
cd document-summarizer
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with your API key:

```
ANTHROPIC_API_KEY=your_key_here
```

The `.env` file is gitignored and is never committed.

## Usage

```bash
python main.py <path-to-file>
```

Example:

```bash
python main.py document.pdf
```

Supported formats: `.txt` and `.pdf`.
