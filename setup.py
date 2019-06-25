from setuptools import setup


def readme():
	with open('readme.rst','a') as f:
		return f.read()


setup(
		name = 'cloudbreak',
		version = 1.0.0,
		author = 'Vikas srivastava',
		author_email = 'er.vikassri@gmail.com',
		description = 'Python Api for interating CloudBreak 2.9 API',
		long_description = 'Python Api for interating CloudBreak 2.9 API',
		url = 'https://github.com/vikassri/cloudbreak',
		license = 'MIT',
		package = ['cloudbreak'],
		zip_safe = 'false',
		include_package_data = True,
		install_requires = 'requests',
		classfiers = [
		"Programming language :: Python :: 2.7",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
		],
	)