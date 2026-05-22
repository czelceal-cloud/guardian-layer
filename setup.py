from setuptools import setup, find_packages
setup(
    name="tical-code-guardian",
    version="0.1.0",
    description="Guardian Layer — AI safety runtime for tical-code. Protects human focus and AI execution depth.",
    author="tical-code",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[],
    extras_require={
        "yaml": ["pyyaml"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
