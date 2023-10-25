import setuptools
import shutil

shutil.make_archive('./dist','zip')

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="behave-performance",
    version="0.5.0",
    author="MPinardi",
    author_email="pinardi@gmail.com",
    description="A behave performance testing tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=['behave_performance','behave_performance.helpers','behave_performance.salad','behave_performance.salad.stream','behave_performance.salad.veggies','behave_performance.formatter','behave_performance.formatter.helpers','behave_performance.formatter.statistics'],
    package_dir = {'behave_performance':'src/behave_performance'},
    entry_points={
        'console_scripts': [
            'behave_performance=behave_performance.__main__:main',
        ]
    },
    python_requires='>=3.9',
    install_requires=['pyee','aiofiles','behave @ git+https://github.com/behave/behave@13893e30eeb8fd5fc4ebeef5763dfe781b6f12a1#egg=behave'],
    test_suite="test"
)