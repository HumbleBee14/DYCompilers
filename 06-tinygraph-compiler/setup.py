from setuptools import setup, find_packages

setup(
    name="tinygraph",
    version="0.0.1",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20",
    ],
    entry_points={
        "console_scripts": [
            "tinygraph-demo=tinygraph.cli:main",
        ]
    },
)


