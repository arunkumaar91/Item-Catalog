# Import neccessary files
import httplib2
import string
import random
import json
import requests
from database_setup import User, Base, Category, ListItems
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import session as login_session
from flask import make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Retail Store List Application"

# To connect to database and create database session
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
session.rollback()

######### LOGIN and LOGOUT functionality ###########

# LOGIN


@app.route('/login')
def showLogin():
    """Function used to display login for the application"""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# LOGIN USING GOOGLE CONNECT
@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Function used to login to application using Google Connect"""
    # Validation for the state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

	# Get Authorization code
    code = request.data

    try:
        # Storing Credential Objects
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)

    except FlowExchangeError:
        response = make_response(json.dumps('Failed to update the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Access Token Validation
    access_token = credentials.access_token
    # login_session['credentials'] = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

	# If error occurs pass 500 as status and abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

	# Access Token Verification
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Given User ID doesn't match with the Token's User ID"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

	# validates access token for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Client's token id doesn't match with App token id"), 401)
        print "Client's token id doesn't match with App token id"
        response.headers['Content-Type'] = 'application/json'
        return response

	# To send status 200 for logged in user
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('User is already logged in'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("You are now logged in as %s" % login_session['user_id'])
        return response

    # To Store credentials of user for later use
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Store user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # login_session['provider'] = 'google'
	# Check and store user info if user is not already in user database
    user_id=getUserID(data['email'])
    if not user_id:
        user_id=createUser(login_session)
        login_session['user_id']=user_id
        # return "Login Successful"
        # login_session['user_id']=useremail
        # For generating message for user and send status 200 code
        output = ''
        output += '<h1>Welcome, '
        output += login_session['username']
        output += '!</h1>'
        output += '<img src="'
        output += login_session['picture']
        output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
        flash("You are now logged in as %s" % login_session['username'])
        print "OK"
        # response = make_response(json.dumps(output),200)
        # response.headers['Content-Type'] = 'application/json'
        #return response
        return output

####### Helper Functions #######

# To create new user and add to existing database
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

# Return user data if user is logged in
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user == None:
        flash("Unauthorised user")
        return redirect(url_for('allcategories'))
    return user

# Return user ID
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

##############


# LOGOUT
# To disconnect current user
@app.route('/gdisconnect')
def gdisconnect():
        # if no user is logged in:
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user is not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    # if given token was valid
    if result['status'] == '200':
        '''del login_session['access_token']
        #del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']'''

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


    '''if result['status'] != '200':
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For users currently logged in - 'status' == '200'
        # Reset current user session
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("Successfully disconnected.")
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response = make_response(redirect(url_for('showLogin')))
        response.headers['Content-Type'] = 'application/json'
        return response'''

####################

# It returns JSON endpoint of all users.
@app.route('/user/JSON')
def userJSON():
    items = session.query(User).all()
    return jsonify(User=[i.serialize for i in items])


# Returns JSON endpoint of all categories
@app.route('/categories/JSON')
def categoryJSON():
    items = session.query(Category).all()
    return jsonify(Cat=[i.serialize for i in items])


# Returns JSON endpoint of entire ListItems for specific category
@app.route('/categories/<int:category_id>/list/JSON')
def categoryListJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).first()
    if category == None:
        flash("Category ID is incorrect")
        return redirect(url_for('allcategories'))
    items = session.query(ListItems).filter_by(
        category_id=category_id).all()
    return jsonify(ListItems=[i.serialize for i in items])


# Returns JSON endpoint of specific Listitem for specific category
@app.route('/categories/<int:category_id>/list/<int:list_id>/JSON')
def categoryListspecificJSON(category_id,item_id):
    category = session.query(Category).filter_by(id=category_id).first()
    if category == None:
        flash("Category ID is incorrect")
        return redirect(url_for('allcategories'))
    items = session.query(ListItems).filter_by(id=list_id).first()
    if items == None:
        flash("Item id is incorrect")
        return redirect(url_for('categoryList',category_id=category_id))
    return jsonify(ListItems=[items.serialize])


# To Shows all Items List if user is not logged in else shows Item List created by the user
@app.route('/')
@app.route('/categories')
def allcategories():
    items = session.query(Category).all()
    if 'username' not in login_session:
        return render_template('publiccategory.html', categories=items)
    else:
        items = session.query(Category).filter_by(user_id=login_session['user_id'])
        return render_template('category.html', items=items)

# Creating a new category
@app.route('/categories/new', methods=['GET', 'POST'])
def newCategory():
    # If user not logged in it redirects to login page
    if 'username' not in login_session:
        flash("Please login to create a new category")
        return redirect('/login')
    # Display form to create new category and validates the id given by user
    if request.method == 'POST':
        id=int(request.form['id'])
        items = session.query(Category).all()
        flag = 0
        for i in items:
            if id == i.id:
                flag = 1
                break
        if flag == 1:
            flash("ID has been used already. Please enter a different ID")
            return redirect(url_for('newCategory'))
        else:
            newItem = Category(name=request.form['name'], id=id, user_id=login_session['user_id'])
            session.add(newItem)
            session.commit()
            flash("New Category Item "+newItem.name+" has been created")
            return redirect(url_for('allcategories'))
    else:
        return render_template('newCategory.html')

# To edit category
@app.route('/categories/<int:category_id>/edit',
           methods=['GET', 'POST'])
def editCategory(category_id):
    if 'username' not in login_session:
        flash("Please login to edit category")
        return redirect('/login')
    output=''
    editedItem = session.query(Category).filter_by(id=category_id).first()
    if editedItem == None:
        flash("Category ID is incorrect")
        return redirect(url_for('allcategories'))
    if editedItem.user_id != login_session['user_id']:
        flash("Not authorised to edit the category which is not created by you")
        return redirect(url_for('allcategories'))
    if request.method == 'POST':
        if request.form['name']:
            n=request.form['name']
            output+='Category '
            output+= editedItem.name
            output+=' renamed to '
            output+=n
            editedItem.name = n
        session.add(editedItem)
        session.commit()
        flash(output)
    else:
        return redirect(url_for('allcategories'))
        return render_template(
        'editCategory.html', category_id=category_id, item=editedItem)

# To Delete Category
@app.route('/categories/<int:category_id>/delete',
           methods=['GET', 'POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        flash("Please login to delete category")
        return redirect('/login')
    deleteItem = session.query(Category).filter_by(id=category_id).first()
    if deleteItem == None:
        flash("Category ID is incorrect")
        return redirect(url_for('allcategories'))

    if deleteItem.user_id != login_session['user_id']:
        flash("Not authorised to delete the category which is not created by you.")
        return redirect(url_for('allcategories'))

    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        itemsDelete = session.query(ListItems).filter_by(category_id=category_id).all()

        for i in itemsDelete:
            session.delete(i)
            session.commit()
            flash("Category "+deleteItem.name+" deleted")
            return redirect(url_for('allcategories'))
    else:
        return render_template('deleteCategory.html', item=deleteItem)






# Displays Listitem of specific category
@app.route('/categories/<int:category_id>/list')
def categoryList(category_id):
    category = session.query(Category).filter_by(id=category_id).first()
    if category == None:
        flash("Category ID is incorrect")
        return redirect(url_for('allcategories'))
    creator = getUserInfo(category.user_id)
    items = session.query(ListItems).filter_by(category_id=category_id)
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publiclist.html', category=category, items=items, category_id=category_id, creator=creator)
    else:
        return render_template('list.html', category=category, items=items, category_id=category_id, creator=creator)


# To create new ListItem
@app.route('/categories/<int:category_id>/new', methods=['GET', 'POST'])
def newListItems(category_id):
    if 'username' not in login_session:
        flash("Please login to create new list item")
        return redirect('/login')
    if request.method == 'POST':
        newItem = ListItems(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], subcategory=request.form['subcategory'], category_id=category_id, user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("New list item "+newItem.name+" is created")
        return redirect(url_for('categoryList', category_id=category_id))
    else:
        return render_template('newListItem.html', category_id=category_id)


# Modify specific List Items.
@app.route('/categories/<int:category_id>/<int:list_id>/edit',
           methods=['GET', 'POST'])
def editListItems(category_id, list_id):
    if 'username' not in login_session:
        flash("Please login to modify specific List Item")
        return redirect('/login')
    output=''
    editedItem = session.query(ListItems).filter_by(id=list_id).first()
    if editedItem == None:
        flash("Incorrect List ID")
        return redirect(url_for('categoryList', category_id=category_id))
    if editedItem.category_id != category_id:
        flash("Incorrect Category and List Item")
        return redirect(url_for('allcategories'))
    if editedItem.user_id != login_session['user_id']:
        flash("Not authorized to edit this list item")
        return redirect(url_for('categoryList'))
    if request.method == 'POST':
        if request.form['name']:
            n=request.form['name']
            output+='List Item '
            output+= editedItem.name
            output+=' renamed to '
            output+=n
            editedItem.name = n
        session.add(editedItem)
        session.commit()
        flash(output)
        return redirect(url_for('categoryList', category_id=category_id))
    else:
        return render_template(
            'editlistitem.html', category_id=category_id, list_id=list_id, item=editedItem)


# Deletes specific List Item.
@app.route('/categories/<int:category_id>/<int:list_id>/delete',
           methods=['GET', 'POST'])
def deleteListItems(category_id, list_id):
    if 'username' not in login_session:
        flash("Please Login to delete a specific list item")
        return redirect('/login')
    itemsDelete = session.query(ListItems).filter_by(id=list_id).first()
    if itemsDelete == None:
        flash("Incorrect List id")
        return redirect(url_for('categoryList', category_id=category_id))
    if itemsDelete.category_id != category_id:
        flash("Incorrect Category and List Item")
        return redirect(url_for('allcategories'))
    if itemsDelete.user_id != login_session['user_id']:
        flash("Not authorized to delete this list item")
        return redirect(url_for('categoryList'))
    if request.method == 'POST':
        session.delete(itemsDelete)
        session.commit()
        flash("List item "+itemsDelete.name+" deleted")
        return redirect(url_for('categoryList', category_id=category_id))
    else:
        return render_template('deleteconfirmation.html', item=itemsDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
