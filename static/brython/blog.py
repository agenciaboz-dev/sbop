from browser import document, ajax, html, bind, window, alert
import datetime


# class Member():
#     def __init__(self, data):
#         self.id = data['id']
#         self.name = data['name']
#         self.uf = data['uf']
#         self.cep = data['cep']
#         self.member = data['member']


def showData(req):
    data = eval(req.text)
    # member = Member(data)

    document['user-title'].text = f'Blog'
    document['user-content'].text = f'Posts: {len(data)}'

    for post in data:
        title = html.H3(f'Titulo: {post[2]}')
        content = html.P(f'Conteúdo: {post[3]}')
        autor = html.P(f'Autor: {post[4]}')

        document['content-container'] <= title
        document['content-container'] <= content
        document['content-container'] <= autor


def ajaxBlog():
    req = ajax.Ajax()
    req.bind('complete', showData)
    req.open('GET', '/get_blog/', True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send({})


ajaxBlog()
