from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .forms import InquiryForm, ArticleCreateForm, CommentCreateForm
import logging
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article, Comment

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
        
class ArticleListView(generic.ListView):
    model = Article
    template_name = 'article_list.html'
    paginate_by = 20

    def get_queryset(self):
        articles = Article.objects.order_by('-created_at')
        return articles

def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    comments = Comment.objects.filter(commented_to=article_id).all()
    comment_form = CommentCreateForm()

    return render(request, "article_detail.html", {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
    })

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
        # messages.success(self.request, '記事を更新しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        # messages.error(self.request, '記事の更新に失敗しました')
        return super().form_invalid(form)

@login_required
def comment_new(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    form = CommentCreateForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.commented_to = article
        comment.commented_by = request.user
        comment.save()
        # messages.add_message(request, messages.SUCCESS,
        #                      "コメントを投稿しました。")
    else:
        pass
        # messages.add_message(request, messages.ERROR,
        #                      "コメントの投稿に失敗しました。")
    return redirect('article:article_detail', article_id=article_id)
