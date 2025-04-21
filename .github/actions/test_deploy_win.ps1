# Copyright (C) 2015, GuardBear Inc.
#
# This program is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License (version 2) as published by the FSF - Free Software
# Foundation.

$VERSION = Get-Content src/VERSION
[version]$VERSION = $VERSION -replace '[v]',''
$MAJOR=$VERSION.Major
$MINOR=$VERSION.Minor
$SHA= git rev-parse --short $args[0]

$TEST_ARRAY=@( 
              @("GUARDBEAR_MANAGER ", "1.1.1.1", "<address>", "</address>"), 
              @("GUARDBEAR_MANAGER_PORT ", "7777", "<port>", "</port>"),
              @("GUARDBEAR_PROTOCOL ", "udp", "<protocol>", "</protocol>"),
              @("GUARDBEAR_REGISTRATION_SERVER ", "2.2.2.2", "<manager_address>", "</manager_address>"),
              @("GUARDBEAR_REGISTRATION_PORT ", "8888", "<port>", "</port>"),
              @("GUARDBEAR_REGISTRATION_PASSWORD ", "password", "<password>", "</password>"),
              @("GUARDBEAR_KEEP_ALIVE_INTERVAL ", "10", "<notify_time>", "</notify_time>"),
              @("GUARDBEAR_TIME_RECONNECT ", "10", "<time-reconnect>", "</time-reconnect>"),
              @("GUARDBEAR_REGISTRATION_CA ", "/var/ossec/etc/testsslmanager.cert", "<server_ca_path>", "</server_ca_path>"),
              @("GUARDBEAR_REGISTRATION_CERTIFICATE ", "/var/ossec/etc/testsslmanager.cert", "<agent_certificate_path>", "</agent_certificate_path>"),
              @("GUARDBEAR_REGISTRATION_KEY ", "/var/ossec/etc/testsslmanager.key", "<agent_key_path>", "</agent_key_path>"),
              @("GUARDBEAR_AGENT_NAME ", "test-agent", "<agent_name>", "</agent_name>"),
              @("GUARDBEAR_AGENT_GROUP ", "test-group", "<groups>", "</groups>"),
              @("ENROLLMENT_DELAY ", "10", "<delay_after_enrollment>", "</delay_after_enrollment>")
)

function install_guardbear($vars)
{

    Write-Output "Testing the following variables $vars"
    Start-Process  C:\Windows\System32\msiexec.exe -ArgumentList  "/i guardbear-agent-$VERSION-0.commit$SHA.msi /qn $vars" -wait
    
}

function remove_guardbear
{

    Start-Process  C:\Windows\System32\msiexec.exe -ArgumentList "/x guardbear-agent-$VERSION-commit$SHA.msi /qn" -wait

}

function test($vars)
{

  For ($i=0; $i -lt $TEST_ARRAY.Length; $i++) {
    if($vars.Contains($TEST_ARRAY[$i][0])) {
      if ( ($TEST_ARRAY[$i][0] -eq "GUARDBEAR_MANAGER ") -OR ($TEST_ARRAY[$i][0] -eq "GUARDBEAR_PROTOCOL ") ) {
        $LIST = $TEST_ARRAY[$i][1].split(",")
        For ($j=0; $j -lt $LIST.Length; $j++) {
          $SEL = Select-String -Path 'C:\Program Files (x86)\ossec-agent\ossec.conf' -Pattern "$($TEST_ARRAY[$i][2])$($LIST[$j])$($TEST_ARRAY[$i][3])"
          if($SEL -ne $null) {
            Write-Output "The variable $($TEST_ARRAY[$i][0]) is set correctly"
          }
          if($SEL -eq $null) {
            Write-Output "The variable $($TEST_ARRAY[$i][0]) is not set correctly"
            exit 1
          }
        }
      }
      ElseIf ( ($TEST_ARRAY[$i][0] -eq "GUARDBEAR_REGISTRATION_PASSWORD ") ) {
        if (Test-Path 'C:\Program Files (x86)\ossec-agent\authd.pass'){
          $SEL = Select-String -Path 'C:\Program Files (x86)\ossec-agent\authd.pass' -Pattern "$($TEST_ARRAY[$i][1])"
          if($SEL -ne $null) {
            Write-Output "The variable $($TEST_ARRAY[$i][0]) is set correctly"
          }
          if($SEL -eq $null) {
            Write-Output "The variable $($TEST_ARRAY[$i][0]) is not set correctly"
            exit 1
          }
        }
        else
        {
          Write-Output "GUARDBEAR_REGISTRATION_PASSWORD is not correct"
          exit 1
        }
      }
      Else {
        $SEL = Select-String -Path 'C:\Program Files (x86)\ossec-agent\ossec.conf' -Pattern "$($TEST_ARRAY[$i][2])$($TEST_ARRAY[$i][1])$($TEST_ARRAY[$i][3])"
        if($SEL -ne $null) {
          Write-Output "The variable $($TEST_ARRAY[$i][0]) is set correctly"
        }
        if($SEL -eq $null) {
          Write-Output "The variable $($TEST_ARRAY[$i][0]) is not set correctly"
          exit 1
        }
      }
    }
  }

}

Write-Output "Download package: https://s3.us-west-1.amazonaws.com/packages-dev.guardbear.com/warehouse/pullrequests/$MAJOR.$MINOR/windows/guardbear-agent-$VERSION-0.commit$SHA.msi"
Invoke-WebRequest -Uri "https://s3.us-west-1.amazonaws.com/packages-dev.guardbear.com/warehouse/pullrequests/$MAJOR.$MINOR/windows/guardbear-agent-$VERSION-0.commit$SHA.msi" -OutFile "guardbear-agent-$VERSION-0.commit$SHA.msi"

install_guardbear "GUARDBEAR_MANAGER=1.1.1.1 GUARDBEAR_MANAGER_PORT=7777 GUARDBEAR_PROTOCOL=udp GUARDBEAR_REGISTRATION_SERVER=2.2.2.2 GUARDBEAR_REGISTRATION_PORT=8888 GUARDBEAR_REGISTRATION_PASSWORD=password GUARDBEAR_KEEP_ALIVE_INTERVAL=10 GUARDBEAR_TIME_RECONNECT=10 GUARDBEAR_REGISTRATION_CA=/var/ossec/etc/testsslmanager.cert GUARDBEAR_REGISTRATION_CERTIFICATE=/var/ossec/etc/testsslmanager.cert GUARDBEAR_REGISTRATION_KEY=/var/ossec/etc/testsslmanager.key GUARDBEAR_AGENT_NAME=test-agent GUARDBEAR_AGENT_GROUP=test-group ENROLLMENT_DELAY=10" 
test "GUARDBEAR_MANAGER GUARDBEAR_MANAGER_PORT GUARDBEAR_PROTOCOL GUARDBEAR_REGISTRATION_SERVER GUARDBEAR_REGISTRATION_PORT GUARDBEAR_REGISTRATION_PASSWORD GUARDBEAR_KEEP_ALIVE_INTERVAL GUARDBEAR_TIME_RECONNECT GUARDBEAR_REGISTRATION_CA GUARDBEAR_REGISTRATION_CERTIFICATE GUARDBEAR_REGISTRATION_KEY GUARDBEAR_AGENT_NAME GUARDBEAR_AGENT_GROUP ENROLLMENT_DELAY " 
remove_guardbear

install_guardbear "GUARDBEAR_MANAGER=1.1.1.1"
test "GUARDBEAR_MANAGER "
remove_guardbear

install_guardbear "GUARDBEAR_MANAGER_PORT=7777"
test "GUARDBEAR_MANAGER_PORT "
remove_guardbear

install_guardbear "GUARDBEAR_PROTOCOL=udp"
test "GUARDBEAR_PROTOCOL "
remove_guardbear

install_guardbear "GUARDBEAR_REGISTRATION_SERVER=2.2.2.2"
test "GUARDBEAR_REGISTRATION_SERVER "
remove_guardbear

install_guardbear "GUARDBEAR_REGISTRATION_PORT=8888"
test "GUARDBEAR_REGISTRATION_PORT "
remove_guardbear

install_guardbear "GUARDBEAR_REGISTRATION_PASSWORD=password"
test "GUARDBEAR_REGISTRATION_PASSWORD "
remove_guardbear

install_guardbear "GUARDBEAR_KEEP_ALIVE_INTERVAL=10"
test "GUARDBEAR_KEEP_ALIVE_INTERVAL "
remove_guardbear

install_guardbear "GUARDBEAR_TIME_RECONNECT=10"
test "GUARDBEAR_TIME_RECONNECT "
remove_guardbear

install_guardbear "GUARDBEAR_REGISTRATION_CA=/var/ossec/etc/testsslmanager.cert"
test "GUARDBEAR_REGISTRATION_CA "
remove_guardbear

install_guardbear "GUARDBEAR_REGISTRATION_CERTIFICATE=/var/ossec/etc/testsslmanager.cert"
test "GUARDBEAR_REGISTRATION_CERTIFICATE "
remove_guardbear

install_guardbear "GUARDBEAR_REGISTRATION_KEY=/var/ossec/etc/testsslmanager.key"
test "GUARDBEAR_REGISTRATION_KEY "
remove_guardbear

install_guardbear "GUARDBEAR_AGENT_NAME=test-agent"
test "GUARDBEAR_AGENT_NAME "
remove_guardbear

install_guardbear "GUARDBEAR_AGENT_GROUP=test-group"
test "GUARDBEAR_AGENT_GROUP "
remove_guardbear

install_guardbear "ENROLLMENT_DELAY=10"
test "ENROLLMENT_DELAY "
remove_guardbear
