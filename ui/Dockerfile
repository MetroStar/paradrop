FROM patrikjuvonen/docker-nginx-http3:latest

ARG URL

COPY localhost.key /etc/ssl/private/
COPY localhost.pem /etc/ssl/
COPY nginx.conf /etc/nginx/
COPY h3.nginx.conf /etc/nginx/conf.d/
RUN rm -rf /usr/share/nginx/html/*
COPY ./ /usr/share/nginx/html/
RUN sed -i "s/http:\/\/127.0.0.1:5000/$URL/g" /usr/share/nginx/html/static/js_min/*
RUN rm -f /usr/share/nginx/html/localhost.pem /usr/share/nginx/html/localhost.key /usr/share/nginx/html/*.conf
EXPOSE 8443
