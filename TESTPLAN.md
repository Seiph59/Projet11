# Pur-beurre Test Plan
Here is the test plan for the "pur-beurre" application you will find all the details about tests implemented for this project.

## Document Usage Guide

### Introduction
This test plan, will explain which tests and fonctionnalities are covered for this project, and where they are located.

### Roles
Im the only author for this Test Plan, if you encounter any problem, please feel free to contact me.

### Environmental needs
To execute these tests, you don't need to install anything more than what is in the "requirements.txt" file.
To test the application, you will need to install the application before, you will find all the installation details on the 'README' file.

### Item pass/fail criteria
* If all tests are Ok you can deploy the application
* If you encounter a warning you are going to have a quick check to be sure of your deployment
* If you encounter an error, make sure to  fix it before to deploy you application

### Approach
You can decide to launch your test with the basic command "python manage.py test"

If you prefer, you can test application one by one instead of all the project:
* python manage.py test food
* python manage.py test accounts
* python manage.py test welcome

Check this process to be sure the application works correctly
1. Create an user account
2. Login with your account
3. Make a search to be sure that your database is well populated
4. Try to save a product and check if it is displayed on your food page

### Features to be tested
__Welcome Application:__
* Views tests

__Accounts Application:__
* Integration tests -> Client test to create User or User already exists
* Urls tests
* Redirection tests

__Food Application:__
* Mock tests for populate_db part
* Unit test for products insertion
* Url resolve tests
* Models tests and to add favorite food into the favorite of the current user

### Features not be tested
* If OpenFoodFacts API is available

### Document Maintenance
Creation date: 05/07/2019
