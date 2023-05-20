FROM node:18.16.0

WORKDIR /backend

COPY . .


#Copying the Bash Script for configuring the Postgres Image Application
COPY configure-postgres-password.sh /usr/src/app/docker-entrypoint-initdb.d/

# Set the script as executable
RUN chmod +x /docker-entrypoint-initdb.d/configure-postgres-password.sh


RUN npm install --production

#Build the application

EXPOSE 5000

#Start the application
CMD ["npm", "start"]