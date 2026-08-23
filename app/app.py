from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'pizza-app-secret-key'


# ── Menu item classes (unchanged from original notebook) ──────────────────────

class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class GarlicBread(MenuItem):
    def __init__(self):
        super().__init__('Garlic Bread', 4.99)


class Beverage(MenuItem):
    def __init__(self):
        super().__init__('Beverage', 2.99)


class Pizza(MenuItem):
    def __init__(self, toppings):
        super().__init__('Pizza', 12.99)
        self.toppings = toppings

    def describe(self):
        return f"{' & '.join(self.toppings)} Pizza"


# ── Topping options ────────────────────────────────────────────────────────────

TOPPINGS = {
    '1': 'Mozzarella',
    '2': 'Pepperoni',
    '3': 'Ham',
    '4': 'Pineapple',
    '5': 'Olives',
    '6': 'No Topping',
    '7': 'Mushrooms',
}


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    session.setdefault('order', [])
    return render_template('index.html', order=session['order'])


@app.route('/add/garlic-bread', methods=['POST'])
def add_garlic_bread():
    gb = GarlicBread()
    order = session.get('order', [])
    order.append({'name': gb.name, 'price': gb.price})
    session['order'] = order
    return redirect(url_for('index'))


@app.route('/add/beverage', methods=['POST'])
def add_beverage():
    bev = Beverage()
    order = session.get('order', [])
    order.append({'name': 'Beverage (self-serve)', 'price': bev.price})
    session['order'] = order
    return redirect(url_for('index'))


@app.route('/pizza')
def pizza_page():
    return render_template('pizza.html', toppings=TOPPINGS)


@app.route('/add/pizza', methods=['POST'])
def add_pizza():
    t1 = TOPPINGS.get(request.form.get('topping1'))
    t2 = TOPPINGS.get(request.form.get('topping2'))

    if not t1 or not t2:
        return redirect(url_for('pizza_page'))

    pizza = Pizza([t1, t2])
    order = session.get('order', [])
    order.append({'name': pizza.describe(), 'price': pizza.price})
    session['order'] = order
    return redirect(url_for('index'))


@app.route('/remove/<int:item_index>', methods=['POST'])
def remove_item(item_index):
    order = session.get('order', [])
    if 0 <= item_index < len(order):
        order.pop(item_index)
        session['order'] = order
    return redirect(url_for('index'))


@app.route('/confirm')
def confirm():
    order = session.get('order', [])
    total = round(sum(item['price'] for item in order), 2)
    return render_template('confirm.html', order=order, total=total)


@app.route('/submit', methods=['POST'])
def submit():
    order = session.get('order', [])
    total = round(sum(item['price'] for item in order), 2)
    session.pop('order', None)
    return render_template('thankyou.html', total=total)


@app.route('/cancel', methods=['POST'])
def cancel():
    session.pop('order', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
