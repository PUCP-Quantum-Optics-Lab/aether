from setuptools import setup, find_packages

requires = [
    "pyserial"
]

requires_dev = []

requires_test = []

setup(
    name="aether",
    version="1.0",
    description="Project for controlling components of a quantum optics experiment table.",
    author="Josue Villasante",
    author_email="josue.villasante@gmail.com",
    REQUIRES_PYTHON=">=3.9.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requires,
    extras_require={
        "dev": requires_dev,
        "test": requires_test,
    },
)
