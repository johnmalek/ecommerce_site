'''
This will include all the authentication routes used for the site
'''
# Blueprint is used to sort our routes
# Render_template is used to render the html pages
# Request is used to get POST data
from flask import Blueprint, render_template, request, flash, url_for, redirect
# Import database handler functions
from .db_main import *
# Import connection variables
from .connections import *

views = Blueprint('views',__name__)


'''
ROUTES TO BE ADDED:

VIEWS:
route for men clothing
  -sub routes for: shirts, sweaters, pants, jerseys, jackets, shoes

route for women clothing
  -sub routes for: skirts, shirts, sweaters, pants, jerseys, jackets, shoes

route for accessories
  -sub route for men
    -sub sub routes: watches, jewelry, bags
  -sub route for women
    -sub sub routes: watches, jewelry, bags
'''

# Create routes
@views.route('/')
def home():
  '''
  Create a route for the Home page

  Functionality:
    view top purchased products
  
  Return:
    home page
  '''
  all_items = find_all_items(collection_1)
  return render_template("home.html", all_items=all_items)


@views.route('/men_clothing')
def men_clothing():
  '''
  Create a route for the men_clothing page

  Functionality:
  add item to cart
 
  Return:
    Display the list of male clothing ONLY
  '''
  return render_template("men_clothing.html")


@views.route('/women_clothing')
def women_clothing():
  '''
  Create a route for the women_clothing page

  Functionality:
  add item to cart
  
  Return:
    Display the list of female clothing ONLY
  '''
  return render_template("women_clothing.html")


@views.route('/accessories')
def accessories():
  '''
  Create a route for the accessories page

  Functionality:
  add item to cart
  
  Return:
    Display and list of male and female assesories
  '''
  return render_template("accessories.html")


@views.route('/contact_us', methods=['POST', 'GET'])
def contact_us():
  '''
  Create a route for the contact_us page

  POST method:
    send a email directly to business email acount
  
  Return:
    contact page
  '''

  if request.method == 'POST':
    # request form data
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    
    # set email fields
    email_sender = os.environ["EMAIL_SENDER"]
    email_password = os.environ["EMAIL_PASSWORD"]
    email_subject = f"{subject} - {name}"
    email_message = message
    
    # configure email feilds
    try:
      em['From'] = email_sender
      em['To'] = email
      em['Subject'] = email_subject
      em.set_content(f"{email_message}")
    except Exception:
      flash('Please fill all fields before submitting!', category='error')
      return render_template("contact_us.html")
      
    # send secure email
    try:
      with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email, em.as_string())
        flash('Email sent!', category='success')
    except Exception:
      flash('There was an error!', category='error')
      flash('Please insert valid Email address!', category='error')
      return render_template("contact_us.html")
      
  return render_template("contact_us.html")


@views.route('/about_us')
def about_us():
  '''
  Create a route for the about_us page

  Return:
    about us page
  '''
  return render_template("about_us.html")

@views.route('/add_new_product', methods=["POST", "GET"])
def addNewProduct():
  '''
  Handle the route to add a new product to the db

  '''
  if request.method == "POST":
    try:
      image = request.files["image"]
    except KeyError:
      flash("No image file found!")
    image_data = image.read()
    # Convert image data to Binary format
    encoded_image = Binary(image_data)
    new_product = {
      "name": request.form["product_name"],
      "price": request.form["product_price"],
      "description": request.form["product_desc"],
      "category": request.form["product_category"],
      "size": request.form["product_size"],
      "image": encoded_image
    }
  
    add_item(collection_1, new_product)
    flash("Item added successfully")
    return render_template("home.html")
  return render_template("new_product.html")
  
  