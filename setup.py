from setuptools import find_packages, setup
from codecs import open
from typing import List
import os
import re

curfile = os.path.abspath(os.path.dirname(__file__))  

PNAME, PTITLE = "src", "test_deploy_azure"

def get_requirements(path: str, version: bool = False) -> List[str]:
    with open(path) as req:
        requirements = []
        for line in req:
            line = re.sub(r"ÿþ|\x00", "", line).replace("\n", "")
            line = os.path.expandvars(line)
            requirements.append(line)
    if version:
        requirements = {
            info.split(" = ")[0]: info.split(" = ")[1].replace('"', '')
            for info in requirements
        }
    return list(filter(len, requirements))

if __name__ == "__main__":
    setup(
        name="lib",
        description="scheduler",
        version="0.0.1",
        author="P4I",
        long_description_content_type="text/markdown",
        author_email="tobia.tommasini@p4i.it",
        classifiers=[
            "Development Status :: 2 - Pre-Alpha",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python 3.11"
        ],
        packages=[PNAME] + [f"{PNAME}.{p}" for p in find_packages(PNAME)],
        package_dir={PTITLE: PNAME},
        py_modules=["settings"],
        include_package_data=True,
        package_data={},
        install_requires=get_requirements("requirements.txt"),
        python_requires=">=3"
    )