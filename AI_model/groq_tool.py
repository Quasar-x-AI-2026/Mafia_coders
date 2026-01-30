# groq_tool.py
from livekit.agents import function_tool, RunContext
from groq import Groq

# Initialize Groq client once
client = Groq()

@function_tool()
async def ask_groq(context: RunContext, prompt: str, temperature: float = 1.0) -> str:
    """
    Ask Groq a question and return the completion as a string.
    """
    try:
        # Create streaming completion
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_completion_tokens=8192,
            top_p=1,
            reasoning_effort="medium",
            stream=True,
            stop=None
        )

        # Aggregate chunks into a single string
        output = ""
        for chunk in completion:
            output += chunk.choices[0].delta.content or ""

        return output

    except Exception as e:
        return f"Groq tool error: {str(e)}"
