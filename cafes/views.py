from allauth.account.views import login, LoginView, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Restaurants, Reviews, Category, Rating, Record
from .forms import ReviewForms, RatingForm, CustomUserCreationForm, RecordForm

class CategoriesSideBar:
    """Category list on sidebar"""
    def get_category(self):
        return Category.objects.all()

class RestaurantView(CategoriesSideBar, ListView):
    """Restaurant list"""
    model = Restaurants
    queryset = Restaurants.objects.filter(draft=False)
    paginate_by = 3
    template_name = "cafes/restaurants_list.html"


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
        return context

class RestaurantDetailView(CategoriesSideBar, View):
    """Detailed info"""

    def get(self, request, slug):
        cafe = get_object_or_404(Restaurants, url=slug)  # Используем get_object_or_404
        star_form = RatingForm()
        return render(request, "cafes/restaurants_detail.html", {"cafes": cafe, "star_form": star_form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context

def add_review(request, restaurant_id):
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            text = request.POST.get('text')

            restaurant = get_object_or_404(Restaurants, id=restaurant_id)
            restaurant.reviews_set.create(name=name, email=email, text=text)
            return redirect(restaurant.get_absolute_url())

class FilterCafesView(CategoriesSideBar, ListView):
    """Filter cafes"""

    paginate_by = 3

    def get_queryset(self):
        queryset = Restaurants.objects.filter(
            Q(category__in=self.request.GET.getlist("category"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["category"] = ''.join([f"category={x}&" for x in self.request.GET.getlist("category")])
        return context

class AddStarRating(View):
    """Add star rating"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            star = form.cleaned_data['star']
            restaurant_id = request.POST.get("restaurant")
            restaurant = Restaurants.objects.get(id=restaurant_id)

            # Обновляем или создаём запись о рейтинге
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                restaurant=restaurant,
                defaults={'star': star}
            )

            return redirect(restaurant.get_absolute_url())
        return redirect(request.META.get('HTTP_REFERER', '/'))

class Search(ListView):
    """Search"""

    paginate_by = 3

    def get_queryset(self):
        return Restaurants.objects.filter(name__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context


def register(request):
    """User registration"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            login(request, user)  # Automatically log in the user
            return redirect('/')  # Redirect to the homepage
    else:
        form = CustomUserCreationForm()
    return render(request, "cafes/register.html", {"form": form})


# Представление для входа
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("/")  # Перенаправление на главную страницу
    else:
        form = AuthenticationForm()
    return render(request, "cafes/login.html", {"form": form})

# Представление для выхода
def logout_view(request):
    """Выход пользователя и перенаправляет на страницу logout."""
    context = {
        "username": request.user.username,
        "email": request.user.email,
        "is_admin": request.user.is_staff,
    }
    logout(request)
    return render(request, "cafes/logout.html", context)


@staff_member_required(login_url="/")
def admin_panel_redirect(request):
    """Перенаправляет на панель администратора, если пользователь является администратором."""
    return redirect("/admin/")

# Проверка доступа: только администратор может создавать, обновлять, удалять записи
def is_admin(user):
    return user.is_staff


# ListView: отображение всех записей
class RecordListView(ListView):
    model = Restaurants
    template_name = "cafes/record_list.html"
    context_object_name = "records"

    def get_queryset(self):
        return Restaurants.objects.all()


# DetailView: просмотр одной записи
class RecordDetailView(DetailView):
    model = Record
    template_name = "cafes/record_detail.html"
    context_object_name = "record"


# CreateView: создание записи (только для администратора)
@method_decorator(user_passes_test(is_admin, login_url="/"), name="dispatch")
class RecordCreateView(CreateView):
    model = Restaurants
    fields = ["name", "street", "phone", "types", "category", "mainPhoto", "description", "url", "draft"]
    template_name = "cafes/record_form.html"
    success_url = reverse_lazy("crud_list")


# UpdateView: обновление записи (только для администратора)
@method_decorator(user_passes_test(is_admin, login_url="/"), name="dispatch")
class RecordUpdateView(UpdateView):
    model = Restaurants
    fields = ["name", "street", "phone", "types", "category", "mainPhoto", "description", "url", "draft"]
    template_name = "cafes/record_form.html"
    success_url = reverse_lazy("crud_list")


# DeleteView: удаление записи (только для администратора)
@method_decorator(user_passes_test(is_admin, login_url="/"), name="dispatch")
class RecordDeleteView(DeleteView):
    model = Restaurants
    template_name = "cafes/record_confirm_delete.html"
    success_url = reverse_lazy("crud_list")


@csrf_exempt
def update_drafts(request):
    if request.method == "POST":
        draft_ids = request.POST.getlist("drafts")  # Получаем ID записей, которые должны быть черновиками
        all_restaurants = Restaurants.objects.all()

        # Обновляем статус черновиков
        for restaurant in all_restaurants:
            restaurant.draft = str(restaurant.id) in draft_ids
            restaurant.save()

        return HttpResponseRedirect(reverse("crud_list"))
