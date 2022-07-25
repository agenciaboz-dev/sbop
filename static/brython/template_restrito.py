from browser import document, ajax, html, bind, window, alert

member = None


class Member():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.uf = data['uf']
        self.cep = data['cep']
        self.member = data['member']


class Video():
    def __init__(self, element, src):
        self.playing = False
        self.element = element
        self.fullscreen = False
        self.src = src
        self.name = src[:-4]

    def play(self):
        self.element.play()
        self.playing = True

    def pause(self):
        self.element.pause()
        self.playing = False


def showData(req):
    global member
    data = eval(req.text)
    member = Member(data)

    document['user-title'].text = f'Você tem acesso a conteúdo do nível: {member.member}'
    document['user-content'].text = f'Conteúdo virá aqui \/'

    def ajaxVideos():
        req = ajax.Ajax()
        req.bind('complete', showList)
        req.open('GET', '/get_videos/', True)
        req.set_header('content-type', 'application/x-www-form-urlencoded')
        req.send({})

    def showList(req):
        videos = eval(req.text)
        for item in videos:
            showVideo(item)

    ajaxVideos()


def showVideo(src):
    video = Video(document['video'], src)
    document['list-container'] <= html.P(
        f'{video.name.replace("_", " ")}', Id=f'video-{video.name}', Class='list-items', Style={'color': '#094e93'})

    @bind(f'#video-{video.name}', 'click')
    def load_video(ev):
        document['video'].src = f'/static/videos/{member.member}/{video.src}'
        document['video'].style.visibility = 'visible'

        for item in document.select('.list-items'):
            item.style.color = '#094e93'

        ev.target.style.color = '#74ace4'

        @bind('#video', 'contextmenu')
        def no_rightclick(ev):
            ev.preventDefault()

    # @bind('#player-button', 'click')
    # def player_button(ev):
    #     if video.playing:
    #         video.pause()
    #         ev.target.text = 'Play'
    #     else:
    #         video.play()
    #         ev.target.text = 'Pause'

    # @bind('#fullscreen', 'click')
    # def player_fullscreen(ev):
    #     video.element.requestFullscreen()

    #     if video.fullscreen:
    #         video.element.style.pointerEvents = 'none'
    #         video.fullscreen = False
    #     else:
    #         video.element.style.pointerEvents = 'auto'
    #         video.fullscreen = True


def ajaxRestrito():
    req = ajax.Ajax()
    req.bind('complete', showData)
    req.open('GET', '/get_member/', True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send({})


ajaxRestrito()
