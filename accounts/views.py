from django.shortcuts import render, redirect
from django.forms import inlineformset_factory

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import Group

# Create your views here.
from .models import Product, Order, Customer
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import already_authenticated_user, allowed_users, admin_only


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    return render(request, 'accounts/dashboard.html', {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'pending': pending,
        'delivered': delivered,
    })


@already_authenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userProfile(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    return render(request, 'accounts/user.html', {
        'orders': orders,
        'total_orders': total_orders,
        'pending': pending,
        'delivered': delivered,
    })


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    return render(request, 'accounts/account_settings.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('login')


@already_authenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            # user = form.save()

            # group = Group.objects.get(name='customer')
            # user.groups.add(group)

            # Customer.objects.create(
            #     user=user,
            #     name=user.username,
            # )

            messages.success(request, 'account was created for ' +
                             form.cleaned_data.get('username'))
            return redirect('login')

    return render(request, 'accounts/register.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    total_orders = orders.count()

    cus_filter = OrderFilter(request.GET, queryset=orders)
    orders = cus_filter.qs

    return render(request, 'accounts/customer.html', {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'cus_filter': cus_filter,
    })


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=10)

    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})

    if request.method == 'POST':
        # print("print request: ",  request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    return render(request, 'accounts/order_form.html', {
        'formset': formset
    })


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        # print("print request: ",  request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'accounts/order_form.html', {
        'form': form
    })


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    return render(request, 'accounts/delete.html', {'item': order})
