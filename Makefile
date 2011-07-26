develop :
	rm -rf tayra-env
	virtualenv tayra-env --no-site-packages
	bash -c "source tayra-env/bin/activate ; python ./setup.py develop"

testall :
	echo "Pending ...."

bdist_egg :
	python ./setup.py bdist_egg

sdist :
	python ./setup.py sdist

upload : 
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
	rm -rf `find ./ -name "*.pyc"`;
	rm -rf `find ./ -name "yacctab.py"`;
	rm -rf `find ./ -name "lextab.py"`;
	rm tayra/ttl/test/stdttl/*.ttl.py;
	rm tayra/ttl/test/stdttl/*.html;
