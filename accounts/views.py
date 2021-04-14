from django.shortcuts import render, redirect

# Create your views here.
from .models import Product, Order, Customer
from .forms import OrderForm


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


def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})


def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()

    return render(request, 'accounts/customer.html', {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders
    })


def createOrder(request):
    form = OrderForm()

    if request.method == 'POST':
        # print("print request: ",  request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'accounts/order_form.html', {
        'form': form
    })


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


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    return render(request, 'accounts/delete.html', {'item': order})
