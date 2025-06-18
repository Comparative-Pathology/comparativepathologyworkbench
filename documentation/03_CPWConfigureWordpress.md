# Setup a Wordpress Server for the Comparative Pathology Workbench (CPW) #

This document describes how to install and setup a Wordpress instance
running within Docker.

Mike Wicks

1<sup>st</sup> May 2024

## Prerequisites ##

However, there are a number of issues with running the CPW software.

1.  The Administrator is required to download, run and configure a
    WordPress "stack", within Docker.

2.  The Administrator is required to turn off any other web servers that
    might be running on your system (eg. Mac's have Apache running by
    default and listening on Port 80). Running a local Webserver
    listening on a Port other than Port 80 is OK.

## Install Required Software ##

Install Docker (Docker Desktop, preferably), from
https://www.docker.com/

## Setup WordPress ##

### Step 1 - Download the WordPress Software Stack ###

In a different folder, download the software from Github:

<https://github.com/Comparative-Pathology/docker-compose-wordpress>

This repository provides a full WordPress "Stack" (ie. MySQL, PHP, WordPress and Nginx), managed by Docker.

### Step 2 - Download the WordPress Software ###

Download WordPress from here:

<https://en-gb.wordpress.org/download/>

Copy the downloaded and expanded WordPress source code into the "**docker-compose-wordpress**" folder, "wordpress"

Delete the file "**wordpress/wp-config.php**"

Rename the file "**wordpress/wp-config_NEW.php**" to
"**wordpress/wp-config.php**"

### Step 3 - Build the WordPress Software Stack ### 

Run the command:

	docker-compose up -d --build

When this completes, point a Browser at **http://localhost/my-wordpress/**

You should see the WordPress Install screen.

### Step 4 -- Install WordPress ### 

Follow the instructions, making a note of account names and passwords.

Create a user of "admin" to manage the system.

### Step 5 - Configure WordPress ###

Login into the WordPress Instance, here:
**http://localhost/my-wordpress/wp-login.php**

Configure "**permalinks**" within the WordPress "**settings**", set to "**Numeric**"

Create a new Application Password for the "**admin**" account.

Write down this password (eg. "NRae TvA6 eq2Z 3Jpd B61K Ehm3") and the "user_id" number (eg. "1")

### Step 6 - Link the WordPress and the CPW ###

The WordPress "**admin**" Account must be linked to the CPW "**admin**" Account.

To do this, a new Credential row linking the CPW "**admin**" Account to WordPress "**admin**" Account must be created, using the previously generated WordPress Application Password.

Login into the CPW with "**admin**" account, and go to "Authorisation", "Blog Credentials".

The new Credential row specifies the CPW User Name, the WordPress "**user_id**" number and the Application Password.

The CPW User Name and the WordPress User Name MUST match!

Save the new Credential Row.

### Step 7 -- Stopping WordPress ###

To bring the system down, use the following command:

	docker-compose down
