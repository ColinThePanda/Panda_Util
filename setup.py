from setuptools import setup, find_packages

setup(
    name='panda_util',
    version='0.1',
    package_dir={"": "src"},  # Tell setuptools packages are under src
    packages=find_packages(where="src"),  # Find packages in src directory
    install_requires=[
        'rich',
        'keyboard',
    ],
    include_package_data=True,
)