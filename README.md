# Reproducing SIEVE: a simpler cache eviction algorithm

Operating Systems group project, Texas Tech University, Fall 2026, Group 1.

This repository reproduces the Zipf experiments from the NSDI 2024 paper "SIEVE is Simpler than LRU" by Zhang, Yang, Yue, Vigfusson and Rashmi [paper PDF](docs/nsdi24-zhang-yazhuo-SIEVE.pdf). It is a fork of the authors' repository, [Thesys-lab/NSDI24-SIEVE](https://github.com/Thesys-lab/NSDI24-SIEVE). We added an independent Python simulator of FIFO, LRU, CLOCK and SIEVE, ran it on generated Zipf traces, and compared our figures with Figures 8a, 9a and 11 of the paper. We also fixed two problems that stopped the authors' simulator from building on Linux.

## Team

| Name | Role |
|---|---|
| Ohi Moiza | Lead, simulator build, experiments, slides |
| Umar Afolami | Repository setup, Zipf runs |
| Kachi Okoye | Workload comparisons, original figures |
| Ufanabasi Ekeng | Algorithm diagram and method explanation |
| Amaan Abdul Rahman | Report lead, results documentation |

## What we changed in the authors' code

1. The libCacheSim install script does not install the zstd development headers, so the build fails on a clean Ubuntu machine. Install them first with `sudo apt install libzstd-dev`.
2. `libCacheSim/libCacheSim/cache/eviction/other/S3LRU.c` included the hash table header with a wrong relative path. We changed `../../dataStructure/hashtable/hashtable.h` to `../../../dataStructure/hashtable/hashtable.h` in commit 79ff556.

With both fixes the simulator builds and runs. Our first Zipf run with it is in [zipf_1.0.pdf](zipf_1.0.pdf) and [result/zipf_1.0](result/zipf_1.0).

## Running our experiments

The Python simulator runs on Windows, macOS or Linux. It needs Python 3 with numpy and matplotlib.

```bash
pip install numpy matplotlib
python experiments/sieve_sim.py
python experiments/make_figures.py
```

`sieve_sim.py` generates Zipf traces of 1,000,000 requests drawn from a set of 100,000 objects, for alpha from 0.6 to 1.4. It runs FIFO, LRU, CLOCK and SIEVE at cache sizes of 0.1%, 0.5%, 1%, 5% and 10% of the unique objects in each trace. Every object has size 1. It also computes a best possible cache that always holds the most requested objects, which serves as a lower bound on the miss ratio. The run takes about 15 seconds on a laptop and writes `experiments/results.json`.

`make_figures.py` reads `results.json`, prints a summary table and writes these files to `experiments/figures/`:

| File | Paired with |
|---|---|
| `fig_miss_ratio_vs_size.png` | Paper Figure 8a, miss ratio against cache size at alpha 1.0 |
| `fig_miss_ratio_vs_skew.png` | Paper Figure 9a, miss ratio against Zipf alpha |
| `fig_reduction_vs_fifo.png` | Paper Figure 11, SIEVE miss reduction compared with FIFO |
| `summary.txt` | The numbers quoted in the report |

Crops of the paper figures are in `paper_figures/`.

### Main result

At alpha 1.0 and a cache of 1% of the objects, the miss ratios are 0.419 for SIEVE, 0.502 for CLOCK, 0.513 for LRU and 0.555 for FIFO. SIEVE has the lowest miss ratio of the four at every cache size and every alpha we tested. The percentage of misses SIEVE removes compared with FIFO is:

| alpha | 0.1% | 0.5% | 1% | 5% | 10% |
|---|---|---|---|---|---|
| 0.8 | 11 | 14 | 15 | 18 | 19 |
| 1.0 | 21 | 24 | 25 | 25 | 26 |
| 1.2 | 30 | 33 | 33 | 32 | 30 |

The paper reports 12%, 22% and 32% at its small cache and 22%, 28% and 33% at its large cache for the same three alpha values. Our values at the matching sizes are within 3 points of these.

## Repository layout

| Path | Contents |
|---|---|
| `experiments/` | Our Python simulator, figure script, results and figures |
| `paper_figures/` | Figures 8a, 9a and 11 cropped from the paper |
| `docs/` | The paper, the course project description, the report template, our slides and our report |
| `libCacheSim/` | The authors' snapshot of the libCacheSim simulator, with our include path fix |
| `mydata/zipf/` | The authors' sample Zipf trace |
| `result/`, `zipf_1.0.pdf` | Output of our first libCacheSim run |
| `doc/diagram/` | The authors' diagrams and logo |

## Original authors' instructions

The rest of this file is adapted from the authors' README. The work, the simulator and the prototypes below belong to the paper's authors.

### Install libCacheSim (Linux)

```bash
sudo apt install libzstd-dev
cd libCacheSim/scripts && bash install_dependency.sh && bash install_libcachesim.sh
```

After the build, `cachesim` is in `_build/bin/`.

```bash
# ./cachesim DATAPATH TRACE_FORMAT EVICTION_ALGO CACHE_SIZE [OPTION...]
# Run a single cache simulation
./_build/bin/cachesim data/trace.oracleGeneral.bin oracleGeneral sieve 1gb
# Run several algorithms over several cache sizes (CACHE_SIZE 0)
./_build/bin/cachesim data/trace.oracleGeneral.bin oracleGeneral fifo,lru,clock,sieve 0 --ignore-obj-size 1
```

Results are written to `result/TRACE_NAME`. The [libCacheSim repository](https://github.com/1a1a11a/libCacheSim) has more detailed instructions.

### Zipf example

The authors include a small Zipf trace in `mydata/zipf/`. This command plots miss ratio against cache size for four algorithms:

```bash
python3 libCacheSim/scripts/plot_mrc_size.py --tracepath mydata/zipf/zipf_1.0 --trace-format txt --algos=fifo,lru,clock,sieve
```

<img src="doc/diagram/mr_zipf.png" alt="Miss ratio against cache size on the authors' Zipf trace" width="480"/>

A new trace can be generated with:

```bash
python3 libCacheSim/scripts/data_gen.py -m 10000 -n 1000000 --alpha 1.0 > mydata/zipf/zipf_1.0
```

### Traces used in the paper

| Trace | Approx time | Traces | Cache type | Requests (million) | Objects (million) |
|---|---|---|---|---|---|
| [Tencent Photo](https://ftp.pdl.cmu.edu/pub/datasets/twemcacheWorkload/cacheDatasets/tencentPhoto/) | 2018 | 2 | object | 5,650 | 1,038 |
| [Wiki CDN](https://ftp.pdl.cmu.edu/pub/datasets/twemcacheWorkload/cacheDatasets/wiki/) | 2019 | 3 | object | 2,863 | 56 |
| [Twitter KV](https://ftp.pdl.cmu.edu/pub/datasets/twemcacheWorkload/cacheDatasets/twitter/) | 2020 | 54 | KV | 195,441 | 10,650 |
| [Meta KV](https://ftp.pdl.cmu.edu/pub/datasets/twemcacheWorkload/cacheDatasets/metaKV/) | 2022 | 5 | KV | 1,644 | 82 |
| [Meta CDN](https://ftp.pdl.cmu.edu/pub/datasets/twemcacheWorkload/cacheDatasets/metaCDN/) | 2023 | 3 | object | 231 | 76 |

### Prototypes

The authors replaced LRU with SIEVE in popular cache libraries written in five languages.

- [groupcache](https://github.com/cacheMon/groupcache) (Go): 21 lines changed.
- [mnemonist](https://github.com/cacheMon/mnemonist) (JavaScript): 12 lines changed.
- [lru-rs](https://github.com/cacheMon/lru-rs) (Rust): 16 lines changed.
- [lru-dict](https://github.com/cacheMon/lru-dict) (Python and C): 21 lines changed.
- [cachelib](https://github.com/Thesys-lab/cachelib-sosp23) (C++): CacheLib contains many optimizations for LRU that SIEVE does not need, so the authors did not report a line count.

## License

Apache License 2.0, as in the original repository. See [LICENSE](LICENSE).

## Reference

```bibtex
@inproceedings{zhang2024-sieve,
  title={SIEVE is Simpler than LRU: an Efficient Turn-Key Eviction Algorithm for Web Caches},
  author={Zhang, Yazhuo and Yang, Juncheng and Yue, Yao and Vigfusson, Ymir and Rashmi, K.V.},
  booktitle={USENIX Symposium on Networked Systems Design and Implementation (NSDI'24)},
  year={2024}
}
```

Y. Zhang, J. Yang, Y. Yue, Y. Vigfusson, and K. V. Rashmi, "SIEVE is Simpler than LRU: an Efficient Turn-Key Eviction Algorithm for Web Caches," in 21st USENIX Symposium on Networked Systems Design and Implementation (NSDI 24), Santa Clara, CA, April 2024, pp. 1229 to 1246.
