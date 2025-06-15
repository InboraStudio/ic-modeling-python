"""Parameter Classes

Copyright 2023 Google LLC
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    https://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

This module provides classes to represent and manage different types of SystemVerilog
parameters including regular parameters and local parameters. Each parameter type 
maintains proper type information and values according to SystemVerilog specifications.
"""

from typing import Any, List
from imp.base.models import component
from imp.base.models.datatypes import DataType


class Parameter(component.Component):
    """Defines a SystemVerilog parameter with type information and default value. 

    This class represents a standard SystemVerilog parameter that can be overridden
    during module instantiation.

    Attributes:
        name: String identifier for the parameter in generated code.
        dtype: DataType representing the SystemVerilog data type.
        default: Optional default value for the parameter.
    """

    def __init__(self, name: str, dtype: DataType, default: Any | None = None):
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
        args = f"name={self.name!r}, dtype={self.dtype}, default={self.default!r}"
        return f"Parameter({args})"


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
        names_repr = ', '.join(repr(n) for n in self.names)
        return f"ParameterDeclaration(names=[{names_repr}], parameter={self.parameter})"


class LocalParam(component.Component):
    """Implements a SystemVerilog localparam with an immutable value.

    Local parameters serve as module-scoped constants that cannot be modified from
    outside the module where they are defined.

    Attributes:
        name: String identifier for the local parameter.
        dtype: DataType representing the SystemVerilog data type.
        value: Compile-time constant value for the parameter.
        comment: Optional string describing the parameter's purpose.
    """
    
    def __init__(self, name: str, dtype: DataType, value: Any, comment: str | None = None):
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
        args = f"name={self.name!r}, dtype={self.dtype}, value={self.value!r}"
        if self.comment is not None:
            args += f", comment={self.comment!r}"
        return f"LocalParam({args})"


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
        names_repr = ', '.join(repr(n) for n in self.names)
        return f"LocalParamDeclaration(names=[{names_repr}], localparam={self.localparam})"
