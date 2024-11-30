from setuptools import setup, find_packages

setup(
    name="advent_of_code_cli",       # The package name, should be unique
    version="0.1",
    packages=find_packages(),
    py_modules=["cli"],             # The Python file (cli.py) containing your CLI code
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "advent=cli:cli",       # Command name = module:function
        ],
    },
    author="BennoCrafter",
    description="A CLI for Advent of Code utilities",  # Short description
    long_description=open("README.md").read(),  # Use README.md as a long description
    long_description_content_type="text/markdown",  # Markdown content type
    python_requires=">=3.10",        # Minimum Python version required
)
