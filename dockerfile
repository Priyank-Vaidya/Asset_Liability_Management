# Priyank Vaidya
# Version 1.0
# 
# Containerisation of backend application


FROM node:18.16.0

# Running firstly the backend Application
WORKDIR /backend

COPY . .

# Requirement for configuring the Postgres Password in the VM
# ----------------------------------------------------------------------------------------
#Copying the Bash Script for configuring the Postgres Image Application
COPY configure-postgres-password.sh /usr/src/app/docker-entrypoint-initdb.d/

# Set the script as executable
RUN chmod +x /docker-entrypoint-initdb.d/configure-postgres-password.sh
# ----------------------------------------------------------------------------------------

RUN npm install --production

#Build the application

EXPOSE 5000

#Start the application
CMD ["npm", "start"]

WORKDIR /backend

COPY ./ml_model /backend/ml_model

RUN python3 install --upgrade pip \
    && pip install -r requirements.txt 

CMD ["python3", "main.py"]