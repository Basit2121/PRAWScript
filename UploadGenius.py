import praw
import random
import time
import pyfiglet
from termcolor import colored
import os

def convert_to_word_art(text):
    ascii_art = pyfiglet.figlet_format(text, font="slant")
    colored_art = colored(ascii_art, "green")
    print(colored_art)

# Main program
input_string = "UploadGenius"
convert_to_word_art(input_string)

desclaimer = "This is a Product of UploadGenius.\nCopyright (c) 2023 UploadGenius.\n"

colored_desclaimer= colored(desclaimer, "red")

print(colored_desclaimer)

import os

# Check if Login.txt file exists
if os.path.isfile("Login.txt"):
    print("Logged In.\n")

else:
    client_id = input("Enter client ID: ")
    client_secret = input("Enter client secret: ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    user_agent = username

    # Save the credentials in a file
    with open("Login.txt", "w") as file:
        file.write(f"client_id = '{client_id}'\n")
        file.write(f"client_secret = '{client_secret}'\n")
        file.write(f"username = '{username}'\n")
        file.write(f"password = '{password}'\n")
        file.write(f"user_agent = '{user_agent}'\n")

    print("Logged In.\n")

while True:

    choice1 = "ENTER 1 TO GENERATE FLAIR ID'S"
    choice2 = "ENTER 2 TO UPLOAD IMAGES TO SUBREDDIT'S"
    colored_choice1 = colored(choice1, "green")
    colored_choice2 = colored(choice2, "green")
    print(colored_choice1)
    print(colored_choice2)

    choice = input("--> ")

    if choice == '2':
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
        key_phrases_file = 'KeyPhrases.txt'

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
                
            
            print(colored("\n1. MAKE SURE THAT THE LOGIN INFORMATION INSIDE THE Login.txt FILE IS CORRECT BEFORE PROCEEDING.\n--> You can find The Client ID, Client Secret for you Reddit Account by Following this Link : https://youtu.be/4Lmfgw4RZCM\n2. MAKE SURE THAT THE FORMAT IN Subreddits.txt  FILE IS CORRECT.\n3. THE CORRECT FORMAT IS -> subredditname:title:flareid:imagename\n4. THE IMAGES THAT ARE TO BE UPLOADED SHOULD BE IN THE assets FOLDER AND IT should be in PNG form.\n5. The Title of the post is randomly selected from a pool of Phrases that are inside the KeyPhrases.txt file + the title that you enter in the Subreddits.txt File.\n--> You Can add more Phrases, one in each line or remove phrases that you want to remove from the pool of choices. You can also keeping the KeyPhrases.txt Empty if you do not want a random Title.\n","green"))

            sleep_intervals = input(colored("Enter Wait time between each post (in minutes) : ","green"))

            # Iterate over the subreddit info
            for subreddit_info in subreddits:
                subreddit_name, title, flair, image_path = subreddit_info

                subreddit = reddit.subreddit(subreddit_name)

                minutes = int(sleep_intervals)
                seconds = minutes * 60
                retry_count = 0
                while retry_count < 5:
                    try:
                        # Select a random key phrase if available
                        if key_phrases:
                            selected_phrase = random.choice(key_phrases)
                            final_title = f"{title} {selected_phrase}"
                        else:
                            final_title = title

                        # Upload the image to the subreddit
                        subreddit.submit_image(title=final_title, image_path=image_path, flair_id=flair)
                        print(colored(f"Image uploaded to r/{subreddit_name}",'green'))
                        print(f"Waiting for {minutes} minutes...")
                        time.sleep(seconds)

                        break  # Upload successful, exit the retry loop
                    except Exception as e:
                        retry_count += 1
                        print(f"Upload with Title: {final_title} attempt {retry_count} failed: r/{subreddit_name}")
                        print(f"Error: {e}")
                        time.sleep(2)

                        # Generate a new title for the next attempt
                        selected_phrase = random.choice(key_phrases)
                        final_title = f"{title} {selected_phrase}"

                # If all retry attempts failed, print an error message
                if retry_count == 5:
                    print(colored(f"Upload failed after 5 attempts: r/{subreddit_name}",'red'))
                    print(colored("Failed Upload Details Saved to Failed_uploads.txt",'red'))
                    print(colored("Moving on to next subreddit...",'green'))

                    # Save the failed upload details to a text file
                    with open("Failed_uploads.txt", "a") as file:
                        file.write(f"Failed Uploads -> {subreddit_name}:{title}:{flair}:{image_path}\n")

        # Read subreddit names, titles, flairs, and image paths from the file
        subreddits = []
        with open(subreddits_file, 'r') as file:
            for line in file:
                line = line.strip()
                if ':' in line:
                    subreddit_name, title, flair, image_filename = line.split(':', 3)
                    image_filename = image_filename.strip()
                    image_path = os.path.join('assets', image_filename)
                    image_path, image_extension = os.path.splitext(image_path)
                    image_extension = image_extension.lower()

                    # Check if the file extension is missing or not .jpg or .png
                    if not image_extension or image_extension not in ['.jpg', '.png']:
                        image_extension = '.png'  # Default to .jpg if the extension is missing or invalid

                    image_path += image_extension
                    subreddits.append((subreddit_name.strip(), title.strip(), flair.strip(), image_path.strip()))

        # Call the function to upload the image to subreddits
        upload_image_to_subreddits(subreddits, key_phrases_file)
        

    elif choice == '1':
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
        username = 'basitcarry'
        password = 'Basit24237'
        user_agent = 'basitcarry'
        subreddit_name=input(colored("Enter Subreddit Name : ", "green"))

        # Call the function to save the flair info
        save_flair_info(subreddit_name, client_id, client_secret, user_agent, username, password)

    elif choice != '1' or '2':
        print(colored("Invalid Choice. Intresting...\n",'red'))
