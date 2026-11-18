import secrets
from datetime import timedelta
from decimal import Decimal
from hashlib import sha1

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage

from .models import Store, Product, Review, ResetToken


# ==============================================================================
# HELPER FUNCTIONS: ROLES & GROUP SETUP
# ==============================================================================

def ensure_groups_and_permissions():
    """
    Ensures 'Vendors' and 'Buyers' groups exist and are seeded with the
    configured product permissions.
    """
    vendors_group, _ = Group.objects.get_or_create(name='Vendors')
    buyers_group, _ = Group.objects.get_or_create(name='Buyers')

    content_type = ContentType.objects.get_for_model(Product)

    # Fetch custom product permissions
    perms = Permission.objects.filter(
        content_type=content_type,
        codename__in=['add_products', 'change_products', 'delete_products', 'view_products']
    )

    for p in perms:
        vendors_group.permissions.add(p)
        if p.codename == 'view_products':
            buyers_group.permissions.add(p)

    return vendors_group, buyers_group


# ==============================================================================
# AUTHENTICATION & REGISTRATION VIEWS
# ==============================================================================

def register_user(request):
    """
    Registers a new user as either a 'Vendor' or a 'Buyer'.
    Automatically assigns the user to the selected Django Group and grants
    default model permissions.
    """
    ensure_groups_and_permissions()

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_conf = request.POST.get('password_conf', '')
        account_type = request.POST.get('account_type', 'Buyer')

        # Form validation
        if not username or not email or not password:
            return render(request, 'store/register.html', {
                'error': 'All fields are required.',
                'username': username,
                'email': email,
                'account_type': account_type
            })

        if password != password_conf:
            return render(request, 'store/register.html', {
                'error': 'Passwords do not match.',
                'username': username,
                'email': email,
                'account_type': account_type
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'store/register.html', {
                'error': f'Username "{username}" is already taken.',
                'email': email,
                'account_type': account_type
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'store/register.html', {
                'error': f'Email "{email}" is already registered.',
                'username': username,
                'account_type': account_type
            })

        # Create user instance and handle password hashing automatically
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Assign user to their selected group and attach permissions
        try:
            if account_type == 'Vendor':
                group = Group.objects.get(name='Vendors')
                user.groups.add(group)
                # Assign vendor permissions
                content_type = ContentType.objects.get_for_model(Product)
                for code in ['add_products', 'change_products', 'delete_products', 'view_products']:
                    perm = Permission.objects.filter(codename=code, content_type=content_type).first()
                    if perm:
                        user.user_permissions.add(perm)
            else:
                group = Group.objects.get(name='Buyers')
                user.groups.add(group)
                # Assign view permission
                content_type = ContentType.objects.get_for_model(Product)
                view_perm = Permission.objects.filter(codename='view_products', content_type=content_type).first()
                if view_perm:
                    user.user_permissions.add(view_perm)
        except Group.DoesNotExist:
            pass

        user.save()

        # Log user in and persist their session
        login(request, user)
        request.session['user_id'] = user.id
        request.session['username'] = user.username

        if account_type == 'Vendor':
            return redirect('store:vendor_dashboard')
        return redirect('store:home')

    return render(request, 'store/register.html')


def login_user(request):
    """
    Authenticates user credentials and establishes a user session.
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            request.session['username'] = user.username

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            # Redirect vendors directly to their dashboard if they own a store
            if user.groups.filter(name='Vendors').exists():
                return redirect('store:vendor_dashboard')
            return redirect('store:home')
        else:
            return render(request, 'store/login.html', {
                'error': 'Invalid credentials. Please verify your username and password.',
                'username': username
            })

    return render(request, 'store/login.html')


def logout_user(request):
    """
    Logs out the user and clears all active session data.
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect('store:login')


# ==============================================================================
# PASSWORD RESET WORKFLOW (Console Email & Secure Token)
# ==============================================================================

def generate_reset_url(request, user):
    """
    Generates a cryptographically secure 16-byte URL-safe token,
    hashes the token using SHA-1 for database persistence, sets a 5-minute
    expiration timestamp, and constructs the recovery URL.
    """
    raw_token = str(secrets.token_urlsafe(16))
    expiry_date = timezone.now() + timedelta(minutes=5)

    # Store hashed token in database for security
    hashed_token = sha1(raw_token.encode()).hexdigest()
    ResetToken.objects.create(
        user=user,
        token=hashed_token,
        expiry_date=expiry_date
    )

    base_url = request.build_absolute_uri('/')[:-1]
    reset_url = f"{base_url}{reverse('store:password_reset', kwargs={'token': raw_token})}"
    return reset_url


def build_email(user, reset_url):
    """
    Constructs an EmailMessage instance containing the recovery link.
    """
    subject = "Password Reset Request - MarketPlace Hub"
    domain_email = "security@marketplacehub.local"
    body = (
        f"Hi {user.username},\n\n"
        f"You requested to reset your password for MarketPlace Hub.\n"
        f"Click the link below or copy and paste it into your browser (expires in 5 minutes):\n\n"
        f"{reset_url}\n\n"
        f"If you did not make this request, you can safely ignore this email.\n"
    )
    email = EmailMessage(subject, body, domain_email, [user.email])
    return email


def send_password_reset(request):
    """
    Accepts user email, locates the user record, generates a tokenized URL,
    and dispatches the email via the configured console backend.
    """
    if request.method == 'POST':
        user_email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email=user_email)
            reset_url = generate_reset_url(request, user)
            email_msg = build_email(user, reset_url)
            email_msg.send()

            return render(request, 'store/password_reset_request.html', {
                'success': f"A reset link has been dispatched to {user_email}. "
                           f"Because this application uses the Console Email Backend for local development, "
                           f"please check your terminal console window to view the generated link."
            })
        except User.DoesNotExist:
            return render(request, 'store/password_reset_request.html', {
                'error': f"No account was found with the email address '{user_email}'."
            })

    return render(request, 'store/password_reset_request.html')


def reset_user_password(request, token):
    """
    Validates the token parameter against stored SHA-1 digests in ResetToken.
    Verifies the 5-minute expiration window, prompts for a new password,
    updates credentials via user.set_password(), and deletes the token upon completion.
    """
    hashed_token = sha1(token.encode()).hexdigest()
    user_token = ResetToken.objects.filter(token=hashed_token, used=False).first()

    # Verify token existence and expiration
    if not user_token:
        return render(request, 'store/password_reset_confirm.html', {
            'error': 'This password reset link is invalid or has already been used.'
        })

    if user_token.expiry_date < timezone.now():
        user_token.delete()
        return render(request, 'store/password_reset_confirm.html', {
            'error': 'This password reset link has expired (links are valid for 5 minutes only).'
        })

    if request.method == 'POST':
        password = request.POST.get('password', '')
        password_conf = request.POST.get('password_conf', '')

        if not password or not password_conf:
            return render(request, 'store/password_reset_confirm.html', {
                'error': 'Please fill out both password fields.',
                'token': token,
                'target_username': user_token.user.username
            })

        if password != password_conf:
            return render(request, 'store/password_reset_confirm.html', {
                'error': 'Passwords do not match.',
                'token': token,
                'target_username': user_token.user.username
            })

        if len(password) < 6:
            return render(request, 'store/password_reset_confirm.html', {
                'error': 'Password must be at least 6 characters long.',
                'token': token,
                'target_username': user_token.user.username
            })

        # Update password and delete used token
        target_user = user_token.user
        target_user.set_password(password)
        target_user.save()

        # Delete token to prevent reuse
        user_token.delete()

        return render(request, 'store/login.html', {
            'success': 'Your password has been reset successfully. Please log in with your new password.'
        })

    return render(request, 'store/password_reset_confirm.html', {
        'token': token,
        'target_username': user_token.user.username
    })


# ==============================================================================
# MARKETPLACE & BUYER VIEWS
# ==============================================================================

def home(request):
    """
    Public landing page allowing visitors and buyers to browse all active stores
    and products available on the platform.
    """
    stores = Store.objects.all()
    products = Product.objects.select_related('store', 'store__owner').all()
    return render(request, 'store/home.html', {
        'stores': stores,
        'products': products
    })


def product_detail(request, product_id):
    """
    Displays full details for an individual product, stock availability,
    the 'Add to Cart' form, and customer reviews.
    """
    product = get_object_or_404(Product.objects.select_related('store', 'store__owner'), pk=product_id)
    reviews = product.reviews.select_related('author').order_by('-created_at')
    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews
    })


@login_required
def add_review(request, product_id):
    """
    Allows authenticated buyers to post a rating and review for a product.
    """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        try:
            rating = int(request.POST.get('rating', 5))
            if rating < 1:
                rating = 1
            elif rating > 5:
                rating = 5
        except ValueError:
            rating = 5

        comment = request.POST.get('comment', '').strip()
        if comment:
            Review.objects.create(
                product=product,
                author=request.user,
                rating=rating,
                comment=comment
            )

    return redirect('store:product_detail', product_id=product.id)


# ==============================================================================
# SHOPPING CART & CHECKOUT VIEWS (Session-Based)
# ==============================================================================

def add_to_cart(request, product_id):
    """
    Adds a specified quantity of a product to the user's session cart.
    Marks session as modified to guarantee database/cookie persistence.
    """
    product = get_object_or_404(Product, pk=product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1

    # Check stock availability
    if product.stock <= 0:
        return redirect('store:product_detail', product_id=product.id)

    # Retrieve existing cart dictionary from session or initialize empty dict
    cart = request.session.get('cart', {})
    prod_id_str = str(product.id)

    current_qty = cart.get(prod_id_str, 0)
    total_requested = current_qty + quantity

    # Cap to available stock
    if total_requested > product.stock:
        total_requested = product.stock

    cart[prod_id_str] = total_requested

    # Save updated cart back to session and mark session as modified
    request.session['cart'] = cart
    request.session.modified = True

    return redirect('store:cart_detail')


def cart_detail(request):
    """
    Inspects items stored in request.session['cart'], looks up matching Product
    records from SQLite, computes line subtotals and grand order total.
    """
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0.00')

    for prod_id_str, quantity in cart.items():
        try:
            product = Product.objects.get(pk=int(prod_id_str))
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
        except (Product.DoesNotExist, ValueError):
            pass

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def update_cart(request, product_id):
    """
    Modifies the quantity of a specific item in the session cart.
    """
    cart = request.session.get('cart', {})
    prod_id_str = str(product_id)

    if request.method == 'POST' and prod_id_str in cart:
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                # Validate against current stock
                product = Product.objects.filter(pk=product_id).first()
                if product and quantity > product.stock:
                    quantity = product.stock
                cart[prod_id_str] = quantity
            else:
                cart.pop(prod_id_str, None)
        except ValueError:
            pass

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('store:cart_detail')


def remove_from_cart(request, product_id):
    """
    Removes an item completely from the session cart.
    """
    cart = request.session.get('cart', {})
    prod_id_str = str(product_id)

    if prod_id_str in cart:
        cart.pop(prod_id_str, None)
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('store:cart_detail')


@login_required
def checkout(request):
    """
    Validates cart stock, deducts inventory levels, generates an itemized invoice,
    dispatches the invoice to the buyer's email via the console backend,
    and flushes the session cart.
    """
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('store:cart_detail')

    cart_items = []
    total = Decimal('0.00')

    # Validate stock before processing
    for prod_id_str, quantity in list(cart.items()):
        try:
            product = Product.objects.get(pk=int(prod_id_str))
            if product.stock < quantity:
                return render(request, 'store/cart.html', {
                    'cart_items': cart_items,
                    'total': total,
                    'error': f'Cannot checkout: Only {product.stock} units of "{product.name}" are available in stock.'
                })
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
        except Product.DoesNotExist:
            cart.pop(prod_id_str, None)

    # Deduct stock and build invoice lines
    invoice_lines = [
        "==================================================",
        "          OFFICIAL PURCHASE INVOICE               ",
        "              MARKETPLACE HUB                     ",
        "==================================================",
        f"Customer: {request.user.username} ({request.user.email})",
        f"Date:     {timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "--------------------------------------------------",
        f"{'Item Name':<28} {'Qty':<5} {'Price':<8} {'Subtotal'}",
        "--------------------------------------------------"
    ]

    for item in cart_items:
        prod = item['product']
        qty = item['quantity']
        # Deduct purchased quantity from inventory
        prod.stock -= qty
        prod.save()

        line = f"{prod.name[:27]:<28} {qty:<5} ${prod.price:<7.2f} ${item['subtotal']:.2f}"
        invoice_lines.append(line)

    invoice_lines.extend([
        "--------------------------------------------------",
        f"TOTAL AMOUNT PAID: ${total:.2f}",
        "==================================================",
        "Thank you for shopping at MarketPlace Hub!",
        "Your order has been processed and your invoice emailed."
    ])

    invoice_text = "\n".join(invoice_lines)

    # Send invoice to buyer via console email backend
    email = EmailMessage(
        subject="Your MarketPlace Hub Order Invoice",
        body=invoice_text,
        from_email="orders@marketplacehub.local",
        to=[request.user.email]
    )
    email.send()

    # Clear cart from session
    request.session['cart'] = {}
    request.session.modified = True

    return render(request, 'store/checkout_success.html', {
        'invoice_text': invoice_text,
        'cart_items': cart_items,
        'total': total,
        'recipient_email': request.user.email
    })


# ==============================================================================
# VENDOR STORE & INVENTORY MANAGEMENT VIEWS
# ==============================================================================

@login_required
def vendor_dashboard(request):
    """
    Displays vendor's store profile, inventory table, and product management actions.
    """
    # Enforce role/permission check
    is_vendor = request.user.groups.filter(name='Vendors').exists() or request.user.has_perm('store.add_products')
    if not is_vendor:
        return render(request, 'store/error.html', {
            'title': 'Access Restricted',
            'message': 'Only registered vendors can access the Vendor Dashboard. Please register or switch to a Vendor account.'
        }, status=403)

    store = Store.objects.filter(owner=request.user).first()
    products = []
    if store:
        products = store.products.all().order_by('name')

    return render(request, 'store/vendor_dashboard.html', {
        'store': store,
        'products': products
    })


@login_required
def create_store(request):
    """
    Allows a vendor without an active store to initialize their storefront.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()

        if not name:
            return render(request, 'store/store_form.html', {
                'error': 'Store name is required.',
                'description': description
            })

        # Ensure user is in Vendors group
        vendors_group, _ = Group.objects.get_or_create(name='Vendors')
        request.user.groups.add(vendors_group)

        store = Store.objects.create(
            name=name,
            description=description,
            owner=request.user
        )
        return redirect('store:vendor_dashboard')

    return render(request, 'store/store_form.html')


@login_required
def add_product(request):
    """
    Allows vendors to add a new product to their store inventory.
    Enforces 'store.add_products' permission.
    """
    # Verify permission
    if not (request.user.has_perm('store.add_products') or request.user.groups.filter(name='Vendors').exists()):
        return render(request, 'store/error.html', {
            'title': 'Permission Denied',
            'message': 'You do not hold permission to add products.'
        }, status=403)

    store = Store.objects.filter(owner=request.user).first()
    if not store:
        return redirect('store:create_store')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        price_str = request.POST.get('price', '').strip()
        stock_str = request.POST.get('stock', '').strip()

        if not name or not price_str or not stock_str:
            return render(request, 'store/product_form.html', {
                'error': 'Name, price, and stock quantity are required.',
                'name': name,
                'description': description,
                'price': price_str,
                'stock': stock_str,
                'action_title': 'Add Product'
            })

        try:
            price = Decimal(price_str)
            stock = int(stock_str)
            if price < 0 or stock < 0:
                raise ValueError("Values cannot be negative.")
        except (ValueError, TypeError):
            return render(request, 'store/product_form.html', {
                'error': 'Please enter valid numerical values for price and stock.',
                'name': name,
                'description': description,
                'price': price_str,
                'stock': stock_str,
                'action_title': 'Add Product'
            })

        Product.objects.create(
            store=store,
            name=name,
            description=description,
            price=price,
            stock=stock
        )
        return redirect('store:vendor_dashboard')

    return render(request, 'store/product_form.html', {
        'action_title': 'Add New Product'
    })


@login_required
def edit_product(request, product_id):
    """
    Allows a vendor to modify an existing product in their store.
    Enforces 'store.change_products' permission and owner verification.
    """
    product = get_object_or_404(Product, pk=product_id)

    # Enforce permission and store ownership
    if not (request.user.has_perm('store.change_products') or request.user.groups.filter(name='Vendors').exists()):
        return render(request, 'store/error.html', {
            'title': 'Permission Denied',
            'message': 'You do not have permission to modify products.'
        }, status=403)

    if product.store.owner != request.user:
        return render(request, 'store/error.html', {
            'title': 'Unauthorized',
            'message': 'You cannot edit products belonging to another vendor.'
        }, status=403)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        price_str = request.POST.get('price', '').strip()
        stock_str = request.POST.get('stock', '').strip()

        if not name or not price_str or not stock_str:
            return render(request, 'store/product_form.html', {
                'error': 'Name, price, and stock quantity are required.',
                'product': product,
                'action_title': f'Edit "{product.name}"'
            })

        try:
            price = Decimal(price_str)
            stock = int(stock_str)
            if price < 0 or stock < 0:
                raise ValueError("Values cannot be negative.")
        except (ValueError, TypeError):
            return render(request, 'store/product_form.html', {
                'error': 'Please enter valid numerical values for price and stock.',
                'product': product,
                'action_title': f'Edit "{product.name}"'
            })

        product.name = name
        product.description = description
        product.price = price
        product.stock = stock
        product.save()

        return redirect('store:vendor_dashboard')

    return render(request, 'store/product_form.html', {
        'product': product,
        'action_title': f'Edit "{product.name}"'
    })


@login_required
def delete_product(request, product_id):
    """
    Allows a vendor to delete a product from their store.
    Enforces 'store.delete_products' permission and owner verification.
    """
    product = get_object_or_404(Product, pk=product_id)

    # Enforce permission and store ownership
    if not (request.user.has_perm('store.delete_products') or request.user.groups.filter(name='Vendors').exists()):
        return render(request, 'store/error.html', {
            'title': 'Permission Denied',
            'message': 'You do not have permission to delete products.'
        }, status=403)

    if product.store.owner != request.user:
        return render(request, 'store/error.html', {
            'title': 'Unauthorized',
            'message': 'You cannot delete products belonging to another vendor.'
        }, status=403)

    if request.method == 'POST':
        product.delete()
        return redirect('store:vendor_dashboard')

    return render(request, 'store/product_confirm_delete.html', {
        'product': product
    })
