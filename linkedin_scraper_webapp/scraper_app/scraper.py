from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re
from urllib.parse import quote
from django.conf import settings
import os
chromedriver_path = "C:/Program Files/chromedriver-win64/chromedriver.exe"

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--enable-unsafe-webgl")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")  # Prevent resource issues
    options.add_argument("--no-sandbox")             # Run Chrome without sandbox
    options.add_argument("--remote-debugging-port=9222")  # Avoid DevTools error
    options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    driver = webdriver.Chrome(options=options)
    return driver

def login_to_linkedin(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "username")))

    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Sign in')]").click()

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "global-nav__me-photo")))
    print("✅ Successfully logged into LinkedIn")

def clean_post_content(content):
    content = re.sub(r'(#\w+|@\w+|http\S+|hashtag+|[\U00010000-\U0010ffff])', '', content)
    return content.replace("\n", " ").strip()

def extract_metadata(engagement, time):
    likes, comments, shares, timestamp = "0", "0", "0", "N/A"
    try:
        if isinstance(engagement, list) and engagement:
            engagement = engagement[0]

        try:
            likes_element = engagement.find_element(By.XPATH, ".//span[contains(@class, 'reactions-count')]")
            likes = likes_element.text if likes_element else "0"
        except:
            likes = "0"

        metadata_text = engagement.text.lower()
        comments_match = re.search(r'(\d+)\s*comment', metadata_text)
        shares_match = re.search(r'(\d+)\s*(share|repost)', metadata_text)

        comments = comments_match.group(1) if comments_match else "0"
        shares = shares_match.group(1) if shares_match else "0"

        timestamp_element = time.find_elements(By.XPATH, ".//span[contains(@class, 'update-components-actor__sub-description')]")
        clean_timestamp = timestamp_element[0].find_element(By.XPATH, ".//span[contains(@class, 'visually-hidden')]")
        timestamp = clean_timestamp.text.strip() if timestamp_element else "N/A"
    except Exception as e:
        print("Error extracting metadata:", e)

    return likes, comments, shares, timestamp

def scrape_posts(keyword, max_posts, filename,driver):
    search_url = f"https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords={quote(keyword)}&origin=FACETED_SEARCH&sid=Z0U"
    driver.get(search_url)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "update-components-text")))
    posts_data = []

    # Moving File to Media Root
    filename = os.path.join(settings.MEDIA_ROOT, filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Open CSV file for writing
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Post Content", "Author", "Likes", "Comments", "Shares", "Timestamp"])

        post_count = 0

        while len(posts_data) < max_posts:
            posts = driver.find_elements(By.CLASS_NAME, "update-components-text")
            actors = driver.find_elements(By.CLASS_NAME, "update-components-actor__title")
            engagement_containers = driver.find_elements(By.CLASS_NAME, "social-details-social-counts")
            time_container = driver.find_elements(By.CLASS_NAME, "update-components-actor__meta")

            for post, actor, eg_container, tm_container in zip(posts, actors, engagement_containers, time_container):
                try:
                    content = clean_post_content(post.text)
                    author = actor.find_element(By.XPATH, ".//span[contains(@class, 'visually-hidden')]").text

                    likes, comments, shares, timestamp = extract_metadata(eg_container, tm_container)

                    if content and not any(p['content'] == content for p in posts_data):
                        post_count += 1
                        post_data = {
                            "content": content,
                            "author": author,
                            "likes": likes,
                            "comments": comments,
                            "shares": shares,
                            "timestamp": timestamp
                        }
                        posts_data.append(post_data)

                        # Save each row immediately
                        writer.writerow([
                            post_data.get("content", "N/A"),
                            post_data.get("author", "N/A"),
                            post_data.get("likes", "0"),
                            post_data.get("comments", "0"),
                            post_data.get("shares", "0"),
                            post_data.get("timestamp", "N/A"),
                        ])

                        print(f"Post {post_count} extracted")

                    if len(posts_data) >= max_posts:
                        break

                except Exception as e:
                    print("Error extracting post:", e)

            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(5)

    print(f"Extracted {len(posts_data)} posts")
    save_posts_to_db(keyword, posts_data)
    return filename

from .models import create_dynamic_table

def save_posts_to_db(keyword, posts_data):
    DynamicPost = create_dynamic_table(keyword)

    # Clear existing data
    DynamicPost.objects.all().delete()

    # Insert new data
    for post in posts_data:
        DynamicPost.objects.create(
            content=post['content'],
            author=post['author'],
            likes=int(post['likes']),
            comments=int(post['comments']),
            shares=int(post['shares']),
            timestamp=post['timestamp']
        )

    print(f"✅ {len(posts_data)} posts saved to '{DynamicPost._meta.db_table}'")