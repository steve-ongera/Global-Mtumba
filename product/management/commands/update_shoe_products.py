from django.core.management.base import BaseCommand
from django.utils.text import slugify
from product.models import Product
import random

class Command(BaseCommand):
    help = 'Update product names, descriptions, and prices with shoe-related content'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without making actual changes',
        )

    def handle(self, *args, **kwargs):
        # Shoe-related content templates
        shoe_types = ['Air Max', 'Jordan', 'Runner', 'Boost', 'Classic', 'Zoom', 'Pro', 'Elite', 'Ultra', 'Sport']
        colors = ['Black', 'White', 'Red', 'Blue', 'Grey', 'Navy', 'Green', 'Gold', 'Silver', 'Brown']
        styles = ['Running', 'Training', 'Basketball', 'Casual', 'Sport', 'Street', 'Urban', 'Track', 'Court', 'Gym']
        materials = ['Leather', 'Mesh', 'Canvas', 'Suede', 'Knit', 'Synthetic', 'Textile', 'Nylon']
        features = ['Breathable', 'Lightweight', 'Durable', 'Flexible', 'Cushioned', 'Responsive', 'Supportive', 'Comfortable']
        
        subtitle_templates = [
            "Premium {material} {style} shoes with enhanced comfort",
            "Professional {style} footwear with {feature} design",
            "Modern {style} shoes featuring {feature} technology",
            "Advanced {style} sneakers with {feature} construction",
            "{feature} {material} shoes for {style} excellence",
        ]
        
        description_templates = [
            """Experience ultimate comfort with these {color} {shoe_type} shoes. Crafted from premium {material}, "
            "these {style} shoes feature {feature} technology for optimal performance. The {feature2} design ensures "
            "lasting durability, while the {material2} lining provides exceptional comfort. Perfect for {style} "
            "enthusiasts who demand both style and functionality.""",
            
            """Elevate your {style} game with these sophisticated {shoe_type} shoes. The {color} colorway combines "
            "with {material} construction to deliver a premium look. Features include {feature} technology and "
            "{feature2} support, making them ideal for {style} activities. The {material2} elements add both "
            "durability and style.""",
            
            """Premium {style} footwear reimagined with these {color} {shoe_type} shoes. Built with {material} "
            "for durability, featuring {feature} technology for comfort, and designed with {feature2} elements "
            "for performance. The {material2} components ensure lasting quality, while the modern design keeps "
            "you stylish during any {style} activity."""
        ]

        try:
            products = Product.objects.all()
            total_products = products.count()
            self.stdout.write(f"Found {total_products} products to update")

            for index, product in enumerate(products, 1):
                # Generate random shoe name (max 12 chars)
                shoe_type = random.choice(shoe_types)
                color = random.choice(colors)
                name = f"{color} {shoe_type}"[:12]

                # Generate random price between 900-14000
                price = round(random.uniform(900, 14000), 2)

                # Generate subtitle and description
                subtitle = random.choice(subtitle_templates).format(
                    material=random.choice(materials),
                    style=random.choice(styles),
                    feature=random.choice(features)
                )

                description = random.choice(description_templates).format(
                    color=color,
                    shoe_type=shoe_type,
                    material=random.choice(materials),
                    material2=random.choice(materials),
                    style=random.choice(styles),
                    feature=random.choice(features),
                    feature2=random.choice(features)
                )

                if kwargs['dry_run']:
                    self.stdout.write(f"Would update product {index}/{total_products}:")
                    self.stdout.write(f"  Name: {name}")
                    self.stdout.write(f"  Price: ${price:.2f}")
                    self.stdout.write(f"  Subtitle: {subtitle}")
                    continue

                # Update the product
                product.name = name
                product.price = price
                product.subtitle = subtitle
                product.description = description
                product.save()

                if index % 100 == 0:
                    self.stdout.write(
                        self.style.SUCCESS(f"Updated {index}/{total_products} products...")
                    )

            if not kwargs['dry_run']:
                self.stdout.write(
                    self.style.SUCCESS(f"\nSuccessfully updated all {total_products} products!")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"\nDry run completed for {total_products} products")
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Command failed: {str(e)}')
            )