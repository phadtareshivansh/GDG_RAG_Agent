"""
Gemini API Wrapper for RAG Systems - WORKBOOK 🎓
=================================================
Fill in every blank marked  ___  to complete the code.
Run demo() at the bottom to test your work!

HOW TO USE THIS WORKBOOK
-------------------------
  • Find every  ___  blank and replace it with the correct value
  • Read the  # ✏️ FILL IN  comment above each blank — it tells you what to write
  • Read the  # 💡 HINT  comment for extra guidance
  • Run the file after each section to catch mistakes early!
===================================================

A clean, production-ready wrapper for Google's Gemini AI API.
Designed specifically for building Retrieval-Augmented Generation (RAG) systems.

Author: GDG Workshop Team
License: MIT
"""

import google.genai as genai
from typing import Optional, List, Dict
import os
"""Gemini API wrapper for simple demos and RAG systems.

This file provides a small, robust wrapper around the google.genai client.
It prefers an explicit api_key but will also read GEMINI_API_KEY from the
environment. If the google.genai SDK is not installed the wrapper will still
import but calls to the API will return a diagnostic message.

Usage:
  - Set GEMINI_API_KEY in your environment or pass api_key to GeminiWrapper
  - Optionally set a persona to influence responses
  - Use generate() for single-shot prompts and chat() for simple chat-style
    interactions that maintain a short transcript
"""

from typing import Optional, List, Dict
import os

try:
    import google.genai as genai
except Exception:
    genai = None

from dotenv import load_dotenv


# Load .env values if present
load_dotenv()


class GeminiWrapper:
    """Small wrapper around Google Gemini (google.genai).

    Behavior:
      - Requires GEMINI_API_KEY (or api_key param) to initialize
      - If google.genai is not installed, client will be None and generate()
        returns a diagnostic message (but still records history)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-2.5-flash",
        temperature: float = 0.7,
        verbose: bool = True,
    ):
        # prefer explicit api_key, fallback to GEMINI_API_KEY env var
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No Gemini API key provided.\n"
                "Either pass api_key parameter or set GEMINI_API_KEY environment variable.\n"
                "Get your key at: https://makersuite.google.com/app/apikey"
            )

        # initialize client if the SDK is available
        if genai is None:
            self.client = None
            if verbose:
                print("⚠️ google.genai SDK not found — client calls will fail until installed.")
        else:
            self.client = genai.Client(api_key=self.api_key)

        self.model_name = model_name
        self.temperature = temperature
        self.verbose = verbose

        self.history: List[Dict] = []
        self.persona: Optional[str] = None
        self._chat_transcript: List[Dict] = []

        if self.verbose:
            print(f"✅ Gemini initialized: {model_name} (temp={temperature})")

    def set_persona(self, persona_description: str) -> None:
        """Set a short persona description used as a SYSTEM prefix for prompts."""
        self.persona = persona_description
        if self.verbose:
            preview = persona_description[:80] + "..." if len(persona_description) > 80 else persona_description
            print(f"✅ Persona set: {preview}")

    def generate(self, prompt: str, temperature: Optional[float] = None, max_tokens: int = 2048) -> str:
        """Generate text for a single prompt.

        If a persona is set it is prefixed as SYSTEM content. Returns the
        text response or an error/diagnostic message.
        """
        full_prompt = f"SYSTEM: {self.persona}\n\nUSER: {prompt}" if self.persona else prompt
        temp = temperature if temperature is not None else self.temperature

        if self.client is None:
            msg = "google.genai client not configured; cannot call API."
            if self.verbose:
                print("⚠️", msg)
            # still append to history for debugging
            self.history.append({"prompt": full_prompt, "response": msg, "temperature": temp, "model": self.model_name})
            return msg

        try:
            resp = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config={
                    "temperature": temp,
                    "max_output_tokens": max_tokens,
                    "top_p": 0.95,
                    "top_k": 40,
                },
            )

            # Extract text from possible response shapes
            text = ""
            if hasattr(resp, "text") and isinstance(resp.text, str):
                text = resp.text
            elif hasattr(resp, "candidates") and resp.candidates:
                for cand in resp.candidates:
                    if getattr(cand, "content", None):
                        parts = getattr(cand.content, "parts", [])
                        for p in parts:
                            if getattr(p, "text", None):
                                text += p.text
                text = text.strip()

            self.history.append({"prompt": full_prompt, "response": text, "temperature": temp, "model": self.model_name})
            return text or ""
        except Exception as e:
            error_msg = f"Error calling Gemini API: {e}"
            if self.verbose:
                print(f"❌ {error_msg}")
            return error_msg

    def chat(self, message: str) -> str:
        """Simple chat that maintains a short in-memory transcript.

        This builds a prompt from the persona (if any) and the last few turns
        and sends it through generate(). It's intentionally minimal.
        """
        self._chat_transcript.append({"role": "user", "text": message})

        convo = []
        if self.persona:
            convo.append(f"SYSTEM: {self.persona}")
        for turn in self._chat_transcript[-10:]:
            prefix = "USER" if turn["role"] == "user" else "ASSISTANT"
            convo.append(f"{prefix}: {turn['text']}")
        convo.append("ASSISTANT:")
        prompt = "\n\n".join(convo)

        reply = self.generate(prompt)
        self._chat_transcript.append({"role": "assistant", "text": reply})
        return reply

    def clear_history(self) -> None:
        self.history = []
        self._chat_transcript = []
        if self.verbose:
            print("✅ History cleared")

    def get_history(self) -> List[Dict]:
        return self.history

    def get_stats(self) -> Dict:
        return {
            "model": self.model_name,
            "temperature": self.temperature,
            "total_interactions": len(self.history),
            "has_persona": self.persona is not None,
        }


def demo() -> None:
    print("\n" + "=" * 70)
    print("GEMINI WRAPPER DEMO")
    print("=" * 70 + "\n")

    try:
        # Try to create a wrapper; if no API key is present this will raise
        llm = GeminiWrapper(temperature=0.7, verbose=True)

        print("1. Basic Generation")
        print("-" * 70)
        print(llm.generate("What is Python in one sentence?"))

        print("2. Persona + Chat")
        llm.set_persona("You are a helpful teacher who explains concepts using simple analogies.")
        print(llm.generate("What is machine learning?"))
        print(llm.chat("My favorite color is blue"))
        print(llm.chat("What's my favorite color?"))
    except ValueError as e:
        print(f"\n❌ Error: {e}\n")
        print("Setup Instructions:")
        print("1. Get API key: https://makersuite.google.com/app/apikey")
        print("2. Create .env file with: GEMINI_API_KEY=your_key_here")
        print("3. Run again\n")


if __name__ == "__main__":
    demo()