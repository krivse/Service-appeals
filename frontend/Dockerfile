#FROM debian
FROM nginx:1.19.3
#RUN apt update
#RUN apt install nginx -y

COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
#COPY /frontend/templates/*.html /usr/share/nginx/html/
COPY ./static/ /usr/share/nginx/html/
#COPY ./static/img/*.ico /usr/share/nginx/html/
#COPY ./static/js/*.js /usr/share/nginx/html/static/js/

#CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
