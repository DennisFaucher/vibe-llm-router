# LLM Router (Created with Claude. Thanks Claude)

An intelligent router for Ollama models that automatically directs prompts to the appropriate model based on task type.

## Features

- **Automatic Task Classification**: Analyzes input prompts to determine task type
- **Smart Routing**: 
  - Routes summarization tasks to `gpot-oss`
  - Routes coding tasks to `qwen2.5-coder`
- **Streaming Support**: Real-time response streaming
- **CLI Interface**: Easy-to-use command-line tool

## Prerequisites

1. **Ollama** must be installed and running
2. Pull the required models:
```bash
   ollama pull gpot-oss
   ollama pull qwen2.5-coder
```

## Installation

Using `uv`:
```bash
uv sync
```

Or with pip:
```bash
pip install -e .
```

## Usage

### Command Line

Basic usage:
```bash
llm-router "Write a Python function to calculate factorial"
```

Summarization task:
```bash
llm-router "Summarize the following text: [your long text here]"
```

Read from file:
```bash
llm-router --file input.txt
```

Custom Ollama host:
```bash
llm-router --host http://localhost:11434 "Your prompt here"
```

Disable streaming:
```bash
llm-router --no-stream "Your prompt here"
```

### Python API
```python
from llm_router import LLMRouter

router = LLMRouter(host="http://localhost:11434")

# Stream response
for chunk in router.route("Write a quicksort function in Python"):
    print(chunk['message']['content'], end='', flush=True)

# Or get complete response
response = router.route("Summarize this article...", stream=False)
print(response['message']['content'])
```

## Task Classification

The router uses keyword matching to classify tasks:

**Summarization Keywords**: summarize, summary, tldr, brief, overview, recap, digest, abstract, synopsis, condense, shorten, key points, main points

**Coding Keywords**: code, program, function, script, implement, write, create, develop, build, algorithm, python, javascript, java, cpp, rust, go, class, method, api, debug, fix, refactor

## Project Structure
```
llm-router/
├── llm_router/
│   ├── __init__.py
│   └── main.py
├── pyproject.toml
└── README.md
```

## Configuration

The router defaults to:
- Ollama host: `http://localhost:11434`
- Summarization model: `gpot-oss`
- Coding model: `qwen2.5-coder`

You can modify these in the `LLMRouter` class if needed.

## Development

Run tests (when added):
```bash
uv run pytest
```

## License

MIT
```

## Directory Structure

Create the files like this:
```
llm-router/
├── pyproject.toml
├── README.md
└── llm_router/
    ├── __init__.py
    └── main.py
