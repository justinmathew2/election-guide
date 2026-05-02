from enum import Enum

class JourneyState(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    REGISTRATION = "REGISTRATION"
    PRIMARY = "PRIMARY"
    GENERAL_ELECTION = "GENERAL_ELECTION"
    COMPLETED = "COMPLETED"

class JourneyFSM:
    def __init__(self):
        self.state = JourneyState.NOT_STARTED

    def advance(self):
        if self.state == JourneyState.NOT_STARTED:
            self.state = JourneyState.REGISTRATION
        elif self.state == JourneyState.REGISTRATION:
            self.state = JourneyState.PRIMARY
        elif self.state == JourneyState.PRIMARY:
            self.state = JourneyState.GENERAL_ELECTION
        elif self.state == JourneyState.GENERAL_ELECTION:
            self.state = JourneyState.COMPLETED
        return self.state

    def get_state(self):
        return self.state

    def reset(self):
        self.state = JourneyState.NOT_STARTED
        return self.state

# In-memory store for demonstration purposes
global_journey = JourneyFSM()
