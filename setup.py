from setuptools import setup, find_packages

long_description = """"""

install_requires = []
with open('requirements.txt') as fh:
    for l in fh:
        if len(l) > 0:
            install_requires.append(l)

setup(
   name='simple_taskfarm',
   version='1.0',
   description='',
   license="GPL3",
   long_description=long_description,
   author='William R Saunders, James Grant',
   author_email='W.R.Saunders@bath.ac.uk',
   url="https://github.com/wrs20/simple_taskfarm",
   packages=find_packages(),
   #install_requires=install_requires,
   scripts=['scripts/task-batch'],
   include_package_data=True
)
