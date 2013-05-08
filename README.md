dbproj
======

Required packages to run web server:
	Flask (web framework)
	Psycopg (postgresql driver)

=========================================
JSON API
=========================================
'/get_salt':
  expects: {'studentno': value}
  returns: {'studentno': value, 'salt': salt_value, 'temp_salt': temp_salt_value}

'/login':
  expects: {'studentno': value, 'hash': hashed_string}
  returns: {'status': boolean} <- lowercase 'true' or 'false'

=========================================

Checking in

Checking in - Pierre :p
