from setuptools import setup, find_packages

setup(
    name='DirDive',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dir_dive=dir_dive.main:main',
        ],
    },
    author='zebang.eth',
    author_email='zebang_li@berkeley.edu',
    description='DirDive: Dive into your directory structure and file contents with ease.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/zebangeth/DirDive',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
