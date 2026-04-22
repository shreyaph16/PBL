FROM node:20-slim as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
# For dev, we just use the dev server
# For production, we would build: RUN npm run build

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
