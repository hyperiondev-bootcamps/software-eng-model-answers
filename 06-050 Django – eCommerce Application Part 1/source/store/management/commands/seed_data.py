from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from store.models import Store, Product, Review
from store.views import ensure_groups_and_permissions


class Command(BaseCommand):
    help = "Seeds database with initial groups, permissions, sample vendors, buyers, and storefronts."

    def handle(self, *args, **options):
        self.stdout.write("Initializing groups and permissions...")
        vendors_group, buyers_group = ensure_groups_and_permissions()

        # Create Admin
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@marketplace.local', 'admin123')
            self.stdout.write(self.style.SUCCESS("Created superuser 'admin' with password 'admin123'"))

        # Create Vendor 1
        v1, created = User.objects.get_or_create(
            username='tech_vendor',
            defaults={'email': 'tech@marketplace.local'}
        )
        if created:
            v1.set_password('vendor123')
            v1.save()
            v1.groups.add(vendors_group)
            content_type = ContentType.objects.get_for_model(Product)
            for code in ['add_products', 'change_products', 'delete_products', 'view_products']:
                perm = Permission.objects.get(codename=code, content_type=content_type)
                v1.user_permissions.add(perm)

        store1, _ = Store.objects.get_or_create(
            name='Tech Gadgets Emporium',
            owner=v1,
            defaults={'description': 'Cutting-edge electronics, computing peripherals, and bespoke mechanical gear.'}
        )

        p1, _ = Product.objects.get_or_create(
            store=store1,
            name='Wireless Mechanical Keyboard',
            defaults={
                'description': 'Compact 75% hot-swappable keyboard with RGB backlight and tactile switches.',
                'price': Decimal('119.99'),
                'stock': 15
            }
        )

        p2, _ = Product.objects.get_or_create(
            store=store1,
            name='Ergonomic Optical Mouse',
            defaults={
                'description': 'Rechargeable wireless ergonomic mouse engineered for all-day wrist comfort.',
                'price': Decimal('49.50'),
                'stock': 24
            }
        )

        p3, _ = Product.objects.get_or_create(
            store=store1,
            name='USB-C Multiport Hub (7-in-1)',
            defaults={
                'description': 'Includes 4K HDMI, 100W Power Delivery, SD Card reader, and high-speed USB 3.0 ports.',
                'price': Decimal('34.99'),
                'stock': 8
            }
        )

        # Create Vendor 2
        v2, created = User.objects.get_or_create(
            username='artisan_crafts',
            defaults={'email': 'crafts@marketplace.local'}
        )
        if created:
            v2.set_password('vendor123')
            v2.save()
            v2.groups.add(vendors_group)
            content_type = ContentType.objects.get_for_model(Product)
            for code in ['add_products', 'change_products', 'delete_products', 'view_products']:
                perm = Permission.objects.get(codename=code, content_type=content_type)
                v2.user_permissions.add(perm)

        store2, _ = Store.objects.get_or_create(
            name='Artisan Leatherworks',
            owner=v2,
            defaults={'description': 'Handcrafted genuine leather wallets, durable travel bags, and custom accessories.'}
        )

        p4, _ = Product.objects.get_or_create(
            store=store2,
            name='Handmade Bifold Leather Wallet',
            defaults={
                'description': 'Full-grain vegetable tanned Italian leather with 8 card slots and cash sleeve.',
                'price': Decimal('45.00'),
                'stock': 12
            }
        )

        p5, _ = Product.objects.get_or_create(
            store=store2,
            name='Artisanal Ceramic Coffee Mug',
            defaults={
                'description': 'Hand-thrown stoneware ceramic mug with a speckled cream glaze (12 oz).',
                'price': Decimal('22.00'),
                'stock': 18
            }
        )

        # Create Buyer 1
        b1, created = User.objects.get_or_create(
            username='buyer_alice',
            defaults={'email': 'alice@marketplace.local'}
        )
        if created:
            b1.set_password('buyer123')
            b1.save()
            b1.groups.add(buyers_group)
            content_type = ContentType.objects.get_for_model(Product)
            perm = Permission.objects.get(codename='view_products', content_type=content_type)
            b1.user_permissions.add(perm)

        # Create Buyer 2
        b2, created = User.objects.get_or_create(
            username='buyer_bob',
            defaults={'email': 'bob@marketplace.local'}
        )
        if created:
            b2.set_password('buyer123')
            b2.save()
            b2.groups.add(buyers_group)
            content_type = ContentType.objects.get_for_model(Product)
            perm = Permission.objects.get(codename='view_products', content_type=content_type)
            b2.user_permissions.add(perm)

        # Sample Reviews
        Review.objects.get_or_create(
            product=p1,
            author=b1,
            defaults={
                'rating': 5,
                'comment': 'Fantastic keyboard! The keystrokes feel smooth and Bluetooth pairs instantly with my MacBook.'
            }
        )

        Review.objects.get_or_create(
            product=p1,
            author=b2,
            defaults={
                'rating': 4,
                'comment': 'Great build quality and very responsive. Battery lasts about 2 weeks on a single charge.'
            }
        )

        Review.objects.get_or_create(
            product=p4,
            author=b1,
            defaults={
                'rating': 5,
                'comment': 'Exquisite craftsmanship. The leather smells genuine and develops a handsome patina quickly.'
            }
        )

        self.stdout.write(self.style.SUCCESS("Database successfully seeded with demo stores, products, reviews, and test accounts!"))

