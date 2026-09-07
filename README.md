# regsmart-metrics 

> script to collect metrics from CI workflows runs (pytest, ranking, regsmart)
> 
> project being evaluated: https://github.com/leticosta4/pytest-regsmart
> 

## metrics to be collected

- TSR time
- RTS time
- RTP time
- Time to first fault
- Number/percentage of hidden faults/changes
- Number/percentage of detected faults/changes
- APFDc


## comparison modes (10)

- pytest only (baseline)
- pytest-ranking strategies (3)
    - QRF: orders tests by shorter runtime (weighted 1–0 in regsmart)
    - RecentFail: orders tests by recent failures (weighted 0–1 in regsmart)
    - SimChgPath: orders tests by how textually similar their IDs are to the paths of changed Python files
- pytest-regsmart strategies (6)
    - selection granularity: per file / per function
    - RTP weight: none / partial / full
    - (2 granularities × 3 weight settings = 6)

