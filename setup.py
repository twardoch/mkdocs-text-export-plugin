from setuptools import setup, find_packages


setup(
    name='mkdocs-text-export-plugin',
    version='1.0.0',
    description='An MkDocs plugin to export content pages as plain-text or Markdown files',
    long_description='The text-export plugin will export all Markdown pages in your MkDocs repository as plain-text or Markdown files',
    keywords='mkdocs txt plaintext markdown export',
    url='https://github.com/twardoch/mkdocs-text-export-plugin',
    author='Adam Twardoch',
    author_email='adam+github@twardoch.com',
    license='MIT',
    python_requires='>=3.10',
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
            'text-export = mkdocs_text_export_plugin.plugin:MdTxtExportPlugin'
        ]
    }
)
