
def load_db(num_load=1000):
    with open('db/db.txt','r') as db:
        return db.read(num_load)
   
def update_db(message:str):
    with open('db/db.txt','a') as db:
        db.write(message)

def delete_db():
    with open('db/db.txt', 'w') as db:
        db.write('')