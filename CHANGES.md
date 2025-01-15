# Selected Cylc UI Server Changes

Internal changes that do not directly affect users may not be listed here.  For
all changes see the [closed
milestones](https://github.com/cylc/cylc-uiserver/milestones?state=closed) for
each release.

<!--
NOTE: Do not add entries here, use towncrier fragments instead:
$ towncrier create <PR-number>.<break|feat|fix>.md --content "Short description"
-->

<!-- towncrier release notes start -->

## cylc-uiserver-1.6.1 (Released 2025-01-15)

### 🚀 Enhancements

[#661](https://github.com/cylc/cylc-uiserver/pull/661) - The GUI can now be launched in standalone mode even if `[hub]url` is configured, using the `--new` option.

### 🔧 Fixes

[#660](https://github.com/cylc/cylc-uiserver/pull/660) - Fixed crash when starting the UI Server if a user has invalid groups in their profile.

## cylc-uiserver-1.6.0 (Released 2025-01-08)

[Updated cylc-ui to 2.7.0](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md)

### 🔧 Fixes

[#619](https://github.com/cylc/cylc-uiserver/pull/619) - Ensure that subprocesses created by Cylc UI Server are cleaned up correctly when the server shuts down.

[#645](https://github.com/cylc/cylc-uiserver/pull/645) - Add a default timeout for the `cylc cat-log` command which is used to provide access to log files in the cylc-ui.
  This timeout can be adjusted with the `log_timeout` option.

## cylc-uiserver-1.5.1 (Released 2024-10-15)

[Updated cylc-ui to 2.6.0](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md)

### 🔧 Fixes

[#607](https://github.com/cylc/cylc-uiserver/pull/607) - Log any errors when trying to list the workflow/job log files in the UI.

[#619](https://github.com/cylc/cylc-uiserver/pull/619) - Ensure that subprocesses created by Cylc UI Server are cleaned up correctly when the server shuts down.

## cylc-uiserver-1.5.0 (Released 2024-06-18)

[Updated cylc-ui to 2.5.0](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md)

### 🚀 Enhancements

[#507](https://github.com/cylc/cylc-uiserver/pull/507) - Added functionality for routing to a multiuser deployment when running cylc gui command.

[#548](https://github.com/cylc/cylc-uiserver/pull/548) - Improve the performance of the GraphQL server.

### 🔧 Fixes

[#592](https://github.com/cylc/cylc-uiserver/pull/592) - Compatibility with JupyterHub 4.1 XSRF changes for static requests

## cylc-uiserver-1.4.4 (Released 2024-04-05)

[Updated cylc-ui to 2.4.0](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md)

### 🔧 Fixes

[#558](https://github.com/cylc/cylc-uiserver/pull/558) - Permit Jupyter Lab to be run in the same Jupyter Server instance as the Cylc UI Server in standalone mode (i.e. via `cylc gui`), note it was already possible to do this in multi-user mode (i.e. via `cylc hub`).

[#570](https://github.com/cylc/cylc-uiserver/pull/570) - Fix an issue that could impose a low limit on the number of active workflows the server is able to track.

## cylc-uiserver-1.4.3 (Released 2023-12-05)

### 🔧 Fixes

[#533](https://github.com/cylc/cylc-uiserver/pull/533) - Fixed bug introduced in 1.4.2 where playing a workflow would fail if using a Cylc environment whose name does not match `cylc-8.X.Y` exactly.

## cylc-uiserver-1.4.2 (Released 2023-11-29)

[Updated cylc-ui to 2.3.0](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md)

### 🔧 Fixes

[#525](https://github.com/cylc/cylc-uiserver/pull/525) - Fix bugs when playing workflows using the form:
  - Specified Cylc version wasn't working
  - Could not play multiple workflows

## cylc-uiserver-1.4.1 (Released 2023-11-03)

[Updated cylc-ui to 2.2.0](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md)

## cylc-uiserver-1.4.0 (Released 2023-09-12)

### 🚀 Enhancements

[#450](https://github.com/cylc/cylc-uiserver/pull/450) - Upgraded to Jupyter Server 2.7+ and Jupyter Hub 4.0+. Note cylc-uiserver 1.3 remains supported and compatible with cylc-flow 8.2 for those not ready to make the jump just yet.


## cylc-uiserver-1.3.1 (Released 2023-09-08)

[Updated cylc-ui to 2.1.0](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md)

### 🔧 Fixes

[#379](https://github.com/cylc/cylc-uiserver/pull/379) - Fixed lack of info for errors recorded in logs.

[#455](https://github.com/cylc/cylc-uiserver/pull/455) - Added an upgrade toggle in cylc play dialog, and a specific warning for cases where workflow needs upgrade.

[#483](https://github.com/cylc/cylc-uiserver/pull/483) - Fixed bug in analysis view server-side query.


## cylc-uiserver-1.3.0 (Released 2023-07-21)

[Updated cylc-ui to 2.0.0](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md)

### Fixes

[#463](https://github.com/cylc/cylc-uiserver/pull/463) - Fixed failure to
connect to workflows when they were restarted.

## cylc-uiserver-1.2.2 (Released 2023-04-28)

[Updated cylc-ui to 1.6.0](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md)

### Enhancements

[#434](https://github.com/cylc/cylc-uiserver/pull/434) - Added the server side
code for the analysis view in the UI.

### Fixes

[#431](https://github.com/cylc/cylc-uiserver/pull/431) - Adds an additional
cleaning check for the UI server contact file. This may have caused problems
running a UI server following a crash.

## cylc-uiserver-1.2.1 (Released 2023-02-20)

[Updated cylc-ui to 1.5.0](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md)

### Enhancements

[#367](https://github.com/cylc/cylc-uiserver/pull/367) -
the log file now captures messages from cylc-flow.

[#370](https://github.com/cylc/cylc-uiserver/pull/370) -
`cylc gui workflow_id` is now supported and will open the GUI at that workflow.

## cylc-uiserver-1.2.0 (Released 2023-01-16)

[Updated cylc-ui to 1.4.0](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md)

### Enhancements

[#376](https://github.com/cylc/cylc-uiserver/pull/376) -
UIServer logs are now archived. The five most recent logs are retained (located
in `~/.cylc/uiserver/log/`). A new log is created with each UIServer instance.

### Fixes

[#386](https://github.com/cylc/cylc-uiserver/pull/386) - Work around bug in
JupyterHub 3.0.0 that prevents `cylc hub` from starting.

## cylc-uiserver-1.1.0 (Released 2022-07-28)

[Updated cylc-ui to 1.3.0](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md#cylc-ui-130-released-2022-07-27)

### Enhancements

[#349](https://github.com/cylc/cylc-uiserver/pull/349) -
Configure default logging. The UIServer log now goes to
`~/.cylc/uiserver/uiserver.log` at the `INFO` level by default. See the
Traitlets `logging_config` "trait" for more information.

[#323](https://github.com/cylc/cylc-uiserver/pull/323) -
`cylc clean` made available for runs and files within runs.

## cylc-uiserver-1.0.3 (Released 2022-05-31)

[Updated cylc-ui to 1.2.1](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md#cylc-ui-121-released-2022-05-30)

## cylc-uiserver-1.0.2 (Released 2022-05-20)

[Updated cylc-ui to 1.2.0](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md#cylc-ui-120-released-2022-05-19)

Internal changes, see https://github.com/cylc/cylc-uiserver/milestone/11?closed=1

## cylc-uiserver-1.0.1 (Released 2022-03-23)

[Updated cylc-ui to 1.1.0](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md#cylc-ui-110-released-2022-03-23)

### Fixes

[#324](https://github.com/cylc/cylc-uiserver/pull/324) -
Fix issues where workflow status could be incorrect.

## cylc-uiserver-1.0.0 (Released 2022-02-17)

[Updated cylc-ui to 1.0.0](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md#cylc-ui-100-released-2022-02-17)

### Enhancements

[#301](https://github.com/cylc/cylc-uiserver/pull/301) -
Version hierarchy added to jupyter_config.py files, to match cylc-flow. Config
files are now sourced from `.cylc/uiserver/<version>` rather than `.cylc/hub`.

[#297](https://github.com/cylc/cylc-uiserver/pull/297) -
Updated for the new Global Universal ID.

### Fixes

[#304](https://github.com/cylc/cylc-uiserver/pull/304) -
Suppressed client connection traceback.

## cylc-uiserver-0.6.0 (Released 2021-11-11)

Multi-user functionality implemented.

[Updated cylc-ui to 0.6.0](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md#cylc-ui-06-released-2021-11-10)

### Enhancements

[#204](https://github.com/cylc/cylc-uiserver/pull/**204**) -
Implementation of configurable multi user authorisation.

[#230](https://github.com/cylc/cylc-uiserver/pull/230) -
Convert the UI Server to a jupyter_server extension.

### Fixes

[#258](https://github.com/cylc/cylc-uiserver/pull/258) -
Fix traceback which could appear when workflows are removed.

[#241](https://github.com/cylc/cylc-uiserver/pull/241) -
Update old, broken hold options for playing workflows.

[#272](https://github.com/cylc/cylc-uiserver/pull/272) -
Allowed broken entries in the group id database to be
ignored and logged without causing total failure.

## cylc-uiserver-0.5.0 (Released 2021-07-28)

### Enhancements

[#214](https://github.com/cylc/cylc-uiserver/pull/214) -
Store the JupyterHub runtime files in ~/.cylc/hub.

## cylc-uiserver-0.4.0 (Released 2021-04-21)

### Enhancements

[#202](https://github.com/cylc/cylc-uiserver/pull/202) -
Add authorisation for multi-user setups.

[#197](https://github.com/cylc/cylc-uiserver/pull/197) -
Make the workflow scan interval configurable.

## cylc-uiserver-0.3.0 (2021-03-29)

Release 0.3.0 of Cylc UI Server.

### Backward incompatible changes

None or N/A.

### Enhancements

[#195](https://github.com/cylc/cylc-uiserver/pull/195) - UI: package 0.3.0

[#188](https://github.com/cylc/cylc-uiserver/pull/188) - UI: package
0.3 prebuild.

[#173](https://github.com/cylc/cylc-uiserver/pull/173) - CLI changes
`jupyterhub` -> `cylc hub`, `cylc-uiserver` -> `cylc uiserver`.

[#167](https://github.com/cylc/cylc-uiserver/pull/167) - Upgrade
JupyterHub to 1.3.x, and Tornado to 6.1.x. Set auto spawn timeout
to 1 second (effectively enabling it) in our demo configuration.

[#125](https://github.com/cylc/cylc-uiserver/pull/125) - Use Tornado
default WebSocket check_origin function.
[#124](https://github.com/cylc/cylc-uiserver/pull/124) - Add decorator
for websockets authentication.

[#151](https://github.com/cylc/cylc-uiserver/pull/151) - Prevent
`asyncio.gather` errors to be ignored, and allow execution to continue,
logging errors when found.

### Fixes

[#153](https://github.com/cylc/cylc-uiserver/pull/153) - Fix websocket
connections on webkit based browsers.

### Documentation

None.

### Security issues

None.

## cylc-uiserver-0.2 (2020-07-14)

Release 0.2 of Cylc UI Server.

### Backward incompatible changes

None or N/A.

### Enhancements

[#82](https://github.com/cylc/cylc-uiserver/pull/82) - Add subscriptions
support to GraphQL.

[#126](https://github.com/cylc/cylc-uiserver/pull/126) - Update JupyterHub
dependency to 1.1.*, and Graphene-Tornado to 2.6.*.

### Fixes

None.

### Documentation

None.

### Security issues

None.

## cylc-uiserver-0.1 (2019-09-18)

Initial release of Cylc UI Server.
