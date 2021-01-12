from setuptools import setup, find_packages

setup(name='aljpy',
      version='0.7',
      description='Andy\'s common tools',
      author='Andy Jones',
      author_email='andyjones.ed@gmail.com',
      url='https://github.com/andyljones/aljpy',
      packages=find_packages(),
      package_data={'aljpy': ['*.txt']},
      install_requires=['tqdm>=4.42'])
