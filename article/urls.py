from django.urls import path
from . import views

app_name = 'article'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    path('article-list/', views.ArticleListView.as_view(), name="article_list"),
    path('article-detail/<int:pk>/', views.ArticleDetailView.as_view(), name="article_detail"),
    path('article-create/', views.ArticleCreateView.as_view(), name="article_create"),
    path('article-update/<int:pk>/', views.ArticleUpdateView.as_view(), name="article_update"),
]

 