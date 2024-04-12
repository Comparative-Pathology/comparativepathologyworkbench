#	Current Production/CZI CPW Configuration	#

## 1. Server ##

The system runs using a non-root user, without superuser privileges:

***"ehgcap"*** on the Server **workbench-czi-cpw.mvm.ed.ac.uk**


### Folder Aliases ###

There are a number of foder aliases required by the system:

1. **/opt/cpw** points to **/home/ehgcap/Django/comparativepathologyworkbench/app**

2. **/opt/cpw-about** points to **/home/ehgcap/WWW/html/about-cpw**

3. **/opt/private_media** points to **/home/ehgcap/WWW/private_media**


### Static Web Pages ###

This system has a set of Static pages which live here:

- **/home/ehgcap/WWW/html/about-cpw**

## 2. Webserver (NGINX) ##

The NGINX Configuration File lives here: **/etc/nginx/conf.d/czi-ws.conf**

The configuration file contains the following Endpoints:

- **/media** points to **/opt/cpw/media**

- **/static** points to **/opt/cpw/static**

- **/private_media** points to **/opt/private_media** (internal)

- **/about** points to **/opt/cpw-about**

- **/** points to **/opt/cpw/uwsgi_params**, uwsgi_pass Django

### CPW Application Home Directories ###

The CPW is a Django Application and has the following folders

- **/home/ehgcap/Django/comparativepathologyworkbench/app**
	- **/home/ehgcap/Django/comparativepathologyworkbench/app/config**
	- **/home/ehgcap/Django/comparativepathologyworkbench/app/matrices**
	- **/home/ehgcap/Django/comparativepathologyworkbench/app/reports**
	- **/home/ehgcap/Django/comparativepathologyworkbench/app/scripts**
	- **/home/ehgcap/Django/comparativepathologyworkbench/app/static**
	- **/home/ehgcap/Django/comparativepathologyworkbench/app/staticfiles**

Note the following Softlink:

**/home/ehgcap/Django/comparativepathologyworkbench/app/media** points to **/home/ehgcap/WWW/media**

## 3. Database Connection ##

This can be achieved Directly within an Environment File, or via a Connection Service File with a Password File

### A. Environment Variables ###

The Environment file lives here:

- **/home/ehgcap/Django/comparativepathologyworkbench/app/config/.env**

This contains the following example Environment Variables:

	DB_ENGINE=django.db.backends.postgresql
	DB_ATOMIC_REQUESTS=True
	DB_NAME=database
	DB_USER=database_user
	DB_PASSWORD=password
	DB_HOST=localhost
	DB_PORT=5432

These variables are picked up in the python file, **settings.py**, thus:

	DATABASES = {
		'default': {
			'ENGINE': config('DB_ENGINE'),
			'ATOMIC_REQUESTS': config('DB_ATOMIC_REQUESTS'),
			'NAME': config('DB_NAME'),
			'USER': config('DB_USER'),
			'PASSWORD': config('DB_PASSWORD'),
			'HOST': config('DB_HOST'),
			'PORT': config('DB_PORT'),
		}
	}


### B. Connection Service File ###

Alternatively, a Connection Service File with a Password File, can be used (it could be argued that this is a more secure solution).

The password file is called **.cpw_password**, and is stored in **/home/ehgcap/Django/comparativepathologyworkbench/app**.

An example **.cpw_password** file:

	localhost:5432:workbench_canada:workbench_canada_user:password

The connection service file is called **.pg_service.conf**, and is stored in **/home/ehgcap**.

An example **.pg_service.conf** file:

	[cpw_service]
	host=localhost
	port=5432
	dbname=database
	user=database_user

These files are picked up in the python file, **settings.py**, thus:

	DATABASES = {
		'default': {
			'ENGINE': config('DB_ENGINE'),
			'ATOMIC_REQUESTS': config('DB_ATOMIC_REQUESTS'),
			"OPTIONS": {
				"service": "cpw_service",
				"passfile": ".cpw_pgpass"
			}
		}
	}


## 4. The CPW Application ##

### CPW Environment Record ###

The CPW Environment Record contains many Global variables used by the system.  The following variables must set up correctly to ensure the correct running of the system

- **Web Root** set to **workbench-czi-cpw.mvm.ed.ac.uk/protected**

Requests to **/protected** are forwarded by the program **nginx_accel.py**, to **/private_media** via the Path, in **urls.py**:

	path(protected /\<str:image_id\>/\', matrices_views.nginx_accel, name=\'nginx_accel\')"

- **Document Root** set to **/home/ehgcap/WWW/private_media**

- **NGINX Private Location** set to **private_media**
