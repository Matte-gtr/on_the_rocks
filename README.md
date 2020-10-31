# On the Rocks

The "On the Rocks" website is designed for the purpose of letting users browse through the products on the site, adding items into their cart along the way.
Users do not have to be registered to make a purchase, although certain features are not accessible to non-registered users, such as viewing their profile and 
previous orders. Staff assigned users have access to add and edit products and cocktail recipes, however they aren't able to delete them. Superuser assigned users
have access to add, edit and delete any product or cocktail recipe. Each of the cocktails contains a link to a product within the store, which is required for
any new cocktails that are added.

## UX

This website features a collapsable navbar that is permanently fixed to the top of the screen and on collapsing, the links from the desktop view are stored under
a burger-button dropdown list. Users can search for products as well as filtering on categories, with pagination implemented on products at 36 per page, and 10 cocktails 
per page. The profile and site management links (staff & superusers only) contain javascript based cookies to remember the last open state of the accordian for 
user convenience, as well as a scroll to top button on all pages which appears once the user starts scrolling up below a certain height on the page.

The layout of the website was designed with a mobile first approach and adjusts according to the screen it is being viewed on, no functionality is lost when viewing 
the site on smaller devices. Messages in the form of toasts are provided where possible to provide users with clear feedback on successful and unsuccessful operations so users don't have to figure out
why an operation has failed.

A deployed version of the site is deployed at https://msnell89-on-the-rocks.herokuapp.com/

#### User story:
I want to be able to view products and if one catches my eye, I would like to be able to find out more about it.

#### User story:
I would like the option of buying in bulk and getting a discount.

#### User story:
I want to be able to make a purchase and receive a confirmation email after purchasing an item(s).

#### User story:
I would like the option of leaving a review on a product that I liked or didn't like.

#### User story:
I want to be able to view my previous orders on my account.

#### User story:
I want to be able to save my billing/delivery details to speed up future purchases.

The wireframes/initial mockups for the "On the Rocks" website can be found at https://github.com/Matte-gtr/on_the_rocks/blob/master/README.md

## Features

* **Landing Page** - This is the first page a user will see when visiting the site, the page is designed to be visually appealing with little other 
functionality.

* **About Us Page** - This is the page the user will be redirected to after entering the site, the page displays some basic information about the site and it's services,
as well as a carousel of some of the most commonly purchased items on the site.

* **Products Page(s)** - This page can be accessed from the navbar links or redirected here after searching for a product. The products on the page are paginated
and can be filtered on their categories from the nav link dropdown menu. Clicking on one of the product cards will take the user to a page where they can see details
about the product and will be able to add the products to their cart.

* **Products Reviews** - Product reviews can be posted by all authenticated users but will not display automatically. Once a review is submitted, staff or superusers will 
see a notification on the site management tab to either approve or delete the review. If a review is approved, it will display on the product detail page, as well as updating 
the overall rating of the product.

* **Create-a-crate Page** - This page can be accessed from the navbar links. The user will select a category from the list, then all the products in that category will 
be loaded below. Once an item from a selected category is in the users crate, they will not be able to change the category until the crate is either emptied, or added
to the cart when full (6 items). The user will receive a 20% discount on all items in the crate for this purchase.

* **Cocktails Page** - This page can be accessed from the navbar links. This page lists a selection of whiskey based cocktail recipe cards which when clicked, take the user
to the recipe display page to view the entire recipe. This page contains a link to the store related product in the form of a bootstrap modal, so the user can add the product to
their cart while remaining on the recipe page.

* **User authentication and registration** - This is implemented through the use of allauth. There are links to log in, sign up and log out on the navigation bar (depending on current authentication)
and these provide further links for a user to reset their password. Email authentication is used to site registration.

* **User Profile** - This page can be accessed from the account button on the navbar (authenticated users only). This page displays a form for a user to update their billing and delivery
information and a list of previous orders by the user. These are both contained within a bootstrap accordian which remembers it's previous state on page refresh for better UX.

* **Checkout/Payment functionality** - This is implemented using Stripe. Webhooks are in use to catch any missed orders. A user can only access the checkout page if items are in their
cart.

* **Site management**  - This page can be accessed from the account button on the navbar (staff and superusers only). This page is laid out in much the same way as the user profile page, 
however it contains the functionality to add products and cocktails, as well as containing notifications of any reviews awaiting approval. 

## Features left to implement:

* **Filter/Sort functionality on Products and Cocktails** - This is to be implemented at a future date due to time constraints.

* **Review approval notifications** - Users will receive a notification of any reviews they have posted that have since been approved.

## Technologies Used

HTML5

CSS3

JavaScript

Python3

Bootstrap
https://getbootstrap.com/docs/4.4/getting-started/introduction/
Bootstrap was used to speed up the development time and make use of their grid system, accordian and carousel.

Google fonts
https://fonts.google.com/
Google fonts was used to provide the fonts for the site.

JQuery
https://jquery.com/
The project uses JQuery to simplify DOM manipulation.

FontAwesome
https://fontawesome.com/icons?d=gallery

Django
https://www.djangoproject.com/

Postgres
https://www.postgresql.org/

aws s3
https://aws.amazon.com/
for media and static file hosting

gunicorn
https://gunicorn.org/

Pillow
https://pillow.readthedocs.io/en/stable/

## Automated testing

Each app within the project contains a test folder, which contain all the test files for the app. These can be found below: 

https://github.com/Matte-gtr/on_the_rocks/tree/master/cart/tests .
https://github.com/Matte-gtr/on_the_rocks/tree/master/checkout/tests .
https://github.com/Matte-gtr/on_the_rocks/tree/master/cocktails/tests .
https://github.com/Matte-gtr/on_the_rocks/tree/master/crate/tests .
https://github.com/Matte-gtr/on_the_rocks/tree/master/home/tests .
https://github.com/Matte-gtr/on_the_rocks/tree/master/products/tests .
https://github.com/Matte-gtr/on_the_rocks/tree/master/site_management .

For a number of the URLs, test scripts have been written to check that the URLs are pointing at the correct templates, as well as
pointing to the correct views.

A number of the views have automated tests to check that they are receiving the correct response of 200 or 302 for redirects, as well
as checking that the views are also returning the correct templates.

Forms have been tested where possible to check that forms are valid or invalid based on the test form data they receive, as well as
testing for any other attributes that have been included in the form init methods, such as checking for placeholders, checking fields do
not have labels and checking they have been assigned their correct class.

Models have also been tested where ever possible, in particular, the functions that are attached to the model class have been tested.

No automated test scripts have been written for views relying on session data as these have been manually tested extensively.

The tests did return some minor issues which have since been corrected. An issue was caught on the about us page/view which was not flagged 
by the debugger, as well as a warning for using pagination with an unordered query set.

To run these tests, open the project in development and run the following transaction in the CLI:

`python3 manage.py test` 

followed by the name of the app (e.g "products"). This will run all the test files within the app.

## Manual Testing

During the creation of this project, Google Chrome developer tools was used to view the site/pages on various different devices.
The developer tools displays used were: Galaxy S5, Pixel 2, Pixel 2 XL, iPhone 5/se, iPhone X, iPhone 6/7/8, iPhone 6/7/8 Plus, iPad, iPad Pro.
These were checked at multiple points throughout the development and then once again on all the above devices when the project was deployed.

The site was also tested on various actual devices listed below once the site was completed:

* Dell Laptop
* Samsung Galaxy S9
* iPhone 8
* Samsung tablet
* iPhone 10

The site was then tested on 3 different browsers:
* Google Chrome
* Internet Explorer
* Apple Safari

The site was also tested for fast user learning by asking 3 people to complete a list of tasks on the site. This initially revealed an issue with the automated
email system which was due to a line break in the settings file. The colour of the delivery banner in the checkout was also lightened to catch the user's attention as
this was also mentioned. 

Another bug was found during the checkout process where 2 orders would be created if a user didn't fill in the non-required fields. This
was due to certain fields in the Order model being set to blank and not null, thus causing the webhook to mismatch the order and create a second one.

## Deployment

This project was Deployed using Heroku.

This was done by creating an app in Heroku, dowloading the Heroku CLI toolbelt, logging in to Heroku from the CLI, initializing a git repository and 
connecting git to heroku (`heroku git remote -a`).

In Heroku, Postgres was attached as the chosen database, then dj database url was used to connect the project to Postgres and the database data was loaded
in via the CLI.

After disabling collect static, the project (without static or media files) was pushed to Heroku using the CLI.

An AWS S3 bucket was then created to host the static and media files and boto3 and django-storages were used to connect to S3, where the media files were 
then copied into. 

After adding S3 access keys and Stripe keys to the Heroku config vars, everything was pushed to heroku again to complete the deployment.

The django settings file has also been altered with settings and paths for media links, static links, a default from email address, email host details, an email 
port and altered email backend settings. Many of these settings point to the config variables that have been set in Heroku, as below:

AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, DATABASE_URL, DEFAULT_FROM_EMAIL, EMAIL_HOST_PASS, EMAIL_HOST_USER, SECRET_KEY, STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY,
STRIPE_WEBHOOK_SECRET and USE_AWS.

To Clone the project from github, use:
 `git clone https://github.com/Matte-gtr/on_the_rocks.git`

I recommend deploying the project in a virtual envioronment:
 `cd directory-name`
 `python3 -m venv virtual-env-name`

You will need to install the dependencies found in the requirements.txt file:
 `pip3 install -r requirements.txt` 

Ensure that the Procfile exists:
 `echo web: gunicorn on_the_rocks.wsgi:application > Procfile`

To run the project locally use:
 `python3 manage.py runserver`

#### Credits
Codeinstitute - The stripe setup and webhooks were created following the tutorials from codeinstitute.
Freecodecamp - examples and explanations of using multiple functions.
w3schools - General learning material and descriptions, as well as providing the initial javascript cookie template used with booptstrap accordians.
Django documentation - Used for a great deal of code at the start of the project.
Stack Overflow - various exaples of code were viewed to develop a better understanding of the django framework.
Youtube - the Dumbfounds - information and lessons on django testing.

#### Content
Google images - The default/no-image images.
WhiskeyExchange - The dataset was built using data and images from https://www.thewhiskyexchange.com/ .
Town and Country Mag - Cocktail recipes and images from https://www.townandcountrymag.com/leisure/drinks/g3242/whiskey-cocktails/ .
Tenor - gif loader.

#### Acknowledgements
**Ignatius Ukwuoma** for providing great insight into create projects on a short timescale.
**Kevin** from Codeinstitute for providing a very quick last minute solution to a code problem.

The inspiration for this site primarily came from the codeinstitute Boutique-ado project, building on some of the ideas used in this.