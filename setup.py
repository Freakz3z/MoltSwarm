"""Setup script for MoltSwarm."""

from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="moltswarm",
    version="0.1.0",
    description="The AI Hive - Decentralized AI collaboration on Moltbook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MoltSwarm Team",
    url="https://github.com/yourname/MoltSwarm",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "isort>=5.12.0",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
