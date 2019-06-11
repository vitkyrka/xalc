from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='xalc',
    description='Hexadecimal calculator',
    long_description=readme(),
    license='MIT',
    url='https://github.com/rabinv/xalc',
    author='Vincent Whitchurch',
    author_email='vincent@whitchurch.se',
    version='0.6.0',
    install_requires=[
        'ipython>=5.0.0',
        'bitstring>=3.1.4',
        'blessed>=1.14.1',
    ],
    tests_require=['nose'],
    test_suite='nose.collector',
    entry_points={
        'console_scripts': 'xalc = xalc.xalc:main'
    },
    packages=['xalc'],
    classifiers=[
        'Environment :: Console',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
)
