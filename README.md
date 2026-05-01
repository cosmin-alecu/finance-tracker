https://finance-tracker-bapy.onrender.com
comenzi test POWERSHELL:
-adauga cont: Invoke-WebRequest -Uri "https://finance-tracker-bapy.onrender.com/accounts" -Method POST -ContentType "application/json" -Body '{"name": "Checking", "type": "checking", "balance": 1000}'
-adauga categorie: Invoke-WebRequest -Uri "https://finance-tracker-bapy.onrender.com/categories" -Method POST -ContentType "application/json" -Body '{"name": "Salary", "type": "income"}'
-adauga tranzactie: Invoke-WebRequest -Uri "https://finance-tracker-bapy.onrender.com/transactions" -Method POST -ContentType "application/json" -Body '{"account_id": 1, "category_id": 1, "amount": 3000, "type": "income", "description": "Salariu"}'
-verificare GET: Invoke-WebRequest -Uri "https://finance-tracker-bapy.onrender.com/accounts" -Method GET | Select-Object -ExpandProperty Content
-delete: Invoke-WebRequest -Uri "https://finance-tracker-bapy.onrender.com/accounts/1" -Method DELETE
