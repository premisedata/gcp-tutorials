FROM node:14-buster-slim

WORKDIR /app

COPY . .

RUN npm install --production

CMD [ "node", "index.js" ]