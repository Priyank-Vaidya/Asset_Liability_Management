#!/bin/bash
#Version 1.0.0
#--------------------------------------------
#Name: Priyank Vaidya
#Project: Asset-Liability Management
#--------------------------------------------

#This is the script to configure the postgres password and database while running the container
#Please ensure that the Password is stored as an environment variable by using
# ENV POSTGRES_PASSWORD=<password> in the VM Instance running

#{ VM Instance > Run the gcloud sql engine > Run the Application Container } -----> Containerized Application

echo "Configuring the Clous SQL Engine"
export GOOGLE_CLOUD_PROJECT=
export GOOGLE_CLOUD_SQL_USERNAME=
export GOOGLE_CLOUD_SQL_PASSWORD=
export GOOGLE_CLOUD_SQL_DATABASE='stock_pred'
export GOOGLE_CLOUD_SQL_HOST=
export GOOGLE_CLOUD_SQL_PORT=3000
 
#Starting the gcloud instance for cloud SQL Engine
gcloud beta emulators sql start --project <project-id> --region <region>

# Run the Flask application.
python app.py