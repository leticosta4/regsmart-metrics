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
- Workflow run time (Github Actions) - _maybe_


## comparison modes (9)

- pytest only (baseline)
- pytest-ranking strategies (4)
    - QTF: orders tests by shorter runtime (weighted 1–0 in regsmart)
    - RecentFail: orders tests by recent failures (weighted 0–1 in regsmart)
    - SimChgPath: orders tests by how textually similar their IDs are to the paths of changed Python files
    - Hybrid: unify/balance all 3 above
- pytest-regsmart strategies (4)
    - selection granularity: per function
    - RTP weight:
      - none (--no-rank)
      - QTF
      - RecentFail
      - Hybrid


## dataset: list of projects (14)

the dataset is composed of 14 forks from the GitHub repositories below:

- aeon-toolkit/aeon - https://github.com/aeon-toolkit/aeon
- ansible/ansible-lint - https://github.com/ansible/ansible-lint
- agronholm/apscheduler - https://github.com/agronholm/apscheduler
- dask/dask - https://github.com/dask/dask
- iterative/dvc - https://github.com/iterative/dvc
- ipython/ipython - https://github.com/ipython/ipython
- librosa/librosa - https://github.com/librosa/librosa
- ansible/molecule - https://github.com/ansible/molecule
- networkx/networkx - https://github.com/networkx/networkx
- pytest-dev/pytest-django - https://github.com/pytest-dev/pytest-django
- pytest-dev/pytest-xdist - https://github.com/pytest-dev/pytest-xdist
- Lightning-AI/pytorch-lightning - https://github.com/Lightning-AI/pytorch-lightning
- mikedh/trimesh - https://github.com/mikedh/trimesh
- ultralytics/ultralytics - https://github.com/ultralytics/ultralytics


## Tables

- Result table example: https://dl.acm.org/doi/pdf/10.1145/3696630.3728587 (pytest-ranking paper)
- [wip] Regsmart experiments table: https://docs.google.com/spreadsheets/d/135Y76Gk5xiq7A5H25R3dVN4CU9mEy-ivjeOr0HiKq0I/edit?usp=sharing
