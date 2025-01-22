from django.urls import path 
from .import views

urlpatterns = [
    path("",views.HomePage,name="HomePage"),   
    path("AdminIndex",views.AdminIndex,name="AdminIndex"),    
    path("HospitalIndex",views.HospitalIndex,name="HospitalIndex"),    
    path("MerchantIndex",views.MerchantIndex,name="MerchantIndex"),    
    path("SignIn",views.SignIn,name="SignIn"),
    path("SignUp",views.SignUp,name="SignUp"),
    path("SignOut",views.SignOut,name="SignOut"),
    path("user_products",views.user_products,name="user_products"),
    path("buy_now/<int:pk>",views.buy_now,name="buy_now"),
    path("payment_start/<int:pk>",views.payment_start,name="payment_start"),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('order_history/', views.order_history, name='order_history'),
    path("hospital_user",views.hospital_user,name="hospital_user"),
    path("book_appointment/<int:pk>",views.book_appointment,name="book_appointment"),
    path("my_appointments",views.my_appointments,name="my_appointments"),
    path("vaccine",views.vaccine,name="vaccine"),
    path("my_pets",views.my_pets,name="my_pets"),
    path("update_pet/<int:pk>",views.update_pet,name="update_pet"),
    path("delete_pet/<int:pk>",views.delete_pet,name="delete_pet"),
    path("grooming_booking",views.grooming_booking,name="grooming_booking"),

    path("user",views.user,name="user"),
    path("user_update/<int:id>",views.user_update,name="user_update"),
    path("user_delete/<int:id>",views.user_delete,name="user_delete"),

    
    path("merchant",views.merchant,name="merchant"),
    path("merchant_update/<int:id>",views.merchant_update,name="merchant_update"),
    path("merchant_delete/<int:id>",views.merchant_delete,name="merchant_delete"),


    # products
    path("products",views.products,name="products"),
    path("product_update/<int:id>",views.product_update,name="product_update"),
    path("product_delete/<int:id>",views.product_delete,name="product_delete"),
    path("customer_orders",views.customer_orders,name="customer_orders"),
    path("order_status_change/<int:pk>/<str:txt>",views.order_status_change,name="order_status_change"),
    

    path("hospital",views.hospital,name="hospital"),
    path("hospital_update/<int:id>",views.hospital_update,name="hospital_update"),
    path("hospital_delete/<int:id>",views.hospital_delete,name="hospital_delete"),
    path("appointment_booking",views.appointment_booking,name="appointment_booking"),
    path("vaccination",views.vaccination,name="vaccination"),
    path("vaccination_update/<int:id>",views.vaccination_update,name="vaccination_update"),
    path("vaccination_delete/<int:id>",views.vaccination_delete,name="vaccination_delete"),

]