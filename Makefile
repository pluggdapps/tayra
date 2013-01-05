develop :
	rm -rf tayra-env
	virtualenv tayra-env --no-site-packages
	bash -c "source tayra-env/bin/activate ; python ./setup.py develop"

testall :
	cd tayra/test/; python ./teststd.py

bench-setup :
	bash -c "source tayra-env/bin/activate ; easy_install mako"
	bash -c "source tayra-env/bin/activate ; easy_install cheetah"
	bash -c "source tayra-env/bin/activate ; easy_install django"
	bash -c "source tayra-env/bin/activate ; easy_install genshi"
	bash -c "source tayra-env/bin/activate ; easy_install kid"
	bash -c "source tayra-env/bin/activate ; easy_install myghty"

benchmark :
	cd tayra/test/bench/; bash -c "source tayra-env/bin/activate; ./basic.py"

bdist_egg :
	python ./setup.py bdist_egg

sdist :
	python ./setup.py sdist

sphinx-doc :
	cp README.rst sphinxdoc/source/
	cp CHANGELOG.rst sphinxdoc/source/
	cp docs/directives.rst sphinxdoc/source
	cp docs/extendingtayra.rst sphinxdoc/source
	cp docs/filter_blocks.rst sphinxdoc/source
	cp docs/functions.rst sphinxdoc/source
	cp docs/gettingstarted.rst sphinxdoc/source
	cp docs/glossary.rst sphinxdoc/source
	cp docs/template_layout.rst sphinxdoc/source
	cp docs/template_libraries.rst sphinxdoc/source
	cp docs/template_plugins.rst sphinxdoc/source
	cp docs/tutorial.rst sphinxdoc/source
	rm -rf sphinxdoc/build/html/
	make -C sphinxdoc html
	cd sphinxdoc/build/html; zip -r tayra.sphinxdoc.zip ./

upload :
	python ./setup.py sdist register -r http://www.python.org/pypi upload -r http://www.python.org/pypi --show-response 
	
pushcode: push-googlecode push-bitbucket push-github 

push-googlecode:
	hg push https://prataprc@code.google.com/p/tayra/

push-bitbucket:
	hg push https://prataprc@bitbucket.org/prataprc/tayra

push-github:
	hg bookmark -f -r default master
	hg push git+ssh://git@github.com:prataprc/tayra.git

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
