from pymitter import EventEmitter as EE


# TODO revisit
class EventEmitter(EE):
    _event_instance = None
    def __new__(cls):
        if cls._event_instance is None:
            cls._event_instance = EE()
        return cls._event_instance


