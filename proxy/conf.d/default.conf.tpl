
server {
    listen ${LISTEN_PORT};

    location /static {
        alias /app/vol/web;
    }

    location / {
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    ${CLIENT_MAX_BODY}M;
    }
}