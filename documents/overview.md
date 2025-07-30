# Social Media Web Server: Technical Design & Architecture

### 1. Overview 📜

This document outlines the technical architecture for a scalable social media web server. The system is designed to handle core social networking features, including user profiles, content creation (posts), a news feed, social relationships, and user interactions.

The architecture prioritizes a clean separation of concerns, using a synchronous **API layer** for immediate user-facing actions and an **asynchronous, event-driven backend** for processing background tasks like feed fan-out and notifications. This approach ensures a responsive user experience while maintaining a scalable and resilient system.

***

### 2. System Architecture 🏗️

The system is built on a modern, asynchronous Python stack and follows a microservices-inspired pattern where responsibilities are clearly defined.

#### 2.1. High-Level Architecture Flow

The system architecture follows a layered request flow:

1.  **Client (Mobile/Web App):** Initiates all requests via HTTP/S.
2.  **Load Balancer:** Distributes incoming traffic to available API service instances.
3.  **API Service (FastAPI):** Acts as the synchronous entry point. It handles authentication, validation, and simple database/cache reads. For complex or slow operations, it publishes an event.
4.  **Message Broker (RabbitMQ/Redis):** This event bus decouples the API service from background processing. It receives events like `post.created`.
5.  **Async Workers:** These background services subscribe to events. They consume messages from the broker and perform the heavy lifting, such as calculating feed updates or sending notifications.
6.  **Database (PostgreSQL) & Cache (Redis):** The persistence and caching layers are the system's source of truth and speed, accessed by both the API Service and the Workers.

#### 2.2. Technology Stack

| Layer | Technology | Justification |
| :--- | :--- | :--- |
| **API Framework** | FastAPI | Provides high performance due to its asynchronous nature (ASGI), automatic data validation with Pydantic, and built-in interactive API documentation. |
| **ORM & Database** | SQLModel & PostgreSQL | SQLModel combines SQLAlchemy and Pydantic for robust, type-safe database operations. PostgreSQL is a production-grade relational database. SQLite is suitable for development. |
| **Async Message Broker** | RabbitMQ / Redis Streams | Decouples services and handles background processing. RabbitMQ is a robust, feature-rich choice. Redis Streams offers a lightweight alternative. |
| **Feed/Data Cache** | Redis | An in-memory data store used for caching pre-computed user feeds and other frequently accessed data, dramatically reducing database load for read-heavy operations. |
| **Authentication** | OAuth2 / JWT | Industry-standard protocols for secure, token-based authentication, managed easily via FastAPI's security utilities. |
| **Transport** | HTTP/S & WebSockets | RESTful API for standard communication. WebSockets can be added for real-time features like live notifications or chat. |

***

### 3. Service Boundaries & Data Flow ⚙️

#### 3.1. Service Responsibilities

* **📡 API Service (FastAPI):** The primary entry point for all client requests. It acts as a thin controller layer.
    * **Responsibilities:** Handles **authentication/authorization**, request validation, and rate limiting. Manages **synchronous CRUD operations** (e.g., creating a user, saving an initial post). Publishes events to the message broker for tasks that don't need to block the user's request.

* **🧠 Asynchronous Workers (Consumers):** Background services that subscribe to events from the message broker and perform the heavy lifting.
    * **Feed Fan-out Worker:** Triggered by `PostCreated` events. It identifies the author's followers and pushes the new post ID into each follower's cached feed (e.g., a Redis Sorted Set). This is the core of the **"fan-out-on-write"** strategy.
    * **Notification Worker:** Triggered by events like `ReactionCreated` or `CommentCreated`. It generates and saves a notification record for the relevant user(s).
    * **Other Workers:** Can be added for tasks like feed cleanup, analytics processing, or content moderation.

#### 3.2. Example Data Flow: Creating & Viewing a Post

**Scenario 1: User A Creates a Post**

1.  `Client` -> `POST /api/v1/posts` with content.
2.  `API Service` validates the request and token.
3.  `API Service` performs a **synchronous** write to the `posts` table in the PostgreSQL database.
4.  `API Service` publishes a `post.created` event to the Message Broker with `{ "post_id": 123, "user_id": "user-a", "timestamp": ... }`.
5.  `API Service` returns a `201 Created` response to the client **immediately**.
6.  The `Feed Fan-out Worker` consumes the `post.created` event. It fetches all followers of "user-a" and, for each follower, adds the `post_id` to their feed cache in Redis (e.g., `ZADD feed:follower_id <timestamp> 123`).

**Scenario 2: User B Views Their Feed**

1.  `Client` -> `GET /api/v1/feed`.
2.  `API Service` validates the request and gets User B's ID.
3.  `API Service` queries Redis to get a list of post IDs from User B's cached feed (e.g., `ZRANGE feed:user-b 0 50 BYSCORE REV`). This is extremely fast.
4.  `API Service` performs a **single** database query to fetch the full post objects for those IDs (e.g., `SELECT * FROM posts WHERE id IN (...)`). This is known as "hydrating" the data.
5.  `API Service` filters out any posts from users that User B has blocked.
6.  `API Service` returns the sorted, hydrated list of posts to the client.