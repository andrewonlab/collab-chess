#!/user/bin/env python

"""
Feb-6-2015

@author: Andrew Lee
    
    Python server to handle clients

    Refer to: http://docs.cherrypy.org/en/latest/tutorials.html
    for web server tutorials using cherrypy
"""

import cherrypy as cher

class HelloWorld(object):
    @cher.expose
    def index(self):
        return file('webpage/index.html') 

if __name__ == '__main__':
    cher.quickstart(HelloWorld())

