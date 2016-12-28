#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_ror.py
#  
#  Copyright 2012 Ariel Biton <ariel@zplinux.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import sys
import urlparse
import datetime
import _mysql
import time
import datetime
#import codecs

#sys.stdout = codecs.getwriter('utf8')(sys.stdout)

#url 
url= 'index.html?period=day&per_page=20'

#port
if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000

#db connector    
con = None

# return db params from file
def getDBParamsFromfile(filename):
	cfgDB = open(curdir + sep + filename)
	# the order in the file is here important (user then pass then db then host)
	#	( username, password, db, host) = \
	#		[line.split('=')[1].split('\n')[0] for line in cfgDB.readlines()]
	temp = [line.split('=')[1].split('\n')[0] for line in cfgDB.readlines()]
	cfgDB.close()    
	return temp


#db connection
try:
	(username, password, db, host ) = getDBParamsFromfile('database.conf')
	con = _mysql.connect(host, username, password, db)
except _mysql.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit(1)



# -- functions 

# return parameters from url
def getParamFromUrl(url,param):
    params = url.split("?")[1]
    # ie: "GET /index.html?per_page=20&period=month HTTP/1.1" 200 -
    params = params.split(''+param+'=')[1].split('&')[0]
    return params

# prepare mysql request according to parameters
def setMysqlRequest(period, per_page):
	#req = 'select * from test_ror where created_at = "2012-07-23 14:27:49"'
	#req = 'select * from test_ror where '
	if period == 'day':
	#	req = 'SELECT * FROM search_queries WHERE DATE(created_at) = "'+getTimestamp("day")\
		req = 'SELECT * FROM test_ror WHERE DATE(created_at) = "'+getTimestamp("day")\
			+'" LIMIT 0, '+per_page
	else:
	#	req = 'SELECT * FROM search_queries WHERE DATE(created_at) BETWEEN "'\
		req = 'SELECT * FROM test_ror WHERE DATE(created_at) BETWEEN "'\
			+getTimestamp(period)+'" AND "'+getTimestamp("day")\
			+'" LIMIT 0, '+per_page
	#print 'req: ',req, '\nperiod: ', period
	return req


# execute mysql request	
def getDataFromDB(params, con):
	#((period, per_page), (username, password, db, host )) = params
	(period, per_page) = params
	
	mysql_request = setMysqlRequest(period, per_page)

	if con:
		try:
			con.query(mysql_request)
			result = con.use_result()
			record = result.fetch_row()
			if record:
				((phrase, status, created_at),) = record
				res = [(phrase,status, created_at)]
				while True:
					record = result.fetch_row()
					if not record: break
					((phrase, status, created_at),) = record
					res.append((phrase, status, created_at))
					
				return res
			else:
				return [('empty','empty','empty')]
		
		except _mysql.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			sys.exit(1)
	else:
		print "problem with db"

# 404 is seen as not an error, all other status are error
def getStatusClass(status):
	if status == '404':
		return 'status_404'
	else:
		return 'status_error'

# prepare html table
def prepareHtml(res):
	temp = ['<tr><th>Phrase</th><th>Time</th><th>Status</th></tr>']
	for (phrase, status, created_at) in res:
		temp.append('<tr><td>'+phrase.decode('utf-8')\
			+'</td><td>'+created_at\
			+'</td><td class="'+getStatusClass(status)+'">'\
				+status+'</td></tr>') 

	return ''.join(temp)

# get "mysql timestamp" according to when (day, week, month) paramater
def getTimestamp(when):
	format = '%Y-%m-%d'
	today = datetime.datetime.now().strftime(format)
	
	if when == 'day':
		return today
	elif when == 'week':
		t = time.mktime(time.strptime(today,format))
		t = t - (60*60*24*7)
		return str(datetime.datetime.fromtimestamp(int(t)))
	elif when == 'month':
		t = time.mktime(time.strptime(today,format))
		# month is 30 days here
		t = t - (60*60*24*30)
		return str(datetime.datetime.fromtimestamp(int(t)))
	else:
		exit(1)
#print getTimestamp('day')+' / ' + getTimestamp('week') + ' / ' +getTimestamp('month')

# class 

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

	
	# handler for the GET requests
	# it's used after the first loading for the non-ajax version
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"
		table_html = ''

		try:
			#Check the file extension required and
			#set the right mime type

			global con
			global url
			#print 'in GET handler', self.path
			
			# use default url to avoid being without parameters
			if 'period=' in self.path:
				url = self.path
				
			sendReply = False
			if ".html" in self.path:
				
				# receive data from DB according to parameters
				res = getDataFromDB((getParamFromUrl(url, 'period'), \
									getParamFromUrl(url,'per_page')), 
								con)
				
				# pepare html table
				table_html = prepareHtml(res)
					
				self.path="/index.html"
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".png"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				
				# add the table generated from mysql result
				modified_html = f.read().replace('CONTENT', table_html)
				self.wfile.write(modified_html)
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
	
	# handler for the POST requests
	# used in ajax version after first loading in GET
	def do_POST(self):
		#print 'in POST handler'
		length = int(self.headers.getheader('content-length'))        
		data_string = self.rfile.read(length)
		try:
			global con
			global url

			# receive data from DB according to parameters
			res = getDataFromDB((getParamFromUrl(data_string, 'period'), \
						getParamFromUrl(data_string,'per_page')), 
						con)
			# pepare html table
			table_html = prepareHtml(res)
			result = table_html
		except:
			result = 'error'
		self.wfile.write(result)

# server init
			
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('127.0.0.1', port), myHandler)
	print 'Started httpserver on port ' , port
	
	#Wait forever for incoming http requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	# close db conector
	con.close()
	# close socket
	server.socket.close()
	

