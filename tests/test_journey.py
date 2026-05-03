from backend.core.journey import JourneyFSM, JourneyState

def test_journey_fsm_initial_state():
    fsm = JourneyFSM()
    assert fsm.get_state() == JourneyState.NOT_STARTED

def test_journey_fsm_advance():
    fsm = JourneyFSM()
    
    assert fsm.advance() == JourneyState.REGISTRATION
    assert fsm.get_state() == JourneyState.REGISTRATION
    
    assert fsm.advance() == JourneyState.PRIMARY
    assert fsm.get_state() == JourneyState.PRIMARY
    
    assert fsm.advance() == JourneyState.GENERAL_ELECTION
    assert fsm.get_state() == JourneyState.GENERAL_ELECTION
    
    assert fsm.advance() == JourneyState.COMPLETED
    assert fsm.get_state() == JourneyState.COMPLETED
    
    # Should stay completed
    assert fsm.advance() == JourneyState.COMPLETED

def test_journey_fsm_reset():
    fsm = JourneyFSM()
    fsm.advance()
    fsm.advance()
    assert fsm.get_state() == JourneyState.PRIMARY
    
    fsm.reset()
    assert fsm.get_state() == JourneyState.NOT_STARTED
