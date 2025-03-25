# import openai
# import random
# from keybert import KeyBERT
# import pandas as pd

# # Set up OpenAI client
# client = openai.Client(api_key="sk-xxxxxxxxxxxxxxxxs")


# # Initialize KeyBERT for keyword extraction
# kw_model = KeyBERT()

# # Devticks Past Posts
# df = pd.read_csv('devticks_past_posts.csv')
# past_posts = df['post_content'].tolist()

# # Company description
# company_info = """
# Name: Devticks
# Overview:
# We are a team of expert full stack developers specialised in creating tailored solutions for clients all over the world. With over 10 years of experience in successfully delivering software solutions, we guarantee that you’ll find the best full-stack developers for your web development project. Our developers are highly communicative and are always willing to collaborate with clients and other team members.
# Our company offers a wide range of full-stack solutions, including:
# - Artificial Intelligence
# - Java Spring boot
# - AngularJS
# - Python/Django
# - Postgres
# - Flask
# - Git
# - Jest
# - Docker
# - Kubernetes
# - AWS

# Devticks provide cloud services to  global clients worldwide. We work in scrum agile development model.

# Website: https://devticks.com
# Phone: 03255831860
# Industry: Software Development
# Company size: 11-50 employees (15 associated members LinkedIn members who’ve listed Devticks as their current workplace on their profile.
# Headquarters: Wyoming, Casper
# Founded: 2022
# Specialties: Cloud Services, Docker, backend developement, RESTful API, MongoD, Postgres, Github, Kubernetes, React, DevOps, 
# Restful Apis, Java Spring boot, Aritificial Intelligence, Python, and Model Tuning
# """

# # Extract trending keywords from posts
# def extract_keywords_optimized(posts, num_keywords=15, top_n=4):
#     combined_text = " ".join(posts)
    
#     # Extract keywords from combined text (to capture overall trends)
#     global_keywords = set(kw[0] for kw in kw_model.extract_keywords(combined_text, top_n=num_keywords))
    
#     # Extract unique keywords per post
#     unique_keywords = set()
#     for post in posts:
#         unique_keywords.update(
#             kw[0] for kw in kw_model.extract_keywords(post, keyphrase_ngram_range=(1, 2), stop_words="english", top_n=top_n)
#         )
#     print("Keywords Done.............................")
#     return list(global_keywords | unique_keywords)  # Union of both sets


# #  Generate a LinkedIn post with AI

def generate_complete_post(file,category):
    print("""The Future of Intelligent Automation

AI is no longer just about responding to commands.

Agentic AI takes automation to the next level. These AI agents operate autonomously, make decisions, and adapt to their environment without constant human input.

Unlike traditional AI, Agentic AI learns, plans, and acts independently, making it a game-changer for industries like finance, healthcare, and e-commerce.

Key Features:
- Autonomous Execution – Functions without supervision
- Goal-Oriented Thinking – Works towards specific objectives
- Adaptive Learning – Improves over time
- Decision-Making Ability – Analyzes options and takes action

From automating workflows to self-learning AI systems, Agentic AI is shaping the future.

How do you see it transforming industries? 

Let’s discuss in the comments!

#AgenticAI #ArtificialIntelligence #AIInnovation #MachineLearning #Automation""")
          
#     print("Generating Post.............................")
#     data = pd.read_csv(file)
#     trending_posts = data['cleaned_content'].tolist()
#     keywords = extract_keywords_optimized(trending_posts, num_keywords=15, top_n=4)
#     prompt = f"""
#     Generate an engaging LinkedIn {category} post using the following keywords:
#     Keywords: {', '.join(keywords)}
#     Include a brief description of the company:
#     {company_info}
#     User’s Style & Tone:
#     Analyze user’s past posts to understand writing style & tone. Here are few past posts {past_posts}

#     Structure:
#     1. Start with a hook (a thought-provoking question or bold statement).
#     2. Integrate the keywords naturally into the content.
#     3. Add a company-specific statement to highlight our strengths.
#     4. End with a call-to-action (e.g., "What are your thoughts?" or "Let's discuss!").
#     Ensure the post story must be completed within 120-150 words, there should be not incomplete sentence (max_tokens problem) and it should be written in the first person.
#     """
#     try:
#         # Initial request with token limit
#         response = client.chat.completions.create(
#             model="gpt-4.5-preview",
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens= 190  # Aim for the middle of the range (130-150)
#         )
        
#         output = response.choices[0].message.content.strip()
#         print("Post is Generated............................")
        
#         return output
#         # return "Dummy Generated Content"
    
#     except Exception as e:
#         print(f"Error: {e}")
#         return None
    

# post = generate_complete_post()
# print(post)