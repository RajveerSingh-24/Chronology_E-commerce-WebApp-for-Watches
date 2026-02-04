from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Product
from .models import Order

def home(request):
    featured_products = Product.objects.filter(featured=True)
    return render(request, 'main/home.html', {'products': featured_products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'main/product_detail.html', {'product': product})

def add_to_cart(request, id):
    cart = request.session.get('cart', {})
    cart[str(id)] = cart.get(str(id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

def cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = quantity * product.price
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'main/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def remove_from_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]
        request.session['cart'] = cart

    return redirect('cart')

def update_cart(request, id, action):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        if action == 'increase':
            cart[str(id)] += 1
        elif action == 'decrease':
            cart[str(id)] -= 1

            if cart[str(id)] <= 0:
                del cart[str(id)]

    request.session['cart'] = cart
    return redirect('cart')


def checkout(request):

    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = quantity * product.price
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    if request.method == "POST":
        name = request.POST['name']
        address = request.POST['address']
        city = request.POST['city']
        phone = request.POST['phone']

        Order.objects.create(
            name=name,
            address=address,
            city=city,
            phone=phone,
            total=total
        )

        request.session['cart'] = {}
        return redirect('success')

    return render(request,'main/checkout.html',{
        'cart_items':cart_items,
        'total':total
    })

def success(request):
    return render(request,'main/success.html')

def contact(request):
    return render(request, 'main/contact.html')