FROM nginxinc/nginx-unprivileged:1-alpine

LABEL maintainer='safarnejad.ho@gmail.com'

COPY . /etc/nginx
COPY ./run.sh /run.sh

USER root

RUN mkdir -p /app/vol/web && \
    chmod -R 755 /app/vol/web && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh


# optional : useful when we want to deploy app on other service
VOLUME /app/vol/web


USER nginx

CMD ["/run.sh"]