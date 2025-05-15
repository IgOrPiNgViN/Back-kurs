from django.contrib import admin
from hotel.models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'category', 'price', 'is_active')
    list_filter = ('is_active',)
    actions = ['make_inactive', 'delete_selected_rooms']

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Деактивировать выбранные номера"

    def delete_selected_rooms(self, request, queryset):
        for room in queryset:
            room.delete()  # Физическое удаление с каскадом
    delete_selected_rooms.short_description = "Удалить выбранные номера полностью (с каскадом)" 