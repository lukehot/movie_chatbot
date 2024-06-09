
from setuptools import setup, find_packages

setup(
    name="movie_chatbot",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "neo4j",
        "pytest",
        "python-dotenv"
    ],
)