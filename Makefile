.PHONY: develop testall bench-setup benchmark bdist_egg sdist \
		sphinx-compile sphinx upload pushcode push-googlecode \
		push-bitbucket push-github vimplugin cleanall clean

# Setup virtual environment under tayra-env/ directory. And installs sphinx
# generator package.
develop :
	@rm -rf tayra-env
	@echo "Setting up virtual environment for python 3.x ..."
	@virtualenv --python=python3.2 tayra-env 
	@bash -c "source tayra-env/bin/activate ; python ./setup.py develop"
	@bash -c "source pa-env/bin/activate ; pip install sphinx"

# Test tayra package with standard test cases.
testall :
	tayra -t ok

# Install other template packages for benchmark.
bench-setup :
	bash -c "source tayra-env/bin/activate ; pip install mako"
	bash -c "source tayra-env/bin/activate ; pip install cheetah"
	bash -c "source tayra-env/bin/activate ; pip install django"
	bash -c "source tayra-env/bin/activate ; pip install genshi"
	bash -c "source tayra-env/bin/activate ; pip install kid"
	bash -c "source tayra-env/bin/activate ; pip install myghty"

# Execute the bench-mark suite. This is work in progress, you can help me to
# setup this benchmark.
benchmark :
	cd tayra/test/bench/; bash -c "source tayra-env/bin/activate; ./basic.py"

# Generate binary egg distribution.
bdist_egg :
	python ./setup.py bdist_egg

# Generate source distribution. This is the command used to generate the
# public distribution package.
sdist :
	python ./setup.py sdist

# Generate sphinx documentation.
sphinx-compile :
	pa -w confdoc -p tayra -o docs/configuration.rst
	cp README.rst docs/index.rst
	cp CHANGELOG.rst docs/
	cp TODO.rst docs/
	cat docs/index.rst.inc >> docs/index.rst
	rm -rf docs/_build/html/
	make -C docs html

# Generate sphinx documentation and zip the same for package upload.
sphinx : sphinx-compile
	cd docs/_build/html; zip -r tayra.sphinxdoc.zip ./

# Upload package to python cheese shop (pypi).
upload :
	python ./setup.py sdist register -r http://www.python.org/pypi upload -r http://www.python.org/pypi
	
# Push code to repositories.
pushcode: push-googlecode push-github push-bitbucket 

push-googlecode:
	hg push https://prataprc@code.google.com/p/tayra/

push-bitbucket:
	hg push https://prataprc@bitbucket.org/prataprc/tayra

push-github:
	hg bookmark -f -r default master
	hg push git+ssh://git@github.com:prataprc/tayra.git

# Package vim plugin.
vimplugin :
	rm -f tayra/ext/vim/vim-tayra.tar.gz
	cd tayra/ext/vim/; tar cvfz ./vim-tayra.tar.gz *

cleanall : clean cleandoc
	rm -rf tayra-env

cleandoc :
	rm -rf docs/_build/*

clean :
	rm -rf docs/_build;
	rm -rf dist;
	rm -rf tayra.egg-info/;
	rm -rf `find ./ -name parsetyrtab.py`;
	rm -rf `find ./ -name lextyrtab.py`;
	rm -rf `find ./ -name "*.pyc"`;
	rm -rf `find ./ -name "yacctab.py"`;
	rm -rf `find ./ -name "lextab.py"`;
	rm -f tayra/test/stdttl/*.ttl.py;
	rm -f tayra/test/stdttl/*.html;
	rm -f tayra/test/tagsttl/*.ttl.py;
	rm -f tayra/test/tagsttl/*.html;
	rm -f tayra/test/bench/tayra/*.html;
	rm -f tayra/test/bench/tayra/*.ttl.py;
	rm -f tayra/ext/vim/vim-tayra.tar.gz
