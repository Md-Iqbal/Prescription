from django.urls import path, include
from . import views
from .views import  EditProfile

app_name = 'patient'

urlpatterns = [
    path('', views.patientHomeView, name='patientHome'),
    path('postViews', views.postViews, name='postViews'),
    path('viewed', views.viewPost, name='view_ignore_Post'),
    path("delete/<int:ID>", views.deletePostView, name='deletePostView'),
    path("<str:username>", views.userProfileView, name='userProfileView'),
    path("patient/follow/<str:username>", views.follow, name='follow'),
    path("search/", views.SearchUserView.as_view(), name='search_user'),
    path("<str:username>/edit", EditProfile.as_view(), name="EditProfile"),
    path("lab_report/", views.LabReportView.as_view(), name='LabReportView'),
    path("prescription/", views.PrescriptionView.as_view(), name='PrescriptionView'),
    path("drug_list/", views.DrugListView.as_view(), name='DrugListView'),
    path("disease/", views.AllDiseaseView.as_view(), name='AllDiseaseView'),
    path("appointment/", views.AppointmentView.as_view(), name='AppointmentView'),
    path("checkout/", views.CheckoutView.as_view(), name='CheckoutView'),
    path("documentation/", views.Documentation.as_view(), name='Documentation'),

]

