#.PHONY: build-docs
#build-docs:
#	docker build -t pytenable-docs -f Dockerfile-docs .
##		--build-arg uid=$(shell id -u) \
##		--build-arg gid=$(shell id -g) .
#
#.PHONY: docs
#docs: build-docs
#	docker run --rm -t \
#	-v "`pwd`":/src pytenable-docs \
#	sphinx-build docs docs/_build

# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = pyTenable
SOURCEDIR     = docs
BUILDDIR      = docs/_build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)