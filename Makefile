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


