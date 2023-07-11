from saracen import SaracenDB

db = SaracenDB('data.sr')

db.put('a', [1, 2, 3])

# db.rm('a')

db.push()
print(db.get('a'))
