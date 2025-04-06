from mongoengine import Document, StringField,EmailField,IntField
import datetime
class User(Document):
    username = StringField(required=True)
    number=StringField(required=True)
    email= EmailField(unique=True,required=True)
    auth_token = StringField()
    password=StringField(required=True)
    address = StringField()
    vehicle_no = StringField(unique=True,required=True)
    fine = IntField(defualt=0)

    def update(self, **kwargs):
        self.clean()
        return super().update(**kwargs)
   
    def to_json(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "number":self.number if self.number else None,
            "email":self.email if self.email else None,
            "address":self.address if self.address else None,
            "vehicle_no":self.vehicle_no if self.vehicle_no else None,
            "fine":self.fine,
        }


    def remove_expired_tokens(self):
        current_time = datetime.datetime.utcnow()
        valid_tokens = [token for token in self.authToken if 'exp' in token and token['exp'] > current_time]
        self.update(set__authToken=valid_tokens if valid_tokens else "")
