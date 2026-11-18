# User Interface Wireframes
## eCommerce Web Application (Part 1)

This document provides plain-text ASCII wireframes illustrating the structural layout, component hierarchy, and navigation patterns for key screens in the eCommerce application.

---

### 1. Global Navigation Bar (Common Header)
Included across all pages via `base.html`:

```text
+-----------------------------------------------------------------------------------------+
| [LOGO] MarketPlace Hub          [Stores & Products]  [Cart (2)]  |  Hi, Alice (Buyer)   |
|                                                                  |  [Logout]            |
+-----------------------------------------------------------------------------------------+
*(When logged in as Vendor: displays [Vendor Dashboard] link)*
*(When unauthenticated: displays [Login] [Register])*
```

---

### 2. Store List & Product Marketplace (Home Page - `home.html`)
The public landing page displaying platform storefronts and featured product cards.

```text
+-----------------------------------------------------------------------------------------+
| [Header / Navigation Bar]                                                               |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  Welcome to MarketPlace Hub                                                             |
|  Discover artisanal products from independent vendor storefronts.                       |
|                                                                                         |
|  +-----------------------------------------------------------------------------------+  |
|  | BROWSE BY STORE                                                                   |  |
|  | +-----------------------+  +-----------------------+  +-----------------------+   |  |
|  | | Tech Gadgets Emporium |  | Artisan Leatherworks  |  | Green Leaf Botanicals |   |  |
|  | | Owner: JohnDoe        |  | Owner: SarahCraft     |  | Owner: PlantLover     |   |  |
|  | | 8 Products Available  |  | 5 Products Available  |  | 12 Products Available |   |  |
|  | +-----------------------+  +-----------------------+  +-----------------------+   |  |
|  +-----------------------------------------------------------------------------------+  |
|                                                                                         |
|  ALL AVAILABLE PRODUCTS                                                                 |
|  +-----------------------+  +-----------------------+  +-----------------------+        |
|  | Mechanical Keyboard   |  | Handmade Wallet       |  | Ceramic Coffee Mug    |        |
|  | Store: Tech Gadgets   |  | Store: Artisan Leather|  | Store: Artisan Leather|        |
|  | Price: $120.00        |  | Price: $45.00         |  | Price: $18.50         |        |
|  | In Stock: 14 units    |  | In Stock: 3 units     |  | In Stock: Out of Stock|        |
|  | [View Details]        |  | [View Details]        |  | [View Details]        |        |
|  +-----------------------+  +-----------------------+  +-----------------------+        |
|                                                                                         |
+-----------------------------------------------------------------------------------------+
| (c) 2026 MarketPlace Hub - eCommerce Application                                       |
+-----------------------------------------------------------------------------------------+
```

---

### 3. Product Detail & Review Page (`product_detail.html`)
Presents in-depth product information, stock status, an add-to-cart form, and customer reviews.

```text
+-----------------------------------------------------------------------------------------+
| [Header / Navigation Bar]                                                               |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  < Back to Marketplace                                                                  |
|                                                                                         |
|  +-----------------------------------------------------------------------------------+  |
|  | PRODUCT DETAILS                                                                   |  |
|  |                                                                                   |  |
|  | Name: Wireless Mechanical Keyboard (RGB)                                          |  |
|  | Sold by: Tech Gadgets Emporium (Owner: JohnDoe)                                   |  |
|  | Price: $120.00 each                                                               |  |
|  | Availability: In Stock (14 items remaining)                                        |  |
|  |                                                                                   |  |
|  | Description:                                                                      |  |
|  | Compact 75% hot-swappable mechanical keyboard featuring pre-lubricated switches,   |  |
|  | double-shot PBT keycaps, and dual Bluetooth 5.1 / 2.4GHz wireless connectivity.   |  |
|  |                                                                                   |  |
|  | +-------------------------------------------------------------------------------+ |  |
|  | | Add to Cart:                                                                 | |  |
|  | | Quantity: [ 1 ] (max 14)       [  ADD TO CART  ]                             | |  |
|  | +-------------------------------------------------------------------------------+ |  |
|  +-----------------------------------------------------------------------------------+  |
|                                                                                         |
|  CUSTOMER REVIEWS & RATINGS                                                             |
|  +-----------------------------------------------------------------------------------+  |
|  | Leave a Review (Logged-in Buyers only):                                           |  |
|  | Rating: [ * * * * * (5 Stars) v ]                                                 |  |
|  | Comment: [ Typing experience is incredible. Battery lasts weeks!                ] |  |
|  |          [ Submit Review ]                                                        |  |
|  +-----------------------------------------------------------------------------------+  |
|                                                                                         |
|  Existing Reviews:                                                                      |
|  - Alice (5/5 Stars): "Amazing build quality and responsive switches!"                 |
|  - Bob (4/5 Stars): "Great keyboard, Bluetooth connects quickly."                       |
|                                                                                         |
+-----------------------------------------------------------------------------------------+
```

---

### 4. Vendor Management Dashboard (`vendor_dashboard.html`)
Restricted vendor workspace for store monitoring and product catalogue CRUD operations.

```text
+-----------------------------------------------------------------------------------------+
| [Header / Navigation Bar]                                                               |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  Vendor Dashboard                                                                       |
|  Store: Tech Gadgets Emporium                                                           |
|  Owner: JohnDoe | Description: Quality electronics, accessories, and computing gear.   |
|                                                                                         |
|  [ + Add New Product to Store ]                                                         |
|                                                                                         |
|  CURRENT PRODUCT INVENTORY                                                              |
|  +-----------------------------------------------------------------------------------+  |
|  | ID | Product Name         | Price    | Stock | Actions                            |  |
|  +----+----------------------+----------+-------+------------------------------------+  |
|  | 01 | Mechanical Keyboard  | $120.00  | 14    | [Edit Product]  [Delete Product]   |  |
|  | 02 | Ergonomic Mouse      | $59.99   | 22    | [Edit Product]  [Delete Product]   |  |
|  | 03 | USB-C Hub Multiport  | $34.50   | 0     | [Edit Product]  [Delete Product]   |  |
|  +----+----------------------+----------+-------+------------------------------------+  |
|                                                                                         |
+-----------------------------------------------------------------------------------------+
```

---

### 5. Shopping Cart & Checkout Page (`cart.html`)
Session-backed order preview with line-item calculations, quantity controls, and checkout trigger.

```text
+-----------------------------------------------------------------------------------------+
| [Header / Navigation Bar]                                                               |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  Your Shopping Cart                                                                     |
|                                                                                         |
|  +-----------------------------------------------------------------------------------+  |
|  | Item Name            | Store        | Unit Price | Qty   | Subtotal | Actions     |  |
|  +----------------------+--------------+------------+-------+----------+-------------+  |
|  | Mechanical Keyboard  | Tech Gadgets | $120.00    | [ 2 ] | $240.00  | [Remove]    |  |
|  | Handmade Leather Mug | Artisan L.   | $18.50     | [ 1 ] | $18.50   | [Remove]    |  |
|  +----------------------+--------------+------------+-------+----------+-------------+  |
|                                              ORDER TOTAL:  $258.50                      |
|                                                                                         |
|  [ Continue Shopping ]                     [  COMPLETE PURCHASE & CHECKOUT  ]            |
|  +-----------------------------------------------------------------------------------+  |
|  *(Checkout issues an itemized email invoice via Django console backend and resets cart)*|
|                                                                                         |
+-----------------------------------------------------------------------------------------+
```

---

### 6. Password Reset Flow (`password_reset_request.html` & `confirm.html`)

#### Step A: Request Link (`password_reset_request.html`)
```text
+-----------------------------------------------------------+
|                   Forgot Password                         |
|  Please enter your account email to receive a reset link: |
|                                                           |
|  Email Address:                                           |
|  [ user@example.com                                     ] |
|                                                           |
|  [ Send Reset Email ]                                     |
|                                                           |
|  < Back to Login                                          |
+-----------------------------------------------------------+
*(Generates secure token, 5-minute expiry, and prints link to console)*
```

#### Step B: Set New Password (`password_reset_confirm.html`)
```text
+-----------------------------------------------------------+
|                   Enter a New Password                    |
|  Account: Alice                                           |
|                                                           |
|  New Password:                                            |
|  [ **********                                           ] |
|                                                           |
|  Confirm New Password:                                    |
|  [ **********                                           ] |
|                                                           |
|  [ Change Password ]                                      |
+-----------------------------------------------------------+
*(Deletes token upon success and redirects to login with confirmation)*
```

