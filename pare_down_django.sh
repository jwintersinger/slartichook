#!/bin/bash
# Remove unnecessary Django files. Useful for reducing load time of
# zip-compressed Django when deployed on App Engine.
rm -rf conf/locale
rm -rf contrib/{admin,admindocs,auth,comments,databrowse,gis,localflavor}
rm -rf db/backends/{mysql,oracle,postgresql,postgresql_psycopg2,sqlite3}
