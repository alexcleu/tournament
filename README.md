#Tournament Database
######Able to work on swiss matching for game pairs
* Vagrant SSH into the fullstack environment
  - Go to the directory under vagrant
  - set up vagrant 
  - ssh vagrant to go into the same environment
* Set up the database
  - cd to tournament
  - run "psql -f tournament.sql" to pull the schema into the database 
* Run the tournament_test.py code
  - cd to tournament
  - Under tournament, run tournament_test.py
* completed! Passed all the test!