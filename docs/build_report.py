"""Build docs/Group1_SIEVE_report.docx from docs/Report_Template_2.docx.

Usage:  python docs/build_report.py
Needs:  pip install python-docx matplotlib
Reads the figures in experiments/figures and paper_figures, draws the lines of code chart,
and writes the report next to this file. Headings use the same formatting as the template.
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUR = os.path.join(ROOT, "experiments", "figures")
PAPER = os.path.join(ROOT, "paper_figures")
EXTRA = os.path.join(HERE, "report_figures")
os.makedirs(EXTRA, exist_ok=True)

# ---------------------------------------------------------------- lines of code chart (Table 3 of [2])
loc_png = os.path.join(EXTRA, "fig_lines_of_code.png")
fig, ax = plt.subplots(figsize=(6.0, 2.6), dpi=200)
names = ["LRU", "SIEVE", "CLOCK", "ARC", "CACHEUS"]
vals = [12, 16, 16, 192, 458]
bars = ax.barh(names[::-1], vals[::-1], color="#595959")
for b, v in zip(bars, vals[::-1]):
    ax.text(v + 6, b.get_y() + b.get_height() / 2, str(v), va="center", fontsize=9)
ax.set_xlabel("Lines of code in the simulator")
ax.set_xlim(0, 520)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(loc_png)
plt.close(fig)

# ---------------------------------------------------------------- document helpers
doc = Document(os.path.join(HERE, "Report_Template_2.docx"))
body = doc.element.body
for el in list(body):
    if el.tag != qn("w:sectPr"):
        body.remove(el)


def para(text="", size=None, bold=False, italic=False, align=None, space_after=6):
    p = doc.add_paragraph()
    if text:
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        if size:
            r.font.size = Pt(size)
    if align:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    return p


def rich(parts, space_after=6):
    """parts: list of (text, bold) pairs in one paragraph."""
    p = doc.add_paragraph()
    for text, bold in parts:
        p.add_run(text).bold = bold
    p.paragraph_format.space_after = Pt(space_after)
    return p


def heading(text):
    # Same look as the template: Normal style, 14 pt, not bold.
    para("", space_after=0)
    p = para(text, size=14, space_after=6)
    p.paragraph_format.keep_with_next = True
    return p


def subheading(text):
    p = para(text, size=12, bold=True, space_after=4)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(6)
    return p


def borders(table, on=True):
    tblPr = table._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single" if on else "nil")
        if on:
            e.set(qn("w:sz"), "4")
            e.set(qn("w:color"), "000000")
        b.append(e)
    tblPr.append(b)


def table(rows, widths, header=True, size=10):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    borders(t)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j)
            c.width = Inches(widths[j])
            p = c.paragraphs[0]
            r = p.add_run(str(val))
            r.font.size = Pt(size)
            r.bold = header and i == 0
            p.paragraph_format.space_after = Pt(0)
    para("", space_after=2)
    return t


def caption(text):
    p = para(text, size=10, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    return p


def pair(left, right, cap, left_label, right_label):
    t = doc.add_table(rows=2, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    borders(t, on=False)
    for j, (img, lab) in enumerate(((left, left_label), (right, right_label))):
        c = t.cell(0, j)
        c.width = Inches(3.2)
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(img, width=Inches(3.1))
        q = t.cell(1, j).paragraphs[0]
        q.alignment = WD_ALIGN_PARAGRAPH.CENTER
        q.add_run(lab).font.size = Pt(9)
    caption(cap)


def single(img, width, cap):
    p = para(align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p.add_run().add_picture(img, width=Inches(width))
    caption(cap)


# ---------------------------------------------------------------- title
para("Project Report", size=16, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
para("Reproducing SIEVE: A Simpler Cache Eviction Algorithm", size=16,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
para("Group 1, Operating Systems, Texas Tech University, Fall 2026", size=11,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

# ---------------------------------------------------------------- group members
heading("Group Member and Contribution")
table([
    ["Name", "Email", "R number"],
    ["Ohi Moiza", "omoiza@ttu.edu", "R11882109"],
    ["Umar Afolami", "kafolami@ttu.edu", "R11973636"],
    ["Kachi Okoye", "onokoye@ttu.edu", "R11878948"],
    ["Ufanabasi Ekeng", "uekeng@ttu.edu", "R11908634"],
    ["Amaan Abdul Rahman", "amaarahm@ttu.edu", "R11969159"],
], widths=[2.0, 2.2, 1.6])

CONTRIB = [
    ("Ohi Moiza (group lead)",
     "Organized the group and set the schedule. Built the authors' libCacheSim simulator on Linux and "
     "fixed the two build errors described in the Simulation Result section. Wrote the Python simulator "
     "and the figure script, ran the experiments and prepared the presentation slides."),
    ("Umar Afolami",
     "Set up our fork of the authors' repository. Ran the Zipf experiments in libCacheSim and recorded "
     "the first Zipf result."),
    ("Kachi Okoye",
     "Compared results across workloads and cache sizes. Produced our original figures and checked each "
     "one against the matching paper figure."),
    ("Ufanabasi Ekeng",
     "Drew the SIEVE algorithm diagram and the eviction example. Wrote the explanation of how SIEVE "
     "works and how it differs from CLOCK."),
    ("Amaan Abdul Rahman (report lead)",
     "Led the writing of this report. Documented the results and the reasons our numbers differ from "
     "the paper."),
]
for name, text in CONTRIB:
    rich([(name + ": ", True), (text, False)])

# ---------------------------------------------------------------- problem statement
heading("Problem Statement")
para("A cache is a small, fast store that holds copies of data whose original copy lives somewhere "
     "slower. When a request finds its object in the cache, the request is a hit. When it does not, the "
     "request is a miss, and the system has to fetch the object from the slower source, such as a disk, "
     "a database or a distant origin server. The miss ratio is the number of misses divided by the number "
     "of requests. A lower miss ratio means less load on the backend and shorter response times for users.")
para("A cache has a fixed capacity. When it is full and a new object has to be stored, the cache must "
     "remove an object it already holds. The rule that chooses this object is the eviction algorithm, "
     "also called the replacement policy. In this course the same problem appears under memory management, "
     "where FIFO, LRU and CLOCK decide which item to replace. A good eviction algorithm keeps the objects "
     "that will be requested again soon and removes the objects that will not.")
para("FIFO removes the object that entered the cache first. It is cheap because a hit changes nothing, "
     "but it ignores popularity, so a popular object is still evicted when it reaches the end of the queue. "
     "LRU removes the object that has gone the longest without a request. It protects popular objects "
     "better than FIFO, but every hit moves the object to the front of a shared list. In a server with "
     "many threads, each hit must take a lock on that list, and the lock limits how many requests per "
     "second the cache can serve.")
para("Researchers have proposed many algorithms with lower miss ratios than LRU, including ARC, LIRS and "
     "CACHEUS. These designs keep several lists, ghost entries for objects already evicted, or parameters "
     "that adapt during the run. Table 3 of the paper counts the lines of code each policy needs in the "
     "same simulator [2]. LRU needs 12 lines, SIEVE and CLOCK need 16, ARC needs 192 and CACHEUS needs 458. "
     "Figure 1 shows these counts. Longer code is harder to test, debug and tune, so most production "
     "caches still run LRU or a FIFO variant.")
single(loc_png, 5.0, "Figure 1. Lines of code for five eviction algorithms. Data from Zhang et al. [2], "
                     "Table 3. Chart drawn by our group.")
para("Eviction matters wherever a cache sits in front of slower storage. Content delivery networks keep "
     "images and videos on servers close to users. Key value caches such as Memcached and Redis hold "
     "database results for web applications. DNS resolvers keep recent name lookups, and operating systems "
     "keep file blocks in memory. In each of these systems, a few percent fewer misses removes a large "
     "amount of backend traffic over millions of requests.")
para("The paper asks whether an eviction algorithm can be as simple as LRU while matching or beating the "
     "miss ratio of the complex algorithms and scaling better with threads [2]. Our project asks a narrower "
     "question. When we implement SIEVE ourselves and run it on generated Zipf workloads, do we see the "
     "same improvement over FIFO and LRU that the paper reports?")

# ---------------------------------------------------------------- problem solution
heading("Problem Solution")
para("SIEVE stores cached objects in a single FIFO queue. New objects enter at the head and older objects "
     "sit toward the tail. Each object carries a visited bit. The algorithm also keeps a pointer called the "
     "hand, which marks where the next search for an object to evict begins.")
para("On a hit, SIEVE sets the visited bit of the object to 1. The object does not move, so a hit does "
     "not change the queue and needs no lock on it. On a miss, the new object is inserted at the head with "
     "its visited bit set to 0. If the cache is full, SIEVE evicts an object first. The hand starts where it "
     "stopped after the previous eviction, or at the tail if there was none. If the object under the hand "
     "has its visited bit set to 1, the hand clears the bit and moves one step toward the head. If the bit "
     "is 0, that object is evicted. The hand then rests at the next object toward the head, and the next "
     "eviction continues from there. When the hand passes the head, it returns to the tail.")
para("The paper explains why this works with two ideas, which it calls lazy promotion and quick demotion "
     "[2]. Lazy promotion means that a hit does not move an object right away. The object is only kept, by "
     "having its bit cleared, when the hand reaches it. This costs far less than moving the object on every "
     "hit, which is what LRU does. Quick demotion means that a new object which is never requested again "
     "leaves the cache soon after it arrives. Web traces contain many objects that are requested only once, "
     "so removing them early leaves more space for popular objects.")
para("CLOCK, which is also called FIFO with reinsertion, uses the same visited bit. The difference is what "
     "happens to an object that survives. CLOCK clears the bit and moves the object back to the head of the "
     "queue. SIEVE clears the bit and leaves the object where it is. Because of this, old survivors stay "
     "behind the hand and are only examined again after the hand wraps around. New objects sit between the "
     "hand and the head, so the hand reaches them on its current pass and removes the ones that were not "
     "requested. In CLOCK the reinserted old objects are mixed in with the new ones at the head, so a new "
     "unpopular object waits longer before it can be evicted. This one change is what gives SIEVE its "
     "lower miss ratio.")
subheading("Worked example")
para("Table 1 follows one eviction. The queue is listed from head to tail and the visited bit is shown in "
     "brackets. The cache holds five objects and is full when object F is requested.")
table([
    ["Step", "Queue, head to tail", "Hand", "What happens"],
    ["1", "A(0) B(1) C(0) D(1) E(1)", "E", "F misses. The cache is full, so SIEVE must evict."],
    ["2", "A(0) B(1) C(0) D(0) E(0)", "C", "E and D have bit 1. The hand clears both and stops at C, "
                                         "which has bit 0. C is evicted."],
    ["3", "F(0) A(0) B(1) D(0) E(0)", "B", "F enters at the head with bit 0. The hand rests on B."],
], widths=[0.5, 2.1, 0.6, 3.3])
caption("Table 1. One SIEVE eviction, as shown on slide 7 of our presentation.")
para("E and D kept their positions in the queue. LRU would have moved them when they were hit, and CLOCK "
     "would have moved them to the head during the search. If no further hits arrive, the next eviction "
     "starts at B, clears its bit and evicts A.")

# ---------------------------------------------------------------- simulation result
heading("Simulation Result")
subheading("Setup")
para("We wrote an independent simulator in Python that implements FIFO, LRU, CLOCK and SIEVE "
     "(experiments/sieve_sim.py in [1]). Each trace has 100,000 unique objects and 1,000,000 requests drawn "
     "from a Zipf distribution, where the object of rank i is requested with probability proportional to "
     "1/i^alpha. A larger alpha means a few objects receive most of the requests. We ran alpha from 0.6 to "
     "1.4 and cache sizes of 0.1%, 0.5%, 1%, 5% and 10% of the unique objects that appear in each trace. "
     "Every object has size 1. The random seed for each trace is fixed, so a second run gives the same "
     "numbers. The simulator also computes a best possible cache, which always holds the most requested "
     "objects. No algorithm can beat it, so it serves as a check on the other results. The full run takes "
     "14 seconds on a laptop. A second script, experiments/make_figures.py, draws the figures below.")
para("We also built the authors' simulator, libCacheSim, on Linux and ran it on the sample Zipf trace "
     "included in their repository [3]. The output is zipf_1.0.pdf in [1].")
para("Table 2 lists our miss ratios at alpha 1.0. SIEVE has the lowest miss ratio at every cache size. At a "
     "1% cache, SIEVE misses on 41.9% of requests, against 50.2% for CLOCK, 51.3% for LRU and 55.5% for FIFO.")
table([
    ["Algorithm", "0.1%", "0.5%", "1%", "5%", "10%"],
    ["FIFO", "0.768", "0.621", "0.555", "0.396", "0.323"],
    ["LRU", "0.729", "0.579", "0.513", "0.356", "0.286"],
    ["CLOCK", "0.716", "0.567", "0.502", "0.347", "0.278"],
    ["SIEVE", "0.607", "0.472", "0.419", "0.295", "0.240"],
    ["Best possible", "0.587", "0.453", "0.397", "0.264", "0.204"],
], widths=[1.4, 0.9, 0.9, 0.9, 0.9, 0.9])
caption("Table 2. Our miss ratios at Zipf alpha 1.0 by cache size (share of unique objects).")

# Pair 1
subheading("Pair 1: miss ratio against cache size")
pair(os.path.join(PAPER, "paper_fig8a_miss_ratio_vs_size.png"),
     os.path.join(OUR, "fig_miss_ratio_vs_size.png"),
     "Figure 2. Miss ratio against cache size at Zipf alpha 1.0. Left: figure from Zhang et al. [2], "
     "Figure 8a. Right: our result.",
     "Paper, Figure 8a", "Ours")
para("At a 10% cache our SIEVE miss ratio is 0.240 and our LRU miss ratio is 0.286. In Figure 8a at the "
     "same size, read from the plot, SIEVE is close to 0.25 and LRU is close to 0.32. Both figures agree on "
     "the main result. Miss ratio falls as the cache grows, and SIEVE stays below LRU at every size. In our "
     "run SIEVE is also below CLOCK and FIFO at every size, and it comes within 0.04 of the best possible "
     "cache at every size.")
para("The two plots look different for three reasons. First, the paper draws cache size on a linear axis "
     "from 0% to 80% of the working set, while our axis covers 0.1% to 10% with equal spacing between the "
     "five sizes. The part of the curve that fills our whole plot is squeezed into the left eighth of the "
     "paper's plot. Second, the paper compares SIEVE with ARC and LFU, which have miss ratios close to "
     "SIEVE. We compared with FIFO and CLOCK, which are simpler and sit well above SIEVE. CLOCK is only "
     "slightly better than LRU in our run (0.502 against 0.513 at 1%), which shows that the visited bit "
     "alone is not enough and that keeping survivors in place is what helps. Third, our gap between SIEVE "
     "and LRU at 10% is 0.046, while the paper's is about 0.07. Our trace is shorter and has fewer objects "
     "than the paper's, as explained in Pair 3, and we read the paper's values from the plot by eye.")

# Pair 2
subheading("Pair 2: miss ratio against popularity skew")
pair(os.path.join(PAPER, "paper_fig9a_miss_ratio_vs_skew.png"),
     os.path.join(OUR, "fig_miss_ratio_vs_skew.png"),
     "Figure 3. Miss ratio against Zipf alpha. Left: figure from Zhang et al. [2], Figure 9a, large cache. "
     "Right: our result with a cache of 1% of the unique objects.",
     "Paper, Figure 9a", "Ours")
para("At alpha 0.8 our SIEVE miss ratio is 0.698, against 0.799 for LRU and 0.824 for FIFO. At alpha 1.4 "
     "SIEVE is 0.098, against 0.131 for LRU. Both figures show the same shape. Miss ratio drops as alpha "
     "rises, because a more skewed workload sends more of its requests to a small set of objects that "
     "stay in the cache. SIEVE has the lowest miss ratio of the tested algorithms at every alpha in both "
     "figures. In both figures the absolute gap between SIEVE and LRU is widest in the middle of the range "
     "and narrows when alpha is high, because at high skew every algorithm keeps the few hot objects. Our "
     "plot also shows that SIEVE moves closer to the best possible cache as skew rises. At alpha 1.2 and "
     "above, SIEVE is within 0.01 of it.")
para("Our miss ratios are higher than the paper's at every alpha. At alpha 1.0 the paper shows SIEVE near "
     "0.25, while ours is 0.419. The main reason is cache size. The paper's Figure 9a uses its large cache, "
     "and we used a 1% cache, which is ten times smaller than our own large size. Our 10% run at alpha 1.0 "
     "gives 0.240 for SIEVE, which is close to the paper's value. The ranges also differ. The paper runs "
     "alpha from 0.2 to 1.6, and we ran 0.6 to 1.4. The paper's baselines are LRU, ARC and LFU, and ours "
     "are FIFO and LRU plus the best possible line.")

# Pair 3
subheading("Pair 3: improvement over FIFO at a small and a large cache")
pair(os.path.join(PAPER, "paper_fig11_instructions_and_miss_ratio.png"),
     os.path.join(OUR, "fig_reduction_vs_fifo.png"),
     "Figure 4. Left: figure from Zhang et al. [2], Figure 11, instructions per request with the miss "
     "ratio printed above each bar, large cache (a) and small cache (b). Right: our result, percent fewer "
     "misses for SIEVE than FIFO at five cache sizes.",
     "Paper, Figure 11", "Ours")
para("Figure 11 in the paper measures CPU instructions per request and prints the miss ratio of LRU, FIFO "
     "and SIEVE above each bar. Its small cache is 0.1% and its large cache is 10% of the unique objects, "
     "the same two endpoints we used. We did not count instructions, so we compare the printed miss ratios. "
     "We converted them to the percent of FIFO misses that SIEVE removes. Table 3 puts the paper's values "
     "beside ours.")
table([
    ["Cache", "Alpha", "Paper miss ratio (LRU, FIFO, SIEVE)", "Paper reduction", "Our reduction"],
    ["0.1%", "0.8", "0.90, 0.91, 0.80", "12%", "11%"],
    ["0.1%", "1.0", "0.60, 0.63, 0.49", "22%", "21%"],
    ["0.1%", "1.2", "0.25, 0.28, 0.19", "32%", "30%"],
    ["10%", "0.8", "0.51, 0.55, 0.43", "22%", "19%"],
    ["10%", "1.0", "0.22, 0.25, 0.18", "28%", "26%"],
    ["10%", "1.2", "0.05, 0.06, 0.04", "33%", "30%"],
], widths=[0.6, 0.6, 2.4, 1.2, 1.2])
caption("Table 3. SIEVE miss reduction compared with FIFO, from the paper's Figure 11 and from our run.")
para("Every one of our six reductions is within 3 percentage points of the paper's. Both sets grow with "
     "alpha, from about 11% at alpha 0.8 to about 30% at alpha 1.2 at the small cache. Our values are "
     "slightly lower in all six cases. In our run SIEVE also has fewer misses than LRU and CLOCK at all 15 "
     "combinations of alpha and cache size.")
para("Our absolute miss ratios are higher than the paper's. At a 10% cache and alpha 1.0, our SIEVE miss "
     "ratio is 0.240 and the paper's is 0.18. The paper states that this experiment used 100 million "
     "requests over 1 million objects [2]. Our traces have 1 million requests over 100,000 objects, so each "
     "object is requested 10 times on average in our trace and 100 times in theirs. The first request to "
     "any object is always a miss, and those cold misses make up a larger share of our shorter trace. Our "
     "0.1% cache also holds only 100 objects, while the paper's holds 1,000. Because these effects raise "
     "the miss ratio of FIFO and SIEVE together, the percent reduction is less affected than the raw miss "
     "ratio, which is why Table 3 compares reductions.")
para("The paper's main point in Figure 11 is that SIEVE executes fewer instructions per request than LRU, "
     "because a hit only sets a bit instead of moving the object. We did not reproduce that measurement. "
     "Instruction counts from a Python program mostly reflect the interpreter, not the algorithm.")

subheading("Why our numbers differ from the paper")
for t in [
    "1. Workloads. The paper's headline results come from 1,559 real traces from 7 sources. We ran "
    "generated Zipf traces only, so we compare our figures with the paper's own Zipf figures (8a, 9a and 11) "
    "and not with its real trace results.",
    "2. Baselines. The paper's Zipf figures compare SIEVE with LRU, ARC and LFU. We compared it with FIFO, "
    "LRU and CLOCK, which are the policies covered in this course.",
    "3. Random seed and trace size. Our traces were generated with our own seed and are smaller than the "
    "paper's (1 million requests over 100,000 objects, against 100 million over 1 million for Figure 11). "
    "This shifts the miss ratios by a few points.",
    "4. Cache size range. Figure 8a runs to 80% of the working set. Our runs stop at 10%. Our Figure 3 uses "
    "a 1% cache, while the paper's Figure 9a uses its large cache.",
    "5. Throughput. We did not run the throughput test. The paper reports more than twice the throughput "
    "of an optimized LRU at 16 threads on a Meta trace [2]. Python cannot measure multi thread speed "
    "fairly, so we left this result untested.",
]:
    para(t)

subheading("Problems we fixed in the authors' code")
para("Published research code often needs repair before it runs, and the authors' repository needed two "
     "fixes before libCacheSim would build on Ubuntu. The first problem was a missing dependency. The "
     "install script does not install the zstd development package that the build needs, and the build "
     "failed until we installed libzstd-dev. The second problem was a wrong include "
     "path in libCacheSim/libCacheSim/cache/eviction/other/S3LRU.c. The file pointed to the hash table "
     "header two directories up instead of three. We corrected the path and committed the fix to our "
     "repository [1].")

# ---------------------------------------------------------------- conclusion
heading("Conclusion")
para("SIEVE had the lowest miss ratio of FIFO, LRU, CLOCK and SIEVE in every run we made, across nine "
     "values of alpha and five cache sizes. At alpha 1.0 and a 1% cache it removed 25% of FIFO's misses and "
     "18% of LRU's misses. Its reduction over FIFO was within 3 percentage points of the values in the "
     "paper's Figure 11 at all six points we could compare. The differences we did find come from our "
     "smaller traces, our different baselines and our narrower range of cache sizes, not from a different "
     "behavior of the algorithm.")
para("The project taught us that a small change in an eviction policy can matter more than added "
     "complexity. SIEVE and CLOCK use the same visited bit and the same amount of code, yet SIEVE removed "
     "about 17% of CLOCK's misses at a 1% cache because it leaves survivors in place. SIEVE also avoids "
     "the lock that LRU takes on every hit, so it is both simpler and faster in a server with many threads.")
para("SIEVE has a known limit. It is not scan resistant. A long scan of objects that are each read once "
     "can push useful objects out, and the paper reports that SIEVE can lose to LRU on block cache "
     "workloads that contain scans [2]. Our Zipf traces contain no scans, so our results do not test this "
     "case. For web caches, where popularity follows a Zipf pattern, our results support the paper's claim "
     "that SIEVE is a simple and effective replacement for LRU.")

# ---------------------------------------------------------------- references
heading("References:")
para("[1] Group 1, SIEVE OS class project repository, https://github.com/Ohimoiza1205/sieve-os-project")
para("[2] Y. Zhang, J. Yang, Y. Yue, Y. Vigfusson, and K. V. Rashmi, \"SIEVE is Simpler than LRU: an "
     "Efficient Turn-Key Eviction Algorithm for Web Caches,\" in 21st USENIX Symposium on Networked Systems "
     "Design and Implementation (NSDI 24), Santa Clara, CA, April 2024, pages 1229 to 1246. "
     "USENIX Association.")
para("[3] Y. Zhang et al., NSDI24-SIEVE artifact repository, https://github.com/Thesys-lab/NSDI24-SIEVE")

out = os.path.join(HERE, "Group1_SIEVE_report.docx")
doc.save(out)
print("wrote", out)
