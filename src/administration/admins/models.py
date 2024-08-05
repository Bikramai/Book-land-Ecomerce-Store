from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from tinymce.models import HTMLField

from src.accounts.models import User
from faker import Faker

fake = Faker()

""" INVENTORY """


class Language(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @classmethod
    def fake(cls, total=10):
        print()
        print("- Langauge: build")
        for x in range(total):
            Language.objects.create(
                name=fake.language_code(),
            )
            print(f"---- Language: {x} faked.")
        print("- END ")
        print()


def book_category_validation(value):
    if not value == "physical" or not value == "digital":
        raise ValidationError("You can only use digital or physical for categories names")

    if Category.objects.count() > 2:
        raise ValidationError("You can only add 2 categories [digital and physical]")

    return value


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    @classmethod
    def fake(cls, total=10):
        print()
        print("- Category: build")
        Category.objects.create(
            name="physical",
        )
        Category.objects.create(
            name="digital",
        )
        print(f"---- Categories: faked.")
        print("- END ")
        print()


class Version(models.Model):
    VERSION_STATUS = (
        ('Digital', 'Digital'),
        ('Physical', 'Physical'),
    )
    name = models.CharField(max_length=255, choices=VERSION_STATUS)

    def __str__(self):
        return self.name

    @classmethod
    def fake(cls, total=2):
        print()
        print("- Version: build")

        Version.objects.get_or_create(name='digital')
        Version.objects.get_or_create(name='physical')

        print(f"---- Version: faked.")
        print("- END ")
        print()


class Product(models.Model):
    BOOK_TYPE_CHOICE = (
        ('Manga', 'Manga'),
        ('Light Novel', 'Light Novel'),
    )

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(null=False, unique=True)
    description = models.TextField(null=True, blank=True)
    thumbnail_image = models.ImageField(upload_to='books/images/thumbnails', null=True, blank=True)
    book_file = models.FileField(blank=True, null=True, upload_to='books/pdf',
                                 help_text="Only pdf files are allowed to upload")

    artist = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    translator = models.CharField(max_length=255)
    illustrator = models.CharField(verbose_name='Editor', max_length=255)

    book_type = models.CharField(max_length=15, default='novel', choices=BOOK_TYPE_CHOICE)
    categories = models.ManyToManyField(Category, verbose_name='Genres')
    languages = models.ManyToManyField(Language)

    pages = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    sales = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    @classmethod
    def fake(cls, total=10):
        print()
        print("- Product: build")
        for x in range(total):
            product = Product.objects.create(
                name=fake.bs(),
                description=fake.paragraph(nb_sentences=1),
                artist=fake.name(),
                author=fake.name(),
                translator=fake.name(),
                illustrator=fake.name(),
                pages=fake.random_number(digits=3, fix_len=False),
                sales=fake.random_number(digits=3, fix_len=False),
                likes=fake.random_number(digits=3, fix_len=False),
                clicks=fake.random_number(digits=3, fix_len=False),
            )
            # categories = Category.objects.order_by('?')[0:2]
            # languages = Category.objects.order_by('?')[0:3]
            # product.languages.bulk_create(languages)
            # product.categories.bulk_create(categories)
            product.save()

            print(f"---- Product: {x} faked.")
        print("- END ")
        print()

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = "Products"

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.thumbnail_image.delete(save=True)
        super(Product, self).delete(*args, **kwargs)

    def get_images(self):
        return ProductImage.objects.filter(product=self)

    def get_versions(self):
        return ProductVersion.objects.filter(product=self)


class ProductVersion(models.Model):
    version = models.ForeignKey(Version, on_delete=models.SET_NULL, null=True, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_version')
    isbn = models.CharField(max_length=255)
    price = models.FloatField(default=0)

    class Meta:
        ordering = ''

    def __str__(self):
        return f"{self.pk}"

    @classmethod
    def fake(cls):
        print()
        print("- ProductVersion: build")
        for product in Product.objects.all():
            for version in Version.objects.all():
                if not ProductVersion.objects.filter(product=product, version=version):
                    ProductVersion.objects.create(
                        version=version,
                        product=product,
                        isbn=fake.isbn10(),
                        price=fake.random_number(digits=3, fix_len=False),
                    )

            print(f"---- ProductVersion: faked.")
        print("- END ")
        print()


class ProductImage(models.Model):
    image = models.ImageField(upload_to='books/images/product_images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')

    class Meta:
        ordering = ['product']
        verbose_name_plural = "Product Images"

    def __str__(self):
        return self.product.name

    def delete(self, *args, **kwargs):
        self.image.delete(save=True)
        super(ProductImage, self).delete(*args, **kwargs)


class OtherPlatform(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_platform')
    image = models.ImageField(upload_to='books/images/other_platform', null=True, blank=True)
    url = models.URLField(null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']
        verbose_name_plural = "Other Platforms"

    def __str__(self):
        return self.product.name

    def delete(self, *args, **kwargs):
        self.image.delete(save=True)
        super(OtherPlatform, self).delete(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_set")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_version = models.ForeignKey(ProductVersion, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    @classmethod
    def get_cart_item_count(cls, user):
        return cls.objects.filter(user=user).count()

    def get_item_price(self):
        return self.quantity * self.product_version.price


""" ORDERS """


class Order(models.Model):
    PAYMENT_STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    ORDER_STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('shipping', 'Shipping'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    SHIPPING_STATUS_CHOICE = (
        ('Free', 'Free'),
        ('Normal', 'Normal'),
        ('Premium', 'Premium'),
    )
    ORDER_COUNTRY = (
        ('USA', 'USA'),
        ('Canada', 'Canada'),
        ('United Kingdom', 'United Kingdom'),
        ('Germany', 'Germany'),
        ('France', 'France'),
        ('Italy', 'Italy'),
        ('Spain', 'Spain'),
        ('Australia', 'Australia'),
        ('Japan', 'Japan'),
        ('China', 'China'),
        ('India', 'India'),
        ('Brazil', 'Brazil'),
        ('South Africa', 'South Africa'),
        ('Mexico', 'Mexico'),
        ('Russia', 'Russia'),
        ('Argentina', 'Argentina'),
        ('Netherlands', 'Netherlands'),
        ('Belgium', 'Belgium'),
        ('Sweden', 'Sweden'),
        ('Norway', 'Norway'),
        ('Denmark', 'Denmark'),
        ('Finland', 'Finland'),
        ('Switzerland', 'Switzerland'),
        ('Austria', 'Austria'),
        ('Greece', 'Greece'),
        ('Turkey', 'Turkey'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('United Arab Emirates', 'United Arab Emirates'),
        ('Singapore', 'Singapore'),
        ('Malaysia', 'Malaysia'),
        ('Philippines', 'Philippines'),
        ('South Korea', 'South Korea'),
        ('New Zealand', 'New Zealand'),
        ('Chile', 'Chile'),
        ('Peru', 'Peru'),
        ('Colombia', 'Colombia'),
        ('Ukraine', 'Ukraine'),
        ('Poland', 'Poland'),
        ('Czech Republic', 'Czech Republic'),
        ('Hungary', 'Hungary'),
        ('Portugal', 'Portugal'),
        ('Israel', 'Israel'),
        ('Egypt', 'Egypt'),
        ('Nigeria', 'Nigeria'),
        ('Kenya', 'Kenya'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255,choices=ORDER_COUNTRY)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    total = models.FloatField(default=0)
    paid = models.FloatField(default=0)

    shipping = models.CharField(max_length=15, choices=SHIPPING_STATUS_CHOICE, default='Free')
    stripe_payment_id = models.CharField(max_length=1000, null=True, blank=True)
    payment_status = models.CharField(max_length=15, choices=PAYMENT_STATUS_CHOICE, default='pending')
    order_status = models.CharField(max_length=15, choices=ORDER_STATUS_CHOICE, default='pending')

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.user.name_or_username()} ordered."

    def order_items(self):
        return OrderItem.objects.filter(order=self)

    @classmethod
    def fake(cls, total=10):
        print()
        print("- Order: build")

        for x in range(total):
            Order.objects.create(
                user=User.objects.order_by('?')[0],
                name=fake.name(),
                street_address=fake.street_address(),
                city=fake.name(),
                postal_code=fake.building_number(),
                country=fake.city(),
                phone=fake.msisdn(),
                email=fake.simple_profile()['mail'],
                total=fake.random_number(digits=3, fix_len=False),
                paid=fake.random_number(digits=3, fix_len=False),
                stripe_payment_id=fake.isbn10(),
            )
            print(f"---- Order {x} : faked.")

        print("- END ")
        print()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_version = models.ForeignKey(ProductVersion, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order} {self.product.name}."

    @classmethod
    def fake(cls):
        print()
        print("- OrderItem: build")

        for order in Order.objects.all():
            products = Product.objects.order_by('?')[0:3]
            for product in products:
                product_version = product.product_version.order_by('?')[0]
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_version=product_version,
                )
                print(f"---- OrderItem {product.pk}: faked.")

        print("- END ")
        print()


""" BLOG DETAILS """


class PostCategory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = 'Post Categories'

    def __str__(self):
        return self.name

    @classmethod
    def fake(cls, total=10):
        print()
        print("- PostCategory: build")
        for x in range(total):
            PostCategory.objects.create(
                name=fake.bs(),
            )
            print(f"---- PostCategory: {x} faked.")
        print("- END ")
        print()


class Post(models.Model):
    STATUS = (
        ('draft', "Draft"),
        ('publish', "Publish")
    )

    title = models.CharField(max_length=255, unique=True)
    thumbnail_image = models.ImageField(upload_to='books/images/posts', null=True, blank=True)
    slug = models.SlugField(unique=True, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(PostCategory, on_delete=models.SET_NULL, blank=False, null=True)
    content = HTMLField()

    read_time = models.PositiveIntegerField(default=0, help_text='read time in minutes')
    visits = models.PositiveIntegerField(default=0)

    status = models.CharField(max_length=15, choices=STATUS, default='publish')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    @classmethod
    def fake(cls, total=10):
        print()
        print("- Post: build")
        for x in range(total):
            Post.objects.create(
                title=fake.sentence(nb_words=8),
                author=User.objects.order_by('?').first(),
                category=PostCategory.objects.order_by('?').first(),
                read_time=fake.random_number(digits=2, fix_len=False),
                visits=fake.random_number(digits=2, fix_len=False),
                content=fake.paragraph(nb_sentences=5),
            )
            print(f"---- Post: {x} faked.")
        print("- END ")
        print()


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @classmethod
    def get_wishlist_item_count(cls, user):
        return cls.objects.filter(user=user).count()

    def __str__(self):
        return f"User : {self.user.email} and Product {self.product.name}"



class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating} Stars)"

    @classmethod
    def fake(cls, total=10):
        print()
        print("- Review: build")
        for x in range(total):
            Review.objects.create(
                user=User.objects.order_by('?').first(),
                product=Product.objects.order_by('?').first(),
                rating=fake.random_element(elements=(1, 2, 3, 4, 5)),
                comment=fake.paragraph(nb_sentences=2),
            )
            print(f"---- Review: {x} faked.")
        print("- END ")
        print()
