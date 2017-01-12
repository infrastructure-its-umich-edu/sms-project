# vim:set ft=dockerfile
FROM python:2.7

RUN yum install -y xmlsec1 \
    && yum clean
