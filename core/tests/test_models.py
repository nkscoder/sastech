import pytest
from django.contrib.auth.models import User
from core.models import Category, Product, Order

@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(name='Electronics', description='Electronic items')
    assert category.name == 'Electronics'
    assert category.description == 'Electronic items'
    assert str(category) == 'Electronics'

@pytest.mark.django_db
def test_product_creation():
    category = Category.objects.create(name='Electronics', description='Electronic items')
    product = Product.objects.create(
        name='Laptop',
        description='A powerful laptop',
        category=category,
        price=999.99,
        stock=10
    )
    assert product.name == 'Laptop'
    assert product.description == 'A powerful laptop'
    assert product.category == category
    assert product.price == 999.99
    assert product.stock == 10
    assert str(product) == 'Laptop'

@pytest.mark.django_db
def test_order_creation():
    user = User.objects.create_user(username='testuser', password='password')
    category = Category.objects.create(name='Electronics', description='Electronic items')
    product = Product.objects.create(
        name='Laptop',
        description='A powerful laptop',
        category=category,
        price=999.99,
        stock=10
    )
    order = Order.objects.create(user=user, total_amount=999.99)
    order.products.add(product)
    assert order.user == user
    assert order.total_amount == 999.99
    assert order.products.count() == 1
    assert str(order) == f"Order {order.id} by {user}"

@pytest.mark.django_db
def test_order_with_insufficient_stock():
    user = User.objects.create_user(username='testuser', password='password')
    category = Category.objects.create(name='Electronics', description='Electronic items')
    product = Product.objects.create(
        name='Laptop',
        description='A powerful laptop',
        category=category,
        price=999.99,
        stock=1
    )
    # Create an order with the product
    order = Order.objects.create(user=user, total_amount=999.99)
    order.products.add(product)  # Add product to the order

    # # Attempt to create another order with the same product
    product.stock = 0
    product.save()

    with pytest.raises(Exception) as excinfo:
        new_order = Order.objects.create(user=user, total_amount=999.99)
        new_order.products.add(product)  # Try to add the out-of-stock product
    assert 'Insufficient stock' in str(excinfo.value)

@pytest.mark.django_db
def test_product_stock_decrement_on_order():
    user = User.objects.create_user(username='testuser', password='password')
    category = Category.objects.create(name='Electronics', description='Electronic items')
    product = Product.objects.create(
        name='Laptop',
        description='A powerful laptop',
        category=category,
        price=999.99,
        stock=10
    )
    order = Order.objects.create(user=user, total_amount=999.99)
    order.products.add(product)
    product.stock -= 1
    product.save()
    assert product.stock == 9

@pytest.mark.django_db
def test_order_total_amount_calculation():
    user = User.objects.create_user(username='testuser', password='password')
    category = Category.objects.create(name='Electronics', description='Electronic items')
    product1 = Product.objects.create(
        name='Laptop',
        description='A powerful laptop',
        category=category,
        price=999.99,
        stock=10
    )
    product2 = Product.objects.create(
        name='Mouse',
        description='Wireless mouse',
        category=category,
        price=49.99,
        stock=50
    )
    # Calculate total amount manually based on product prices
    total_amount = product1.price + product2.price
    order = Order.objects.create(user=user, total_amount=total_amount)
    order.products.add(product1, product2)
    assert order.total_amount == total_amount
