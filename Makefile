.PHONY: lint test clean clean-dist bump release

VENV = .venv
VENV_ACTIVATE = . $(VENV)/bin/activate
BUMPTYPE = patch

PWD = $(shell pwd)

TOX = tox

$(VENV):
	virtualenv $(VENV)
	$(VENV_ACTIVATE); pip install tox bumpversion twine 'readme_renderer[md]'
	$(VENV_ACTIVATE); pip install -e .

lint: $(VENV)
	$(VENV_ACTIVATE); $(TOX) -e lint

test: $(VENV) lint
#	$(VENV_ACTIVATE); $(TOX)

dist: clean-dist
	python setup.py sdist bdist_wheel
	tar tzf dist/*.tar.gz
	ls -ls dist
	$(VENV_ACTIVATE); twine check dist/*

bump: $(VENV)
	$(VENV_ACTIVATE); bumpversion $(BUMPTYPE)
	git show -q
	@echo
	@echo "SUCCESS: Version was bumped and committed. Now push the commit."
	@echo
	@echo "    git push origin master && git push --tags"

test-release: clean test dist
	$(VENV_ACTIVATE); twine upload --repository-url https://test.pypi.org/legacy/ dist/*

release: test dist
	$(VENV_ACTIVATE); twine upload dist/*

clean-dist:
	rm -rf dist

clean: clean-dist
	rm -rf $(VENV)
	find tests -name .tox -type d -exec rm -r "{}" +
