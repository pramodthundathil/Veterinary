from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserAddForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import admin_only, unauthenticated_user, allowed_users, student_user_check
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .models import Products, Order, Pet
from .forms import UserProfileForm, ProductForm, BookAppointmentForm, VaccinationForm, PetForm
from .models import UserProfile, BookAppointment, Vaccinations
from django.db.models import Q



# Create your views here.
@admin_only
def HomePage(request):
    products = Products.objects.all()

    context = {
        "products":products
    }
    return render(request,"index.html",context)


def user_products(request):

    context = {
        "products":Products.objects.all()
    }
    return render(request,"products.html",context)


import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Products

# Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def buy_now(request, pk):
    product = get_object_or_404(Products, id=pk)

    if request.method == "POST":
        order = Order.objects.create(order_item = product, customer = request.user)
        order.save()
        return redirect("payment_start", pk = pk)

    # Create an order using Razorpay API
    order_data = {
        'amount': product.price * 100,  # Razorpay expects amount in paise (1 INR = 100 paise)
        'currency': 'INR',
        'payment_capture': '1',  # 1 means automatic capture, 0 means manual capture
    }
    razorpay_order = razorpay_client.order.create(data=order_data)
    order_id = razorpay_order['id']

    context = {
        "product": product,
        "order_id": order_id,
        "razorpay_key_id": settings.RAZOR_KEY_ID,
    }
    return render(request, "buynow.html", context)


def payment_start(request,pk):
    product = get_object_or_404(Products, id=pk)

    # Create an order using Razorpay API
    order_data = {
        'amount': product.price * 100,  # Razorpay expects amount in paise (1 INR = 100 paise)
        'currency': 'INR',
        'payment_capture': '1',  # 1 means automatic capture, 0 means manual capture
    }
    razorpay_order = razorpay_client.order.create(data=order_data)
    order_id = razorpay_order['id']

    context = {
        "product": product,
        "order_id": order_id,
        "razorpay_key_id": settings.RAZOR_KEY_ID,
    }
    return render(request,"payment_start.html",context)


from django.http import JsonResponse
from django.conf import settings


def verify_payment(request):
    if request.method == "POST":
        payment_id = request.POST.get('payment_id')
        signature = request.POST.get('razorpay_signature')
        order_id = request.POST.get('order_id')

        params = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            razorpay_client.utility.verify_payment_signature(params)
            # Payment verified, update your order status in the database here
            return JsonResponse({"status": "success"})
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"status": "failure"})


def my_bookings(request):
    orders = Order.objects.filter(completion_status = False, customer = request.user)
    context = {
        "orders":orders
    }
    return render(request,"mybookings.html",context)


def order_history(request):
    orders = Order.objects.filter(completion_status = True, customer = request.user)
    context = {
        "orders":orders
    }
    return render(request,"order_history.html",context)


def hospital_user(request):
    hospitals = User.objects.filter(groups__name = "hospital" )
    context = {
        "hospitals":hospitals
    }
    return render(request,"hospitals.html",context)


def book_appointment(request, pk):
    hospital = User.objects.get(id = pk)
    user = request.user
    form = BookAppointmentForm()
    if request.method == "POST":
        form = BookAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.hospital = hospital
            appointment.user = user
            appointment.save()
            messages.info(request,f"Appointment Booked For {appointment.booking_date} Token Number is {appointment.id}")
            return redirect("my_appointments")

    context = {
        "hospital":hospital,
        "form":form
    }
    return render(request,"book-appointment.html",context)


def my_appointments(request):
    appointment = BookAppointment.objects.filter(user = request.user)
    return render(request,"my_appointments.html",{"appointment":appointment})


def vaccine(request):
    vaccine = Vaccinations.objects.all()
    return render(request,"vaccinations.html",{"vaccine":vaccine})


def my_pets(request):
    form = PetForm()
    pets = Pet.objects.filter(owner = request.user)
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            messages.info(request,"Pet added....")
            return redirect("my_pets")

    context = {
        "form":form,
        "pets":pets
    }
    return render(request,"my_pets.html",context)

def update_pet(request,pk):
    pet = get_object_or_404(Pet, id = pk)
    form = PetForm(instance = pet)
    if request.method== "POST":
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.info(request,"pet updated....")
            return redirect(my_pets)

    context ={
        "form":form
    }
    return render(request,"update_pet.html",context)

def delete_pet(request,pk):
    pet = get_object_or_404(Pet, id= pk)
    pet.delete()
    messages.success(request,"Pet Deleted..")
    return redirect(my_pets)



@login_required(login_url="SignIn")
def AdminIndex(request):
    form = UserAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='staff')
            user.groups.add(group) 
            messages.success(request,"User Registration Successful")
            return redirect("AdminIndex")
        else:
            messages.error(request,"Something went Wrong!!! Try To use password Includes (UPPERCASE, Numbers, Sepecial Characters and Minimum Legth 8  Characters) or User or email id Already Exists")
            return redirect("AdminIndex")
    context = {
        "form":form,
        
    }
    return render(request,"admin/admin_index.html",context)

@unauthenticated_user
def SignIn(request):
    if request.method == "POST":
        uname = request.POST['uname']
        password = request.POST["pswd"]
        user = authenticate(request,username= uname, password = password)
        if user is not None:
            login(request,user)
            return redirect('HomePage')
        else:
            messages.info(request,"Username or Password Incorrect")
            return redirect('SignIn')
    return render(request,"login.html")

@unauthenticated_user
def SignUp(request):
    form = UserAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Successful")
            return redirect("SignIn")
        else:
            messages.error(request,form.errors)
            return redirect("SignUp")
    
    context = {"form":form}
    return render(request,"register.html",context)


def SignOut(request):
    logout(request)
    return redirect("SignIn")



# user admin


def user(request):
    form1 = UserAddForm()
    form2 = UserProfileForm()
    

    users = User.objects.filter(Q(groups__name='users') | Q(groups=None)).distinct()
    if request.method == "POST":
        form1 = UserAddForm(request.POST)
        form2 = UserProfileForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            volunteer = form2.save(commit=False)
            volunteer.user = user
            volunteer.save()
            group = Group.objects.get(name='users')
            user.groups.add(group)
            messages.success(request,"User Registration Successful")
            return redirect("user")
        else:
            messages.error(request,f"Something went Wrong!!! Try To use password Includes (UPPERCASE, Numbers, Sepecial Characters and Minimum Legth 8  Characters) or User or email id Already Exists <br> {form1.errors} <br> {form2.errors}")
            return redirect("user")

    context = { "form1":form1, "form2":form2,"users":users}   
    return render(request,"admin/user-details.html",context)

def user_update(request,id):
    user = User.objects.get(id=id)
    try:
        user_profile = user.user_profile
    except:
        user_profile = UserProfile.objects.create(user = user)
        user_profile.save()
    form1 = UserUpdateForm(instance=user)
    form2 = UserProfileForm(instance=user_profile)
    if request.method == "POST":
        form1 = UserUpdateForm(request.POST, instance=user)
        form2 = UserProfileForm(request.POST, instance=user_profile)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(request,"user Updated Successfully")
            return redirect("user")
        else:
            messages.error(request,"Something went Wrong!!!")
            return redirect("user")
    context = {"form1":form1,"form2":form2, "volunteer":user}
    return render(request,"admin/users-update.html",context)


def user_delete(request,id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request,"User Deleted Successfully")
    return redirect("user")


# merchant  

def merchant(request):
    form1 = UserAddForm()
    form2 = UserProfileForm()
    users = User.objects.filter(groups__name='merchant').distinct()
    if request.method == "POST":
        form1 = UserAddForm(request.POST)
        form2 = UserProfileForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            volunteer = form2.save(commit=False)
            volunteer.user = user
            volunteer.save()
            group = Group.objects.get(name='merchant')
            user.groups.add(group)
            messages.success(request,"Merchant Registration Successful")
            return redirect("merchant")
        else:
            messages.error(request,f"Something went Wrong!!! Try To use password Includes (UPPERCASE, Numbers, Sepecial Characters and Minimum Legth 8  Characters) or User or email id Already Exists <br> {form1.errors} <br> {form2.errors}")
            return redirect("merchant")

    context = { "form1":form1, "form2":form2,"users":users}   
    return render(request,"admin/merchant-details.html",context)

def merchant_update(request,id):
    user = User.objects.get(id=id)
    try:
        user_profile = user.user_profile
    except:
        user_profile = UserProfile.objects.create(user = user)
        user_profile.save()
    form1 = UserUpdateForm(instance=user)
    form2 = UserProfileForm(instance=user_profile)
    if request.method == "POST":
        form1 = UserUpdateForm(request.POST, instance=user)
        form2 = UserProfileForm(request.POST, instance=user_profile)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(request,"Merchant Updated Successfully")
            return redirect("merchant")
        else:
            messages.error(request,"Something went Wrong!!!")
            return redirect("merchant")
    context = {"form1":form1,"form2":form2, "volunteer":user}
    return render(request,"admin/merchant-update.html",context)


def merchant_delete(request,id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request,"User Deleted Successfully")
    return redirect("merchant")

def customer_orders(request):
    orders = Order.objects.filter(order_item__user = request.user )
    return render(request,"merchant/customer_bookings.html",{"orders":orders})

def order_status_change(request, pk, txt):
    order = get_object_or_404(Order,id = pk)
    order.status = txt 
    order.save()

    if txt == "delivered":
        order.completion_status = True
        order.save()
    messages.info(request,"Order Updated")
    return redirect("customer_orders")



# Hospital  

def hospital(request):
    form1 = UserAddForm()
    form2 = UserProfileForm()
    users = User.objects.filter(groups__name='hospital').distinct()
    if request.method == "POST":
        form1 = UserAddForm(request.POST)
        form2 = UserProfileForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            volunteer = form2.save(commit=False)
            volunteer.user = user
            volunteer.save()
            group = Group.objects.get(name='hospital')
            user.groups.add(group)
            messages.success(request,"hospital Registration Successful")
            return redirect("hospital")
        else:
            messages.error(request,f"Something went Wrong!!! Try To use password Includes (UPPERCASE, Numbers, Sepecial Characters and Minimum Legth 8  Characters) or User or email id Already Exists <br> {form1.errors} <br> {form2.errors}")
            return redirect("hospital")

    context = { "form1":form1, "form2":form2,"users":users}   
    return render(request,"admin/hospital-details.html",context)

def hospital_update(request,id):
    user = User.objects.get(id=id)
    try:
        user_profile = user.user_profile
    except:
        user_profile = UserProfile.objects.create(user = user)
        user_profile.save()
    form1 = UserUpdateForm(instance=user)
    form2 = UserProfileForm(instance=user_profile)
    if request.method == "POST":
        form1 = UserUpdateForm(request.POST, instance=user)
        form2 = UserProfileForm(request.POST, instance=user_profile)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(request,"hospital Updated Successfully")
            return redirect("hospital")
        else:
            messages.error(request,"Something went Wrong!!!")
            return redirect("hospital")
    context = {"form1":form1,"form2":form2, "volunteer":user}
    return render(request,"admin/hospital-update.html",context)


def hospital_delete(request,id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request,"Hospital User Deleted Successfully")
    return redirect("hospital")



# merchant 

def MerchantIndex(request):
    return render(request,"merchant/merchant-index.html")


@login_required(login_url='SignIn')
def products(request):
    product = Products.objects.filter(user = request.user)
    form = ProductForm()
   
    if request.method == "POST":
   
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            messages.success(request,"Product Created success")
            return redirect(products)
        else:
            messages.error(request,"Something wrong....")
            return redirect(products)

    context = {
        "products":product,
        "form":form
    }
    return render(request,"merchant/product.html",context)


def product_delete(request,id):
    product = Products.objects.get(id=id)
    product.delete()
    messages.success(request,"Product Deleted Successfully")
    return redirect("products")


def product_update(request,id):
    product = Products.objects.get(id=id)
   
    form1 = ProductForm(instance=product)
    
    if request.method == "POST":
        form1 = ProductForm(request.POST, request.FILES, instance=product)
      
        if form1.is_valid():
            form1.save()
            
            messages.success(request,"Product Updated Successfully")
            return redirect("products")
        else:
            messages.error(request,"Something went Wrong!!!")
            return redirect("products")
    context = {"form1":form1, "product":product}
    return render(request,"merchant/product-update.html",context)





# hospital 

def HospitalIndex(request):
    return render(request,"hospital/hospital-index.html")


def appointment_booking(request):
    appointment = BookAppointment.objects.filter(hospital = request.user)
    return render(request,"hospital/customer_bookings.html",{"appointment":appointment})


def grooming_booking(request):
    appointment = BookAppointment.objects.filter(hospital = request.user, treatment = "Grooming")
    return render(request,"hospital/grooming_bookings.html",{"appointment":appointment})


def vaccination(request):
    form = VaccinationForm()
    vaccinations = Vaccinations.objects.filter(hospital = request.user)
    if request.method == "POST":
   
        form = VaccinationForm(request.POST)
        if form.is_valid():
            vaccine = form.save(commit=False)
            vaccine.hospital = request.user
            vaccine.save()
            messages.success(request,"Vaccine  Created success")
            return redirect(vaccination)

    context = {
        "form":form,
        "vaccinations":vaccinations
    }
    return render(request,"hospital/vaccinations.html",context)


def vaccination_delete(request,id):
    product = Products.objects.get(id=id)
    product.delete()
    messages.success(request,"Vaccine Deleted Successfully")
    return redirect("vaccination")


def vaccination_update(request,id):
    vaccinations = Vaccinations.objects.get(id=id)
   
    form1 = VaccinationForm(instance=vaccinations)
    
    if request.method == "POST":
        form1 = VaccinationForm(request.POST, request.FILES, instance=vaccinations)
      
        if form1.is_valid():
            form1.save()
            
            messages.success(request,"Vaccine Updated Successfully")
            return redirect("vaccination")
        else:
            messages.error(request,"Something went Wrong!!!")
            return redirect("vaccination")
    context = {"form1":form1, "vaccinations":vaccinations}
    return render(request,"hospital/vaccine-update.html",context)
