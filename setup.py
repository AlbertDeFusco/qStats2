from setuptools import setup

setup( name='qStats',
        version='0.1',
        description='Moab queue stat report generator',
        author='Albert DeFusco',
        license='MIT',
        packages=['qstats'],

        package_data= {
            'qstats.tests' : ['data/*']
            },

        entry_points = {
            'scripts':'qstats = qstats.__main__:main'
            }

        )

