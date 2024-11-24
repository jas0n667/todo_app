# Используем официальный Node.js образ
FROM node:16

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
# COPY ./project_todo/package.json ./project_todo/package-lock.json ./

# Копируем файлы проекта в контейнер
COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json

# Устанавливаем зависимости
RUN npm install

# Копируем все остальные файлы
COPY ./ /app/ 

# Собираем проект
RUN npm run build

# Открываем порт для сервера Vue.js
EXPOSE 8080

# Запускаем Vue.js приложение
CMD ["npm", "run", "serve"]
