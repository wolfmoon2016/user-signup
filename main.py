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
import webapp2
import re
import cgi
import os
from string import letters
page_header = """
<!DOCTYPE html>

<html>
    <head>
        <style>
            .error, .var1, .var2, .var3, .var4 {
                color: red;
            }
        </style>
    </head>
    <body>
"""
body="""
    <h1>Signup</h1>
        <form action="/add" method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" >
                        <span class="var1">{0}</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password"/>
                        <span  class="var2">{1}</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password"/>
                        <span  class="var3">{2}</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email"/>
                        <span  class="var4">{3}</span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>

"""
page_footer = """
</body>
</html>
"""
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        # error = self.request.get("error")
        # error_element = "<p class='error'>" + error + "</p>" if error else ""
        var1 = self.request.get("var1")
        var2 = self.request.get("var2")
        var3 = self.request.get("var3")
        var4 = self.request.get("var4")
        main_content = body.format(var1,var2,var3,var4)

        content = page_header  +  main_content   + page_footer
        self.response.write(content)



class AddResponse(webapp2.RequestHandler):
    def post(self):
        error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        #  self.redirect("/?var1=val1&var2=val2&")
        # build the string first, of what goes inside redirect
        # e.g. "/?var1=val1&var2=val2" etc
        #build it as you find the errors (or lack of errors)
        # "/?" + "var1=val1&" + "var2=val2&""etc
        #track whether you have found any error
        # hasError = True or False
        # once you have found all the errors, send the whole string with self.redirect


        if not valid_username(username):
            error = "That's not a valid username."
            error_escaped = cgi.escape(error,quote=True)
            self.redirect('/?var1=' + error_escaped)

        if not valid_password(password):
            error ="That wasn't a valid password."
            error_escaped = cgi.escape(error,quote=True)
            self.redirect('/?var2=' + error_escaped)
        elif password != verify:
            error = "Your passwords didn't match."
            error_escaped = cgi.escape(error, quote=True)
            self.redirect('/?var3=' + error_escaped)

        if not valid_email(email):
            error = "That's not a valid email."
            error_escaped = cgi.escape(error, quote=True)
            self.redirect('/?var4=' + error_escaped)

        if error:
             error_escaped = cgi.escape(error, quote=True)
        else:
            self.redirect('/?username=' + username)
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/add', AddResponse)
], debug=True)
