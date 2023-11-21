FROM node:18 as build
WORKDIR /src
COPY package.json ./
COPY package-lock.json ./
RUN npm install
COPY . ./
RUN npm run build
