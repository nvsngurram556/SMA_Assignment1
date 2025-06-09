import tweepy
import config # Import your configuration file

def get_user_id_from_username(username):
    """
    Retrieves the User ID for a given username using the Twitter API v2.

    Args:
        username (str): The Twitter username (e.g., "TwitterDev").

    Returns:
        str or None: The User ID if found, otherwise None.
    """
    try:
        client = tweepy.Client(config.BEARER_TOKEN)
        response = client.get_user(username=username)

        if response.data:
            return response.data.id
        else:
            print(f"Could not find user with username: @{username}")
            if response.errors:
                print("API Errors:", response.errors)
            return None
    except tweepy.TweepyException as e:
        print(f"Tweepy API Error getting user ID: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred getting user ID: {e}")
        return None

def get_account_holder_posts(username, max_results=5):
    """
    Retrieves a specified number of recent posts (tweets) shared by an account holder.

    Args:
        username (str): The Twitter username of the account holder (e.g., "TwitterDev").
        max_results (int): The maximum number of tweets to retrieve (Twitter API limit is 100 for this endpoint per request).

    Returns:
        list: A list of dictionaries, each representing a tweet. Returns an empty list if no tweets found or an error occurs.
    """
    user_id = get_user_id_from_username(username)
    if not user_id:
        return []

    print(f"\nRetrieving recent posts for user: @{username} (ID: {user_id})\n")

    tweets_list = []
    try:
        client = tweepy.Client(config.BEARER_TOKEN)

        # Retrieve user's tweets
        # tweet_fields: Request specific fields for the tweet object
        # expansions: Request additional objects to be included (like author details)
        # max_results: Number of tweets to retrieve (up to 100 per request)
        response = client.get_users_tweets(
            id=user_id,
            tweet_fields=["created_at", "text", "public_metrics"],
            max_results=max_results
        )

        if response.data:
            print(f"Successfully retrieved {len(response.data)} tweets for @{username}:\n")
            for tweet in response.data:
                print("--- Tweet ---")
                print(f"ID: {tweet.id}")
                print(f"Text: {tweet.text}")
                print(f"Created At: {tweet.created_at}")
                if tweet.public_metrics:
                    print(f"Likes: {tweet.public_metrics.like_count}, Retweets: {tweet.public_metrics.retweet_count}")
                print("-" * 20)
                tweets_list.append(tweet.data) # Append the raw tweet data dictionary

            return tweets_list
        else:
            print(f"No tweets found for @{username} or user has no public tweets.")
            if response.errors:
                print("API Errors:", response.errors)
            return []

    except tweepy.TweepyException as e:
        print(f"Tweepy API Error retrieving user tweets: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred retrieving user tweets: {e}")
        return []

if __name__ == "__main__":
    # Replace with the Twitter username of the account you want to retrieve posts from
    target_username = "satyagnv" # Example: Official Twitter Developer account

    # Retrieve 5 recent posts from the specified account
    posts = get_account_holder_posts(target_username, max_results=5)

    if posts:
        print(f"\nRetrieved {len(posts)} posts from @{target_username}.")
        # You can now process the 'posts' list as needed
    else:
        print(f"\nFailed to retrieve posts from @{target_username}.")

    # Example for another user
    # target_username_2 = "NASA"
    # nasa_posts = get_account_holder_posts(target_username_2, max_results=3)