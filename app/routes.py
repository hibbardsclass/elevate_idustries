from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/blog')
def blog():
    return render_template('blog.html')

@main.route('/shop')
def shop():
    products = [
        {"name": "small leaf dragon", "price": 3},
        {"name": "leaf dragon", "price": 5},
        {"name": "large leaf dragon", "price": 15},
    ]
    return render_template('shop.html', products=products)

@main.route('/business')
def business():
    return render_template('business.html')

@main.route('/website-design')
def website_design():
    return render_template('website_design.html')

@main.route('/construction')
def construction():
    return render_template('construction.html')
