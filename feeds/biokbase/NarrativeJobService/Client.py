# -*- coding: utf-8 -*-
############################################################
#
# Autogenerated by the KBase type compiler -
# any changes made here will be overwritten
#
############################################################

from __future__ import print_function
# the following is a hack to get the baseclient to import whether we're in a
# package or not. This makes pep8 unhappy hence the annotations.
try:
    # baseclient and this client are in a package
    from .baseclient import BaseClient as _BaseClient  # @UnusedImport
except:
    # no they aren't
    from baseclient import BaseClient as _BaseClient  # @Reimport


class NarrativeJobService(object):

    def __init__(
            self, url=None, timeout=30 * 60, user_id=None,
            password=None, token=None, ignore_authrc=False,
            trust_all_ssl_certificates=False,
            auth_svc='https://kbase.us/services/authorization/Sessions/Login'):
        if url is None:
            url = 'https://kbase.us/services/njs_wrapper/'
        self._service_ver = None
        self._client = _BaseClient(
            url, timeout=timeout, user_id=user_id, password=password,
            token=token, ignore_authrc=ignore_authrc,
            trust_all_ssl_certificates=trust_all_ssl_certificates,
            auth_svc=auth_svc)

    def list_config(self, context=None):
        """
        :returns: instance of mapping from String to String
        """
        return self._client.call_method(
            'NarrativeJobService.list_config',
            [], self._service_ver, context)

    def ver(self, context=None):
        """
        Returns the current running version of the NarrativeJobService.
        :returns: instance of String
        """
        return self._client.call_method(
            'NarrativeJobService.ver',
            [], self._service_ver, context)

    def status(self, context=None):
        """
        Simply check the status of this service to see queue details
        :returns: instance of type "Status" -> structure: parameter
           "reboot_mode" of type "boolean" (@range [0,1]), parameter
           "stopping_mode" of type "boolean" (@range [0,1]), parameter
           "running_tasks_total" of Long, parameter "running_tasks_per_user"
           of mapping from String to Long, parameter "tasks_in_queue" of
           Long, parameter "config" of mapping from String to String,
           parameter "git_commit" of String
        """
        return self._client.call_method(
            'NarrativeJobService.status',
            [], self._service_ver, context)

    def run_job(self, params, context=None):
        """
        Start a new job (long running method of service registered in ServiceRegistery).
        Such job runs Docker image for this service in script mode.
        :param params: instance of type "RunJobParams" (method - service
           defined in standard JSON RPC way, typically it's module name from
           spec-file followed by '.' and name of funcdef from spec-file
           corresponding to running method (e.g.
           'KBaseTrees.construct_species_tree' from trees service); params -
           the parameters of the method that performed this call; Optional
           parameters: service_ver - specific version of deployed service,
           last version is used if this parameter is not defined rpc_context
           - context of current method call including nested call history
           remote_url - run remote service call instead of local command line
           execution. source_ws_objects - denotes the workspace objects that
           will serve as a source of data when running the SDK method. These
           references will be added to the autogenerated provenance. app_id -
           the id of the Narrative application running this job (e.g.
           repo/name) mapping<string, string> meta - user defined metadata to
           associate with the job. This data is passed to the User and Job
           State (UJS) service. wsid - a workspace id to associate with the
           job. This is passed to the UJS service, which will share the job
           based on the permissions of the workspace rather than UJS ACLs.)
           -> structure: parameter "method" of String, parameter "params" of
           list of unspecified object, parameter "service_ver" of String,
           parameter "rpc_context" of type "RpcContext" (call_stack -
           upstream calls details including nested service calls and parent
           jobs where calls are listed in order from outer to inner.) ->
           structure: parameter "call_stack" of list of type "MethodCall"
           (time - the time the call was started; method - service defined in
           standard JSON RPC way, typically it's module name from spec-file
           followed by '.' and name of funcdef from spec-file corresponding
           to running method (e.g. 'KBaseTrees.construct_species_tree' from
           trees service); job_id - job id if method is asynchronous
           (optional field).) -> structure: parameter "time" of type
           "timestamp" (A time in the format YYYY-MM-DDThh:mm:ssZ, where Z is
           either the character Z (representing the UTC timezone) or the
           difference in time to UTC in the format +/-HHMM, eg:
           2012-12-17T23:24:06-0500 (EST time) 2013-04-03T08:56:32+0000 (UTC
           time) 2013-04-03T08:56:32Z (UTC time)), parameter "method" of
           String, parameter "job_id" of type "job_id" (A job id.), parameter
           "run_id" of String, parameter "remote_url" of String, parameter
           "source_ws_objects" of list of type "wsref" (A workspace object
           reference of the form X/Y/Z, where X is the workspace name or id,
           Y is the object name or id, Z is the version, which is optional.),
           parameter "app_id" of String, parameter "meta" of mapping from
           String to String, parameter "wsid" of Long
        :returns: instance of type "job_id" (A job id.)
        """
        return self._client.call_method(
            'NarrativeJobService.run_job',
            [params], self._service_ver, context)

    def get_job_params(self, job_id, context=None):
        """
        Get job params necessary for job execution
        :param job_id: instance of type "job_id" (A job id.)
        :returns: multiple set - (1) parameter "params" of type
           "RunJobParams" (method - service defined in standard JSON RPC way,
           typically it's module name from spec-file followed by '.' and name
           of funcdef from spec-file corresponding to running method (e.g.
           'KBaseTrees.construct_species_tree' from trees service); params -
           the parameters of the method that performed this call; Optional
           parameters: service_ver - specific version of deployed service,
           last version is used if this parameter is not defined rpc_context
           - context of current method call including nested call history
           remote_url - run remote service call instead of local command line
           execution. source_ws_objects - denotes the workspace objects that
           will serve as a source of data when running the SDK method. These
           references will be added to the autogenerated provenance. app_id -
           the id of the Narrative application running this job (e.g.
           repo/name) mapping<string, string> meta - user defined metadata to
           associate with the job. This data is passed to the User and Job
           State (UJS) service. wsid - a workspace id to associate with the
           job. This is passed to the UJS service, which will share the job
           based on the permissions of the workspace rather than UJS ACLs.)
           -> structure: parameter "method" of String, parameter "params" of
           list of unspecified object, parameter "service_ver" of String,
           parameter "rpc_context" of type "RpcContext" (call_stack -
           upstream calls details including nested service calls and parent
           jobs where calls are listed in order from outer to inner.) ->
           structure: parameter "call_stack" of list of type "MethodCall"
           (time - the time the call was started; method - service defined in
           standard JSON RPC way, typically it's module name from spec-file
           followed by '.' and name of funcdef from spec-file corresponding
           to running method (e.g. 'KBaseTrees.construct_species_tree' from
           trees service); job_id - job id if method is asynchronous
           (optional field).) -> structure: parameter "time" of type
           "timestamp" (A time in the format YYYY-MM-DDThh:mm:ssZ, where Z is
           either the character Z (representing the UTC timezone) or the
           difference in time to UTC in the format +/-HHMM, eg:
           2012-12-17T23:24:06-0500 (EST time) 2013-04-03T08:56:32+0000 (UTC
           time) 2013-04-03T08:56:32Z (UTC time)), parameter "method" of
           String, parameter "job_id" of type "job_id" (A job id.), parameter
           "run_id" of String, parameter "remote_url" of String, parameter
           "source_ws_objects" of list of type "wsref" (A workspace object
           reference of the form X/Y/Z, where X is the workspace name or id,
           Y is the object name or id, Z is the version, which is optional.),
           parameter "app_id" of String, parameter "meta" of mapping from
           String to String, parameter "wsid" of Long, (2) parameter "config"
           of mapping from String to String
        """
        return self._client.call_method(
            'NarrativeJobService.get_job_params',
            [job_id], self._service_ver, context)

    def update_job(self, params, context=None):
        """
        :param params: instance of type "UpdateJobParams" (is_started -
           optional flag marking job as started (and triggering
           exec_start_time statistics to be stored).) -> structure: parameter
           "job_id" of type "job_id" (A job id.), parameter "is_started" of
           type "boolean" (@range [0,1])
        :returns: instance of type "UpdateJobResults" -> structure: parameter
           "messages" of list of String
        """
        return self._client.call_method(
            'NarrativeJobService.update_job',
            [params], self._service_ver, context)

    def add_job_logs(self, job_id, lines, context=None):
        """
        :param job_id: instance of type "job_id" (A job id.)
        :param lines: instance of list of type "LogLine" -> structure:
           parameter "line" of String, parameter "is_error" of type "boolean"
           (@range [0,1])
        :returns: instance of Long
        """
        return self._client.call_method(
            'NarrativeJobService.add_job_logs',
            [job_id, lines], self._service_ver, context)

    def get_job_logs(self, params, context=None):
        """
        :param params: instance of type "GetJobLogsParams" (skip_lines -
           optional parameter, number of lines to skip (in case they were
           already loaded before).) -> structure: parameter "job_id" of type
           "job_id" (A job id.), parameter "skip_lines" of Long
        :returns: instance of type "GetJobLogsResults" (last_line_number -
           common number of lines (including those in skip_lines parameter),
           this number can be used as next skip_lines value to skip already
           loaded lines next time.) -> structure: parameter "lines" of list
           of type "LogLine" -> structure: parameter "line" of String,
           parameter "is_error" of type "boolean" (@range [0,1]), parameter
           "last_line_number" of Long
        """
        return self._client.call_method(
            'NarrativeJobService.get_job_logs',
            [params], self._service_ver, context)

    def finish_job(self, job_id, params, context=None):
        """
        Register results of already started job
        :param job_id: instance of type "job_id" (A job id.)
        :param params: instance of type "FinishJobParams" (Either 'result',
           'error' or 'is_canceled' field should be defined; result - keeps
           exact copy of what original server method puts in result block of
           JSON RPC response; error - keeps exact copy of what original
           server method puts in error block of JSON RPC response;
           is_cancelled - Deprecated (field is kept for backward
           compatibility), please use 'is_canceled' instead.) -> structure:
           parameter "result" of unspecified object, parameter "error" of
           type "JsonRpcError" (Error block of JSON RPC response) ->
           structure: parameter "name" of String, parameter "code" of Long,
           parameter "message" of String, parameter "error" of String,
           parameter "is_cancelled" of type "boolean" (@range [0,1]),
           parameter "is_canceled" of type "boolean" (@range [0,1])
        """
        return self._client.call_method(
            'NarrativeJobService.finish_job',
            [job_id, params], self._service_ver, context)

    def check_job(self, job_id, context=None):
        """
        Check if a job is finished and get results/error
        :param job_id: instance of type "job_id" (A job id.)
        :returns: instance of type "JobState" (job_id - id of job running
           method finished - indicates whether job is done (including
           error/cancel cases) or not, if the value is true then either of
           'returned_data' or 'detailed_error' should be defined; ujs_url -
           url of UserAndJobState service used by job service status - tuple
           returned by UserAndJobState.get_job_status method result - keeps
           exact copy of what original server method puts in result block of
           JSON RPC response; error - keeps exact copy of what original
           server method puts in error block of JSON RPC response; job_state
           - 'queued', 'in-progress', 'completed', or 'suspend'; position -
           position of the job in execution waiting queue; creation_time,
           exec_start_time and finish_time - time moments of submission,
           execution start and finish events in milliseconds since Unix
           Epoch, cancelled - Deprecated field, please use 'canceled' field
           instead.) -> structure: parameter "job_id" of String, parameter
           "finished" of type "boolean" (@range [0,1]), parameter "ujs_url"
           of String, parameter "status" of unspecified object, parameter
           "result" of unspecified object, parameter "error" of type
           "JsonRpcError" (Error block of JSON RPC response) -> structure:
           parameter "name" of String, parameter "code" of Long, parameter
           "message" of String, parameter "error" of String, parameter
           "job_state" of String, parameter "position" of Long, parameter
           "creation_time" of Long, parameter "exec_start_time" of Long,
           parameter "finish_time" of Long, parameter "cancelled" of type
           "boolean" (@range [0,1]), parameter "canceled" of type "boolean"
           (@range [0,1])
        """
        return self._client.call_method(
            'NarrativeJobService.check_job',
            [job_id], self._service_ver, context)

    def check_jobs(self, params, context=None):
        """
        :param params: instance of type "CheckJobsParams" -> structure:
           parameter "job_ids" of list of type "job_id" (A job id.),
           parameter "with_job_params" of type "boolean" (@range [0,1])
        :returns: instance of type "CheckJobsResults" -> structure: parameter
           "job_states" of mapping from type "job_id" (A job id.) to type
           "JobState" (job_id - id of job running method finished - indicates
           whether job is done (including error/cancel cases) or not, if the
           value is true then either of 'returned_data' or 'detailed_error'
           should be defined; ujs_url - url of UserAndJobState service used
           by job service status - tuple returned by
           UserAndJobState.get_job_status method result - keeps exact copy of
           what original server method puts in result block of JSON RPC
           response; error - keeps exact copy of what original server method
           puts in error block of JSON RPC response; job_state - 'queued',
           'in-progress', 'completed', or 'suspend'; position - position of
           the job in execution waiting queue; creation_time, exec_start_time
           and finish_time - time moments of submission, execution start and
           finish events in milliseconds since Unix Epoch, cancelled -
           Deprecated field, please use 'canceled' field instead.) ->
           structure: parameter "job_id" of String, parameter "finished" of
           type "boolean" (@range [0,1]), parameter "ujs_url" of String,
           parameter "status" of unspecified object, parameter "result" of
           unspecified object, parameter "error" of type "JsonRpcError"
           (Error block of JSON RPC response) -> structure: parameter "name"
           of String, parameter "code" of Long, parameter "message" of
           String, parameter "error" of String, parameter "job_state" of
           String, parameter "position" of Long, parameter "creation_time" of
           Long, parameter "exec_start_time" of Long, parameter "finish_time"
           of Long, parameter "cancelled" of type "boolean" (@range [0,1]),
           parameter "canceled" of type "boolean" (@range [0,1]), parameter
           "job_params" of mapping from type "job_id" (A job id.) to type
           "RunJobParams" (method - service defined in standard JSON RPC way,
           typically it's module name from spec-file followed by '.' and name
           of funcdef from spec-file corresponding to running method (e.g.
           'KBaseTrees.construct_species_tree' from trees service); params -
           the parameters of the method that performed this call; Optional
           parameters: service_ver - specific version of deployed service,
           last version is used if this parameter is not defined rpc_context
           - context of current method call including nested call history
           remote_url - run remote service call instead of local command line
           execution. source_ws_objects - denotes the workspace objects that
           will serve as a source of data when running the SDK method. These
           references will be added to the autogenerated provenance. app_id -
           the id of the Narrative application running this job (e.g.
           repo/name) mapping<string, string> meta - user defined metadata to
           associate with the job. This data is passed to the User and Job
           State (UJS) service. wsid - a workspace id to associate with the
           job. This is passed to the UJS service, which will share the job
           based on the permissions of the workspace rather than UJS ACLs.)
           -> structure: parameter "method" of String, parameter "params" of
           list of unspecified object, parameter "service_ver" of String,
           parameter "rpc_context" of type "RpcContext" (call_stack -
           upstream calls details including nested service calls and parent
           jobs where calls are listed in order from outer to inner.) ->
           structure: parameter "call_stack" of list of type "MethodCall"
           (time - the time the call was started; method - service defined in
           standard JSON RPC way, typically it's module name from spec-file
           followed by '.' and name of funcdef from spec-file corresponding
           to running method (e.g. 'KBaseTrees.construct_species_tree' from
           trees service); job_id - job id if method is asynchronous
           (optional field).) -> structure: parameter "time" of type
           "timestamp" (A time in the format YYYY-MM-DDThh:mm:ssZ, where Z is
           either the character Z (representing the UTC timezone) or the
           difference in time to UTC in the format +/-HHMM, eg:
           2012-12-17T23:24:06-0500 (EST time) 2013-04-03T08:56:32+0000 (UTC
           time) 2013-04-03T08:56:32Z (UTC time)), parameter "method" of
           String, parameter "job_id" of type "job_id" (A job id.), parameter
           "run_id" of String, parameter "remote_url" of String, parameter
           "source_ws_objects" of list of type "wsref" (A workspace object
           reference of the form X/Y/Z, where X is the workspace name or id,
           Y is the object name or id, Z is the version, which is optional.),
           parameter "app_id" of String, parameter "meta" of mapping from
           String to String, parameter "wsid" of Long
        """
        return self._client.call_method(
            'NarrativeJobService.check_jobs',
            [params], self._service_ver, context)

    def cancel_job(self, params, context=None):
        """
        :param params: instance of type "CancelJobParams" -> structure:
           parameter "job_id" of type "job_id" (A job id.)
        """
        return self._client.call_method(
            'NarrativeJobService.cancel_job',
            [params], self._service_ver, context)
