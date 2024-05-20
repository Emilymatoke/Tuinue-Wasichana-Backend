from models import User , Role , db

def create_roles ():
    administrator= Role(id=1,name='administrator')
    charity=Role(id=2,name='charity')
    donor=Role(id=3 ,name='donor')

    db.session.add(administrator)
    db.session.add(charity)
    db.session.add(donor)

    db.session.commit()
    print('Roles created')

create_roles ()