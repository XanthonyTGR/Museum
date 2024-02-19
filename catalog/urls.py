from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('museums/', views.MuseumListView.as_view(), name='museum_list'),
    path('explore/', views.ExploreView.as_view(), name='explore'),
    path('artworks/', views.ArtworkListView.as_view(), name='artwork_list'),
    path('artworks/category/<int:category_id>/', views.ArtworksByCategoryView.as_view(), name='artworks_by_category'),
    path('explore_results/', views.FilterResultsView.as_view(), name='filter_results'),
    path('about_us/', views.AboutUsView.as_view(), name='about_us'),
    path('contact_us/', views.ContactUsView.as_view(), name='contact_us'),
    path('search_museum/', views.SearchMuseumView.as_view(), name='search_museum'),
    path('museum/<int:pk>/', views.MuseumDetailView.as_view(), name='museum_detail'),
    path('get_artifact_title/<int:artifact_id>/', views.GetArtifactTitleView.as_view(), name='get_artifact_title'),
    path('artifact/<int:pk>/', views.ArtifactDetailsView.as_view(), name='artifact_details'),
]