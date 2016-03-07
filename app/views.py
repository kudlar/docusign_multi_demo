from flask import Flask, render_template, flash, redirect, session, url_for, request, g, jsonify
from app import app
import os.path
from flask.ext.autoindex import AutoIndex
import py_012_multiple_docs_lib

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home - Multiple Documents--Python')

@app.route('/sent')
def sent():
    r = py_012_multiple_docs_lib.send()
    return render_template('sent.html', title='Sent - Multiple Documents--Python', data=r)

################################################################################
################################################################################

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

