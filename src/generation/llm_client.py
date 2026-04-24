import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        # Ensure client does not crash on init if key is missing (for local testing without key)
        if self.api_key and self.api_key != "your_groq_api_key_here":
            # Groq API is compatible with the OpenAI Python client
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.groq.com/openai/v1"
            )
        else:
            self.client = None

    def generate(self, prompt: str, model: str = "llama-3.1-8b-instant", max_tokens: int = 500) -> str:
        """Standard synchronous generation."""
        if not self.client:
            return "Error: GROQ_API_KEY not found or invalid."
            
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during generation: {str(e)}"

    def generate_stream(self, prompt: str, model: str = "llama-3.1-8b-instant", max_tokens: int = 500):
        """Generator for streaming responses."""
        if not self.client:
            yield "Error: GROQ_API_KEY not found or invalid."
            return
            
        try:
            stream = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.1,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Error during streaming: {str(e)}"

    def generate_pure_llm(self, query: str, model: str = "llama-3.1-8b-instant") -> str:
        """Pure LLM mode without retrieval (for evaluation comparison)."""
        prompt = f"Answer the following question to the best of your knowledge:\n\nQuestion: {query}\nAnswer:"
        return self.generate(prompt, model=model)
