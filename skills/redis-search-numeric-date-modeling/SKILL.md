---
name: redis-search-numeric-date-modeling
description: Use when designing or troubleshooting Redis Search or Redis Query Engine schemas for numeric precision, 64-bit identifiers, large integer rounding, NUMERIC versus TAG field choices, timestamp/date storage, epoch seconds versus milliseconds, ISO date strings, range filters, numeric sorting, or missing results caused by field type or prefix mismatches.
---

# Redis Search Numeric And Date Modeling

Use this skill to choose reliable Redis Search and Query Engine field types for numbers, identifiers, and dates.

## Core Rules

- Use `NUMERIC` for values that need range filters, numeric sorting, scoring, durations, prices, metrics, or timestamps.
- Use `TAG` for identifiers and large exact-match values, especially 64-bit IDs that must not be rounded.
- Store dates and times as Unix epoch seconds in a `NUMERIC` field when range queries or sorting matter.
- Avoid ISO 8601 strings for indexed date ranges unless an external integration requires them and the application handles parsing and ordering.
- Check whether incoming timestamps are seconds or milliseconds before indexing.

## Precision Boundary

Redis numeric indexes use double-precision floating-point representation. Integers above the 53-bit exact range can be approximated.

Treat values above `9007199254740992` as unsafe for exact numeric identity matching. If the value is an order ID, user ID, trace ID, invoice ID, or any other identifier, model it as a string and index it as `TAG`.

## Type Decision Matrix

| Field purpose | Recommended type | Why |
| --- | --- | --- |
| Price, score, duration, quantity | `NUMERIC` | Supports numeric range filters and sorting. |
| Created/updated timestamp | `NUMERIC` epoch seconds | Supports efficient time windows and sorting. |
| Large ID or opaque ID | `TAG` | Preserves exact equality. |
| Category, month name, status | `TAG` | Exact filtering without numeric semantics. |
| Display-only formatted date | Usually not indexed | Convert in the application after retrieval. |

## Implementation Pattern

For hashes:

```redis
HSET user:1001 created_at 1714848000 order_id "999999999999999999"
FT.CREATE user_idx ON HASH PREFIX 1 user: SCHEMA created_at NUMERIC order_id TAG
```

For JSON:

```redis
JSON.SET user:1001 $ '{"created_at":1714848000,"order_id":"999999999999999999"}'
FT.CREATE user_idx ON JSON PREFIX 1 user: SCHEMA $.created_at AS created_at NUMERIC $.order_id AS order_id TAG
```

Convert human-readable dates at the application boundary:

```python
import time

epoch_seconds = int(time.time())
```

```javascript
const epochSeconds = Math.floor(Date.now() / 1000);
```

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Large numbers come back rounded | Identifier indexed as `NUMERIC`. | Store as string and index as `TAG`; rebuild or recreate the index as needed. |
| Range query returns no results | Field is indexed as `TAG` or document path/prefix does not match. | Check `FT.INFO`, schema aliases, and key prefixes. |
| Date windows are off by 1000x | Milliseconds stored where seconds were expected, or the reverse. | Normalize units and backfill indexed documents. |
| Timezone mismatch | Formatted local-time strings are being indexed. | Store UTC epoch seconds and format for display after retrieval. |
| Sort order is lexical, not numeric | Date or number stored as a string field. | Reindex as `NUMERIC` if sorting by value is required. |

## Verification

1. Run `FT.INFO <index>` and confirm field types.
2. Inspect one stored document and confirm numbers are stored in the intended representation.
3. Run a narrow equality query for TAG identifiers and a range query for NUMERIC fields.
4. Test boundary values near the largest expected ID or timestamp.
5. Confirm the application converts epoch seconds back to display dates after retrieval.
