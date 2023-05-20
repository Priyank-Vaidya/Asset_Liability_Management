FROM node:18.16.0

WORKDIR /backend

COPY . .

RUN npm install --production

#Build the application

EXPOSE 5000

#Start the application
CMD ["npm", "start"]