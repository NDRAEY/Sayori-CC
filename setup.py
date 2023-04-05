from setuptools import setup, find_packages

setup(
    name='sayori_cc',
    version='0.1.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points = {
        'console_scripts': [
            'sayori-cc = sayori_cc.main:premain',
        ]
    },
    package_data={'lucario_fs': ['utils/*']},
)
