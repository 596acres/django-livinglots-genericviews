from setuptools import setup, find_packages
import os

import livinglots_genericviews


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
]

setup(
    author='Eric Brelsford',
    author_email='eric@596acres.org',
    name='django-livinglots-genericviews',
    version=livinglots_genericviews.__version__,
    description=("A set of helpers views for projects that use 596 Acres' "
                 "Living Lots."),
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='https://github.com/596acres/django-livinglots-genericviews/',
    license='GNU Affero General Public License v3 or later (AGPLv3+)',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'Django>=1.7',
    ],
    packages=find_packages(),
    include_package_data=True,
)
