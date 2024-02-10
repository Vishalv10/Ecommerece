from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import UserProfile,Product,Category,CartItem,Cart
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth import logout
from django.db.models import F




# def home(request):
#     return render(request,'home.html')

def home(request):
    # Retrieve all categories from the database
    categories = Category.objects.all()

    # Pass the categories to the context
    context = {
        'categories': categories,
    }

    return render(request, 'home.html', context)


def login1(request):
    return render(request,'login.html')

def registration(request):
    return render(request,'registration.html')


def buyer(request):
    categories = Category.objects.all()
    products = Product.objects.all()  # Assuming you have a queryset for all products
    return render(request, 'buyer.html', {'categories': categories, 'products': products})


def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')

        # Create user in auth_user table
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)

        # Create user profile in UserProfile table
        profile = UserProfile(user=user, contact_number=contact_number, address=address)
        profile.save()

        return redirect('home')  # Redirect to the login page or any other page

    return render(request, 'registration.html')


def login1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('admin_dashboard')
            else:
                login(request, user)
                return redirect('buyer')  # Redirect to the home page or any other page after successful login
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'login.html')


@login_required(login_url='/login/')
def admin_dashboard(request):
    # Check if the user is an admin
    if not request.user.is_staff:
        return redirect('home')  # Redirect to home page if not an admin

    # Retrieve data for the dashboard
    total_users = UserProfile.objects.count()
    total_products = Product.objects.count()
    categories = Category.objects.all()

    return render(request, 'admin_dashboard.html', {
        'total_users': total_users,
        'total_products': total_products,
        'categories': categories,
    })


def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if category_name:
            Category.objects.create(name=category_name)
            return redirect('admin_dashboard')  # Redirect to admin dashboard after adding category

    return render(request, 'add_category.html')


def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')  # Assuming you have a select input for category
        price = request.POST.get('price')
        image = request.FILES.get('image')

        if product_name and description and category_id and price and image:
            category = Category.objects.get(id=category_id)
            Product.objects.create(
                name=product_name,
                description=description,
                category=category,
                price=price,
                image=image
            )
            return redirect('admin_dashboard')  # Redirect to admin dashboard after adding product

    categories = Category.objects.all()
    return render(request, 'add_product.html', {'categories': categories})


def show_products(request):
    products = Product.objects.all()
    return render(request, 'show_products.html', {'products': products})



def delete_product(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if request.method == 'POST':
        product.delete()
        return redirect('show_products')  # Redirect to the product listing page after deletion

    return render(request, 'delete_product.html', {'product': product})



def user_details(request):
    users_with_profile = UserProfile.objects.select_related('user').all()
    return render(request, 'user_details.html', {'users_with_profile': users_with_profile})



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Retrieve or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        # If the item already exists, increment the quantity
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to your cart.")
    return redirect('view_cart')  # Change 'buyer_home' to the actual URL for the buyer's homepage



def view_cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    categories = Category.objects.all()  # Add this line to get all categories

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'categories': categories})


def delete_from_cart(request, item_id):
    cart_items = CartItem.objects.filter(id=item_id, user=request.user)

    if cart_items.exists():
        cart_items.first().delete()
        messages.success(request, "Item removed from your cart.")
    else:
        messages.error(request, "Item not found in your cart.")

    return redirect('view_cart')  # Redirect to the cart page after removing an item


def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to your home page or any other page after logout

class CategoryProductsView(View):
    template_name = 'category_products.html'

    def get(self, request, category_id):
        category = Category.objects.get(pk=category_id)
        products = Product.objects.filter(category=category)
        return render(request, self.template_name, {'category': category, 'products': products})



def categories(request):
    categories_list = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories_list})


def category_products(request, category_id):
    category = Category.objects.get(pk=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()  # Add this line to get all categories
    return render(request, 'category_products.html', {'category': category, 'products': products, 'categories': categories})


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    # Decrement the quantity by 1
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        # If quantity is 1, remove the item
        cart_item.delete()

    return redirect('view_cart')  # Redirect back to the cart page





@login_required
def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    categories = Category.objects.all()  # Add this line to get all categories
    return render(request, 'profile.html', {'user_profile': user_profile, 'categories': categories})


def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_details')


def deleteproduct(request):
    return render(request,'delete_product.html')








