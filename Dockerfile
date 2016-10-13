FROM matthiaskoenig/linux-setup-combine:latest
MAINTAINER Matthias Koenig <konigmatt@googlemail.com>

WORKDIR $HOME
RUN pip install cobra --upgrade

# run the tests in docker container
RUN git clone https://github.com/sys-bio/tellurium
WORKDIR $HOME/tellurium

# testing mkoenig branch, but this should be done for master & develop also
RUN git checkout mkoenig
RUN nosetests

# test the installation
RUN python setup.py install

# RUN pip install codecov && codecov
# RUN bash <(curl -s https://codecov.io/bash)