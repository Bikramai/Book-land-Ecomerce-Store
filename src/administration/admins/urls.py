from django.urls import pathfrom .views import (    DashboardView, UserOwnUpdateView, UserOwnPasswordChangeView,    UserPasswordResetView, UserListView, UserUpdateView, UserDeleteView, UserDetailView, UserCreateView,    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,    PostCategoryListView, PostCategoryCreateView, PostCategoryUpdateView, PostCategoryDeleteView,    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView, ProductDetailView,    ProductVersionAddView, ProductVersionUpdateView, ProductVersionDeleteView,    ProductImageAddView, ProductImageDeleteView,    OrderListView, OrderDetailView, OrderDeleteView, OrderStatusChangeView,    PostListView, PostCreateView, PostUpdateView, PostDeleteView, PostDetailView,    LanguageListView, LanguageCreateView, LanguageUpdateView, LanguageDeleteView, ProductOtherPlatformAdd,    ProductOtherPlatformDelete)app_name = 'admins'urlpatterns = [    path('', DashboardView.as_view(), name='dashboard'),    path('profile/change/', UserOwnUpdateView.as_view(), name='my-profile-change'),    path('password/change/', UserOwnPasswordChangeView.as_view(), name='my-password-change'),]urlpatterns += [    path('user/', UserListView.as_view(), name='user-list'),    path('user/add/', UserCreateView.as_view(), name='user-add'),    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),    path('user/<int:pk>/change/', UserUpdateView.as_view(), name='user-update'),    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),    path('user/<int:pk>/reset/password/', UserPasswordResetView.as_view(), name='user-password-reset'),]urlpatterns += [    path('category/', CategoryListView.as_view(), name='category-list'),    path('category/add/', CategoryCreateView.as_view(), name='category-add'),    path('category/<int:pk>/change/', CategoryUpdateView.as_view(), name='category-update'),    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),    path('post-category/', PostCategoryListView.as_view(), name='post-category-list'),    path('post-category/add/', PostCategoryCreateView.as_view(), name='post-category-add'),    path('post-category/<int:pk>/change/', PostCategoryUpdateView.as_view(), name='post-category-update'),    path('post-category/<int:pk>/delete/', PostCategoryDeleteView.as_view(), name='post-category-delete'),    path('language-category/', LanguageListView.as_view(), name='language-list'),    path('language-category/add/', LanguageCreateView.as_view(), name='language-add'),    path('language-category/<int:pk>/change/', LanguageUpdateView.as_view(), name='language-update'),    path('language-category/<int:pk>/delete/', LanguageDeleteView.as_view(), name='language-delete'),    path('order/', OrderListView.as_view(), name='order-list'),    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),    path('order/<int:pk>/status/change/', OrderStatusChangeView.as_view(), name='order-status-change'),    path('order/<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),    path('post/', PostListView.as_view(), name='post-list'),    path('post/add/', PostCreateView.as_view(), name='post-add'),    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),    path('post/<int:pk>/change/', PostUpdateView.as_view(), name='post-update'),    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),]urlpatterns += [    path('product/', ProductListView.as_view(), name='product-list'),    path('product/add/', ProductCreateView.as_view(), name='product-add'),    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),    path('product/<int:pk>/change/', ProductUpdateView.as_view(), name='product-update'),    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),    path('product/<int:product_id>/version/add/', ProductVersionAddView.as_view(), name='product-version-add'),    path(        'product/<int:product_id>/version/<int:pk>/change/',        ProductVersionUpdateView.as_view(), name='product-version-update'    ),    path(        'product/<int:product_id>/version/<int:pk>/delete/',        ProductVersionDeleteView.as_view(), name='product-version-delete'    ),    path('product/<int:product_id>/image/add/', ProductImageAddView.as_view(), name='product-image-add'),    path(        'product/<int:product_id>/image/<int:pk>/delete/',        ProductImageDeleteView.as_view(), name='product-image-delete'    ),    path('product/<int:product_id>/platform/add/', ProductOtherPlatformAdd.as_view(), name='product-other-add'),    path('product/<int:product_id>/platform/<int:pk>/delete/', ProductOtherPlatformDelete.as_view(), name='product-other-delete'),]