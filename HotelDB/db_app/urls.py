from django.urls import path
from db_app import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'db_app'

urlpatterns = [
    # Гостевая страница:
    path('guest/', views.guest_view, name='guest_rooms'),
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    # JWT и регистрация:
    path('api/register/', views.RegisterView.as_view(), name='api_register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', views.UserView.as_view(), name='api_user'),
    path('', views.list_tables, name='list_tables'),
    path('count_bookings/', views.count_bookings, name='count_bookings'),
    path('bookings/', views.view_bookings, name='view_bookings'),
    path('<str:table_name>/', views.view_table, name='view_table'),
    path('<str:table_name>/edit/<int:key>/', views.edit_record, name='edit_record'),
    path('<str:table_name>/delete/<int:key>/', views.delete_record, name='delete_record'),
    path('add/<str:table_name>', views.add_record, name='add_record'),
    path('guest/room/<int:room_id>/', views.guest_room_detail, name='guest_room_detail'),
    path('guest/book/<int:room_id>/', views.guest_book_room, name='guest_book_room'),
    path('guest/success/<int:room_id>/', views.guest_booking_success, name='guest_booking_success'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)