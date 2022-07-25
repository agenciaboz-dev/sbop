from browser import document, ajax, html, bind, window, alert


def showData(req):
    data = eval(req.text)
    data.reverse()

    document['user-title'].text = f'Blog'
    document['user-content'].text = f'Posts: {len(data)}'

    for post in data:
        div = html.DIV('', Class='blog-post')
        title = html.H3(f'Titulo: {post[2]}')
        content = html.P(f'Conteúdo: {post[3]}')
        autor = html.P(f'Autor: {post[4]}')
        date = html.P(f'Data: {post[5]}', style={'margin-bottom': '30px'})

        document['content-container'] <= div
        div <= title
        div <= content
        div <= autor
        div <= date


def ajaxBlog():
    req = ajax.Ajax()
    req.bind('complete', showData)
    req.open('GET', '/get_blog/', True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send({})


ajaxBlog()
