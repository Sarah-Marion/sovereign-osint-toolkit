from setuptools import setup, find_packages

setup(
    name="sovereign-osint-toolkit",
    version="1.0.0",
    author="Sarah Marion",
    author_email="dev@sarahmarion.com",
    description="Advanced Kenyan-Focused OSINT Toolkit by Sarah Marion",
    long_description=open("README.md").read(),
    url="https://github.com/Sarah-Marion/sovereign-osint-toolkit",
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