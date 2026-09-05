FROM node:20-bookworm-slim
WORKDIR /app/backend
COPY backend/package*.json ./
RUN npm install
COPY backend/ ./
ENV NODE_ENV=production
EXPOSE 8001
CMD ["npm", "start"]
