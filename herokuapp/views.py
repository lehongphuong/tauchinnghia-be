from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
# from .models import User
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
import requests
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.http import JsonResponse
from django.core import serializers
import json

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

# from models import User
from . import models

from django.db import connection


def index(request):
    return render(request, "index.html", {"users": 1})

# *********************************************
# begin common


# convert cursor to json data
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


# execute query sql with cursor
def executeQuery(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        data = dictfetchall(cursor)
    return data
# end common
# *********************************************


# *********************************************
# begin User
@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from User
def sendMail(request, format=None):
    data = json.loads(json.dumps(request.data)) 
    subject, from_email, to = 'Vé Tàu Lý Sơn - IziShip', 'Vé tàu Đảo Lý Sơn<vetaudaolyson@gmail.com>', data['to']
    text_content = 'Đây là tin nhắn quan trọng.'
    html_content = data['content']
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()  
    return Response([{"result": "ok"}])
 
# end User
# *********************************************


# *********************************************
# begin User
@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from User
def createDataUser(request, format=None):
    data = json.loads(json.dumps(request.data))
    # check user exists by phone or CMND
    phone = models.User.objects.filter(phone=data['phone'])
    cmnd = models.User.objects.filter(cmnd=data['cmnd']) 

    if phone.count() == 0 and cmnd.count() == 0:
        data['company'] = models.Company.objects.get(pk=data['company'])
        obj = models.User(**data)
        obj.save()
        return Response([{"id": obj.id, "result": "ok"}])

    return Response([{"id": '0', "result": "ok"}])


@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from User Booking
def createDataUserBooking(request, format=None):
    data = json.loads(json.dumps(request.data))
    # check user exists by phone or CMND
    phone = models.User.objects.filter(phone=data['phone'])
    cmnd = models.User.objects.filter(cmnd=data['cmnd'])  

    if phone.count() == 0 and cmnd.count() == 0:
        data['company'] = models.Company.objects.get(pk=data['company'])
        obj = models.User(**data)
        obj.save() 
        return Response([{"id": obj.id, "result": "ok"}])

    if cmnd.count() == 0:
        cmnd = phone 
        
    return Response([{"id": cmnd[0].pk, "result": "ok"}])


@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from User
def readDataUser(request, format=None):
    return Response(serializers.serialize("json", models.User.objects.filter(company=request.data['company'])))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get update data from User
def updateDataUser(request, format=None):
    data = json.loads(json.dumps(request.data))
    data['company'] = models.Company.objects.get(pk=data['company'])
    models.User(**data).save()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from User
def deleteDataUser(request, format=None):
    data = json.loads(json.dumps(request.data))
    models.User(**data).delete()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from User
def findDataUser(request, format=None):
    return Response(serializers.serialize("json", models.User.objects.filter(pk=request.data['pk'], company=request.data['company'])))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get data user of company
def searchDataUserOfCompany(request, format=None):
    return Response(serializers.serialize("json", models.User.objects.filter(company=request.data['company'])))

# end User
# *********************************************


# *********************************************
# begin Booking
@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from Booking
def createDataBooking(request, format=None):
    data = json.loads(json.dumps(request.data)) 
    data['trip'] = models.Trip.objects.get(pk=data['trip']) 
    data['user'] = models.User.objects.get(pk=data['user']) 
    obj = models.Booking(**data)
    obj.save()
    return Response([{"id": obj.id, "result": "ok"}])


@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from Booking
def readDataBooking(request, format=None):
    return Response(serializers.serialize("json", models.Booking.objects.all()))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get update data from Booking
def updateDataBooking(request, format=None):
    data = json.loads(json.dumps(request.data))
    data['trip'] = models.Trip.objects.get(pk=data['trip']) 
    data['user'] = models.User.objects.get(pk=data['user'])
    models.Booking(**data).save()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from Booking
def deleteDataBooking(request, format=None):
    data = json.loads(json.dumps(request.data))
    models.Booking(**data).delete()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from Booking
def findDataBooking(request, format=None):
    return Response(serializers.serialize("json", models.Booking.objects.filter(pk=request.data['pk'])))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get data Booking of company
def searchDataBookingOfCompany(request, format=None):
    return Response(serializers.serialize("json", models.Booking.objects.filter(user=request.data['user'])))

# end Booking
# *********************************************

# *********************************************
# begin Ticket
@api_view(['POST'])
@parser_classes((JSONParser,))
# create data from Ticket
def createDataTicket(request, format=None):
    data = json.loads(json.dumps(request.data))
    data['company'] = models.Company.objects.get(pk=data['company'])
    data['booking'] = models.Booking.objects.get(pk=data['booking'])
    data['trip'] = models.Trip.objects.get(pk=data['trip'])
    data['train'] = models.Train.objects.get(pk=data['train'])
    data['user'] = models.User.objects.get(pk=data['user'])
    obj = models.Ticket(**data)
    obj.save()
    return Response([{"id": obj.id, "result": "ok"}])


@api_view(['POST'])
@parser_classes((JSONParser,))
# create data Ticket Auto
def createDataTicketAuto(request, format=None):
    data = json.loads(json.dumps(request.data))

    # get number seat from train
    sql = "SELECT herokuapp_Train.total_seat  FROM herokuapp_Train"
    sql = sql.strip() + " WHERE id = %s" % (data[0]['train'])
    total_seat = executeQuery(sql)[0]['total_seat']
    # print(total_seat)

    # get ticket by trip
    sql = "SELECT herokuapp_Ticket.number_seat FROM herokuapp_Ticket"
    sql = sql.strip() + " WHERE trip_id = %s" % (data[0]['trip'])
    sql = sql.strip() + " AND start_date = '%s'" % (data[0]['start_date'])
    tickets_book = executeQuery(sql)

    # loop in data ticket prepare insert 
    booked_list = [0]*total_seat
    # đánh dấu các ghế được book = 1
    for book in tickets_book:
        booked_list[book['number_seat']] = 1
    
    ans = 1
    for ticket in data: 
        for i in range(ans, total_seat):
            # nếu ghế chưa được đặt thì sẽ chọn ghế
            if(booked_list[i] == 0):
                ans = i + 1
                ticket['number_seat'] = i
                break

    # print(data) 
    id_tickets = []
    for item in data: 
        # check and update number_seat and insert ticket 
        item['company'] = models.Company.objects.get(pk=item['company'])
        item['booking'] = models.Booking.objects.get(pk=item['booking'])
        item['trip'] = models.Trip.objects.get(pk=item['trip'])
        item['train'] = models.Train.objects.get(pk=item['train'])
        item['user'] = models.User.objects.get(pk=item['user'])
        obj = models.Ticket(**item)
        obj.save()

        # save id of ticket insert 
        id_tickets.append(obj.id)

    return Response([{"id": id_tickets, "result": "ok"}]) 

@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from Ticket
def readDataTicket(request, format=None):
    return Response(serializers.serialize("json", models.Ticket.objects.filter(company=request.data['company'])))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get update data from Ticket
def updateDataTicket(request, format=None):
    data = json.loads(json.dumps(request.data))
    data['company'] = models.Company.objects.get(pk=data['company'])
    data['train'] = models.Train.objects.get(pk=data['train'])
    data['trip'] = models.Trip.objects.get(pk=data['trip'])
    data['user'] = models.User.objects.get(pk=data['user'])
    models.Ticket(**data).save()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get update status of ticket
def updateStatusDataTicket(request, format=None):
    data = json.loads(json.dumps(request.data))
    ticket = models.Ticket.objects.filter(pk=request.data['pk'])
    # vé đã thanh toán
    ticket.update(status=3) 
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from Ticket
def deleteDataTicket(request, format=None):
    data = json.loads(json.dumps(request.data))
    models.Ticket.objects.get(pk=data['ticket']).delete()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from Ticket
def findDataTicket(request, format=None):
    return Response(serializers.serialize("json", models.Ticket.objects.filter(pk=request.data['pk'], company=request.data['company'])))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get search data from Ticket is order with train, trip
def searchDataTicketOrder(request, format=None):
    sql = "SELECT * FROM herokuapp_Ticket"
    sql = sql.strip() + " WHERE trip_id = %s" % (request.data['trip'])
    sql = sql.strip() + " AND start_date = '%s'" % (request.data['start_date'])

    return Response(executeQuery(sql))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from Ticket
def searchDataTicketByStatus(request, format=None):
    return Response(serializers.serialize("json", models.Ticket.objects.filter(status=request.data['status']).order_by('-time_check_in')))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get data Ticket of company
def searchDataTicketOfCompany(request, format=None):
    return Response(serializers.serialize("json", models.Ticket.objects.filter(company=request.data['company']).order_by('-pk')))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get data Ticket of company
def searchDataTicketByCondition(request, format=None): 
    print(request.data)
    data = ""
    # ID
    if(request.data['type'] == '0'):
        data = models.Ticket.objects.filter(
            company=request.data['company'], pk=request.data['value'])

    # CMND
    if(request.data['type'] == '1'):
        user = models.User.objects.filter(
            company=request.data['company'], cmnd=request.data['value'])
        print("phuong")
        print(user.values('pk'))
        print(user.values('pk')[0]['pk'])
        data = models.Ticket.objects.filter(
            company=request.data['company'], user=user.values('pk')[0]['pk'])

    # SDT
    if(request.data['type'] == '2'):
        user = models.User.objects.filter(
            company=request.data['company'], phone=request.data['value'])
        data = models.Ticket.objects.filter(
            company=request.data['company'], user=user.values('pk')[0]['pk'])

    return Response(serializers.serialize("json", data))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get search data from Ticket is order with train, trip
def searchDataTicketByCondition1(request, format=None):
    sql = "SELECT herokuapp_Ticket.*, herokuapp_Ticket.id ticket, herokuapp_Train.name trainname, herokuapp_User.*, herokuapp_Trip.* FROM herokuapp_Ticket"
    sql = sql.strip() + \
        " INNER JOIN herokuapp_Train on herokuapp_Ticket.train_id = herokuapp_Train.id"
    sql = sql.strip() + " INNER JOIN herokuapp_User on herokuapp_Ticket.user_id = herokuapp_User.id"
    sql = sql.strip() + " INNER JOIN herokuapp_Trip on herokuapp_Ticket.trip_id = herokuapp_Trip.id"
    sql = sql.strip() + \
        " WHERE herokuapp_Ticket.company_id = %s" % (request.data['company'])

    # (0,1,2,3) vé giử, vé đã mua, vé đã dùng, book online đã thanh toán
    sql = sql.strip() + " AND herokuapp_Ticket.status in(0,1,2,3)"

    # ID
    if(request.data['type'] == '0'):
        sql = sql.strip() + \
            " AND herokuapp_Ticket.id = '%s'" % (request.data['value'])

    # CMND
    if(request.data['type'] == '1'):
        sql = sql.strip() + \
            " AND herokuapp_User.cmnd = '%s'" % (request.data['value'])

    # SDT
    if(request.data['type'] == '2'):
        sql = sql.strip() + \
            " AND herokuapp_User.phone = '%s'" % (request.data['value'])

    # Họ và tên
    if(request.data['type'] == '3'):
        sql = sql.strip() + \
            " AND herokuapp_User.name = like'%%s%'" % (request.data['value'])

    sql = sql.strip() + \
        " AND herokuapp_Ticket.start_date = '%s'" % (
            request.data['start_date'])
    sql = sql.strip() + " ORDER BY herokuapp_Ticket.id desc"

    print(sql)

    return Response(executeQuery(sql))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get search data from Ticket is order with train, trip
def searchDataTicketByCondition2(request, format=None):
    sql = "SELECT herokuapp_Ticket.*, herokuapp_Ticket.id ticket, herokuapp_Train.name trainname, herokuapp_User.*, herokuapp_Trip.*, herokuapp_User.id user1, herokuapp_Trip.id trip FROM herokuapp_Ticket"
    sql = sql.strip() + \
        " INNER JOIN herokuapp_Train on herokuapp_Ticket.train_id = herokuapp_Train.id"
    sql = sql.strip() + " INNER JOIN herokuapp_User on herokuapp_Ticket.user_id = herokuapp_User.id"
    sql = sql.strip() + " INNER JOIN herokuapp_Trip on herokuapp_Ticket.trip_id = herokuapp_Trip.id"
    sql = sql.strip() + \
        " WHERE herokuapp_Ticket.company_id = %s" % (
            request.data['company'])

    # ID
    if(request.data['type'] == '0'):
        sql = sql.strip() + \
            " AND herokuapp_Ticket.id = '%s'" % (request.data['value'])

    # CMND
    if(request.data['type'] == '1'):
        sql = sql.strip() + \
            " AND herokuapp_User.cmnd = '%s'" % (request.data['value'])

    # SDT
    if(request.data['type'] == '2'):
        sql = sql.strip() + \
            " AND herokuapp_User.phone = '%s'" % (request.data['value'])

    # start date
    if(request.data['type'] == '3'):
        sql = sql.strip() + \
            " AND herokuapp_User.start_date = '%s'" % (request.data['value'])

    # start date
    if(request.data['type'] == '5'):
        if(request.data['start_date']):
            sql = sql.strip() + \
                " AND herokuapp_Trip.start_date = '%s'" % (
                    request.data['start_date'])

        if(request.data['phone']):
            sql = sql.strip() + \
                " AND herokuapp_User.phone = '%s'" % (request.data['phone'])

    sql = sql.strip() + " ORDER BY herokuapp_Ticket.id desc"

    return Response(executeQuery(sql))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get search data from Ticket is order with train, trip quản lý vé đặt online
def searchDataTicketByCondition3(request, format=None):
    sql = "SELECT herokuapp_Ticket.*, herokuapp_Ticket.id ticket, herokuapp_Train.name trainname, herokuapp_User.*, herokuapp_Trip.* FROM herokuapp_Ticket"
    sql = sql.strip() + \
        " INNER JOIN herokuapp_Train on herokuapp_Ticket.train_id = herokuapp_Train.id"
    sql = sql.strip() + " INNER JOIN herokuapp_User on herokuapp_Ticket.user_id = herokuapp_User.id"
    sql = sql.strip() + " INNER JOIN herokuapp_Trip on herokuapp_Ticket.trip_id = herokuapp_Trip.id"
    sql = sql.strip() + \
        " WHERE herokuapp_Ticket.company_id = %s" % (request.data['company'])

    # (4) book online chưa thanh toán
    sql = sql.strip() + " AND herokuapp_Ticket.status in(4)"

    # ID
    if(request.data['type'] == '0'):
        sql = sql.strip() + \
            " AND herokuapp_Ticket.id = '%s'" % (request.data['value'])

    # CMND
    if(request.data['type'] == '1'):
        sql = sql.strip() + \
            " AND herokuapp_User.cmnd = '%s'" % (request.data['value'])

    # SDT
    if(request.data['type'] == '2'):
        sql = sql.strip() + \
            " AND herokuapp_User.phone = '%s'" % (request.data['value'])

    # Họ và tên
    if(request.data['type'] == '3'):
        sql = sql.strip() + \
            " AND herokuapp_User.name = like'%%s%'" % (request.data['value'])

    sql = sql.strip() + \
        " AND herokuapp_Ticket.start_date = '%s'" % (
            request.data['start_date'])
    sql = sql.strip() + " ORDER BY herokuapp_Ticket.id desc"

    print(sql)

    return Response(executeQuery(sql))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get search data from Ticket is order with train, trip
def searchDataTicketStatic(request, format=None):
    # sql = "SELECT count(herokuapp_Ticket.train_id) as number_customer, herokuapp_Ticket.*, herokuapp_Ticket.id ticket, herokuapp_Train.name trainName, herokuapp_User.*, herokuapp_Trip.* FROM herokuapp_Ticket"
    sql = "SELECT herokuapp_Ticket.*, herokuapp_Ticket.id ticket, herokuapp_Train.name trainName, herokuapp_User.*, herokuapp_Trip.* FROM herokuapp_Ticket"
    sql = sql.strip() + \
        " INNER JOIN herokuapp_Train on herokuapp_Ticket.train_id = herokuapp_Train.id"
    sql = sql.strip() + " INNER JOIN herokuapp_User on herokuapp_Ticket.user_id = herokuapp_User.id"
    sql = sql.strip() + " INNER JOIN herokuapp_Trip on herokuapp_Ticket.trip_id = herokuapp_Trip.id"
    sql = sql.strip() + \
        " WHERE herokuapp_Ticket.company_id = %s" % (request.data['company'])
    sql = sql.strip() + \
        " AND herokuapp_Ticket.start_date = '%s'" % (request.data['value'])

    # sql = sql.strip() + " GROUP BY herokuapp_Ticket.train_id, herokuapp_Trip.type_ticket"
    sql = sql.strip() + " ORDER BY herokuapp_Ticket.id asc"

    return Response(executeQuery(sql))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get update data from change one ticket
def updateDataTicketChangeOneTicket(request, format=None):
    data = json.loads(json.dumps(request.data))
    oldTicket = models.Ticket.objects.get(pk=data['id'])
    oldTrip = models.Trip.objects.get(pk=oldTicket.trip.id)
    trip = models.Trip.objects.get(pk=data['trip'])

    sql = "SELECT number_seat FROM herokuapp_Ticket"
    sql = sql.strip() + " WHERE trip_id = %s" % (request.data['trip'])
    sql = sql.strip() + " AND start_date = '%s'" % (request.data['start_date'])
    sql = sql.strip() + " ORDER BY number_seat asc"

    ticketOrder = executeQuery(sql)

    # start date and start time train is not same
    if(oldTrip.type_ticket != trip.type_ticket or oldTrip.start_date != trip.start_date or oldTrip.start_time_train != trip.start_time_train):
        # check number_seat exists in list order
        flg = False
        for t in ticketOrder:
            if(int(data['number_seat']) == int(t['number_seat'])):
                flg = True
                break

        # check exists ticket
        # exists
        if(flg):
            # find new ticket suggest for employees
            flg1 = False
            for i in range(1, 139):
                flg1 = False
                for t in ticketOrder:
                    if(i == int(t['number_seat'])):
                        flg1 = True
                        break

                # number seat ok
                if(flg1 == False):
                    return Response([{"result": "nok", "error": "Ghế số " + str(data['number_seat']) + " đã có người đặt! Bạn vui lòng đổi ghế mới! Gợi ý đổi qua ghế " + str(i)}])

    # đổi ghế cùng chuyến
    else:
        if(oldTicket.number_seat == data['number_seat']):
            return Response([{"result": "nok", "error": "Ghế không thay đổi! vui lòng chọn ghế khác hoặc kết thúc."}])
        else:
            # check number_seat exists in list order
            flg = False
            for t in ticketOrder:
                if(int(data['number_seat']) == int(t['number_seat'])):
                    flg = True
                    break

            # check exists ticket
            # exists
            if(flg):
                # find new ticket suggest for employees
                flg1 = False
                for i in range(1, 139):
                    flg1 = False
                    for t in ticketOrder:
                        if(i == int(t['number_seat'])):
                            flg1 = True
                            break

                    # number seat ok
                    if(flg1 == False):
                        return Response([{"result": "nok", "error": "Ghế số " + str(data['number_seat']) + " đã có người đặt! Bạn vui lòng đổi ghế mới! Gợi ý đổi qua ghế " + str(i)}])

    ticket = models.Ticket.objects.get(pk=data['id'])
    ticket.type_ticket = data['type_ticket']
    ticket.start_date = data['start_date']
    ticket.number_seat = data['number_seat']
    ticket.trip = models.Trip.objects.get(pk=data['trip'])
    ticket.train = ticket.trip.train
    ticket.save()
    return Response([{"result": "ok"}])


@api_view(['POST'])
@parser_classes((JSONParser,))
# get update data from change many ticket
def updateDataTicketChangeManyTicket(request, format=None):
    data = json.loads(json.dumps(request.data))
    tickets = data['tickets']

    sql = "SELECT number_seat FROM herokuapp_Ticket"
    sql = sql.strip() + " WHERE trip_id = %s" % (request.data['trip'])
    sql = sql.strip() + " AND start_date = '%s'" % (request.data['start_date'])
    sql = sql.strip() + " ORDER BY number_seat asc"

    ticketOrder = executeQuery(sql)

    trip = models.Trip.objects.get(pk=data['trip'])
    if (trip.train.id == 1):
        totalSeat = 139
    else:
        totalSeat = 152

    # kiểm tra chuyến đi có đủ số lượng để đổi qua hay không
    if int((totalSeat - len(ticketOrder))) < len(tickets):
        return Response([{"result": "nok", "error": "Vui lòng chọn chuyến khác! Số ghế không đủ để chuyển"}])

    ans = 1

    for t in tickets:

        # duyệt số ghế
        for i in range(ans, totalSeat):
            flg = False

            # kiểm tra xem ghế có trống hay không để đổi ghế qua
            for to in ticketOrder:
                if(i == int(to['number_seat'])):
                    flg = True
                    break

            # nếu đã tìm được ghế thì thoát ra cho vé khác
            if flg == False:
                ans = i+1
                # save ticket to data base
                # print('t', t)
                ticket = models.Ticket.objects.get(pk=t['ticket'])
                ticket.type_ticket = data['type_ticket']
                ticket.start_date = data['start_date']
                ticket.number_seat = i
                ticket.trip = models.Trip.objects.get(pk=data['trip'])
                ticket.train = ticket.trip.train
                print('phuong', t['number_seat'], i, ticket)
                ticket.save()
                break

    return Response([{"result": "ok"}])
 

@api_view(['POST'])
@parser_classes((JSONParser,))
# delete many ticket
def deleteManyTicket(request, format=None):
    data = json.loads(json.dumps(request.data))
    tickets = data['tickets']

    for t in tickets:
        ticket = models.Ticket.objects.get(pk=t['ticket'])
        ticket.delete()

    return Response([{"result": "ok"}])

# end Ticket
# *********************************************

# *********************************************
# begin Train
@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from Train
def createDataTrain(request, format=None):
    data = json.loads(json.dumps(request.data))
    obj = models.Train(**data)
    obj.save()
    return Response([{"id": obj.id, "result": "ok"}])


@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from Train
def readDataTrain(request, format=None):
    return Response(serializers.serialize("json", models.Train.objects.all()))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get update data from Train
def updateDataTrain(request, format=None):
    data = json.loads(json.dumps(request.data))
    models.Train(**data).save()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from Train
def deleteDataTrain(request, format=None):
    data = json.loads(json.dumps(request.data))
    models.Train(**data).delete()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from Train
def findDataTrain(request, format=None):
    return Response(serializers.serialize("json", models.Train.objects.filter(pk=request.data['pk'])))

# end Train
# *********************************************

# *********************************************
# begin Debt
@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from Debt
def createDataDebt(request, format=None):
    data = json.loads(json.dumps(request.data))
    data['company'] = models.Company.objects.get(pk=data['company'])
    data['ticket'] = models.Ticket.objects.get(pk=data['ticket'])
    data['user'] = models.User.objects.get(pk=data['user'])
    obj = models.Debt(**data)
    obj.save()
    return Response([{"id": obj.id, "result": "ok"}])


@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from Debt
def readDataDebt(request, format=None):
    return Response(serializers.serialize("json", models.Debt.objects.filter(company=request.data['company'])))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get update data from Debt
def updateDataDebt(request, format=None):
    data = json.loads(json.dumps(request.data))
    data['company'] = models.Company.objects.get(pk=data['company'])
    data['ticket'] = models.Ticket.objects.get(pk=data['ticket'])
    data['user'] = models.User.objects.get(pk=data['user'])
    models.Debt(**data).save()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from Debt
def deleteDataDebt(request, format=None):
    data = json.loads(json.dumps(request.data))
    models.Debt(**data).delete()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from Debt
def findDataDebt(request, format=None):
    return Response(serializers.serialize("json", models.Debt.objects.filter(pk=request.data['pk'], company=request.data['company'])))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get data acengy of company
def searchDataDebtOfCompany(request, format=None):
    return Response(serializers.serialize("json", models.Debt.objects.filter(company=request.data['company'])))


# end Debt
# *********************************************

# *********************************************
# begin Company
@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from Company
def createDataCompany(request, format=None):
    data = json.loads(json.dumps(request.data))
    obj = models.Company(**data)
    obj.save()
    return Response([{"id": obj.id, "result": "ok"}])


@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from Company
def readDataCompany(request, format=None):
    return Response(serializers.serialize("json", models.Company.objects.all()))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get update data from Company
def updateDataCompany(request, format=None):
    data = json.loads(json.dumps(request.data))
    models.Company(**data).save()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from Company
def deleteDataCompany(request, format=None):
    data = json.loads(json.dumps(request.data))
    models.Company(**data).delete()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from Company
def findDataCompany(request, format=None):
    return Response(serializers.serialize("json", models.Company.objects.filter(pk=request.data['pk'])))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get data acengy of company
def searchDataAgencyOfCompany(request, format=None):
    return Response(serializers.serialize("json", models.Company.objects.filter(idParent=request.data['company'])))


# end Company
# *********************************************

# *********************************************
# begin PriceTicket
@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from PriceTicket
def createDataPriceTicket(request, format=None):
    data = json.loads(json.dumps(request.data))
    data['company'] = models.Company.objects.get(pk=data['company'])
    data['trip'] = models.Trip.objects.get(pk=data['trip'])
    obj = models.PriceTicket(**data)
    obj.save()
    return Response([{"id": obj.id, "result": "ok"}])


@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from PriceTicket
def readDataPriceTicket(request, format=None):
    return Response(serializers.serialize("json", models.PriceTicket.objects.filter(company=request.data['company'])))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get update data from PriceTicket
def updateDataPriceTicket(request, format=None):
    data = json.loads(json.dumps(request.data))
    data['company'] = models.Company.objects.get(pk=data['company'])
    data['trip'] = models.Trip.objects.get(pk=data['trip'])
    models.PriceTicket(**data).save()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from PriceTicket
def deleteDataPriceTicket(request, format=None):
    data = json.loads(json.dumps(request.data))
    models.PriceTicket(**data).delete()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from PriceTicket
def findDataPriceTicket(request, format=None):
    return Response(serializers.serialize("json", models.PriceTicket.objects.filter(pk=request.data['pk'], company=request.data['company'])))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get data acengy of company
def searchDataPriceTicketOfCompany(request, format=None):
    return Response(serializers.serialize("json", models.PriceTicket.objects.filter(company=request.data['company'])))

# end PriceTicket
# *********************************************

# *********************************************
# begin Trip
@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from Trip
def createDataTrip(request, format=None):
    data = json.loads(json.dumps(request.data))
    data['company'] = models.Company.objects.get(pk=data['company'])
    data['train'] = models.Train.objects.get(pk=data['train'])
    obj = models.Trip(**data)
    obj.save()
    return Response([{"id": obj.id, "result": "ok"}])


@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from Trip
def readDataTrip(request, format=None): 
    return Response(serializers.serialize("json", models.Trip.objects.all().order_by('-id')))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get update data from Trip
def updateDataTrip(request, format=None):
    data = json.loads(json.dumps(request.data))
    models.Trip(**data).save()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from Trip
def deleteDataTrip(request, format=None):
    data = json.loads(json.dumps(request.data))
    data['company'] = models.Company.objects.get(pk=data['company'])
    data['train'] = models.Train.objects.get(pk=data['train'])
    models.Trip(**data).delete() 
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from Trip
def findDataTrip(request, format=None):
    return Response(serializers.serialize("json", models.Trip.objects.filter(pk=request.data['pk'])))


@api_view(['POST'])
@parser_classes((JSONParser,))
# find data trip by date
def findDataTripByDate(request, format=None):
    return Response(serializers.serialize("json", models.Trip.objects.filter(start_date=request.data['start_date']).order_by('start_time_train')))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get all trip and number seat by date
def get_all_trip_and_number_seat_by_date(request, format=None):
    data = json.loads(json.dumps(request.data)) 
    sql = "SELECT herokuapp_Trip.*, herokuapp_Train.total_seat, count(herokuapp_Ticket.trip_id) number_book FROM herokuapp_Trip"
    sql = sql.strip() + " INNER JOIN herokuapp_Train ON herokuapp_Trip.train_id = herokuapp_Train.id"
    sql = sql.strip() + " INNER JOIN herokuapp_Ticket ON herokuapp_Trip.id = herokuapp_Ticket.trip_id"
    sql = sql.strip() + " WHERE herokuapp_Trip.start_date = '%s'" % (data['start_date'])
    sql = sql.strip() + " GROUP BY herokuapp_Ticket.trip_id"
    sql = sql.strip() + " ORDER BY start_time_train asc"  
    return Response(executeQuery(sql))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get all trip and number seat by date
def get_all_trip_and_number_seat_by_date(request, format=None):
    data = json.loads(json.dumps(request.data)) 
    sql = "SELECT herokuapp_Trip.*, herokuapp_Train.total_seat, count(herokuapp_Ticket.trip_id) number_book FROM herokuapp_Trip"
    sql = sql.strip() + " INNER JOIN herokuapp_Train ON herokuapp_Trip.train_id = herokuapp_Train.id"
    sql = sql.strip() + " INNER JOIN herokuapp_Ticket ON herokuapp_Trip.id = herokuapp_Ticket.trip_id"
    sql = sql.strip() + " WHERE herokuapp_Trip.start_date = '%s'" % (data['start_date'])
    sql = sql.strip() + " GROUP BY herokuapp_Ticket.trip_id"
    sql = sql.strip() + " ORDER BY start_time_train asc"  
    return Response(executeQuery(sql))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from Trip
def createDataTripFromExcel(request, format=None):
    data = json.loads(json.dumps(request.data))   
    trips = []

    for i in range(1,len(data)):
        trip = {}
        trip['company'] = 1
        trip['train'] = int(data[i][0])
        trip['start_date'] = data[i][1]
        trip['start_time_train'] = data[i][2]
        trip['end_time_train'] = data[i][3]
        trip['type_ticket'] = data[i][4]
        trip['price_origin'] = data[i][5]
        trip['price'] = data[i][6]
        trips.append(trip)
 
    for trip in trips: 
        trip['company'] = models.Company.objects.get(pk=trip['company'])
        trip['train'] = models.Train.objects.get(pk=trip['train']) 
        obj = models.Trip(**trip)
        obj.save()  
    
    return Response([{"id": obj.id, "result": "ok"}])

# end Trip
# *********************************************

# *********************************************
# begin Staff
@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from Staff
def createDataStaff(request, format=None):
    data = json.loads(json.dumps(request.data))
    data['company'] = models.Company.objects.get(pk=data['company'])
    obj = models.Staff(**data)
    obj.save()
    return Response([{"id": obj.id, "result": "ok"}])


@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from Staff
def readDataStaff(request, format=None):
    return Response(serializers.serialize("json", models.Staff.objects.filter(company=request.data['company'])))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get update data from Staff
def updateDataStaff(request, format=None):
    data = json.loads(json.dumps(request.data))
    data['company'] = models.Company.objects.get(pk=data['company'])
    models.Staff(**data).save()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from Staff
def deleteDataStaff(request, format=None):
    data = json.loads(json.dumps(request.data))
    models.Staff(**data).delete()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from Staff
def findDataStaff(request, format=None):
    return Response(serializers.serialize("json", models.Staff.objects.filter(pk=request.data['pk'], company=request.data['company'])))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get data acengy of company
def searchDataStaffOfCompany(request, format=None):
    return Response(serializers.serialize("json", models.Staff.objects.filter(company=request.data['company'])))

# end Staff
# *********************************************


# *********************************************
# begin Point
@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from Point
def createDataPoint(request, format=None):
    data = json.loads(json.dumps(request.data))
    data['user'] = models.User.objects.get(pk=data['user'])
    obj = models.Point(**data)
    obj.save()
    return Response([{"id": obj.id, "result": "ok"}])


@api_view(['POST'])
@parser_classes((JSONParser,))
# get all data from Point
def readDataPoint(request, format=None):
    return Response(serializers.serialize("json", models.Point.objects.all()))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get update data from Point
def updateDataPoint(request, format=None):
    data = json.loads(json.dumps(request.data))
    data['user'] = models.User.objects.get(pk=data['user'])
    models.Point(**data).save()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from Point
def deleteDataPoint(request, format=None):
    data = json.loads(json.dumps(request.data))
    models.Point(**data).delete()
    return Response({"result": "ok"})


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from Point
def findDataPoint(request, format=None):
    return Response(serializers.serialize("json", models.Point.objects.filter(pk=request.data['pk'])))


@api_view(['POST'])
@parser_classes((JSONParser,))
# get delete data from Point
def findDataPointByUser(request, format=None):
    data = json.loads(json.dumps(request.data))
    return Response(serializers.serialize("json", models.Point.objects.filter(user=models.User.objects.get(pk=data['user']))))

# end Point
# *********************************************
