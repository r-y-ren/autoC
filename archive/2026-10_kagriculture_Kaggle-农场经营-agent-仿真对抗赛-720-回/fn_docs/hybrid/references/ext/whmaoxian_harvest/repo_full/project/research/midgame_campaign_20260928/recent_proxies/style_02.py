# Strategy: Use the inspected Pipe-16 HybridOpening controller. Reassign idle workers during the first three days to plant, water and harvest one temporary wheat crop, then restore the planned pasture and deliver the wheat. Preserve the public Metav4 production and market controller. This is attributed reuse, and its stronger public source still needs live confirmation. Disable optional environment-dependent external library loading so the archive is self-contained.
# Local packaging modifications, 2026-09-20. Original attribution retained.
# Kaggriculture submission v9/3: public V39 (Apache-2.0, notices below) plus the v9 layers
# RACEPX gate, RACE (reservation from step 192, horizon 40 / margin 12), COURIER, CARROT and HERD
# appended at the end of this file.
# EXP-173 isolate opening market sequence inspired by yhay81/shop-router-0911-simple (Apache-2.0).
# Kaggriculture EXP-167 candidate. Not submitted automatically.
# Attribution: thomastschinkel, yhay81, destbreso, aurax7, tetsutani,
# prvsiyan and Dmitrii Gluzdov. Apache-2.0 derivations; notices retained below.
# Kaggriculture v31 / EXP-157, Ahmed Berat Ozer, September 9 2026.
# Selected mechanism: crop_public_order. New independent confirmation is required.
# Public V221B/V224C production/timing lineage: prvsiyan, Apache-2.0.
# Original economics and integration; retained upstream licenses follow.
# Kaggriculture v28 / EXP-154, Ahmed Berat Ozer, September 9 2026.
# Changes: aurax7 day-end storage guard; Dmitrii Gluzdov physical terminal rescue
# adapted to v27, with 64 deterministic simulations. Apache-2.0.
# New action tapes and ordered shop-pair map: yhay81/shop-router-0909, Apache-2.0.
# Kaggriculture v25, EXP-149: Shop0908 production, sale lead, terminal cargo rescue.
# Runtime chassis: Apache-2.0; thomastschinkel, yhay81, tetsutani.
# Routing and public action data: yhay81/shop-router-0908, frozen September 8, 2026.
# 
#                                  Apache License
#                            Version 2.0, January 2004
#                         http://www.apache.org/licenses/
# 
#    TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
# 
#    1. Definitions.
# 
#       "License" shall mean the terms and conditions for use, reproduction,
#       and distribution as defined by Sections 1 through 9 of this document.
# 
#       "Licensor" shall mean the copyright owner or entity authorized by
#       the copyright owner that is granting the License.
# 
#       "Legal Entity" shall mean the union of the acting entity and all
#       other entities that control, are controlled by, or are under common
#       control with that entity. For the purposes of this definition,
#       "control" means (i) the power, direct or indirect, to cause the
#       direction or management of such entity, whether by contract or
#       otherwise, or (ii) ownership of fifty percent (50%) or more of the
#       outstanding shares, or (iii) beneficial ownership of such entity.
# 
#       "You" (or "Your") shall mean an individual or Legal Entity
#       exercising permissions granted by this License.
# 
#       "Source" form shall mean the preferred form for making modifications,
#       including but not limited to software source code, documentation
#       source, and configuration files.
# 
#       "Object" form shall mean any form resulting from mechanical
#       transformation or translation of a Source form, including but
#       not limited to compiled object code, generated documentation,
#       and conversions to other media types.
# 
#       "Work" shall mean the work of authorship, whether in Source or
#       Object form, made available under the License, as indicated by a
#       copyright notice that is included in or attached to the work
#       (an example is provided in the Appendix below).
# 
#       "Derivative Works" shall mean any work, whether in Source or Object
#       form, that is based on (or derived from) the Work and for which the
#       editorial revisions, annotations, elaborations, or other modifications
#       represent, as a whole, an original work of authorship. For the purposes
#       of this License, Derivative Works shall not include works that remain
#       separable from, or merely link (or bind by name) to the interfaces of,
#       the Work and Derivative Works thereof.
# 
#       "Contribution" shall mean any work of authorship, including
#       the original version of the Work and any modifications or additions
#       to that Work or Derivative Works thereof, that is intentionally
#       submitted to Licensor for inclusion in the Work by the copyright owner
#       or by an individual or Legal Entity authorized to submit on behalf of
#       the copyright owner. For the purposes of this definition, "submitted"
#       means any form of electronic, verbal, or written communication sent
#       to the Licensor or its representatives, including but not limited to
#       communication on electronic mailing lists, source code control systems,
#       and issue tracking systems that are managed by, or on behalf of, the
#       Licensor for the purpose of discussing and improving the Work, but
#       excluding communication that is conspicuously marked or otherwise
#       designated in writing by the copyright owner as "Not a Contribution."
# 
#       "Contributor" shall mean Licensor and any individual or Legal Entity
#       on behalf of whom a Contribution has been received by Licensor and
#       subsequently incorporated within the Work.
# 
#    2. Grant of Copyright License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       copyright license to reproduce, prepare Derivative Works of,
#       publicly display, publicly perform, sublicense, and distribute the
#       Work and such Derivative Works in Source or Object form.
# 
#    3. Grant of Patent License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       (except as stated in this section) patent license to make, have made,
#       use, offer to sell, sell, import, and otherwise transfer the Work,
#       where such license applies only to those patent claims licensable
#       by such Contributor that are necessarily infringed by their
#       Contribution(s) alone or by combination of their Contribution(s)
#       with the Work to which such Contribution(s) was submitted. If You
#       institute patent litigation against any entity (including a
#       cross-claim or counterclaim in a lawsuit) alleging that the Work
#       or a Contribution incorporated within the Work constitutes direct
#       or contributory patent infringement, then any patent licenses
#       granted to You under this License for that Work shall terminate
#       as of the date such litigation is filed.
# 
#    4. Redistribution. You may reproduce and distribute copies of the
#       Work or Derivative Works thereof in any medium, with or without
#       modifications, and in Source or Object form, provided that You
#       meet the following conditions:
# 
#       (a) You must give any other recipients of the Work or
#           Derivative Works a copy of this License; and
# 
#       (b) You must cause any modified files to carry prominent notices
#           stating that You changed the files; and
# 
#       (c) You must retain, in the Source form of any Derivative Works
#           that You distribute, all copyright, patent, trademark, and
#           attribution notices from the Source form of the Work,
#           excluding those notices that do not pertain to any part of
#           the Derivative Works; and
# 
#       (d) If the Work includes a "NOTICE" text file as part of its
#           distribution, then any Derivative Works that You distribute must
#           include a readable copy of the attribution notices contained
#           within such NOTICE file, excluding those notices that do not
#           pertain to any part of the Derivative Works, in at least one
#           of the following places: within a NOTICE text file distributed
#           as part of the Derivative Works; within the Source form or
#           documentation, if provided along with the Derivative Works; or,
#           within a display generated by the Derivative Works, if and
#           wherever such third-party notices normally appear. The contents
#           of the NOTICE file are for informational purposes only and
#           do not modify the License. You may add Your own attribution
#           notices within Derivative Works that You distribute, alongside
#           or as an addendum to the NOTICE text from the Work, provided
#           that such additional attribution notices cannot be construed
#           as modifying the License.
# 
#       You may add Your own copyright statement to Your modifications and
#       may provide additional or different license terms and conditions
#       for use, reproduction, or distribution of Your modifications, or
#       for any such Derivative Works as a whole, provided Your use,
#       reproduction, and distribution of the Work otherwise complies with
#       the conditions stated in this License.
# 
#    5. Submission of Contributions. Unless You explicitly state otherwise,
#       any Contribution intentionally submitted for inclusion in the Work
#       by You to the Licensor shall be under the terms and conditions of
#       this License, without any additional terms or conditions.
#       Notwithstanding the above, nothing herein shall supersede or modify
#       the terms of any separate license agreement you may have executed
#       with Licensor regarding such Contributions.
# 
#    6. Trademarks. This License does not grant permission to use the trade
#       names, trademarks, service marks, or product names of the Licensor,
#       except as required for reasonable and customary use in describing the
#       origin of the Work and reproducing the content of the NOTICE file.
# 
#    7. Disclaimer of Warranty. Unless required by applicable law or
#       agreed to in writing, Licensor provides the Work (and each
#       Contributor provides its Contributions) on an "AS IS" BASIS,
#       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#       implied, including, without limitation, any warranties or conditions
#       of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
#       PARTICULAR PURPOSE. You are solely responsible for determining the
#       appropriateness of using or redistributing the Work and assume any
#       risks associated with Your exercise of permissions under this License.
# 
#    8. Limitation of Liability. In no event and under no legal theory,
#       whether in tort (including negligence), contract, or otherwise,
#       unless required by applicable law (such as deliberate and grossly
#       negligent acts) or agreed to in writing, shall any Contributor be
#       liable to You for damages, including any direct, indirect, special,
#       incidental, or consequential damages of any character arising as a
#       result of this License or out of the use or inability to use the
#       Work (including but not limited to damages for loss of goodwill,
#       work stoppage, computer failure or malfunction, or any and all
#       other commercial damages or losses), even if such Contributor
#       has been advised of the possibility of such damages.
# 
#    9. Accepting Warranty or Additional Liability. While redistributing
#       the Work or Derivative Works thereof, You may choose to offer,
#       and charge a fee for, acceptance of support, warranty, indemnity,
#       or other liability obligations and/or rights consistent with this
#       License. However, in accepting such obligations, You may act only
#       on Your own behalf and on Your sole responsibility, not on behalf
#       of any other Contributor, and only if You agree to indemnify,
#       defend, and hold each Contributor harmless for any liability
#       incurred by, or claims asserted against, such Contributor by reason
#       of your accepting any such warranty or additional liability.
# 
#    END OF TERMS AND CONDITIONS
# 
#    APPENDIX: How to apply the Apache License to your work.
# 
#       To apply the Apache License to your work, attach the following
#       boilerplate notice, with the fields enclosed by brackets "[]"
#       replaced with your own identifying information. (Don't include
#       the brackets!)  The text should be enclosed in the appropriate
#       comment syntax for the file format. We also recommend that a
#       file or class name and description of purpose be included on the
#       same "printed page" as the copyright notice for easier
#       identification within third-party archives.
# 
#    Copyright [yyyy] [name of copyright owner]
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""Kaggriculture route-replay chassis (pure Python, stdlib only).

A *route* is a pre-computed tape of 719 Kaggle-format actions
``{"farmer": [op, ...], "hands": [[op, ...], ...], "market": [[order, item, qty], ...]}``.
The chassis replays the tape chosen by a caller-supplied ``router`` and wraps it
in small reactive layers (each independently switchable via ``settings``):

    hand_align            pad/truncate hands to the real hand count      (fieldbook_logic)
    weed_repair           DIG a weed that blocks PLANT/BUILD, replay      (tetsutani + task spec)
    sell_lead             sell next step's lots one step early            (fieldbook _lead_sale)
    front_run             sell before the opponent's scheduled SELL       (hook; opponent_plan)
    budget_guard          fund each 72-step block's purchases             (six_day_budget_guard.hpp)
    room_guard            keep shed <= 99 at hour 23                      (tetsutani)
    clamp_sells           trim SELL orders to the projected shed          (tetsutani)
    dead_stock            sell stock the route will never sell            (tetsutani)
    terminal_liquidation  step >= 718: sell the whole projected shed      (fieldbook _terminal_sale)

Engine facts (verified against kaggle_environments 1.32.7, env_1_32_7.py):
  observation["farms"][p] = {"money", "tiles"[y][x], "farmer"[x,y], "hands"[[x,y]..],
                             "unlocked_quadrants", "hires_today"}
  tiles: None (empty) | "LOCKED" | {"kind": WEED|COOP|PASTURE|PLANT, "crop"/"animal", ...}
  observation["private"] = {"shed": {item: n}, "seeds": {crop: n}, "inventories": [{}...]}
  observation["market"] = {"inventory": {...}, "prices": {...}}
  observation["town"] = {"unlocked_shops": [...]}
  Agents act on steps 0..718 (interpreter marks DONE once step >= episodeSteps-2).
"""
from __future__ import annotations

import copy

PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
SEED_PRICE = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
ANIMAL_STRUCTURE = {"GOOSE": "COOP", "COW": "PASTURE", "SHEEP": "PASTURE"}
LAND_PRICES = (1000, 2000, 4000)
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
FRONT_RUN_ITEMS = ("MILK", "WOOL", "STRAWBERRY", "MELON")
LAST_ACT_STEP = 718
PASS_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}

DEFAULT_SETTINGS = {
    "hand_align": True,
    "weed_repair": True,
    "sell_lead": True,
    "front_run": True,
    "budget_guard": True,
    "room_guard": True,
    "clamp_sells": True,
    "dead_stock": True,
    "terminal_liquidation": True,
    # tunables
    "block_turns": 72,
    "shed_capacity": 100,
    "board_size": 10,
    "max_orders": 10,
    "turns_per_day": 24,
    "min_sell_price": 2,
}


# --------------------------------------------------------------------------- helpers
def _get(value, key, default=None):
    """Field access that works for dicts and Kaggle Struct/attribute objects."""
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def _int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _step_of(observation):
    raw = _get(observation, "step")
    if raw is not None:
        return _int(raw)
    return _int(_get(observation, "day", 0)) * 24 + _int(_get(observation, "hour", 0))


def _shed_adjacent(pos, board):
    if not isinstance(pos, (list, tuple)) or len(pos) < 2:
        return False
    half = board // 2
    return pos[0] in (half - 1, half) and pos[1] in (half - 1, half)


def _tile_at(tiles, pos):
    try:
        x, y = int(pos[0]), int(pos[1])
        return tiles[y][x]
    except (TypeError, ValueError, IndexError):
        return "LOCKED"


def _is_noop(act, tile, inv, seeds, pos, board):
    """True when the engine will certainly ignore ``act`` (mirrors _apply_unit_action)."""
    if not act:
        return True
    op = act[0]
    x, y = pos[0], pos[1]
    if op in MOVES:
        dx, dy = MOVES[op]
        return not (0 <= x + dx < board and 0 <= y + dy < board)
    if op == "PASS":
        return True
    adjacent = _shed_adjacent(pos, board)
    if op == "DROP":
        return (not adjacent) or (not inv)
    if op == "PICKUP":
        return not adjacent
    if op == "PLACE":
        item = act[1] if len(act) > 1 else None
        if item in ANIMAL_STRUCTURE and isinstance(tile, dict) \
                and _get(tile, "kind") == ANIMAL_STRUCTURE[item] and _get(tile, "animal") is None:
            return _int(_get(inv, item, 0)) <= 0
        return (not adjacent) or _int(_get(inv, item, 0)) <= 0
    if tile == "LOCKED":
        return True
    is_dict = isinstance(tile, dict)
    kind = _get(tile, "kind") if is_dict else None
    animal = is_dict and _get(tile, "animal") is not None
    if op == "PLANT":
        return tile is not None or _int(_get(seeds, act[1] if len(act) > 1 else None, 0)) <= 0
    if op == "WATER":
        return kind != "PLANT" or bool(_get(tile, "watered_today"))
    if op == "HARVEST":
        return (not is_dict) or _int(_get(tile, "yield_units", 0)) <= 0
    if op == "FERTILIZE":
        return kind != "PLANT" or _int(_get(inv, "FERTILIZER", 0)) <= 0
    if op == "DIG":
        return tile is None or animal
    if op in ("BUILD_COOP", "BUILD_PASTURE"):
        return tile is not None
    if op == "FEED":
        return (not animal) or bool(_get(tile, "fed_today")) or _int(_get(inv, "WHEAT", 0)) <= 0
    if op == "COLLECT_FERTILIZER":
        return (not animal) or (not _get(tile, "fertilizer_available"))
    if op == "CARE":
        return (not animal) or bool(_get(tile, "cared_today"))
    return True


class _View:
    """Cheap per-step snapshot of everything the layers read from the observation."""

    def __init__(self, observation, player, cfg):
        farms = list(_get(observation, "farms", []) or [])
        self.farm = farms[player] if player < len(farms) else {}
        self.rival = farms[1 - player] if len(farms) >= 2 and 1 - player < len(farms) else {}
        private = _get(observation, "private", {}) or {}
        self.shed = {k: max(0, _int(v)) for k, v in dict(_get(private, "shed", {}) or {}).items()}
        self.seeds = dict(_get(private, "seeds", {}) or {})
        self.invs = [dict(i or {}) for i in (_get(private, "inventories", []) or [])]
        market = _get(observation, "market", {}) or {}
        self.prices = {k: _int(v) for k, v in dict(_get(market, "prices", {}) or {}).items()}
        self.money = float(_get(self.farm, "money", 0.0) or 0.0)
        self.tiles = _get(self.farm, "tiles", []) or []
        self.board = len(self.tiles) or cfg["board_size"]
        self.positions = [_get(self.farm, "farmer", None)] + [list(p) for p in (_get(self.farm, "hands", []) or [])]
        self.hires_today = _int(_get(self.farm, "hires_today", 0))
        self.quadrants = len(list(_get(self.farm, "unlocked_quadrants", []) or []))

    def inv(self, idx):
        return self.invs[idx] if idx < len(self.invs) else {}

    def in_hands(self, item):
        return sum(max(0, _int(_get(inv, item, 0))) for inv in self.invs)


# --------------------------------------------------------------------------- chassis
class Chassis:
    """Replays ``routes[router(...)]`` with reactive safety/market layers.

    routes         : {route_id: list of >= 719 Kaggle action dicts}
    router         : callable(observation, step, state_dict) -> route_id, called every
                     step; ``state_dict`` is per-player and persists across the game.
    settings       : overrides for DEFAULT_SETTINGS (layer switches + tunables)
    opponent_plan  : optional list of the opponent's expected actions (front_run hook)
    """

    def __init__(self, routes, router=None, settings=None, opponent_plan=None):
        self.routes = {rid: list(tape) for rid, tape in routes.items()}
        self.router = router or (lambda observation, step, state: next(iter(self.routes)))
        self.cfg = dict(DEFAULT_SETTINGS)
        self.cfg.update(settings or {})
        self.opponent_plan = opponent_plan
        self.players = {}
        self.diagnostics = {"layer_fallbacks": 0, "entry_fallbacks": 0}
        self._future_sells = {}   # route id -> {item: [remaining planned SELL qty from step t]}

    # ---- state -----------------------------------------------------------------
    def _state(self, player, step):
        st = self.players.get(player)
        if st is None or step == 0 or step <= st["last_step"]:
            st = {"last_step": -1, "route": None, "router_state": {},
                  "pending": {}, "sell_state": {"due_step": -1, "suppress": {}}}
            self.players[player] = st
        st["last_step"] = step
        return st

    def _route_action(self, route, step):
        tape = self.routes[route]
        if 0 <= step < len(tape) and isinstance(tape[step], dict):
            return copy.deepcopy(tape[step])
        return copy.deepcopy(PASS_ACTION)

    def future_sells(self, route, item, step):
        """Planned SELL quantity of ``item`` in route steps >= ``step`` (suffix sums)."""
        table = self._future_sells.get(route)
        if table is None:
            tape = self.routes[route]
            n = len(tape)
            table = {p: [0] * (n + 1) for p in PRODUCTS}
            for t in range(n - 1, -1, -1):
                for p in PRODUCTS:
                    table[p][t] = table[p][t + 1]
                for o in (tape[t].get("market") or []) if isinstance(tape[t], dict) else []:
                    if o and o[0] == "SELL" and len(o) >= 3 and o[1] in table:
                        table[o[1]][t] += max(0, _int(o[2]))
            self._future_sells[route] = table
        col = table.get(item)
        return col[step] if col and 0 <= step < len(col) else 0

    # ---- main entry -----------------------------------------------------------
    def act(self, observation, configuration=None):
        if len(_get(observation, "farms", []) or []) < 2:
            raise ValueError("incomplete observation")  # factory falls back to tape
        step = _step_of(observation)
        player = _int(_get(observation, "player", 0))
        st = self._state(player, step)
        cfg = self.cfg
        view = _View(observation, player, cfg)

        route = self.router(observation, step, st["router_state"])
        if route not in self.routes:
            route = st["route"] if st["route"] in self.routes else next(iter(self.routes))
        st["route"] = route
        action = self._route_action(route, step)
        raw = copy.deepcopy(action)
        try:
            if cfg["hand_align"]:
                self._hand_align(action, view)
            if cfg["weed_repair"]:
                self._weed_repair(action, view, st, route, step)
            if cfg["sell_lead"] or cfg["front_run"]:
                self._apply_suppression(action, st["sell_state"], step)
            projected = self._projected_shed(action, view)
            lead_available = dict(projected)
            next_sup = {"due_step": -1, "suppress": {}, "r36_debts": st["sell_state"].get("r36_debts", {})}
            if cfg["sell_lead"]:
                self._sell_lead(action, view, lead_available, route, step, next_sup)
            if cfg["front_run"] and self.opponent_plan:
                self._front_run(action, view, lead_available, route, step, next_sup)
            st["sell_state"] = next_sup
            if cfg["budget_guard"]:
                self._budget_guard(action, view, route, step)
            if cfg["room_guard"]:
                self._room_guard(action, view, route, step)
            if cfg["clamp_sells"]:
                self._clamp_sells(action, projected)
            if cfg["dead_stock"]:
                self._dead_stock(action, view, projected, route, step)
            if cfg["terminal_liquidation"]:
                self._terminal_liquidation(action, projected, step)
            action["market"] = action["market"][: cfg["max_orders"]]
            return action
        except Exception:
            self.diagnostics["layer_fallbacks"] += 1
            return raw

    # ---- layer: hand_align ----------------------------------------------------
    def _hand_align(self, action, view):
        """Pad with PASS / truncate the tape's hand list to the real number of hands
        (fieldbook_logic.act). Extra hands would be ignored by the engine anyway;
        missing ones just idle, so alignment only tidies the action."""
        expected = max(0, len(view.positions) - 1)
        hands = list(action.get("hands") or [])
        hands.extend([["PASS"] for _ in range(max(0, expected - len(hands)))])
        action["hands"] = hands[:expected]

    # ---- layer: weed_repair ---------------------------------------------------
    def _weed_repair(self, action, view, st, route, step):
        """If a PLANT/BUILD_* target tile is a WEED, DIG now and queue the intended
        action for that unit; the queue replays on a later step when the unit still
        stands there and its tape action would be a no-op (the displaced no-op is
        queued behind it, so PLANT -> WATER chains survive). A PLANT is only replayed
        when the unit's next tape action is not a move, so the mandatory same-day
        WATER can follow; otherwise the seed is kept. A no-op turn spent on a weed
        is also converted to DIG (tetsutani weed_dig)."""
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        pending = st["pending"]
        tape = self.routes[route]
        nxt = tape[step + 1] if step + 1 < len(tape) and isinstance(tape[step + 1], dict) else {}
        next_units = [nxt.get("farmer") or ["PASS"]] + list(nxt.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            pos = view.positions[i]
            if not isinstance(pos, (list, tuple)):
                continue
            pos = (int(pos[0]), int(pos[1]))
            tile = _tile_at(view.tiles, pos)
            act = list(units[i])
            queue = pending.get(i)
            if queue and queue[0][0] != pos:
                pending.pop(i, None)
                queue = None
            is_weed = isinstance(tile, dict) and _get(tile, "kind") == "WEED"
            noop = _is_noop(act, tile, view.inv(i), view.seeds, pos, view.board)
            next_op = next_units[i][0] if i < len(next_units) and next_units[i] else "PASS"
            if act and act[0] in ("PLANT", "BUILD_COOP", "BUILD_PASTURE") and is_weed:
                pending.setdefault(i, []).append((pos, act))
                act = ["DIG"]
            elif queue and noop:
                _, replay = queue[0]
                if replay[0] == "PLANT" and next_op in MOVES:
                    pending.pop(i, None)          # WATER could never follow: keep the seed
                else:
                    queue.pop(0)
                    if act and act[0] != "PASS" and act[0] not in MOVES:
                        queue.append((pos, act))
                    act = replay
                    if not queue:
                        pending.pop(i, None)
            elif is_weed and noop:
                act = ["DIG"]
            units[i] = act
        action["farmer"] = units[0]
        action["hands"] = units[1:]

    # ---- projected shed -------------------------------------------------------
    def _projected_shed(self, action, view):
        """Shed contents after this step's unit actions but before the market runs:
        PICKUP removes, DROP/PLACE(non-animal) near the shed adds up to capacity
        (fieldbook _projected_shed / tetsutani projected shed)."""
        cap = self.cfg["shed_capacity"]
        proj = {p: view.shed.get(p, 0) for p in PRODUCTS}
        for k, v in view.shed.items():
            proj.setdefault(k, v)
        total = sum(proj.values())
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            if not _shed_adjacent(view.positions[i], view.board):
                continue
            act = units[i]
            op = act[0] if act else "PASS"
            inv = view.inv(i)
            if op == "PICKUP" and len(act) >= 2 and act[1] in proj:
                qty = min(proj[act[1]], max(0, _int(act[2]) if len(act) >= 3 else 1))
                proj[act[1]] -= qty
                total -= qty
            elif op == "DROP":
                for item, held in inv.items():
                    take = min(max(0, _int(held)), max(0, cap - total))
                    if take > 0:
                        proj[item] = proj.get(item, 0) + take
                        total += take
            elif op == "PLACE" and len(act) >= 2 and act[1] not in ANIMAL_STRUCTURE:
                item = act[1]
                take = min(max(0, _int(act[2]) if len(act) >= 3 else 1),
                           max(0, _int(_get(inv, item, 0))), max(0, cap - total))
                if take > 0:
                    proj[item] = proj.get(item, 0) + take
                    total += take
        return proj

    # ---- layer: sell_lead / front_run suppression ------------------------------
    @staticmethod
    def _apply_suppression(action, sell_state, step):
        """Remove from this step's SELLs the quantities already sold a step early."""
        if sell_state.get("due_step") != step:
            return
        remaining = dict(sell_state.get("suppress", {}))
        kept = []
        for order in action.get("market") or []:
            order = list(order)
            if order and order[0] == "SELL" and len(order) >= 3 and remaining.get(order[1], 0) > 0:
                removed = min(max(0, _int(order[2])), remaining[order[1]])
                order[2] = _int(order[2]) - removed
                remaining[order[1]] -= removed
                # A zero-quantity order keeps later market race slots intact.
            kept.append(order)
        action["market"] = kept

    @staticmethod
    def _add_sell(action, item, qty, max_orders, merge=True):
        market = action.setdefault("market", [])
        if merge:
            for order in market:
                if order and order[0] == "SELL" and order[1] == item:
                    order[2] = _int(order[2]) + qty
                    return True
        if len(market) >= max_orders:
            return False
        market.append(["SELL", item, qty])
        return True

    def _sell_lead(self, action, view, projected, route, step, next_sup):
        """fieldbook _lead_sale: when step % 4 != 0 (no town consumption between the
        two steps) sell the lots the tape plans to SELL next step now, for products
        other than WHEAT/FERTILIZER we already hold, and suppress them next step.
        Skipped at the last step, at shop-unlock boundaries and if a SELL for that
        product is already queued this step."""
        cfg = self.cfg
        nxt = step + 1
        unlock_period = 3 * cfg["turns_per_day"]
        if nxt > LAST_ACT_STEP or nxt % unlock_period == 0 or step % 4 == 0:
            return
        tape = self.routes[route]
        future = tape[nxt] if nxt < len(tape) and isinstance(tape[nxt], dict) else {}
        planned = {}
        for o in future.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3 and o[1] in PRODUCTS:
                planned[o[1]] = planned.get(o[1], 0) + max(0, _int(o[2]))
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for item in PRODUCTS:
            if item in ("WHEAT", "FERTILIZER") or planned.get(item, 0) <= 0 or item in already:
                continue
            qty = min(projected.get(item, 0), planned[item])
            if qty <= 0 or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    def _front_run(self, action, view, projected, route, step, next_sup):
        """Hook: if ``opponent_plan`` (their expected tape) schedules a SELL of
        MILK/WOOL/STRAWBERRY/MELON next step, sell what we hold of it now (before
        their supply depresses the price) and suppress our own SELL of that quantity
        next step. Bounded by our own remaining planned sales so it never dumps."""
        cfg = self.cfg
        nxt = step + 1
        plan = self.opponent_plan
        if nxt > LAST_ACT_STEP or nxt >= len(plan) or not isinstance(plan[nxt], dict):
            return
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for o in plan[nxt].get("market") or []:
            if not (o and o[0] == "SELL" and len(o) >= 3 and o[1] in FRONT_RUN_ITEMS):
                continue
            item = o[1]
            if item in already or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            own_next = sum(max(0, _int(x[2])) for x in self.routes[route][nxt].get("market", [])
                           if len(x) >= 3 and x[0] == "SELL" and x[1] == item)
            qty = min(projected.get(item, 0), max(0, _int(o[2])), own_next)
            if qty <= 0:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            already.add(item)
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    # ---- layer: budget_guard --------------------------------------------------
    def _block_requirements(self, view, route, start, end):
        """Planned purchase cost and item reserves for tape steps [start, end)
        (six_day_budget_guard.hpp calculate_six_day_requirements)."""
        tape = self.routes[route]
        budget = 0.0
        seed_bal, item_bal = {}, {}
        seed_need, item_need = {}, {}
        hires_by_day = {}
        quadrants = view.quadrants
        for t in range(start, min(end, len(tape))):
            a = tape[t] if isinstance(tape[t], dict) else {}
            for u in [a.get("farmer") or ["PASS"]] + list(a.get("hands") or []):
                if not u:
                    continue
                op = u[0]
                arg = u[1] if len(u) > 1 else None
                qty = max(1, _int(u[2]) if len(u) > 2 else 1)
                if op == "PLANT" and arg in SEED_PRICE:
                    seed_bal[arg] = seed_bal.get(arg, 0) - 1
                    seed_need[arg] = max(seed_need.get(arg, 0), -seed_bal[arg])
                elif op == "FEED":
                    item_bal["WHEAT"] = item_bal.get("WHEAT", 0) - 1
                    item_need["WHEAT"] = max(item_need.get("WHEAT", 0), -item_bal["WHEAT"])
                elif op == "FERTILIZE":
                    item_bal["FERTILIZER"] = item_bal.get("FERTILIZER", 0) - 1
                    item_need["FERTILIZER"] = max(item_need.get("FERTILIZER", 0), -item_bal["FERTILIZER"])
                elif op == "PLACE" and arg is not None:
                    item_bal[arg] = item_bal.get(arg, 0) - qty
                    item_need[arg] = max(item_need.get(arg, 0), -item_bal[arg])
            for o in a.get("market") or []:
                if not o:
                    continue
                op = o[0]
                item = o[1] if len(o) > 1 else None
                qty = max(1, _int(o[2]) if len(o) > 2 else 1)
                if op == "HIRE":
                    day = (t - start) // self.cfg["turns_per_day"]
                    hires_by_day[day] = hires_by_day.get(day, 0) + 1
                elif op == "BUY_LAND":
                    extra = quadrants - 1
                    if 0 <= extra < len(LAND_PRICES):
                        budget += LAND_PRICES[extra]
                        quadrants += 1
                elif op == "BUY_SEED" and item in SEED_PRICE:
                    budget += SEED_PRICE[item] * qty
                    seed_bal[item] = seed_bal.get(item, 0) + qty
                elif op == "BUY_PRODUCT" and item in ("WHEAT", "FERTILIZER"):
                    budget += view.prices.get(item, 0) * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
                elif op == "BUY_ANIMAL" and item in ANIMAL_COST:
                    budget += ANIMAL_COST[item] * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
        for day, n in hires_by_day.items():
            first = view.hires_today if day == 0 else 0
            for k in range(n):
                budget += _fib(first + k)
        return budget, item_need

    def _budget_guard(self, action, view, route, step):
        """At every block boundary (step % 72 == 0) make sure cash + the value of
        stock the block already plans to sell covers the block's purchases (hires,
        land, seeds, animals, products). A shortfall is covered by extra SELLs of
        unprotected shed stock, highest price first; SELLs are moved in front of
        the buys so the money is there when they execute."""
        cfg = self.cfg
        block = cfg["block_turns"]
        if block <= 0 or step % block != 0:
            return
        budget, item_need = self._block_requirements(view, route, step, step + block)
        market = action.setdefault("market", [])
        existing = {}
        for o in market:
            if o and o[0] == "SELL" and len(o) >= 3:
                existing[o[1]] = existing.get(o[1], 0) + max(0, _int(o[2]))
        cash = view.money
        for item in PRODUCTS:
            planned = max(existing.get(item, 0), self.future_sells(route, item, step)
                          - self.future_sells(route, item, step + block))
            cash += min(view.shed.get(item, 0), planned) * view.prices.get(item, 0)
        shortfall = budget - cash
        if shortfall <= 0:
            return
        candidates = []
        for item in PRODUCTS:
            price = view.prices.get(item, 0)
            if price < cfg["min_sell_price"]:
                continue
            protected = max(0, item_need.get(item, 0) - view.in_hands(item))
            avail = view.shed.get(item, 0) - protected - existing.get(item, 0)
            if avail > 0:
                candidates.append((-price, item, avail, price))
        candidates.sort()
        added = False
        for _, item, avail, price in candidates:
            if shortfall <= 0:
                break
            qty = min(avail, -(-int(shortfall) // price))
            if self._add_sell(action, item, qty, cfg["max_orders"]):
                shortfall -= qty * price
                added = True
        if added:
            sells = [o for o in market if o and o[0] == "SELL"]
            others = [o for o in market if not (o and o[0] == "SELL")]
            action["market"] = sells + others

    # ---- layer: room_guard ----------------------------------------------------
    def _room_guard(self, action, view, route, step):
        """tetsutani room_guard: at hour 23 the end-of-day drop pushes every unit's
        inventory into the shed and overflow is destroyed. Estimate the shed after
        this step (stock + carried + harvest/collect - feed/fertilize/place + buys -
        sells) and, if it exceeds capacity-1, add SELLs preferring products with no
        future planned sale, then highest price."""
        cfg = self.cfg
        if step % cfg["turns_per_day"] != cfg["turns_per_day"] - 1:
            return
        cap = cfg["shed_capacity"]
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        carried = sum(max(0, _int(n)) for inv in view.invs for n in inv.values())
        produced = consumed = 0
        for i in range(min(len(units), len(view.positions))):
            tile = _tile_at(view.tiles, view.positions[i])
            a = units[i]
            if not a:
                continue
            op = a[0]
            if op == "HARVEST" and isinstance(tile, dict):
                produced += max(0, _int(_get(tile, "yield_units", 0)))
            elif op == "COLLECT_FERTILIZER" and isinstance(tile, dict) and _get(tile, "fertilizer_available"):
                produced += 1
            elif op in ("FEED", "FERTILIZE"):
                consumed += 1
            elif op == "PLACE" and len(a) > 1 and a[1] in ANIMAL_STRUCTURE:
                consumed += 1
        market = action.setdefault("market", [])
        planned_sells, planned_buys = {}, 0
        for o in market:
            if not o:
                continue
            if o[0] == "SELL" and len(o) >= 3:
                planned_sells[o[1]] = planned_sells.get(o[1], 0) + max(0, _int(o[2]))
            elif o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                planned_buys += max(0, _int(o[2]))
        shed_total = sum(view.shed.values())
        fillable = sum(min(view.shed.get(it, 0), n) for it, n in planned_sells.items())
        needed = shed_total + carried + produced - consumed + planned_buys - fillable - (cap - 1)
        if needed <= 0:
            return
        priority = sorted(PRODUCTS, key=lambda it: (self.future_sells(route, it, step + 1) > 0,
                                                   -view.prices.get(it, 0), it))
        for item in priority:
            avail = max(0, view.shed.get(item, 0) - planned_sells.get(item, 0))
            qty = min(needed, avail)
            if qty <= 0 or view.prices.get(item, 0) < 1:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"]):
                continue
            planned_sells[item] = planned_sells.get(item, 0) + qty
            needed -= qty
            if needed <= 0:
                break

    # ---- layer: clamp_sells ---------------------------------------------------
    @staticmethod
    def _clamp_sells(action, projected):
        """Clamp against a sequential stock upper bound, retaining market slots.

        Earlier BUY_PRODUCT orders can fund a wheat wash's sell leg. Their full
        quantity is an upper bound; the engine enforces actual cash/capacity.
        Removing empty orders would change the later lockstep market races.
        """
        avail = dict(projected)
        kept = []
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                have = avail.get(o[1], 0)
                n = min(_int(o[2]), have)
                n = max(0, n)
                avail[o[1]] = have - n
                kept.append(["SELL", o[1], n])
            else:
                kept.append(o)
                if o and o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                    avail[o[1]] = avail.get(o[1], 0) + max(0, _int(o[2]))
        action["market"] = kept

    # ---- layer: dead_stock ----------------------------------------------------
    def _dead_stock(self, action, view, projected, route, step):
        """tetsutani dead_stock: stock beyond everything the rest of the route still
        plans to SELL is dead; sell it now when price > 1 (on day 29 everything not
        already in this step's orders is dead). Highest value lots first."""
        planned = {}
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                planned[o[1]] = planned.get(o[1], 0) + _int(o[2])
        day = step // self.cfg["turns_per_day"]
        extra = []
        for item in PRODUCTS:
            have = projected.get(item, 0) - planned.get(item, 0)
            if have <= 0:
                continue
            surplus = have if day >= 29 else have - self.future_sells(route, item, step + 1)
            if surplus > 0 and view.prices.get(item, 0) > 1:
                extra.append(["SELL", item, surplus])
        extra.sort(key=lambda o: -view.prices.get(o[1], 0) * o[2])
        action["market"] = (action.get("market") or []) + extra

    # ---- layer: terminal_liquidation -----------------------------------------
    def _terminal_liquidation(self, action, projected, step):
        """fieldbook _terminal_sale: on the final acting step (>= 718) replace the
        market orders with a SELL of the whole projected shed."""
        if step < LAST_ACT_STEP:
            return
        action["market"] = [["SELL", item, qty] for item, qty in projected.items()
                            if qty > 0 and item in PRODUCTS][: self.cfg["max_orders"]]


# --------------------------------------------------------------------------- factory
def make_agent(routes, router=None, opponent_plan=None, **settings):
    """Build a Kaggle ``agent(observation, configuration)`` closure that never raises:
    a failure inside a layer falls back to the raw tape action, and a failure even
    before that falls back to PASS (with hands padded when possible)."""
    chassis = Chassis(routes, router, settings, opponent_plan)

    def agent(observation, configuration=None):
        try:
            return chassis.act(observation, configuration)
        except Exception:
            chassis.diagnostics["entry_fallbacks"] += 1
            try:
                step = _step_of(observation)
                player = _int(_get(observation, "player", 0))
                tape = chassis.routes.get(chassis.players.get(player, {}).get("route"),
                                          next(iter(chassis.routes.values())))
                if 0 <= step < len(tape):
                    return copy.deepcopy(tape[step])
            except Exception:
                pass
            try:
                farms = _get(observation, "farms", []) or []
                hands = _get(farms[_int(_get(observation, "player", 0))], "hands", []) or []
                return {"farmer": ["PASS"], "hands": [["PASS"] for _ in hands], "market": []}
            except Exception:
                return copy.deepcopy(PASS_ACTION)

    agent.chassis = chassis
    return agent

# Extracted from the frozen One More Wheat source on 2026-09-22.
# Upstream Apache-2.0 notices are retained above. Generic library only.


# Public actions only; no hidden-state or rival-identity input.
import base64,json,zlib
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rM%!ERhha{L#b`yjF@O6wa(>KzG74F!tY#(E$O2JjjNjP+sco8f;qEwZ~`zl@BC%vVim#wQU?v0qiatg6h&$jG1n`|MwT{p}xr|LyFbem?tn{pr)$m(|(7{rVsO@}CbMJpA~NUw`}ezyH_6&p)62@cD1QT>td`!}ZPC>g>(!_H1?jW%c;+$Gh9NpWoa+e7=3RxqkTf<?c88Klt=+v-vprlfo~){LkuWl<(jC<@3kM7?SaR+T7e6M)dXj-@U)voQWTjX+HjbHk2PezrT6=%fqtWfByQ{`;kmWIh`N>@bEC}|MA(*7wzWy%?7R6&u2f~-rc|ZI(78ZcJt|e`jK2?Xb<^IeEJXTqap1dI)C~qu6Z&tZy0Z`=kG0k{ch=|@8U2V^4mC|Pn*r#hyVLwb94LC+3LbyuBUaF+8224(`?ZCJ^r9aG<)u!|L@mF&yCNBD+br_r~CbLj>a*2;^ulj(@(dbgH_JW8L!9o`hIgqW}U6}?m2Li%%)P<EXI@LdLQ24<7B2!i9^|a^7#Gr_q|)|V?#^lJA2&mD80pBYg0dbCw<;RQ;*M`yw{Oy@4x%_jPQ7S<&RJ5OMMVdR{hZ}n0_=j`SM$yyBd6I@fKLR*yQ=l+|p$qIsmZcX9hUnan5BwV4>m7HCsdBfs8xF>8ssY`RoUBSH(p=+*M%vEcxQ>OG;n+=Jw`h^XC4SKX2~t-`~9d=dS}yyywhAPW;NrS1R|C43J*D%mJM}e&)^x|0*2*d}Ta`N?)b$DO00C|A9Q>?cMFi%>MR%+M`3ojBVzMUt|`&oBHEpz4ri@f32^+r>UiD76<K*=hzW2VuIOPR&CK+18`8r7c&{c<DitAQ}HnOYyS9uh{*sSZGU^CLHo-kAGCiL`(rOIg#41HMVJg*P8r=M`#JB1^0ZmlW}CTmIK;3|^xZ8(oyH~iPI`?ExxN1Xd<hDyzR^%BUcfwRFfp`It^)t5cR&FjH@Rclr<U?2fWy82VSeA1pps-F*~h!1bbs*cg=H?s{B~S*yf-5*H=hXN2Km+dmDvAa0Sx}FWdwP~5+yLTaXCb+`7pF0GX>kro2ni>#A6zRrcuWJYu;Vo{k1c2{_XoOLa65ck*Qbr>Hh9|`@`n$?r+}vo=#%!r9h}-@_^<j!2AIo48}5B?6TK02ZWFP!=r_kG0|b&;JLH^?t>#af3b!SI9+S;oc%#JeW7s{9wHN051ga>nH8Mdcp>e-C3SAS6(fER0dm5x^pk*}MlqfFN8dN7bL`H&TI9|}PvDg98^tJ}+ka!e<TLtjF>wD5{I_${Imxs5a7f6lFx@5RhKhb4x2f#1)=%2sM*APY6$s9$MV=r7FF@oGthqVG?eR@@bX-cng>Wm7eI7<Xy&@$xM0gRv<o4Eacp7|Fw#P=o)OgqIFH;2l8Gt7pigHR&3N(0F@ue>EUfE*MH&93^1IOg>)r04Q;sEeedF4az^zfC?>7V&?3*6JAuSfrP>K+}BW7tY2&t;ot$p{L#=qf<eCBq!z5~2nBUAdYgAVhF{SN)n@1hxLsfjwORG)d~82xvq%CL73e`K+h)UM&`5$Fr)svEbgxR;q(E0sNBqc}rc`{a5lStm0CP!#E9~KX<SlD98bGiR*0HHSu+U4+N~K5CIa8mrZP&cof3|LXUqJ?V99)UG@iZJ&}WmQri<p0R7sH<lI$)t{*u15R)rn|1CU>Iawe|SmHy++XlGn7_qk_K<gP14W%*ik{L#VL;S&~EkrVl;|UI$Tp{T_{UN3c<TRVuYLYbQJ!niw(D$*=pWny+P7&V|dejx@_gVev<h7mDzXqALcAB3T1TjPy{AFnsYw>xu%;_)Gi(?4`*MR}016h_0KU%HJA|D;xL8RpE@X`KN?{D7<=tl{A$YcO_Hl+T#d4DhifGTGRU2Omkahe9*jmWHHmNUmCb*kgxD&w?hW%Qr|ndxOfGP<SWV-a`STTI|gL5CMijF5Bv*X=lb@r6fUZswUMY#x1Afm0>8a}<?hm{5U1jB27<6CywZFx%7-Y2w1bY8ALY*jYX;)wqXvhjaB54!G}|<HXO#@`xDeG~XUIXy7RIs$6vH;HMvzyw|-4k$Pv~InzlL2XwHA+uMhKu6AeV!$x|0R-qw)4ZoiY1-j?hpfkEe)Bzs&e}vx^Lq6b{g2OVt9&`)LqL+Gn3O3!LBB&HOCa1gMBG#-6R6f;c2?C9X9!Ab79S|+%E0@;%@Aub_x3`}*EQz%L58SPp6BNXOfgF=Eohy;9=wY1up&jT}!s(E|$FFL(E1h>U=u`oxJE+WxFWyL|q4znx>D=|{S4<Yx;c<Juxt(9lVCeCOXv=bO1S#4&Y~VHo+et3EFxmiTd<#R3yOSw?fVvnS_wcDN3_lzEHc)tZ80?X;ssh|-oQNr&su##xf${XCr6SFSqB(+jEZI%DVd0BYoot9rP_eG@Ovu7~;@Jjvl37?kY)`l~R)Xy(4G(|}WggDrxo%8r1kROw<1F>3q@b!^1lSodWvtalmX1vA5|XqgpVS9gsB)5N+2l&j{_fPc)U%N^bM=(o4_p!w{H7fA9bO!|qL~Io0huyT`j-_JQ-K;9X-?$>Q;$^vAF6B|B(>%%e_2GRnff29CDcjpW+K?l%4k#7&?C=<0Ux65JR4h%rr#lG0unhJ<r)tu)}j#dtVm`RII&~$>(oz*3qrD-b*co*bn<ZtD#EhLd4@%0X{%Cxk7W)4C;9l3+N=&%<PnYf5){!*@#)oxC|OgYqJ)8>P&dzsl7SG8Kq|Y1Q|o%MnaCxti%3>sZt|s@jRv-~KyA^}C>tbC%XW@UYtA4zG@}6L`lwZIEfQ^{c+F53Kd!44?|s*E0;z5JwqKq+;T}`Uwa8<gcyK%@AWW<e?{EI{lw5-YZu<0=0;{_1xH=*{GOkYHPs4(MRz$EO`r8FX%}eb}=X5j-hH|8IQ)BW$dIIx#SqP{(7fV)pI$$>Xc-2Q2G)4%(&^bre&52L8tv7yFcBh=vys$I-C0%f<S}99n(1-!>Y+*(eIY_=xM<D~VY6`WhH-fgpg>d2FO5{FcgRNbhwxf#+2R+NGF%fRL+e~5drD_;{VKqpa@#Gvb=2GIYEV$09CuvncRT>75Z`D?7&l3h(sGiwfYJp`VD)jM)9{N1ntXn!H#+7>oW$R(sQmC85XEfLm+|q4JYUny6cPh{}(D?%jjf=KY;z%L2_<#d3V|PUzak%SiX)US-D0qI%oE%#lVEK%e%$6Iy6nsq#?yN!T4jdAaPIH@@wQ=y5%j+z2sm+zpXgrB+fThmM#&}m7SeTrdM&a6IfLe_y(5QZsN6GpdS4+rdX-1^lNg3zFX!e_0?FCH3nw>P(URm+r0*#n4geXpBV!p1<jJkg5zXy)=0DwJRPe$AJ%5$<=)U_d1wu7mNqg>6f_hZJhPGhwMnz~L~7-nr!5*KCE>#>TbSz|=&t+`pg1r2Y?^b@2#1dBH^M1GAmNN1jXhvftI4B)Ats2SkA`|&XBYbft0_jIGT75NmRmWJwHC7wXhGQj4HP8bWHayNcVf4kWh)LL)(vJY%7$~tMF=aDrfS&CAwA80OUtkhr58N$+CI9O^v^X3&<4n<_(t|ZV(eb_3-@*tadf<~C7+ls*H?Lx-{jMVJW>97a#maK;_XDTJ&RWB`II$?<Fq#4`9V`N7hAcQ;|zpG(nV0-v#L=6~eMUI0C=ux&g#k&>_Ks3^!J!(4Oz_v>4cy)4YprQ_RS^E%`OPhd!Nu@u(sEDT%5+<n(mSk=~t|&{E2P}p;ZL}A}MmzVFjads>k^E&Qgh?If%NmsQCr!A+6d2%k#l}LADiND2SSJ8Me$<*42&mM@O1>xQxwYeMJXSnk6}BRWgkU2la4Un`XZjbw*O-4~*w4AqY%dlrsuxD@t%wuxrY9}W2k?1-#RGIs%`qkg8CCD8TK-W7cxF%9(L}Lz^fgPMZhReFL5$R+W)mqW(i85!!!8`p_4j>ru1u|N5ep^E7I^N(!h~_w6fvoyqPQ8jzc!=#&iU09`~PvKdRBsla4}fV?WLP~-GB~9(;-W%aQbCxO`2{pnV1zF7;d|Sb_&<Y?V@jaYZ#DdonDql?}pHdCf+mrlW|}ikHz@m!%$jihc(W>2cZ&%ZNZ7tv4o$o$`%251MJN7;Nk**ng`(UQZ{#CM>mtH_uHv(3hGo%P*yR-+`YL`TDi!DLY^9Tyf``D0n!w0lw+;I0r*=2?Ge)aWnoS%YgO<6F3HGomP>m<`h*iL1lyH_?G}Q9<G<F9zJa;45ht*avV@po(o5SSOA`RcTIOLIv?Sr3khUZ!&Ziw%l(Q(`B;v-p(i9-LBX<YgeghU!?u>9C(1I_g?%Nt^gy#q!OVvSPCEd(cNf)U!1df%Lv?wL<+`-93Q$%@3p>Bag!Rug98ZroK(j&%B8TQi`PisyxQ!d$q6^%0{F6-QtVfj;&5-qM4WxrYfx4qrs*n5t!4SDS>!@*i0kg%MdEagGRxGNF#7S~d1bFyN*M|XDJA(!CT@Yo1JfCypUaRmqseu+CZB-|YSR7RD}Tbieqcmb{2iH(L(CjW)WV;<HFoz_laQ)0X$7B4SHQk5oJaFmcaY84QpTSh!{_z#02NvvPQdFVy^e@dqSqJYT6_9zY(z*gA?(SOE;3OUUIrr(RYPlRn=%u;u``!olfw#RGgM9Dk~ZRq7E`)WiNRzM5jDV1lAP8Pn)>o(g^J;N*zPZncExs#lQ@noZ~7wYfF?Z-@#t8!I3(KW;bY)eVOpbZw)?>0Ac`1Le4piS;(Dk&A2YQzR8omn)o;`Ved>@5V-3D=jNMb4{**T2^kPl6{Tuw(p@V?msSk%m0ObGbk(WzP&^1gqT7Nyyj1eeGU)5HAXrfJ_!J({^fh#^dq;<Y9O#(L1asUTM9DbU-NBJ-QJFu;h;46}Yd#X}}aH(mUdWz(Vpm4`~3kpMljZ?hzdC-dfWln89Y$8q<3U#(P+ttf^=j{}6W?3jjAi{s=~i*eGBuF|3CXRgCAsbeqb4`XYEy5zq%t?!~vx{KF5g288`<JrAb3mJ5*M1EL`DTgvehi8Mlvvg7?$@7k`)zo&StV^q^YFP*S7#z)EZ(i{!X0G_zM!P<c~FBJoqSI5C4AzeqX2~uG@WDWF|sr@l%#CWew@=iR4aHk3@@lok5xd0sjw<>g?eEX!*sSDYiT-mn}*KcI3&~x@Z94YfgQODSNcZ8f^fwP3*sd)dCxH`V;j{Qu+J5gQhXxF<@GL^*JCqRhH%J$1hXbPp(y<}ElVWYa+VkV`hG;7~OV1(c#$kXV~&901`Wuelfz1*;c(}Af;8edOOCO7`{qD>mt#xp>W%nDj$;s(SOau701xnqXlKq+94k_J2iCuO{XE}w%5I7p8pBM~=~Q(*dpY{|Y3>*bdLJtba$gPs!QMEqLj++D?i7=<4j;rTk9hpBx>b(lQntr3y%FkNMsh{zgj(!kU9NljeikUCN9US&R86*P(kPr_kZj)g1cb>zN1X{cvBpLj^Nd=z0vXX<WN-wrYo#yoW|i)KC|*EHbNFh%fO9JP>GpJt-t>Q09mBkmK5=||dlHWa?rUj6au$h;g8lUM*3JgDFl(SYO5K{Rot3Qcp?=3ZMhnXgo9oe@6p4xCT82Ch`K;I~HdbiSsema-(N3B0saD?k8oPUM9P;Yim~8uiJ&Ht^ofqUJ*1BVF?E^gfzmsaK^IM~n%@sT4V&Uh!<>9;X);XDB!|==FBCG{c+0B2ktIA3=;+RZ2MtKmdQrj(0pp!j8*e0otRH6aY{tSQXD1iTsrS4X6NHDz!+Pl-lJ_?X><_WT2o<c#3lU{fE>2d6_h13;!n;`)6N6i0S7OGfAipUGUXuOJ1SfHxk)lvYl9yw!Ky`eUB5nt>?Cf6!lX`OQ!Qvfyg1;Y$kNjcp>77BX|5oA(UpiK-x*7u0ls@&C>bQq&=5!+VwVlAD2?m3{T-i0APIoAg`J%B0+>|%Gx_?T{(djWh=l4CYpBqLHqpDl6p)Z39{(wV$UU~+40jww`OBmo!;bpvPQ}0{Oe(EmupiHZTbBBm_tm%$1E{wDHqgrtDHX~uw{jTR1ocB_aiV7rwX0~umftuC6^~LnO<#wqfN>2t9TgA-R*tH`k?Bt$qR5Y2o*<%DH9TrPg=(y0S0(zjMM_6BE_^PLj*yx%X`GOB~vIs@n%*@IDvJdiPV(!_=4HKoV$PW9=IsB^kY<~Y7=LJ@l?ld02V{rTe$VL9>Vx_n3rFcmTOGP5}zC3i9OUMs3X`1>4{-DDJzKGUKOUuGCDDW24d_IBVY$1|Knx)Jh%q}CGa%j#8aRd3J&4~7lZUb<=XvsqIb*QURVJLqh<5^9WKF8A$;gpam%8?p}*dZ6a#w!wsz_MFQ7VH_8R)H#B96(y#>+PkRZw|<HA}Pc-LGZ2V_G-x^bGf_vKq-6Pw;XmnEqZ(woprwwZPG1Gp<dcf@Q5r^8@X-Z+e=#r$Me?^Mu&C*MmXC8!Dcl>H<g#Fun&Tc94oN9cg3E<y36Z7%cySv_{bf(3g}CxufhtR196ITJ2*3c%1GO5z|mccTv_5l=}{i5jYkI|wZ0b-_{?2I{E#axl2YN%xF`o#ji4nLyK1Kg-0B&J^Kuguag2M(0QEe1>%!F}p|V3?eyAiGM4>H$B`K8_J#=HY*-DbVFn{xrVKfbw%yWXqUgl&{Vn2>yob!IXgnVnA8Mi9AsOg^Y?@cK|Fy~46SP*l0)_J4(u+1<QIy>dr)}A1@=fm`@aep9U?5+Y0WM(De&F9Y}`{<9x(~Vaj&X?x>_m@^)^;5wpfz>iW?&y@C*(!ik?fsO|LjYRL3zF)MK-bEs|i`b84RwF$2!{9?-H4C8FIPaUIEsA*c>bh0<}L+=8qO8D%4^<jzy1-sbxtV`A$jYOy9o5n8Bz^S09&VJX3lBBj8PIb6(`m?a_tITSjCRoUCX(u5sl&O(fdrSbeaO`J74(FWD%Uv?WR)Y1c)XqVKc@G0SGYIX}xw1;TcU^5IhEukQ%x`t5kr5b(!4nPJRS;EMqN9F16qzt2(DRb9VUdcJTG|R}XQ&lZfcn008v<+pY^+}?>?$I;w|1$8HRT-c`>l^VF?yM%h#GLX|fMeDQjyYnBmsC}+e|rDn`s-J`+iX5QZKqSRcaG7R=~Ll{hMlNhsSQz^$$4^r`{DZj_Up2Cyj;;$-rEKp%7|BM${<RBnmgpG)2g$UY6f7Wuf#E0!)7}mX{Q#$I6;MK3ADo_Vm*YM^TX%&H*bG=ILz)pn??EL=iSBnwB3|U-MD*n%Jz7(nVmjnT2!S?q;5VKq4Bn@E>DbkBA2$K_{qA;6pl1gEVW(>NVRi)#c6zu&=6+`QIRPj?>$$N7s%C;wP#_({RbMHSV@HylFUBVjPQ}S^NXVVuid7&k#uM2?PU;5!l|kBs<Kt+Am0U?=@yr-T{R_GH;ReE3w11F;xeUnUIM}hVU_k<wzfFcLlNWziyfkD`tAE43r(X`M0_|MzkV&epiDa55tWv*&%z$y?4nKXSA*SD+;#DQ8kQ6i=cgx*%u*JtfkkNpc2t^(-)dzXqZQWDoUT%^?NCcJU3`-k#9h_f*uWcCsIoIz9OOY-0mRkfvZ>=d-yeh|a}rS;1>UratEM{CU*o!or0;M69M4Z00nb#aGd0FYxk#zr4)(-68mg0nJcQi8S`7C9=^~qEZg}a#cw0$J<PrUPG^ZQfE=F0<sD3_Da8k2TmI$SosyhJaVfB-|hXK3V%M}TfvqEZ;r0Nc*$s?D<Q{HhZ&nswXf1gSpZ1UE{|J27WjQI#rek+8K0X5O&o;2Ha0<ncSnu1zat-H%EVk}4~`d)iO?jfHESJ*D<^VvIwmHn_PQN?d4Fsm|l!Ke_|Zy_@?t#}pghWaEzW9cY~Fl|&RnPL!lXPIxVn4A7}yVdBO6sxiiG5jBQyPxi~3RMEw5=XXtQNaC4wfS_KraOemto8k*ujFw5QaVd{6Tn-Ml4LmlhC5!ZiyNAXrm9Dtja)>5v<Tz`hY*xLMhJT)lbVO{xwZ~7^h*g@#Xdz;Zkde-#E7v$l&63YI~64@sTOgHE}BG|Hl{@c$1Uh;U7_4mIx}Brf#wEU<?-X4p^s6Rv3NmSXAdq?Tz)RfP>fWIF&=9&r)NNn9q}qeu#z`(H84#-i+)in(yg?L(w%rZ+A0NRNHlRqZ{ywzX;j_p`n!Y<WVnOX9Cvia(e8JYuDNEWkwGhlt!$AYcaXZ|eL?gEhnp=s6>El3XWhWBF)8evUSlMv)>a3dEctPfepq3<bb5Bpx<kHbS0hNSs(<X0LW{JsiAkd7xM_~On;qb2y&dM!T0)~mYEi|b;1MCy;Ili&&7%8qm`i$eo5Fbl+Xb(vT(~C3Oc9bovm@#r(LfQ$xJYV_F<*BG&F)_lH1J{+9Q!f3LKlSL8#f*>WrpT7tgI4@Bw^8$<rd-@3YLsH3V4miXo)Qvj7R{2ya0|QLe}66;Kjq7NKt|wA1_mC*qK`8K~m=kvE6;F6$6t$%$j%Sd+}m14s*0GE>2D+iU)5WZ@Cz%ytDR|cOH-Gbpl$g7x9S*{81=sI1#6#z=d#qZKHDFTPp1Eat?R4)yC^RFvrr=S%~e87u6w_ALo(Pyi($L2dn`;7Bhg1XQE{c3au7Uhc6d!#OiNGf&9`QWa5e^wJqC<c#^6rFG4rSOtV2K?=Z=cxoOA6;xk){WO96t{x@S^i9?qaG%?KEZi%f|PPJ>++=N{Jh{~J#Jwb{%31g39*EDWI(IJ@-WOgybu$D=-4RPUjB|>V|Z};s;D59&n<w+#Q(5Zf>^>q0`jvXUq1x`1Z6`+`K>gI@@vbA0qjIw#i4<-nL)H>4Aknh6gqErfaEBeO3X;+uY%g05foKLT&<;qu_SGu{gV~6rJkiE=Y_z@lq8#^6>G7WS!%<m0>yEybt2#^$7_F+B@-VNH3Sp=)R{{5pWYXQe~aT7&x@g-SVR@zqv{5GOEF<e8*UP_Pev0p}GC~lHCI-H#sQxX?}{+W$Z8LSewrgWLM&gGX59;6&HOhLvsL7)Klq+JpkJBt5g%CeH}EU>Iw{d#bd2GVsoCN-ySu@R=9Qh}R$gcccXU>FP1R;of!OLIv)$yT%Uy>q+K#m>A%9O%UxgC#FbLFxQVDTaZJDK(&57)3tgXm~U`|2x*>XyzU*;KL~52pFjuz0g;M8X}z#@X?nQ)hVyAIyw?Obg9@z<?UnYCxBZDX}%WJ4V>Y`4&yd%E2k8)d!r~d<VXdbacQ<>wdpl(#m7m;EPS1?wJ4s&E(g{K7rshDkHt-)som(xzC7gjqq?QJ%w%GgvUXf*c9-ZDlLntszkuBkvRfKE$<W$KiKWW}eL9I=PWJKc6k1o38}Q;{HB{Ls;}3Ps(?14c#58>_7S%wNtD%mO+HWJ-v%J4m6>%BBu<^+!e$xdhIa|;C3I|Oj=msNQj31n{Q#^*h!y{b=7}<(D6?}_I!{YlO1B{!Mfz4V!j%Lt`rH$FMpdbysbyN#gQ&MOrw3lQ-QNz;NbXSi3C!H#AKq1mk9f)JlC|?MN*jCUj(ot0p<dy=^7_HbD3k9)V%X?cz4YQ3a4qT8q@R2!mq|u`vYA5w-zn2BFz!aEPoRXK{XX3pX(2N&F3QNrp>-K_ANX}N8hJ9CGYGV3Uv@Pyc(13L*h?~PYH2{lW{^+jmwk`6bS-)2i(6U#5Olo1M@#JiWyj(7nib9~4cc*8?KCCK+Zs4R4CU2XhGPZ1&<bo8-P$yH$P}xwy%cN|WK<7#DKi2pPtSsw_WynZ)9G<H$er;Mp>B^8lP(>BBYh-Uu=#$N`r69?3xfsKl5M2HMe4o5bs@BB3qRl+n7Hxc|sByDchj}2TL-;?kK*?8Eu2jbK%BDacmKcjQ*~2HQmCD5Lb|A68yi3y!k9**}Q#w_+oT!^eFYgo71@f|w3M`gplv)Ha96iL7Chf)OG$mCqQ%6<?2;zu{D{WR|xsQqS!lVHz;A0@f(4-G%hwxpd4m{ihXyY`Tm%^;7Oeh7QdTbr9_m3u4IBuPWB+2mx5e-}3#H(|tFqkg}NY>N@$&6aan)c4p`jWWLF{ezmg%vYX^nF;=PRJ2|A%>LMcs0>5x>PHP(m`7SaTO3v-Hk2~98#HO_V3y9(k2dNnY!+Sb${7;$p9eN&U68Ky%36Vkg8QrssvVBWi78o6Dg+OX@G#>D@>B7?>f=^LZNhyz9};H!^yJ}GBip#Co@+{*YQ-P*(r3)*jbszUqyj-%XGf}qZNLQme5&-^H_<|ic&+Tn^n9WKHlBF{ru*hprynuB)LY0+0uCZd6aTkiqS6f>M}c;Eo$U*NsFzFJ82!bBkH_-%|{q?WL_)>P}=ogT#3eZ+IYssF78^SM@|_HuA63Py4b-OWbEwy0jer&U@sP$vb?y<5>Db0z1kfnyd+w)T0xM^x~Nj;LsPD2ZndQyD#Rm9`3~L5wxA4OsJ2YrGd;K+8B)r%8?hB)>Qr{G133$B7toYQCC9{r^&ESX?#0<77Hl3jz7fujC~?x#a~e#k>&F&|NkFN`E{Zd&%dEBoV<A+JpJWoN=*h*W)NCwBTNLquQQVp|q@A<=MvR#&YEj>Z5K{^*arruu)zB4Hfa!=X6VsTN@u;BiT&i+Eu@*21L;%}JZ0GzEP-W~1iZclHoiUU(B01>ja0;r)TiJvCNc@@32soPGG5S;P!G4judE>yINikQPSpu1?Tred%vd8sZSH~9}1ifNG*s^v~esyY%MInNsEq(R;s`xGhgj#J|3TrOCHoH#A>Z!#VYj4dCAJk*4!$?-w^}ro*7$YKa-7)ttj+&K<o)RQ8o8x393dU+VGlSHIu?aBxiQTGoL54jBQY!vWs8q<`)c-@02ToFVLn}I9nioW3dH<LS2IXlJ6xf1J`K#1v^}OL!*ippRQ9fQ>mxT(lmWl-rq1|dvhK-*Hi`7U5jrkN7M=Mng5bBX?#32C&Ci%S{SjnQmY6_>Pcc{+i(Kf|6mF(3CQpPE@g?OR|MJWpGq6$4;|LMN2G^xd*9Z(2zTaaHrCjF_lM_lQtRK&~QV(lDwRnda!Rh2Swb}sHSq~DlV`xi|B8i-5UGh2QiDyAHVh=Q!k*>5&^vDW;{X<LSll1NwrA0<V|2+cC8@AM6>+=7#$QrIYLT9T9;VrXxUR7nsQ8T`3HPy&!=45^vqki!HAK}Hi*dOA2dVK(Vjt$>vhHL`%fmM|aEqu5B&wWNHyy^?f|8R>IPO9H|BIZZ1KQjXbQZL^<()2%Yo>|qU8n?MwAU%9-8k>41M0ZUo>%Tl!Hwh%<VCgE<-4$ieGXk4oe-1;YY$3Tq*>{O-lH2dC~Rj6WOQ&>s{Wh#H_vjyRfk)zM3anLI+)QH+C87f}S%N%MAo5|UIHAok?ELzWL$vvTrMNQOGJW7erW)_{JB=J<y?xHkjzg>N`1Wg_yh<CwDM3WxJ7G;5|_LxWY#CI=5bng4*O%h4FT5{cB6sASzf_9EPL+6Gh%G(s(h#|&|nc)*!tM!SkayJJNhf-=dPoWt{u+_0;?h%_Qa!YmBEZ)-wpcgr>08Zil_QUo4?St8zPiC<P04yvaJh|S&j`Un7NC8!R24kgo=EaMVP|SRFUxD<&F$A%gHl&Jq3IrlE1l^%`>sDo4#9(4*x>#e@47?g`!xolhZJkX$uoHLzte5S=dR1eKUP{eJ76}`aG^rHc*w-2_A>%phuoaB^77w=={t+%!4I5Q8=CWP5^U`IZ2`hH6r6cOJ2@@o7N&v0Uc%Za{T^nRXJJNLeB1@jbuk<BMUE?K6RbFYQIH>?`zFaO&k+rA|Hn5-*W%I!zVQ80IZIb?M3SDr=ogu%Oy)gaNQl~*de%pFowQEu!d<P4tP)BpL>}y2qCf+dA>INdgRHN5wD|FyrDB=h_n7{x;@vi24=7$}b$1XIwbcH_{_NBNw1xYU&`7az&*3Za?CPti~VAOimtZvgJw@7XI<=mF9YDpd7Y-J>LplGu(;~qoUSn5P@2;%ZtAqd7w=JzLO{+Wo))hHwZNmCPo2Ti^+nc`9HtQG&wZiLBv-%@}lD9<A%QsAyu{p$kfWPtpTd9*!R-peKJm01v=;x1qzq6%YyMdO5c%_e9jNA5qfXvaSDbqmOaeZOT`A~XKpUz-fOdP2Hl3L<9g>%UfupWQ;fRbltpM$sO%8i8t0W=2uOfMeoH^d?f5RT|TtI^iY|0<%?Sbl(l0a4ei*!;=RS7%B)nfiz=-js3bZa@OX-8ew;+)qNF56^DSFMexgt_1bY-Ox&~9F)qy~vTcd-&~BMg!<JXJX2WC5C0gcy5wb#y38m{eWlX__S0LtiA?B7eqY0B@un%aX1GY()1-J1NQclr+S77LIoXVFb`F&%Gu`N@U-neqgWXK$2Z=?9DZLV}unbi4<7un%;g{<$({{kfJo@)')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
