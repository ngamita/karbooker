#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# "KarBooker App" -  for Security Team(Dublin Office) and for Employees Travelling to different Countries in Africa . 

# __Author__= Richard Ngamita(ngamita@gmail.com)


import cgi
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import mail



class KarBookerDb(db.Model):
  """
  # This should setup the instance with info of what the Traveler has Booked 
  # Per instance 
  # Watch out for Injection - use the CGI import to shoot this......
  
  """
  traveller = db.UserProperty(required = True)
  trav_name = db.StringProperty()
  country = db.StringProperty()
  email = db.EmailProperty()
  trav_reg_worksite = db.StringProperty()
  created = db.DateTimeProperty(auto_now_add = True)
  updated= db.DateTimeProperty(auto_now_add = True)
  
  
  #check out the use of a picker here for Date time ?? Reasearch this
  arriv_date = db.StringProperty()
  arriv_fli_num = db.StringProperty()
  dep_date = db.StringProperty()
  dep_fli_num = db.StringProperty()
  hotel_addr = db.StringProperty(multiline = True )
  trav_add_comments = db.StringProperty(multiline = True)
  sec_comments_int = db.StringProperty(multiline = True)
  
# Kar Auth Models - still thinking of what and how this will work .   
  
class KarAuthDb(db.Model):
  # Admin here should pick data from the KarBookerDB and do check box to accept or throw out , If no accepted , reason for not accepting + Comments . 
  trans_confirm = db.BooleanProperty()
  driv_name = db.StringProperty()
  # May have to Add different driver DB - so as i can do CRUD on drives 
  driv_contacts = db.StringProperty()
  
  #May have to Add different Car DB - so as i can do crude on Cars 
  veh_type = db.StringProperty()
  sec_comments_ext = db.StringProperty(multiline = True)
  
  
#The MainPage Class - makes page where the User can Login and Logout 
# Note that the main page is a subclass of webapp.RequestHandler and overwrites the get method
  
class MainPage(webapp.RequestHandler):
  
  def get(self):
    user = users.get_current_user()
    url = users.create_login_url(self.request.uri)
    url_linktext = 'Login'
    
    if user:
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
      
    #GQL - very similar to SQL here to query our db and put data into the p_karbooker var .
    #p_karbooker = db.GqlQuery("SELECT * FROM KarBookerDb")
    p_karbooker = KarBookerDb.gql("WHERE traveller = :traveller " ,traveller = users.get_current_user())
    
    
    
    template_values = {
    "p_karbooker": p_karbooker,
    "numberbookings": p_karbooker.count(),
    "user":user,
    "url": url,
    "url_linktext": url_linktext,
    
    }
    
    path = os.path.join(os.path.dirname(__file__),'templates/html/index.html')
    self.response.out.write(template.render(path,template_values))

# This KarBookMe class creates a new BookMe class 
    
class KarBookMe(webapp.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if user:
      p_karbooker = KarBookerDb(
        traveller = users.get_current_user(),
        country = self.request.get('country'),
        email = self.request.get('email'),
        trav_reg_worksite = self.request.get('trav_reg_worksite'),
        trav_name = self.request.get('trav_name'),

        #check out the use of a picker here for Date time ?? Reasearch this
        arriv_date = self.request.get('arriv_date'),
        arriv_fli_num = self.request.get('arriv_fli_num'),
        dep_date = self.request.get('dep_date'),
        dep_fli_num = self.request.get('dep_fli_num'),
        hotel_addr = self.request.get('hotel_addr'),
        trav_add_comments = self.request.get('trav_add_comments'),
        sec_comments_int = self.request.get('sec_comments_int')
      )
      p_karbooker.put()
      self.redirect('/')
    
    
#This KarBookDel class should help Delete the selected Booking item     
class KarBookDel(webapp.RequestHandler):
  def get(self):
    if user:
      raw_id = self.request.get('id')
      id = int(raw_id)
      p_karbooker = KarBookerDb.get_by_id(id)
      p_karbooker.delete()
      self.redirect('/')
    
      
      
    
    
    
def main():
  application = webapp.WSGIApplication([('/', MainPage),
                                        ('/karbook_me',KarBookMe),
                                        ('/karbook_del',KarBookDel)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
