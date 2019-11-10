from setuptools import setup, find_packages
setup(
  name='scte',
  packages=find_packages(),
  version='1.1.1',
  license='apache-2.0',
  description='Tools for working with SCTE standards.',
  author='James Fining',
  author_email='james.fining@nbcuni.com',
  url='https://github.com/jamesfining/scte',
  download_url='https://github.com/jamesfining/scte/archive/v1.1.1.tar.gz',
  keywords=['scte', 'scte35', 'transport', 'stream', 'broadcast'],
  install_requires=[
          'bitstring'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Multimedia',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3'
  ],
)
