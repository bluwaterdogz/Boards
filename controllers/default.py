# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

from datetime import datetime
from gluon import utils as gluon_utils
import json
import time

def index():
    draft_id = gluon_utils.web2py_uuid()
    return dict(
                draft_id = draft_id,
                )

def load_boards():
    boards = db(db.boards.id > 0).select()
    board_dict = {b.board_id:{
            'board_title':b.title,
            'board_createdBy':b.createdBy,
            'board_createdOn':b.createdOn,
            'board_updatedOn':b.updatedOn,
            'board_description':b.description,

        } for b in boards}
    return response.json(dict(board_dict = board_dict))

@auth.requires_login()
@auth.requires_signature()
def save_board():
    db.boards.update_or_insert((db.boards.board_id == request.vars.board_id),
        title = request.vars.title,
        description = request.vars.descrption,
        board_id = request.vars.board_id,
        createdBy = request.vars.createdBy
    )
    return request

@auth.requires_login()
@auth.requires_signature()
def delete_board():
    board_id = request.vars.board_id
    db(db.boards.board_id == request.vars.board_id).delete()
    return board_id

def get_new_id():
    draft_id = gluon_utils.web2py_uuid()
    return response.json(dict(draft_id=draft_id))

def board():
    draft_id = gluon_utils.web2py_uuid()
    board_id = request.args(0)
    return dict(
                draft_id = draft_id,
                board_id = board_id
                )

def load_posts():
    posts = db(db.posts.id > 0).select()
    post_dict = {p.post_id:{
            'post_board':p.board_id,
            'post_title':p.title,
            'post_createdBy':p.createdBy,
            'post_user':p.createdBy.first_name,
            'post_createdOn':p.createdOn,
            'post_description':p.description,
            # 'post_is_draft':p.is_draft

        } for p in posts}
    # time.sleep(2)
    return response.json(dict(post_dict = post_dict))

@auth.requires_login()
@auth.requires_signature()
def save_post():
    time.sleep(2)
    db.posts.update_or_insert((db.posts.board_id == request.vars.post_id),
        board_id = request.vars.board_id,
        title = request.vars.title,
        description = request.vars.descrption,
        post_id = request.vars.post_id,

    )
    return request

@auth.requires_login()
@auth.requires_signature()
def delete_post():
    post = request.vars.post_id
    db(db.posts.post_id == request.vars.post_id).delete()
    return post

# reset field for testing
# def reset():
#     db(db.posts.id > 0).delete()
#     db(db.boards.id > 0).delete()
#     return dict(momo="Howdy")


#     # Count new posts
# def num_new_posts(board_id):
#     num_new_posts = 0
#     post_list = db(db.posts.board == board_id).select()
#     for p in post_list:
#         now = datetime.utcnow()
#         c = ( now - p['createdOn'] )
#         if c.days== 0:
#             num_new_posts = num_new_posts+1
#     return num_new_posts
#
#     # Count my posts
# @auth.requires_login()
# def num_my_posts(board_id):
#     num_my_posts = 0
#     post_list = db(db.posts.board == board_id).select()
#     for p in post_list:
#         if auth.user_id == p['createdBy']:
#             num_my_posts = num_my_posts+1
#     return num_my_posts
#
#     # Delete post
# @auth.requires_login()
# @auth.requires_signature()
# def deletePost():
#     post_id = request.args(0)
#     post = db.posts(post_id)
#     if post is None:
#         redirect(URL('default','board', args=request.args(1)))
#         session.flash = "Sorry, no such post homie!"
#     db(db.posts.id == post_id).delete()
#     redirect(URL("default","board", args=[request.args(1)]), client_side= True)
#     session.flash = "Post Deleted"
#     return True
#
#
#     # update post
# @auth.requires_login()
# @auth.requires_signature()
# def updatePost():
#     record = db.posts(request.args(0))
#     if record is None:
#         redirect(URL('default','board', args=request.args(1)))
#         session.flash = "No such Post"
#     form = SQLFORM(db.posts,record = record, deletable = True)
#     form.add_button(T('Home'),URL('default','board', args=request.args(1)),_class='btn btn-primary')
#     if form.process().accepted:
#         redirect(URL('default','board', args=request.args(1)))
#         session.flash = "Post Updated"
#     return dict(form = form)
#
# @auth.requires_login()
# def likePost():
#     record = db(db.posts.id == request.args(0))
#     if record is None:
#         redirect(URL('default','board', args=request.args(1)))
#         session.flash = "No such Post"
#     lks = int(request.args(2))
#     record.update(likes=lks+1)
#     redirect(URL('default','board', args=request.args(1)))
#     return True
#



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
