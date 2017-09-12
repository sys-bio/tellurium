##############################################################################
# Dockerfile
##############################################################################
# Dockerfile for running the webapp in a container.
# The container can be build and run via:
#
#       docker build -t sys-bio/tellurium . && docker run -it sys-bio/tellurium
#
##############################################################################
FROM python:3.5
MAINTAINER Matthias Koenig <konigmatt@googlemail.com>

WORKDIR /tellurium
# requirements first for caching
ADD ./requirements.txt .
RUN pip install -r requirements.txt

# copy everything and build
COPY . .
RUN pip install -e .

# RUN nosetests
CMD ["nosetests"]
