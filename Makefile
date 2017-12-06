
MDFILES=$(shell find ./docs -type f -name '*.md')
TOC=markdown-toc -i

prepare:
	@$(foreach mdfile, $(MDFILES), echo $(TOC) $(mdfile); ($(TOC) $(mdfile)) || exit;)
	pandoc --from=markdown \
               --to=rst \
               --output=README.rst README.md

release: prepare
	python setup.py sdist upload -r pypi


