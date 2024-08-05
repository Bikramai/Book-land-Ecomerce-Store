def fake_data():
    from src.accounts.models import User
    from .models import (
        Language, Category, Version, Product, ProductVersion,
        PostCategory, Post,
        OrderItem, Order
    )

    # User.fake(total=50)
    # Language.fake()
    # Category.fake()
    # Version.fake()

    # Product.fake(total=50)
    # ProductVersion.fake()
    #
    # Order.fake(50)
    # OrderItem.fake()
    #
    # PostCategory.fake()
    # Post.fake(50)
