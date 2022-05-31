from django.shortcuts import render
from django.views import generic
from .forms import InquiryForm, ArticleCreateForm
import logging
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article

# Create your views here.

logger = logging.getLogger(__name__)

class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('article:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request,'メッセージを送信しました')
        logger.info(('Inquiry sent by {}'.format(form.cleaned_data['name'])))
        return super().form_valid(form)
        
class ArticleListView(LoginRequiredMixin, generic.ListView):
    model = Article
    template_name = 'article_list.html'
    paginate_by = 4

    def get_queryset(self):
        # articles = Article.objects.filter(user=self.request.user).order_by('-created_at')
        articles = Article.objects.order_by('-created_at')
        return articles

class ArticleDetailView(LoginRequiredMixin, generic.DetailView):
    model = Article
    template_name = 'article_detail.html'
    pk_url_kwarg = 'pk'

class ArticleCreateView(LoginRequiredMixin, generic.CreateView):
    model = Article
    template_name = 'article_create.html'
    form_class = ArticleCreateForm
    success_url = reverse_lazy('article:article_list')

    def form_valid(self, form):
        article = form.save(commit=False)
        article.user = self.request.user
        article.save()
        # messages.success(self.request, '記事を投稿しました')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # messages.error(self.request, '記事の投稿に失敗しました')
        return super().form_invalid(form)

class ArticleUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Article
    template_name = 'article_update.html'
    form_class = ArticleCreateForm

    def get_success_url(self):
        return reverse_lazy('article:article_detail', kwargs={'pk':self.kwargs['pk']})
    
    def form_valid(self, form):
        messages.success(self.request, '記事を更新しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '記事の更新に失敗しました')
        return super().form_invalid(form)

