FROM node:18-alpine AS build
WORKDIR /todo_frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
  # Удаляем дефолтный конфиг nginx, если нужно (необязательно)
  # RUN rm /etc/nginx/conf.d/default.conf
  # Копируем собранные файлы в веб-папку nginx
COPY ./infra/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /todo_frontend/dist /usr/share/nginx/html
  # Если требуется, можно скопировать свой конфиг nginx:
  # COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
