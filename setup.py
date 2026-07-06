from setuptools import find_packages,setup
from typing import List

HYPHEN_DOT_E="-e ."
def get_packages(file_path)->List[str]:
    requirement=[]
    with open(file_path) as file_obj:
        requirement=file_obj.readlines()
        requirement=[req.replace("\n","") for req in requirement]
        if HYPHEN_DOT_E in requirement:
            requirement.remove(HYPHEN_DOT_E)
    return requirement

setup(
    name="llm project",
    version="0.0.1",
    author="Arjun Kumar",
    author_email="aarrjunkkumar619@gmail.com",
    packages=find_packages(),
    install_requires=get_packages("requirements.txt")
)