# HappySQL
## Description
HappySQL is a RESTful API that allows anyone to perform simple SQL resquests.
The SQL interpretation is abstacted so any developper can create it's own SQL
module to fulfill his needs.

<br/>

## Project Structure
* ### HappySQL_Server
  Core of the project! A Python REST server that implements the API calls and
translate them into SQL requests.
* ### WebApp_Client
  An AngularJS client. HappySQL implementation example.
* ### Python_Client
  A minimalistic Python client. HappySQL implementation example.
