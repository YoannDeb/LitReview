# LitReview

Training django project - Book reviewing web application.

Part of [Open Classrooms](/https://openclassrooms.com) "DA Python" formation, 9th Project.

## Creating Virtual environment, downloading and running the program:

You need Python 3 (tested on 3.9.5), git and venv installed on your machine.

Open a terminal and navigate into the folder you want LitReview to be downloaded, and run the following commands:

* On Linux or macOS:
```bash
git clone https://github.com/YoannDeb/LitReview.git
cd LitReview
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cd LitReview
python manage.py runserver
```

* On Windows:
```bash
git clone https://github.com/YoannDeb/LitReview.git
cd LitReview
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
cd LitReview
python manage.py runserver
```

You can then access LitReview locally at the following address: http://127.0.0.1:8000

## Example database:

### Consultation of examples:

An example db.sqlite3 is included in the repository.
It contains fictional users, tickets and reviews.
The password for all users is their username.
You can use the user yoann, password yoann, which is admin of the site (can access http://127.0.0.1:8000/admin).
You can then consult all users in his follow page, or in the admin interface, or create new users.

List of example users:
* Adonis
* Aude
* Gérard
* Jacques
* Jerome
* Julien
* Paul
* Robert
* audrey
* bernard
* yoann

### Reset of database:

Just delete db.sqlite3 file, then enter the following command in a terminal in the app folder with the environment activated:
```
python manage.py migrate
```


If you want to recreate an admin user, type in a terminal in the app folder with the environment activated:
```
python manage.py createsuperuser 
```
Then fill the username, mail and password two times when asked.

## How to use the app?

### Authentication:

If you are not logged in, you will be redirected to the login page.
There you can log in with your username and password or create an account using "inscription" tab.

### Flux:

"Flux" page is your main feed where you'll see all your posts and all your followed users' posts, including tickets and reviews, sorted by time of publication (newer first).

You can create a new ticket (i.e. ask for a book review) by clicking "Demander une critique" button.
You can create a new review (i.e. create a ticket and the review associated) by clicking the "Créer une critique" button.
You can create a review in response to a ticket by clicking the "Soumettre une critique" button in a not yet answered ticket you want to answer.

### Mes posts:

Here you can see all your previous posts on the site.

You can modify a post (ticket or review) by clicking the "Modifier" button.
You can delete a post (ticket or review) by clicking the "Supprimer" button.

Be careful, if you delete a ticket and a response existed, the ticket and the review will be deleted.

### Abonnements:

Here you can consult and manage your follows and followers.

#### Search section:

You can search for users to follow:
* Type the exact name of your follow, it will be added to your follows.
* Type a part of the name to see all matches in users database and click the "s'abonner" button in front of the user you want to add to your follows.
* Click "Montrer tous les utilisateurs auxquels je ne suis pas déjà abonné" to show all existing users you don't follow yet. Then click the "s'abonner" button in front of the user you want to add to your follows.

### Abonnements:

You'll see there all the users you actually follow.
You can click on the "Se désabonner" button in front of the user you want to unfollow.

### Abonnés:

Here you can see all users that follows you.
You can follow them back if you don't already by clicking on the "Ajouter à mes abonnements" button in front of the user you want to follow back.

## Se déconnecter du compte <user>

You can close your session by clicking on this menu entry.
You'll be redirected to the login page.
