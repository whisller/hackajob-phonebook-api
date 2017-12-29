from setuptools import setup, find_packages
import os
import pip

install_reqs = pip.req.parse_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'),
                                          session=pip.download.PipSession())
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='hackajob-phonebook-api',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'api=hackajob_phone_book_api.api:main'
        ]
    },
    install_requires=reqs,
    python_requires='>=3.6'
)
