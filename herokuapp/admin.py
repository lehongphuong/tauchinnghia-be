from django.contrib import admin

# Register your models here.
from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'cmnd', 'address', 'born')
    list_filter = ['id', 'name', 'phone', 'cmnd', 'address', 'born']
    search_fields = ['id', 'name', 'phone', 'cmnd', 'address', 'born']


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'train', 'trip', 'user', 'number_seat',
                    'is_debt', 'start_date', 'status', 'pay_type', 'price_origin', 'price', 'time_check_in', 'role')
    list_filter = ('id', 'train', 'trip', 'user', 'number_seat',
                   'is_debt', 'start_date', 'status', 'pay_type', 'price_origin', 'price', 'time_check_in', 'role')
    search_fields = ('id', 'train', 'trip', 'user', 'pay_type', 'number_seat',
                     'is_debt', 'start_date', 'status', 'price_origin', 'price', 'time_check_in', 'role')


class TrainAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'total_seat')
    list_filter = ('id', 'name', 'total_seat')
    search_fields = ('id', 'name', 'total_seat')


class DebtAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ticket', 'status',
                    'start_date', 'end_date', 'money')
    list_filter = ('id', 'user', 'ticket', 'status',
                   'start_date', 'end_date', 'money')
    search_fields = ('id', 'user', 'ticket', 'status',
                     'start_date', 'end_date', 'money')


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_parent', 'username',
                    'password', 'name', 'born', 'address')
    list_filter = ('id', 'id_parent', 'username',
                   'password', 'name', 'born', 'address')
    search_fields = ('id', 'id_parent', 'username',
                     'password', 'name', 'born', 'address')


class PriceTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'trip', 'company', 'price_origin', 'price')
    list_filter = ('id', 'trip', 'company', 'price_origin', 'price')
    search_fields = ('id', 'trip', 'company', 'price_origin', 'price')


class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'train', 'start_date', 'start_time_train', 'end_time_train',
                    'type_ticket')
    list_filter = ('id', 'train', 'start_date', 'start_time_train', 'end_time_train',
                   'type_ticket')
    search_fields = ('id', 'train', 'start_date', 'start_time_train', 'end_time_train',
                     'type_ticket')


class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'name', 'born', 'address')
    list_filter = ('id', 'username', 'name', 'born', 'address')
    search_fields = ('id', 'username', 'name', 'born', 'address')


class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'coin')
    list_filter = ('id', 'user', 'coin')
    search_fields = ('id', 'user', 'coin')


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Ticket, TicketAdmin)
admin.site.register(models.Train, TrainAdmin)
admin.site.register(models.Debt, DebtAdmin)
admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.PriceTicket, PriceTicketAdmin)
admin.site.register(models.Trip, TripAdmin)
admin.site.register(models.Staff, StaffAdmin)
admin.site.register(models.Point, PointAdmin)
