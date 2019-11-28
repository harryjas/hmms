from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('home/', views.index, name='index'),
    # /register/
    path('register/', views.register, name='register'),
    # /login/
    path('', views.login_user, name='login'),
    # /home/album/add/
    path('management/album/add/', views.create_meal, name='meal_add'),
    # /music/<album_id>/create_item/
    path('management/<int:meal_id>/create_item/', views.create_item, name='create_item'),
    # /music/<meal_id>/delete_item/<song_item>/
    path('management/<int:meal_id>/delete_item/<int:item_id>', views.delete_item, name='delete_item'),
    # /music/<meal_id>/
    path('management/<int:meal_id>/', views.detail, name='detail'),
    # /music/<meal_id>/delete_meal/
    path('management/<int:meal_id>/delete_meal/', views.delete_meal, name='delete_meal'),
    # /music/meal/<meal_id>/
    path('management/meal/<int:meal_id>/', views.update_meal, name='meal_update'),
    # /logout/
    path('logout/', views.logout_user, name='logout'),
    # /music/items/( )/
    path('management/items/<slug:filter_by>/', views.items, name='items'),
]
