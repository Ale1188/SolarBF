Create a virtual environment:
MAC: python3 -m venv venv
Windows: py -m venv venv

Activate the virtual environment
MAC: source venv/bin/activate
Windows: venv/Scripts/activate

Install requirements
pip install -r requirements.txt


Create .env in config with this:
---------------------------------------
HOST_PASSWORD='Yours'
HOST_EMAIL='Yours'

STRIPE_PUBLIC_KEY ='Yours'
STRIPE_SECRET_KEY='Yours'

STRIPE_PUBLIC_KEY_TEST ='Yours'
STRIPE_SECRET_KEY_TEST='Yours'

DEBUG=True
SECRET_KEY='Yours'
---------------------------------------


Run server
python3 manage.py runsever