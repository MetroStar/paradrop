FROM node:current-alpine

WORKDIR /app

COPY . .

RUN yarn install --frozen-lockfile

EXPOSE 3008

CMD ["yarn", "start"]