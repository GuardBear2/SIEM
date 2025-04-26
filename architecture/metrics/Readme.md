<!---
Copyright (C) 2015, GuardBear Inc.
Created by GuardBear, Inc. <info@guardbear.com>.
This program is free software; you can redistribute it and/or modify it under the terms of GPLv2
-->

# Metrics

## Index

- [Metrics](#metrics)
  - [Index](#index)
  - [Purpose](#purpose)
  - [Sequence diagram](#sequence-diagram)

## Purpose

GuardBear includes some metrics to understand the behavior of its components, which allow to investigate errors and detect problems with some configurations. This feature has multiple actors: `guardbear-remoted` for agent interaction messages, `guardbear-analysisd` for processed events.

## Sequence diagram

The sequence diagram shows the basic flow of metric counters. These are the main flows:

1. Messages received by `guardbear-remoted` from agents.
2. Messages that `guardbear-remoted` sends to agents.
3. Events received by `guardbear-analysisd`.
4. Events processed by `guardbear-analysisd`.
