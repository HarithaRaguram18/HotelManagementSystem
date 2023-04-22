from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db import connection


# Create your views here.

def listing(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM bed")
    bedlist = dictfetchall(cursor)

    context = {
        "bedlist": bedlist
    }

    # Message according medicines Role #
    context['heading'] = "Bed Details";
    return render(request, 'bed-details.html', context)

def lists(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM bed")
    bedlist = dictfetchall(cursor)

    context = {
        "bedlist": bedlist
    }

    # Message according medicines Role #
    context['heading'] = "Bed Details";
    return render(request, 'bed-list.html', context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM bed WHERE bed_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, bedId):
    context = {
        "fn": "update",
        "bedDetails": getData(bedId),
        "heading": 'Update Bed',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE bed
                   SET bed_name=%s, bed_description=%s WHERE bed_id = %s
                """, (
            request.POST['bed_name'],
            request.POST['bed_description'],
            bedId
        ))
        context["bedDetails"] =  getData(bedId)
        messages.add_message(request, messages.INFO, "Bed updated succesfully !!!")
        return redirect('bed-listing')
    else:
        return render(request, 'bed.html', context)


def add(request):
    context = {
        "fn": "add",
        "heading": 'Add Bed'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO bed
		   SET bed_name=%s, bed_description=%s
		""", (
            request.POST['bed_name'],
            request.POST['bed_description']))
        return redirect('bed-listing')
    return render(request, 'bed.html', context)

def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM bed WHERE bed_id=' + id
    cursor.execute(sql)
    messages.add_message(request, messages.INFO, "Bed Deleted succesfully !!!")
    return redirect('bed-listing')
