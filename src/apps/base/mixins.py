
class SerializeByActionMixin:
    def get_serializer_class(self):  # type: ignore
        try:
            return self.serialize_by_action[self.action]  # type: ignore
        except KeyError:
            return super().get_serializer_class()  # type: ignore
