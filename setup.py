import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="behave-performance",
    version="0.7.0",
    author="MPinardi",
    author_email="pinardi@gmail.com",
    description="A behave performance testing tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mpinardi/behave-performance",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Testing",
    ],
    packages=['behave_performance','behave_performance.helpers','behave_performance.salad','behave_performance.salad.stream',
            'behave_performance.salad.veggies','behave_performance.formatter','behave_performance.formatter.helpers',
            'behave_performance._behave','behave_performance.formatter.statistics'],
    package_dir = {'behave_performance':'src/behave_performance'},
    entry_points={
        'console_scripts': [
            'behave_performance=behave_performance.__main__:main',
        ]
    },
    package_data={'': ['salad/salad-languages.json']},
    include_package_data=True,
    python_requires='>=3.9',
    install_requires=['pyee','aiofiles','behave[toml] @ git+http://github.com/behave/behave.git@v1.2.7.dev5'],
    test_suite="test"
)