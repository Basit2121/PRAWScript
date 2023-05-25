import praw
import random
import time

# Read the login credentials from the file
with open("Login.txt", "r") as file:
    credentials = file.read()

# Split the credentials into lines
lines = credentials.split("\n")

# Create a dictionary to store the credentials
login_info = {}

# Iterate over the lines and extract the variable name and value
for line in lines:
    if line.strip():
        var_name, var_value = line.split("=")
        var_name = var_name.strip()
        var_value = var_value.strip().strip("'")

        # Add the variable to the dictionary
        login_info[var_name] = var_value

# Path to the text file containing subreddit names
subreddits_file = 'Subreddits.txt'
# Path to the text file containing key phrases
key_phrases_file = 'key_phrases.txt'

def upload_image_to_subreddits(subreddits, key_phrases_file):
    # Initialize the Reddit API

    reddit = praw.Reddit(
        client_id=login_info['client_id'],
        client_secret=login_info['client_secret'],
        username=login_info['username'],
        password=login_info['password'],
        user_agent=login_info['user_agent']
    )

    # Read the key phrases from the file
    with open(key_phrases_file, 'r', encoding='utf-8') as file:
        key_phrases = [line.strip() for line in file if line.strip()]
    
    sleep_intervals = input("Enter Wait time between each post (in minutes) : ")

    # Iterate over the subreddit info
    for subreddit_info in subreddits:
        subreddit_name, title, flair, image_path = subreddit_info

        subreddit = reddit.subreddit(subreddit_name)

        minutes = int(sleep_intervals)
        seconds = minutes * 60
        retry_count = 0
        while retry_count < 5:
            try:
                # Select a random key phrase
                selected_phrase = random.choice(key_phrases)

                # Construct the final title
                final_title = f"{title} {selected_phrase}"
                # Upload the image to the subreddit
                subreddit.submit_image(title=final_title, image_path=image_path, flair_id=flair)
                print(f"Image uploaded to r/{subreddit_name}")
                print(f"Waiting for {minutes} minutes...")
                time.sleep(seconds)
                break  # Upload successful, exit the retry loop
            except Exception as e:
                retry_count += 1
                print(f"Upload with Title: {final_title} attempt {retry_count} failed: r/{subreddit_name}")
                print(f"Error: {e}")

                # Generate a new title for the next attempt
                selected_phrase = random.choice(key_phrases)
                final_title = f"{title} {selected_phrase}"

        # If all retry attempts failed, print an error message
        if retry_count == 5:
            print(f"Upload failed after 5 attempts: r/{subreddit_name}")
            print("Failed Upload Details Saved to Failed_uploads.txt")
            print("Moving on to next subreddit...")

            # Save the failed upload details to a text file
            with open("Failed_uploads.txt", "a") as file:
                file.write(f"{subreddit_name}:{title}:{flair}:{image_path}\n")

# Read subreddit names, titles, flairs, and image paths from the file
subreddits = []
with open(subreddits_file, 'r') as file:
    for line in file:
        line = line.strip()
        if ':' in line:
            subreddit_name, title, flair, image_path = line.split(':', 3)
            subreddits.append((subreddit_name.strip(), title.strip(), flair.strip(), image_path.strip()))

# Call the function to upload the image to subreddits
upload_image_to_subreddits(subreddits, key_phrases_file)
