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


## comparison modes

- pytest only (baseline)
- pytest-ranking strategies
    - QRF: ordering by tests with shorter runtime (weight as **1-0** in regsmart)
    - RecentFail:ordering by recently-failed tests (weight as **0-1** in regsmart)
    - SimChgPath: ordering by tests whose IDs are more textually similar to the paths of Python files changed
- pytest-regsmart strategies
    - selecting per file
    - selecting per function
    - (both above varying RTP weigts)

