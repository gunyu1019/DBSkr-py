from setuptools import setup

setup(
    name='DBSKR',
    version='v1.0',
    packages=['DBSkr'],
    url='https://github.com/gunyu1019/DBSkr-py',
    license='MIT',
    author='gunyu1019',
    author_email='gunyu1019@gmail.com',
    description='Koreanbots와 top.gg를 위한 비공식 파이썬 API 레퍼입니다.',
    python_requires='>=3.6',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=open('requirements.txt').read(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
