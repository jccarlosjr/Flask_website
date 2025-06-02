# Flask Blog

This is a blog project developed with Flask and Python. It allows users to create accounts, log in, edit their profiles, and publish blog posts. Additionally, users can view posts from other users and delete their own posts.

## Requirements

Before getting started, make sure you have the following installed:

- Python 3.7 or higher  
- pip (Python package manager)  
- Virtualenv (recommended for creating an isolated virtual environment)

## Installation

Follow the steps below to set up the development environment:

1. Clone the repository:

   git clone https://github.com/jccarlosjr/Flask_website.git

2. Navigate to the project directory:

   cd flask-blog

3. Create and activate the virtual environment:

   python -m venv venv  
   source venv/bin/activate  # On Windows use: venv\Scripts\activate

4. Install the dependencies:

   pip install -r requirements.txt

5. Create the database:

   flask shell

6. In the Python prompt, run:

   from comunidadeimpressionadora import database  
   database.create_all()  
   exit()

7. Run the project:

   flask run

## Features

- Sign Up and Login: Users can create an account and log in.  
- Profile Editing: Users can update their profile information and profile picture.  
- Post Creation and Editing: Users can create and edit posts.  
- Post Deletion: Users can delete their own posts.  
- User Listing: Users can view a list of all registered users.
