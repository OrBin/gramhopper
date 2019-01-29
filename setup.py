from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='gramhopper',
    version='1.0.4',

    description='A bot platform for automatic responses based on various triggers',
    long_description=long_description,
    long_description_content_type="text/markdown",

    url='https://github.com/OrBin/gramhopper',

    author='Or Bin, Meir Halachmi',
    author_email='orbin50@gmail.com, meir.halachmi@gmail.com',
    install_requires=[
        'python_telegram_bot==11.1.0',
        'boolean.py==3.6',
        'ruamel_yaml==0.15.46'
    ],

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Communications :: Chat',
    ],

    keywords='gramhopper telegram bot',

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'gramhopper=gramhopper.bot:main',
        ],
    },
)
