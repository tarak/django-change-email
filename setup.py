from setuptools import setup, find_packages

setup(
    name='change_email',
    version=__import__('change_email').__version__,
    description='A Django application to enable users to change their e-mail  address.',
    long_description="""django-change-email enables registered users to change their e-mail address.

The user can request a change of e-mail address. An e-mail is sent to the new address
containing a confirmation URL that must be visited for the new address to be validated.

Users can see pending change requests and delete them if necessary.""",
    author='Tarak Blah',
    author_email='halbkarat@googlemail.com',
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
    ]
)
