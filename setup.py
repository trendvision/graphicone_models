from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='graphicone_models',
    url='https://github.com/trendvision/graphicone_models',
    # author='John Ladan',
    # author_email='jladan@uwaterloo.ca',
    # Needed to actually package something
    packages=['models'],
    # Needed for dependencies
    install_requires=['sqlalchemy'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='TRV',
    description='all models',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)