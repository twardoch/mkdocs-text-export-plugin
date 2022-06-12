from setuptools import setup, find_packages


setup(
    name='mkdocs-plugin-toplaintext',
    version='0.0.1',
    description='An MkDocs plugin to export content pages as plain-text files',
    long_description='The toplaintext plugin will export all markdown pages in your MkDocs repository as plain-text files',
    keywords='mkdocs txt plaintext export',
    url='https://github.com/twardoch/mkdocs-plugin-toplaintext',
    author='Adam Twardoch',
    author_email='adam+github@twardoch.com',
    license='MIT',
    python_requires='>=3.10',
    install_requires=[
        'mkdocs>=0.17',
        'beautifulsoup4>=4.6.3'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10',
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'toplaintext = mkdocs_plugin_toplaintext.plugin:TxtExportPlugin'
        ]
    }
)
