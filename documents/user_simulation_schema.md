# 🧠 User Simulation System — High-Level Data & Workflow Design

This document outlines a high-level design of the **User Simulation Engine**, focusing on how we represent, enrich, and use simulated user data to drive LLM-based workflows such as generating posts, comments, reactions, and more.

The simulation engine is built to reflect realistic user behavior through external control loops and LangGraph-powered workflows. All actions (e.g., posting, commenting) are triggered based on deterministic logic (not autonomous agent reasoning yet). Each workflow prompts an LLM (Google Gemini) with rich, evolving user context to generate lifelike content.

---

## 🌐 Social Server Context

The **User Simulation Engine** is designed to operate alongside a real **social media backend** server. The simulation interacts with the platform via REST APIs and references user records from the platform’s main database.

- The main server database includes real models like `User`, `Post`, `Comment`, `Reaction`, `Follow`, and `UserFeed`, implemented using SQLModel.
- Each `SimUser` in the simulation maps to a real `User` via `user_id`, ensuring that all actions (posts, comments, reactions) affect the shared ecosystem.
- The simulation system uses the main platform APIs to create content, read feeds, and simulate activity. This allows simulated users to coexist with real users or other simulations in a shared state.
- SQLite is used for the simulation-specific database, but the platform itself can be backed by any relational DB (Postgres, MySQL, etc.).

This architecture allows:

- Seamless integration of simulated content into a live or test social app
- Realistic interactions using shared feed algorithms, visibility rules, and ranking logic
- Monitoring and experimentation on how simulated behavior impacts network dynamics

> 📌 **Design Note**: Consider maintaining a reference map of real user IDs and simulated user instances to make it easier to differentiate user types across workflows.

---

## 📊 Practical Data Usage Scenarios

### When We Update Simulation Tables:
- `SimUser.tick_count`: Every time the simulation loop processes a user
- `SimUser.cooldown_until`: After taking an action
- `UserMentalState`: Updated based on feedback from posts, time of day, or scheduled emotional shifts (can be LLM-inferred or rule-driven)
- `UserActionHistory`: After every simulated user action
- `UserReflection`: On a timed interval (e.g., every 5 actions), or after significant events
- `UserRelationship`: Triggered by interactions (e.g., replies, likes, mentions); sentiment/strength may use deterministic rules or be LLM-evaluated
- `UserPreference`: Periodic updates, such as evolving tone/emojis use over time
- `UserTraitTag`: Used for tagging users in experiments, e.g., A/B test groups, personalities

### When We Use Simulation Tables:
- For building **LLM prompts** with persona, mood, relationship context, memory
- For **workflow logic**, such as filtering eligible users for reflection
- For **behavioral conditioning**, e.g., generating text aligned with long-term traits
- To inform **user targeting** (e.g., whom to comment on based on relationship data)
- For **memory summarization**, feeding past actions into RAG

---

## ❓ Key Design Considerations (Open Questions)

To ensure continued scalability and clarity, the following design issues should be reflected on and formalized:

### 🔄 SimUser ↔ Real User Mapping
- Ensure that the one-to-one mapping between `SimUser` and real `User` is enforced or clearly represented.
- Consider how the system distinguishes between simulated and real users in shared state or during actions.

### 🧠 UserMentalState Evolution
- Define clear logic for how moods are updated: deterministic events (e.g., receiving likes), periodic triggers (e.g., morning → refreshed), or LLM-generated emotional reflection.
- Establish when and how obsession topics or energy levels reset or evolve.

### 🔁 Reflection Triggers and Content
- Determine whether reflection is:
  - A scheduled step (e.g., every N ticks)
  - Triggered by emotional peaks or unusual activity
- Define how `UserActionHistory` entries are aggregated for reflection prompts

### 📚 RAG Integration Strategy
- Clarify where memory lives: vector DB, blob store, or long JSON
- Consider adding `UserMemoryVectorRef` or embedding snapshots to support long-term recall and learning

### 👥 Updating UserRelationship Data
- Define interaction weights (e.g., like = +0.1 strength)
- Decide if sentiment tags are raw labels or generated summaries (e.g., "disrespects", "idolizes")
- Determine whether relationship drift occurs over time without interaction

### 📆 Behavior Scheduling / Determinism
- Document rules that guide when users act
  - Time-based (post every X ticks)
  - State-based (if angry → comment, if bored → scroll feed)
- Create a system to balance stochastic behavior with rule-based predictability

### 🗃️ Growth Management & Archiving
- Specify retention strategy for `UserActionHistory`, `UserReflection`
  - Rolling window (last 500 events)
  - Archival pipeline
  - RAG summary checkpointing

---

## 🧠 Summary

This simulation database structure supports:

- Persistent and evolving simulation memory
- Rich LLM context retrieval per workflow
- Behavioral logging for analysis or learning
- Modular step building with shared state access
- Configurable memory lifespan and summarization
- Clear paths for RAG, reflection, and emotion modeling

You can now easily:

- Generate deeply contextual prompts
- Support user growth over time
- Conduct RAG-style persona prompting
- Run controlled experiments on social behavior

---

Next steps:

- Implement `schema.py` with all these models
- Add `crud.py` to simplify querying and updates
- Define reflection intervals and update policies
- Build `PostWorkflow`, `CommentWorkflow`, `FeedScanWorkflow`, `RelationshipUpdateWorkflow`

