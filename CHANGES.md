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
## __cylc-uiserver-0.4.0 (<span actions:bind='release-date'>2021-04-?</span>)__

### Enhancements

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
