# Pur-beurre Test Plan
Here is the test plan for the "pur-beurre" application you will find all the details about tests implemented for this project.

## Document Usage Guide

### Introduction
This test plan, will explain which tests and fonctionnalities are covered for this project, and where they are located.

### Roles
Im the only author for this Test Plan, if you encounter any problem, please feel free to contact me.

### Environmental needs
To execute these tests, you don't need to install anything more than what is in the "requirements.txt" file.

### Testing Tasks
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

### Features to be tested
__Welcome Application:__
* test_root_url_resolves_to_home_page_view
* test_welcome_get

__Accounts Application:__
*test_accounts.py*
* test_no_account_db
* test_new_user_account_created
* test_account_created_by_client

*test_forms.py*
* test_valid_form_true
* test_valid_form_false
* test_error_user_already_exists

*test_urls.py*
* test_register_url_resolves_to_register_view
* test_myaccount_url_resolves_to_my_account_view

*test_views.py*
* test_redirect_if__try_access_myaccount_without_login
* test_redirect_when_account_created_to_homepage
* test_redirect_when_login_to_homepage

__Food Application:__
*test_api_off.py*
* test_get_product_name
* test_populate_db_foods_added
* test_populate_db_categories_added

*test_models.py*
* test_saving_and_retrieving_food
* test_link_favorite_food_to_user

*tests_urls.py*
* test_url_resolve_to_result_page_view
* test_url_resolve_to_food_page_view

*tests_views.py*
* test_food_page_template

### Features not be tested
* If OpenFoodFacts API is available

### Document Maintenance
Creation date: 05/07/2019

# Testing
If you want to be sure than your app is working let's try this process
1. Create an user account
2. Login with your account
3. Make a search to be sure that your database is well populated
4. Try to save a product and check if it is displayed on your food page

