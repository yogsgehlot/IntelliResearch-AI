import app.core.ai_container as container
from app.core.ai_container import AIContainer


def initialize_ai():

    print("Initializing AI...")

    if container.ai_container is None:

        container.ai_container = AIContainer()

    print("Done")