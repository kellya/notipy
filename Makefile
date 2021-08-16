# Set output dir
BUILDDIR=dist

#GH/github command used to initiate a release
GH=/usr/bin/gh

build: dir
	poetry build

dir: 
	[ -d $(BUILDDIR) ] || mkdir -p $(BUILDDIR)


clean:
	rm -rf $(BUILDDIR)

poetry-release: build
	poetry publish

gh-release: build
	#Figure out what the last/most recent build is
	$(eval LATEST = $(shell ls -t1 ${BUILDDIR}/*|head -n1))
	$(eval TAG = $(shell git describe --abbrev=0))
	@echo "Sending $(TAG) to github"
	${GH} release create $(TAG) $(LATEST)

release: poetry-release gh-release

.PHONY: dir clean release gh-release poetry-release
