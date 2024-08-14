import tkinter as tk
import uuid
from typing import Optional, TypeVar

import customtkinter as ctk

T = TypeVar("T")


class TypedVar[T](ctk.StringVar):
    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        *,
        value: Optional[T] = None,
        value_type: Optional[type[T]] = None,
        name: Optional[str] = None,
    ) -> None:
        """
        Construct a typed variable.

        Do not use for `str`, `int` and `bool`, use built-ins instead.

        MASTER can be given as master widget. VALUE is an optional value, but it
        has to be `set()` at least once before being read with `get()`. Otherwise
        an AttributeError will be raised. 

        NAME is an optional Tcl name (defaults to PY_VARnum).

        If NAME matches an existing variable and VALUE is omitted then the
        existing value is retained.
        """
        super().__init__(master, "InitAnyVar", name)
        if value is not None:
            self._value = value
        elif value_type is not None:
            self._value: value_type  # type: ignore
        else:
            raise ValueError("Either value or value type must not be None.")
        return None

    def get(self) -> T:
        """
        Return the typed variable.
        """
        _ = super().get()
        return self._value

    def set(self, value: T) -> None:
        """
        Set the variable to VALUE.
        """
        self._value = value
        super().set(str(uuid.uuid4()))
        return None


class State():
    """
    Nested state class for custom widgets.

    Children must never call `super().__init__()`. Instead, they should set
    "inherit" their parents state by setting each property of `vars()` again.
    """

    def __init__(self) -> None:
        self.widget_scaling = TypedVar(value_type=float)
        self.appearance_mode = ctk.StringVar()
        return None
