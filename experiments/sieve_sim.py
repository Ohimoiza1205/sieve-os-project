"""Independent Python re-implementation of FIFO, LRU, CLOCK and SIEVE for the OS class project.

Run:   python sieve_sim.py        (about 15 seconds; writes results.json next to this file)
Then:  python make_figures.py    (writes the three report figures to figures/)

Setup matches the slides: 100,000 unique objects, 1,000,000 requests, Zipf traces,
cache sizes 0.1%, 0.5%, 1%, 5%, 10% of unique objects, alpha 0.6 to 1.4.
BEST is a best possible cache that always holds the most requested objects; it is a sanity bound,
no algorithm may beat it.
"""
import os, sys, json, time
from collections import OrderedDict, deque
import numpy as np

N_OBJ = 100_000
N_REQ = 1_000_000


def make_trace(alpha, seed):
    rng = np.random.default_rng(seed)
    w = 1.0 / np.arange(1, N_OBJ + 1) ** alpha
    p = w / w.sum()
    cdf = np.cumsum(p)
    u = rng.random(N_REQ)
    ids = np.searchsorted(cdf, u).astype(np.int64)
    ids[ids >= N_OBJ] = N_OBJ - 1
    return ids.tolist(), p


def fifo(trace, cap):
    q = deque()
    s = set()
    miss = 0
    for k in trace:
        if k in s:
            continue
        miss += 1
        if len(s) >= cap:
            s.discard(q.pop())
        q.appendleft(k)
        s.add(k)
    return miss / len(trace)


def lru(trace, cap):
    d = OrderedDict()
    miss = 0
    for k in trace:
        if k in d:
            d.move_to_end(k)
            continue
        miss += 1
        if len(d) >= cap:
            d.popitem(last=False)
        d[k] = 1
    return miss / len(trace)


def clock(trace, cap):
    # FIFO-reinsertion: survivors go back to the head with bit cleared
    q = deque()
    vis = {}
    miss = 0
    for k in trace:
        if k in vis:
            vis[k] = True
            continue
        miss += 1
        if len(vis) >= cap:
            while True:
                o = q.pop()
                if vis[o]:
                    vis[o] = False
                    q.appendleft(o)
                else:
                    del vis[o]
                    break
        q.appendleft(k)
        vis[k] = False
    return miss / len(trace)


def sieve(trace, cap):
    # doubly linked list, head = newest, tail = oldest, prev points toward head
    prev = {}
    nxt = {}
    vis = {}
    head = tail = hand = None
    size = 0
    miss = 0
    for k in trace:
        if k in vis:
            vis[k] = True
            continue
        miss += 1
        if size >= cap:
            o = hand if hand is not None else tail
            while vis[o]:
                vis[o] = False
                o = prev[o] if prev[o] is not None else tail
            hand = prev[o]
            po, no = prev[o], nxt[o]
            if po is not None:
                nxt[po] = no
            else:
                head = no
            if no is not None:
                prev[no] = po
            else:
                tail = po
            del prev[o], nxt[o], vis[o]
            size -= 1
        prev[k] = None
        nxt[k] = head
        if head is not None:
            prev[head] = k
        head = k
        if tail is None:
            tail = k
        vis[k] = False
        size += 1
    return miss / len(trace)


def best_possible(trace, cap):
    cnt = np.bincount(np.array(trace), minlength=N_OBJ)
    top = np.sort(cnt)[::-1][:cap].sum()
    return 1 - top / len(trace)


if __name__ == "__main__":
    out = {}
    t0 = time.time()
    # cache size as a share of the unique objects that appear in each trace
    SIZES = {"0.1%": 0.001, "0.5%": 0.005, "1%": 0.01, "5%": 0.05, "10%": 0.10}
    algs = {"FIFO": fifo, "LRU": lru, "CLOCK": clock, "SIEVE": sieve}

    def cap_for(trace, share):
        return max(1, round(len(set(trace)) * share))

    for alpha in [0.8, 1.0, 1.2]:
        tr, _ = make_trace(alpha, seed=int(alpha * 100))
        for lab, share in SIZES.items():
            c = cap_for(tr, share)
            for n, f in algs.items():
                out[f"a{alpha}|{lab}|{n}"] = f(tr, c)
            out[f"a{alpha}|{lab}|BEST"] = best_possible(tr, c)
        print("done alpha", alpha, round(time.time() - t0, 1), flush=True)
    for alpha in [0.6, 0.7, 0.9, 1.1, 1.3, 1.4]:
        tr, _ = make_trace(alpha, seed=int(alpha * 100))
        c = cap_for(tr, 0.01)
        for n in ["FIFO", "LRU", "SIEVE"]:
            out[f"a{alpha}|1%|{n}"] = algs[n](tr, c)
        out[f"a{alpha}|1%|BEST"] = best_possible(tr, c)
        print("done alpha", alpha, round(time.time() - t0, 1), flush=True)
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json"), "w"), indent=1)
    print("total seconds", round(time.time() - t0, 1))
