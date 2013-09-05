from setuptools import setup, find_packages

setup(
    name='django-change-email',
    version=__import__('change_email').__version__,
    description='A Django application to enable users to change their e-mail address.',
    long_description="""django-change-email enables registered users to change
their e-mail address.""",
    author='Tarak Blah',
    author_email='halbkarat@gmail.com',
    url='https://github.com/tarak/django-change-email',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires=['django>=1.5,<=1.6',
                      'django-easysettings',
    ],
    test_suite='tests.main',
)
