/* [ROUTERJIT1] compiled kernels of route_vrp's hot loops: route_eval/_sim, Solver.best_insert and the intra-route 2-opt
 * of Solver.improve. Exact ports: integer arithmetic, and every float (route_key = elapsed + 0.01 * moves, insertion
 * deltas, the 1e-9 acceptance margin) is the same IEEE double operation in the same order as the Python path
 * (build with -ffp-contract=off, no -ffast-math). No libc: built with -nostdlib, loaded by ctypes (no Python ABI), so
 * one .so serves any CPython. route_vrp falls back to the Python path when the library does not load.
 *
 * ctx (int32): [0] n stops, [1] n items, [2] end, [3] reserved, [4 .. 4+ni) item_av per item (default 2 filled in),
 *              then 9 ints per stop: x, y, early, late, dur, need_off, need_cnt, give_off, give_cnt (offsets index ctx),
 *              then (item, value) pairs.
 */
#define HDR 4
#define SW 9
#define MAXI 64
#define MAXR 256
#define MAXU 64
#define MAXC 4096
#define MAXK 64
#define INF_D 1000000.0
#define MOVE_W 0.01

static const int AX[4] = {4, 5, 4, 5};
static const int AY[4] = {4, 4, 5, 5};

static inline int iabs(int a) { return a < 0 ? -a : a; }

static int sim(const int *ctx, const int *r, int n, int sx, int sy, int t0, int pi, int nk, int pav, int *o)
{
    const int *S = ctx + HDR + ctx[1];
    int t = t0, px = sx, py = sy, moves = 0, waits = 0;
    for (int i = 0; i <= n; i++) {
        if (i == pi) {
            int nx, ny;
            if (i < n) { const int *s = S + SW * r[i]; nx = s[0]; ny = s[1]; } else { nx = px; ny = py; }
            int bq = 0, bv = 0;
            for (int q = 0; q < 4; q++) {
                int v = iabs(px - AX[q]) + iabs(py - AY[q]) + iabs(AX[q] - nx) + iabs(AY[q] - ny);
                if (q == 0 || v < bv) { bq = q; bv = v; }
            }
            int ax = AX[bq], ay = AY[bq];
            int dd = iabs(px - ax) + iabs(py - ay); moves += dd; t += dd;
            if (t < pav) { waits += pav - t; t = pav; }
            t += nk; px = ax; py = ay;
        }
        if (i == n) break;
        const int *s = S + SW * r[i];
        int dd = iabs(px - s[0]) + iabs(py - s[1]); moves += dd; t += dd;
        if (t < s[2]) { waits += s[2] - t; t = s[2]; }
        if (t > s[3]) return 0;
        t += s[4]; px = s[0]; py = s[1];
    }
    if (t > ctx[2]) return 0;
    o[0] = t; o[1] = moves; o[2] = waits;
    return 1;
}

/* route_eval: out = (finish, moves, waits, pickup slot (-1 = None), n kinds, pickup avail); 0 = infeasible (None) */
int rv_eval(const int *ctx, const int *r, int n, int sx, int sy, int t0, int *out)
{
    int ni = ctx[1];
    const int *iav = ctx + HDR, *S = ctx + HDR + ni;
    int cum[MAXI], mdef[MAXI];
    for (int k = 0; k < ni; k++) { cum[k] = 0; mdef[k] = 0; }
    int first_c = -1;
    for (int i = 0; i < n; i++) {
        const int *s = S + SW * r[i];
        const int *e = ctx + s[5];
        for (int m = 0; m < s[6]; m++) {
            int k = e[2 * m], c = cum[k] - e[2 * m + 1];
            cum[k] = c;
            if (-c > mdef[k]) { mdef[k] = -c; if (first_c < 0) first_c = i; }
        }
        e = ctx + s[7];
        for (int m = 0; m < s[8]; m++) cum[e[2 * m]] += e[2 * m + 1];
    }
    int nk = 0, pav = 0;
    for (int k = 0; k < ni; k++)
        if (mdef[k] > 0) { if (nk == 0 || iav[k] > pav) pav = iav[k]; nk++; }
    int o[3];
    if (nk == 0) {
        if (!sim(ctx, r, n, sx, sy, t0, -1, 0, 0, o)) return 0;
        out[0] = o[0]; out[1] = o[1]; out[2] = o[2]; out[3] = -1; out[4] = 0; out[5] = 0;
        return 1;
    }
    int found = 0; double bk = 0.0;
    int npi = first_c == 0 ? 1 : 2;
    for (int q = 0; q < npi; q++) {
        int pi = q == 0 ? 0 : first_c;
        if (sim(ctx, r, n, sx, sy, t0, pi, nk, pav, o)) {
            double key = (double)o[0] + MOVE_W * (double)o[1];
            if (!found || key < bk) {
                found = 1; bk = key;
                out[0] = o[0]; out[1] = o[1]; out[2] = o[2]; out[3] = pi; out[4] = nk; out[5] = pav;
            }
        }
    }
    return found;
}

/* Solver.rcost: 0.0 empty, INF infeasible, else route_key(finish - start, moves) */
static double rcost(const int *ctx, const int *r, int n, int sx, int sy, int t0)
{
    if (n == 0) return 0.0;
    int out[6];
    if (!rv_eval(ctx, r, n, sx, sy, t0, out)) return INF_D;
    return (double)(out[0] - t0) + MOVE_W * (double)out[1];
}

/* best_insert core over per-unit routes R[ui] (length L[ui]); candidates sorted by (det, uid, pos). */
static void bi_core(const int *ctx, int j, int nu, const int *uid, const int *sx, const int *sy, const int *st,
                    const int *const *R, const int *L, int K, double *oc, int *oui, int *opos)
{
    const int *S = ctx + HDR + ctx[1];
    int jx = S[SW * j], jy = S[SW * j + 1];
    long long cand[MAXC];
    int nc = 0;
    for (int ui = 0; ui < nu; ui++) {
        int px = sx[ui], py = sy[ui], len = L[ui];
        const int *r = R[ui];
        for (int pos = 0; pos <= len; pos++) {
            int d1 = iabs(px - jx) + iabs(py - jy), det;
            if (pos < len) {
                int nx = S[SW * r[pos]], ny = S[SW * r[pos] + 1];
                det = d1 + iabs(jx - nx) + iabs(jy - ny) - iabs(px - nx) - iabs(py - ny);
                px = nx; py = ny;
            } else {
                det = d1;
            }
            cand[nc++] = ((long long)(det + (1 << 20)) << 32) | ((long long)uid[ui] << 20) | ((long long)ui << 12) | pos;
        }
    }
    /* the K smallest keys in order (keys are unique: (uid, pos) unique, so the order equals Python's tuple sort) */
    long long sel[MAXK];
    int nsel = 0;
    for (int c = 0; c < nc; c++) {
        long long x = cand[c];
        if (nsel == K && x > sel[K - 1]) continue;
        int b = nsel < K ? nsel++ : K - 1;
        while (b > 0 && sel[b - 1] > x) { sel[b] = sel[b - 1]; b--; }
        sel[b] = x;
    }
    double base[MAXU]; int hb[MAXU];
    for (int ui = 0; ui < nu; ui++) hb[ui] = 0;
    double bc = INF_D; int bu = -1, bp = -1;
    int tmp[MAXR + 1];
    for (int pass = 0; pass < 2; pass++) {
        int lo = pass == 0 ? 0 : K, hi = pass == 0 ? nsel : nc;
        if (pass == 1) {
            if (!(bu < 0 && nc > K)) break;
            /* tight windows: the full scan in sorted order (Python's cand[INSERT_K:]) */
            for (int a = 1; a < nc; a++) {
                long long x = cand[a]; int b = a - 1;
                while (b >= 0 && cand[b] > x) { cand[b + 1] = cand[b]; b--; }
                cand[b + 1] = x;
            }
        }
        for (int c = lo; c < hi; c++) {
            long long x = pass == 0 ? sel[c] : cand[c];
            int ui = (int)((x >> 12) & 0xFF), pos = (int)(x & 0xFFF);
            int len = L[ui]; const int *r = R[ui];
            if (!hb[ui]) { base[ui] = rcost(ctx, r, len, sx[ui], sy[ui], st[ui]); hb[ui] = 1; }
            for (int i = 0; i < pos; i++) tmp[i] = r[i];
            tmp[pos] = j;
            for (int i = pos; i < len; i++) tmp[i + 1] = r[i];
            double cc = rcost(ctx, tmp, len + 1, sx[ui], sy[ui], st[ui]) - base[ui];
            if (cc < bc && cc < INF_D / 2) { bc = cc; bu = ui; bp = pos; }
        }
    }
    *oc = bc; *oui = bu; *opos = bp;
}

/* q = [j, n units, insert_k, then per unit: uid, sx, sy, start, len, route...] -> unit arrays */
static int unpack(const int *q, int *uid, int *sx, int *sy, int *st, const int **R, int *L)
{
    int nu = q[1], p = 3;
    for (int ui = 0; ui < nu; ui++) {
        const int *h = q + p;
        uid[ui] = h[0]; sx[ui] = h[1]; sy[ui] = h[2]; st[ui] = h[3]; L[ui] = h[4]; R[ui] = h + 5;
        p += 5 + h[4];
    }
    return nu;
}

/* Solver.best_insert. oc[0] = delta cost (INF when none), oi[0] = uid (-1 = None), oi[1] = pos. */
int rv_best_insert(const int *ctx, const int *q, double *oc, int *oi)
{
    int uid[MAXU], sx[MAXU], sy[MAXU], st[MAXU], L[MAXU];
    const int *R[MAXU];
    int nu = unpack(q, uid, sx, sy, st, R, L);
    int ui, pos;
    bi_core(ctx, q[0], nu, uid, sx, sy, st, R, L, q[2], oc, &ui, &pos);
    oi[0] = ui < 0 ? -1 : uid[ui]; oi[1] = pos;
    return ui >= 0;
}

/* Sequential best insertion of seq[0..ns) into the routes of q (the loops of ruin_recreate / mode2_ii / construct):
 * each stop goes to its best_insert slot. stop_on_fail: the first stop with no slot ends it (return 0). Otherwise a
 * stop with no slot is appended to the miss list. out = [n miss, miss..., then per unit: len, route...];
 * oc[ui] = the unit's final route cost (Solver.rcost). Returns 1 when the sequence completed. */
int rv_insert_seq(const int *ctx, const int *q, const int *seq, int ns, int stop_on_fail, int *out, double *oc)
{
    int uid[MAXU], sx[MAXU], sy[MAXU], st[MAXU], L[MAXU];
    const int *R0[MAXU];
    static int BUF[MAXU][MAXR + 1];
    const int *R[MAXU];
    int nu = unpack(q, uid, sx, sy, st, R0, L);
    for (int ui = 0; ui < nu; ui++) {
        for (int i = 0; i < L[ui]; i++) BUF[ui][i] = R0[ui][i];
        R[ui] = BUF[ui];
    }
    int nm = 0;
    for (int m = 0; m < ns; m++) {
        double c; int ui, pos, j = seq[m];
        bi_core(ctx, j, nu, uid, sx, sy, st, R, L, q[2], &c, &ui, &pos);
        if (ui < 0 || c >= INF_D / 2) {
            if (stop_on_fail) return 0;
            out[1 + nm++] = j;
            continue;
        }
        if (L[ui] >= MAXR) return -1;
        int *r = BUF[ui];
        for (int i = L[ui]; i > pos; i--) r[i] = r[i - 1];
        r[pos] = j; L[ui]++;
    }
    out[0] = nm;
    int p = 1 + nm;
    for (int ui = 0; ui < nu; ui++) {
        out[p++] = L[ui];
        for (int i = 0; i < L[ui]; i++) out[p++] = BUF[ui][i];
        oc[ui] = rcost(ctx, BUF[ui], L[ui], sx[ui], sy[ui], st[ui]);
    }
    return 1;
}

/* Solver.improve intra-route 2-opt (first-improvement, the route updated in place as Python rebinds r).
 * Returns 1 when r changed; oc[0] = final route cost. */
int rv_two_opt(const int *ctx, int *r, int n, int sx, int sy, int t0, double *oc)
{
    double bc = rcost(ctx, r, n, sx, sy, t0);
    int imp = 0, r2[MAXR];
    for (int a = 0; a < n - 1; a++) {
        for (int b = a + 1; b < n; b++) {
            for (int i = 0; i < a; i++) r2[i] = r[i];
            for (int i = a; i <= b; i++) r2[i] = r[a + b - i];
            for (int i = b + 1; i < n; i++) r2[i] = r[i];
            double c2 = rcost(ctx, r2, n, sx, sy, t0);
            if (c2 < bc - 1e-9) {
                for (int i = 0; i < n; i++) r[i] = r2[i];
                bc = c2; imp = 1;
            }
        }
    }
    oc[0] = bc;
    return imp;
}
