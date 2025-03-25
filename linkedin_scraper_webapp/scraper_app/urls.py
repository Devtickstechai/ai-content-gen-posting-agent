from django.urls import path
from .views import index, check_status, generate_post,post_to_linkedIn

urlpatterns = [
    path('', index, name='index'),
    path("check_status/<str:session_id>/", check_status, name="check_status"),
    path("generate_post/<str:session_id>/", generate_post, name="generate_post"),   # ✅ Ensure it's here
    path("post_to_linkedin/<str:session_id>/", post_to_linkedIn, name="post_to_linkedin"), 
    # path("post_to_linkedin/", post_to_linkedin, name="post_to_linkedin"), 
]
