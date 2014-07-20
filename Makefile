# Reference card for usual actions in development environment.
#
# For standard installation of cashmere, see INSTALL.
#
# For details about cashmere's development environment, see CONTRIBUTING.rst.
#
NPM = npm
NODE_BIN = node_modules/.bin
PIP = pip
BOWER = $(NODE_BIN)/bower
CIRCUS = circusd
GRUNT = $(NODE_BIN)/grunt


.PHONY: help develop bower watch public clean dist-clean maintainer-clean


#: help - Display available targets.
help:
	@echo "Reference card for usual actions in development environment."
	@echo "Here are available targets:"
	@egrep -o "^#: (.+)" [Mm]akefile  | sed 's/#: /* /'


#: develop - Develop the Python project
develop:
	$(PIP) install tox
	$(PIP) install -e ./
	$(NPM) install
	$(PIP) install circus


#: bower - Download libraries with bower.
bower:
	$(BOWER) install


#: watch - Watch in-development files and automatically build them on update.
watch:
	$(GRUNT) watch


#: public - Generate public/ folder contents.
public: bower
	$(GRUNT) copy less uglify


#: serve - Run all servers
serve:
	$(CIRCUS) circus.ini


#: serve-static - Run static files service.
serve-static:
	node_modules/.bin/ws -d public/ --port 8001


#: serve-ui - Run UI service.
serve-ui:
	cashmere runserver


#: clean - Basic cleanup, mostly temporary files.
clean:


#: distclean - Remove local builds
dist-clean: clean
	rm -rf public/
	rm -rf bower_components/


#: maintainer-clean - Remove almost everything that can be re-generated.
maintainer-clean: dist-clean
	rm -rf node_modules/
