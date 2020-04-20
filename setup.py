from setuptools import setup

setup(name='aljpy',
      version='0.5',
      description='Andy\'s common tools',
      author='Andy Jones',
      author_email='andyjones.ed@gmail.com',
      url='https://github.com/andyljones/aljpy',
      packages=['aljpy'],
      package_data={'aljpy': ['*.txt']},
      include_package_data=True,
      install_requires=['tqdm>=4.42'])
