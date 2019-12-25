clean-package:
	rm -rf dist

test:
	coverage run -m unittest discover -s tests/

package: clean-package package-dist package-upload

package-dist:
	python ./setup.py sdist

package-upload:
	twine upload dist/*
