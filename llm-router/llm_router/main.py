"""Main LLM router module."""
import click
import ollama
from typing import Literal


class LLMRouter:
    """Routes requests to appropriate Ollama models based on task type."""

    # Keywords for task classification
    SUMMARIZE_KEYWORDS = [
        'summarize', 'summary', 'summarise', 'tldr', 'brief',
        'overview', 'recap', 'digest', 'abstract', 'synopsis',
        'condense', 'shorten', 'key points', 'main points'
    ]

    CODE_KEYWORDS = [
        'code', 'program', 'function', 'script', 'implement',
        'write', 'create', 'develop', 'build', 'algorithm',
        'python', 'javascript', 'java', 'cpp', 'rust', 'go',
        'class', 'method', 'api', 'debug', 'fix', 'refactor'
    ]

    def __init__(self, host: str = "http://localhost:11434"):
        """Initialize router with Ollama host."""
        self.client = ollama.Client(host=host)
        self.gpt_model = "gpt-oss"
        self.coder_model = "qwen2.5-coder"

    def classify_task(self, prompt: str) -> Literal["summarize", "code", "general"]:
        """
        Classify the task based on the input prompt.

        Args:
            prompt: The user's input string

        Returns:
            Task type: 'summarize', 'code', or 'general'
        """
        prompt_lower = prompt.lower()

        # Get first 500 characters (the instruction part) for better classification
        # This prevents content in long texts from affecting classification
        instruction_part = prompt_lower[:500]

        # Check for summarization keywords in the instruction
        summarize_score = sum(1 for kw in self.SUMMARIZE_KEYWORDS if kw in instruction_part)

        # Check for coding keywords in the instruction
        code_score = sum(1 for kw in self.CODE_KEYWORDS if kw in instruction_part)

        # Decide based on scores
        if summarize_score > code_score and summarize_score > 0:
            return "summarize"
        elif code_score > summarize_score and code_score > 0:
            return "code"
        else:
            # Default to code model if unclear (you can change this)
            return "general"

    def route(self, prompt: str, stream: bool = True):
        """
        Route the prompt to the appropriate model.

        Args:
            prompt: The user's input string
            stream: Whether to stream the response

        Returns:
            Generator of response chunks if streaming, else complete response
        """
        task_type = self.classify_task(prompt)

        # Select model based on task
        if task_type == "summarize":
            model = self.gpt_model
            print(f"🔀 Routing to {model} (summarization task)")
        elif task_type == "code":
            model = self.coder_model
            print(f"🔀 Routing to {model} (coding task)")
        else:
            # Default to coder model for general tasks
            model = self.coder_model
            print(f"🔀 Routing to {model} (general task)")

        # Make the request
        response = self.client.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
            stream=stream
        )

        return response


@click.command()
@click.argument('prompt', required=False)
@click.option('--file', '-f', type=click.File('r'), help='Read prompt from file')
@click.option('--host', default='http://localhost:11434', help='Ollama host URL')
@click.option('--no-stream', is_flag=True, help='Disable streaming output')
def cli(prompt, file, host, no_stream):
    """
    LLM Router - Route prompts to appropriate Ollama models.

    Usage:
        llm-router "Write a Python function to sort a list"
        llm-router "Summarize this text: ..."
        llm-router --file input.txt
    """
    # Get prompt from file or argument
    if file:
        prompt = file.read()
    elif not prompt:
        click.echo("Error: Please provide a prompt or use --file", err=True)
        raise click.Abort()

    # Initialize router
    router = LLMRouter(host=host)

    # Route and display response
    try:
        response = router.route(prompt, stream=not no_stream)

        if no_stream:
            # Non-streaming response
            print(f"\n{response['message']['content']}")
        else:
            # Streaming response
            print()
            for chunk in response:
                content = chunk['message']['content']
                print(content, end='', flush=True)
            print()  # New line at end

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    cli()
