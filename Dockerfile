# vim:set ft=dockerfile
FROM python:2.7

USER root
RUN yum install -y \
    libffi-devel
    xmlsec1 \
    && yum clean
