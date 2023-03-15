Initial changes
===============

Started off with a review of the existing code, and made some quick changes to tick off
the speed improvement aspect and tweak for best practise.  I added some Meta sorting to
the Models, along with a string response.  I also amended the test to use reverse for the
url collection rather than having the URL be hard-coded in the test.
For the speed improvements I added pagination on the existing API list response
and the queryset prefetch_related on the API view.  Also installed the python linting
to ensure code quality, so I can add comments etc as I move through the code and save time.

I then setup the basic admin for the existing models to help with checking the create method
once it has been done.  At this point I noticed the issue with the initial DB import and 
updated the values of ANIMAL_TYPE_CHOICES before re-importing the data correctly.

Part 1: Allow assignments to be created
=======================================

Made a quick list of the tasks to be done:
 - Create the basic serialiser for the Assignment model
 - Create the API View and link in the URL, check creation worked correctly
 - Add the Validation for the date restrictions
 - Add the validation for the overlap
 - Add tests for the new functionality

I ran through the above list, did some checks all was working.

Part 2: Scaling Trouble
=======================
The previous changes made (DRF pagination and prefetch_related) would help with scaling on the
listings API.  Further improvements to be made would include:
- Django side caching, which could be invalidated by writes.  This effectiveness would depend on the frequency of listings being updated.
- DRF could be bypassed for the high-traffic APIs, with performance being increased by returning specifically what is required without the overhead of the DRF serialiser.  This would depend on what other DRF functionality was required (authentication, caching, rate-limiting etc) on if this could be an option or not.

Other Notes:
============
There are no additional requirements needed to run the project.  The only additional install was the pycodestyle linter for Visual Studio Code.
Constraints could be made on the date fields to ensure end date is after the start date, this would however also need custom exception handling in DRF as the constraint is currently only DB level in Django and fails on save rather than validating prior to this.
The initial data provided with the app with the provided instructions do not correctly assign the "animal type" to the "Pet".  Looks like the ANIMAL_TYPE_CHOICES has been defined backwards, with the key being second instead of being first.  After reversing this and running the loaddata command again, the data is correctly assigned.
There is a potential issue using the DRF Validation of the data, as the validation is then only being done if data is being updated via the API and not VIA the admin.  I gave
consideration to moving the validation to the Model layer while using a custom error handler on DRF to catch the Django Validation error correctly, but decided that the
expected solution was probably to use DRF validation, so I went with that for this example.
There is no awareness of timezone in the API start_date and end_date being received, this would likly cause issues when used in timezones different from the server time.
Testing could be more comprehensive, firstly around the edge cases of the date checks and also around testing the existing functionality etc.  I went with matching a 
similar level of test coverage to what already existed within the app, and only adding tests for functionality which was added.


Run project
===========

```
source venv/bin/activate
cd ths
./manage.py runserver
````

This runs the Django devserver on port 8000.

You can now access the API using curl, e.g.

```
curl http://localhost:8000/listings/
```

or go to http://localhost:8000/listings/ in your browser



Run test suite
==============

```
source venv/bin/activate
cd ths
./manage.py test
````