#!/usr/bin/env python

from test_musescore_backup_module import test_batch_job_creator
from test_musescore_backup_module import test_musescore_hash_database

if __name__ == '__main__':
    test_batch_job_creator.test_batch_job()
    test_batch_job_creator.test_batch_job_hash()

    test_musescore_hash_database.test_musescore_hash_database()
