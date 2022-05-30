from django.shortcuts import render
from django.views import generic
from .forms import InquiryForm
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
    paginate_by = 20

    def get_queryset(self):
        # articles = Article.objects.filter(user=self.request.user).order_by('-created_at')
        articles = Article.objects.order_by('-created_at')
        return articles

class ArticleDetailView(LoginRequiredMixin, generic.DetailView):
    model = Article
    template_name = 'article_detail.html'
    pk_url_kwarg = 'pk'
