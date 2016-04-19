from twisted.web import server, resource


class EventsEndpoint(resource.Resource):

    isLeaf = True

    def __init__(self):
        resource.Resource.__init__(self)
        self.event_request = None

    def render_GET(self, request):
        self.event_request = request
        return server.NOT_DONE_YET
