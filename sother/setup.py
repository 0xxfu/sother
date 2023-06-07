from setuptools import setup, find_packages

setup(
    name="sother",
    description="Slither -> sother",
    url="https://github.com/trailofbits/slither-plugins",
    author="xfu",
    version="0.1",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["slither-analyzer>=0.9.0"],
    entry_points={
        "console_scripts": ["sother=sother:main"],
    },
)
