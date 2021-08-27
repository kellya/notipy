# Set output dir
BUILDDIR=dist
PROJECT_BASE=noti_py

#GH/github command used to initiate a release
GH=/usr/bin/gh

test:
	pytest -v

build: dir
	poetry build

dir: 
	[ -d $(BUILDDIR) ] || mkdir -p $(BUILDDIR)

clean:
	rm -rf $(BUILDDIR)
	find . -name __pycache__|xargs rm -rf

poetry-release: build
	poetry publish

coverage:
	coverage run -m pytest
	coverage report -m

pyflakes:
	pyflakes ${PROJECT_BASE}

pylint:
	pylint --load-plugins=pylint_django --django-settings-module=fam_mac.settings ${PROJECT_BASE}

gh-release: build
	#Figure out what the last/most recent build is
	$(eval LATEST = $(shell ls -t1 ${BUILDDIR}/*|head -n1))
	$(eval TAG = $(shell git describe --abbrev=0))
	@echo "Sending $(TAG) to github"
	${GH} release create $(TAG) $(LATEST)

release: poetry-release gh-release

.PHONY: dir clean release gh-release poetry-release coverage
