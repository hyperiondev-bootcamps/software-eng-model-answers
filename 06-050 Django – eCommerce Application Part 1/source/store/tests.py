import re
from datetime import timedelta
from decimal import Decimal
from hashlib import sha1

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core import mail

from .models import Store, Product, Review, ResetToken
from .views import ensure_groups_and_permissions


class RoleAndAuthenticationTests(TestCase):
    def setUp(self):
        ensure_groups_and_permissions()
        self.client = Client()

    def test_vendor_registration(self):
        """Test registering as a Vendor assigns the user to the Vendors group."""
        response = self.client.post(reverse('store:register'), {
            'username': 'merchant_bob',
            'email': 'bob@example.com',
            'password': 'password123',
            'password_conf': 'password123',
            'account_type': 'Vendor'
        })
        self.assertRedirects(response, reverse('store:vendor_dashboard'))

        user = User.objects.get(username='merchant_bob')
        self.assertTrue(user.groups.filter(name='Vendors').exists())
        self.assertTrue(user.has_perm('store.add_products'))
        self.assertTrue(user.has_perm('store.change_products'))
        self.assertTrue(user.has_perm('store.delete_products'))
        self.assertTrue(user.has_perm('store.view_products'))

    def test_buyer_registration(self):
        """Test registering as a Buyer assigns the user to the Buyers group."""
        response = self.client.post(reverse('store:register'), {
            'username': 'shopper_alice',
            'email': 'alice@example.com',
            'password': 'password123',
            'password_conf': 'password123',
            'account_type': 'Buyer'
        })
        self.assertRedirects(response, reverse('store:home'))

        user = User.objects.get(username='shopper_alice')
        self.assertTrue(user.groups.filter(name='Buyers').exists())
        self.assertTrue(user.has_perm('store.view_products'))
        self.assertFalse(user.has_perm('store.add_products'))

    def test_user_login_and_session(self):
        """Test login updates session with user attributes."""
        User.objects.create_user(username='john', email='john@example.com', password='secretpassword')
        response = self.client.post(reverse('store:login'), {
            'username': 'john',
            'password': 'secretpassword'
        })
        self.assertRedirects(response, reverse('store:home'))
        self.assertEqual(self.client.session['username'], 'john')

    def test_invalid_login(self):
        """Test invalid credentials render an error message."""
        response = self.client.post(reverse('store:login'), {
            'username': 'nonexistent',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid credentials')


class PasswordResetTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='samuel',
            email='samuel@example.com',
            password='oldpassword123'
        )

    def test_password_reset_flow(self):
        """Test the end-to-end tokenized password reset flow."""
        # 1. Request reset
        response = self.client.post(reverse('store:password_reset_request'), {
            'email': 'samuel@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A reset link has been dispatched')
        self.assertEqual(len(mail.outbox), 1)

        email_body = mail.outbox[0].body
        match = re.search(r'/reset_password/([a-zA-Z0-9_\-]+)/', email_body)
        self.assertIsNotNone(match)
        token = match.group(1)

        # Check DB record
        hashed_token = sha1(token.encode()).hexdigest()
        token_record = ResetToken.objects.get(token=hashed_token)
        self.assertEqual(token_record.user, self.user)

        # 2. Access reset page via URL token
        confirm_url = reverse('store:password_reset', kwargs={'token': token})
        response = self.client.get(confirm_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a New Password')

        # 3. Post new password
        post_response = self.client.post(confirm_url, {
            'password': 'newpassword123',
            'password_conf': 'newpassword123'
        })
        self.assertEqual(post_response.status_code, 200)
        self.assertContains(post_response, 'Your password has been reset successfully')

        # Verify token deleted
        self.assertFalse(ResetToken.objects.filter(token=hashed_token).exists())

        # Verify user can log in with new password
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_expired_token(self):
        """Test expired token rejection and cleanup."""
        # Create an already expired token
        raw_token = "expiredtoken12345"
        hashed = sha1(raw_token.encode()).hexdigest()
        ResetToken.objects.create(
            user=self.user,
            token=hashed,
            expiry_date=timezone.now() - timedelta(minutes=1)
        )

        confirm_url = reverse('store:password_reset', kwargs={'token': raw_token})
        response = self.client.get(confirm_url)
        self.assertContains(response, 'expired')
        self.assertFalse(ResetToken.objects.filter(token=hashed).exists())


class VendorInventoryAndCartTests(TestCase):
    def setUp(self):
        ensure_groups_and_permissions()
        self.client = Client()

        # Vendor
        self.vendor = User.objects.create_user(username='vendor1', email='vendor1@example.com', password='pw')
        vendors_group = Group.objects.get(name='Vendors')
        self.vendor.groups.add(vendors_group)
        content_type = ContentType.objects.get_for_model(Product)
        for code in ['add_products', 'change_products', 'delete_products', 'view_products']:
            perm = Permission.objects.get(codename=code, content_type=content_type)
            self.vendor.user_permissions.add(perm)

        self.store = Store.objects.create(name='Gadget World', description='Tech gear', owner=self.vendor)
        self.product = Product.objects.create(
            store=self.store,
            name='Wireless Headphones',
            description='Noise cancelling',
            price=Decimal('99.99'),
            stock=10
        )

        # Buyer
        self.buyer = User.objects.create_user(username='buyer1', email='buyer1@example.com', password='pw')
        buyers_group = Group.objects.get(name='Buyers')
        self.buyer.groups.add(buyers_group)

    def test_vendor_can_add_product(self):
        self.client.force_login(self.vendor)
        response = self.client.post(reverse('store:add_product'), {
            'name': 'USB Microphone',
            'description': 'Studio quality',
            'price': '49.99',
            'stock': '15'
        })
        self.assertRedirects(response, reverse('store:vendor_dashboard'))
        self.assertTrue(Product.objects.filter(name='USB Microphone').exists())

    def test_buyer_cannot_add_product(self):
        self.client.force_login(self.buyer)
        response = self.client.post(reverse('store:add_product'), {
            'name': 'Hacker Tool',
            'description': 'Disallowed',
            'price': '1.00',
            'stock': '1'
        })
        self.assertEqual(response.status_code, 403)

    def test_session_cart_and_checkout(self):
        # Add to cart
        self.client.post(reverse('store:add_to_cart', kwargs={'product_id': self.product.id}), {
            'quantity': 2
        })
        session = self.client.session
        self.assertIn('cart', session)
        self.assertEqual(session['cart'][str(self.product.id)], 2)

        # View cart
        response = self.client.get(reverse('store:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Wireless Headphones')
        self.assertContains(response, '199.98')

        # Checkout as logged-in buyer
        self.client.force_login(self.buyer)
        # Update session with cart for the logged-in client
        s = self.client.session
        s['cart'] = {str(self.product.id): 2}
        s.save()

        checkout_response = self.client.post(reverse('store:checkout'))
        self.assertEqual(checkout_response.status_code, 200)
        self.assertContains(checkout_response, 'Thank You for Your Order!')

        # Verify stock deducted
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)

        # Verify cart cleared
        self.assertEqual(self.client.session['cart'], {})

        # Verify email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('PURCHASE INVOICE', mail.outbox[0].body)
