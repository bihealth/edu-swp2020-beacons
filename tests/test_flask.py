import pytest
from the_modul.becaon import flask_app
from the_module.beacon import database
from the_module.beacon import common

#to test home(for call html and )
from flask.ext.testing import TestCase


class MyTest(TestCase):
    #test the calling with creating
       def create_app(self):
           return flask_app
    #test the output
       def test_greeting(self):
           self.app.get('/')
           self.assert_template_used('hello.html')
           self.assert_context("greeting", "hello")
#for information for test flask https://github.com/jarus/flask-testing/tree/master/tests




def test_handle ():
    #test to connect data base(setting.database)
    #test to post from database 
    #test diff. bool inputs (occ and bool)
    #test database.handle()
    #test method with post
    response = flask_app.app.test_client().post("/api/1-1-A-A")
    bool1  = True
    bool2 = False
    occ = 


    #pass