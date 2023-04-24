from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from .models import room
from django.contrib import messages
from django.db import connection
from hotel_booking_system.utils import getDropDown, dictfetchall
from datetime import date
from datetime import datetime


# Create your views here.
def orderlisting(request):
    cursor = connection.cursor()
    if (request.session.get('user_level_id', None) == 1):
        SQL = "SELECT * FROM `booking`,`users_user`,`room_room` WHERE booking_room_id = room_id AND booking_user_id = user_id"
    else:
        customerID = str(request.session.get('user_id', None))
        SQL = "SELECT * FROM `booking`,`users_user`,`room_room` WHERE booking_room_id = room_id AND booking_user_id = user_id AND user_id = " + customerID

    cursor.execute(SQL)
    orderlist = dictfetchall(cursor)

    context = {
        "orderlist": orderlist
    }

    # Message according Room #
    context['heading'] = "Order Reports";
    return render(request, 'order-listing.html', context)

# Create your views here.
def roomlisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM room_room, bed, type WHERE bed_id = room_bed_id AND type_id = room_type_id")
    roomlist = dictfetchall(cursor)

    context = {
        "roomlist": roomlist
    }

    # Message according Room #
    context['heading'] = "Rooms Details";
    return render(request, 'room-listing.html', context)

# Create your views here.
def payment(request):
    today = date.today()
    todayDate = today.strftime("%B %d, %Y")

    if (request.method == "POST" and 'order_amount' in request.POST): 
        date_format = "%m/%d/%Y"
        from_date = datetime.strptime(request.session.get('from_date', None), date_format)
        to_date = datetime.strptime(request.session.get('to_date', None), date_format)
        total_days = to_date - from_date
        request.session['order_id'] = "0"
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO booking
		   SET `booking_user_id` = %s, `booking_room_id` = %s, `booking_from_date` = %s, `booking_to_date` = %s, `booking_persons` = %s, `booking_room_price` = %s, `booking_total_cost` = %s, `booking_days` = %s, `booking_date` = %s
		""", (
            request.session.get('user_id', None),
            request.POST['room_id'],
            request.session.get('from_date', None),
            request.session.get('to_date', None),
            request.session.get('total_person', None),
            request.POST['room_price'],
            request.POST['order_amount'],
            total_days,
            todayDate))
        
        print('Checking',cursor.lastrowid);
        bookingId = cursor.lastrowid
        return redirect('order-items/'+str(bookingId))
    else:
        date_format = "%m/%d/%Y"
        from_date = datetime.strptime(request.session.get('from_date', None), date_format)
        to_date = datetime.strptime(request.session.get('to_date', None), date_format)
        total_days = to_date - from_date

        totalAmount = (int(request.POST['room_price']) * int(total_days.days))
        print('Checking1',request.POST['room_price'],request.POST['room_id'])
        context = {
            "totalAmount": totalAmount,
            "room_price": request.POST['room_price'],
            "room_id": request.POST['room_id']
        }
    # Message according Room #
    context['heading'] = "Rooms Details"
    return render(request, 'payment.html', context)

# Create your views here.
def cancel_order(request, orderID):
    cursor = connection.cursor()
    cursor.execute("""
                UPDATE `booking`
                SET booking_status= 'Cancelled' WHERE booking_id = %s
            """, (
        orderID
    ))
    messages.add_message(request, messages.INFO, "Your order has been cancelled successfully !!!")
    return redirect('orderlisting')

# Create your views here.
def order_items(request, orderID):
    cursor = connection.cursor()

    cursor.execute("SELECT *  FROM `room_room`, `booking`, `users_user`, `type`, `bed` WHERE bed_id = room_bed_id AND type_id = room_type_id AND  booking_room_id = room_id AND user_id =  booking_user_id  AND booking_id = "+ str(orderID))
    customerOrderDetails = dictfetchall(cursor)

    
    context = {
        "customerOrderDetails": customerOrderDetails[0],
    }

    # Message according Room #
    context['heading'] = "Rooms Details";
    return render(request, 'order-items.html', context)

# Create your views here.
def room(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM room_room, bed, type WHERE bed_id = room_bed_id AND type_id = room_type_id")
    roomlist = dictfetchall(cursor)

    context = {
        "roomlist": roomlist
    }

    # Message according Room #
    context['heading'] = "Rooms Details";
    return render(request, 'room.html', context)

# Create your views here.
def list(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM room_room, bed, type WHERE bed_id = room_bed_id AND type_id = room_type_id")
    roomlist = dictfetchall(cursor)

    context = {
        "roomlist": roomlist
    }

    # Message according Room #
    context['heading'] = "Rooms Details";
    return render(request, 'list.html', context)
# Create your views here.
def room_filter(request, typeID):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM room_room, bed, type WHERE bed_id = room_bed_id AND type_id = room_type_id AND type_id = "+ str(typeID))
    roomlist = dictfetchall(cursor)

    context = {
        "roomlist": roomlist
    }

    # Message according Room #
    context['heading'] = "Rooms Details";
    return render(request, 'room.html', context)

def update(request, roomId):
    roomdetails = getRoomDetails(roomId)
    context = {
        "fn": "add",
        "probedlist":getDropDown('bed', 'bed_id', 'bed_name', roomdetails['room_bed_id'], '1'),
        "protypelist":getDropDown('type', 'type_id', 'type_name', roomdetails['room_type_id'], '1'),
        "roomdetails":roomdetails
    }
    if (request.method == "POST"):
        try:
            room_image = None
            room_image = roomdetails['room_image']
            if(request.FILES and request.FILES['room_image']):
                roomImage = request.FILES['room_image']
                fs = FileSystemStorage()
                filename = fs.save(roomImage.name, roomImage)
                room_image = fs.url(roomImage)
            
            cursor = connection.cursor()
            cursor.execute("""
            UPDATE `room_room`
            SET `room_name` = %s, `room_type_id` = %s, `room_bed_id` = %s, `room_price` = %s, `room_image` = %s, `room_description` = %s, `room_facility` = %s WHERE room_id = %s
            """, (
                request.POST['room_name'],
                request.POST['room_type_id'],
                request.POST['room_bed_id'],
                request.POST['room_price'],
                room_image,
                request.POST['room_description'],
                request.POST['room_facility'],
                request.POST['room_id']
                ))
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        context["roomdetails"] = getRoomDetails(roomId)
        messages.add_message(request, messages.INFO, "Room updated succesfully !!!")
        return redirect('roomlisting')

    else:
        return render(request,'room-add.html', context)

def room_details(request, roomId):
    if(request.session.get('authenticated', False) == False):
        messages.add_message(request, messages.ERROR, "Login to your account, to buy the room !!!")
        return redirect('/users')
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM room_room, bed, type WHERE bed_id = room_bed_id AND type_id = room_type_id AND room_id = "+roomId)
    roomdetails = dictfetchall(cursor)

    context = {
        "fn": "add",
        "roomdetails": roomdetails[0],
        "from_date": request.session.get('from_date', None),
        "to_date": request.session.get('to_date', None),
        "total_person": request.session.get('total_person', None)
    }
    if (request.method == "POST"):
        try:
           "dfd"
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        messages.add_message(request, messages.INFO, "Room updated succesfully !!!")
        return redirect('cart_listing')
    else:
        return render(request,'room-details.html', context)

def add(request):
    context = {
        "fn": "add",
        "probedlist":getDropDown('bed', 'bed_id', 'bed_name',0, '1'),
        "protypelist":getDropDown('type', 'type_id', 'type_name',0, '1'),
        "heading": 'Room add'
    };
    if (request.method == "POST"):
        try:
            room_image = None

            if(request.FILES and request.FILES['room_image']):
                roomImage = request.FILES['room_image']
                fs = FileSystemStorage()
                filename = fs.save(roomImage.name, roomImage)
                room_image = fs.url(roomImage)

            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO `room_room`
            SET `room_name` = %s, `room_type_id` = %s, `room_bed_id` = %s, `room_price` = %s, `room_image` = %s, `room_description` = %s, `room_facility` = %s
            """, (
                request.POST['room_name'],
                request.POST['room_type_id'],
                request.POST['room_bed_id'],
                request.POST['room_price'],
                room_image,
                request.POST['room_description'],
                request.POST['room_facility']
                ))
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        return redirect('roomlisting')

    else:
        return render(request,'room-add.html', context)

def book(request):
    context = {
        "fn": "add",
        "heading": 'Room add'
    }
    if (request.method == "POST"):
        try:
            request.session['from_date'] = request.POST['from_date']
            request.session['to_date'] = request.POST['to_date']
            request.session['total_person'] = request.POST['total_person']
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        return redirect('room')

    else:
        return render(request,'book-room.html', context)

def delete_item(request, itemId):
    cursor = connection.cursor()
    sql = 'DELETE FROM order_item WHERE oi_id=' + itemId
    cursor.execute(sql)
    return redirect('cart_listing')

def delete(request, prodId):
    cursor = connection.cursor()
    sql = 'DELETE FROM room_room WHERE room_id=' + prodId
    cursor.execute(sql)
    return redirect('roomlisting')

def getRoomDetails(roomId):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM room_room WHERE room_id = "+roomId)
    roomList = dictfetchall(cursor)
    return roomList[0]

def deletestock(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM stock WHERE stock_id=' + id
    cursor.execute(sql)
    return redirect('stock')

def bedlisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM bed")
    bedlist = dictfetchall(cursor)

    context = {
        "bedlist": bedlist
    }

    # Message according Room #
    context['heading'] = "Rooms Bed";
    return render(request, 'viewbed.html', context)

def deletebed(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM bed WHERE bed_id=' + id
    cursor.execute(sql)
    return redirect('bed')

def addbed(request):
    context = {
        "fn": "add",
        "heading": 'Add Bed'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO bed
		   SET bed_name=%s
		""", (
            request.POST['bed_name']))
        return redirect('bedlisting')
    return render(request, 'addbed.html', context)

def order(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM order_item")
    orderlist = dictfetchall(cursor)

    context = {
        "orderlist": orderlist
    }

    # Message according Orders #
    context['heading'] = "Rooms Order Details";
    return render(request, 'orders.html', context)
