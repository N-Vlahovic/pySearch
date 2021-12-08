import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pySearch",
    version="0.0.1",
    author="Nikolai Vlahovic",
    author_email="nikolai@nexup.com",
    description="A cli to search for Python packages.",
    install_requires=[
        "colorama",
        "lxml",
        "requests"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/n-vlahovic/pySearch",
    project_urls={
        "Bug Tracker": "https://github.com/n-vlahovic/pySearch/issues",
        "Contributing": "https://github.com/N-Vlahovic/pySearch/blob/master/contributing.md",
        "Documentation": "https://n-vlahovic.github.io/pySearch/"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        "console_scripts": ["py-search=pySearch.cli:main"],
    }
)
