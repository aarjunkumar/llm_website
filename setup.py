from setuptools import find_packages,setup
from typing import List

HYPHEN_DOT_E="-e ."
def get_packages(file_path):
    requirements=[]
    with open(file_path, "r", encoding="utf-8") as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.strip() for req in requirements]
    if "-e ." in requirements:
        requirements.remove("-e .")
    return requirements
    

setup(
    name="llm project",
    version="0.0.1",
    author="Arjun Kumar",
    author_email="aarrjunkkumar619@gmail.com",
    packages=find_packages(),
    install_requires=get_packages("requirements.txt")
)