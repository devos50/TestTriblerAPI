import logging

from twisted.internet import reactor
from twisted.web.server import Site

from endpoints.root_endpoint import RootEndpoint
from tribler_data import TriblerData
import tribler_utils


def generate_tribler_data():
    tribler_utils.tribler_data = TriblerData()

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

logger.info("Generating random Tribler data")
generate_tribler_data()

site = Site(RootEndpoint())
logger.info("Starting fake Tribler API on port 8085")
reactor.listenTCP(8085, site)
reactor.run()
