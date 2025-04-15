from typing import List, Sequence
from google import generativeai as genai
class GeminiEmbeddingFunction:
    def __call__(self, input: Sequence[str]) -> List[List[float]]:
        # Defaulting to retrieval_document task type for indexing
        return [self.embed_text(text, task_type="retrieval_document") for text in input]

    def embed_text(self, text: str, task_type="retrieval_document") -> list[float]:
        response = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type=task_type
        )
        return response["embedding"]