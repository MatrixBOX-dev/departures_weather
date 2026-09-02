# Station cycling and optional weather

Show one stop at a time and switch to the next on a timer, instead of side by side.
Optionally show the weather in between.

![Cycling between two stops with a weather screen in between](media/two-stations.gif)

A demo recording of two stops with a switch screen between them. The timings are the
defaults, 15 seconds per stop and 3 seconds on the switch screen, and both are
settings.

## Taking the changes

Four commits, oldest first. Pick any of them:

| | |
|---|---|
| [`fix: persist day timers`](https://github.com/MatrixBOX-dev/departures_weather/commit/1e5e2dfb113f33e089d02bbec045b1277ac150ba) | independent |
| [`fix: decode percent-escaped params as UTF-8`](https://github.com/MatrixBOX-dev/departures_weather/commit/12b876be40afd0ed12b67fc8b8d19868fd771d66) | independent |
| [`feat: cycle configured stations on a timer`](https://github.com/MatrixBOX-dev/departures_weather/commit/cb16af0161556a0f25ded06a55a5a179a3daadc0) | independent |
| [`feat: optional weather screen between stations`](https://github.com/MatrixBOX-dev/departures_weather/commit/f4eb8c648f433fa877c42355a4611066b336af7f) | needs the one above |

```
git remote add jw https://github.com/MatrixBOX-dev/departures_weather.git
git fetch jw
git cherry-pick <sha>
```

The branch has one more commit adding this file and the recording. Skip it.

## The two fixes

Both turned up by accident while building the features. Neither is related to them,
and both can go in on their own.

Day timers were kept in memory and lost on reboot. They are now saved when set or
cleared.

Text from the settings page was decoded with a table covering only Western European
letters. A Polish stop like Śródmieście was stored, and shown, as
`%C5%9Aródmie%C5%9Bcie`. Greek and Cyrillic behaved the same way.

## Cycling

The sign names the stop it is switching to. That pause is when the next stop's
departures are fetched, so they are ready when it ends instead of leaving the panel
blank.

## Weather

Second row of the switch screen: conditions for the next couple of hours, the current
temperature, and today's high while it is still ahead. No text on the row.

Weather is for one location you configure, not per stop.

It also works with a single stop and cycling off. The switch screen still appears on
the interval.

## Settings

| | |
|---|---|
| Cycle stations | one stop at a time, switching on a timer |
| Seconds per screen | how long each stop stays up (15) |
| Switch screen seconds | how long the next stop's name shows (3) |
| Weather on switch screen | draw the weather on row two |
| Latitude, longitude | decimal degrees, comma or dot |

Both features are off by default. Neither runs in portrait, or while side by side is
on.

## Tested

Simulator, live SL and weather data, all three sign sizes. 21 switches in a row at
192x32: departures ready every time, no failed fetches, no errors. Both fixes
confirmed through the settings page. Not run on hardware.

## Why not a separate app

Cycling and the weather screen sit on top of most of the departures app: fetching and
parsing, both display modes, the settings page, the 63 KB operator table. A standalone
version would be a copy of the app under a new name, around 214 KB, re-merged by hand
every time the original changes. `DSA_2_0` is that, and `departures_skins` exists to
avoid more of it.

This is 372 added lines behind two settings switches. No existing line in the settings
or startup files changes. Cycling reuses the stop slots side by side already defines,
so nothing gets configured twice.
