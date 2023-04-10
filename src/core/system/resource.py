
from core.events import EventEmitter
from core.enums import EventType

event = EventEmitter()


class Resource:

  __instances = {}

  def __new__(cls, **kwargs):
      ins = object.__new__(cls)
      # hold up in memory?
      cls.__instances.update({ id(ins): ins })
      base_cls_name = cls.__bases__[0].__name__

      event.emit(
          EventType.RESOURCE_ATTACH.value, \
          resource_id=id(ins), \
          type=base_cls_name
      )

      return ins

  def __del__(self):
      event.emit(EventType.RESOURCE_DETACH.value, resource_id=id(self))

  # def load_config(self):
  #   """ Load configuration from collection """
  #     pass

  @staticmethod
  def get_instance(id):
      return Resource.__instances.get(id)

  @staticmethod
  def get_instances(ttype = None):
      if not ttype:
          return Resource.__instances.values()
      return [s for s in Resource.__instances.values() if s.trade_type == ttype]