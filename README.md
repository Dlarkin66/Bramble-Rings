
Title: Bramble Rings E-Commerce Website

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Description: An E-commerce website where customers can go to purchase handmade rings. 

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Prerequisites: Check requirements.txt

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Installation: 

After downloading create a secret.py file under the website folder. Here you will need to create a variable named "admin" and set it equal to the email you created an account with. This will give you permission to add, remove, and edit products. 

Create a variable named "secret_key" as well and set it equal to a key of your choice. 

Create another variable in secret.py called "stripe_secret_key" and set it to your live stripe API key. You can find this on stripes website after creating an account, see their documentation for more details. 

Create another variable in secret.py called "mail_email" and set this to a gmail that you want customers to be able to contact you with. 

Create another variable named "mail_password" to gmail app password key linked to the "mail_email" you chose. You can find further information on app password keys online in googles settings. 

You will then need to set one last variable named "endpoint_secret" and set it to your webhook endpoint. For more details on this refer to the Stripe CLI documentation. 

Next, in the auth.py file locate the "/cart" route. You will see a "checkout_public_key" variable. Replace the existing key with your stripe public key (see stripe documentation for more detail).

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Usage:

To add new products login into your admin account and add "/add-product" to the url while on the home page. This will take you to a form where you can add all the information you need. 

The "order" field is the order in which you want your products to be displayed on the home page. If you set it to 0 it will be the first the you see, if its 1 it will be the second thing you see, so on so forth. 

The "Stripe Price ID" field is needed for checkout to work. Go to stripe and add your product there, then copy and paste the stripe price id to the form.

To remove a product simply click the remove button under each item on the home page. 

To edit a product click on it and then click the "edit" button on the product details page. Here you can change all the information and send it to the database. 

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Project Structure:

The instance folder contains your website database.

The migrations folder contains any database migrations if you need to add new columns to your database table. 

The venv folder is the virtual environment. 

The website folder contains everything needed to run the website. 

In the static folder we have all of the css rules for styling, gallery.js which makes the product details gallery interactive, and script-no-ajax.js which is used for redirecting to the stripe checkout page. 

The templates folder contains all of the html templates. They are all clearly labeled and can be customized to your liking. 

Init.py has the database creation, flask mail setup, and user login manager.

auth.py contains any and all routes that require some sort of authentification. I.E, admin routes or routes that can only be accessed by users when they are logged in. This is where a majority of the routes are. 

models.py has the database tables.

secret.py will contain all sensitive information. See the instructions above on how to set that up.

views.py contains the remaining routes that everyone has access to regardless of being logged in or not. 

app.py is used to run the code. 

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


