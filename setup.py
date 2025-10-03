from setuptools import setup, find_packages

setup(
    name="sovereign-osint-toolkit-by-sarah-marion",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.28.0",
        "redis>=4.5.0", 
        "python-dotenv>=0.19.0",
        "click>=8.0.0",
    ],
    python_requires=">=3.8",
)