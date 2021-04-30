# ESP-assessment - E-Commerce Django Application

This is a django e-commerce application that's built to sell clothing items to people on the internet. The data used in this application was gotten from Kaggle. It is a csv sheet of various clothing items and other details relating to each item. Further details on the data can be found on the kaggle website [here](https://www.kaggle.com/PromptCloudHQ/flipkart-products)

In this application, a customer can place order for various items, check the items in the cart, checkout and make payment. 
An admin can do all that a customer can do in adition to being able to add new products, edit products, delete products and 
check the dashboard for useful information relating to number of products in stock and the customer orders.

## Getting Started 

This document outlines how to set up a local copy of this project. This project consists of a web application developed with Django to inform policymakers on the impact of climate change on crop yield production. 

### Prerequisites 

 Among other requirements set the out in the ‘Requirements.txt’ file, some of the key ones are as follows: 

- Python 3.x 

- Django 3.1.7  

### Installation 

Install the latest Python 3.x. from https://www.python.org/downloads/  

 

Clone this repository into your environment using the following command: 

```
git clone https://github.com/McKeagney/turbo-bassoon.git 
```

In your working folder root, aka /turbo-bassoon, activate the virtual environment with the following command (use set for Windows): 

```
source .venv/bin/activate  
```

After activating the virtual environment, install all the requirements with the following command:

```
pip install -r requirements.txt  
```

Time to execute the program with the following command: 

```
python manage.py runserver 
``` 

Open a browser tab and write `localhost:8000` to enter to the web application. Enjoy! 

## Testing 

This application uses both TDD (unit tests) and BDD (behave tests)
To run the unit tests that have been developed here, run the following command in your terminal: 
```
./manage.py test   
```
To run behave tests, run the following command:
```
behave   
```

 ## Deployment

This application was deployed to Heroku using Gunicorn as it's HTTP server. Click the link below to check out the deployed website
https://powerful-wildwood-78943.herokuapp.com/
## Roadmap 

This application is still in an early stage of development and can be enhanced further by implementing several features. These include, but are not limited to: 


- A feature to allow the user remove items from cart

- A feature to allow usrr increase or reduce quantity of items from the cart page


Contributing these if you are able is more than welcome. Fork the project, create a feature branch and commit-push your changes as you see fit.  



## License 

Distributed under the Unlicensed license terms of agreement. See LICENSE for more information 
 
