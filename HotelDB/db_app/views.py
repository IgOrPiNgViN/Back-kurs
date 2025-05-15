from django.shortcuts import render, redirect
from django.db import connection
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.forms import modelform_factory
from .models import *  # Импортируем все модели
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.views.generic import ListView
from django import forms
from .forms import GuestBookingForm
import uuid


EXCLUDED_TABLES = [
    'auth_user', 'auth_group', 'auth_permission', 'django_migrations', 
    'django_content_type', 'django_session', 'django_admin_log',
    'auth_group_permissions', 'auth_user_groups', 'auth_user_user_permissions'
]


def list_tables(request):
    """Вывод списка пользовательских таблиц в базе данных, исключая системные."""
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        all_tables = [row[0] for row in cursor.fetchall()]

    # Исключаем стандартные Django-таблицы
    user_tables = [table for table in all_tables if table not in EXCLUDED_TABLES]

    return render(request, 'db_app/list_tables.html', {'tables': user_tables})


def view_table(request, table_name):
    """Вывод данных из выбранной таблицы с пагинацией и названиями столбцов."""
    with connection.cursor() as cursor:
        # Получаем данные из выбранной таблицы
        cursor.execute(f"SELECT * FROM `{table_name}`;")
        rows = cursor.fetchall()

        # Получаем названия колонок (первый элемент из cursor.description)
        column_names = [desc[0] for desc in cursor.description]

    # Пагинация: 6 записей на страницу
    paginator = Paginator(rows, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "db_app/view_table.html",
        {
            "table_name": table_name,
            "columns": column_names,  # Передаем названия колонок в шаблон
            "page_obj": page_obj,  # Объект пагинации
        },
    )


def get_model_by_name(table_name):
    # Используем Python reflection, чтобы найти модель по имени
    model_name = ''.join(tmp.capitalize() for tmp in table_name.split('_'))
    try:
        model = globals()[model_name]  # Получаем модель по имени
        return model
    except KeyError:
        raise Http404("Модель не найдена для таблицы: " + table_name, 'model_name:', model_name)


@login_required
def edit_record(request, table_name, key):
    # Получаем модель по имени таблицы
    model = get_model_by_name(table_name)

    print('afasdf', model)
    record = get_object_or_404(model, pk=key)


    # Создаем форму для этой модели
    form_class = modelform_factory(model, exclude=[model._meta.pk.name])
    form = form_class(instance=record)

    if request.method == 'POST':

        form = form_class(request.POST, request.FILES, instance=record)  # Обрабатываем файлы с request.FILES
        
        if form.is_valid():
            form.save()   
            return redirect('db_app:view_table', table_name=table_name)
    
    context = {
        'form': form,
        'table_name': table_name,
        'record': record,
    }
    return render(request, 'db_app/edit_record.html', context)

@login_required
def delete_record(request, table_name, key):
    # Получаем модель по имени таблицы
    model = get_model_by_name(table_name)

    # Определяем запись
    record = model.objects.filter(pk=key).first()

    if not record:
        raise Http404("Запись не найдена")

    # Удаляем запись
    if request.method == 'POST':
        record.delete()
        return redirect('db_app:view_table', table_name=table_name)

    # Преобразуем запись в словарь
    record_dict = model_to_dict(record)

    # Передаём запись в шаблон для отображения
    return render(request, 'db_app/confirm_delete.html', {
        'record': record_dict,  # Передаем словарь напрямую
        'table_name': table_name
    })


@login_required
def add_record(request, table_name):
    model = get_model_by_name(table_name)
    if table_name == 'bookings':
        form_class = modelform_factory(
            model,
            exclude=['id'],
            widgets={
                'check_in_date': forms.DateInput(attrs={'type': 'date'}),
                'check_out_date': forms.DateInput(attrs={'type': 'date'}),
            }
        )
    else:
        form_class = modelform_factory(model, exclude=['id'])
    form = form_class()

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('db_app:view_table', table_name=table_name)

    context = {'form': form, 'table_name': table_name}
    return render(request, 'db_app/add_record.html', context)


def count_bookings(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT CountBookings();")
        bookings_count = cursor.fetchone()[0]

    return render(request, 'db_app/count_bookings.html', {'bookings_count': bookings_count})


def view_bookings(request):
    # Получаем GET параметры
    date_in_min = request.GET.get('date_in_min')
    date_in_max = request.GET.get('date_in_max')
    date_out_min = request.GET.get('date_out_min')
    date_out_max = request.GET.get('date_out_max')

    # Начальный QuerySet
    bookings = Bookings.objects.all()

    # Применяем фильтры
    if date_in_min:
        bookings = bookings.filter(check_in_date__gte=date_in_min)
    if date_in_max:
        bookings = bookings.filter(check_in_date__lte=date_in_max)
    if date_out_min:
        bookings = bookings.filter(check_out_date__gte=date_out_min)
    if date_out_max:
        bookings = bookings.filter(check_out_date__lte=date_out_max)

    # Добавляем пагинацию
    paginator = Paginator(bookings, 6)  # 6 записей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Для каждой брони ищем первую картинку комнаты
    from .models import RoomImages
    bookings_with_images = []
    for booking in page_obj:
        image = RoomImages.objects.filter(room=booking.room).first()
        bookings_with_images.append({
            'booking': booking,
            'image': image.image_path.url if image and image.image_path else None
        })

    context = {
        'bookings': page_obj,
        'bookings_with_images': bookings_with_images
    }
    return render(request, 'db_app/bookings.html', context)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

def guest_view(request):
    today = date.today()
    from .models import Rooms, Bookings
    booked_rooms = Bookings.objects.filter(
        check_in_date__lte=today,
        check_out_date__gte=today
    ).values_list('room_id', flat=True)
    rooms = Rooms.objects.exclude(room_id__in=booked_rooms)

    # Фильтрация по цене
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        rooms = rooms.filter(price_per_night__gte=price_min)
    if price_max:
        rooms = rooms.filter(price_per_night__lte=price_max)

    # Фильтрация по дате (ищем свободные на дату)
    date_in = request.GET.get('date_in')
    if date_in:
        booked_on_date = Bookings.objects.filter(
            check_in_date__lte=date_in,
            check_out_date__gte=date_in
        ).values_list('room_id', flat=True)
        rooms = rooms.exclude(room_id__in=booked_on_date)

    # Сортировка по цене
    sort_price = request.GET.get('sort_price')
    if sort_price == 'asc':
        rooms = rooms.order_by('price_per_night')
    elif sort_price == 'desc':
        rooms = rooms.order_by('-price_per_night')

    return render(request, 'db_app/guest_rooms.html', {'rooms': rooms})

def login_page(request):
    return render(request, 'db_app/auth.html', {'title': 'Вход'})

def register_page(request):
    return render(request, 'db_app/auth.html', {'title': 'Регистрация'})

def guest_room_detail(request, room_id):
    room = get_object_or_404(Rooms, room_id=room_id)
    images = RoomImages.objects.filter(room_id=room_id)
    if not images.exists():
        images = None  # Если изображений нет, передаем None
    return render(request, 'db_app/guest_room_detail.html', {'room': room, 'images': images})

class BookingListView(ListView):
    model = Bookings
    template_name = 'db_app/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Bookings.objects.all().order_by('-created_at')  # Сортировка по дате создания

def guest_book_room(request, room_id):
    from .models import Rooms, Bookings, Users
    room = get_object_or_404(Rooms, room_id=room_id)
    if request.method == 'POST':
        form = GuestBookingForm(request.POST)
        if form.is_valid():
            # Создаём уникального гостя
            unique_username = f"guest_{uuid.uuid4().hex[:8]}"
            guest_user = Users.objects.create(
                username=unique_username,
                password_hash='',
                email=f'{unique_username}@example.com',
                full_name=f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}"
            )
            Bookings.objects.create(
                user=guest_user,
                room=room,
                check_in_date=form.cleaned_data['check_in_date'],
                check_out_date=form.cleaned_data['check_out_date'],
                total_price=room.price_per_night,
                status="Гостевое бронирование"
            )
            return redirect('db_app:guest_booking_success', room_id=room.room_id)
    else:
        form = GuestBookingForm()
    return render(request, 'db_app/guest_book_room.html', {'room': room, 'form': form})

def guest_booking_success(request, room_id):
    from .models import Rooms
    room = get_object_or_404(Rooms, room_id=room_id)
    return render(request, 'db_app/guest_booking_success.html', {'room': room})
