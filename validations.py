from flask import jsonify,request
import re


class Validator:
        def validate_email(self,email):
                expression = re.compile(
                        r"(^[a-zA-Z0-9-.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
                if not expression.match(email) or email.isspace():
                        return False
                return True

        def  validate_password(self,password):
                if not password or password.isspace() or len(password)<8:
                        return False
                return True

        def validate_string_input(self,text):
                letters = re.compile('[A-Za-z]')
                if not letters.match(text) or not text or text.isspace():
                        return False
                return True
