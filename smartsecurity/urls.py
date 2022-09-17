from django.urls import path
#from .views import Home, video_feed
from smartsecurity import views
from .views import RegiformView,home,gen,video_feed,UserListView, UserDetailView, RegiformView, UserDeleteView, UserUpdateView


urlpatterns = [
    path('',views.home, name="home"),
    path('video_feed/',views.video_feed,name="video_feed"),
    path('registration_form/',RegiformView.as_view(),name="registration_form"),
    path('user_list/',UserListView.as_view(),name="user_list"),
    path('user-details/<int:pk>/', UserDetailView.as_view(), name='user_details'),
    path('user-delete/<int:pk>/delete/', UserDeleteView.as_view(), name='userdelete'),
    path('user-update/<int:pk>/update/', UserUpdateView.as_view(), name='userupdate'),
    path('login/',views.loginPage, name="login"),
    path('registration_admin/',views.registrationPage, name="registration"),
    path('about_us',views.about_us, name="about_us"),
    path('logout/',views.logoutUser, name="logout"),
    path('table1/',views.table1,name="table1"),


]
