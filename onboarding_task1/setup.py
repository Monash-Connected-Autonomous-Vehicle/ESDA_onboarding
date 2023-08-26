from setuptools import find_packages, setup

package_name = 'onboarding_task1'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yentung-yen',
    maintainer_email='ychi0036@student.monash.edu',
    description='TODO: Package description',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'control_publisher = onboarding_task1.control:main',
            'laserscan = onboarding_task1.sense:main',
            'trial = onboarding_task1.trial:main'
        ],
    },
)
