from setuptools import setup

setup(
    name = "task",
    version = "1.0.0",
    description = "Task manager on your CLI",
    author = "darren",
    author_email="darren2what4u@gmail.com",
    py_modules=["main"],
    entry_points = {
        # (cli command i want to type) = (name of file):(function inside that file)
        "console_scripts": ["main=main:main"]
    }

)