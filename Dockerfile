FROM ubuntu:latest
LABEL authors="nowog"

ENTRYPOINT ["top", "-b"]