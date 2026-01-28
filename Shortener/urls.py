from django.urls import path , include
from .views import(CreateShortLinkView,RedirectAndTrack,LinkStats,CodeExists,HomePage)

urlpatterns = [
    path("", HomePage.as_view(), name="home"), 
    path("api/links/", CreateShortLinkView.as_view()),
    path("api/links/<str:code>/stats/",LinkStats.as_view()),
    path("api/links/<str:code>/available/",CodeExists.as_view()),
    path("<str:code>/",RedirectAndTrack.as_view()),

]