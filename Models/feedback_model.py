from mongoengine import Document, StringField,ReferenceField,DateTimeField
from datetime import datetime
from Models.user_model import User

class Feedback(Document):
    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    feedback = StringField(required=True)
    created_at = DateTimeField(default=datetime.now)
   

    def update(self, **kwargs):
        self.clean()
        return super().update(**kwargs)
   
    def to_json(self):
        return {
            "id": str(self.id),
            "user": self.user,
            "feedback":self.feedback if self.feedback else None,
            "created_at":self.created_at if self.created_at else None,

        }
