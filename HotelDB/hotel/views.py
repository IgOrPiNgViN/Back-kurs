from django.views.generic import ListView, DetailView
from hotel.models import Room

class RoomListView(ListView):
    model = Room
    template_name = 'hotel/room_list.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        return Room.objects.filter(is_active=True)  # Фильтрация только активных номеров

class RoomDetailView(DetailView):
    model = Room
    template_name = 'hotel/room_detail.html'
    context_object_name = 'room'

    def get_queryset(self):
        return Room.objects.filter(is_active=True)  # Фильтрация только активных номеров 