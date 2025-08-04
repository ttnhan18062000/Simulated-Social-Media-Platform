# 🧠 Sim-Engine: User Simulation System  
**Epic Requirement Document**

## 💡 Objective  
Build a modular simulation engine that mimics realistic user behavior over time. Simulated users will interact with a social app via HTTP-like APIs to read, write, and occasionally modify content (posts). Their behavior should follow natural patterns—daily routines, usage habits, and random variance—giving the illusion of a living, breathing digital community.

---

## 🗂️ Components

### 1. **User Generation**
**Purpose**: Spawn users at randomized intervals to simulate organic userbase growth.

**Requirements**:
- Users are created at random time intervals (configurable).
- Each user is assigned a unique `id`, `created_at` timestamp, and a `personality profile` (see below).
- Optional: assign each user a name/avatar/faction for richer context.

---

### 2. **Daily Routine Engine**
**Purpose**: Each user mimics real-world daily behavior with defined time blocks and actions.

**States**:
- `sleeping`: 0% chance of interaction.
- `working`: low chance of interaction.
- `relaxing`: high activity period.

**Requirements**:
- Users switch states based on a simulated 24-hour clock (accelerated for testing).
- Each state influences:
  - Activity frequency
  - Action probabilities
  - Content creation/consumption behavior

**Example Time Block**:

| Time        | State     |
|-------------|-----------|
| 00:00–06:00 | Sleeping  |
| 06:00–09:00 | Working   |
| 09:00–11:00 | Relaxing  |
| ...         | ...       |

---

### 3. **User Personality Profiles**
**Purpose**: Introduce behavioral variety across users.

**Types (examples)**:
- `Lurker`: mostly reads posts, rarely posts or updates.
- `Chatterbox`: high post frequency, frequent updater.
- `Night Owl`: active during off-hours.
- `Content Curator`: often updates own posts.

**Each profile** defines:
- Active hours skew
- Action weight matrix per state
- Update/post frequencies

---

### 4. **Action Simulation**
**Purpose**: Simulate real-time interaction with the API.

**Actions**:
- `GET /posts`: browsing the feed
- `GET /posts/{id}`: reading a specific post
- `POST /posts`: creating a new post
- `PUT /posts/{id}`: updating a post (rare)
- Optional: `DELETE /posts/{id}`: very rare

**Requirements**:
- Each action has a base probability per state and is influenced by user profile.
- Each action call is logged (console, file, or DB) for traceability.
- Actions must be asynchronously dispatched (via async HTTP or direct function call to avoid overhead).

---

### 5. **Simulation Controller**
**Purpose**: The orchestrator loop that drives the simulation.

**Responsibilities**:
- Maintain the global clock.
- Handle new user spawning.
- Tick each user's lifecycle and schedule actions.
- Log/report results and metrics.

**Optional Features**:
- Pause/resume simulation.
- Variable tick speed (real-time or accelerated).
- Save/load user state snapshots.

---

### 6. **Metrics & Monitoring**
**Purpose**: Track and understand simulation dynamics.

**Requirements**:
- Total number of users over time.
- Number of actions per action type (per hour).
- Top posters / top viewed posts.
- Log of latest N actions (print or JSON file).

**Optional**:
- Live dashboard (e.g., simple terminal dashboard or streamed to a frontend).

---

## 🧪 Stretch Features (Not MVP but Valuable Later)

- **Trend-aware Behavior**: Users react to top posts (e.g., like/repost/quote).
- **Interaction Web**: Users follow other users and interact more with them.
- **Reputation System**: Users with more posts are more likely to be viewed.
- **Post Categories/Tags**: More realistic posting and filtering.
- **Fail Simulation**: Users retry actions on failure, simulate network blips.

---

## 🧱 Tech Stack Notes
- **Language**: Python 3.10+
- **Concurrency**: `asyncio` for async user behavior.
- **API Interface**: Interact with your FastAPI backend directly or mock endpoints for speed.
- **Storage (optional)**: SQLite / file-based for action logs, or just in-memory.

---

## ✅ Deliverables
1. `sim_engine/` module containing:
   - `user.py`: `SimUser` logic
   - `routine.py`: state/time logic
   - `controller.py`: simulation loop
   - `actions.py`: API interaction logic
2. Config file (`sim_config.py` or `.yaml`) for:
   - Simulation tick rate
   - Probabilities and schedules
   - Personality profiles
3. CLI or main script to start/pause/stop simulation
4. Logs or console output showing what users are doing
