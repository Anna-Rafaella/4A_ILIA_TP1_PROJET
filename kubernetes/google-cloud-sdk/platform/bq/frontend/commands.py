#!/usr/bin/env python
"""All the BigQuery CLI commands."""

import datetime
import sys
import time
import typing
from typing import Optional, TextIO

from absl import app
from absl import flags

import bq_flags
import bq_utils
from clients import client_job
from clients import utils as bq_client_utils
from frontend import bigquery_command
from frontend import bq_cached_client
from frontend import utils as frontend_utils
from frontend import utils_flags
from frontend import utils_formatting
from utils import bq_error
from utils import bq_id_utils
from utils import bq_processor_utils
from pyglib import stringutil

FLAGS = flags.FLAGS

# These aren't relevant for user-facing docstrings:
# pylint: disable=g-doc-return-or-yield
# pylint: disable=g-doc-args


class Partition(bigquery_command.BigqueryCmd):  # pylint: disable=missing-docstring
  usage = """partition source_prefix destination_table"""

  def __init__(self, name: str, fv: flags.FlagValues):
    super(Partition, self).__init__(name, fv)
    flags.DEFINE_boolean(
        'no_clobber',
        False,
        'Do not overwrite an existing partition.',
        short_name='n',
        flag_values=fv,
    )
    flags.DEFINE_string(
        'time_partitioning_type',
        'DAY',
        'Enables time based partitioning on the table and set the type. The '
        'default value is DAY, which will generate one partition per day. '
        'Other supported values are HOUR, MONTH, and YEAR.',
        flag_values=fv,
    )
    flags.DEFINE_integer(
        'time_partitioning_expiration',
        None,
        'Enables time based partitioning on the table and sets the number of '
        'seconds for which to keep the storage for the partitions in the table.'
        ' The storage in a partition will have an expiration time of its '
        'partition time plus this value.',
        flag_values=fv,
    )
    self._ProcessCommandRc(fv)

  def RunWithArgs(
      self, source_prefix: str, destination_table: str
  ) -> Optional[int]:
    """Copies source tables into partitioned tables.

    Usage:
    bq partition <source_table_prefix> <destination_partitioned_table>

    Copies tables of the format <source_table_prefix><time_unit_suffix> to a
    destination partitioned table, with the <time_unit_suffix> of the source
    tables becoming the partition ID of the destination table partitions. The
    suffix is <YYYYmmdd> by default, <YYYY> if the time_partitioning_type flag
    is set to YEAR, <YYYYmm> if set to MONTH, and <YYYYmmddHH> if set to HOUR.

    If the destination table does not exist, one will be created with
    a schema and that matches the last table that matches the supplied
    prefix.

    Examples:
      bq partition dataset1.sharded_ dataset2.partitioned_table
    """

    client = bq_cached_client.Client.Get()
    formatter = utils_flags.get_formatter_from_flags()

    source_table_prefix = bq_client_utils.GetReference(
        id_fallbacks=client, identifier=source_prefix
    )
    bq_id_utils.typecheck(
        source_table_prefix,
        bq_id_utils.ApiClientHelper.TableReference,
        'Cannot determine table associated with "%s"' % (source_prefix,),
        is_usage_error=True,
    )
    # TODO(b/333595633): Fix typecheck so the response is cast.
    source_table_prefix = typing.cast(
        bq_id_utils.ApiClientHelper.TableReference, source_table_prefix
    )
    destination_table = bq_client_utils.GetReference(
        id_fallbacks=client, identifier=destination_table
    )
    bq_id_utils.typecheck(
        destination_table,
        bq_id_utils.ApiClientHelper.TableReference,
        'Cannot determine table associated with "%s"' % (destination_table,),
        is_usage_error=True,
    )
    # TODO(b/333595633): Fix typecheck so the response is cast.
    destination_table = typing.cast(
        bq_id_utils.ApiClientHelper.TableReference, destination_table
    )

    source_dataset = source_table_prefix.GetDatasetReference()
    source_id_prefix = stringutil.ensure_str(source_table_prefix.tableId)
    source_id_len = len(source_id_prefix)

    job_id_prefix = utils_flags.get_job_id_from_flags()
    if isinstance(job_id_prefix, bq_client_utils.JobIdGenerator):
      job_id_prefix = job_id_prefix.Generate(
          [source_table_prefix, destination_table]
      )

    destination_dataset = destination_table.GetDatasetReference()

    utils_formatting.configure_formatter(
        formatter, bq_id_utils.ApiClientHelper.TableReference
    )
    results = map(
        utils_formatting.format_table_info,
        client.ListTables(source_dataset, max_results=1000 * 1000),
    )

    partition_ids = []
    representative_table = None

    time_format = '%Y%m%d'  # default to format for DAY
    if self.time_partitioning_type == 'HOUR':
      time_format = '%Y%m%d%H'
    elif self.time_partitioning_type == 'MONTH':
      time_format = '%Y%m'
    elif self.time_partitioning_type == 'YEAR':
      time_format = '%Y'

    for result in results:
      table_id = stringutil.ensure_str(result['tableId'])
      if table_id.startswith(source_id_prefix):
        suffix = table_id[source_id_len:]
        try:
          partition_id = datetime.datetime.strptime(suffix, time_format)
          partition_ids.append(partition_id.strftime(time_format))
          representative_table = result
        except ValueError:
          pass

    if not representative_table:
      print('No matching source tables found')
      return

    print(
        'Copying %d source partitions to %s'
        % (len(partition_ids), destination_table)
    )

    # Check to see if we need to create the destination table.
    if not client.TableExists(destination_table):
      source_table_id = representative_table['tableId']
      source_table_ref = source_dataset.GetTableReference(source_table_id)
      source_table_schema = client.GetTableSchema(source_table_ref)
      # Get fields in the schema.
      if source_table_schema:
        source_table_schema = source_table_schema['fields']

      time_partitioning = frontend_utils.ParseTimePartitioning(
          self.time_partitioning_type, self.time_partitioning_expiration
      )

      print(
          'Creating table: %s with schema from %s and partition spec %s'
          % (destination_table, source_table_ref, time_partitioning)
      )

      client.CreateTable(
          destination_table,
          schema=source_table_schema,
          time_partitioning=time_partitioning,
      )
      print('%s successfully created.' % (destination_table,))

    for partition_id in partition_ids:
      destination_table_id = '%s$%s' % (destination_table.tableId, partition_id)
      source_table_id = '%s%s' % (source_id_prefix, partition_id)
      current_job_id = '%s%s' % (job_id_prefix, partition_id)

      source_table = source_dataset.GetTableReference(source_table_id)
      destination_partition = destination_dataset.GetTableReference(
          destination_table_id
      )

      avoid_copy = False
      if self.no_clobber:
        maybe_destination_partition = client.TableExists(destination_partition)
        avoid_copy = (
            maybe_destination_partition
            and int(maybe_destination_partition['numBytes']) > 0
        )

      if avoid_copy:
        print("Table '%s' already exists, skipping" % (destination_partition,))
      else:
        print('Copying %s to %s' % (source_table, destination_partition))
        kwds = {
            'write_disposition': 'WRITE_TRUNCATE',
            'job_id': current_job_id,
        }
        if bq_flags.LOCATION.value:
          kwds['location'] = bq_flags.LOCATION.value
        job = client_job.CopyTable(
            client, [source_table], destination_partition, **kwds
        )
        if not bq_flags.SYNCHRONOUS_MODE.value:
          self.PrintJobStartInfo(job)
        else:
          print(
              'Successfully copied %s to %s'
              % (source_table, destination_partition)
          )




class Cancel(bigquery_command.BigqueryCmd):
  """Attempt to cancel the specified job if it is running."""

  usage = """cancel [--nosync] [<job_id>]"""

  def __init__(self, name: str, fv: flags.FlagValues):
    super(Cancel, self).__init__(name, fv)
    self._ProcessCommandRc(fv)

  def RunWithArgs(self, job_id: str = '') -> Optional[int]:
    # pylint: disable=g-doc-exception
    """Request a cancel and waits for the job to be cancelled.

    Requests a cancel and then either:
    a) waits until the job is done if the sync flag is set [default], or
    b) returns immediately if the sync flag is not set.
    Not all job types support a cancel, an error is returned if it cannot be
    cancelled. Even for jobs that support a cancel, success is not guaranteed,
    the job may have completed by the time the cancel request is noticed, or
    the job may be in a stage where it cannot be cancelled.

    Examples:
      bq cancel job_id  # Requests a cancel and waits until the job is done.
      bq --nosync cancel job_id  # Requests a cancel and returns immediately.

    Arguments:
      job_id: Job ID to cancel.
    """
    client = bq_cached_client.Client.Get()
    job_reference_dict = dict(
        bq_client_utils.GetJobReference(
            id_fallbacks=client,
            identifier=job_id,
            default_location=bq_flags.LOCATION.value,
        )
    )
    job = client_job.CancelJob(
        bqclient=client,
        job_id=job_reference_dict['jobId'],
        location=job_reference_dict['location'],
    )
    frontend_utils.PrintObjectInfo(
        job,
        bq_id_utils.ApiClientHelper.JobReference.Create(**job['jobReference']),
        custom_format='show',
    )
    status = job['status']
    if status['state'] == 'DONE':
      if (
          'errorResult' in status
          and 'reason' in status['errorResult']
          and status['errorResult']['reason'] == 'stopped'
      ):
        print('Job has been cancelled successfully.')
      else:
        print('Job completed before it could be cancelled.')
    else:
      print('Job cancel has been requested.')
    return 0


class Head(bigquery_command.BigqueryCmd):
  usage = """head [-n <max rows>] [-j] [-t] <identifier>"""

  def __init__(self, name: str, fv: flags.FlagValues):
    super(Head, self).__init__(name, fv)
    flags.DEFINE_boolean(
        'job',
        False,
        'Reads the results of a query job.',
        short_name='j',
        flag_values=fv,
    )
    flags.DEFINE_boolean(
        'table',
        False,
        'Reads rows from a table.',
        short_name='t',
        flag_values=fv,
    )
    flags.DEFINE_integer(
        'start_row',
        0,
        'The number of rows to skip before showing table data.',
        short_name='s',
        flag_values=fv,
    )
    flags.DEFINE_integer(
        'max_rows',
        100,
        'The number of rows to print when showing table data.',
        short_name='n',
        flag_values=fv,
    )
    flags.DEFINE_string(
        'selected_fields',
        None,
        'A subset of fields (including nested fields) to return when showing '
        'table data. If not specified, full row will be retrieved. '
        'For example, "-c:a,b".',
        short_name='c',
        flag_values=fv,
    )
    self._ProcessCommandRc(fv)

  def RunWithArgs(self, identifier: str = '') -> Optional[int]:
    # pylint: disable=g-doc-exception
    """Displays rows in a table.

    Examples:
      bq head dataset.table
      bq head -j job
      bq head -n 10 dataset.table
      bq head -s 5 -n 10 dataset.table
    """
    client = bq_cached_client.Client.Get()
    if self.j and self.t:
      raise app.UsageError('Cannot specify both -j and -t.')

    if self.j:
      reference = bq_client_utils.GetJobReference(
          id_fallbacks=client,
          identifier=identifier,
          default_location=bq_flags.LOCATION.value,
      )
    else:
      reference = bq_client_utils.GetTableReference(
          id_fallbacks=client, identifier=identifier
      )

    if isinstance(reference, bq_id_utils.ApiClientHelper.JobReference):
      fields, rows = client_job.ReadSchemaAndJobRows(
          client, dict(reference), start_row=self.s, max_rows=self.n
      )
    elif isinstance(reference, bq_id_utils.ApiClientHelper.TableReference):
      fields, rows = client.ReadSchemaAndRows(
          reference,
          start_row=self.s,
          max_rows=self.n,
          selected_fields=self.c,
      )
    else:
      raise app.UsageError("Invalid identifier '%s' for head." % (identifier,))

    bq_cached_client.Factory.ClientTablePrinter.GetTablePrinter().PrintTable(
        fields, rows
    )


class Insert(bigquery_command.BigqueryCmd):
  usage = """insert [-s] [-i] [-x=<suffix>] <table identifier> [file]"""

  def __init__(self, name: str, fv: flags.FlagValues):
    super(Insert, self).__init__(name, fv)
    flags.DEFINE_boolean(
        'skip_invalid_rows',
        None,
        'Attempt to insert any valid rows, even if invalid rows are present.',
        short_name='s',
        flag_values=fv,
    )
    flags.DEFINE_boolean(
        'ignore_unknown_values',
        None,
        'Ignore any values in a row that are not present in the schema.',
        short_name='i',
        flag_values=fv,
    )
    flags.DEFINE_string(
        'template_suffix',
        None,
        'If specified, treats the destination table as a base template, and '
        'inserts the rows into an instance table named '
        '"{destination}{templateSuffix}". BigQuery will manage creation of the '
        'instance table, using the schema of the base template table.',
        short_name='x',
        flag_values=fv,
    )
    flags.DEFINE_string(
        'insert_id',
        None,
        'Used to ensure repeat executions do not add unintended data. '
        'A present insert_id value will be appended to the row number of '
        'each row to be inserted and used as the insertId field for the row. '
        'Internally the insertId field is used for deduping of inserted rows.',
        flag_values=fv,
    )
    self._ProcessCommandRc(fv)

  def RunWithArgs(
      self, identifier: str = '', filename: Optional[str] = None
  ) -> Optional[int]:
    """Inserts rows in a table.

    Inserts the records formatted as newline delimited JSON from file
    into the specified table. If file is not specified, reads from stdin.
    If there were any insert errors it prints the errors to stdout.

    Examples:
      bq insert dataset.table /tmp/mydata.json
      echo '{"a":1, "b":2}' | bq insert dataset.table

    Template table examples:
    Insert to dataset.table_suffix table using dataset.table table as its
    template.
      bq insert -x=_suffix dataset.table /tmp/mydata.json
    """
    if filename:
      with open(filename, 'r') as json_file:
        return self._DoInsert(
            identifier,
            json_file,
            skip_invalid_rows=self.skip_invalid_rows,
            ignore_unknown_values=self.ignore_unknown_values,
            template_suffix=self.template_suffix,
            insert_id=self.insert_id,
        )
    else:
      return self._DoInsert(
          identifier,
          sys.stdin,
          skip_invalid_rows=self.skip_invalid_rows,
          ignore_unknown_values=self.ignore_unknown_values,
          template_suffix=self.template_suffix,
          insert_id=self.insert_id,
      )

  def _DoInsert(
      self,
      identifier: str,
      json_file: TextIO,
      skip_invalid_rows: Optional[bool] = None,
      ignore_unknown_values: Optional[bool] = None,
      template_suffix: Optional[int] = None,
      insert_id: Optional[str] = None,
  ) -> int:
    """Insert the contents of the file into a table."""
    client = bq_cached_client.Client.Get()
    reference = bq_client_utils.GetReference(
        id_fallbacks=client, identifier=identifier
    )
    bq_id_utils.typecheck(
        reference,
        (bq_id_utils.ApiClientHelper.TableReference,),
        'Must provide a table identifier for insert.',
        is_usage_error=True,
    )
    batch = []

    def Flush():
      result = client.InsertTableRows(
          reference,
          batch,
          skip_invalid_rows=skip_invalid_rows,
          ignore_unknown_values=ignore_unknown_values,
          template_suffix=template_suffix,
      )
      del batch[:]
      return result, result.get('insertErrors', None)

    result = {}
    errors = None
    lineno = 1
    for line in json_file:
      try:
        unique_insert_id = None
        if insert_id is not None:
          unique_insert_id = insert_id + '_' + str(lineno)
        batch.append(
            bq_processor_utils.JsonToInsertEntry(unique_insert_id, line)
        )
        lineno += 1
      except bq_error.BigqueryClientError as e:
        raise app.UsageError('Line %d: %s' % (lineno, str(e)))
      if (
          FLAGS.max_rows_per_request
          and len(batch) == FLAGS.max_rows_per_request
      ):
        result, errors = Flush()
      if errors:
        break
    if batch and not errors:
      result, errors = Flush()

    if bq_flags.FORMAT.value in ['prettyjson', 'json']:
      bq_utils.PrintFormattedJsonObject(result)
    elif bq_flags.FORMAT.value in [None, 'sparse', 'pretty']:
      if errors:
        for entry in result['insertErrors']:
          entry_errors = entry['errors']
          sys.stdout.write('record %d errors: ' % (entry['index'],))
          for error in entry_errors:
            print(
                '\t%s: %s'
                % (
                    stringutil.ensure_str(error['reason']),
                    stringutil.ensure_str(error.get('message')),
                )
            )
    return 1 if errors else 0


class Wait(bigquery_command.BigqueryCmd):  # pylint: disable=missing-docstring
  usage = """wait [<job_id>] [<secs>]"""

  def __init__(self, name: str, fv: flags.FlagValues):
    super(Wait, self).__init__(name, fv)
    flags.DEFINE_boolean(
        'fail_on_error',
        True,
        'When done waiting for the job, exit the process with an error '
        'if the job is still running, or ended with a failure.',
        flag_values=fv,
    )
    flags.DEFINE_string(
        'wait_for_status',
        'DONE',
        'Wait for the job to have a certain status. Default is DONE.',
        flag_values=fv,
    )
    self._ProcessCommandRc(fv)

  def RunWithArgs(self, job_id='', secs=sys.maxsize) -> Optional[int]:
    # pylint: disable=g-doc-exception
    """Wait some number of seconds for a job to finish.

    Poll job_id until either (1) the job is DONE or (2) the
    specified number of seconds have elapsed. Waits forever
    if unspecified. If no job_id is specified, and there is
    only one running job, we poll that job.

    Examples:
      bq wait # Waits forever for the currently running job.
      bq wait job_id  # Waits forever
      bq wait job_id 100  # Waits 100 seconds
      bq wait job_id 0  # Polls if a job is done, then returns immediately.
      # These may exit with a non-zero status code to indicate "failure":
      bq wait --fail_on_error job_id  # Succeeds if job succeeds.
      bq wait --fail_on_error job_id 100  # Succeeds if job succeeds in 100 sec.

    Arguments:
      job_id: Job ID to wait on.
      secs: Number of seconds to wait (must be >= 0).
    """
    try:
      secs = bq_client_utils.NormalizeWait(secs)
    except ValueError:
      raise app.UsageError('Invalid wait time: %s' % (secs,))

    client = bq_cached_client.Client.Get()
    if not job_id:
      running_jobs = client_job.ListJobRefs(
          bqclient=client, state_filter=['PENDING', 'RUNNING']
      )
      if len(running_jobs) != 1:
        raise bq_error.BigqueryError(
            'No job_id provided, found %d running jobs' % (len(running_jobs),)
        )
      job_reference = running_jobs.pop()
    else:
      job_reference = bq_client_utils.GetJobReference(
          id_fallbacks=client,
          identifier=job_id,
          default_location=bq_flags.LOCATION.value,
      )
    try:
      job = client_job.WaitJob(
          bqclient=client,
          job_reference=job_reference,
          wait=secs,
          status=self.wait_for_status,
      )
      frontend_utils.PrintObjectInfo(
          job,
          bq_id_utils.ApiClientHelper.JobReference.Create(
              **job['jobReference']
          ),
          custom_format='show',
      )
      return 1 if self.fail_on_error and bq_client_utils.IsFailedJob(job) else 0
    except StopIteration as e:
      print()
      print(e)
    # If we reach this point, we have not seen the job succeed.
    return 1 if self.fail_on_error else 0


class Version(bigquery_command.BigqueryCmd):
  usage = """version"""

  def _NeedsInit(self) -> bool:
    """If just printing the version, don't run `init` first."""
    return False

  def RunWithArgs(self) -> Optional[int]:
    """Return the version of bq."""
    print('This is BigQuery CLI %s' % (bq_utils.VERSION_NUMBER,))
