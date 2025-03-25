import numpy as np
import pandas as pd
import re
import sqlite3

# Improved cleaning function
def clean_post_content(content):
    if pd.isna(content):
        return ""  # Handle null values
    
    content = content.lower()  # Lowercase the text

    # Remove special characters, emojis, and bullet points
    content = re.sub(r'[^\w\s.,?!-]', '', content)

    # Remove emojis and other symbols (e.g., ✅, ❤️)
    content = re.sub(r'[^\x00-\x7F]+', '', content)  

    # Normalize multiple spaces (spaces, tabs, newlines)
    content = re.sub(r'\s+', ' ', content)

    # Trim whitespace
    content = content.strip()

    # Fix punctuation spacing
    content = re.sub(r'\s+([?.!,-])', r'\1', content)

    return content

def process_scraped_data(keyword):
    # Connect to SQLite database
    conn = sqlite3.connect('db.sqlite3')

    # Ensure keyword matches the table format
    keyword = keyword.replace(" ", "_").lower()

    # Fetch rows from the dynamically named table
    query = f"SELECT * FROM scraped_posts_{keyword}"
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # Apply cleaning function
    df['cleaned_content'] = df['content'].apply(clean_post_content)

    # Display original vs cleaned content
    # print(df[['content', 'cleaned_content']].head())

    # Save cleaned data (optional)
    df.to_csv(f'cleaned_{keyword}_posts.csv', index=True)
    return f'cleaned_{keyword}_posts.csv'

    # print(f"✅ Data cleaned and saved for keyword: {keyword}")

