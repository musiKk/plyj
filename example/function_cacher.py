#!/usr/bin/env python2
#
# This small program will take any Java class and alter any number of its
# functions to cache their result for their given input.
#
# This was made to reduce the number of native calls required in a SWIG Java
# wrapper when you know the result of a function will never change.
#
# I.E, for some const array class that may look similar to this
#
# class ConstArray {
#     public String name() {
#         return SwigJNI.ConstArray_name(this);
#     }
#     public int count() {
#         return SwigJNI.ConstArray_count(this);
#     }
#     public Item get(int index) {
#         return SwigJNI.ConstArray_get(this, index);
#     }
# }
#
# Then we want this:
#
# class ConstArray {
#     private boolean isNameCached = false;
#     private String nameCached = null;
#     public String name() {
#         if (!isNameCached) {
#             nameCached = SwigJNI.ConstArray_name(this);
#             isNameCached = true;
#         }
#         return nameCached;
#     }
#     private Item[] array1 = null;
#     public int count() {
#         if (array1 == null) {
#             array1 = new Item[SwigJNI.ConstArray_count(this)];
#         }
#         return array1.length;
#     }
#     public Item get(int index) {
#         count()
#         if (array1[index] == null) {
#             array1[index] = SwigJNI.ConstArray_get(this, index);
#         }
#         return array1[index];
#     }
# }
#
# The input function_list_file looks like this:
#
# cache ConstArray name
# cache_array_no_nulls ConstArray count get
import os

import sys
from plyj.model.classes import ClassDeclaration, FieldDeclaration
from plyj.model.expression import Equality, FieldAccess, Assignment, \
    ArrayCreation, MethodInvocation, ArrayAccess, Cast, Unary
from plyj.model.literal import Literal
from plyj.model.method import MethodDeclaration
from plyj.model.modifier import BasicModifier
from plyj.model.name import Name
from plyj.model.statement import IfThenElse, Return, Block, ExpressionStatement
from plyj.model.variable import VariableDeclarator, Variable
from plyj.parser import Parser
import abc


def find_function_declaration(name, class_decl):
    for i, decl in enumerate(class_decl.body):
        if isinstance(decl, MethodDeclaration) and decl.name.value == name:
            return i, decl
    return None, None


class Instruction(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def run(self, fully_qualified_name, class_decl):
        pass


class CacheInstruction(Instruction):
    def __init__(self, fields):
        if len(fields) != 2:
            raise ValueError("cache instruction has 2 fields "
                             "(<class_name> <func_name>)")
        self.class_name = fields[0]
        self.func_name = fields[1]

    def run(self, fully_qualified_name, class_decl):
        if fully_qualified_name != self.class_name:
            return

        func_index, func_decl = find_function_declaration(self.func_name,
                                                          class_decl)

        if func_decl is None:
            raise ValueError("Could not locate function " + self.func_name +
                             " in class " + fully_qualified_name)

        if len(func_decl.type_parameters) != 0:
            raise ValueError("Type parameters not supported")

        if len(func_decl.parameters) != 0:
            raise ValueError("Parameters are not supported")

        is_cached_name = "is" + func_decl.name.value + "Cached"
        is_cached_decl = FieldDeclaration(
            "boolean",
            VariableDeclarator(Variable(is_cached_name), Literal("false")))

        cached_name = func_decl.name.value + "Cached"
        cached_decl = FieldDeclaration(
            func_decl.return_type,
            VariableDeclarator(Variable(cached_name)))

        class_decl.body.insert(func_index, cached_decl)
        class_decl.body.insert(func_index, is_cached_decl)

        func_decl_name = func_decl.name
        func_decl.name = Name(func_decl.name.value + "Uncached")
        BasicModifier.set_visibility(func_decl.modifiers, "private")

        # create count_decl again, it returns size of the array or if the array
        # is null it creates it with the size of count_decl_uncached
        func_decl_cached_body = [
            IfThenElse(
                Unary("!", Name(is_cached_name)),
                Block([
                    ExpressionStatement(Assignment(
                        "=",
                        Name(is_cached_name),
                        Literal("true")
                    )),
                    ExpressionStatement(Assignment(
                        "=",
                        Name(cached_name),
                        MethodInvocation(func_decl.name)
                    ))
                ])
            ),
            Return(Name(cached_name))
        ]
        func_decl_cached = MethodDeclaration(
            func_decl_name, ["public"],
            return_type=func_decl.return_type, body=func_decl_cached_body)
        class_decl.body.insert(func_index, func_decl_cached)


class CacheArrayNoNullsInstruction(Instruction):
    def __init__(self, fields):
        if len(fields) != 3:
            raise ValueError("cache instruction has 4 fields "
                             "(<class_name> <count_func_name> <get_func_name>)"
                             )

        self.class_name = fields[0]
        self.count_func_name = fields[1]
        self.get_func_name = fields[2]

    def run(self, fully_qualified_name, class_decl):
        if fully_qualified_name != self.class_name:
            return

        count_index, count_decl = find_function_declaration(
            self.count_func_name, class_decl)

        get_index, get_decl = find_function_declaration(
            self.get_func_name, class_decl)

        if count_decl is None or get_decl is None:
            raise ValueError("Could not locate count and get function in "
                             "class " + fully_qualified_name)

        if len(count_decl.type_parameters) != 0:
            raise ValueError("Type parameters not supported")

        if len(get_decl.type_parameters) != 0:
            raise ValueError("Type parameters not supported")

        if count_decl.return_type.name.value not in ["int", "long"]:
            raise ValueError("Count must return int or long.")

        if len(count_decl.parameters) != 0:
            raise ValueError("Parameters in count function are not supported")

        if len(get_decl.parameters) != 1:
            raise ValueError("Exactly 1 parameter allowed in get function.")

        if get_decl.parameters[0].type.name.value not in ["int", "long"]:
            raise ValueError("Get parameter muse be int or long.")

        get_decl_name = get_decl.name.value
        count_decl_name = count_decl.name.value

        # rename get_decl to a new private function
        BasicModifier.set_visibility(get_decl.modifiers, "private")
        get_decl.name = get_decl_name + "Uncached"

        # rename count_decl to a new private function
        BasicModifier.set_visibility(count_decl.modifiers, "private")
        count_decl.name = count_decl_name + "Uncached"

        # add a new array field called <self.array_name> of the return type of
        #     get_decl
        null = Literal("null")
        array_name = get_decl_name + count_decl_name + "Cache"
        earliest_index = min(count_index, get_index)
        declarator = VariableDeclarator(Variable(array_name, 1), null)
        array_decl = FieldDeclaration(get_decl.return_type,
                                      declarator, ["private"])
        array_decl_name = Name(array_name)
        class_decl.body.insert(earliest_index, array_decl)

        # create count_decl again, it returns size of the array or if the array
        # is null it creates it with the size of count_decl_uncached
        count_decl_cached_body = [
            IfThenElse(
                Equality("==", array_decl_name, null),
                ExpressionStatement(Assignment(
                    "=",
                    array_decl_name,
                    ArrayCreation(
                        get_decl.return_type,
                        [MethodInvocation(count_decl.name)]
                    )
                ))
            ),
            Return(FieldAccess("length", array_decl_name))
        ]
        count_decl_cached = MethodDeclaration(
            count_decl_name, ["public"], parameters=count_decl.parameters,
            return_type="int", body=count_decl_cached_body)
        class_decl.body.insert(count_index, count_decl_cached)

        # create get_decl again: it calls count_decl first (to ensure array
        # existance) and then checks if the array at the passed index is null
        # if it is null, it initializes it. Then it returns the value.
        get_param_name = get_decl.parameters[0].variable.name
        array_at_index = ArrayAccess(Cast("int", get_param_name),
                                     array_decl_name)
        get_decl_cached_body = [
            ExpressionStatement(MethodInvocation(count_decl_name)),
            IfThenElse(
                Equality("==", array_at_index, null),
                ExpressionStatement(Assignment(
                    "=",
                    array_at_index,
                    MethodInvocation(get_decl.name, [get_param_name])
                ))
            ),
            Return(array_at_index)
        ]
        get_decl_cached = MethodDeclaration(
            get_decl_name, ["public"], parameters=get_decl.parameters,
            return_type=get_decl.return_type, body=get_decl_cached_body)
        class_decl.body.insert(get_index, get_decl_cached)


class InstructionFile:
    @staticmethod
    def _make_instruction(x):
        fields = x.split(" ")
        if len(fields) == 0:
            return None
        if fields[0] == "cache":
            return CacheInstruction(fields[1:])
        elif fields[0] == "cache_array_no_nulls":
            return CacheArrayNoNullsInstruction(fields[1:])

    def __init__(self, data):
        self.instructions = []
        for line in data.split("\n"):
            new_instruction = self._make_instruction(line)
            if new_instruction is not None:
                self.instructions.append(new_instruction)

    def rewrite_class_decl(self, fully_qualified_name, class_decl):
        # First, let's recurse into all child class definitions
        for declaration in class_decl.body:
            if isinstance(declaration, ClassDeclaration):
                name = fully_qualified_name + "." + declaration.name.value
                self.rewrite_class_decl(name, declaration)

        # Now we run all our instructions on the class declaration
        for instruction in self.instructions:
            instruction.run(fully_qualified_name, class_decl)


def cache_file(input_filename, instruction_file, output_filename,
               tree_callback=None):
    """
    Takes the input filename (not a folder) and runs the instructions on it.
    :param tree_callback: A callback that accepts three arguments: the tree of
                          the input_file, the input filename and the output
                          filename. Use this to apply any modifications before
                          the file is written out. Note that by this point the
                          caching has been applied.
    """
    # Parse input file
    parser = Parser()
    tree = parser.parse_file(input_filename)

    # Run all instructions.
    package = ""
    if tree.package_declaration is not None:
        package = tree.package_declaration.name + "."
    for type_decl in tree.type_declarations:
        if isinstance(type_decl, ClassDeclaration):
            name = package + type_decl.name.value
            instruction_file.rewrite_class_decl(name, type_decl)

    if tree_callback is not None:
        tree_callback(tree, input_filename, output_filename)

    # Write tree to output.
    with open(output_filename, "w") as f:
        f.write(tree.serialize())


def main(input_filename, instruction_file_filename, output_filename,
         tree_callback=None):
    """
    :param tree_callback: See cache_file.
    """
    # Load instruction_file
    with open(instruction_file_filename) as f:
        instruction_file = InstructionFile(f.read())

    if os.path.isfile(input_filename):
        cache_file(input_filename, instruction_file, output_filename)
    else:
        if os.path.isfile(output_filename):
            raise ValueError("Output must be a directory if input is a "
                             "directory")
        if not os.path.exists(output_filename):
            os.mkdir(output_filename)
        for root, folders, files in os.walk(input_filename):
            rel_path = os.path.relpath(root, input_filename)
            for file_ in files:
                file_loc = os.path.join(rel_path, file_)
                out_path = os.path.join(output_filename, file_loc)
                out_path = os.path.abspath(out_path)
                in_path = os.path.join(root, file_)
                print("{} -> {}".format(in_path, out_path))
                cache_file(in_path, instruction_file, out_path, tree_callback)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("usage: function_cacher.py <input> <instruction_file> <output>")
        print("    input: Some Java source file or folder")
        print("    instruction_file: A file where each line is one of the")
        print("                      following commands:")
        print("        cache <fully_qualified_type> <function_name>")
        print("        cache_array_no_nulls <fully_qualified_type> "
              "<count_function> <get_function>")
        print("    output: Where to write the new Java source file.")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])
