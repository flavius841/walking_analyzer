from setuptools import setup, find_packages

setup(
    name="walking_analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "colorama",
        "prompt_toolkit",
        "pandas",
        "numpy",
        "scipy",
    ],
    entry_points={
        "console_scripts": [
            "analyzer=analyzer.cli:main",
            "walking_analyzer=analyzer.main:main",
        ],
    },
)
