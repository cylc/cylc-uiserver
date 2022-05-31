# Selected Cylc UI Server Changes

Internal changes that do not directly affect users may not be listed here.  For
all changes see the [closed
milestones](https://github.com/cylc/cylc-uiserver/milestones?state=closed) for
each release.

<!-- The topmost release date is automatically updated by GitHub Actions. When
creating a new release entry be sure to copy & paste the span tag with the
`actions:bind` attribute, which is used by a regex to find the text to be
updated. Only the first match gets replaced, so it's fine to leave the old
ones in. -->
-------------------------------------------------------------------------------
## __cylc-uiserver-1.0.3 (<span actions:bind='release-date'>Released 2022-05-20</span>)__

[Updated cylc-ui to 1.2.1](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md#cylc-ui-121-released-2022-05-30)

-------------------------------------------------------------------------------
## __cylc-uiserver-1.0.2 (<span actions:bind='release-date'>Released 2022-05-20</span>)__

[Updated cylc-ui to 1.2.0](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md#cylc-ui-120-released-2022-05-19)

Internal changes, see https://github.com/cylc/cylc-uiserver/milestone/11?closed=1

-------------------------------------------------------------------------------
## __cylc-uiserver-1.0.1 (<span actions:bind='release-date'>Released 2022-03-23</span>)__

[Updated cylc-ui to 1.1.0](https://github.com/cylc/cylc-ui/blob/master/CHANGES.md#cylc-ui-110-released-2022-03-23)

### Fixes

[#324](https://github.com/cylc/cylc-uiserver/pull/324) -
Fix issues where workflow status could be incorrect.

-------------------------------------------------------------------------------
## __cylc-uiserver-1.0.0 (<span actions:bind='release-date'>Released 2022-02-17</span>)__

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

-------------------------------------------------------------------------------
## __cylc-uiserver-0.6.0 (<span actions:bind='release-date'>Released 2021-11-11</span>)__

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

-------------------------------------------------------------------------------
## __cylc-uiserver-0.5.0 (<span actions:bind='release-date'>Released 2021-07-28</span>)__

### Enhancements

[#214](https://github.com/cylc/cylc-uiserver/pull/214) -
Store the JupyterHub runtime files in ~/.cylc/hub.

-------------------------------------------------------------------------------
## __cylc-uiserver-0.4.0 (<span actions:bind='release-date'>Released 2021-04-21</span>)__

### Enhancements

[#202](https://github.com/cylc/cylc-uiserver/pull/202) -
Add authorisation for multi-user setups.

[#197](https://github.com/cylc/cylc-uiserver/pull/197) -
Make the workflow scan interval configurable.

-------------------------------------------------------------------------------
## __cylc-uiserver-0.3.0 (2021-03-29)__

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

-------------------------------------------------------------------------------
## __cylc-uiserver-0.2 (2020-07-14)__

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

-------------------------------------------------------------------------------
## __cylc-uiserver-0.1 (2019-09-18)__

Initial release of Cylc UI Server.
