# The Comparative Pathology Workbench Configuration #

This document describes how to set up and run the Software for the Comparative Pathology Workbench

## Workbench Configuration ##

Configuration of the workbench is achieved by using a superuser account, when the application is running.

Logging in as a Superuser provides 2 more main menu options on the main menu:

1.	Maintenance
2.	Authorisation

### Adding Wordpress Server Functionality ###

The Workbench creates, updates and deletes Blog Posts on an associated Wordpress instance.

In order to converse with a Wordpress instance, the Workbench needs configuring for:

1. Credentials on that instance
2. Commands that use the REST API of that instance.

#### Wordpress Credentials ####

Log in as a Superuser, and access the “Maintenance” main menu option.

For each User of the Workbench, there must be matching Wordpress credentials in order to ensure, Blog Commentary is possible for each Matrix and Cell. – if matching credentials are not found, no Blog Commentary is created.

Add matching credentials as a “New Blog Credential” – you will need to supply the “User Name”, “Wordpress ID”and “Application. Password”, obtained from your Wordpress instance.

(Your Wordpress Instance must have the “Application Password” Plugin installed and activated – each Wordpress user must have a consequent application password generated, and this must be stored in the Workbench)

#### Wordpress Commands ####

Log in as a Superuser, and access the “Maintenance” main menu option

Blog Posts are created, updated and deleted from an associated Wordpress instance that you have access to; the Workbench must be updated with the relevant REST API commands to enable this functionality to work. Add commands using the “Add New Blog Command” button.

There must be the entries added for ALL the following commands:

| **Name** | **Protocol** | **URL** | **Application** | **Preamble** | **Postamble** |
| --- | --- | --- | --- | --- | --- |
| **PostAPost** | http | &lt;URL of your Wordpress Instance&gt; | wp-json/wp/v2 | posts | &lt;None&gt; |
| **GetPostComments** | http | &lt;URL of your Wordpress Instance&gt; | wp-json/wp/v2 | comments?post= | &lt;None&gt; |
| **PostAComment** | http | &lt;URL of your Wordpress Instance&gt; | wp-json/wp/v2 | comments | &lt;None&gt; |
| **GetPost** | http | &lt;URL of your Wordpress Instance&gt; | wp-json/wp/v2 | posts | &lt;None&gt; |
| **LinkPost** | http | &lt;URL of your Wordpress Instance&gt; | archives | &lt;None&gt; | &lt;None&gt; |
| **DeletePost** | http | &lt;URL of your Wordpress Instance&gt; | wp-json/wp/v2 | posts | &lt;None&gt; |

### Adding Image Server Functionality ###

In order to converse with an Image Server instance, the Workbench needs configuring for:

1. Protocols to access Image Servers
2. Types of Image Server
3. Commands that use the REST API for a given Type of Image Server

#### Image Server Type ####

Log in as a Superuser, and access the “Maintenance” main menu option

Scroll down to “Server Types”, and press “Add New Type”

At present the Workbench can cater for 4 types of Image Server:

1. “OMERO_5.4.7”
2. “WORDPRESS”
3. “EBI_SCA”
4. “CPW”

Add these Image Servers here.

#### Image Server Protocol #### 

Log in as a Superuser, and access the “Maintenance” main menu option

Scroll down to “Protocols”, and press “Add New Protocol”

At present the Workbench can only cater for 2 types of Protocol:

1. “HTTP”
2. “HTTPS”

Add these types here.

#### Image Server (API) Commands ####

Log in as a Superuser, and access the “Maintenance” main menu option

Scroll down to “API Commands”, and press “Add New Command”

In order for the Workbench to successfully access OMERO 5.4.7 Image servers, the following commands need to be added, thus:

| **Name** | **Type** | **Protocol** | **Application** | **Preamble** | **Postamble** |
| --- | --- | --- | --- | --- | --- |
| **Images** | OMERO_5.4.7 | https | api/v0/m | images |     |
| **ImageDatasets** | OMERO_5.4.7 | https | api/v0/m | images | datasets |
| **Api** | OMERO_5.4.7 | https | api |     |     |
| **Token** | OMERO_5.4.7 | https | api/v0/token |     |     |
| **Login** | OMERO_5.4.7 | https | api/v0/login |     |     |
| **GroupDatasets** | OMERO_5.4.7 | https | api/v0/m | datasets/?group= | &childCount=true |
| **GroupImages** | OMERO_5.4.7 | https | api/v0/m | images/?group= | &childCount=true |
| **Projects** | OMERO_5.4.7 | https | api/v0/m | projects | &childCount=true |
| **GroupProjects** | OMERO_5.4.7 | https | api/v0/m | projects/?group= | &childCount=true |
| **Region** | OMERO_5.4.7 | https | webgateway | render_image_region | 0/0/?region= |
| **Thumbnail** | OMERO_5.4.7 | https | webgateway | render_thumbnail |     |
| **Viewer** | OMERO_5.4.7 | https | iviewer | ?images= |     |
| **BirdsEye** | OMERO_5.4.7 | https | webgateway | render_birds_eye_view | 175 |
| **Dataset** | OMERO_5.4.7 | https | api/v0/m | datasets | &childCount=true |
| **DatasetImages** | OMERO_5.4.7 | https | api/v0/m | datasets | images/?childCount=true |
| **DatasetProjects** | OMERO_5.4.7 | https | api/v0/m | datasets | projects |
| **ImageROIs** | OMERO_5.4.7 | https | api/v0/m | images | rois/?childCount=true |
| **ProjectDatasets** | OMERO_5.4.7 | https | api/v0/m | projects | datasets/?childCount=true |
| **PublicViewer** | OMERO_5.4.7 | https | webclient | img_detail |     |
| **WordpressImage** | WORDPRESS | https | wp-json/wp/v2 | media |     |
| **WordpressImages** | WORDPRESS | https | wp-json/wp/v2 | media?per_page=35&page= | &author= |

### Adding Image Servers ###

In order for the Workbench to access Image Servers, it must be supplied with the connection details of an image server.

Log in as an ordinary User, and access the “View Imaging Host List” main menu option.

Ordinary Users can add, update and delete their own Image Servers; Admin Users can administer ALL Image Servers.

Scroll down the list of Servers, and press “Add New Server”.

You must supply a Name for the Server, a URL of the server, and credentials on the server (User id (Uid) , and Password (Pwd)).

OMERO 5.4.7 servers can either be:

1.	Fully Public

	-	no credentials required, simply a URL without a Uid and Pwd.

2.	Private

	-	Specific Credentials are required with the URL to ALL data; Uid and Pwd mandatory

3.	Semi-Public

	-	credentials typically required for a “public user”, to access all data; Uid and Pwd mandatory

## Authorization ##

Log in as a Superuser, and access the “Authorisation” main menu option.

A Superuser can edit and delete Workbench users here.

Ordinary users can via the login drop-down menu, as well as reset and change their passwords here. This is achieved via email, using the email address supplied during Registration.

Mike Wicks

20<sup>th</sup> June 2025