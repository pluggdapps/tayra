# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 SKR Farms (P) LTD.

import re
from   setuptools import setup, find_packages
from   os.path    import abspath, dirname, join

here = abspath( dirname(__file__) )
README = open(join(here, 'README.rst')).read()

v = open(join(dirname(__file__), 'tayra', '__init__.py'))
version = re.compile(r".*__version__[ ]*=[ ]*'(.*?)'", re.S).match(v.read()).group(1)
v.close()

description='An integrated web templating environment'

classifiers = [
'Development Status :: 4 - Development',
'Environment :: Web Environment',
'Intended Audience :: Developers',
'Programming Language :: Python :: 2.6',
'Programming Language :: Python :: 2.7',
'Programming Language :: JavaScript',
'Programming Language :: CSS',
'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
]

setup(
    name='tayra',
    version=version,
    py_modules=[],
    package_dir={},
    packages=find_packages(),
    ext_modules=[],
    scripts=[],
    data_files=[],
    package_data={},                        # setuptools / distutils
    include_package_data=True,              # setuptools
    exclude_package_data={},                # setuptools
    zip_safe=False,                         # setuptools
    entry_points={                          # setuptools
        'console_scripts' : [
           'tayra = tayra.tyr:main',
        ],
        'tayra.plugins' : [
            'ITTLPlugin = tayra.plugins:TestPlugins',
        ],
    },
    install_requires=[                      # setuptools
        'ply>=3.4',
        'zope.component',
        'zope.interface',
        'MarkupSafe>=0.9.2',
    ],
    extras_require={},                      # setuptools
    setup_requires={},                      # setuptools
    dependency_links=[],                    # setuptools
    namespace_packages=[],                  # setuptools
    test_suite='tayra.test',             # setuptools

    provides=[ 'tayra', ],
    requires='',
    obsoletes='',

    author='Pratap R Chakravarthy',
    author_email='prataprc@gmail.com',
    maintainer='Pratap R Chakravarthy',
    maintainer_email='prataprc@gmail.com',
    url='http://tayra.pluggdapps.com',
    download_url='',
    license='Simplified BSD license',
    description=description,
    long_description=README,
    platforms='',
    classifiers=classifiers,
    keywords=[ 'template, web, html, css' ],
)
