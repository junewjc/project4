[![Build Status](https://travis-ci.com/junewjc/project4.svg?branch=master)](https://travis-ci.com/junewjc/project4)

# [PHONENATICS](https://finalproject-django.herokuapp.com/)</p>

## Introduction

Phonenatics is an online store that sells phone accessories. 


The website allows users to buy products from the online store. It uses a relational database ([PostgreSQL](https://www.postgresql.org/)). Python and Django is used to retrieve the list of products, search and filter products based on various criteria. 


## Demo

The deployed version of the website can be found at https://finalproject-django.herokuapp.com/. 



| Contents                          |
|-----------------------------------|
|[UX](#UX)                          |
|[Features](#Features)              |
|[Technologies Used](#Technologies-Used)|
|[Testing](#Testing)                |
|[Deployment](#Deployment)          |
|[Credits](#Credits)                |



## UX


### Strategy

The website was designed to be minimalistic and user friendly. 
White and different shades of blue were chosen as the theme colour as it gives a professional feel to the website.



Users are able to
 * Sign up and log in to an account
 * View the list of products available for purchase
 * Search and filter products by categories
 * Add products to shopping cart
 * Update and delete the number of products in the shopping cart
 * Checkout and make payment using Stripe 


Superuser is able to 
 * Perform CRUD operations for the products and users


#### User Stories

As a user, I want to be able to 

*  View and navigate the website easily on my computer and mobile devices
*  Have quick access to all the products available on the website
*  Search and filter the products easily
*  Sign up and log in to my account
*  Add products to shopping cart and make changes to the products in the shopping cart
*  Checkout and make payment for the products



As a superuser, I want to be able to 

*  View all the user profiles and products in the online store
*  Perform CRUD for the products
*  Upload images for the products


## Features


### Existing Features

* Navigation Bar/ Dropdown Menu
  * The navigation bar was created using Bootstrap. The navigation bar is mobile responsive as it toggles a dropdown menu when the website is in mobile view. Users do not have to use back-button or scroll up to the top to use the navigation bar.


* Homepage
  * Users are able to view all the products that are available for purchase in the online store.

* Search and Filter
  *  Users are able to search and filter the products by categories

* Product Details
  *  Users are able to view the product descriptions by clicking on the individual products

* User Authentication
  *  Users are able to Sign Up, Log In and Log Out of their accounts

* Shopping Cart
  *  Users are able to add items to a shopping cart and edit the number of items in the shopping cart

* Checkout and Payment
  * Users are able to checkout and make payment for the items in the shopping cart


### Features Left to Implement

* Reviews feature
  * A reviews feature to allow users to review the products they have purchased

* User Dashboard
  * A dashboard that displays details on the purchase history and order status



## Technologies Used

HTML

CSS

Javascript

jQuery

Python

[Bootstrap](https://getbootstrap.com/)

[Django](https://www.djangoproject.com/)

[Django-allauth](https://django-allauth.readthedocs.io/en/latest/installation.html)

[Django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/install.html)

[Django-countries](https://pypi.org/project/django-countries/)

[Heroku](https://heroku.com/)

[Heroku Postgres](https://www.heroku.com/postgres)

[Stripe](https://stripe.com/en-sg)

[AWS S3](https://aws.amazon.com/s3/)


## Testing

Testing was done manually for all CRUD operations, user authentication and also for all buttons and forms. Chrome developer tools was used for all testing to make sure that the website is mobile responsive.


## Deployment

The project was written on AWS Cloud9 and was saved and tested locally. The website was hosted through Heroku and is deployed from the master branch so that it can be updated through new commits to the master branch. Regular commits were performed and pushed to Heroku which allows ease of tracking for any changes to the codes.


## Credits

#### Extra Sources

This project was done based on the youtube tutorials by [JustDjango](https://www.youtube.com/channel/UCRM1gWNTDx0SHIqUJygD-kQ/videos)


The Bootstrap template was obtained from [MDBootstrap](https://mdbootstrap.com/freebies/)

#### Content

All images and product descriptions were sourced from [Pexels](https://www.pexels.com/) and [Shopee](https://shopee.sg/remaxandwkofficialstore)



**This site has been created for educational purposes only**
