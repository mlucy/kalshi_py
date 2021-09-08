from setuptools import setup

setup(name='kalshi',
      version='0.1.1',
      description='Library for accessing Kalshi API',
      url='https://github.com/mlucy/kalshi_py',
      author='Michael Lucy',
      author_email='michaelglucy@gmail.com',
      license='MIT',
      packages=['kalshi'],
      zip_safe=True,

      install_requires=['requests'],
      python_requires='>=3',
)
