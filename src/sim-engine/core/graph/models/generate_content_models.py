# models.py
from typing import List, Optional
from pydantic import BaseModel, Field


class PersonaOutput(BaseModel):
    thinking: str = Field(
        description="Rationale behind choosing this persona: why this persona fits the target audience and the intended voice."
    )
    name: str = Field(
        description="Persona name or identifier (e.g., 'The Witty Historian')."
    )
    traits: List[str] = Field(
        description="Key personality traits that define the persona."
    )
    writing_style: str = Field(
        description="Description of the persona's tone, cadence, and stylistic quirks."
    )

    # Example expected output (exactly matches these field names):
    # {
    #   "thinking": "This persona targets young readers interested in tech culture; a witty, slightly sarcastic tone fits best.",
    #   "name": "Alex Quantum",
    #   "traits": ["curious", "witty", "irreverent"],
    #   "writing_style": "Short punchy sentences, pop-culture analogies, mild sarcasm."
    # }


class TopicOutput(BaseModel):
    thinking: str = Field(
        description="Reasoning for selecting this topic/category, tied back to the persona's interests and audience fit."
    )
    category: str = Field(
        description="High-level category (e.g., 'Technology', 'Lifestyle')."
    )
    topic: str = Field(description="Specific post topic or headline idea.")

    # Example expected output:
    # {
    #   "thinking": "Alex likes tech culture and satire; a topic about AI 'life hacks' gives room for humor and opinion.",
    #   "category": "Technology & Culture",
    #   "topic": "How AI Became My Personal Life Coach (and Then Ghosted Me)"
    # }


class PostDraftOutput(BaseModel):
    thinking: str = Field(
        description="Short note that explains the draft approach (structure, POV, hook)."
    )
    title: str = Field(description="Draft post title / headline.")
    content: str = Field(
        description="Draft post content. Should aim for 500–2000 words during final generation."
    )
    word_count: Optional[int] = Field(
        description="Estimated or actual word count of content, if available."
    )

    # Example expected output:
    # {
    #   "thinking": "Start with a hook anecdote, then explain the problem, add 2 examples and close with a punchy takeaway.",
    #   "title": "How My AI Became My Worst Life Coach (And Why I Kept Paying It)",
    #   "content": "Last month my calendar auto-rescheduled my emotional life... [long content here]",
    #   "word_count": 1342
    # }


class QualityCheckOutput(BaseModel):
    thinking: str = Field(
        description="Detailed reviewer reasoning that explains the quality decision and context."
    )
    score: int = Field(description="Numeric quality score (1–10).")
    passed: bool = Field(
        description="Whether the draft passed the quality gate (True if score >= threshold)."
    )
    issues: List[str] = Field(description="Concrete issues found (empty list if none).")
    suggestions: List[str] = Field(
        description="Actionable suggestions for improvement."
    )

    # Example expected output:
    # {
    #   "thinking": "The draft has strong voice and structure, but the middle section drags and examples need specificity.",
    #   "score": 6,
    #   "passed": false,
    #   "issues": ["Middle section lacks concrete examples", "Some sentences are repetitive"],
    #   "suggestions": ["Add two concrete, named examples", "Tighten paragraph transitions"]
    # }


class RewriteOutput(BaseModel):
    thinking: str = Field(
        description="Reasoning for the editorial decisions made during rewriting/enhancement."
    )
    rewritten_content: str = Field(description="Final improved content after rewrite.")
    changes_made: List[str] = Field(
        description="Short summary list of the most significant changes applied."
    )

    # Example expected output:
    # {
    #   "thinking": "I tightened the middle section, added two vivid examples, and strengthened the conclusion.",
    #   "rewritten_content": "Last month my calendar auto-rescheduled my emotional life... [rewritten long content here]",
    #   "changes_made": ["Added two concrete examples", "Shortened middle paragraphs", "Amplified the final takeaway"]
    # }


class GraphState(BaseModel):
    """
    GraphState holds the output of each node so the next node can receive the previous node's exact output shape.
    - persona -> passed into topic generation
    - topic -> passed into draft generation (or used to create a draft)
    - draft -> passed into quality_check
    - quality_check -> its feedback passed into rewrite
    - rewrite -> final enhanced content
    """

    persona: Optional[PersonaOutput] = None
    topic: Optional[TopicOutput] = None
    draft: Optional[PostDraftOutput] = None
    quality_check: Optional[QualityCheckOutput] = None
    rewrite: Optional[RewriteOutput] = None
