# System Requirements Specification (SRS)
## eCommerce Web Application (Part 1)

### 1. Project Overview
The goal of this project is to build an accessible, multi-vendor eCommerce web platform using the Django framework. The platform supports two core user personas:
1. **Vendors (Sellers)**: Independent merchants who manage their own virtual storefronts, add items to the market catalogue, update pricing and inventory levels, and track their listings.
2. **Buyers (Shoppers)**: Consumers who explore vendor stores, browse product listings, inspect detailed product specifications, submit customer reviews, manage a session-persisted shopping cart, and perform checkout with email invoice delivery.

---

### 2. User Roles & Personas

| Role | Description | Core Capabilities |
| :--- | :--- | :--- |
| **Anonymous Visitor** | Unauthenticated user browsing the public web pages. | Browse stores, view public product catalogues, view product details, register as a Vendor or Buyer, log in, request password resets. |
| **Buyer (Shopper)** | Authenticated consumer seeking to purchase products. | Browse all products, view product details, add items to session cart, update cart item quantities, submit product reviews, complete checkout, and receive itemized email invoices. |
| **Vendor (Seller)** | Authenticated merchant selling goods on the platform. | Create a dedicated store, view store dashboard, add new products to their store, edit existing product details/prices/stocks, and delete listed products. |
| **Administrator** | Superuser with backend administrative privileges. | Manage all models via the Django admin panel (`/admin`), manage user permissions and groups, and oversee platform activity. |

---

### 3. Functional Requirements

#### 3.1 Authentication & Account Management
- **FR-AUTH-01 (Registration)**: The system shall allow new users to register by supplying a unique username, valid email address, password, password confirmation, and an account role selection ("Vendor" or "Buyer").
- **FR-AUTH-02 (Automatic Role Assignment)**: Upon registration, the system shall automatically assign the user to the corresponding Django Group (`Vendors` or `Buyers`) and grant associated model permissions.
- **FR-AUTH-03 (Authentication)**: Registered users shall authenticate using their username and password. Unsuccessful authentication attempts must display a clear, descriptive error message.
- **FR-AUTH-04 (Session Management)**: Upon successful login, the system shall bind the user's identity to the active session. Logging out shall terminate the session and redirect the user safely.
- **FR-AUTH-05 (Password Reset Request)**: The system shall allow users to request a password reset by submitting their registered email address. The system will generate a secure URL-safe token with a 5-minute expiry and send a reset link to the user's email (routed to the terminal console during development).
- **FR-AUTH-06 (Password Reset Confirmation)**: The system shall validate the reset token from the URL, ensure it is unexpired and unused, and allow the user to set a new password securely.

#### 3.2 Vendor Store & Product Inventory Management
- **FR-VND-01 (Store Creation)**: A user in the `Vendors` group shall be able to create a store by providing a store name and description. Each store is linked to the authenticated vendor as owner.
- **FR-VND-02 (Vendor Dashboard)**: Vendors shall have access to a private dashboard displaying their store profile and a list of all products belonging to their store.
- **FR-VND-03 (Add Product)**: Vendors with the `add_products` permission shall be able to list new products under their store, specifying product name, optional description, unit price, and starting stock count.
- **FR-VND-04 (Edit Product)**: Vendors with the `change_products` permission shall be able to edit product details, including title, description, price, and stock quantity.
- **FR-VND-05 (Delete Product)**: Vendors with the `delete_products` permission shall be able to remove products from their store catalogue with confirmation.
- **FR-VND-06 (Vendor Isolation)**: A vendor cannot modify or delete products or stores belonging to other merchants.

#### 3.3 Buyer Browsing & Product Reviews
- **FR-BYR-01 (Store & Product Discovery)**: Buyers and visitors can browse all active storefronts and see product cards displaying product name, price, stock status, and seller name.
- **FR-BYR-02 (Product Detail View)**: Selecting any product opens its detail page, presenting the full description, price, current stock count, vendor store information, and customer reviews.
- **FR-BYR-03 (Product Reviews)**: Logged-in buyers can submit a rating (1 to 5 stars) and a written review comment for any product. Submitted reviews are immediately appended to the product page.

#### 3.4 Shopping Cart & Checkout (Session-Based)
- **FR-CRT-01 (Session Cart)**: The shopping cart shall be stored within the visitor's Django session (`request.session['cart']`), allowing cart persistence across browsing sessions without requiring immediate database commits.
- **FR-CRT-02 (Add to Cart)**: Buyers can add products and quantities to their cart directly from product detail pages. Adding an existing item shall increment its quantity.
- **FR-CRT-03 (Cart Inspection & Management)**: The cart view shall display each item's name, unit price, quantity, line-item subtotal, and the combined cart total price. Buyers can adjust quantities or remove items.
- **FR-CRT-04 (Checkout & Stock Validation)**: During checkout, the system must verify that sufficient stock exists for every cart item.
- **FR-CRT-05 (Invoice Generation & Emailing)**: Upon successful checkout confirmation, the system generates an itemized text invoice, deducts purchased quantities from inventory stock, sends the invoice to the buyer's email address via Django's `EmailMessage` console backend, and flushes the cart session data.

---

### 4. Non-Functional Requirements

- **NFR-SEC-01 (Data Security & Password Hashing)**: Plaintext passwords must never be stored in the database. All user passwords must be hashed using Django's PBKDF2 algorithm with SHA-256.
- **NFR-SEC-02 (Access Control & Authorization)**: Vendor modification actions must be secured via `@login_required` decorators and explicit permission checks (`user.has_perm('store.add_products')`, etc.) or group membership checks.
- **NFR-REL-01 (Data Consistency)**: Foreign key relations (`CASCADE`) between User, Store, Product, and Review must preserve relational integrity.
- **NFR-USAB-01 (Usability)**: The user interface must be clean, responsive, and clearly communicate error messages, stock alerts, and navigation links appropriate to the active session.
- **NFR-MAINT-01 (Simplicity & Maintainability)**: The project follows standard Django MTV (Model-Template-View) conventions, avoiding heavy external dependencies or redundant JavaScript frameworks.

