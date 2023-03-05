# scale-models-log-clocks

Run default with  `python main.py --duration 60`

Run unit tests for file initialization and writing using `python unit_test.py`

Run pre-defined experiments using `./experiments.sh`

## Flags

- `--clock_range`, sets the range from which each process's clock will randomly choose their clock rate. default `7`.
- `--act_range`, sets the range from which each process will roll the dice at each of their clock ticks to do an action. default `11`.
- `--duration`, how many seconds the experiment will run for. default `10`.
- `--log_name`, the base log name to which processes will write their logs. Will write to `logs/<log_name>_<0,1,2>` based on thread_id. default `process`
- `--p0_clock`, to manually set process 0's clock rate instead of allowing to randomly choose.
- `--p1_clock`, to manually set process 1's clock rate instead of allowing to randomly choose.
- `--p2_clock`, to manually set process 2's clock rate instead of allowing to randomly choose.
- `--p0_act`, to manually set process 0's action range instead of using the act_range.
- `--p1_act`, to manually set process 1's action range instead of using the act_range.
- `--p2_act`, to manually set process 2's action range instead of using the act_range.
