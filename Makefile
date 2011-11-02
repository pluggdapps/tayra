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
	cp CHANGELOG docs/CHANGELOG
	cp LICENSE docs/LICENSE
	cp README docs/README
	cp ROADMAP docs/ROADMAP
	python ./setup.py sdist

upload : 
	cp CHANGELOG docs/CHANGELOG
	cp LICENSE docs/LICENSE
	cp README docs/README
	cp ROADMAP docs/ROADMAP
	python ./setup.py bdist_egg register upload --show-response 
	
vimplugin :
	rm -rf ./vim-plugin/vim-tayra.tar.gz
	cd ./vim-plugin; tar cvfz ./vim-tayra.tar.gz *

cleanall : clean
	rm -rf tayra-env

clean :
	rm -rf build;
	rm -rf dist;
	rm -rf tayra.egg-info;
	rm -rf tayra.egg-info/;
	rm -rf `find ./ -name parsetyrtab.py`;
	rm -rf `find ./ -name "*.pyc"`;
	rm -rf `find ./ -name "yacctab.py"`;
	rm -rf `find ./ -name "lextab.py"`;
	rm -f tayra/test/stdttl/*.ttl.py;
	rm -f tayra/test/stdttl/*.html;
	rm -f tayra/test/bench/tayra/*.html;
	rm -f tayra/test/bench/tayra/*.ttl.py;
	rm -f tayra/test/tagsttl/*.html;
	rm -f tayra/test/tagsttl/*.ttl.py;
