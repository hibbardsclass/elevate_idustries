from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app import db
from app.models import Order, OrderItem, Product

orders = Blueprint('orders', __name__)

@orders.route('/place_order', methods=['GET', 'POST'])
@login_required
def place_order():
    print("Accessing place_order route")  # Debug print
    if request.method == 'POST':
        try:
            shipping_details = request.form['shipping_details']
            total_amount = sum(float(request.form[f'price_{item_id}']) * int(request.form[f'quantity_{item_id}']) for item_id in request.form.getlist('item_ids'))
            order = Order(user_id=current_user.id, shipping_details=shipping_details, total_amount=total_amount)
            db.session.add(order)
            db.session.commit()

            for item_id in request.form.getlist('item_ids'):
                product = Product.query.get(item_id)
                quantity = int(request.form[f'quantity_{item_id}'])
                price = float(request.form[f'price_{item_id}'])
                order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=quantity, price=price)
                db.session.add(order_item)

            db.session.commit()
            flash('Order placed successfully!', 'success')
            return redirect(url_for('orders.order_detail', order_id=order.id))
        except Exception as e:
            flash(f'Error placing order: {e}', 'error')
            return redirect(url_for('orders.place_order'))
    products = Product.query.all()
    return render_template('orders/place_order.html', products=products)

@orders.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    print("Accessing order_detail route")  # Debug print
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('You do not have permission to view this order.', 'error')
        return redirect(url_for('main.index'))
    return render_template('orders/order_detail.html', order=order)

@orders.route('/my_orders')
@login_required
def my_orders():
    print("Accessing my_orders route")  # Debug print
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('orders/my_orders.html', orders=orders)
