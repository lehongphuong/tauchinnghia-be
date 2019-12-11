from django.urls import path, include
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    # *******************************************************
    # begin ultil
    path('sendMail', views.sendMail, name='sendMail'), 
    # end ultil
    # *******************************************************

    # *******************************************************
    # begin User
    path('createDataUser', views.createDataUser, name='createDataUser'),
    path('createDataUserBooking', views.createDataUserBooking, name='createDataUserBooking'),
    path('readDataUser', views.readDataUser, name='readDataUser'),
    path('updateDataUser', views.updateDataUser, name='updateDataUser'),
    path('deleteDataUser', views.deleteDataUser, name='deleteDataUser'),
    path('findDataUser', views.findDataUser, name='findDataUser'),
    path('searchDataUserOfCompany', views.searchDataUserOfCompany,
         name='searchDataUserOfCompany'),
    # end User
    # *******************************************************

    # *******************************************************
    # begin Booking
    path('createDataBooking', views.createDataBooking, name='createDataBooking'), 
    path('readDataBooking', views.readDataBooking, name='readDataBooking'),
    path('updateDataBooking', views.updateDataBooking, name='updateDataBooking'),
    path('deleteDataBooking', views.deleteDataBooking, name='deleteDataBooking'),
    path('findDataBooking', views.findDataBooking, name='findDataBooking'),
    path('searchDataBookingOfCompany', views.searchDataBookingOfCompany,
         name='searchDataBookingOfCompany'),
    # end Booking
    # *******************************************************

    # *******************************************************
    # begin Ticket
    path('createDataTicket', views.createDataTicket, name='createDataTicket'),
    path('createDataTicketAuto', views.createDataTicketAuto, name='createDataTicketAuto'),
    path('readDataTicket', views.readDataTicket, name='readDataTicket'),
    path('updateDataTicket', views.updateDataTicket, name='updateDataTicket'),
    path('updateStatusDataTicket', views.updateStatusDataTicket, name='updateStatusDataTicket'),
    path('deleteDataTicket', views.deleteDataTicket, name='deleteDataTicket'),
    path('findDataTicket', views.findDataTicket, name='findDataTicket'),
    path('searchDataTicketOrder', views.searchDataTicketOrder,
         name='searchDataTicketOrder'),
    path('searchDataTicketByStatus', views.searchDataTicketByStatus,
         name='searchDataTicketByStatus'),
    path('searchDataTicketOfCompany', views.searchDataTicketOfCompany,
         name='searchDataTicketOfCompany'),
    path('searchDataTicketByCondition', views.searchDataTicketByCondition,
         name='searchDataTicketByCondition'),
    path('searchDataTicketByCondition1', views.searchDataTicketByCondition1,
         name='searchDataTicketByCondition1'),
    path('searchDataTicketByCondition2', views.searchDataTicketByCondition2,
         name='searchDataTicketByCondition2'),
    path('searchDataTicketByCondition3', views.searchDataTicketByCondition3,
         name='searchDataTicketByCondition3'),
    path('searchDataTicketStatic', views.searchDataTicketStatic,
         name='searchDataTicketStatic'),
    path('updateDataTicketChangeOneTicket', views.updateDataTicketChangeOneTicket,
         name='updateDataTicketChangeOneTicket'),
    path('updateDataTicketChangeManyTicket', views.updateDataTicketChangeManyTicket,
         name='updateDataTicketChangeManyTicket'),
    path('deleteManyTicket', views.deleteManyTicket,
         name='deleteManyTicket'),
    # end Ticket
    # *******************************************************

    # *******************************************************
    # begin Train
    path('createDataTrain', views.createDataTrain, name='createDataTrain'),
    path('readDataTrain', views.readDataTrain, name='readDataTrain'),
    path('updateDataTrain', views.updateDataTrain, name='updateDataTrain'),
    path('deleteDataTrain', views.deleteDataTrain, name='deleteDataTrain'),
    path('findDataTrain', views.findDataTrain, name='findDataTrain'),
    # end Train
    # *******************************************************

    # *******************************************************
    # begin Debt
    path('createDataDebt', views.createDataDebt, name='createDataDebt'),
    path('readDataDebt', views.readDataDebt, name='readDataDebt'),
    path('updateDataDebt', views.updateDataDebt, name='updateDataDebt'),
    path('deleteDataDebt', views.deleteDataDebt, name='deleteDataDebt'),
    path('findDataDebt', views.findDataDebt, name='findDataDebt'),
    path('searchDataDebtOfCompany', views.searchDataDebtOfCompany,
         name='searchDataDebtOfCompany'),
    # end Debt
    # *******************************************************

    # *******************************************************
    # begin Company
    path('createDataCompany', views.createDataCompany, name='createDataCompany'),
    path('readDataCompany', views.readDataCompany, name='readDataCompany'),
    path('updateDataCompany', views.updateDataCompany, name='updateDataCompany'),
    path('deleteDataCompany', views.deleteDataCompany, name='deleteDataCompany'),
    path('findDataCompany', views.findDataCompany, name='findDataCompany'),
    path('searchDataAgencyOfCompany', views.searchDataAgencyOfCompany,
         name='searchDataAgencyOfCompany'),
    # end Company
    # *******************************************************

    # *******************************************************
    # begin PriceTicket
    path('createDataPriceTicket', views.createDataPriceTicket,
         name='createDataPriceTicket'),
    path('readDataPriceTicket', views.readDataPriceTicket,
         name='readDataPriceTicket'),
    path('updateDataPriceTicket', views.updateDataPriceTicket,
         name='updateDataPriceTicket'),
    path('deleteDataPriceTicket', views.deleteDataPriceTicket,
         name='deleteDataPriceTicket'),
    path('findDataPriceTicket', views.findDataPriceTicket,
         name='findDataPriceTicket'),
    path('searchDataPriceTicketOfCompany', views.searchDataPriceTicketOfCompany,
         name='searchDataPriceTicketOfCompany'),
    # end PriceTicket
    # *******************************************************

    # *******************************************************
    # begin Trip
    path('createDataTrip', views.createDataTrip, name='createDataTrip'),
    path('readDataTrip', views.readDataTrip, name='readDataTrip'),
    path('updateDataTrip', views.updateDataTrip, name='updateDataTrip'),
    path('deleteDataTrip', views.deleteDataTrip, name='deleteDataTrip'),
    path('findDataTrip', views.findDataTrip, name='findDataTrip'),
    path('findDataTripByDate', views.findDataTripByDate, name='findDataTripByDate'),
    path('get_all_trip_and_number_seat_by_date', views.get_all_trip_and_number_seat_by_date, name='get_all_trip_and_number_seat_by_date'),
    path('createDataTripFromExcel', views.createDataTripFromExcel, name='createDataTripFromExcel'),
    # end Trip
    # *******************************************************


    # *******************************************************
    # begin Staff
    path('createDataStaff', views.createDataStaff, name='createDataStaff'),
    path('readDataStaff', views.readDataStaff, name='readDataStaff'),
    path('updateDataStaff', views.updateDataStaff, name='updateDataStaff'),
    path('deleteDataStaff', views.deleteDataStaff, name='deleteDataStaff'),
    path('findDataStaff', views.findDataStaff, name='findDataStaff'),
    path('searchDataStaffOfCompany', views.searchDataStaffOfCompany,
         name='searchDataStaffOfCompany'),
    # end Staff
    # *******************************************************

    # *******************************************************
    # begin Point
    path('createDataPoint', views.createDataPoint, name='createDataPoint'),
    path('readDataPoint', views.readDataPoint, name='readDataPoint'),
    path('updateDataPoint', views.updateDataPoint, name='updateDataPoint'),
    path('deleteDataPoint', views.deleteDataPoint, name='deleteDataPoint'),
    path('findDataPoint', views.findDataPoint, name='findDataPoint'),
    path('findDataPointByUser', views.findDataPointByUser, name='findDataPointByUser'), 
    # end Point
    # *******************************************************
]
