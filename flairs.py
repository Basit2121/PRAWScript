import praw


def save_flair_info(subreddit_name, client_id, client_secret, user_agent, username, password):
    # Initialize the Reddit API client
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
        username=username,
        password=password
    )

    try:
        # Retrieve the subreddit
        subreddit = reddit.subreddit(subreddit_name)

        # Get the list of flairs
        flairs = subreddit.flair.link_templates

        # Extract the flair IDs and text
        flair_info = [{'id': flair['id'], 'text': flair['text']} for flair in flairs]

        # Save the flair info in a text file
        with open('flair_ids.txt', 'a', encoding='utf-8') as file:
            file.write(f"\n\nSubreddit: {subreddit_name}\n\n")
            for flair in flair_info:
                file.write(f"ID: {flair['id']} - Text: {flair['text']}\n")

        print("Flair IDs appended to flair_ids.txt file.")

    except praw.exceptions.RedditAPIException as e:
        print(f"An error occurred: {e}")


# Set up the credentials and parameters
client_id = 'XJauAx6ojQ442IOs9tlyFg'
client_secret = 'YWJHr2B3SJTr1MF9ljElwLLSAx0hjA'
username = ''
password = ''
user_agent = ''
subreddit_name=input("Enter Subreddit Name : ")

# Call the function to save the flair info
save_flair_info(subreddit_name, client_id, client_secret, user_agent, username, password)
