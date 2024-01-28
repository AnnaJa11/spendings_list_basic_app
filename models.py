import json

class Spendings:
    def __init__(self):
        try:
            with open("spendings.json", "r") as f:
                self.spendings = json.load(f)
        except FileNotFoundError:
            self.spendings = []
    
    def all(self):
        return self.spendings
    
    def get(self, id):
        return self.spendings[id]
    
    def create(self, data):
        data.pop('csrf_token')
        self.spendings.append(data)

    def save_all(self):
        with open("spendings.json", "w") as f:
            json.dump(self.spendings, f)
    
    def update(self, id, data):
        data.pop('csrf_token')
        self.spendings[id] = data
        self.save_all()

spendings = Spendings()