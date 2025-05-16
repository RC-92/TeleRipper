from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="teleripper",
    version="0.1.0",
    author="RC-92",
    description="Download media files from Telegram channels",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RC-92/TeleRipper",
    packages=find_packages(),
    install_requires=[
        "telethon>=1.24.0",
        "configparser>=5.2.0",
    ],
    entry_points={
        'console_scripts': [
            'teleripper=teleripper.teleripper:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
