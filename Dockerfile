FROM python:3

# Update OS
RUN apt-get update
RUN sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list
RUN apt-get -y upgrade

# Install dependencies
# I need LaTeX and pandoc to generate the CV:
RUN apt-get install make git tex-common texlive pandoc -y
RUN pip install pelican Markdown ghp-import ipython typogrify nbconvert
RUN pip install --upgrade pelican Markdown ghp-import beautifulsoup4


WORKDIR /site
# Generate the website when running the container:
CMD pelican content/ -o output/ -s publishconf.py

