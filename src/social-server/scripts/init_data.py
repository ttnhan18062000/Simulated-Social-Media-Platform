import asyncio
import random
from faker import Faker
from datetime import datetime, timezone
from server.db.session import init_db
from server.schemas.user import UserCreate
from server.schemas.post import PostCreate
from server.schemas.comment import CommentCreate
from server.schemas.reaction import ReactionCreate
from server.schemas.follow import FollowCreate
from server.schemas.friendship import FriendshipCreate
from server.schemas.tag import TagCreate
from server.schemas.post_tag import PostTagCreate
from server.schemas.category import CategoryCreate
from server.schemas.post_category import PostCategoryCreate
from server.schemas.user_feed import UserFeedCreate

from server.services.user import create_user
from server.services.post import create_post
from server.services.comment import create_comment
from server.services.reaction import create_reaction
from server.services.follow import create_follow
from server.services.friendship import create_friendship
from server.services.tag import create_tag
from server.services.post_tag import add_tag_to_post
from server.services.category import create_category
from server.services.post_category import add_category_to_post
from server.services.user_feed import create_user_feed

fake = Faker()

NUM_USERS = 50
NUM_POSTS = 250
NUM_COMMENTS = 500
NUM_REACTIONS = 1000
NUM_FOLLOWS = 300
NUM_FRIENDSHIPS = 200
NUM_TAGS = 30
NUM_CATEGORIES = 10
NUM_VIEW_HISTORY = 700
NUM_FEED_ENTRIES = 1000


async def seed():
    await init_db()
    print("🔥 Seeding DB...")

    # Users
    users = []
    print(f"👤 Creating {NUM_USERS} users...")
    for _ in range(NUM_USERS):
        user = UserCreate(
            username=fake.user_name(),
            password="test123",
            bio=fake.sentence(),
        )
        users.append(await create_user(user))

    # Posts
    posts = []
    print(f"📝 Creating {NUM_POSTS} posts...")
    for _ in range(NUM_POSTS):
        post = PostCreate(
            user_id=random.choice(users).id,
            content_text=fake.paragraph(nb_sentences=random.randint(1, 3)),
            image_url=fake.image_url() if random.random() < 0.3 else None,
            visibility=random.choice(["public", "friends", "private"]),
        )
        posts.append(await create_post(post))

    # Comments
    print(f"💬 Creating {NUM_COMMENTS} comments...")
    for _ in range(NUM_COMMENTS):
        comment = CommentCreate(
            post_id=random.choice(posts).id,
            user_id=random.choice(users).id,
            content_text=fake.sentence(),
        )
        await create_comment(comment)

    # Reactions
    print(f"👍 Creating {NUM_REACTIONS} reactions...")
    for _ in range(NUM_REACTIONS):
        reaction = ReactionCreate(
            post_id=random.choice(posts).id,
            user_id=random.choice(users).id,
            type=random.choice(["like", "upvote", "love", "haha", "wow"]),
        )
        await create_reaction(reaction)

    # Follows
    print(f"🔗 Creating {NUM_FOLLOWS} follows...")
    for _ in range(NUM_FOLLOWS):
        follower = random.choice(users)
        following = random.choice(users)
        if follower.id != following.id:
            await create_follow(
                FollowCreate(
                    follower_id=follower.id,
                    following_id=following.id,
                )
            )

    # Friendships
    print(f"👯 Creating {NUM_FRIENDSHIPS} friendships...")
    for _ in range(NUM_FRIENDSHIPS):
        u1 = random.choice(users)
        u2 = random.choice(users)
        if u1.id != u2.id:
            await create_friendship(
                FriendshipCreate(
                    user_id=u1.id,
                    friend_id=u2.id,
                    status=random.choice(["requested", "accepted", "blocked"]),
                )
            )

    # Tags & PostTags
    print(f"🏷️ Creating {NUM_TAGS} tags + tagging posts...")
    tags = []
    for _ in range(NUM_TAGS):
        tag = await create_tag(TagCreate(name=fake.word()))
        tags.append(tag)

    for post in posts:
        for _ in range(random.randint(0, 3)):
            tag = random.choice(tags)
            await add_tag_to_post(PostTagCreate(post_id=post.id, tag_id=tag.id))

    # Categories & PostCategories
    print(f"📁 Creating {NUM_CATEGORIES} categories + assigning posts...")
    categories = []
    for _ in range(NUM_CATEGORIES):
        category = await create_category(
            CategoryCreate(name=fake.word().capitalize(), description=fake.sentence())
        )
        categories.append(category)

    for post in posts:
        for _ in range(random.randint(0, 2)):
            category = random.choice(categories)
            await add_category_to_post(
                PostCategoryCreate(post_id=post.id, category_id=category.id)
            )

    # Feed Entries
    print(f"📰 Creating {NUM_FEED_ENTRIES} feed entries...")
    for _ in range(NUM_FEED_ENTRIES):
        await create_user_feed(
            UserFeedCreate(
                user_id=random.choice(users).id,
                post_id=random.choice(posts).id,
                rank_score=random.uniform(0, 1),
                source_type=random.choice(
                    ["follow", "friend", "trending", "recommended"]
                ),
                visibility=random.choice(["public", "friends", "private"]),
                is_seen=random.choice([True, False]),
            )
        )

    print("✅ Done seeding!")


if __name__ == "__main__":
    asyncio.run(seed())
