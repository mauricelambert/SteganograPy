from setuptools import setup

setup(
    name="SteganograPy",
    version="0.0.1",

    py_modules=["SteganograPy"],
    install_requires=["pillow"],

    author="Maurice Lambert",
    author_email="mauricelambert434@gmail.com",
    maintainer="Maurice Lambert",
    maintainer_email="mauricelambert434@gmail.com",
 
    description="This package hide text or bytes in image.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
 
    include_package_data=True,

    url="https://github.com/mauricelambert/SteganograPy",
    project_urls={
        "Documentation": "https://mauricelambert.github.io/info/python/security/SteganograPy.html",
        "Executable": "https://mauricelambert.github.io/info/python/security/SteganograPy.pyz",
    },
    download_url="https://mauricelambert.github.io/info/python/security/SteganograPy.pyz",
 
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Topic :: Security",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
    ],

    keywords=["Package"],
    platforms=['Windows', 'Linux', "MacOS"],
    license="GPL-3.0 License",

    entry_points = {
        'console_scripts': [
            'Stegano = Stegano:main',
        ],
    },
 
    python_requires='>=3.6',
)