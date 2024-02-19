import datetime

from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View, generic
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from .models import Museum, Artifact, Category
from users.models import UserProfile


class IndexView(View):
    def get(self, request):
        num_museums = Museum.objects.all().count()
        num_artworks = Artifact.objects.all().count()
        num_categories = Category.objects.all().count()
        num_user_profiles = UserProfile.objects.all().count()

        return render(
            request, 'index.html',
            context={
                'num_museums': num_museums,
                'num_artworks': num_artworks,
                'num_categories': num_categories,
                'num_user_profiles': num_user_profiles,
            },
        )


class MuseumListView(View):
    def get(self, request):
        museums = Museum.objects.all()
        return render(request, 'museum_list.html', {'museums': museums})


class ArtworkListView(View):
    def get(self, request):
        artworks = Artifact.objects.all()
        return render(request, 'artwork_list.html', {'artworks': artworks})


class ArtworksByCategoryView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        artworks = Artifact.objects.filter(categories=category)
        return render(request, 'artworks_by_category.html', {'category': category, 'artworks': artworks})


class AboutUsView(View):
    def get(self, request):
        return render(request, 'catalog/aboutUs.html')


class ContactUsView(View):
    def get(self, request):
        return render(request, 'catalog/contactUs.html')


class SearchMuseumView(View):
    def get(self, request):
        # Add logic to handle museum search functionality
        return render(request, 'catalog/searchMuseum.html')


class ExploreView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/explore.html'

    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artifacts = Artifact.objects.all().select_related('museum')
        museums = Museum.objects.all()

        # Get search parameters from the query string
        search_query = self.request.GET.get('search', '')
        origin_filter = self.request.GET.get('origin', '')

        # Apply filters based on user input
        if search_query:
            artifacts = artifacts.filter(name__icontains=search_query) | artifacts.filter(
                description__icontains=search_query)
        if origin_filter:
            artifacts = artifacts.filter(origin__icontains=origin_filter)

        # Add century filter
        century_filter = self.request.GET.get('century', '')
        if century_filter:
            artifacts = artifacts.filter(date_created__gte=get_start_of_century(int(century_filter)),
                                         date_created__lt=get_start_of_century(int(century_filter) + 100))

        # Add this line to filter out artifacts without images
        artifacts = artifacts.exclude(image__exact='')

        context['artifacts'] = artifacts
        context['museums'] = museums
        context['century_filter'] = century_filter

        return context


class FilterResultsView(generic.ListView):
    def get(self, request):
        # Retrieve artifacts filtered by century from the query string
        century_filter = request.GET.get('century', '')

        # Check if century_filter is not empty
        if century_filter:
            # Filter artifacts based on the century field
            artifacts = Artifact.objects.filter(century=century_filter)

            # Pass the filtered artifacts to the template
            context = {'artifacts': artifacts, 'century_filter': century_filter}
            return render(request, 'catalog/explore_results.html', context)
        else:
            # Handle the case where no century filter is provided
            return render(request, 'catalog/explore.html')


class GetArtifactTitleView(View):
    def get(self, request, artifact_id):
        artifact = get_object_or_404(Artifact, pk=artifact_id)
        return JsonResponse({'title': artifact.title})


def get_start_of_century(century):
    return datetime.datetime(century, 1, 1)


# login
def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("index.html")

    context = {'loginform': form}
    return render(request, 'users.html', context=context)


@login_required(login_url="login")
def dashboard(request):
    return render(request, 'registration/login.html')


def user_logout(request):
    auth.logout(request)
    return redirect("")


class ArtifactDetailsView(DetailView):
    model = Artifact
    template_name = 'catalog/artifact_detail.html'
    context_object_name = 'artifact'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class MuseumDetailView(View):
    template_name = 'catalog/museum_detail.html'

    def get(self, request, pk):
        museum = get_object_or_404(Museum, pk=pk)
        return render(request, self.template_name, {'museum': museum})