"""Defines parameter classes for SystemVerilog model generation.

This module provides classes to represent and manage different types of SystemVerilog
parameters including regular parameters and local parameters. Each parameter type 
maintains proper type information and values according to SystemVerilog specifications.
"""

from typing import Any, List, Optional, Union
from imp.base.models import component


class Parameter(component.Component):
    """Defines a SystemVerilog parameter with type information and default value.

    This class represents a standard SystemVerilog parameter that can be overridden
    during module instantiation.

    Attributes:
        name: String identifier for the parameter in generated code.
        dtype: String representing the SystemVerilog data type.
        default: Optional default value for the parameter.
    """
    def __init__(self, name: str, dtype: str, default: Optional[Any] = None):
        super().__init__()
        if not name:
            raise ValueError("Parameter name cannot be empty")
        self.name = name
        self.dtype = dtype
        self.default = default

    @property
    def is_constant(self) -> bool:
        """Returns True as parameters are constant by definition."""
        return True

    def __str__(self) -> str:
        """Returns string representation of the parameter."""
        return f"Parameter({self.name}: {self.dtype} = {self.default})"


class ParameterDeclaration(component.Component):
    """Groups multiple parameters of the same type into a single declaration.

    Provides a more compact representation for parameters sharing identical type
    information in the generated SystemVerilog code, improving readability.

    Attributes:
        names: List of parameter names to be declared.
        parameter: Reference Parameter object containing shared type information.
    """
    
    def __init__(self, names: List[str], parameter: Parameter):
        super().__init__()
        if not names:
            raise ValueError("Names list cannot be empty")
        self.names = names
        self.parameter = parameter

    def __str__(self) -> str:
        """Returns string representation of the parameter declaration."""
        return f"ParameterDeclaration({', '.join(self.names)})"


class LocalParam(component.Component):
    """Implements a SystemVerilog localparam with an immutable value.

    Local parameters serve as module-scoped constants that cannot be modified from
    outside the module where they are defined.

    Attributes:
        name: String identifier for the local parameter.
        dtype: String representing the SystemVerilog data type.
        value: Compile-time constant value for the parameter.
        comment: Optional string describing the parameter's purpose.
    """
    def __init__(self, name: str, dtype: str, value: Any, comment: Optional[str] = None):
        super().__init__()
        if not name:
            raise ValueError("LocalParam name cannot be empty")
        self.name = name
        self.dtype = dtype
        self.value = value
        self.comment = comment

    @property
    def is_constant(self) -> bool:
        """Returns True as local parameters are constant by definition."""
        return True

    def __str__(self) -> str:
        """Returns string representation of the local parameter."""
        base = f"LocalParam({self.name}: {self.dtype} = {self.value})"
        return f"{base} // {self.comment}" if self.comment else base


class LocalParamDeclaration(component.Component):
    """Groups multiple local parameters into a single declaration.

    Enables efficient declaration of multiple local parameters that share common
    type and value definitions in the generated SystemVerilog code.

    Attributes:
        names: List of local parameter names to be declared.
        localparam: Reference LocalParam object containing shared information.
    """
    
    def __init__(self, names: List[str], localparam: LocalParam):
        super().__init__()
        if not names:
            raise ValueError("Names list cannot be empty")
        self.names = names
        self.localparam = localparam

    def __str__(self) -> str:
        """Returns string representation of the local parameter declaration."""
        return f"LocalParamDeclaration({', '.join(self.names)})"