# eCommerce Web Application (Part 1\)

A Django marketplace supporting vendor stores, product management, reviews, and session-based shopping carts.

The application includes the following features:

- **Role-Based Access Control**: Django `Group` and custom model `Permission` mappings separating **Vendors** (inventory CRUD) from **Buyers** (browsing, reviewing, session shopping cart, and checkout).  
- **Session-Based Cart Management**: Managing a multi-item shopping cart dynamically inside `request.session['cart']` without premature database locking.  
- **Secure Password Reset**: Generating cryptographically secure tokens with 5-minute expiry, SHA-1 database hashing, and link delivery via Django's `ConsoleEmailBackend`.  
- **Checkout & Invoicing**: Atomic stock deduction, itemized invoice text generation, and confirmation email dispatch.

---

## Directory Structure

```
source/
├── Planning/
│   ├── requirements.md              # Functional & non-functional requirements (Vendor & Buyer)
│   ├── ui_wireframes.md             # Text/ASCII wireframe layouts for all core screens
│   ├── security_access_control.md   # RBAC, custom permissions, and password hashing plan
│   └── failure_recovery.md          # Failure modes and recovery strategies
├── ecommerce_project/
│   ├── __init__.py
│   ├── settings.py                  # Configured with store, SQLite, sessions, console email
│   ├── urls.py                      # Root URL router including store.urls
│   ├── asgi.py
│   └── wsgi.py
├── store/
│   ├── migrations/                  # Generated database migrations
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py         # Management command populating demo vendors, stores, products
│   ├── __init__.py
│   ├── admin.py                     # Admin registrations for Store, Product, Review, ResetToken
│   ├── apps.py
│   ├── models.py                    # Store, Product (with custom permissions), Review, ResetToken
│   ├── tests.py                     # Automated test suite covering auth, cart, reset, permissions
│   ├── urls.py                      # App routes for authentication, marketplace, cart, and dashboard
│   └── views.py                     # Views enforcing RBAC, cart sessions, checkout, and reset flow
├── templates/
│   ├── base.html                    # Common layout, dynamic navbar based on user role/session
│   └── store/
│       ├── home.html                # Marketplace browsing all stores & products
│       ├── product_detail.html      # Product info, reviews, add-to-cart form
│       ├── vendor_dashboard.html    # Vendor storefront & product inventory management
│       ├── store_form.html          # Form to create a vendor storefront
│       ├── product_form.html        # Form to add / edit store products
│       ├── product_confirm_delete.html # Confirmation before removing product
│       ├── cart.html                # Shopping cart view with quantity updates & subtotal
│       ├── checkout_success.html    # Invoice confirmation and terminal instructions
│       ├── login.html               # User authentication form
│       ├── register.html            # Registration form with 'Vendor' vs 'Buyer' role selection
│       ├── password_reset_request.html # Form to request reset token via email
│       ├── password_reset_confirm.html # Form to set new password with token validation
│       └── error.html               # Friendly error template for 403 / 404 conditions
├── static/
│   └── css/
│       └── styles.css               # Clean, responsive CSS styling
├── db.sqlite3                       # Initialized SQLite database with seeded data
├── manage.py                        # Django management script
├── requirements.txt                 # Dependencies (Django)
└── research_answers.md              # Practical Task 2 research report (requests, JSON/XML, REST)
```

---

## Quickstart Guide

### 1\. Create the Virtual Environment and Install Requirements

From this directory on macOS / Linux, using Python 3.10+:

```sh
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```
Windows (Command Prompt)

```sh
py -m venv venv
venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```
Windows (PowerShell)

```sh
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
Windows (Git Bash)

```sh
py -m venv venv
source venv/Scripts/activate
python -m pip install -r requirements.txt
```
Once activated, the terminal should display (venv) to indicate that the virtual environment is active.

Note: If PowerShell blocks virtual environment activation, use Command Prompt instead or review the PowerShell execution policy settings.

### 2\. Apply Database Migrations

```sh
python manage.py makemigrations
python manage.py migrate
```

### 3\. Seed Demo Data (Optional but Recommended)

Populates demo stores, products, reviews, and test accounts:

```sh
python manage.py seed_data
```

**Pre-seeded Demo Accounts:**

| Account | Username | Password | Role / Access |
| :---- | :---- | :---- | :---- |
| **Superuser** | `admin` | `admin123` | Django Admin Panel (`/admin`) |
| **Vendor 1** | `tech_vendor` | `vendor123` | Owns "Tech Gadgets Emporium", has 3 products |
| **Vendor 2** | `artisan_crafts` | `vendor123` | Owns "Artisan Leatherworks", has 2 products |
| **Buyer 1** | `buyer_alice` | `buyer123` | Shopper account with sample reviews |
| **Buyer 2** | `buyer_bob` | `buyer123` | Shopper account |

### 4\. Run the Development Server

```sh
python manage.py runserver
```

Visit the marketplace in your browser at: `http://127.0.0.1:8000/`

### 5\. Running the Automated Test Suite

```sh
python manage.py test
```

Run `deactivate` when finished.

All unit tests verify:

- Automatic group and permission assignment upon registration  
- Restricted access control (preventing buyers from modifying vendor inventory)  
- Session-based cart persistence, quantity modifications, and subtotal arithmetic  
- Atomic stock decrement upon checkout and invoice email generation  
- Cryptographic password reset token generation, 5-minute expiration, and one-time invalidation.

---

## Application Features

### 1\. Registration & Automatic Role Assignment

- Go to `/register/`.  
- Choose **Vendor** or **Buyer** in the dropdown.  
- When registering as a **Vendor**, the user is automatically added to the `Vendors` Django Group and granted `store.add_products`, `store.change_products`, `store.delete_products`, and `store.view_products`.  
- When registering as a **Buyer**, the user is added to `Buyers` and receives `store.view_products`.

### 2\. Session Cart & Checkout Flow

- Browse products on the homepage and click **View Details**.  
- Select a quantity and click **Add to Cart**. Items are saved directly in `request.session['cart']`.  
- In `/cart/`, review your items, subtotals, and total. You can update quantities or remove items.  
- Click **Proceed to Checkout**. The view validates stock levels, deducts purchased items from inventory, formats an itemized purchase invoice, sends it via `EmailMessage`, and flushes the session cart.

### 3\. Password Reset via Console Email Backend

- Click **Forgot password?** on the login page (`/password_reset/`).  
- Enter a registered email address (e.g., `tech@marketplace.local` or `alice@marketplace.local`).  
- Check your **terminal console window**. Because `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` is configured in `settings.py`, Django writes the full email and reset link directly to standard output.  
- Copy the reset link from the console into your browser to set a new password. The token is verified against the 5-minute TTL and deleted immediately upon successful password change.