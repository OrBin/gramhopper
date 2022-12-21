from pathlib import Path
from setuptools import setup, find_namespace_packages


LONG_DESCRIPTION = Path("README.md").read_text(encoding='utf-8')


setup(
    name='gramhopper',
    version='3.0.1',

    description='A bot platform for automatic responses based on various triggers',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",

    url='https://github.com/OrBin/gramhopper',

    author='Or Bin, Meir Halachmi',
    author_email='orbin50@gmail.com, meir.halachmi@gmail.com',
    install_requires=[
        'python_telegram_bot==13.15',
        'boolean.py==3.6',
        'ruamel_yaml~=0.17'
    ],

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Topic :: Communications :: Chat',
    ],

    keywords='gramhopper telegram bot',

    packages=find_namespace_packages(include=['gramhopper', 'gramhopper.*']),

    entry_points={
        'console_scripts': [
            'gramhopper=gramhopper.bot:start_bot',
        ],
    },
)
