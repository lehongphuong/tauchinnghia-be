from django.db import models

# Create your models here.
# https://docs.djangoproject.com/en/2.2/ref/models/fields/
# https://docs.djangoproject.com/en/2.2/topics/db/sql/


class Company(models.Model):
    id = models.AutoField
    id_parent = models.IntegerField(default=0)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    born = models.DateField()
    address = models.CharField(max_length=200)


class User(models.Model):
    id = models.AutoField
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    cmnd = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    born = models.DateField()


class Train(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=100)
    total_seat = models.IntegerField(default=0)


class Trip(models.Model):
    id = models.AutoField
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time_train = models.TimeField()
    end_time_train = models.TimeField() 
    type_ticket = models.IntegerField(default=0)
    price_origin = models.FloatField(max_length=20)
    price = models.FloatField(max_length=20)


class Ticket(models.Model):
    id = models.AutoField
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_seat = models.IntegerField(default=0)
    is_debt = models.BooleanField(default=False)
    start_date = models.DateField()
    status = models.IntegerField(default=0)
    pay_type = models.IntegerField(default=0)
    price_origin = models.FloatField(max_length=20, default=0)
    price = models.FloatField(max_length=20, default=0)
    time_check_in = models.DateTimeField()
    role = models.IntegerField(default=0)


class Debt(models.Model):
    id = models.AutoField
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    money = models.FloatField(max_length=20)

class PayDebt(models.Model):
    id = models.AutoField
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    money_spend = models.IntegerField(default=0)
    note = models.CharField(max_length=200)

class PriceTicket(models.Model):
    id = models.AutoField
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    price_origin = models.FloatField(max_length=20)
    price = models.FloatField(max_length=20)


class Staff(models.Model):
    id = models.AutoField
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    born = models.DateField()
    address = models.CharField(max_length=200)


class Point(models.Model):
    id = models.AutoField
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.IntegerField(default=0)
