from django.shortcuts import render
from django.http import JsonResponse
from .forms import ScrapeForm
from .scraper import scrape_posts, setup_driver, login_to_linkedin
from .preprocessing import process_scraped_data
import threading
import uuid
from .post_generation import generate_complete_post
from .linkedin_poster import post_content_to_linkedin  # ✅ Import LinkedIn posting function
from django.views.decorators.csrf import csrf_exempt

scraping_status = {}

def start_scraping(keyword, max_posts, username, password, session_id):
    """Function to start scraping and store the processed file."""
    driver = setup_driver()

    try:
        login_to_linkedin(driver, username, password)

        filename = f"{keyword}_posts.csv"
        scrape_posts(keyword, max_posts, filename, driver)

        clean_file = process_scraped_data(keyword)

        if session_id in scraping_status:
            scraping_status[session_id].update({
                "status": "completed",
                "clean_file": clean_file
            })
    except Exception as e:
        scraping_status[session_id] = {"status": "error", "error": str(e)}

    finally:
        driver.quit()


def index(request):
    """Handles the scraping form submission."""
    if request.method == 'POST':
        form = ScrapeForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            max_posts = form.cleaned_data['max_posts']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            post_category = form.cleaned_data['post_category']

            session_id = str(uuid.uuid4())

            # ✅ Store username and password immediately
            scraping_status[session_id] = {
                "status": "in_progress",
                "post_category": post_category,
                "username": username,  # ✅ Ensures credentials are available
                "password": password
            }

            thread = threading.Thread(target=start_scraping, args=(keyword, max_posts, username, password, session_id))
            thread.start()
            return JsonResponse({"status": "started", "session_id": session_id})
    else:
        form = ScrapeForm()

    return render(request, 'scraper_app/index.html', {'form': form})


def check_status(request, session_id):
    """Check the status of the scraping process."""
    status_info = scraping_status.get(session_id, {"status": "unknown"})
    return JsonResponse(status_info)

def generate_post(request, session_id):
    """Generate a LinkedIn post using the processed file."""
    session_data = scraping_status.get(session_id, {})
    clean_file = session_data.get("clean_file")
    post_category = session_data.get("post_category")

    if clean_file:
        result = generate_complete_post(clean_file, post_category)
        try:
            return JsonResponse({"status": "success", "post": result})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "No clean file found for this session."})
@csrf_exempt
def post_to_linkedIn(request, session_id):
    """Post the generated LinkedIn post using Selenium."""
    print("Happening 1")
    if request.method == "POST":
        data = request.POST
        post_content = data.get("post")

        session_data = scraping_status.get(session_id, {})  # ✅ Now should always have credentials
        username = session_data.get("username")
        password = session_data.get("password")

        if not username or not password:
            return JsonResponse({"status": "error", "message": "Login credentials not found."})

        success, message = post_content_to_linkedin(username, password, post_content)

        if success:
            return JsonResponse({"status": "success", "message": "Successfully posted to LinkedIn!"})
        else:
            return JsonResponse({"status": "error", "message": message})

    return JsonResponse({"status": "error", "message": "Invalid request method."})

