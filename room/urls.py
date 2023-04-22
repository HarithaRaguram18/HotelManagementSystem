from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.room, name="room"),
    url(r'^list$', views.list, name="list"),
    url(r'^book$', views.book, name="book"),
    url(r'^filters/(?P<typeID>\w{0,50})/$', views.room_filter, name="room_filter"),
    url(r'^room-listing$', views.roomlisting, name="roomlisting"),
    url(r'^payment$', views.payment, name="payment"),
    url(r'^order-listing$', views.orderlisting, name="orderlisting"),
    url(r'^order-items/(?P<orderID>\w{0,50})/$', views.order_items, name="order_items"),
    url(r'^order-cancel/(?P<orderID>\w{0,50})/$', views.cancel_order, name="cancel_order"),
    url(r'^add$', views.add, name="add"),
    url(r'^room-details/(?P<roomId>\w{0,50})/$', views.room_details, name="room_details"),
    url(r'^update/(?P<roomId>\w{0,50})/$', views.update, name="update"),
    url(r'^cart-delete/(?P<itemId>\w{0,50})/$', views.delete_item, name="delete_item"),
    url(r'^delete/(?P<prodId>\w{0,50})/$', views.delete, name="delete"),
    url(r'^deletestock/(?P<id>\w{0,50})/$', views.deletestock, name="deletestock"),
    url(r'^order$', views.order, name="order"),
    url(r'^bedlisting$', views.bedlisting, name="bedlisting"),
    url(r'^addbed$', views.addbed, name="addbed"),
    url(r'^deletebed/(?P<id>\w{0,50})/$', views.deletebed, name="deletebed"),
]
