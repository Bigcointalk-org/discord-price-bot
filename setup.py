import re
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

with open(here / "requirements.txt", "r") as f:
    dependencies = f.readlines()

with open('src/discord_price_bot/version.py') as f:
    version = re.search(r'VERSION\s*=\s*\"((\w+\.?)+)', f.read(), re.MULTILINE).group(1)

setup(
    # TODO: Adjust your project information here
    name='discord_price_bot',
    version=version,
    description='A cryptocurrency price bot for Discord.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Bigcointalk-org/discord-price-bot',
    author='veriz0wn',
    author_email='hello@bigcointalk.org',
    project_urls={
        'Bug Reports': 'https://github.com/Bigcointalk-org/discord-price-bot/issues',
        'Source': 'https://github.com/Bigcointalk-org/discord-price-bot',
    },
    keywords='discord-price-bot',
    python_requires='>=3.8, <4',
    install_requires=dependencies,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Other Audience',
        'Topic :: Communications :: Chat',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Typing :: Typed',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    entry_points={
        'console_scripts': [
            'discord-bot=discord_price_bot:main',
        ],
    },
)
