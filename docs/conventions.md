# ASTx Code Styling and Conventions

This document outlines the coding standards and conventions for the ASTx
project. Following these guidelines ensures consistency, readability, and
maintainability across the codebase.

## General Guidelines

- **Type Safety:** Always use the `@typechecked` decorator on all new ASTx
  classes to enforce runtime type checks. Additionally, do not reuse a variable
  for different types within the same context.

- **Reference Existing Syntax:** When implementing an ASTx class that
  corresponds to a Python syntax construct, refer to Python’s AST (e.g., using
  `ast.dump(ast.parse("class MyClass:\n attr1: int = 1"))`) to validate that all
  necessary attributes and subnodes are correctly implemented.

- **Avoid Excessive Nesting:** Follow the "never nesting" approach to reduce
  code complexity. Review resources such as
  [Never Nester – Why You Shouldn’t Nest Your Code](https://buildfactory.dk/never-nester-why-you-shouldnt-nest-your-code/)
  and
  [How and Why to Avoid Excessive Nesting](https://www.codeproject.com/Articles/626403/How-and-Why-to-Avoid-Excessive-Nesting).

## **str** Method Conventions

- **Class Name:** The `__str__` method of an ASTx node should return the name of
  the class in CapitalizedCamelCase.

- **Attributes Representation:**
  - If a node has one attribute (that is not another ASTx node), display it in
    square brackets immediately after the class name. _Example:_
    `LiteralInt32[1]`
  - If a node has multiple non-ASTx attributes, list them with the attribute
    name(s) and value(s) separated by commas. _Example:_
    `LiteralComplex32[real=1, imag=1]`
  - For boolean attributes, you may:
    - Include the attribute name if its value is `True` (e.g.,
      `Class[abstract]`), omitting it if `False`.
    - Alternatively, differentiate using distinct names (e.g., `Class[static]`
      vs. `Class[non-static]`), as appropriate for the specific node.

## get_struct Method Conventions

- **Naming Consistency:** The key in the `get_struct` output should match the
  string returned by the node’s `__str__` method. When the `simplified` flag is
  `True`, append `#{id(self)}` to the name to prevent grouping in ASCII
  representations.

- **Sub-node Keys:** Each sub-node in the structure should be represented with a
  key in lowercase using hyphen separators. _Example:_
  ```python
  {
      "except": except_.get_struct(simplified),
      "finally-handler": finally_handler.get_struct(simplified)
  }
  ```
