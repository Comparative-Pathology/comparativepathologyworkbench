**DOCUMENT 4**

**Administering the Comparative Pathology Workbench (CPW)**

This document describes how to administer the CPW software system with
new Image Sources and how to link CPW Users with WordPress Users.

Mike Wicks

29^th^ November 2023

**Workbench Configuration**

Configuration of the Comparative Pathology Workbench (CPW) is achieved
by using a superuser account.

**Configure the CPW Environment Record**

The CPW has an Environment record which may need configuring:

+-----------------------+----------------------------------------------+
| **Name**              | **CPW** (**MANDATORY!**)                     |
+=======================+==============================================+
| **Location**          | **DEVELOPMENT** or CZI or CANADA or COELIAC  |
+-----------------------+----------------------------------------------+
| **Protocol**          | http                                         |
+-----------------------+----------------------------------------------+
| **Web Root**          | workbench-czi-cpw.mvm.ed.ac.uk/protected     |
|                       |                                              |
|                       | (The URL of the Web Root for all documents   |
|                       | and images referenced by the CPW, typically  |
|                       | "localhost:8888/some_folder" )               |
+-----------------------+----------------------------------------------+
| **Document Root**     | /home/ehgcap/WWW/private_media               |
|                       |                                              |
|                       | (The complete Path of the Web Root Folder    |
|                       | used for all documents and images referenced |
|                       | by the CPW, typically                        |
|                       | "/Library/WebServer/Documents/some_folder/"  |
|                       | )                                            |
+-----------------------+----------------------------------------------+
| **NGINX Private       | "some_other_folder"                          |
| Location**            |                                              |
|                       | (Not relevant in a development setting)      |
+-----------------------+----------------------------------------------+
| **WordPress Web       | workbench-czi-cpw.mvm.ed.ac.uk/wordpress     |
| Root**                |                                              |
|                       | (The URL of the WordPress server used by the |
|                       | CPW -- typically in a development setting,   |
|                       | this will be "localhost/my-wordpress" or     |
|                       | similar)                                     |
+-----------------------+----------------------------------------------+
| **WordPress Active?** | True or False                                |
+-----------------------+----------------------------------------------+
| **From Email**        | The Comparative Pathology Workbench (CZI)    |
|                       | Team                                         |
|                       | \<edgutcellatlas-cpw@mlist.is.ed.ac.uk\>     |
|                       |                                              |
|                       | Not that relevant in a development setting   |
|                       | as all emails are written out to a file      |
|                       | instead.                                     |
+-----------------------+----------------------------------------------+
| **Date Format**       | %A, %B %e, %Y                                |
+-----------------------+----------------------------------------------+
| **Minimum Cell        | 75                                           |
| Height**              |                                              |
+-----------------------+----------------------------------------------+
| **Maximum Cell        | 450                                          |
| Height**              |                                              |
+-----------------------+----------------------------------------------+
| **Minimum Cell        | 75                                           |
| Width**               |                                              |
+-----------------------+----------------------------------------------+
| **Maximum Cell        | 450                                          |
| Width**               |                                              |
+-----------------------+----------------------------------------------+
| **Maximum Initial     | 10                                           |
| Columns**             |                                              |
+-----------------------+----------------------------------------------+
| **Minimum Initial     | 1                                            |
| Columns**             |                                              |
+-----------------------+----------------------------------------------+
| **Maximum Initial     | 10                                           |
| Rows**                |                                              |
|                       |                                              |
| **10**                |                                              |
+-----------------------+----------------------------------------------+
| **Minimum Initial     | 1                                            |
| Rows**                |                                              |
+-----------------------+----------------------------------------------+
| **Maximum REST        | 1000                                         |
| Columns**             |                                              |
+-----------------------+----------------------------------------------+
| **Minimum REST        | 3                                            |
| Columns**             |                                              |
+-----------------------+----------------------------------------------+
| **Maximum REST Rows** | 1000                                         |
+-----------------------+----------------------------------------------+
| **Minimum REST Rows** | 3                                            |
+-----------------------+----------------------------------------------+
| **Maximum Bench       | 10                                           |
| Count**               |                                              |
+-----------------------+----------------------------------------------+
| **Maximum Collection  | 10                                           |
| Count**               |                                              |
+-----------------------+----------------------------------------------+

**WordPress Server Functionality within the CPW**

The CPW creates, updates, and deletes Blog Posts on an associated
WordPress instance whenever new Benches are created and deleted, and
Cells are updated with Images.

For the system to converse with the associated WordPress instance, the
CPW needs updating with Credentials for each user.

***Adding WordPress Credentials***

For each User of the Workbench, there must be matching WordPress
credentials.

Add matching Credentials by going to "Authorisation", "Blog Credentials"
menu option.

From your WordPress instance, you will need to supply:

-   The "User Name",

-   The "WordPress ID"

-   The "Application. Password"

    -   (This password is generated by Editing the relevant user within
        WordPress).

**Adding Image Sources**

For the CPW to access an Image Source, it must be supplied with the
connection details of the image source.

New Image Sources are added on the Search Sources Page.

For each new Source of Images, you must supply:

-   A Name for the Server

-   A URL of the server

-   Some Credentials on the server

    -   (eg. User id and Password)

-   A Type

-   Specify whether the source is Accessible.

    -   (True means Credentials are required, False, they are not)
