#!/usr/bin/env python2
from plyj.model import CompilationUnit, PackageDeclaration, ImportDeclaration


class CompilationUnitParser(object):
    @staticmethod
    def p_compilation_unit(p):
        """compilation_unit : package_declaration"""
        p[0] = CompilationUnit(package_declaration=p[1])

    @staticmethod
    def p_compilation_unit2(p):
        """compilation_unit : package_declaration import_declarations"""
        p[0] = CompilationUnit(package_declaration=p[1],
                               import_declarations=p[2])

    @staticmethod
    def p_compilation_unit3(p):
        """compilation_unit : \
               package_declaration import_declarations type_declarations"""

        p[0] = CompilationUnit(package_declaration=p[1],
                               import_declarations=p[2],
                               type_declarations=p[3])

    @staticmethod
    def p_compilation_unit4(p):
        """compilation_unit : package_declaration type_declarations"""
        p[0] = CompilationUnit(package_declaration=p[1],
                               type_declarations=p[2])

    @staticmethod
    def p_compilation_unit5(p):
        """compilation_unit : import_declarations"""
        p[0] = CompilationUnit(import_declarations=p[1])

    @staticmethod
    def p_compilation_unit6(p):
        """compilation_unit : type_declarations"""
        p[0] = CompilationUnit(type_declarations=p[1])

    @staticmethod
    def p_compilation_unit7(p):
        """compilation_unit : import_declarations type_declarations"""
        p[0] = CompilationUnit(import_declarations=p[1],
                               type_declarations=p[2])

    @staticmethod
    def p_compilation_unit8(p):
        """compilation_unit : empty"""
        p[0] = CompilationUnit()

    @staticmethod
    def p_package_declaration(p):
        """package_declaration : package_declaration_name ';' """
        if p[1][0]:
            p[0] = PackageDeclaration(p[1][1], modifiers=p[1][0])
        else:
            p[0] = PackageDeclaration(p[1][1])

    @staticmethod
    def p_package_declaration_name(p):
        """package_declaration_name : modifiers PACKAGE name
                                    | PACKAGE name"""
        if len(p) == 3:
            p[0] = (None, p[2])
        else:
            p[0] = (p[1], p[3])

    @staticmethod
    def p_import_declarations(p):
        """import_declarations : import_declaration
                               | import_declarations import_declaration"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    @staticmethod
    def p_import_declaration(p):
        """import_declaration : single_type_import_declaration
                              | type_import_on_demand_declaration
                              | single_static_import_declaration
                              | static_import_on_demand_declaration"""
        p[0] = p[1]

    @staticmethod
    def p_single_type_import_declaration(p):
        """single_type_import_declaration : IMPORT name ';' """
        p[0] = ImportDeclaration(p[2])

    @staticmethod
    def p_type_import_on_demand_declaration(p):
        """type_import_on_demand_declaration : IMPORT name '.' '*' ';' """
        p[0] = ImportDeclaration(p[2], on_demand=True)

    @staticmethod
    def p_single_static_import_declaration(p):
        """single_static_import_declaration : IMPORT STATIC name ';' """
        p[0] = ImportDeclaration(p[3], static=True)

    @staticmethod
    def p_static_import_on_demand_declaration(p):
        """static_import_on_demand_declaration \
               : IMPORT STATIC name '.' '*' ';' """

        p[0] = ImportDeclaration(p[3], static=True, on_demand=True)

    @staticmethod
    def p_type_declarations(p):
        """type_declarations : type_declaration
                             | type_declarations type_declaration"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]