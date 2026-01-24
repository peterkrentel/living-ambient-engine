"""Setup script for Living Ambient Engine."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="living-ambient-engine",
    version="0.1.0",
    author="Peter Krentel",
    description="Automated hypnotic ambient video generation engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/peterkrentel/living-ambient-engine",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "Pillow>=10.0.0",
        "opencv-python>=4.8.0",
        "pyyaml>=6.0",
        "pydub>=0.25.1",
        "soundfile>=0.12.1",
        "click>=8.1.0",
        "python-dotenv>=1.0.0",
        "tqdm>=4.65.0",
        "colorama>=0.4.6",
        "ffmpeg-python>=0.2.0",
    ],
    entry_points={
        "console_scripts": [
            "ambient-engine=run_job:main",
        ],
    },
)

