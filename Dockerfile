# vim:set ft=dockerfile
FROM python:2.7

RUN yum install -y \
    libffi-devel
    xmlsec1 \
    && yum clean
