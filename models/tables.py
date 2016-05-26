#########################################################################
## Define your tables below; for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

from datetime import datetime

db.define_table('boards',
                Field("title"),
                Field("createdBy", db.auth_user, default = auth.user_id),
                Field("createdOn", 'datetime', default = datetime.utcnow()),
                Field("updatedOn", 'datetime'),
                Field("description"),
                Field("board_id")
                )


db.define_table('posts',
                Field("title"),
                Field('description'),
                Field('board_id'),
                Field('post_id'),
                Field("is_draft","boolean"),
                Field("createdBy",db.auth_user, default = auth.user_id),

                Field("createdOn", 'datetime', default = datetime.utcnow()),
                Field('likes', 'integer', default = 0)
                )

