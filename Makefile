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
	@bash -c "source pa-env/bin/activate ; easy_install-3.2 sphinx"

# Test tayra package with standard test cases.
testall :
	tayra -t ok

# Install other template packages for benchmark.
bench-setup :
	bash -c "source tayra-env/bin/activate ; easy_install mako"
	bash -c "source tayra-env/bin/activate ; easy_install cheetah"
	bash -c "source tayra-env/bin/activate ; easy_install django"
	bash -c "source tayra-env/bin/activate ; easy_install genshi"
	bash -c "source tayra-env/bin/activate ; easy_install kid"
	bash -c "source tayra-env/bin/activate ; easy_install myghty"

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
	cp README.rst sphinxdoc/source/
	cp CHANGELOG.rst sphinxdoc/source/
	cp docs/commandline.rst sphinxdoc/source
	cp docs/develop.rst sphinxdoc/source
	cp docs/directives.rst sphinxdoc/source
	cp docs/filter_blocks.rst sphinxdoc/source
	cp docs/functions.rst sphinxdoc/source
	cp docs/gettingstarted.rst sphinxdoc/source
	cp docs/glossary.rst sphinxdoc/source
	cp docs/template_layout.rst sphinxdoc/source
	cp docs/template_libraries.rst sphinxdoc/source
	cp docs/template_plugins.rst sphinxdoc/source
	rm -rf sphinxdoc/build/html/
	make -C sphinxdoc html

# Generate sphinx documentation and zip the same for package upload.
sphinx : sphinx-compile
	cd sphinxdoc/build/html; zip -r tayra.sphinxdoc.zip ./

# Upload package to python cheese shop (pypi).
upload :
	python ./setup.py sdist register -r http://www.python.org/pypi upload -r http://www.python.org/pypi
	
# Push code to repositories.
pushcode: push-googlecode push-bitbucket push-github 

push-googlecode:
	hg push https://prataprc@code.google.com/p/tayra/

push-bitbucket:
	hg push https://prataprc@bitbucket.org/prataprc/tayra

push-github:
	hg bookmark -f -r default master
	hg push git+ssh://git@github.com:prataprc/tayra.git

# Package vim plugin.
vimplugin :
	rm -rf ./vim-plugin/vim-tayra.tar.gz
	cd ./vim-plugin; tar cvfz ./vim-tayra.tar.gz *

cleanall : clean
	rm -rf tayra-env

clean :
	rm -rf build;
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
