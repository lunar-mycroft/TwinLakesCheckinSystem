import peewee as pw

db = pw.SqliteDatabase('test.db')

class Card(pw.Model):
    lastName = pw.CharField()
    isGuest = pw.BooleanField()

    class Meta:
        database = db

class Visit(pw.Model):
    card = pw.ForeignKeyField(Card)
    numberVisitors = pw.IntegerField()
    date = pw.DateField()
    name = pw.CharField()
    enteredOwnerName = pw.CharField(null=True)
    isGuest = pw.BooleanField()

    class Meta:
        database = db

db.connect()
db.create_tables([Card, Visit], safe=True)

if __name__ == "__main__":
    for name in ['Abet', 'Smith', 'Jones', 'Park', 'Clark']:
        Card.create(
            lastName = name,
            isGuest = True
        )
        Card.create(
            lastName = name,
            isGuest = False
        )
