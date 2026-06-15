---
name: redis-search-ftexplain-optimization
description: "Interpret and optimize Redis Search `FT.EXPLAIN` and `FT.EXPLAINCLI` output for text, tag, numeric, and vector hybrid queries. Use when the user asks how to read a Redis Query Engine plan, compare dialect behavior, debug unexpected Search results, or improve slow vector/text queries before using `FT.PROFILE`."
---

# Redis Search FT.EXPLAIN Optimization

Use this skill to turn `FT.EXPLAIN` or `FT.EXPLAINCLI` output into a concrete diagnosis and query/index tuning plan.

## Workflow

1. Capture the exact `FT.SEARCH`, `FT.AGGREGATE`, or vector query, including `DIALECT`, `PARAMS`, `SORTBY`, `LIMIT`, and field names.
2. Ask for or run `FT.EXPLAINCLI <index> "<query>" DIALECT <n>` when the plan is long or nested; use `FT.EXPLAIN` when a compact single-line plan is enough.
3. Confirm the dialect. Prefer `DIALECT 2` or newer for modern Search and vector use cases; compare against `DIALECT 1` only when investigating legacy parsing behavior.
4. Read the plan from the most selective filters toward the expensive stages. Confirm that TAG, NUMERIC, or TEXT filters constrain candidates before vector search when the query is intended to be filtered KNN.
5. Compare the logical plan with the schema and data model. Verify that fields used in filters are indexed with the expected type and that query syntax matches the schema.
6. If the plan looks reasonable but runtime is slow, switch to `FT.PROFILE` to measure iterator work and elapsed time.

## Operator Map

| Plan operator | Meaning | Tuning cue |
| --- | --- | --- |
| `INTERSECT` | Logical AND between child predicates | Good when selective filters are combined before expensive work. |
| `UNION` | Logical OR between child predicates | Watch for broad candidate expansion. |
| `NOT` | Negated predicate | Check that exclusions do not force broad scans. |
| `VECTOR` | Vector similarity stage | Should usually appear after selective pre-filters for hybrid queries. |
| `TAG` | Exact tag field filter | Use for low-cardinality exact filters. |
| `TEXT` | Text field search | Check stemming and tokenization effects. |
| `NUMERIC` | Numeric range or equality filter | Use for selective ranges and exact numeric constraints. |

## Interpretation Rules

- A filtered hybrid query should show candidate-limiting predicates such as `INTERSECT`, `TAG`, or `NUMERIC` feeding the vector stage.
- A `+` on a term indicates stemming or expansion. Treat it as expected only if stemming matches user intent.
- Unexpected result counts usually mean schema mismatch, indexing lag/failure, query syntax parsing differences, or a dialect mismatch.
- Do not optimize from the explain plan alone. Use `FT.PROFILE` after the logical plan is understood.

## Troubleshooting Matrix

| Symptom | Likely cause | Next action |
| --- | --- | --- |
| Fewer results than expected | Indexing failure, stale index, or schema mismatch | Check `FT.INFO` for indexing failures and compare stored fields with schema. |
| Unexpected matches | Query parsed differently than intended | Compare `FT.EXPLAINCLI` under the current dialect and a legacy dialect if relevant. |
| Slow hybrid query | Vector stage sees too many candidates | Add or tighten TAG/NUMERIC/TEXT pre-filters and confirm plan shape. |
| Output is hard to read | Large nested plan | Use `FT.EXPLAINCLI` instead of `FT.EXPLAIN`. |
| Dialect changes behavior | Legacy parser compatibility issue | Pin the intended dialect in the application query. |

## Examples

Filtered hybrid plan check:

```text
FT.EXPLAINCLI myindex "(@content:carbonara) @genre:{technical}=>[KNN 2 @embedding $vec AS score]" PARAMS 2 vec <blob> DIALECT 2
```

Look for the text/tag filters narrowing candidates before the KNN/vector stage. If the vector stage is effectively unfiltered, revise the query or index fields before benchmarking.

Numeric exclusion check:

```text
INTERSECT {
  NOT{ NUMERIC {79 <= @st <= 79} }
  NUMERIC {71 <= @rag <= 71}
}
```

Interpret this as an AND of one exclusion and one positive numeric filter; validate that both fields are indexed as numeric fields.
