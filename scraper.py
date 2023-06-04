import requests
import csv
import time

# reddit api requires a user agent
headers = {'User-agent': 'Mozilla/5.0'}
after = None

# defining key names (from scraper) in fieldnames variable
fieldnames = ['title', 'selftext', 'subreddit', 'author_flair_text', 'num_comments', 'downs',
              'is_crosspostable', 'view_count', 'ups', 'url', 'is_video', 'num_crossposts', 'subreddit_subscribers',
              'author', 'treatment_tags', 'all_awardings', 'media']

# writes to a csv called 'data.csv' in python
with open('data.csv', 'w', newline='') as file:
    file_writer = csv.DictWriter(file, fieldnames=fieldnames)
    file_writer.writeheader()

    for _ in range(4):  # Loop 4 times to get 100 posts, 25 each time
        url = 'https://www.reddit.com/r/CatAdvice/.json' # [add .json at end] replace with the subreddit url you want to scrape
        if after:
            url += '?after=' + after
        r = requests.get(url, headers=headers)
        data = r.json()  # Parse JSON data

# Adds the scraped data (fieldnames) into rows in our csv
        for post in data['data']['children']:
            row = {'title': post['data']['title'],
                   'author_flair_text': post['data']['author_flair_text'],
                   'selftext': post['data']['selftext'],
                   'subreddit': post['data']['subreddit'],
                   'media': post['data']['media'],
                   'is_video': post['data']['is_video'],
                   'num_crossposts': post['data']['num_crossposts'],
                   'subreddit_subscribers': post['data']['subreddit_subscribers'],
                   'url': post['data']['url'],
                   'num_comments': post['data']['num_comments'],
                   'author': post['data']['author'],
                   'treatment_tags': post['data']['treatment_tags'],
                   'all_awardings': post['data']['all_awardings'],
                   'is_crosspostable': post['data']['is_crosspostable'],
                   'view_count': post['data']['view_count'],
                   'downs': post['data']['downs'],
                   'ups': post['data']['ups']}
            file_writer.writerow(row)

        after = data['data']['after']

        time.sleep(2)  # sleep for 2 seconds to avoid hitting Reddit's rate limit

file.close()