#!/bin/sh
PATH=/home/ehgcap/miniconda3/condabin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/ehgcap/.local/bin:/home/ehgcap/bin:/home/ehgcap/miniconda3/envs/cpw_env_python38_django4/bin
conda run -n cpw_env_python38_django4 python /home/ehgcap/Django/comparativepathologyworkbench/app/manage.py mailer --a /home/ehgcap/Django/comparativepathologyworkbench/app/reports/checkblogposts.txt -s 'checkblogposts Report' -m 'This is the checkblogposts Report from the Server' -r edgutcellatlas-cpw@mlist.is.ed.ac.uk
