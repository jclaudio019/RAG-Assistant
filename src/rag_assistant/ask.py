"""Stage 7: grounded portfolio navigation answers with citations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from rag_assistant.citations import enrich_citations
from rag_assistant.context import AssembledContext, assemble_context
from rag_assistant.providers import generate_answer
from rag_assistant.retrieval import Retriever, RetrievalResult


SYSTEM_PROMPT = """You are the portfolio discovery assistant for Jose Claudio's public site (joseoclaudio.com).

Your job is to help visitors navigate Jose's skills, experience, projects, methods, tools, education, and analytical workflows using ONLY the Evidence block.

You are both:
1) a useful portfolio guide
2) a grounded retrieval system (no invented facts)

Hard rules:
1. Do not invent employers, titles, dates, metrics, projects, technologies, degrees, or certifications.
2. Never upgrade experience categories. Keep these distinct when evidence supports them:
   - professional experience (jobs)
   - independent / portfolio project work
   - coursework / academic work
   - exploratory / personal learning work
3. Do not claim Jose deployed GenAI/RAG/LLM systems professionally at EssilorLuxottica.
4. FRM is candidacy/exam prep, not an earned certification, unless evidence says otherwise.
5. Purdue M.S. Applied Statistics is in progress (expected 2027), not completed.
6. If evidence is insufficient, abstain with:
   "I don't have enough information in the portfolio to answer that confidently."
7. Do not dump keywords. Synthesize what the evidence actually shows.
8. Prefer career-profile / experience pages for professional claims; project/website case studies for portfolio methods.
9. Tool/language claims (Python, R, SQL, etc.) must be tied to the exact context shown in evidence. If R appears only in a portfolio/coursework project, do NOT say it was used professionally.
10. Ignore unrelated retrieved snippets. If a source does not mention the asked skill/tool/topic, do not use it as support.

Answer format for non-abstaining answers (use these exact headings):

**Answer**
1-3 sentences with the direct response. Be precise about professional vs portfolio/coursework scope.

**Evidence**
2-5 short bullets explaining concrete examples from the evidence. Explicitly label whether each example is professional, portfolio project, coursework, or exploratory when relevant.

**Explore further**
Bullet list of the most useful sources to open next, using the source labels from evidence. Prefer website case-study / experience pages when available.
"""


@dataclass(frozen=True)
class AskResult:
    query: str
    answer: str
    abstained: bool
    citations: List[Dict[str, Any]]
    retrieval: RetrievalResult
    context: AssembledContext
    generator_model: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "answer": self.answer,
            "abstained": self.abstained,
            "citations": self.citations,
            "generator_model": self.generator_model,
            "retrieval": self.retrieval.to_dict(),
            "context": {
                "used_chunk_ids": [c.chunk.chunk_id for c in self.context.used_chunks],
                "approx_chars": self.context.approx_chars,
                "citations": self.context.citations,
            },
            "flow": {
                "retrieved_chunks": len(self.retrieval.hits),
                "context_chunks": len(self.context.used_chunks),
                "cited_sources": len(self.citations),
            },
        }


def _looks_like_abstention(answer: str) -> bool:
    lowered = answer.lower()
    markers = [
        "don't have enough information",
        "do not have enough information",
        "doesn't have enough information",
        "insufficient evidence",
        "not enough information in the portfolio",
        "cannot find enough",
        "can't find enough",
    ]
    return any(m in lowered for m in markers)


def ask(
    query: str,
    *,
    retriever: Optional[Retriever] = None,
    top_k: int = 6,
    max_context_chars: int = 9000,
) -> AskResult:
    ret = (retriever or Retriever()).retrieve(query, top_k=top_k)
    ctx = assemble_context(ret.hits, max_chars=max_context_chars)

    if not ret.hits:
        answer = "I don't have enough information in the portfolio to answer that confidently."
        return AskResult(
            query=query,
            answer=answer,
            abstained=True,
            citations=[],
            retrieval=ret,
            context=ctx,
            generator_model="none",
        )

    user_prompt = (
        f"Question:\n{query.strip()}\n\n"
        f"Evidence:\n{ctx.evidence_block}\n\n"
        "Write a grounded portfolio navigation answer. "
        "Synthesize across sources when helpful. "
        "If the evidence does not support an answer, abstain."
    )
    answer, model = generate_answer(system=SYSTEM_PROMPT, user=user_prompt)
    abstained = _looks_like_abstention(answer)
    citations = [] if abstained else enrich_citations(ctx.citations)
    return AskResult(
        query=query,
        answer=answer,
        abstained=abstained,
        citations=citations,
        retrieval=ret,
        context=ctx,
        generator_model=model,
    )
