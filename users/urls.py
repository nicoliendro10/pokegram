from django.urls import path
from users import views
from users.views import UserDetailView

urlpatterns = [
    path(
        route = 'login/',
        view= views.login_view, 
        name='login'
    ),
    path(
        route = 'logout/',
        view= views.logout_view, 
        name='logout'
    ),
    path(
        route = 'signup/',
        view= views.signup, 
        name='signup'
    ),
    path(
        route = 'me/profile/',
        view= views.update_profile,
        name='profile'
    ),
    path(
        route='<str:username>/',
        view=UserDetailView.as_view(template_name='users/detail.html'),
        name='detail'
    ),
]


    