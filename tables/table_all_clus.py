# -*- coding: utf-8 -*-

from .table_utils import tabit


def taball(data, con_vars, cat_vars, clu_vars, outfile=None):
    """
    con_vars: list of vars
    cat_vars: list of vars
    clu_vars: list of clu vars
    outfile: path to file name, with xlsx extension
    """
    print("{:-^100}".format(" start tabulation "))
    startcol = 0
    flag = True
    for clu_col in clu_vars:
        startcol += tabit(
            data=data,
            con_vars=con_vars,
            cat_vars=cat_vars,
            clu_col=clu_col,
            outfile=outfile,
            startcol=startcol,
            incl_total=flag,
        )
        flag = False
    print("tabulation done successfully!")
