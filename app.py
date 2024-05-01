from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/shop')
def shop():
    # Assuming you have a list of products
    products = [
        {"name": "small leaf dragon", "price": 3},
        {"name": "leaf  dragon", "price": 5},
        {"name": "large leaf dragon", "price": 15},
        # Add more products as needed
    ]
    return render_template('shop.html', products=products)


# Business Program Route
@app.route('/business')
def business():
    return render_template('business.html')


# Website Design Program Route
@app.route('/website-design')
def website_design():
    return render_template('website_design.html')


# Construction Program Route
@app.route('/construction')
def construction():
    return render_template('construction.html')


if __name__ == '__main__':
    app.run(debug=True)
