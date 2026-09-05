FROM node:20-bookworm-slim AS builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build
FROM node:20-bookworm-slim
WORKDIR /app
RUN npm install -g http-server
COPY --from=builder /app/dist ./dist
EXPOSE 5172
CMD ["http-server", "dist", "-p", "5172", "--host", "0.0.0.0"]
