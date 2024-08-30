import requests
import csv
import time
import os

# Reddit API requires a user agent
headers = {"User-agent": "Mozilla/5.0"}
after = None

subreddit = input("Enter the Subreddit without r/ to be Scraped : ")

# Defining key names (from scraper) in fieldnames variable
fieldnames = [
    "title",
    "selftext",
    "subreddit",
    "link_flair_text",
    "num_comments",
    "downs",
    "is_crosspostable",
    "view_count",
    "ups",
    "url",
    "is_video",
    "num_crossposts",
    "subreddit_subscribers",
    "author",
    "treatment_tags",
    "all_awardings",
    "media",
]

os.makedirs(os.path.join(os.getcwd(), "scraped"), exist_ok=True)

# Writes to a CSV called 'data.csv' in Python
with open(f"scraped/{subreddit}.csv", "w", newline="", encoding="utf-8") as file:
    file_writer = csv.DictWriter(file, fieldnames=fieldnames)
    file_writer.writeheader()
    count = 1
    while True:  # Continue looping until there's no more data
        url = f"https://www.reddit.com/r/{subreddit}/.json"  # Replace with the subreddit URL you want to scrape
        if after:
            url += "?after=" + after
        r = requests.get(url, headers=headers)
        data = r.json()  # Parse JSON data

        # If there's no more data, break the loop
        if "data" not in data or "children" not in data["data"]:
            break

        # Adds the scraped data (fieldnames) into rows in our CSV
        for post in data["data"]["children"]:
            row = {
                "title": post["data"]["title"],
                "link_flair_text": post["data"]["link_flair_text"],
                "selftext": post["data"]["selftext"],
                "subreddit": post["data"]["subreddit"],
                "media": post["data"]["media"],
                "is_video": post["data"]["is_video"],
                "num_crossposts": post["data"]["num_crossposts"],
                "subreddit_subscribers": post["data"]["subreddit_subscribers"],
                "url": post["data"]["url"],
                "num_comments": post["data"]["num_comments"],
                "author": post["data"]["author"],
                "treatment_tags": post["data"]["treatment_tags"],
                "all_awardings": post["data"]["all_awardings"],
                "is_crosspostable": post["data"]["is_crosspostable"],
                "view_count": post["data"]["view_count"],
                "downs": post["data"]["downs"],
                "ups": post["data"]["ups"],
            }
            file_writer.writerow(row)
            print(f"    Total Posts Scraped : {count}",end="\r", flush=True)
            count +=1

        after = data["data"]["after"]

        if not after:
            break  # Break the loop if there's no more pages

        time.sleep(2)  # Sleep for 2 seconds to avoid hitting Reddit's rate limit

file.close()
