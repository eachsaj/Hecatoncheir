#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import getopt
import os
import re
import sys

import DbProfilerRepository
import logger as log
from msgutil import gettext as _


def verify_column(col):
    assert 'validation' in col
    valid = 0
    invalid = 0
    for v in col['validation']:
        if v['invalid_count'] > 0:
            invalid += 1
        else:
            valid += 1
    return (valid, invalid)


def verify_table(tab):
    valid = 0
    invalid = 0
    for c in tab['columns']:
        v, i = verify_column(c)
        valid += v
        invalid += i
    return (valid, invalid)


class DbProfilerVerify():
    repofile = None

    def __init__(self, repofile, debug=False):
        self.repofile = repofile

        log.debug_enabled = debug

    def verify(self):
        repo = DbProfilerRepository.DbProfilerRepository(self.repofile)
        repo.open()

        log.info(_("Verifying the validation results."))

        table_list = repo.get_table_list()
        valid = 0
        invalid = 0
        for t in table_list:
            table = repo.get_table(t[0], t[1], t[2])
            v, i = verify_table(table)
            valid += v
            invalid += i

        if invalid == 0:
            log.info(_("No invalid results: %d/%d") % (invalid, valid+invalid))
        else:
            log.info(_("Invalid results: %d/%d") % (invalid, valid+invalid))

        repo.close()
        return (True if invalid > 0 else False)