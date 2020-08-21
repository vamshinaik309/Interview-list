# Interview-list
A simple app where we can create interviews by selecting participants, interview start time and end time.
download all the files ,create a virtual environment for flask
run these commands :
  set FLASK_APP=app.py
  set FLASK_ENV=true
  flask run
  
An interview creation page where the admin can create an interview by selecting participants, start time, and end time. Backend should throw an error with a proper error message if: 
  Any of the participants is not available during the scheduled time (i.e, has another interview scheduled)
  No of participants is less than 2
An interview list page where admin can see all the upcoming interviews.
An interview edit page where the admin can edit the created interview with the same validations as on the creation page.
Note: No need to add a page to create Users/Participants. Create them directly in the database


