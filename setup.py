from setuptools import setup,find_packages

setup(
   name='deltaNiner',
   version='1.01',
   description='This thing that I made',
   author='Christopher Gallo',
   author_email='cgallo@us.ibm.com',
   packages=['deltaNiner'],  #same as name
   include_package_data=True,
   install_requires=[
        'flask',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
 #external packages as dependencies
)