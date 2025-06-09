import tweepy
import config # Import your configuration file

def get_sample_tweet(tweet_id):
    """
    Connects to the Twitter API v2 using a Bearer Token and retrieves a specific tweet.

    Args:
        tweet_id (str): The ID of the tweet to retrieve.

    Returns:
        dict or None: A dictionary containing the tweet data if successful, otherwise None.
    """
    try:
        # Authenticate with the Twitter API v2 using your Bearer Token
        # The Bearer Token is generally sufficient for read-only operations like getting tweets.
        client = tweepy.Client(config.BEARER_TOKEN)

        # Retrieve the tweet using the v2 client.
        # We can request additional fields for richer data, e.g., 'author_id', 'created_at'.
        # For a full list of available fields, refer to Twitter API v2 documentation.
        response = client.get_tweet(tweet_id, tweet_fields=["created_at", "author_id", "text", "public_metrics"], user_fields=["username", "name"])

        if response.data:
            tweet_data = response.data
            includes = response.includes # Contains expanded objects like user details
            author_data = None

            if "users" in includes and includes["users"]:
                # Find the author's data if it's included
                for user in includes["users"]:
                    if user["id"] == tweet_data.author_id:
                        author_data = user
                        break

            print(f"Successfully retrieved Tweet ID: {tweet_id}\n")
            print("--- Tweet Details ---")
            print(f"Tweet ID: {tweet_data.id}")
            print(f"Text: {tweet_data.text}")
            print(f"Created At: {tweet_data.created_at}")

            if author_data:
                print(f"Author Username: @{author_data.username}")
                print(f"Author Name: {author_data.name}")
            else:
                print(f"Author ID: {tweet_data.author_id} (details not expanded)")

            if tweet_data.public_metrics:
                print("\n--- Public Metrics ---")
                for metric, value in tweet_data.public_metrics.items():
                    print(f"{metric.replace('_', ' ').title()}: {value}")
            return tweet_data
        else:
            print(f"No tweet found with ID: {tweet_id}")
            if response.errors:
                print("API Errors:", response.errors)
            return None

    except tweepy.TweepyException as e:
        print(f"Tweepy API Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    # Replace this with an actual Tweet ID you want to retrieve
    # You can find Tweet IDs by looking at the URL of a tweet:
    # e.g., https://twitter.com/TwitterDev/status/1460323737035677698 -> ID is 1460323737035677698
    sample_tweet_id = "1460323737035677698" # A popular tweet from @TwitterDev as an example

    print(f"Attempting to retrieve tweet with ID: {sample_tweet_id}")
    retrieved_tweet = get_sample_tweet(sample_tweet_id)

    if retrieved_tweet:
        print("\nRetrieval successful!")
    else:
        print("\nTweet retrieval failed.")

    # Example of getting a non-existent tweet (should return None)
    # print("\nAttempting to retrieve a non-existent tweet...")
    # non_existent_tweet = get_sample_tweet("1234567890123456789") # A fake ID