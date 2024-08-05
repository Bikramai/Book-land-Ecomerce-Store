from django.contrib import admin
from .models import (
    OrderItem, Product, ProductVersion, Version, ProductImage, Language, Category, Order, Post, PostCategory, Wishlist,
    Cart, OtherPlatform, Review
)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class VersionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'created_on']


class VersionInline(admin.TabularInline):
    model = ProductVersion
    fields = ['version', 'isbn', 'price']
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['created_on', 'clicks', 'sales', 'likes']
    list_display = ['id', 'name', 'book_type', 'pages', 'sales', 'is_active', 'created_on']
    fieldsets = (
        (None, {'fields': ('thumbnail_image','book_file', 'name', 'description')}),
        ('Writers and Creators', {'fields': ('artist', 'author', 'translator', 'illustrator')}),
        ('Types and Selections', {
            'fields': ('book_type', 'categories', 'languages'),
        }),
        ('Statistics', {'fields': ('pages', 'clicks', 'sales', 'likes')}),
        ('Permissions', {'fields': ('is_active',)}),
        ('Dates', {'fields': ('created_on',)}),
    )
    search_fields = ['name', 'artist', 'author', 'translator', 'illustrator']
    list_filter = ['book_type', 'categories', 'languages']

    inlines = [
        VersionInline
    ]


class ProductVersionAdmin(admin.ModelAdmin):
    list_display = ['id', 'version', 'product', 'isbn', 'price']


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'product']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'product_version', 'qty']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'product_version', 'qty']
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['created_on', 'updated_on', 'total', 'paid']
    list_display = ['id', 'user', 'total', 'paid', 'stripe_payment_id', 'payment_status', 'order_status', 'created_on']
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Shipping Address', {'fields': ('name', 'street_address', 'postal_code', 'city', 'country', 'phone', 'email')}),
        ('Statistics', {'fields': ('total', 'paid')}),
        ('Stripe', {'fields': ('stripe_payment_id', )}),
        ('Status', {'fields': ('payment_status', 'order_status')}),
        ('Dates', {'fields': ('created_on', 'updated_on')}),
    )
    search_fields = ['name']
    list_filter = ['payment_status', 'order_status']

    inlines = [
        OrderItemInline
    ]


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'created_on']


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ['created_on', 'updated_on', 'visits']
    list_display = ['id', 'title', 'author', 'read_time', 'visits', 'status', 'created_on']

    fieldsets = (
        (None, {'fields': ('title', 'thumbnail_image','author', 'read_time')}),
        ('Content', {'fields': ('content',)}),
        ('Permissions', {'fields': ('status', 'category')}),
        ('Statistics', {'fields': ('visits', )}),
        ('Dates', {'fields': ('created_on', 'updated_on')}),
    )
    search_fields = ['id', 'title']
    list_filter = ['status']




@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_on', 'updated_on')
    list_filter = ('rating', 'created_on', 'updated_on')
    search_fields = ('user__username', 'product__name', 'comment')
    raw_id_fields = ('user', 'product')



admin.site.register(Language, LanguageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVersion, ProductVersionAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(OtherPlatform)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Cart)
admin.site.register(Wishlist)
