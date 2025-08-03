🔧 Core API Resource Design (Production Ready)
🧑‍ Users
Action	Method & Route
Create user	POST /users
Get user profile	GET /users/{user_id}
Update profile	PATCH /users/{user_id}
Follow user	POST /users/{user_id}/follow
Unfollow user	DELETE /users/{user_id}/follow
Get followers / following	GET /users/{user_id}/followers, GET /users/{user_id}/following

🧾 Posts
Action	Method & Route
Create post	POST /posts
Get post	GET /posts/{post_id}
Update/delete post	PATCH /posts/{post_id}, DELETE /posts/{post_id}
Get user’s posts	GET /users/{user_id}/posts
Feed (timeline)	GET /feeds/{user_id} or GET /users/{user_id}/feed

💬 Comments
Action	Method & Route
Create comment	POST /posts/{post_id}/comments
List comments for post	GET /posts/{post_id}/comments
Update/delete comment	PATCH /comments/{comment_id}, DELETE /comments/{comment_id}
All user comments	GET /users/{user_id}/comments

❤️ Reactions
Action	Method & Route
React to post	POST /posts/{post_id}/reactions
Update/remove reaction	PATCH /reactions/{reaction_id}, DELETE /reactions/{reaction_id}
Get all reactions for a post	GET /posts/{post_id}/reactions

🏷 Tags
Action	Method & Route
Get all tags	GET /tags
Add tag to post	POST /posts/{post_id}/tags
Remove tag from post	DELETE /posts/{post_id}/tags/{tag_id}
Get posts by tag	GET /tags/{tag_id}/posts

📂 Categories
Action	Method & Route
Get all categories	GET /categories
Add category to post	POST /posts/{post_id}/categories
Remove category	DELETE /posts/{post_id}/categories/{category_id}
Get posts by category	GET /categories/{category_id}/posts

👁 View History
Action	Method & Route
Track view (auto on view)	POST /posts/{post_id}/views (or internal)
Get user view history	GET /users/{user_id}/view-history
Admin bulk view log	GET /views?post_id=...&user_id=...

👯 Friendships
Action	Method & Route
Send friend request	POST /users/{user_id}/friendships
Accept/decline request	PATCH /friendships/{friendship_id}
Remove/block friend	DELETE /friendships/{friendship_id}
List friends	GET /users/{user_id}/friends

📰 User Feed
Action	Method & Route
Get feed	GET /users/{user_id}/feed
Mark post as seen	PATCH /feeds/{feed_id}
Ranking/debug	GET /feeds/{feed_id}/debug (optional for internal use)

🧠 Why this structure slaps:
Easy for mobile + web clients

Scales with microservices or modular backends

Cleanly separates user-level, post-level, and system-level concerns

Follows REST while leaving room for gRPC/WebSockets later

