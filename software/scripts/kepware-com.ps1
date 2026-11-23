# Kepware COM Control Script
# Usage: powershell -File kepware-com.ps1 [action] [channel] [device] [tag] [value]
#
# Examples:
#   powershell -File kepware-com.ps1 list-channels
#   powershell -File kepware-com.ps1 list-devices -Channel "ModbusTCP"
#   powershell -File kepware-com.ps1 read-tag -Channel "ModbusTCP" -Device "PLC1" -Tag "Temperature"
#   powershell -File kepware-com.ps1 write-tag -Channel "ModbusTCP" -Device "PLC1" -Tag "Temperature" -Value 25.5
#   powershell -File kepware-com.ps1 channel-status
#   powershell -File kepware-com.ps1 start-channel -Channel "ModbusTCP"
#   powershell -File kepware-com.ps1 stop-channel -Channel "ModbusTCP"

param(
    [Parameter(Mandatory=$true)]
    [string]$Action,
    [string]$Channel = "",
    [string]$Device = "",
    [string]$Tag = "",
    [string]$Value = ""
)

$ErrorActionPreference = "Stop"

try {
    $kps = New-Object -ComObject "Kepware.KEPServerEX.V4"
    $kps.Connect()

    switch ($Action) {
        "list-channels" {
            $channels = $kps.GetChannels()
            foreach ($ch in $channels) {
                Write-Output "CHANNEL| $($ch.Name) | $($ch.Status) | $($ch.Driver)"
            }
        }
        "list-devices" {
            $channel = $kps.GetChannel($Channel)
            if (-not $channel) { throw "Channel not found: $Channel" }
            Write-Output "Channel: $Channel"
            $devices = $channel.GetDevices()
            foreach ($d in $devices) {
                Write-Output "DEVICE| $($d.Name) | $($d.Status) | $($d.Address)"
            }
        }
        "list-tags" {
            $channel = $kps.GetChannel($Channel)
            if (-not $channel) { throw "Channel not found: $Channel" }
            $device = $channel.GetDevice($Device)
            if (-not $device) { throw "Device not found: $Device" }
            Write-Output "Device: $Device"
            $tags = $device.GetTags()
            foreach ($t in $tags) {
                Write-Output "TAG| $($t.Name) | $($t.Datatype) | $($t.Status)"
            }
        }
        "read-tag" {
            $channel = $kps.GetChannel($Channel)
            if (-not $channel) { throw "Channel not found: $Channel" }
            $device = $channel.GetDevice($Device)
            if (-not $device) { throw "Device not found: $Device" }
            $tag = $device.GetTag($Tag)
            if (-not $tag) { throw "Tag not found: $Tag" }
            $val = $tag.Read()
            Write-Output "VALUE| $($tag.Name) | $($val.Value) | $($val.Quality) | $($val.Timestamp)"
        }
        "write-tag" {
            if (-not $Value) { throw "Value required for write" }
            $channel = $kps.GetChannel($Channel)
            if (-not $channel) { throw "Channel not found: $Channel" }
            $device = $channel.GetDevice($Device)
            if (-not $device) { throw "Device not found: $Device" }
            $tag = $device.GetTag($Tag)
            if (-not $tag) { throw "Tag not found: $Tag" }
            $tag.Write($Value)
            Write-Output "OK| Tag $Tag written with value: $Value"
        }
        "channel-status" {
            $channels = $kps.GetChannels()
            foreach ($ch in $channels) {
                Write-Output "CHANNEL_STATUS| $($ch.Name) | Enabled: $($ch.Enabled) | Status: $($ch.Status)"
            }
        }
        "start-channel" {
            $channel = $kps.GetChannel($Channel)
            if (-not $channel) { throw "Channel not found: $Channel" }
            if ($channel.Status -eq 0) {
                $channel.Start()
                Write-Output "OK| Channel $Channel started"
            } else {
                Write-Output "INFO| Channel $Channel already running"
            }
        }
        "stop-channel" {
            $channel = $kps.GetChannel($Channel)
            if (-not $channel) { throw "Channel not found: $Channel" }
            if ($channel.Status -ne 0) {
                $channel.Stop()
                Write-Output "OK| Channel $Channel stopped"
            } else {
                Write-Output "INFO| Channel $Channel already stopped"
            }
        }
        default {
            Write-Output "ERROR| Unknown action: $Action"
            Write-Output "Available actions: list-channels, list-devices, list-tags, read-tag, write-tag, channel-status, start-channel, stop-channel"
        }
    }

    $kps.Disconnect()
} catch {
    Write-Output "ERROR| $($_.Exception.Message)"
}
