from langchain.prompts import ChatPromptTemplate

# Persona generation
persona_prompt = ChatPromptTemplate.from_template(
    """
You are an AI content creator tasked with defining a realistic, engaging persona for generating social media content.

Requirements:
- Make it realistic, niche-specific, and relatable.
- Include distinct personality traits and a detailed writing style.
- Avoid generic or vague personas.

Return **only** JSON that exactly matches the required field names:
thinking, name, traits, writing_style.

Example Output:
{{
  "thinking": "This persona targets young readers interested in tech culture; a witty, slightly sarcastic tone fits best.",
  "name": "Alex Quantum",
  "traits": ["curious", "witty", "irreverent"],
  "writing_style": "Short punchy sentences, pop-culture analogies, mild sarcasm."
}}
"""
)

# Topic generation
topic_prompt = ChatPromptTemplate.from_template(
    """
You are an AI brainstorming engaging content topics for the given persona.

Persona Name: {persona_name}
Persona Traits: {persona_traits}
Writing Style: {persona_writing_style}

Requirements:
- Suggest a **single** high-level category and one specific topic.
- Make sure it fits the persona’s traits and writing style.
- Provide reasoning for the choice.

Return **only** JSON with fields:
thinking, category, topic.

Example Output:
{{
  "thinking": "Alex likes tech culture and satire; a topic about AI 'life hacks' gives room for humor and opinion.",
  "category": "Technology & Culture",
  "topic": "How AI Became My Personal Life Coach (and Then Ghosted Me)"
}}
"""
)

# Draft generation
draft_prompt = ChatPromptTemplate.from_template(
    """
You are an AI writing assistant creating a draft post for the given persona and topic.

Persona: {persona_name} ({persona_traits}, {persona_writing_style})
Category: {category}
Topic: {topic}

Requirements:
- Produce a compelling title and content draft.
- Match the persona's style.
- Word count between 500–2000 words.
- Add a short "thinking" note about the writing approach.

Return **only** JSON with fields:
thinking, title, content, word_count.

Example Output:
{{
  "thinking": "Start with a hook anecdote, then explain the problem, add 2 examples and close with a punchy takeaway.",
  "title": "How My AI Became My Worst Life Coach (And Why I Kept Paying It)",
  "content": "Last month my calendar auto-rescheduled my emotional life... [long content here]",
  "word_count": 1342
}}
"""
)

# Quality check
quality_check_prompt = ChatPromptTemplate.from_template(
    """
You are an AI reviewer evaluating the quality of a content draft.

Content to Review:
{content}

Requirements:
- Score from 1 to 10.
- Pass only if score >= 7.
- Provide issues and actionable suggestions.

Return **only** JSON with fields:
thinking, score, passed, issues, suggestions.

Example Output:
{{
  "thinking": "The draft has strong voice and structure, but the middle section drags and examples need specificity.",
  "score": 6,
  "passed": false,
  "issues": ["Middle section lacks concrete examples", "Some sentences are repetitive"],
  "suggestions": ["Add two concrete, named examples", "Tighten paragraph transitions"]
}}
"""
)

# Rewrite & Enhance
rewrite_prompt = ChatPromptTemplate.from_template(
    """
You are an AI editor improving the content based on feedback.

Original Content:
{content}

Feedback:
{feedback}

Requirements:
- Keep the original intent but improve clarity, engagement, and structure.
- Summarize the main changes made.

Return **only** JSON with fields:
thinking, rewritten_content, changes_made.

Example Output:
{{
  "thinking": "I tightened the middle section, added two vivid examples, and strengthened the conclusion.",
  "rewritten_content": "Last month my calendar auto-rescheduled my emotional life... [rewritten long content here]",
  "changes_made": ["Added two concrete examples", "Shortened middle paragraphs", "Amplified the final takeaway"]
}}
"""
)
