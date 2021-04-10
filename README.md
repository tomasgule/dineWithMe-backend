### Kom i gang
- Åpne terminalen og gå inn i mappa du vil ha koden i 
- `git clone https://gitlab.stud.idi.ntnu.no/tdt4140/landsby-3/gruppe-50/dinewithme.git`
- `pipenv install` fra root-mappa
- `npm install` fra root-mappa

### Starte serveren:
- `cd dineWithM`
- `python manage.py runserver`

### Bygge endringer
- `npm run dev`

############
# For å regristere en bruker
http://127.0.0.1:8000/api/auth/register

# For å åpne bruker
http://127.0.0.1:8000/api/auth/user

# For å logge inn
http://127.0.0.1:8000/api/auth/login

# For å opprette middagsarrangement
http://127.0.0.1:8000/api/dinnerEvent/ 

# For å logge ut
http://127.0.0.1:8000/api/auth/logout 
