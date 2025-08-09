from ..models.generate_content_models import (
    GraphState,
    PersonaOutput,
    TopicOutput,
    PostDraftOutput,
    QualityCheckOutput,
    RewriteOutput,
)
from ..prompts.generate_content_prompts import (
    persona_prompt,
    topic_prompt,
    draft_prompt,
    quality_check_prompt,
    rewrite_prompt,
)
from langchain.chat_models import init_chat_model

# Init model (Gemini example)
model = init_chat_model("gemini-2.0-flash-lite", model_provider="google_genai")

# Chains
persona_chain = persona_prompt | model.with_structured_output(PersonaOutput)
topic_chain = topic_prompt | model.with_structured_output(TopicOutput)
draft_chain = draft_prompt | model.with_structured_output(PostDraftOutput)
quality_chain = quality_check_prompt | model.with_structured_output(QualityCheckOutput)
rewrite_chain = rewrite_prompt | model.with_structured_output(RewriteOutput)


def generate_persona(state: GraphState) -> GraphState:
    output = persona_chain.invoke({})
    state.persona = output
    return state


def generate_topic(state: GraphState) -> GraphState:
    output = topic_chain.invoke(
        {
            "persona_name": state.persona.name,
            "persona_traits": ", ".join(state.persona.traits),
            "persona_writing_style": state.persona.writing_style,
        }
    )
    state.topic = output
    return state


def generate_draft(state: GraphState) -> GraphState:
    output = draft_chain.invoke(
        {
            "persona_name": state.persona.name,
            "persona_traits": ", ".join(state.persona.traits),
            "persona_writing_style": state.persona.writing_style,
            "category": state.topic.category,
            "topic": state.topic.topic,
        }
    )
    state.draft = output
    return state


def quality_check(state: GraphState) -> GraphState:
    output = quality_chain.invoke({"content": state.draft.content})
    state.quality_check = output
    return state


def rewrite_content(state: GraphState) -> GraphState:
    output = rewrite_chain.invoke(
        {
            "content": state.draft.content,
            "feedback": " | ".join(state.quality_check.suggestions),
        }
    )
    state.rewrite = output
    return state
