import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='aiothingy',
    version='0.0.2',
    author='davy wybiral',
    author_email="davy.wybiral@gmail.com",
    description='Asynchronous Python library for interacting with the Nordic Thingy52 over Bluetooth',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wybiral/aiothingy",
    packages=['aiothingy'],
    install_requires=['bleak'],
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
