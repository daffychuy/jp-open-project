FROM node:14

RUN apt-get update
RUN apt-get install -y python3

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .
EXPOSE 7771
CMD [ "npm", "run", "dev" ]
