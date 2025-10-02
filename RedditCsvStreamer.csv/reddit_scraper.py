import praw
import pandas as pd
import time

# ---------- CONFIGURE HERE ----------
CLIENT_ID = "bHUWyehHGpIzX8jM4q2WjQ"
CLIENT_SECRET = "C7QqDcdYnQ15m-btlQCg58YFG8_P0A"
USER_AGENT = "MyScraper by u/InstructionSilent334"
CSV_FILE_NAME = "reddit_data.csv"

SUBREDDITS = ["worldnews", "news", "technology", "politics", "environment"]
POST_LIMIT_HOT = 1500    # priority fetch
POST_LIMIT_OTHERS = 800  # for new/top/controversial
# ------------------------------------

# Authenticate
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

all_posts = []

print("Fetching data from subreddits:", ", ".join(SUBREDDITS))

for sub in SUBREDDITS:
    subreddit = reddit.subreddit(sub)

    # HOT posts first (priority)
    print(f"Fetching HOT from r/{sub} ...")
    for submission in subreddit.hot(limit=POST_LIMIT_HOT):
        all_posts.append(submission)

    # NEW posts
    print(f"Fetching NEW from r/{sub} ...")
    for submission in subreddit.new(limit=POST_LIMIT_OTHERS):
        all_posts.append(submission)

    # TOP posts with different time filters
    time_filters = ["day", "week", "month", "year", "all"]
    for tf in time_filters:
        print(f"Fetching TOP ({tf}) from r/{sub} ...")
        for submission in subreddit.top(time_filter=tf, limit=POST_LIMIT_OTHERS):
            all_posts.append(submission)
        time.sleep(1)

    # CONTROVERSIAL posts
    for tf in time_filters:
        print(f"Fetching CONTROVERSIAL ({tf}) from r/{sub} ...")
        for submission in subreddit.controversial(time_filter=tf, limit=POST_LIMIT_OTHERS):
            all_posts.append(submission)
        time.sleep(1)

# Remove duplicates by ID
unique_posts = {p.id: p for p in all_posts}.values()

# Prepare data (15 columns)
data = []
for submission in unique_posts:
    data.append([
        submission.id,
        submission.title,
        submission.score,
        submission.author.name if submission.author else "deleted",
        submission.created_utc,
        submission.num_comments,
        submission.domain,
        submission.url,
        submission.subreddit.display_name,
        submission.upvote_ratio,
        submission.over_18,
        submission.link_flair_text,
        submission.is_self,
        submission.num_crossposts,
        submission.permalink
    ])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    "ID", "Title", "Score", "Author", "Created_UTC", "Comments",
    "Domain", "URL", "Subreddit", "Upvote_Ratio", "NSFW", "Flair",
    "Is_Self", "Crossposts", "Permalink"
])

# Save to CSV
df.to_csv(CSV_FILE_NAME, index=False, encoding="utf-8")

print(f"✅ Done! Saved {len(df)} unique posts to {CSV_FILE_NAME}")