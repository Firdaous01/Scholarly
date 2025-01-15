import datetime
from typing import List, Dict

def format_context(results: List[Dict]) -> str:
    """Format retrieved documents into context."""
    context_parts = []
    for idx, result in enumerate(results, 1):
        context_parts.append(
            f"[Article {idx}]\n"
            f"Title: {result['title']}\n"
            f"Abstract: {result['abstract']}\n"
            f"Authors: {', '.join(result['authors'])}\n"
            f"Year: {result['year']}\n"
            f"Link: {result.get('url', 'No link available')}\n"
            "---\n"
        )
    return "\n".join(context_parts)