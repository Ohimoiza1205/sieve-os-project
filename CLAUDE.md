# SIEVE OS class project: handoff and plan

This file is the full context for the project. Read it before doing anything. It was written after the
slides were finished and submitted, so the remaining work is the final package: report, video and repo.

## 1. What this project is

Operating Systems group project at Texas Tech University, Fall 2026. The assignment is to pick a recent
OS research paper, run its method, compare our figures with the paper's figures, and explain the differences.
The paper we picked:

Y. Zhang, J. Yang, Y. Yue, Y. Vigfusson, and K. V. Rashmi, "SIEVE is Simpler than LRU: an Efficient
Turn-Key Eviction Algorithm for Web Caches," 21st USENIX Symposium on Networked Systems Design and
Implementation (NSDI 24), Santa Clara, CA, April 2024, pages 1229 to 1246. USENIX Association.
Authors' code: https://github.com/Thesys-lab/NSDI24-SIEVE
Our repo (a fork of the authors' repo): https://github.com/Ohimoiza1205/sieve-os-project
A copy of the paper is in this folder: nsdi24-zhang-yazhuo-SIEVE.pdf

SIEVE is a cache eviction policy. In class terms it belongs with FIFO, LRU and CLOCK under memory
management. We describe it as a cache replacement policy, not as virtual memory page replacement.

## 2. Team (Group 1)

| Name | Email | Role so far |
|---|---|---|
| Umar Afolami | kafolami@ttu.edu | repo setup, Zipf runs |
| Kachi Okoye | onokoye@ttu.edu | workload comparisons, original figures |
| Ohi Moiza | omoiza@ttu.edu | lead, simulator build, experiments, slides |
| Ufanabasi Ekeng | uekeng@ttu.edu | algorithm diagram and method explanation |
| Amaan Abdul Rahman | amaarahm@ttu.edu | report lead, results documentation |

R numbers are needed for the report. Ask Ohi for them. Do not invent them.
The contribution section of the report must be specific per person. Ask Ohi to confirm or adjust the
roles above before the report is final.

## 3. Course requirements that still apply

Final package, due Tuesday 12/1/2026, 11:59 pm, on Canvas. It must contain:
1. The original paper (the PDF in this folder).
2. The final report, following the course template exactly. Template sections, in order:
   - Project Report (title)
   - Group Member and Contribution (names, emails, R numbers, detailed contribution per person)
   - Problem Statement (background and applications, own words, figures allowed)
   - Problem Solution (own words)
   - Simulation Result (our figures beside the original figures, at least 3 pairs, describe and explain
     each, give reasons for differences)
   - Conclusion (own words)
   - References: [1] the GitHub link, [2] the paper in standard journal format
3. A video showing how we run our code and generate our results.

The instructor's rules: do not copy text from the paper, use our own words. Explaining why results
differ is a graded part. State clearly what each member contributed. The presentation happens in class
during the last two weeks of the semester, using the slides already on Canvas (no changes allowed).

## 4. What is already done

- Slides submitted on Canvas 11/6. File: Group1_SIEVE_slides.pptx in this folder. 15 slides. Speaker notes
  are in the file. Slide order: title, background (2 slides), problem statement, novelty, method (2 slides),
  what the paper reports, how we reproduced, three result slides (pairs with paper Figures 8a, 9a and 11),
  why our numbers differ, conclusion, references.
- The authors' simulator (libCacheSim) builds on Linux after two fixes, both already in our repo:
  install libzstd-dev (the authors' install script skips it) and a wrong include path in
  libCacheSim/libCacheSim/cache/eviction/other/S3LRU.c. The first Zipf run output is zipf_1.0.pdf at the repo root.
- Independent Python re-implementation of FIFO, LRU, CLOCK and SIEVE: experiments/sieve_sim.py. It
  produces the numbers on the slides to within 0.002 miss ratio. experiments/make_figures.py turns its
  output into the three report figures. Both run on Windows with plain Python, numpy and matplotlib.
  This is the code the video must show.

## 5. Numbers that must stay consistent everywhere

Setup: a set of 100,000 objects, 1,000,000 requests, Zipf traces, alpha 0.6 to 1.4, cache size 0.1% to
10% of the unique objects that appear in each trace, every object has size 1. Run time about 15 seconds.
A best possible cache (always holds the most requested objects) is a sanity bound; no algorithm beats it.

Our results (alpha 1.0): SIEVE has the lowest miss ratio at every cache size. At 1% cache, SIEVE 0.419,
CLOCK 0.503, LRU 0.514, FIFO 0.556. Percent fewer misses than FIFO:

| alpha | 0.1% | 0.5% | 1% | 5% | 10% |
|---|---|---|---|---|---|
| 0.8 | 11 | 14 | 15 | 18 | 19 |
| 1.0 | 21 | 24 | 25 | 25 | 26 |
| 1.2 | 30 | 33 | 33 | 32 | 30 |

Paper figures we pair with (crops are in paper_figures/):
- Figure 8a: miss ratio vs cache size, Zipf alpha 1.0, LRU, ARC, LFU, SIEVE, cache up to 80% of working set.
- Figure 9a: miss ratio vs Zipf alpha 0.2 to 1.6, large cache, LRU, ARC, LFU, SIEVE.
- Figure 11: instructions per request for LRU, FIFO, SIEVE at alpha 0.8, 1.0, 1.2, with the miss ratio
  printed above each bar. Large cache = 10% of unique objects, small cache = 0.1%. Same endpoints as ours.
  Paper miss ratios (LRU, FIFO, SIEVE): small cache 0.90/0.91/0.80, 0.60/0.63/0.49, 0.25/0.28/0.19;
  large cache 0.51/0.55/0.43, 0.22/0.25/0.18, 0.05/0.06/0.04.
  Paper reduction vs FIFO: small cache 12%, 22%, 32%; large cache 22%, 28%, 33%.
  Ours: 0.1% cache 11%, 21%, 30%; 10% cache 19%, 26%, 30%. Within 3 points.

Paper headline facts (verified against the paper text): 1,559 traces from 7 sources; SIEVE has the lowest
miss ratio on more than 45% of traces, runner up TwoQ on 15%; up to 63.2% lower miss ratio than ARC
(mean 1.5%); more than 2x the throughput of optimized LRU at 16 threads on the Meta trace; Table 3
lines of code: LRU 12, SIEVE 16, CLOCK 16, ARC 192, CACHEUS 458; fewer than 20 lines changed on average
in five production libraries; Section 7.2: SIEVE is not scan resistant and can lose to LRU on block
cache workloads with scans.

Why our numbers differ from the paper (use these, they are accurate):
1. The paper's headline numbers come from 1,559 real traces. We ran generated Zipf traces, so we only
   compare with the paper's own Zipf figures (8, 9, 11).
2. The paper's Zipf figures compare SIEVE with LRU, ARC and LFU. We compared with FIFO, LRU and CLOCK.
3. Our traces were generated with our own random seed, so values shift by a point or two.
4. Cache size range differs: Figure 8a runs to 80% of the working set, ours stops at 10%.
5. We did not run the throughput test. Python cannot measure multi thread speed fairly.

## 6. Writing rules for everything produced (report, README, video script, messages)

- Plain declarative sentences. No filler, no hedging, no marketing tone.
- No em dashes. No hyphens in prose (write "multi thread", "scan resistant", "16 thread"). The paper
  title "Turn-Key" stays as the paper wrote it inside the reference only.
- Never use repetitive parallel phrasing like "one queue, one bit, one hand" or "no locks, no lists".
  Write it as a normal sentence instead.
- Do not copy sentences from the paper. Paraphrase in our own words and cite the paper as [2].
- Metrics first: lead with the number, then the explanation.
- No emojis, no icons, no decorative colour in documents. Black text, white page, standard fonts.

## 7. Plan: what to do, in order

### Step 1. Put the experiment code in the repo and make it run
```
cd C:\Users\ohimo\sieve-os-project
mkdir experiments
copy <handoff>\experiments\sieve_sim.py experiments\
copy <handoff>\experiments\make_figures.py experiments\
pip install numpy matplotlib
python experiments\sieve_sim.py
python experiments\make_figures.py
```
Expected: sieve_sim.py prints "done alpha ..." lines and "total seconds" around 15 to 30 on a laptop.
make_figures.py prints a table of reductions (first row about 11, 14, 15, 18, 19) and writes three PNGs
plus summary.txt to experiments\figures\. Commit them. Do not commit __pycache__.

### Step 2. Rewrite the repo README so it describes our project, not the authors'
Keep the authors' build instructions in a section, add at the top: project title, course, team, what we
changed (the two build fixes), how to run experiments\sieve_sim.py and make_figures.py, where the figures
land, and a link to the paper. Keep the authors' license and reference block. Credit the original repo.

### Step 3. Write the final report as a .docx from the course template
Use Report_Template_2.docx as the base so headings match. Target 6 to 10 pages. Content per section:

- Title: Reproducing SIEVE: a simpler cache eviction algorithm (or similar, Ohi decides).
- Group Member and Contribution: table with name, email, R number, then 2 to 4 specific lines per
  person. Get the final wording from Ohi.
- Problem Statement: what a cache is, hit, miss, miss ratio, why eviction matters, FIFO and LRU and
  their costs (LRU needs a lock on every hit), why complex algorithms (ARC, LIRS, CACHEUS) are rarely
  adopted, the research question. One figure is fine: a simple cache diagram or the lines of code chart
  (data from Table 3). Applications: CDNs, key value caches, DNS caches.
- Problem Solution: SIEVE mechanics. A FIFO queue, a visited bit per object, a hand pointer. Hit sets the
  bit. Miss inserts at the head. Eviction: the hand walks toward the head, clears bits that are 1, evicts
  the first object with bit 0, stays where it stopped. Lazy promotion and quick demotion. The difference
  from CLOCK (CLOCK moves survivors to the front, SIEVE leaves them in place). Include the worked example
  from slide 7: cache A B C D E, hand at E (visited 1), new object F misses, hand clears E and D, evicts C,
  F enters at the head, hand rests on B.
- Simulation Result: describe our setup (Section 5 above). Then three pairs, each as paper figure on the
  left and our figure on the right, with a caption and 1 to 2 paragraphs: what the figure shows, what
  matches, what differs and why. Pairs: Figure 8a with fig_miss_ratio_vs_size.png, Figure 9a with
  fig_miss_ratio_vs_skew.png, Figure 11 with fig_reduction_vs_fifo.png. Then a short subsection
  "Why the numbers differ" using the five reasons in Section 5. Also mention the two build bugs we fixed
  in the authors' code, because the instructor said published code is often buggy.
- Conclusion: what we learned, in our words. SIEVE is simpler than LRU and had the lowest miss ratio in
  every run. Our Zipf results are within 3 points of the paper's. Limit: not scan resistant.
- References: [1] https://github.com/Ohimoiza1205/sieve-os-project (and the authors' repo as [3] if
  wanted), [2] the paper in the exact format in Section 1 of this file.

Figure captions cite the paper for the left panel ("Figure from Zhang et al. [2], Figure 8a").
Read the whole report once at the end against the rules in Section 6. Then export a PDF too.

### Step 4. Video (3 to 6 minutes, screen recording with voice)
Record with Windows Game Bar (Win+G), OBS, or PowerPoint's screen recorder. Script:
1. Show the repo in the file explorer and the README. Say what the project is in two sentences.
2. Open experiments\sieve_sim.py, scroll through the four policies, point to the SIEVE eviction loop.
3. Run python experiments\sieve_sim.py in a terminal. Let it finish (about 15 to 30 seconds).
4. Run python experiments\make_figures.py. Show the printed table.
5. Open the three PNGs in experiments\figures. For each, hold the paper figure beside it and say what
   matches and what differs.
6. Optional, if WSL or a Linux machine is available: show the authors' simulator run
   python3 libCacheSim/scripts/plot_mrc_size.py --tracepath mydata/zipf/zipf_1.0 --trace-format txt --algos=fifo,lru,clock,sieve
   and the zipf_1.0.pdf it makes. If not available, say the first Zipf run was done on Linux and show zipf_1.0.pdf.
Export as MP4. Name it Group1_SIEVE_video.mp4.

### Step 5. Package and submit
Folder Group1_SIEVE_final with: nsdi24-zhang-yazhuo-SIEVE.pdf, Group1_SIEVE_report.docx (and PDF),
Group1_SIEVE_video.mp4. Zip it. One member uploads once before 12/1 11:59 pm.

### Step 6. Presentation prep (in parallel)
Speaker split used in the notes: Umar slides 1 to 3, Kachi 4 and 5, Ufanabasi 6 to 8, Ohi 9 to 12,
Amaan 13 and 14 plus Q&A. 8 minutes talk, 2 minutes questions. Rehearse once with a timer. Likely
questions: why not scan resistant, how is it different from CLOCK, why Zipf, why no throughput test.

## 8. Things only Ohi can answer (ask, do not guess)
- R numbers for all five members.
- Final contribution wording per person.
- Whether the presentation date is known.
- Whether a teammate has a different Python script from the one in experiments/. If so, keep whichever
  one the video will show and make sure the report figures come from that script.

## 9. Environment notes
- Ohi works on Windows (Git Bash and cmd). The Python experiment runs there directly.
- libCacheSim is Linux only. Use WSL or a lab machine if it must be shown live.
- Claude Code CLI is started from C:\Users\ohimo\sieve-os-project with permissions skipped. This file
  sits at the repo root so Claude Code reads it automatically. Commit it.
