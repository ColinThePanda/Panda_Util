from setuptools import setup, find_packages

setup(
    name='panda_util',  # Name of the package
    version='0.1',
    packages=find_packages(),  # Automatically discover all packages in the project
    install_requires=[  # Any dependencies you need
        'rich',     # Rich module for styled text and pretty formatting
        'keyboard', # Keyboard module for keyboard event handling
    ],
    include_package_data=True,  # Ensure non-Python files are included (if any)
)
