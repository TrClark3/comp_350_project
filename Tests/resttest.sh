#! /bin/bash 

echo "Test 1: Inserting users into the database"
curl -H "Content-Type: application/json" -d '{	"username": "suscipit.nonummy@nenec.co.uk",	"password": "KLH24GVU5RE",	"f_name": "Hayfa",	"l_name": "Gray",	"age": 36}' -X POST http://localhost:8000/api/users
curl -H "Content-Type: application/json" -d '{	"username": "mi.ac@lobortis.co.uk",	"password": "YWR25ETU2MO",	"f_name": "Athena",	"l_name": "Bentley",	"age": 95}' -X POST http://localhost:8000/api/users
curl -H "Content-Type: application/json" -d '{	"username": "placerat@augueid.ca",	"password": "QNH11HER6RH",	"f_name": "Paloma",	"l_name": "Potts",	"age": 57}' -X POST http://localhost:8000/api/users
curl -H "Content-Type: application/json" -d '{	"username": "quis.lectus@ametconsectetuer.net",	"password": "UOU42VFI5YI",	"f_name": "Isaac",	"l_name": "Kane",	"age": 21}' -X POST http://localhost:8000/api/users
curl -H "Content-Type: application/json" -d '{	"username": "justo.nec@diam.com",	"password": "RFV29FGZ3UD",	"f_name": "Daquan",	"l_name": "Vance",	"age": 63}' -X POST http://localhost:8000/api/users

echo ""
echo "Test 2: Get all Users"
curl -X GET http://localhost:8000/api/users

echo ""
echo "Test 3: Get a User"
curl -X GET http://localhost:8000/api/users?user_id=2

echo ""
echo "Test 4: Update a user"
curl  -H "Content-Type: application/json" -d '{	"username": "mi.ac@lobortis.co.uk",	"password": "YWR25ETU2MO",	"f_name": "Athena",	"l_name": "Bentley",	"age": 55}' -X PUT http://localhost:8000/api/users?user_id=2

echo ""
echo "Test 5: Delete a user"
curl -X DELETE http://localhost:8000/api/users?user_id=3

echo ""
echo "Test 6: End result"
curl -X GET http://localhost:8000/api/users