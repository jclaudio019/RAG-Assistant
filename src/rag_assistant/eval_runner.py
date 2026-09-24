"""Stage 5: small retrieval evaluation harness (~25 questions)."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set

from rag_assistant.paths import EVAL_QUESTIONS, EVAL_RESULTS
from rag_assistant.retrieval import Retriever


@dataclass
class QuestionScore:
    id: str
    question: str
    should_answer: bool
    source_hit: bool
    fact_hit: bool
    expected_document_ids: List[str]
    retrieved_document_ids: List[str]
    matched_facts: List[str]
    missing_facts: List[str]
    top_scores: List[float]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _load_questions(path: Path = EVAL_QUESTIONS) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["questions"]


def _fact_present(hits_text: str, fact: str) -> bool:
    return fact.lower() in hits_text.lower()


def score_question(
    item: Dict[str, Any],
    retriever: Retriever,
    *,
    top_k: int = 5,
) -> QuestionScore:
    result = retriever.retrieve(item["question"], top_k=top_k)
    retrieved_docs = [h.chunk.document_id for h in result.hits]
    expected: Set[str] = set(item.get("expected_document_ids") or [])
    source_hit = bool(expected.intersection(retrieved_docs)) if expected else True

    joined = "\n".join(h.chunk.content for h in result.hits)
    required_facts: List[str] = list(item.get("required_facts") or [])
    matched = [f for f in required_facts if _fact_present(joined, f)]
    missing = [f for f in required_facts if f not in matched]
    # Abstain questions: fact_hit means we did NOT retrieve misleading "yes" evidence poorly —
    # we simply check required_facts if any; otherwise treat as N/A success when should_answer is false.
    if item.get("should_answer", True):
        fact_hit = (not required_facts) or (len(matched) == len(required_facts))
    else:
        fact_hit = True

    return QuestionScore(
        id=item["id"],
        question=item["question"],
        should_answer=bool(item.get("should_answer", True)),
        source_hit=source_hit,
        fact_hit=fact_hit,
        expected_document_ids=sorted(expected),
        retrieved_document_ids=retrieved_docs,
        matched_facts=matched,
        missing_facts=missing,
        top_scores=[round(h.score, 4) for h in result.hits],
    )


def run_evaluation(
    *,
    top_k: int = 5,
    questions_path: Path = EVAL_QUESTIONS,
    results_path: Path = EVAL_RESULTS,
    retriever: Optional[Retriever] = None,
) -> Dict[str, Any]:
    questions = _load_questions(questions_path)
    ret = retriever or Retriever()
    scores = [score_question(q, ret, top_k=top_k) for q in questions]

    answerable = [s for s in scores if s.should_answer]
    source_hits = sum(1 for s in answerable if s.source_hit)
    fact_hits = sum(1 for s in answerable if s.fact_hit)
    n = len(answerable) or 1

    report = {
        "top_k": top_k,
        "question_count": len(scores),
        "answerable_count": len(answerable),
        "source_hit_rate": round(source_hits / n, 3),
        "fact_hit_rate": round(fact_hits / n, 3),
        "both_hit_rate": round(
            sum(1 for s in answerable if s.source_hit and s.fact_hit) / n, 3
        ),
        "failures": [
            s.to_dict()
            for s in answerable
            if not (s.source_hit and s.fact_hit)
        ],
        "scores": [s.to_dict() for s in scores],
        "reranking_needed": None,  # filled by operator after inspecting failures
        "notes": (
            "Baseline vector retrieval only. Reranking should be added only if "
            "source/fact hit rates show clear ranking problems."
        ),
    }
    results_path.parent.mkdir(parents=True, exist_ok=True)
    results_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report
