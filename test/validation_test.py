from unittest import TestCase
from app.validation.field_validation import *
from app.exception.copy_exception import CopyException
from app.validation.validate_email_address import *





class TestValidation(TestCase):

    def test_valid_password(self):
         password = "password@123"

         try:
              validate_password(password)
         except CopyException as e:
              self.fail(e.message)


    def test_invalid_password(self):
        password = "wrong password"

        with self.assertRaises(CopyException):
               validate_password(password)


    def test_valid_role(self):
         data = {"role":"personal"}

         try :
              validate_user_role(data)
         except CopyException as e:
              self.fail(e.message)

    
    def test_invalid_role(self):
         data = {"role":"invalid_role"}

         with self.assertRaises(CopyException):
              validate_user_role(data)

    
    def test_organization_name_cannot_be_empty(self):
         data = {"organization_name": ""}
         
         with self.assertRaises(CopyException):
              validate_organization_name(data)


    def test_organization_name_wont_fail_if_value(self):
         data = {"organization_name": "default"}

         try:
              validate_organization_name(data)
         
         except CopyException as e:
              self.fail(e.message)
    
     
    def test_organization_name_cannot_be_null(self):
         data = {"organization_name": "null"}
         
         with self.assertRaises(CopyException):
              validate_organization_name(data)

    
    def test_organization_name_cannot_be_Null(self):
         data = {"organization_name": "Null"} 
         
         with self.assertRaises(CopyException):
              validate_organization_name(data)

    
    def test_firstname_cannot_be_empty(self):

        required_fields = {'first_name' : "", 'last_name' : "testing last name", 'email_address' : "test@email.com", 'phone_number' : "090345678", 'password' : "pass@2490", 'role' : "personal"}
        
        with self.assertRaises(CopyException):
             validate_registration_field(required_fields)

    
    def test_firstname_cannot_be_null(self):

        required_fields = {'first_name' : "null", 'last_name' : "testing last name", 'email_address' : "test@email.com", 'phone_number' : "090345678", 'password' : "pass@2490", 'role' : "personal"}
        
        with self.assertRaises(CopyException):
             validate_registration_field(required_fields)

    
    def test_firstname_cannot_be_Null(self):

        required_fields = {'first_name' : "Null", 'last_name' : "testing last name", 'email_address' : "test@email.com", 'phone_number' : "090345678", 'password' : "pass@2490", 'role' : "personal"}
        
        with self.assertRaises(CopyException):
             validate_registration_field(required_fields)


    def test_field_wont_fail_if_value(self):
        required_fields = {'first_name' : "testing first name", 'last_name' : "testing last name", 'email_address' : "test@email.com", 'phone_number' : "090345678", 'password' : "pass@2490", 'role' : "personal"}
        
        try:
             validate_registration_field(required_fields)
        except CopyException as e :
            self.fail(e.message) 
    
    
    def test_lastname_cannot_be_empty(self):

        required_fields = {'first_name' : "testing first name", 'last_name' : " ", 'email_address' : "test@email.com", 'phone_number' : "090345678", 'password' : "pass@2490", 'role' : "personal"}
        
        with self.assertRaises(CopyException):
             validate_registration_field(required_fields)


    def test_lastname_cannot_be_null(self):

        required_fields = {'first_name' : "testing first name", 'last_name' : "null", 'email_address' : "test@email.com", 'phone_number' : "090345678", 'password' : "pass@2490", 'role' : "personal"}
        
        with self.assertRaises(CopyException):
             validate_registration_field(required_fields)


    def test_lastname_cannot_be_Null(self):

        required_fields = {'first_name' : "testing first name", 'last_name' : "Null", 'email_address' : "test@email.com", 'phone_number' : "090345678", 'password' : "pass@2490", 'role' : "personal"}
        
        with self.assertRaises(CopyException):
             validate_registration_field(required_fields) 

    
    def test_email_address_cannot_be_empty(self):
        required_fields = {'first_name' : "testing first name", 'last_name' : "testing last name", 'email_address' : " ", 'phone_number' : "090345678", 'password' : "pass@2490", 'role' : "personal"}
        
        with self.assertRaises(CopyException):
             validate_registration_field(required_fields) 
    
    def test_email_address_cannot_be_null(self):
        required_fields = {'first_name' : "testing first name", 'last_name' : "testing last name", 'email_address' : "null", 'phone_number' : "090345678", 'password' : "pass@2490", 'role' : "personal"}
        
        with self.assertRaises(CopyException):
             validate_registration_field(required_fields) 
    
    def test_email_address_cannot_be_Null(self):
        required_fields = {'first_name' : "testing first name", 'last_name' : "testing last name", 'email_address' : "Null", 'phone_number' : "090345678", 'password' : "pass@2490", 'role' : "personal"}
        
        with self.assertRaises(CopyException):
             validate_registration_field(required_fields) 
    
    def test_phone_number_cannot_be_empty(self):
        required_fields = {'first_name' : "testing first name", 'last_name' : "testing last name", 'email_address' : "test@gmail.com", 'phone_number' : " ", 'password' : "pass@2490", 'role' : "personal"}
        
        with self.assertRaises(CopyException):
             validate_registration_field(required_fields) 
    
    def test_phone_number_cannot_be_null(self):
        required_fields = {'first_name' : "testing first name", 'last_name' : "testing last name", 'email_address' : "test@gmail.com", 'phone_number' : "null", 'password' : "pass@2490", 'role' : "personal"}
        
        with self.assertRaises(CopyException):
             validate_registration_field(required_fields) 
    
    def test_phone_number_cannot_be_Null(self):
        required_fields = {'first_name' : "testing first name", 'last_name' : "testing last name", 'email_address' : "test@gmail.com", 'phone_number' : "Null", 'password' : "pass@2490", 'role' : "personal"}
        
        with self.assertRaises(CopyException):
             validate_registration_field(required_fields)
    
    def test_password_cannot_be_empty(self):
        required_fields = {'first_name' : "testing first name", 'last_name' : "testing last name", 'email_address' : "test@gmail.com", 'phone_number' : "0908756378", 'password' : " ", 'role' : "personal"}
        
        with self.assertRaises(CopyException):
             validate_registration_field(required_fields) 
    
    def test_password_cannot_be_null(self):
        required_fields = {'first_name' : "testing first name", 'last_name' : "testing last name", 'email_address' : "test@gmail.com", 'phone_number' : "0908756378", 'password' : "null", 'role' : "personal"}
        
        with self.assertRaises(CopyException):
             validate_registration_field(required_fields) 
    
    def test_password_cannot_be_Null(self):
        required_fields = {'first_name' : "testing first name", 'last_name' : "testing last name", 'email_address' : "test@gmail.com", 'phone_number' : "0908756378", 'password' : "Null", 'role' : "personal"}
        
        with self.assertRaises(CopyException):
             validate_registration_field(required_fields) 
    
    def test_role_cannot_be_empty(self):
        required_fields = {'first_name' : "testing first name", 'last_name' : "testing last name", 'email_address' : "test@gmail.com", 'phone_number' : "0908756378", 'password' : "password@123", 'role' : ""}
        
        with self.assertRaises(CopyException):
             validate_registration_field(required_fields) 
    
    def test_role_cannot_be_null(self):
        required_fields = {'first_name' : "testing first name", 'last_name' : "testing last name", 'email_address' : "test@gmail.com", 'phone_number' : "0908756378", 'password' : "password@1234", 'role' : "null"}
        
        with self.assertRaises(CopyException):
             validate_registration_field(required_fields) 
    
    def test_role_cannot_be_Null(self):
        required_fields = {'first_name' : "testing first name", 'last_name' : "testing last name", 'email_address' : "test@gmail.com", 'phone_number' : "0908756378", 'password' : "password@1234", 'role' : "Null"}
        
        with self.assertRaises(CopyException):
             validate_registration_field(required_fields) 
    
    def test_valid_email(self):
         email = "test@gmail.com"

         try:
              validate_email(email)
         except CopyException as e:
              self.fail(e.message)
    
    def test_invalid_email(self):
        email = "invalid email"

        with self.assertRaises(CopyException):
             validate_email(email)
    
    