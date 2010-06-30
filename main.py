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

# KarBooker App for Security Team and for Employees Travelling to different Countries in Africa . 

# __Author__= Richard Ngamita(ngamita@gmail.com)


import cgi
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db



class KarBookerDb(db.Model):
  #This should setup the instance with info of what the Traveler has Booked 
  # Per instance 
  country = db.StringProperty()
  email = db.StringProperty()
  trav_reg_worksite = db.StringProperty()
  trav_name = db.StringProperty()
  booked_datetime = db.DateTimeProperty()
  
  
  #check out the use of a picker here for Date time ??Reasearch this
  arriv_date = db.DateProperty()
  arriv_fli_num = db.StringProperty()
  dep_date = db.DateProperty()
  dep_fli_num = db.StringProperty()
  hotel_add = db.StringProperty(multiline = True )
  trav_add_comments = db.StringProperty(multiline = True)
  Sec_comments_int = db.StringProperty(multiline = True)
  
  
class KarBookerExtDb(db.Model):
  # Admin here should pick data from the KarBookerDB and do check box to accept or throw out , If no accepted , reason for not accepting + Comments . 
  trans_confirm = db.BooleanProperty()
  driv_name = db.StringProperty()
  # May have to Add different driver DB - so as i can do CRUD on drives 
  driv_contacts = db.StringProperty()
  
  #May have to Add different Car DB - so as i can do crude on Cars 
  veh_type = db.StringProperty()
  sec_comments_ext = db.StringProperty(multiline = True)
  
  
  


class MainHandler(webapp.RequestHandler):

  def get(self):
    #self.response.out.write('Internal Karbooker App!')
    p_karbooker = db.GqlQuery("SELECT * FROM KarBookerDb")
    
    
    
    
    template_values = {
    "p_karbooker":p_karbooker
    
    }
    
    
    
    path = os.path.join(os.path.dirname(__file__),'index.html')
    self.response.out.write(template.render(path,template_values))
    
    
class BookMe(webapp.RequestHandler):
  def post(self):
    karbooker = KarBookerDb()
    karbooker.country = self.request.get('country')
    #Add the KarBooker data from the Form to the DataStore as for now .
    karbooker.put()
    self.redirect("/")
    


def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
