# Foodmart-Assignment
The foodmart vending machine contains 2 APIs, one for Loading or updating the machine with items and other one for fetching items based on amount and requirement.

##Running the Server
To run the program first enter your MongoDB credentials in the .env file including mongo HOST, PORT, USERNAME and PASSWORD.
To run the server:
`python server.py`

##APIs:

1. POST /loadmachine
- Accepts json body for item, cost and quantity as request parameters and initialises or updates the Database for those items.

2. GET /fetchitems
- Accepts item, amount and quantity as request parameters and return response for the successful or unsuccessful purchase. Also update the database after a successful purchase.

