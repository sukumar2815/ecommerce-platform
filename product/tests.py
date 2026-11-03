from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from product.models import Brand, Category, Product, Review


class ProductRatingTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Shoes', slug='shoes')
        self.brand = Brand.objects.create(name='Test Brand', slug='test-brand')

    def test_avg_rate_uses_saved_rating_when_no_reviews_exist(self):
        product = Product.objects.create(
            name='Sample Shoe',
            flag='New',
            image=SimpleUploadedFile('shoe.png', b'fake-image', content_type='image/png'),
            price=120.0,
            sku='SKU-001',
            subtitle='Sample subtitle',
            description='Sample description',
            quantity=5,
            category=self.category,
            brand=self.brand,
            rating=4.5,
        )

        self.assertEqual(product.avg_rate(), 4.5)

    def test_avg_rate_uses_review_average_when_reviews_exist(self):
        product = Product.objects.create(
            name='Rated Shoe',
            flag='New',
            image=SimpleUploadedFile('shoe-2.png', b'fake-image', content_type='image/png'),
            price=130.0,
            sku='SKU-002',
            subtitle='Sample subtitle',
            description='Sample description',
            quantity=5,
            category=self.category,
            brand=self.brand,
            rating=1.0,
        )

        Review.objects.create(product=product, user=None, rate=5, review='Great')
        Review.objects.create(product=product, user=None, rate=3, review='Okay')

        self.assertEqual(product.avg_rate(), 4.0)
