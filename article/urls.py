from django.urls import path
from . import views

app_name = 'article'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    path('article-list/', views.ArticleListView.as_view(), name="article_list"),
    path('article-detail/<int:article_id>/', views.article_detail, name="article_detail"),
    path('article-create/', views.ArticleCreateView.as_view(), name="article_create"),
    path('article-update/<int:article_id>/', views.ArticleUpdateView.as_view(), name="article_update"),
    path('article-comment/<int:article_id>/', views.comment_new, name="comment_new"),
]

 