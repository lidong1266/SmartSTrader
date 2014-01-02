import os
import sys
import re

import logging

class MySqlConfig:
	def __init__(self, host = 'localhost', port=3306, user='root', password = '', dbname = 'mysql', mysql_sock = '', defaults_file = '', tags = None, options={}):
		self.host = host
		self.port = port
		self.user = user
		self.password = password
		self.mysql_sock = mysql_sock
		self.defaults_file = defaults_file
		self.tags = tags
		self.options = options
		self.dbname = dbname
		
	def get(self, key, default_value):
		if hasattr(self, key):
			return getattr(self, key)
		else:
			return default_value
	
class MySql:
	def __init__(self, name, dbname = ''):
		self.mysql_version = {}
		self.log = logging.getLogger(name)
		self.log.setLevel(logging.WARNING)
		self.cursor = None
		self.db = None
		self.configinstance = None
		self.dbname = dbname
	#def 
	def get_library_versions(self):
		try:
			import MySQLdb
			version = MySQLdb.__version__
		except ImportError:
			version = "Not Found"
		except AttributeError:
			version = "Unknown"
	
		return {"MySQLdb": version}
	
	def check(self, instance):
		host, port, user, password, dbname, mysql_sock, defaults_file, tags, options = self._get_config(instance)
	
		if (not host or not user) and not defaults_file:
			raise Exception("Mysql host and user are needed.")
		
		self.configinstance = instance
		self.db = self._connect(host, port, mysql_sock, user, password, dbname, defaults_file)
		self.cursor = self.db.cursor()
	
	
	def _get_config(self, instance):
		host = instance.get('host', '')
		user = instance.get('user', '')
		print "user", user
		port = int(instance.get('port', 0))
		password = instance.get('pass', '')
		mysql_sock = instance.get('sock', '')
		defaults_file = instance.get('defaults_file', '')
		tags = instance.get('tags', None)
		options = instance.get('options', {})
		dbname = instance.get('dbname', 'mysql')
	
		return host, port, user, password, dbname, mysql_sock, defaults_file, tags, options
	
	def _connect(self, host, port, mysql_sock, user, password, dbname, defaults_file):
		try:
			import MySQLdb
		except ImportError:
			raise Exception("Cannot import MySQLdb module. Check the instructions "
				"to install this module at https://app.datadoghq.com/account/settings#integrations/mysql")
	
		if defaults_file != '':
			db = MySQLdb.connect(read_default_file=defaults_file)
		elif  mysql_sock != '':
			db = MySQLdb.connect(unix_socket=mysql_sock,
									user=user,
									passwd=password,
									db = dbname)
		elif port:
			db = MySQLdb.connect(host=host,
									port=port,
									user=user,
									passwd=password,
									db = dbname)
		else:
			db = MySQLdb.connect(host=host,
									user=user,
									passwd=password,
									db = dbname)
		self.log.debug("Connected to MySQL")
	
		return db
	
	
	def _get_version(self, db, host):
		if host in self.mysql_version:
			return self.mysql_version[host]
	
		# Get MySQL version
		cursor = db.cursor()
		cursor.execute('SELECT VERSION()')
		result = cursor.fetchone()
		cursor.close()
		del cursor
		# Version might include a description e.g. 4.1.26-log.
		# See http://dev.mysql.com/doc/refman/4.1/en/information-functions.html#function_version
		version = result[0].split('-')
		version = version[0].split('.')
		self.mysql_version[host] = version
		return version
	def query(self, sql):
		"""Executes the given SQL statement and returns a sequence of rows."""
		assert self.cursor, "%s already closed?" % (self,)
		try:
			self.cursor.execute(sql)
		except MySQLdb.OperationalError, (errcode, msg):
			if errcode != 2006:  # "MySQL server has gone away"
				raise
			self._reconnect()
		return self.cursor.fetchall()
	def close(self):
		"""Closes the connection to this MySQL server."""
		if self.cursor:
			self.cursor.close()
			self.cursor = None
		if self.db:
			self.db.close()
			self.db = None
	
	def _reconnect(self):
		"""Reconnects to this MySQL server."""
		self.close()
		self.db = slef.check(self.configinstance)
		#self.cursor = self.db.cursor()
	
	def _collect_dict(self, metric_type, field_metric_map, query, db, tags):
		"""
		Query status and get a dictionary back.
		Extract each field out of the dictionary
		and stuff it in the corresponding metric.
	
		query: show status...
		field_metric_map: {"Seconds_behind_master": "mysqlSecondsBehindMaster"}
		"""
		try:
			cursor = db.cursor()
			cursor.execute(query)
			result = cursor.fetchone()
			"""if result is not None:
				for field in field_metric_map.keys():
					# Get the agent metric name from the column name
					metric = field_metric_map[field]
					# Find the column name in the cursor description to identify the column index
					# http://www.python.org/dev/peps/pep-0249/
					# cursor.description is a tuple of (column_name, ..., ...)
					try:
						col_idx = [d[0].lower() for d in cursor.description].index(field.lower())
						if metric_type == GAUGE:
							self.gauge(metric, float(result[col_idx]), tags=tags)
						elif metric_type == RATE:
							self.rate(metric, float(result[col_idx]), tags=tags)
						else:
							self.gauge(metric, float(result[col_idx]), tags=tags)
					except ValueError:
						self.log.exception("Cannot find %s in the columns %s" % (field, cursor.description))
			"""
			cursor.close()
			del cursor
		except Exception:
			#self.warning("Error while running %s\n%s" % (query, traceback.format_exc()))
			self.log.exception("Error while running %s" % query)
	
if __name__ == "__main__":
	cfg = MySqlConfig(dbname='smartstrader')
	print cfg.get("host", "")
	print cfg.get("hostx", "x")
	msql = MySql('daily')
	msql.check(cfg)
	print msql.query("""SELECT * 
FROM  `stock_symbols` 
LIMIT 0 , 30""")