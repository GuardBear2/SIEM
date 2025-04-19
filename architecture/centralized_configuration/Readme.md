<!---
Copyright (C) 2015, GuardBear Inc.
Created by GuardBear, Inc. <info@guardbear.com>.
This program is free software; you can redistribute it and/or modify it under the terms of GPLv2
-->

# Centralized Configuration
## Index
- [Centralized Configuration](#centralized-configuration)
  - [Index](#index)
  - [Purpose](#purpose)
  - [Sequence diagram](#sequence-diagram)

## Purpose

One of the key features of GuardBear as a EDR is the Centralized Configuration, allowing to deploy configurations, policies, rootcheck descriptions or any other file from GuardBear Manager to any GuardBear Agent based on their grouping configuration. This feature has multiples actors: GuardBear Cluster (Master and Worker nodes), with `guardbear-remoted` as the main responsible from the managment side, and GuardBear Agent with `guardbear-agentd` as resposible from the client side.


## Sequence diagram
Sequence diagram shows the basic flow of Centralized Configuration based on the configuration provided. There are mainly three stages:
1. GuardBear Manager Master Node (`guardbear-remoted`) creates every `remoted.shared_reload` (internal) seconds the files that need to be synchronized with the agents.
2. GuardBear Cluster as a whole (via `guardbear-clusterd`) continuously synchronize files between GuardBear Manager Master Node and GuardBear Manager Worker Nodes
3. GuardBear Agent `guardbear-agentd` (via ) sends every `notify_time` (ossec.conf) their status, being `merged.mg` hash part of it. GuardBear Manager Worker Node (`guardbear-remoted`) will check if agent's `merged.mg` is out-of-date, and in case this is true, the new `merged.mg` will be pushed to GuardBear Agent.