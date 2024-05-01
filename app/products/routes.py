from flask import request, redirect, url_for, render_template, flash
from . import products
from app.models import Product, db

@products.route('/')
def home():
    return render_template('home.html')

@products.route('/list')
def list_products():
    product_list = Product.query.all()  # Changed variable name to avoid conflict
    return render_template('list_products.html', products=product_list)

@products.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form.get('description', '')
            price = float(request.form['price'])
            cte_program = request.form['cte_program']

            new_product = Product(name=name, description=description, price=price, cte_program=cte_program)
            db.session.add(new_product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('products.list_products'))
        except Exception as e:
            flash(f'Error adding product: {e}', 'error')
            return redirect(url_for('products.add_product'))
    return render_template('add_products.html')

@products.route('/update/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        try:
            product.name = request.form['name']
            product.description = request.form['description']
            product.price = float(request.form['price'])
            product.cte_program = request.form['cte_program']
            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('products.list_products'))
        except Exception as e:
            flash(f'Error updating product: {e}', 'error')
            return redirect(url_for('products.update_product', id=id))
    return render_template('update_product.html', product=product)

@products.route('/delete/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting product: {e}', 'error')
    return redirect(url_for('products.list_products'))
