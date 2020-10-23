# AUTOGENERATED BY EdgeDB WITH
#     $ edb gen-meta-grammars edgeql


from __future__ import annotations


class EdgeQL:
    reserved_keywords = (
        "__source__",
        "__std__",
        "__subject__",
        "__type__",
        "abort",
        "alter",
        "analyze",
        "and",
        "anyarray",
        "anytuple",
        "anytype",
        "begin",
        "case",
        "check",
        "commit",
        "configure",
        "create",
        "deallocate",
        "declare",
        "delete",
        "describe",
        "detached",
        "discard",
        "distinct",
        "do",
        "drop",
        "else",
        "empty",
        "end",
        "execute",
        "exists",
        "explain",
        "extending",
        "fetch",
        "filter",
        "for",
        "get",
        "global",
        "grant",
        "group",
        "if",
        "ilike",
        "import",
        "in",
        "insert",
        "introspect",
        "is",
        "like",
        "limit",
        "listen",
        "load",
        "lock",
        "match",
        "module",
        "move",
        "not",
        "notify",
        "offset",
        "optional",
        "or",
        "order",
        "over",
        "partition",
        "policy",
        "populate",
        "prepare",
        "raise",
        "refresh",
        "reindex",
        "release",
        "reset",
        "revoke",
        "rollback",
        "select",
        "set",
        "start",
        "typeof",
        "union",
        "update",
        "variadic",
        "when",
        "window",
        "with",
    )
    unreserved_keywords = (
        "abstract",
        "after",
        "alias",
        "all",
        "allow",
        "annotation",
        "as",
        "asc",
        "assignment",
        "before",
        "by",
        "cardinality",
        "cast",
        "config",
        "conflict",
        "constraint",
        "current",
        "database",
        "ddl",
        "default",
        "deferrable",
        "deferred",
        "delegated",
        "desc",
        "emit",
        "explicit",
        "expression",
        "final",
        "first",
        "from",
        "function",
        "implicit",
        "index",
        "infix",
        "inheritable",
        "into",
        "isolation",
        "json",
        "last",
        "link",
        "migration",
        "multi",
        "named",
        "object",
        "of",
        "oids",
        "on",
        "only",
        "onto",
        "operator",
        "overloaded",
        "owned",
        "postfix",
        "prefix",
        "property",
        "proposed",
        "pseudo",
        "read",
        "reject",
        "rename",
        "repeatable",
        "required",
        "restrict",
        "role",
        "roles",
        "savepoint",
        "scalar",
        "schema",
        "sdl",
        "serializable",
        "session",
        "single",
        "source",
        "superuser",
        "system",
        "target",
        "ternary",
        "text",
        "then",
        "to",
        "transaction",
        "type",
        "unless",
        "using",
        "verbose",
        "view",
        "write",
    )
    bool_literals = (
        "false",
        "true",
    )
    type_builtins = (
        "BaseObject",
        "Object",
        "anyenum",
        "anyfloat",
        "anyint",
        "anynumeric",
        "anyreal",
        "anyscalar",
        "array",
        "bigint",
        "bool",
        "bytes",
        "datetime",
        "decimal",
        "duration",
        "enum",
        "float32",
        "float64",
        "int16",
        "int32",
        "int64",
        "json",
        "local_date",
        "local_datetime",
        "local_time",
        "sequence",
        "str",
        "tuple",
        "uuid",
    )
    module_builtins = (
        "cal",
        "cfg",
        "math",
        "schema",
        "std",
        "stdgraphql",
        "sys",
    )
    constraint_builtins = (
        "constraint",
        "exclusive",
        "expression",
        "len_value",
        "max_ex_value",
        "max_len_value",
        "max_value",
        "min_ex_value",
        "min_len_value",
        "min_value",
        "one_of",
        "regexp",
    )
    fn_builtins = (
        "abs",
        "advisory_lock",
        "advisory_unlock",
        "advisory_unlock_all",
        "all",
        "any",
        "array_agg",
        "array_get",
        "array_join",
        "array_unpack",
        "bytes_get_bit",
        "ceil",
        "contains",
        "count",
        "date_get",
        "datetime_current",
        "datetime_get",
        "datetime_of_statement",
        "datetime_of_transaction",
        "datetime_truncate",
        "duration_to_seconds",
        "duration_truncate",
        "enumerate",
        "find",
        "floor",
        "get_current_database",
        "get_transaction_isolation",
        "get_version",
        "get_version_as_str",
        "json_array_unpack",
        "json_get",
        "json_object_unpack",
        "json_typeof",
        "len",
        "lg",
        "ln",
        "log",
        "max",
        "mean",
        "min",
        "random",
        "re_match",
        "re_match_all",
        "re_replace",
        "re_test",
        "round",
        "sleep",
        "stddev",
        "stddev_pop",
        "str_lower",
        "str_lpad",
        "str_ltrim",
        "str_pad_end",
        "str_pad_start",
        "str_repeat",
        "str_rpad",
        "str_rtrim",
        "str_split",
        "str_title",
        "str_trim",
        "str_trim_end",
        "str_trim_start",
        "str_upper",
        "sum",
        "time_get",
        "to_bigint",
        "to_datetime",
        "to_decimal",
        "to_duration",
        "to_float32",
        "to_float64",
        "to_int16",
        "to_int32",
        "to_int64",
        "to_json",
        "to_local_date",
        "to_local_datetime",
        "to_local_time",
        "to_str",
        "uuid_generate_v1mc",
        "var",
        "var_pop",
    )
    operators = (
        "!=",
        "%",
        "*",
        "+",
        "++",
        "-",
        "/",
        "//",
        ":=",
        "<",
        "<=",
        "=",
        ">",
        ">=",
        "?!=",
        "?=",
        "??",
        "^",
    )
    navigation = (
        ".<",
        ".>",
        "@",
        ".",
    )