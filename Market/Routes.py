from Market import app
from flask import render_template, redirect, url_for, flash, request
from Market.Models import Item, User
from Market.Forms import RegisterForm, LoginForm, PurchaseItemForm, ReturnItemForm
from Market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template("Home.html")


@app.route('/market', methods=["GET", "POST"])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    return_form = ReturnItemForm()
    if request.method == "POST":
        # Purchase Logic
        purchased_item = request.form.get("purchased_item")
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You Have Purchased {p_item_object.name} For ₹ {p_item_object.price}",
                      category="success")
            else:
                flash(f"Sorry You Don't Have Enough Money To Purchase {p_item_object.name}", category="danger")
        # Return Logic
        return_item = request.form.get("return_item")
        s_item_object = Item.query.filter_by(name=return_item).first()
        if s_item_object:
            if current_user.can_return(s_item_object):
                s_item_object.returns(current_user)
                flash(f"You Have Returned {s_item_object.name}",
                      category="success")
            else:
                flash(f"Sorry You Don't Have {s_item_object.name} To Return", category="danger")
        return redirect(url_for('market_page'))
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        purchased_items = Item.query.filter_by(owner=current_user.id)
        return render_template("Market.html", items=items, purchase_form=purchase_form, purchased_items=purchased_items,
                               return_form=return_form)


@app.route('/register', methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Congratulations {user_to_create.username} You Have created Your Account Successfully",
              category='Success')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('Register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email_address=form.email_address.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Welcome {attempted_user.username}", category="success")
            return redirect(url_for("market_page"))
        else:
            flash("Email_address and Password Don't Match, Please Try Again", category="danger")
    return render_template("Login.html", form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You Have Been logged Out Successfully", category="info")
    return redirect(url_for("home_page"))
