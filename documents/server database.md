# 🧠 Social Media MVP: Core Design (Posts, Users, Newsfeed)

## 🔑 Core Entities

### 1. User

```json
{
  "id": "...",
  "username": "...",
  "email": "...",
  "password_hash": "...",
  "bio": "...",
  "avatar_url": "...",
  "created_at": "...",
  "last_active_at": "..."
}
```

### 2. Post

```json
{
  "id": "...",
  "user_id": "...",
  "content_text": "...",
  "image_url": "...",
  "visibility": "public | friends-only | private",
  "created_at": "...",
  "updated_at": "..."
}
```

---

## 📌 Relationships

### 3. Friendship (bidirectional via two rows)

```json
{
  "id": "...",
  "user_id": "...",
  "friend_id": "...",
  "status": "requested | accepted | blocked",
  "created_at": "..."
}
```

### 4. Follow (one-way, Twitter-style)

```json
{
  "id": "...",
  "follower_id": "...",
  "following_id": "...",
  "created_at": "..."
}
```

### 5. Block (one-way hard block)

```json
{
  "id": "...",
  "blocker_id": "...",
  "blocked_id": "...",
  "created_at": "..."
}
```

---

## 💬 User Interactions

### 6. Comment

```json
{
  "id": "...",
  "post_id": "...",
  "user_id": "...",
  "content_text": "...",
  "created_at": "..."
}
```

### 7. Reaction

```json
{
  "id": "...",
  "user_id": "...",
  "post_id": "...",
  "type": "like | love | upvote | etc.",
  "created_at": "..."
}
```

---

## 🍿 Post Classification

### 8. Category (admin/curated)

```json
{
  "id": "...",
  "name": "..."
}
```

### 9. Tag (user-generated)

```json
{
  "id": "...",
  "name": "..."
}
```

### 10. PostCategory (many-to-many)

```json
{
  "post_id": "...",
  "category_id": "..."
}
```

### 11. PostTag (many-to-many)

```json
{
  "post_id": "...",
  "tag_id": "..."
}
```

---

## 📰 Feed & History

### 12. UserPostViewHistory

```json
{
  "id": "...",
  "user_id": "...",
  "post_id": "...",
  "viewed_at": "..."
}
```

*You can optionally add:*

- `UserReactionHistory`
- `UserCommentHistory`
- `UserFollowedTags`
- `UserFollowedCategories`

---

## ✨ Optional but MVP-Worthy

### 13. Notification

```json
{
  "id": "...",
  "user_id": "...",     // recipient
  "actor_id": "...",    // who triggered the event
  "type": "reaction | comment | follow | friend_request",
  "post_id": "...",
  "read": true,
  "created_at": "..."
}
```

### 14. FriendRequest (separate from Friendship)

```json
{
  "id": "...",
  "from_user_id": "...",
  "to_user_id": "...",
  "status": "pending | accepted | declined",
  "created_at": "..."
}
```

---

## 🚀 Query-Based Feed (Simplified Logic)

- Posts from `Followed` users
- Posts from `Friends`
- Posts matching tags/categories the user has interacted with
- Posts recently `Liked`, `Viewed`, or `Commented`

*Sort options:*

- By `created_at`
- By hybrid score: `recency + engagement relevance`

---

## 🧠 Design Notes

- ✅ Posts support visibility: `public`, `friends-only`, `private`
- ✅ Follow ≠ Friend
- ✅ Block disables access to both profile & content
- ✅ Categories are curated, Tags are user-generated
- ✅ Feed is customizable using follow & interaction data

---

## 🔗 Entity Relationship Diagram (Textual Form)

```
User
 ├─< Post >─├─< Reaction >─┐
 │          ├─< Comment >─┐
 │          ├─< PostTag >─├─> Tag
 │          └─< PostCategory >─> Category
 ├─< Follow >─> User
 ├─< Friendship >─> User
 ├─< Block >─> User
 ├─< Notification
 └─< ViewHistory >─> Post
```

