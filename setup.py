from setuptools import setup, find_packages

setup(
    name="django-thumborize",
    version="0.0.1",
    description="",
    packages=find_packages(),
    author="Thiago Pisani",
    author_email="pisani.thiago@gmail.com",
    url="https://github.com/tpisani/django-thumborize",
    license="BSD",
    install_requires=["Django", "libthumbor"],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
    ],
)
