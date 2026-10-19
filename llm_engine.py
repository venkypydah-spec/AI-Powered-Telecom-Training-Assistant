"""
IBM Granite LLM Integration via watsonx.ai REST API
Works on any Python version — uses requests directly.
"""

import logging
import requests

from config import (
    WATSONX_API_KEY,
    WATSONX_PROJECT_ID,
    WATSONX_URL,
    GRANITE_MODEL_ID,
    GENERATE_PARAMS,
    QUIZ_PARAMS,
)

logger = logging.getLogger(__name__)

# IAM token endpoint
IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"


class GraniteLLM:
    """Wrapper for IBM Granite model via watsonx.ai REST API."""

    def __init__(self):
        self._token: str = ""
        self._token_expiry: float = 0.0

    # ── Authentication ──────────────────────────────────────────────────────────

    def _get_iam_token(self) -> str:
        """Fetch or return cached IBM IAM bearer token."""
        import time
        if self._token and time.time() < self._token_expiry - 60:
            return self._token

        resp = requests.post(
            IAM_TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": WATSONX_API_KEY,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        self._token = data["access_token"]
        import time as _t
        self._token_expiry = _t.time() + data.get("expires_in", 3600)
        logger.info("IBM IAM token acquired successfully.")
        return self._token

    # ── Core generation ─────────────────────────────────────────────────────────

    def _generate(self, prompt: str, params: dict) -> str:
        """Call watsonx.ai text generation endpoint."""
        token = self._get_iam_token()
        url = f"{WATSONX_URL}/ml/v1/text/generation?version=2023-05-29"

        payload = {
            "model_id": GRANITE_MODEL_ID,
            "input": prompt,
            "parameters": {
                "max_new_tokens": params.get("max_new_tokens", 1024),
                "min_new_tokens": params.get("min_new_tokens", 10),
                "temperature": params.get("temperature", 0.7),
                "top_p": params.get("top_p", 0.9),
                "repetition_penalty": params.get("repetition_penalty", 1.1),
                "decoding_method": "greedy" if params.get("temperature", 0.7) == 0 else "sample",
                "stop_sequences": [],
            },
            "project_id": WATSONX_PROJECT_ID,
        }

        resp = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json=payload,
            timeout=120,
        )

        if resp.status_code != 200:
            logger.error(f"watsonx.ai API error {resp.status_code}: {resp.text[:500]}")
            resp.raise_for_status()

        result = resp.json()
        generated = result["results"][0]["generated_text"]
        return generated.strip()

    # ── Public methods ──────────────────────────────────────────────────────────

    def explain_concept(self, topic: str, context: str) -> str:
        """Generate a simplified explanation of a telecom concept using RAG context."""
        prompt = f"""You are an expert telecom training instructor. Use the provided reference material to give a clear, structured, and student-friendly explanation of the topic.

Reference Material:
{context}

Topic to Explain: {topic}

Instructions:
- Provide a clear and structured explanation suitable for telecom students.
- Use bullet points, numbered lists, or sections where appropriate.
- Define any technical acronyms on first use.
- Give a practical real-world example if possible.
- Keep the explanation comprehensive yet easy to understand.

Explanation:"""

        return self._generate(prompt, GENERATE_PARAMS)

    def answer_question(self, question: str, context: str, chat_history: list) -> str:
        """Answer a user's question with RAG context and conversation history."""
        history_str = ""
        if chat_history:
            recent = chat_history[-6:]
            for role, msg in recent:
                prefix = "Student" if role == "user" else "Assistant"
                history_str += f"{prefix}: {msg}\n"

        prompt = f"""You are a friendly and knowledgeable Telecom Training Assistant powered by IBM Granite. Answer the student's question using the provided reference material. Be accurate, clear, and educational.

Reference Material:
{context}

{"Previous Conversation:" + chr(10) + history_str if history_str else ""}
Student's Question: {question}

Instructions:
- Answer directly and accurately using the reference material.
- If the question is beyond the provided context, use your general telecom knowledge but note it.
- Keep your answer concise but complete (3-6 sentences or bullet points).
- Be encouraging and supportive as a good teacher would be.

Answer:"""

        return self._generate(prompt, GENERATE_PARAMS)

    def generate_quiz(self, topic: str, context: str, num_questions: int = 5) -> str:
        """Generate a multiple-choice quiz on a given telecom topic."""
        prompt = f"""You are a telecom training expert creating a quiz. Generate exactly {num_questions} multiple-choice questions based on the topic and reference material below.

Reference Material:
{context}

Topic: {topic}

Format each question EXACTLY as shown below:
Q1. [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Answer: [Correct letter]
Explanation: [Brief explanation of why this is correct]

Rules:
- Each question must have exactly 4 options (A, B, C, D).
- Only one answer is correct.
- Questions should test genuine understanding, not just memorization.
- Cover different aspects of the topic.
- Vary difficulty from easy to medium to hard.

Quiz:"""

        return self._generate(prompt, QUIZ_PARAMS)

    def generate_summary(self, topic: str, context: str) -> str:
        """Generate a concise summary/study note for a topic."""
        prompt = f"""You are a telecom expert. Create a concise study summary for the following topic.

Reference Material:
{context}

Topic: {topic}

Create a study summary that includes:
1. One-sentence definition
2. Key components or concepts (5-7 bullet points)
3. Key standards or protocols mentioned
4. One practical use case

Summary:"""

        return self._generate(prompt, GENERATE_PARAMS)

    def suggest_learning_path(self, current_topic: str, context: str) -> str:
        """Suggest what to learn next based on the current topic."""
        prompt = f"""You are a telecom training advisor. Based on the current topic the student is learning, suggest a structured learning path.

Current Topic: {current_topic}

Reference Material:
{context}

Provide:
1. A brief assessment of prerequisites needed for this topic.
2. What related topics to explore next (3-4 topics).
3. Recommended practice areas.
Keep the response concise and actionable.

Learning Path:"""

        return self._generate(prompt, GENERATE_PARAMS)


# Global singleton
granite_llm = GraniteLLM()
