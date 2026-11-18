# Failure Mode and Recovery Strategy
## eCommerce Web Application (Part 1)

### 1. Overview
In web development, edge cases and user errors are inevitable. A robust system must gracefully handle unexpected input, missing data, and concurrent operations without crashing or exposing raw stack traces.

This document identifies five primary operational failure scenarios and defines the corresponding error detection mechanisms, user-facing recovery guidance, and system safeguards.

---

### 2. Failure Scenarios and Recovery Matrix

| Scenario | Trigger / Root Cause | System Response & User Message | Recovery Action / Fallback |
| :--- | :--- | :--- | :--- |
| **1. Invalid Login Credentials** | User submits mistyped username or wrong password. | Renders the login template with HTTP 200/400 and displays an inline alert: *"Invalid credentials. Please verify your username and password."* | Retains username in form; offers a direct link to the *"Forgot Password?"* recovery workflow. |
| **2. Insufficient / Out-of-Stock Items** | Buyer attempts to add or checkout more quantity than currently available in `product.stock`. | Form prevents submission if quantity > stock. If stock drops before checkout, checkout aborts with alert: *"Sorry, only X units of [Item] are currently available."* | Cart quantity is capped to the maximum available stock; prompts the user to adjust the order before retrying. |
| **3. Empty Cart Checkout Attempt** | User navigates directly to `/cart/checkout/` with no items stored in `request.session['cart']`. | Redirects immediately to `/cart/` with a friendly informational message: *"Your shopping cart is currently empty. Browse our marketplace to add items!"* | Displays a button directing the user back to the home product catalogue (`reverse('store:home')`). |
| **4. Expired or Invalid Reset Token** | User clicks a password reset link after the 5-minute TTL has elapsed, or clicks a previously consumed link. | Deletes expired record from `ResetToken` table and renders recovery page with message: *"This password reset link is invalid or has expired (links expire after 5 minutes)."* | Provides a direct button: *"Request a New Reset Link"* pointing to `reverse('store:password_reset_request')`. |
| **5. Missing Database Objects (404 Not Found)** | User requests a product, store, or review with a non-existent primary key or URL parameter. | Catches `DoesNotExist` exceptions (or uses `get_object_or_404`) and renders a polite error page: *"The requested product or store could not be found."* | Gracefully displays a *"Return to Marketplace"* link without raising unhandled 500 server errors. |

---

### 3. Detailed Failure Workflows

#### 3.1 Authentication Failure
```python
user = authenticate(request, username=username, password=password)
if user is not None:
    login(request, user)
    return redirect('store:home')
else:
    # Safe error handling: Do not specify whether username or password failed (prevents account enumeration)
    return render(request, 'store/login.html', {
        'error': 'Invalid username or password. Please try again or reset your password.',
        'submitted_username': username
    })
```

#### 3.2 Inventory Stock Depletion on Checkout
```python
for item in cart_items:
    product = item['product']
    requested_qty = item['quantity']
    if product.stock < requested_qty:
        return render(request, 'store/cart.html', {
            'error': f'Insufficient stock for "{product.name}". Only {product.stock} available.',
            'cart': cart_items,
            'total': total_price
        })
```

#### 3.3 Password Reset Expiration Check
```python
# Check token existence and expiration
user_token = ResetToken.objects.filter(token=hashed_token, used=False).first()
if not user_token:
    return render(request, 'store/password_reset_confirm.html', {
        'error': 'This reset token is invalid or has already been used.'
    })

# Check if 5-minute window has passed
if timezone.now() > user_token.expiry_date:
    user_token.delete()  # Clean up expired token
    return render(request, 'store/password_reset_confirm.html', {
        'error': 'This password reset link has expired. Reset links are only valid for 5 minutes.'
    })
```

#### 3.4 Missing Database Record Handling
```python
try:
    product = Product.objects.get(pk=product_id)
except Product.DoesNotExist:
    return render(request, 'store/error.html', {
        'title': 'Product Not Found',
        'message': 'The product you are looking for does not exist or may have been removed by the vendor.'
    }, status=404)
```

---

### 4. Session Resilience & Edge Cases
- **Session Expiry**: Sessions are configured to persist user shopping data while active, but will handle expired sessions by smoothly initializing an empty cart dictionary `{}` rather than throwing a `KeyError`.
- **Session Mutation Flag**: Whenever the cart dictionary is altered, views explicitly set `request.session.modified = True` to guarantee that Django serializes and persists modifications back to the session store.

