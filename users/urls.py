
from django.urls import path
from .views import (
    PatientListView, PatientDetailView, PatientCreateView, PatientUpdateView, PatientDeleteView,
    AssignAgentView, CategoryListView, CategoryDetailView, CategoryUpdateView,
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView, PatientJsonView, 
    FollowUpCreateView, FollowUpUpdateView, FollowUpDeleteView
)

app_name = "users"

urlpatterns = [
    path('', PatientListView.as_view(), name='patient-list'),
    path('json/', PatientJsonView.as_view(), name='patient-list-json'),
    path('<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('<int:pk>/update/', PatientUpdateView.as_view(), name='patient-update'),
    path('<int:pk>/delete/', PatientDeleteView.as_view(), name='patient-delete'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
    path('<int:pk>/category/', CategoryUpdateView.as_view(), name='patient-category-update'),
    path('<int:pk>/followups/create/', FollowUpCreateView.as_view(), name='patient-followup-create'),
    path('followups/<int:pk>/', FollowUpUpdateView.as_view(), name='patient-followup-update'),
    path('followups/<int:pk>/delete/', FollowUpDeleteView.as_view(), name='patient-followup-delete'),
    path('create/', PatientCreateView.as_view(), name='patient-create'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('create-category/', CategoryCreateView.as_view(), name='category-create'),
]