🔑 Core Entities
1. User
json
Copy
Edit
{
  id,
  username,
  email,
  password_hash,
  bio,
  avatar_url,
  created_at,
  last_active
}
2. Post
json
Copy
Edit
{
  id,
  user_id,
  content_text,
  created_at,
  updated_at,
  visibility, // public, friends-only, private
}
📎 Relationships (Core)
3. Friendship
Bidirectional (or two rows for undirected model)

json
Copy
Edit
{
  id,
  user_id,
  friend_id,
  status, // requested, accepted, blocked
  created_at
}
4. Follow
One-way relationship (Twitter-style)

json
Copy
Edit
{
  id,
  follower_id,
  following_id,
  created_at
}
5. Block
One-way hard block (prevents seeing/interaction)

json
Copy
Edit
{
  id,
  blocker_id,
  blocked_id,
  created_at
}
💬 Interactions
6. Comment
json
Copy
Edit
{
  id,
  post_id,
  user_id,
  content_text,
  created_at
}
7. Reaction
json
Copy
Edit
{
  id,
  user_id,
  post_id,
  type, // upvote or downvote
  created_at
}
🏷️ Categorization
8. Category
json
Copy
Edit
{
  id,
  name
}
9. Tag
json
Copy
Edit
{
  id,
  name
}
10. PostCategory / PostTag (many-to-many pivot)
json
Copy
Edit
{
  post_id,
  category_id
}
json
Copy
Edit
{
  post_id,
  tag_id
}
📰 Feed System (Basic Personalization)
You mentioned feeds that reflect:

history (interacted content)

follows

friends

So you’ll need:

11. UserPostViewHistory
json
Copy
Edit
{
  id,
  user_id,
  post_id,
  viewed_at
}
You can combine this with:

UserReactionHistory

UserCommentHistory

UserFollowedCategories/Tags (for interest personalization)

✨ Optional but Practical
12. Notification
For likes, comments, friend requests

json
Copy
Edit
{
  id,
  user_id, // recipient
  type, // comment, reaction, follow, friend_request
  actor_id,
  post_id,
  read: boolean,
  created_at
}
13. FriendRequest (separate from friendship table, cleaner logic)
json
Copy
Edit
{
  id,
  from_user_id,
  to_user_id,
  status, // pending, accepted, declined
  created_at
}
🚀 Query-Based Feeds (Simplified Logic)
Pull in:

Posts by followed users

Posts from friends

Posts tagged with your interaction history

Sort by recency or hybrid "score" (recency + interaction relevance)

🧠 What You Missed (Must-Have Even in MVP):
Visibility/privacy on posts

Blocking should restrict access to user profile + content

Post timestamps

Follow vs friend distinction — follow = one-way, friend = mutual

Tag/category separation — categories are curated, tags are user-generated

Feed curation — without history or follow data, you can’t personalize feed

TL;DR Entity Relationship Visual (simplified):
sql
Copy
Edit
User --< Post >-- Tag
User --< Reaction >-- Post
User --< Comment >-- Post
User --< ViewHistory >-- Post
User --< Follow >-- User
User --< Block >-- User
User --< FriendRequest
Post >-- Category
