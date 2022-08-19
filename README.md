# URL Shortener
A small python based URL Shortener service using Flask and MYSQL Database that provides support for two primary operations :

1. Shorten URL - Given a long URL, generate a shorter unique url alias and return this short url called the short link.
2. On accessing the Short URL - Redirected to the original long URL link.

## Getting Started 

The **_URL Shortener_** service is a python based flask application which takes a long crude url link and transforms it into a unique, short and easy to copy-paste url link. On accessing these short links the users will be redirected to the original long url without having to deal with the long cumbersome links. 

This document provides information on 
- how to install this application
- how to start the service
- how to use the application through a simple GUI 

## Installation
To start using the service, first download the **_URL Shortener_** repository.

The downloaded repository contains 2 primary files :
- main.py
- index.html

The **_URL Shortener_** app requires 2 prerequisites that can be installed using the [pip](https://pip.pypa.io/en/stable/) package manager along with setting up MYSQL Database in your system.

1. Flask and
```bash
pip install flask
```

2. mysql-connector-python
```bash
pip install mysql-connector-python
```

or just use the requirements.txt for installations using 
```bash
pip install -r requirements.txt
```

3. For installing MYSQL database, download the installer for the Community Server Edition from the offical [MYSQL website](https://dev.mysql.com/downloads/mysql/) with official steps on [MYSQL documentation](https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/)

Just select the default settings and set an admin user-password,
which will be required in running the **_URL Shortener_** and connecting it to the MYSQL database.


**Note :** 
- The mysql-connector-python enables Python programs to access MySQL databases, using an API.
- To test the installation by running on terminal
```bash
mysql
```
- In case it is not recognized on MacOS, try running the following :
```bash
alias mysql=/usr/local/mysql/bin/mysql
```

## Usage


The **_URL Shortener_** application provides a basic html frontend UI that takes the long urls in a form and on pressing the submit button, returns the Short URL link unique to it. 

Next on accessing this short url link, the application redirects the user to the original long url.

To start using the service, follow the steps below :

1. Download the **_URL Shortener_** repository and switch to the 'src' folder as the working directory.

2. Update line **_12_** of 'main.py' with MYSQL user name and password.

3. Run the 'main.py' python file as follows:
```
python main.py
```
which starts the Flask app and the webserver can be accessed at :
- http://127.0.0.1:5000 or http://localhost:5000

4. Go to http://127.0.0.1:5000 and enter a long url in the form and press submit to get it's unique short url.

5. Click on the short url link to be redirected to the original long url.


## Functional Requirements :

1. Given a URL, our service should generate a shorter and unique alias of it. This is
called a short link. This link should be short enough to be easily copied and pasted
into applications.
2. When users access a short link, our service should redirect them to the original
link.
3. Python based application 

### Assumptions 

- Fixed length of short url's hash id is taken as 7, allowing for generation of a significantly large (64^7) hashes after which collision could take place.

- When the same long url is submitted through the app again, the application responds back with the existing short url link for that Long url instead of generating a new url.

## Future Work 

What additional features should we expect might be needed?

- The URL Shortener service can be equipped with various functional requirements like :
   * Generating a unique short url every time a same url is entered into the service.
   * Asking the users for custom url names to be to assigned to the 
   short url links.
   * Maintaining a time to live for each URL so as to avoid keeping stale urls forever.
   * User login based system for keeping track of individual user as well as analytics of individual short links including time of usage, frequency of usage, etc.


What do we expect the maintenance of this service to entail?

- In order to maintain the URL Shortener service, following issues can be expected :
   * To provide a better throughput, and for highly available and consistent service, the application needs to be scaled horizontally using Distributed systems.
   * Incorporate a 3rd Caching layer apart from current App and Database layer to handle majority of traffic.
   * Based on the Data storage requirements, the database and Cache would need to be horizontally scaled and techniques like Replication, Sharding , partitioning, will come into play.
   * Might have to implement load balancers for handling traffic spikes.
   * Might haave to meet certain Service Level Objectives for customers like availability >=99.9%
   * For generating analytics, performing aggrgations and redesigning the database schema to optimize performance.


## Testing

The **_URL Shortener_** application provides various test cases for testing some of the invocations possible with the service. 

There are 10 test cases including Tests to id for the Short link url from the long url link taken as input. The test generate the MD5 hash with base64 encoding for various long urls and compare them with their correct value. Also included are some mock patch tests for multiple functions with fixed return values.


### Running the Test Cases

The test cases for the **_URL Shortener_** service use "unittest", a built in python library which on execution, returns the results of all the tests with either a pass ('ok') or fail message along with individual test results. 

In order to execute the test, run the following command from the **src** folder of the repository on terminal :

```Python
python -m unittest -v test_url-shortener.py 
```

In the successful scenario all test cases pass as shown below :

```bash
$python -m unittest -v test_url-shortener.py 
test_01_hashing_function (test_url-shortener.UrlShortenerTestCase) ... ok
test_02_hashing_function (test_url-shortener.UrlShortenerTestCase) ... ok
test_03_hashing_function (test_url-shortener.UrlShortenerTestCase) ... ok
test_04_mock_exists_id (test_url-shortener.UrlShortenerTestCase) ... ok
test_05_mock_store_id_url (test_url-shortener.UrlShortenerTestCase) ... ok
test_06_mock_shorten_url (test_url-shortener.UrlShortenerTestCase) ... ok
test_07_mock_get_url (test_url-shortener.UrlShortenerTestCase) ... ok
test_08_hashing_function (test_url-shortener.UrlShortenerTestCase) ... ok
test_09_hashing_function (test_url-shortener.UrlShortenerTestCase) ... ok
test_10_hashing_function (test_url-shortener.UrlShortenerTestCase) ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.002s

OK
```

