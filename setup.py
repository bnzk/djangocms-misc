from setuptools import setup, find_packages
import os


# not so bad: http://joebergantine.com/blog/2015/jul/17/releasing-package-pypi/
version = __import__('djangocms_misc').__version__


def read(fname):
    # read the contents of a text file
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="djangocms-misc",
    version=version,
    url='https://github.com/bnzk/djangocms-misc',
    license='MIT Licence',
    platforms=['OS Independent'],
    description="djangocms misc",
    long_description=read('PYPI.md'),
    long_description_content_type="text/markdown",
    author=u'Ben Stähli',
    author_email='bnzk@bnzk.ch',
    packages=find_packages(),
    install_requires=(
        # 'Django>=1.3,<1.5',  # no need to limit while in development
        'django>=1.8',
        'django-appconf>=1.0'
    ),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
