test:
	python -m unittest discover -s tests/

package: package-dist package-upload

package-dist:
	python ./setup.py sdist

package-upload:
	twine upload dist/*
