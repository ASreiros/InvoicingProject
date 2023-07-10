# Invoicing service
This is a service where you can write, review, edit and delete your invoices and print them. Invoicing functionality is available to registered users. There is also a demo account.

## Link to working demo
This project is hosted: https://invoice-asreiros.koyeb.app

## Main functionality:
* User can register into the system
* User can log in into existing account
* User can edit his account information, relevant to invoice.(VAT code, Tax code, address)
* User can also edit his password
* Active user can see list of his invoices
* Active user can delete and edit his invoices
* Active user can issue new invoice
* Invoice (new or edited) can be saved into the database. If the data is missing invoice return error instead
* Invoice can be printed(downloaded as pdf) from the invoice window or from the list window
* PDf is deleted from the system, when the next invoice is printed, after old pdf is no longer needed


## Technology used
* Python (Flask) for backend
* HTML, CSS, Javascript for front end.
* All calculations, even simplest ones are done at backend, frontend responsible only for the visual part  
* Full project requirements can be seen at requirement.txt


## Start
* flask run

## Contact
* Anton Sokolkin 
* email: ansokolkin@gmail.com
* github: https://github.com/ASreiros



