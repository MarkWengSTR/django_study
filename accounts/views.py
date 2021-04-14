from django.shortcuts import render

# Create your views here.
from .models import Product, Order, Customer


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    return render(request, 'accounts/dashboard.html',
                  {
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


def customer(request):
    return render(request, 'accounts/customer.html')
