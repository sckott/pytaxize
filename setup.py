from setuptools import setup

setup(name='pytaxize',
	version='0.4.900',
	description='Taxonomic toolbelt for Python',
  author='Scott Chamberlain',
  author_email='myrmecocystus@gmail.com',
  url='https://github.com/sckott/pytaxize',
  packages=['pytaxize'],
  install_requires=['requests>=2.7.0',
                    'pandas>0.15.0',
                    'lxml'],
  data_files=[('pytaxize/data', ['data/apg_orders.csv', 'data/apg_families.csv', 'data/plantGenusNames.csv', 'data/plantNames.csv', 'data/rank_ref.csv'] )],
)
