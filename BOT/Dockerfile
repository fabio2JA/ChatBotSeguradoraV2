FROM node:latest

WORKDIR /app

COPY package*.json ./
RUN apt-get update && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]