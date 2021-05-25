import sqlite3
from flask import Blueprint, render_template, request, flash, url_for, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_contact(contact_id):
     conn = get_db_connection()
     contact = conn.execute('SELECT * FROM contacts WHERE id =?',(contact_id,)).fetchone()
     conn.close()
     if contact is None:
         abort(404)
     return contact

auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    conn = get_db_connection()
    contacts = conn.execute('SELECT * FROM contacts').fetchall()
    conn.close()
    
    return render_template("home.html", contacts=contacts)


@auth.route('/addcontact', methods=('GET', 'POST'))
def add_contact():
    if request.method == 'POST':
        firstName= request.form['firstName']
        lastName= request.form['lastName']
        email= request.form['email']
        phone= request.form['phone']


        if not firstName :
            flash('First Name is required!')
        if not lastName :
            flash('Last Name is required!')
        if not email :
            flash('Email is required!')
        if not phone :
            flash('Phone Number  is required!')
        elif len(email)< 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 2 characters', category='error')
        elif len(lastName) < 2:
            flash('Last name must be greater than 2 characters', category='error')
        elif len(phone) < 4:
            flash('Phone number must be greater than 4 digits', category='error')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO contacts (firstName,lastName,email,phone) Values (?,?,?,?)',(firstName,lastName,email,phone))
            conn.commit()
            conn.close()
            flash('Contact added!', category="success")
            return redirect(url_for('auth.index'))
    return render_template("add.html")


@auth.route('<int:id>/edit_contact', methods=('GET', 'POST'))
def edit_contact(id):
    contact= get_contact(id)

    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        phone = request.form['phone']

        if not (firstName or lastName or email or phone):
            flash('All spaces must be filled!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE contacts SET firstName=?, lastName=?, email=?, phone=?' 'WHERE id=?', (firstName,lastName,email,phone,id))
            conn.commit()
            conn.close()
            return redirect(url_for('auth.index'))

    return render_template("edit.html", contact=contact)


@auth.route('/<int:contact_id>/')
def retrieve_contact(contact_id):
    contact = get_contact(contact_id)
    return render_template("retrieve.html", contact=contact)


@auth.route('/deletecontact')
def delete_contact():
    return render_template("delete.html")

@auth.route('/<int:contact_id>')
def contact(contact_id):
    contact = get_contact(contact_id)
    return render_template('contact.html', contact=contact)