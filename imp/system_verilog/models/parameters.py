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
"""

from typing import Any, List, Optional, Union
from imp.base.models import component


class Parameter(component.Component):
    """Parameters for SystemVerilog models.
    
    Attributes:
        name: Parameter name
        dtype: Parameter data type
        default: Default value for the parameter
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
    """Declaration of one or more parameters."""
    
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
    """Local parameters for SystemVerilog models.
    
    Attributes:
        name: LocalParam name
        dtype: LocalParam data type
        value: LocalParam value
        comment: Optional comment describing the local parameter
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
    """Declaration of one or more local parameters."""
    
    def __init__(self, names: List[str], localparam: LocalParam):
        super().__init__()
        if not names:
            raise ValueError("Names list cannot be empty")
        self.names = names
        self.localparam = localparam

    def __str__(self) -> str:
        """Returns string representation of the local parameter declaration."""
        return f"LocalParamDeclaration({', '.join(self.names)})"