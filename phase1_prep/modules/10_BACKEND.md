# Module: Backend Application Server

## Purpose
Hosts REST APIs and real-time WebSocket channels serving streaming biosignals and model inferences.

## Inputs
HTTP requests & WebSocket client connections

## Processing
Runs asynchronous event loop broadcasting telemetry frames over `/ws` at 250Hz.

## Outputs
JSON WebSocket frames & HTTP responses

## Technologies
Python, FastAPI, Uvicorn, WebSockets

## Current Implementation
Fully operational backend server script (`app.py`).

## Evidence
`app.py` (lines 1-250)

## Current Status
`STATUS: COMPLETE`

## Remaining Work
JWT authentication token endpoints.

## Dependencies
Preprocessing, ML, & Authentication Modules

## Review Explanation
> "Our backend is powered by FastAPI and Uvicorn, pushing 250Hz streaming biosignals, DSP filter outputs, and ML model decisions to the frontend via WebSockets."
