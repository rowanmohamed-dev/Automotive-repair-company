# Reactive Agent

## Overview

The Reactive Agent is a rule-based agent that uses predefined rules
to select and execute the appropriate vehicle repair tool.

## Architecture

User Request
    ↓
Reactive Agent
    ↓
Predefined Rules
    ↓
VehicleTools
    ↓
Dataset

## Available Requests

- Customer history
- Similar problems
- Problem solution
- Problems by vehicle brand
- Location statistics

## Limitations

The Reactive Agent does not use an LLM or reasoning process.
It relies on predefined rules and therefore may fail on unexpected
or complex user requests.