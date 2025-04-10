FROM node:18-alpine AS build
WORKDIR /todo_frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY ./infra/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /todo_frontend/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
