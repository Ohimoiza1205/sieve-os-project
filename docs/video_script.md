# Group 1 SIEVE video script

Target length: about 5 minutes. Output file: `Group1_SIEVE_video.mp4`.

The left column is what to do on screen. The right column is what to say. Read the narration at a normal pace. Each scene lists a rough time.

## Before you record

1. Close everything you do not want on screen: email, chat, browser tabs.
2. Open these windows so you only switch between them during the recording:
   - File Explorer at `C:\Users\ohimo\sieve-os-project`
   - VS Code with the repo folder open
   - A terminal (Command Prompt or Git Bash) already in `C:\Users\ohimo\sieve-os-project`
   - The three paper figures from `paper_figures\` and the three figures from `experiments\figures\`. Open them in Photos or VS Code so you can show them side by side.
   - Optional for Scene 7: an Ubuntu (WSL) terminal.
3. Make the terminal and editor font bigger (Ctrl and plus in VS Code, right click title bar, Properties, Font in Command Prompt). Viewers need to read the numbers.
4. Do one test run of `python experiments\sieve_sim.py` before recording so you know it works.
5. Start recording: Win + Alt + R starts and stops Game Bar recording of the active window. To record several windows, use OBS with a Display Capture source instead. Game Bar only records one app window.

## Scene 1. Introduction (about 30 seconds)

| On screen | Say |
|---|---|
| File Explorer at the repo root. | "This is Group 1's Operating Systems project. We reproduced the SIEVE cache eviction algorithm from the NSDI 2024 paper by Zhang and others." |
| Open `README.md` on GitHub or in VS Code preview. Scroll slowly past the title, team and "What we changed" section. | "Our repository is a fork of the authors' code. We added our own Python simulator of FIFO, LRU, CLOCK and SIEVE, and we fixed two problems that stopped the authors' simulator from building on Linux." |

## Scene 2. The simulator code (about 1 minute 15 seconds)

| On screen | Say |
|---|---|
| Open `experiments\sieve_sim.py`. Show the top of the file and `make_trace` (around line 20). | "The script first builds Zipf traces. Each trace has one million requests drawn from a set of 100,000 objects. A higher alpha means a few objects get most of the requests." |
| Scroll to `fifo` (line 30) and `lru` (line 45). | "FIFO evicts the oldest object and does nothing on a hit. LRU moves an object to the front on every hit, which is the step that needs a lock in a real server." |
| Scroll to `clock` (line 59). Point to the line `q.appendleft(o)`. | "CLOCK gives each object a visited bit. When it finds a visited object, it clears the bit and moves the object back to the front." |
| Scroll to `sieve` (line 83). Highlight the `while vis[o]:` loop at line 98. | "This loop is SIEVE's eviction. The hand starts where it stopped last time. If the object has its visited bit set, the hand clears it and moves toward the head. The first object with the bit at zero is evicted. Unlike CLOCK, SIEVE never moves the object that survives. That is the whole difference, and it is what lowers the miss ratio." |
| Scroll to `best_possible` (line 125). | "We also compute a best possible cache that always holds the most requested objects. No algorithm can beat it, so it checks our results." |

## Scene 3. Run the experiment (about 45 seconds)

| On screen | Say |
|---|---|
| Switch to the terminal. Type `python experiments\sieve_sim.py` and press Enter. | "Now we run all four algorithms at five cache sizes and nine values of alpha." |
| Wait while the "done alpha" lines appear. | "Each line is one alpha value finishing. The whole run takes about 15 seconds on a laptop." |
| When "total seconds" prints, stop and let it show for a second. | "The results are saved to results.json." |

## Scene 4. Make the figures (about 30 seconds)

| On screen | Say |
|---|---|
| Type `python experiments\make_figures.py` and press Enter. | "This script reads the results and draws our three figures." |
| Point to the reduction table and then the alpha 1.0 miss ratio table. | "The first table shows how many fewer misses SIEVE has than FIFO. At alpha 1.0 it removes about 21 to 26 percent of FIFO's misses. The second table shows that at a 1% cache, SIEVE's miss ratio is 0.419, against 0.502 for CLOCK, 0.513 for LRU and 0.555 for FIFO." |

## Scene 5. Compare with the paper (about 1 minute 30 seconds)

Put each paper figure on the left and ours on the right.

| On screen | Say |
|---|---|
| `paper_fig8a_miss_ratio_vs_size.png` beside `fig_miss_ratio_vs_size.png`. | "This pair shows miss ratio against cache size at alpha 1.0. Both show SIEVE below LRU at every size. The paper's axis runs to 80% of the working set and compares against ARC and LFU. Ours stops at 10% and compares against FIFO and CLOCK, so the shapes look different, but the order of the algorithms is the same." |
| `paper_fig9a_miss_ratio_vs_skew.png` beside `fig_miss_ratio_vs_skew.png`. | "This pair varies the skew. In both, miss ratio falls as alpha rises and SIEVE is lowest everywhere. Our values are higher because we used a 1% cache and the paper used its large cache. At alpha 1.2 and above, SIEVE is within 0.01 of the best possible cache." |
| `paper_fig11_instructions_and_miss_ratio.png` beside `fig_reduction_vs_fifo.png`. | "The paper prints miss ratios above these bars at a 0.1% and a 10% cache, the same sizes we used. Converted to fewer misses than FIFO, the paper gets 12, 22 and 32 percent at the small cache, and we get 11, 21 and 30. At the large cache the paper gets 22, 28 and 33, and we get 19, 26 and 30. Every value is within 3 points." |

## Scene 6. Why the numbers differ (about 30 seconds)

| On screen | Say |
|---|---|
| Open `docs\Group1_SIEVE_report.pdf` at the "Why our numbers differ from the paper" section. | "Our numbers differ a little for clear reasons. The paper's main results use 1,559 real traces, and we used generated Zipf traces. Our traces are smaller: one million requests over 100,000 objects, against 100 million over one million in the paper. We compared with different algorithms and a smaller range of cache sizes. We did not test throughput, because Python cannot measure multi thread speed fairly." |

## Scene 7. The authors' simulator (optional, about 45 seconds)

Your WSL Ubuntu already has the authors' repo built at `~/NSDI24-SIEVE` and a Python environment at `~/venvs/sieve`. Run this in the Ubuntu terminal:

```bash
source ~/venvs/sieve/bin/activate
cd ~/NSDI24-SIEVE
python3 libCacheSim/scripts/plot_mrc_size.py --tracepath mydata/zipf/zipf_1.0 --trace-format txt --algos=fifo,lru,clock,sieve
```

| On screen | Say |
|---|---|
| Run the commands above in the Ubuntu terminal. | "We also ran the authors' own simulator, libCacheSim, on Linux. Before it would build, we had to install the zstd development package and fix a wrong include path in one source file." |
| Open the PDF it writes (or `zipf_1.0.pdf` at the repo root). | "Its result agrees with ours. On the authors' sample Zipf trace, SIEVE has the lowest miss ratio of FIFO, LRU, CLOCK and SIEVE at every cache size above one object. At 100 objects it misses 33% of requests, against 41% for CLOCK, 42% for LRU and 48% for FIFO." |

If you skip the live run, show `zipf_1.0.pdf` from the repo root and say: "We ran the authors' simulator on Linux earlier. This is its output on their sample Zipf trace, and SIEVE has the lowest miss ratio of the four here too."

## Scene 8. Close (about 15 seconds)

| On screen | Say |
|---|---|
| Back to the README on GitHub. | "In every run we made, SIEVE had the lowest miss ratio of the four algorithms, and our results are within 3 points of the paper's. Everything shown here is in our GitHub repository. Thank you." |

## After recording

1. Game Bar saves to `C:\Users\ohimo\Videos\Captures`. OBS saves where you set it.
2. Check the video is 3 to 6 minutes long and the terminal text is readable.
3. Rename it `Group1_SIEVE_video.mp4`.
