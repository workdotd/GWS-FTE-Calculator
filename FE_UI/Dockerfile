# Stage 1: Build the React application
FROM node:18-alpine AS build

#ENV JFROG_USERNAME=us_svc_edp_ansible@cbre.com
#ENV JFROG_REPO=https://us-east-1.aws.us.artifactory.gcso.cbre.com/artifactory/api/npm/devx-npm-nonprod-virtual/
#ARG JFROG_PASS

#RUN echo "//${JFROG_REPO}:_authToken=${JFROG_USERNAME}:${JFROG_PASS}" > ~/.npmrc 
#RUN echo "registry=https://${JFROG_REPO}" >> ~/.npmrc

WORKDIR /app

ARG ENV_NAME
ENV NODE_ENV=${ENV_NAME}
COPY .npmrc ./
COPY package*.json ./
RUN npm install

COPY . ./
RUN rm -rf .env*
COPY .env.${NODE_ENV} .env
RUN npm run build

# Stage 2: Serve the built app with Nginx
FROM nginx:1.25-alpine

COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

RUN  touch /var/run/nginx.pid && \
     chown -R nginx:nginx /var/cache/nginx /var/run/nginx.pid

RUN chown -R nginx:nginx /usr/share/nginx/html
RUN chown -R nginx:nginx /etc/nginx/conf.d/default.conf
RUN chown -R nginx:nginx /var/cache/nginx

USER nginx

EXPOSE 8501

CMD ["nginx", "-g", "daemon off;"]