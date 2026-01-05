from typing import Any, Dict, Type, Optional

class Visitor:
    _dispatch_cache: Dict[Type, str] = {}

    def __init__(self):
        self.dispatch = self._get_dispatch_cache()

    @classmethod
    def _get_dispatch_cache(cls) -> Dict[Type, str]:
        # Ruby's Hash.new with default block. In Python we'll handle it in visit.
        return {}

    def accept(self, object: Any, collector: Any = None) -> Any:
        return self.visit(object, collector)

    def visit(self, object: Any, collector: Any = None) -> Any:
        klass = object.__class__
        method_name = self.dispatch.get(klass)

        if not method_name:
            # Ruby: visit_#{(klass.name || "").gsub("::", "_")}
            # We'll use module + class name
            module_name = klass.__module__.replace(".", "_")
            class_name = klass.__name__
            method_name = f"visit_{module_name}_{class_name}"
            self.dispatch[klass] = method_name

        method = getattr(self, method_name, None)

        if method:
            if collector is not None:
                return method(object, collector)
            else:
                return method(object)
        else:
            # Fallback to superclasses
            for base in klass.__mro__[1:]:
                base_method_name = self.dispatch.get(base)
                if not base_method_name:
                    base_module_name = base.__module__.replace(".", "_")
                    base_class_name = base.__name__
                    base_method_name = f"visit_{base_module_name}_{base_class_name}"

                if hasattr(self, base_method_name):
                    self.dispatch[klass] = base_method_name
                    method = getattr(self, base_method_name)
                    if collector is not None:
                        return method(object, collector)
                    else:
                        return method(object)

            from arel.errors import UnsupportedVisitError
            raise UnsupportedVisitError(object)

