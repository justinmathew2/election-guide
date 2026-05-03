from enum import Enum

class JourneyState(str, Enum):
    """
    Enum representing the different states of the election journey.
    """
    NOT_STARTED = "NOT_STARTED"
    REGISTRATION = "REGISTRATION"
    PRIMARY = "PRIMARY"
    GENERAL_ELECTION = "GENERAL_ELECTION"
    COMPLETED = "COMPLETED"

class JourneyFSM:
    """
    Finite State Machine to track the progress of a voter's journey.
    """
    def __init__(self) -> None:
        self.state: JourneyState = JourneyState.NOT_STARTED

    def advance(self) -> JourneyState:
        """
        Advances the FSM to the next logical state.
        """
        if self.state == JourneyState.NOT_STARTED:
            self.state = JourneyState.REGISTRATION
        elif self.state == JourneyState.REGISTRATION:
            self.state = JourneyState.PRIMARY
        elif self.state == JourneyState.PRIMARY:
            self.state = JourneyState.GENERAL_ELECTION
        elif self.state == JourneyState.GENERAL_ELECTION:
            self.state = JourneyState.COMPLETED
        return self.state

    def get_state(self) -> JourneyState:
        """
        Returns the current state of the FSM.
        """
        return self.state

    def reset(self) -> JourneyState:
        """
        Resets the FSM back to the initial state.
        """
        self.state = JourneyState.NOT_STARTED
        return self.state

# In-memory store for demonstration purposes
global_journey = JourneyFSM()
