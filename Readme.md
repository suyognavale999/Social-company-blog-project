## Application Overview:-

* Flask-based web application for blog management.
* Users can register and log in securely.
* Manage user profiles and upload profile pictures.
* Create, edit, and delete blog posts.
* Uses SQLite for data storage.
* Provides a simple, clean, and responsive user interface.
* Built using Flask, SQLAlchemy, Jinja2, and Bootstrap.

==================================================================================================
## Project Setup:

1. Clone the Repository
git clone https://github.com/suyognavale999/Social-company-blog-project.git
cd Social-company-blog-project

2. Create & Activate Virtual Environment
py -3.11 -m venv Blogvenv
Blogvenv\Scripts\Activate

3. Install Dependencies
pip install -r requirements.txt

If required:

pip install Pillow
pip install gunicorn

4. Run the Application
flask run
or
python app.py

Open in your browser:
http://127.0.0.1:5000

5. Database
Database: SQLite
Open the .db file using the SQLite Viewer extension in VS Code.