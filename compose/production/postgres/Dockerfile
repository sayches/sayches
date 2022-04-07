FROM postgres:11.3

COPY ./compose/production/postgres/maintenance /usr/production/bin/maintenance
RUN chmod +x /usr/production/bin/maintenance/*
RUN mv /usr/production/bin/maintenance/* /usr/production/bin \
    && rmdir /usr/production/bin/maintenance
