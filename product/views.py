from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Product
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (                 # generic способ выявления программ
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView
)


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'object_list'
    ordering = ['-created_date']

    def get_queryset(self, *args, **kwargs):
        qs = Product.objects.all()
        query = self.request.GET.get('q', None)
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query),
                Q(author__username__icontains=query)
            )
        return qs


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user              # юзер который отправляет
        return super().form_valid(form)                        # вызывает родительский класс


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        return context


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'image']
    template_name = 'product/product_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'product/product_confirm_delete.html'
    success_url = reverse_lazy('blog-home')

    # def get_success_url(self):
    #     return reverse('blog-home')
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



