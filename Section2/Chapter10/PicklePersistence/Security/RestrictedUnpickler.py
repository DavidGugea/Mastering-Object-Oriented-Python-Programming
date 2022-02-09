from typing import Any
import pickle
import builtins


class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, __module_name: str, __global_name: str) -> Any:
        if __module_name == "builtins":
            if __global_name not in ("exec", "vals"):
                return getattr(builtins, __global_name)
        elif __module_name == "__main__":
            # Valid module names depends on execution context
            return globals()["__main__"]