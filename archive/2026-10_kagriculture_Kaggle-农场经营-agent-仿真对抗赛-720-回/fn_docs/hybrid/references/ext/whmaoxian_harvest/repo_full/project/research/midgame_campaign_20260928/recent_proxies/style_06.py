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
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rk<U2j}ha{MoR=7Tvy(RAKuY1S52HU)~xU}F%5fou>U*gQCS3-aHi6*+hA+^(*w?t4fnPM$Ovj_y6*r@Okk`j`JY`<LH-|Jz@GKl_JY&fedA_;B`ce)g}w{rf-v$EPnoef-;RzyI4`|MS!5U(UY&_?KUAet!GY&AYSnv)8x#v-69G^TpR6e%$TeulmFLyW2M(U*CWF%l^mR&8L4~Jv{vP`AI9^zW(#a_p>%6?ftNO_wM+Z&oB7#?cMIo{eb$rXv+5=-@beE>!)G6|M>YoO)Z(Va^6Ay<#9}{-|^lq2kqU>>m3@iU(SBMy}SSMbC1!d{qDp4{3|)ea1t-lNqqXj_M}PEOP6myk7J&+%xlK$o8`R4#~+4nJ{QO4kiW(Tec0{ZeERKAyLY!gpPg^~;d&Z}`T7Fyed-MwzsC={MT__T>F<9&d2f7295FbCKi^O9Icdk@jk}v=Pr({ku4X(O`<wgS9qDv7*oXI=j`qC$=ja=E&loL;!~WEl^OH}9*W|5xd_jHQKiqy?4goqG7Oy!6?Noi=T1%aG506T7$;bCU)7Td#KWyjnz@Hw}8+{HQU-f7d%-^tF>E$_I8XB-e<PKOn#PR*d&c&9*Z)O9~JY!-D4qFbdw`_a{ym*@6SqrAI&l)iDz0(J1e+(Po_&zYzr@tZhl=J-A=nZ{t_JKV1_3gWNyVv)>{%Lo2|MuP6fBM|6#Bk1R;>4t!J<_)<NmIe~3$9kQ{GSfFMS~I>D;!FEh-R;bKSV9kmum8;CnLys=9|0Q_t`n}^f&w#wgeZp`6hY(WC}huSI))8pNn`0CaVp45{IU#yWg_>7LQ+;|7O?oWmvh2kFR~4+H(Kmus(e=o6I=-M(?x@b?C$NLb<f#L#8$^Z>rK$qGj{gCblCMMjm~dJc|$40zBYW-4xLlUGcQ%y}kbbAus=siV?61JsW8$6s-rc-@!SW+`kO#q6eR{AyPx8cBn;=B<V=@_2D3$Oauen3pW+BJthmroW;aokdte^5qJ^u(bL#WA1si;zr_GbXF2iErV>asxN`vRd~Di~o`MbMb+vL~QglW(+H*F3yt(_wPQ&@rrw1Ju@$s+ID^nxy!~NaO{`=kC-Cw-<o_7NI{K3_qy`b3&(0_mpYy6?MHUK(&c*V59nFYUi!*Sf;xwEh$(Zm{-<$SEgd!~bKKB34DF;EgPdf*(LdbXUZ(iJs5B{g>OgIB{n1my{T(j5a{JlsSX2=sMhKc`pzx2w#)XdnC^HuH{Oy`Y^py`9;4FKyLbw5&R0OPDs2@xo~9@g<X8(E9!ZHxRh@;4!$u{A0itF#nK2qEAL{rk&nYCkLa%U*d#;2Ok?fzZeA)ST&-+d#5FHY=FAO=v$$^fy~BedBlO_Xr$8|WuZiaE<$3<g*9wCqNxXl=QuBNp@DsZ!jJLE9ncSstmuJ!4_rORM?xpyi2X_nMJ$F8pkDMXF4_3XRSN>fPA60BwCAHNG13<evL^6xZB~5j_Js_`@5*eu)xaUxr#YX^;EHV?I{1cbbAAQZCmWNOvP0K~I63G?P=t||Dd5G}A!4r`;93IcBtw)tILhJxBHhZ7tZ@Klq=gaQ?D4DIxc2-^aK%hVc8rr_ETHm250Hcy&=RNazGb@4z+zu=b;jD7Y_wy{A~q@|3+dC{f-3pc0|PNZai3wFq9wfW3KHOL7}hJ?7U1_rSWz!rWq@+~HlAo5yFIQuuw%#@{4qt0p`;7$%ZuX~=O{CKyG~GUpEhO-3>bMq3a&GoIM8!^jMiG=Un)q?(AxCeyIhakQp@e7f!i!`;$>mmnCK903O&-=cLLXYq=U6%^*qA|ygOx}Z5tfM3V|^DL+(8dGBC)Qy1Y^9<L?|)IT&5D9X%?yel(c1fZe1BZ12#H#Kh<K-Qvr^M0BVNVECoWrcV+!E7N0Qphk9p%nIS~I8P?<-7@M>V;hhM15>v$$X1h6#!&OYDW_#zlb@CA_%%E>Y(o$7Xn>=>Er){uF^i0Qu`HrqIH!P3eiEQFaZ+&ytO68|9$mo}n0KPsprhq}d;961tAp?V$r*cdRssKjGd=Z%Vxvp+(rI0i{0|)2a&8R(?!b8(yM_)fl00J}FB!!MtmC8YTC(qx;24<ImzuDPdgLXdV?2Kl&<#cmT1I@+202f2ig?;GjEtv;1_-LzLU5+eo0<DldyX8Jn?-v5Vr(HrCGN9q3Z~`v!|m;d9q*RozQpX7!wk+}APru&aA$~+zucZ_1`!t_8~k%{hrt*~dR}&R5LshjXCxyE@)gs~^aa+~GUpB-YV)_lFXh7O$IFbKUzFC?;|6(s`_x_7A28AIcWBUZEs&S(ao91igYs<bEP`%UyCaUleP^^WksDCFZbiE#?h4w6J}s6e?`pHHz|K>&rm$E}#3RDmqP|TjBA4|cBG71n7Nf~-7Yi)$mO^^yl0gkaNJN3)&zK~SG5<6-Mo8j#9F<j}EuMA|TC|w=Mj$V`(1qYvGFOdoUn5o)thAN*3)b)YrtVJx2zWTHOzX56Hx9)*a_7y%RaPh|ysBP0imZm*9~b~_bV8ojGntK&n>-m@@x=CZ^1iJv-*kq7F^{4h)6t*;eMM=JSIX_bq;enIqziBz#36U1cZF3Qoh~C>toI)XT8s^L0)zR)-b7ylphd)D*R2hrkHSH7x}qE5$(SRKMgS4J2B^0%R|&jwwskv!FGrJx&@w9I6Ee<DhI+AM&Fd!*cv57zo3TnK6r?oE6dL-rX}rN}Bg`Ljx60R&ViJKRD*?o+oEFmQp{yRq%!^cDTZL;?7?<ygRpDszAyO{osvq^D=ju|P=Ji!{3WSj5(z<;1z;^UIiEdd&B?Ax`_qoW<`swYvKR-p>V1rj*0uB>Kg$#Ye|7xJ&AMa`$F>j_4Rp>x<lONnqGzOOAkA5I}Lumla?vK|hO5MmNs%(hFg#=q1%`L?64QU-<bxUX1ijL3rYK3eOIhjc#^3*yN7p^iDVkD#>JOHx%VYC9}FM&xiq<U50##h1~2Q)#Kjs|O1$ubms4m=f0DVBvuQn8z4=~Bh#5oG&FSrTAAFgQ^c${O^g?E|&|%`s%TueRFJ`3m4A2dy?rg-(VJszTvxuapl1c;1q>Ct7DtY{^_m2Eza~+J!;0^&TgoE2E{hY@}!aiz9L!&>WD^r>QY-Wa!60X5c&>+a?`<qv}E_+k8FmP$n(72W33Bx=YBiQ>plow{yppCWxDqn)UX<k`|39^FV6curyYW#fmth(_IEE)iaMZaB)6r!<DZcO|2nWO%|SG8p*2@3btQ3p&-RzF48Z(VhTF2jicDt549Ww9@Q0p?Yq@05*1i-zwDW!t!s+;<*0ZoFp5)+)>3AylXr31)*eX)j>an)Wm1yj`+CqBL{P|(jd8fCqhS8h0(~Q=1hB|D$4orAfPO|KR1eUgw4GyhKr()Xz;&7>q==+>8Zb2GB1gyu*r23J3}!)){C|zBmkmzt$|eH_^l3D;b08!Fg2)Mulx`p7euF5%h}K3{0c}5$bjjSm0qgUK&Z^A;nh#bj<0*_qAdzFKz)F$g1-P?qwy`*7QR{K+BrQ)^NU13wtnr?usgI}+pmu?cH$HuRfBVzT{jKNZG3$*=%co@*pWZ&C(AY(ZsOA+q1waxgqp|t`_QZ%$^ieWf3@VA_t5UTBCSWkAAPB1>0ij8v2GwCy(TW-_3|DBvzDmxxxEP5Nz}<EIP>@rGo~i#O%8aH~!*jqQOs|l6=sYnC_7`&}1ixiPWpoqqp;-$|y#HYNJqG2s4O6?4wo~Jn0566osEKJn97|V*_)@0|2qB7TiekN(a~C#lF?$Jo<>M#ln2h@V^Z#pzi$wWUOc;60%)ZLaiA@ddiW|bW`<WF5d;*)kV0Mh;dMl`6J|X<p^BFezN*UnkM1h28A_3ql#u(#&bJHwNSKx&c0BW9bR<vk7h0!NbyNvNC3mru1X5k(p7N(?tvqg$3?k;#`g+QomQ;icD?dwdA%``bSBlCKrONT<I_>=%cMqI|de!w%PuFtR1r{Bt?6?DahpPxRC(n^gEam$Xfj2Ha^3kg?B<UY|rkS{I?3Qdv#t#_S)F&Y71F1vwk+N0$&pA~L8VM{#cGvu5MRBNaQW5`%A%SUo~3>21-iAKP=pd4RdkReV9iQ%9g788%CN0c2_`ih~SQgU-mL79#>J)*$cWk}@QqNHbA$<HyD9sQ#xc2_Aa;V6Mx2}^mBYdPx(`dS^j&I{vT7!Jy7lt?@)3yIX3DTLKc%-4%TubA&pufi$AMzNR8l8egO?zFj;h>YSUy)39y<zdBm%M@SNg0vkj=7TPsy<W}XRGQ)3FsTS<dw?<%@L|D0Z=hQ0zjac#{XFDo%pgnD=!U4+=?`pdQFg~8THXAYEd1MZ!lKOpmMWY@1|_9|Hh$%ngi&c88F3|KJ|}Q{TONkLiqrE?tdhh7%q;5OdS)_o$N)o0ddMe5?vE?EldTvAbpZz)2xumCv{=H$Za52zMDkCk6h~Z8*vN`*x7UNOS;5i~7=1`9u$HM#a8()t!{lC@&kd=8e6VyI3xWBy_&7LWVUu+{@OZHCI4ByNwva~c#=wvBO~fzWd56?FJdh4&A#z4?k_hAxT#Kye?L(nxUFw!|T;ZHhe8$%Zp_oUfs#-m%<^}KqxD{mf#ww0Xo<B+jBe#M4v!DiER<xKAeJavHi0_6r4770yhF?wX6hb(8FcKT^HH(;JO%#i-sW7_=85fdGrHRr}Z6j)cB7evq@=gg|JJenQ*+n#PWkun*X0dHc59A7Uv!Uq$z_!8)#J*3xHW?U;;t2%^%{unNj^*php-aFq0DvWqj~jP`ysD}+R?q|Vr$4hNJFzI@!Qk6RL}2NsS#wLPljJPSmYZF?N?6$y8VpOt(clRhLF^*Tx|xWydr;k`vZ+WS506)JHp0l2A@_=Z;A<_b72BOK6HX4yh$iV&0xJTxEmqM3F99M!{HTDRNgFq_@aXP`AIxJOo`Aq1gz`WX&{*uSc81($1?!5fT{O;~iVIsWPb1%!Z$TGCOz?8s?B>m$ETpnnK4gFbVT`ou8Tp`H&tAb}lyM(h?4{Nb;n~Hy_-5ANR8ODK#3eFuJvx!csg<>c+u(mW7N@|9tYMiDy>VnBuXR#NbOvHzfW-P>G5f75>8STaZT+N=fuk*h-mJh06E3%-fwYAyr`}gJ2gX|-L+OArB>REmHL|!;B~Yo8nfrC|K=ujsWGI=%@sMfCZ#=bt>mj(xDst9QRp_QJB$KapS2KJDHkW_~UExNfAM05}ar;4-YdOD|Cr(5>7oD)r*ddt}5`(IwUV!5mtel0jRY6iskA!BF*5E*WS}<Iau@&;0VNbo)0v9tU_|f+>M`%Rm#r$phaKM|o?QF{Oish&;Z%UQ<PX+y-LH&dW9T;`QQRvTIxN9eAg;iA5j1Ysyuq!G+;E_NU7bENuzJle6&Di7=r%E;&Jw+W|6$S+5Gyd&ErHT<)T|oW=fDXBP%e>mFhh}Y-Sup*DtFn|y3|oW5P$k`?aR6{iUcAMWt|Xb8={6^65*#0Bgj;xllZbUl&MrQ%1_t<*e;d6Hq-)H}&NO&}uDuFigQg;yEtJ+Ix-5^HSF=5mjDqbs*$S4lkb-5n7qkNi#+RfCq;AugB8N!*!n^01SstVcqV3HyfRWprb+4<7HpbnE&#lb6)Rb7x&8YESDOdyyVV=a^fpP@Pn%dyBI%(05jS<Wk&*QvcI;t6NrlPJru6vOitSH=SUz%=jC3YrMqr3_UUK(S$**HR99A8tgu!uNrN^#(P56i7?^IqWspQGVd#o+}CJ4A)2p_D;=a!-=MS0-VE7Zvlpe&|Ur>|LEQ`kxcDtVC#b*-H3sP;5&B%R28CtJU*nr<7s*Mn;{#lVC?|HC4=@nHffogt5~XExzm%6viS8p8CJx<Ql|-qaZo|T_|x2DyoIwM2&{ipLpe=PFVgIB?d>o;sAjLl)t+6?-8n4EA;^GCVKc28&a2NwtZt?fI^L!WY5E}Z`nm;3IF`YU_)Ebc4(|#=B9Am*o*}a$qp%nmhv=Y;l0&}2iDGt<tM<<CxK+69~{$Il?q`gGsdzNAR&P`b+pH9;maF4Qh|N9PGNP1IE+$8Q2>?RJbrDQc&6918KBu~Cka9S$XE2WofHe0)C~LxtWcmtC0rmW0fP@Em-?j{DvT$-yBd)`hhLzvPy>SkxpeSLSsTug4s?gq`ZOp-b`(4l8Ysgk$zp(QRg4G8h$Hd{7S}$ZAQrSS-3+oc;f?v3ypWYs#Z1&yY$oYItFcfDfR&1N<tulFK7OHGhgb5;FoaG{;#g2MCB;+%o$y`*g6Cvc(1JOnRLe4sTZb~Pqg}MEy22EIVSp3p+DSOfQNo;Cv|tZj4$UQb%vO0;b_feKjZYT=kROwu|GWV%{T!L86xKJ%A6`|0LPS4PrRp+KTLG+>xWsF6Vgw&9)>3d%AnO9{JG1Brq@UuA%toKFm})*ZAhi_g1Qw+(upO^UH(b?=Z(gSLTK2{Vheo+@)!8|_=_H7$r4;jjK}N7E2xAqgx!4S#E7|d=#7u@$X=gr+6j+%m;KmekZ~)PoaeFU8`!sv<T(MdbKgKI<0t}DX&-u8+LM|4aCEMjJ+n}UXt34Otk&c5lnY%(461WbS0syV}bBu>ROBz!_dI*oZkPFDS|Jry1vVABy*sCHl5RODIEaq4MK>(1czBm%(d30SU;q6k)FybQgT+yHDimgKu{S2NIqUR*s*@+N0J*{Y`&w;sj%hU6T;v+q}G`p1*nCCi6BMTt&WeFFfts8|eMN;vL?kye_NK7bCKtnkrZb2_O>?(>PfvW0t$;)(c=@K~L;K`VzDzu~|-)hN>FjOkOk@Ooc7tYneWlKuAG~DPtD4wi^qynP%(ukC-x$7q^!C&eEDJ|I-Kh40pn!2Du?dyK3mXQa4^!(^FFclS3AVpw|W3m_sDNDdrmf>0GKv722UtI+ck-`#{oDx#aRyt6jhq+df@wi6h2o^6(SBDl)5FU6j(TXKn*eqw2vs1~vVx}=cw~Z3S!gNT3i5`B`tANSND&OQxE&i#U+-a2tA#6<n`FQF5a!VlvTy<h9b9cvU3MCY{@k)uiQYB!j%TX0dq_iHDUE-!Z?02q5RaqlU7L2P{6%aOX@)^rw{WwaTJ}%y2A{DIYsX(!*dq(7<9SX$xT7aTajKsjn1ty+5W!nPeht{)-KhygT+(EFxeL<cWSIa5I+^cs{7CGYA4;?`!dKhr=mNZ-;T}dZ7u@DXCyh~N)NolhHLeHgEJ!bW5+25F=O9A6~wNA6;`7w}CaK)kLY|}4&oq!ye^AM1%YOO2cvaNG*?5rk3&1I`Pe8}~x)Xj+Ivoc=!mR+C3PfctAbwG=xDPzC9<GKKc&%hCEPGRD#)p4Qu+-or?g=NT-o~g2pDr7_a9eM~sRDZo>uSOAqC$6%s(Jx6v*vFHiKW>U|xw+ttG^dL-LiPS$-FpQbXS)`ipjEjg*X`gDF6P)1+8ITP+Fm`_q<D46DJhhrU`iAn5Yt8^Y5rJ@y)<^jWk->Vhr{2z{Xt8hxaNN|=K-H*EVXQJFQHTmZn#1*m%7U2rcyhT#Tz#cQF>jObgO77zyjkLgSN%zRoA!xu5=F)?I&h;$e~8YaGLotU>1OF5<eUZuaJ#m)R*Oa=ytN&-ldFCvKeqb%yZMNh(t_8I(X3^%nN<46mHIe5|N0mM$h5=ejdl~P#)Fst0@ttST&2=S*&6Y`Jh?;uLdgKWViGmfwS^*S~s)QD~M38A-jNT!bHoaQk++_LaBlc?CV7Ket&oS=Hu)85hW8$_DdbvGCe7y(*x5z_N?@#oU+`A@7A%+*)SF>r!neM&A622q-nCIni2ziR!jaMy=9ASV-cX&Q{B2y7SZ3*#ZiT=+f0!mObu64NtWc@@7A-pz>=U0@|^y!OE|2mA<dvRzv4;s<PYDNbvF%TS;;F)G@q^tCD9T8ZU&M!RTUY8FT}Z#Iw*zGy&h=K^ko>M$RiYxltQm4P02YIGB~Ua>v@350suD?ucMM(9fz&Q7;80}qD?7bs;g#|7mJS0b6gF!j0}gAiJvZqaTQYraxTItoZ~IY>LO)un;AMpe??WOPYwo@>0Q26Xf>U*2}K=maODRlK(6ZTLrY7Drf<z$=*TIFu9#6186*%H$PA0gGd@x_L7bCRC=Jgj8ae?q9z@$01Yyc}%Ql4^^6+#~yQZpk6w#7s6@eew;DPIbS1?nz&QWw&Ff?M@9u-fDKvXuik@*ESNU)l@L+ctrp1!Ac=*O5>lLDH|7Ebww4)zP+1C4rPJXqeWMa)VVRjVMcS69w!7*P_-iAu_;^ITG)E5L&et!<YT3gr5hORWeNCOdCd8YWl}qc`IN!p&IsXv{WZIHax|$p~Fp-bl4mM65+(xV~*)xv~>j>!2q=BPuw}lu-ieC9B6=q#>5ggFin!x<L3?+#73_&*r4Cf($GWn2F9U(J2os{ZsMvY~+i?4p!|ht3yQ<io7aS9%H42tTOpAmPhT;Eb^(^w8Qv%J``F^>o+q!T|x4AT&DHPdM13Z{3CN_7t2ZxU#b;F%<jx3C*xL?52E$8WwtyeGYcAFez2sg)jc|5@g%8alLj-N3(&a!8n`4|8_(FJzeEY1h#<1Hy~0>rJUqv(m=vy~Z`apL@`pyyn1{%$JYy{-yB-v^n)#G_Hp8%rOC)``D}OVl-cnA^FG3K-`b%re^0HVr4Gy<*>W%nXp1Q5vt-V!PcCSUcn`K0*WfXY0>LnR0V97e<3x#yn*-i|J&DmOB2+A!nGoUK3o#~0F3(WLp<-=A`v|JWVA+npqDLeXAT(_F$_V~nvlID+yr-L)X#t-pWlH@~#aWFizX`HKUM^%i#q~WYC7sGRX>LsrQQO}FC8%KsvaW<7O(1@gGA`MrT(gjE&63feQ%?f8ZC;2dCdx*NxE~iH!2$JmLRH_Eb(;{MnY8cZhaY`#V94V^8GB_I1H8OQA<rU6<WR|<HmA4MyC|Yk0VSaC91d9~J2#2T&55{Bxy_OTgO0iRDFUJ`=CO)vzO=+Pof;3({{O<yH;s}08Y-i&KYK&S;zEKb96N8Fa7ZOTJ7>pmijK+P0FKG1x@RcpY->osLVy=G8Yh8nKk4h&C5T>gCg6~9iLnFQc_2KGZzUP|5DB7V#tbF(3H!Mk92GV-srqO2y7XZ20ErvXE^$WEsdevJZ<l~20Ox3|?wKecbxO%dEAS97wq2uTR)^$mIxbn#T2s{Js16B?Mw)Mv_0U(7lrwaw@6Ypyrn=GZE?7|YEN@dRGSq-s&9-`OeX4Hz%uoQp43O92m8};UE=_##rTM9`rMDiK0n6%b96Q|1~DjCt{upGM=M{ju{@fLc>>4PjiRCK3Kag|SPySu%wue?1M9&--8C_t=5e0WCRAqwGEZz35-4x0>ZB<p~v)-`V(-<$#>X~9-;ZmHC}Qqcx*<OHzlYWFS{p~fOlsayqNA*I*n-03s9<>fgo>M(XIn=ybAmbhfA8~lirjV*0?1$9{|T3`tl^@}5<hbYV`0`2Jm9ooMIP@jU!Hl70V=8wXH$|+AJX&n<egGG~8XNVES6)vYUmeI6dQ{0u*7?J+HN&fGpgpGsCSn=Y9ZcmG(#7GpCy6UytWV3!nn-#L4FS)N(ai|x~V8x(uD4h7h+NkeWqhTHuD_2FaE2`Tpi61CR09`wabDv?)wOuSLmR&v!tXZVXwMym%rzZ5VwqB|bf)LCK89FbnP?NS%GH|cuhTPKgH9uLrK_%*)A{K6;TxIKb6Hx+2n_>Jgy)$>D6AVG5CK~4=$qH$NA!^bt*<L4Ph%R*NX~J40R;Zuh<UQ7<2SxUXRa%!BVTd+7%s*xxf4&!T?rjQyVwpU2m)4Sb92<hVu571JN*FLvn@rtkV*sz4<6um{IaS>&s2VZzJ(=@tAyo-d9iazBhca+SRl<x@U5WZOxFKsx{?Y{WBbcN4uG9a)vbKRIRZeEh0i3aL%^wQ45k<p3XRB>q7^rE|pPnT-ZS$<K4x_VB(vX%S8HVTdRH!XR%d_UE#c@aK+n!1=&97Rm7hI3wrl)NW)+{L8aIc36U$=xGlvmo9CJd{C`|g$sA)|pb3xR{2e@RQ?UP~*>@-iigS1Nx~>VYOt(#pwQXr31-!hUyEP0A{;y&^#DA>beth^>7ye@xahHoO$U6Z6ZyC%crhCsdAsT_Uban`Y(X`N%6wMVt#GQ1p^$l3&KzJ;VA1ry9hu>b|EoMX^-Vrjlj@+9J4$Y8G%5)l4D1a<J>{P=tmk-_Z{ENQ<Bf(%31p;Ce-2DzcLq=Yv9j3_V_d1i-VpBgI2kEBIpsci7yduss31NwKZUra6*d^5@Aon@`d6YIH@Qg$}mBmUg-uDxR`otPoyuniNi(#y+MJk`Dl+0)#9_3|OaACVeWikq)QK6&Ty=FAZ_YDu%0a_b#nKMTK@W4&SmWd`Sgdk${zgMRjFT24M}V)n(;*n8?xyz>DQ#VhfNKJ+vmnuXW9mDW$htMkzQme*_?)ca8xR(xOgWO2n&AQo@m(0@cP^5{d;jt0jriSUOiMMCq4%O67$bxiFiO*$llJ05d5t!_JhgP@~MmT?N_(@8l^X1ydFxNq+Y8uvG>Gl;d%#2UFJJRS83NIGAWwDViE*5DWei)c;*srMX#EK&cyvBqM@;lGt^lio&)_-o(lv%xi|{2QI0l2qcwb%PycrQzqGwyd*yBjgGV4wl#I{J(aB87g#=uovlMv%+u#Zo^=&6!N@=-wX>Aw`{KGJB}Bb>7M6>iK1)F=m9oC5P+_?AHBZZ%oOK3n7?RFgyEY?SvM~n@CWP@m6QZF=@2VU?EKE*=-G&l^xoYYZTmu5%hpfA14IIKOWH<V3!!K_r3R616P)xdJX?e$kDnej2hYYL?Lc7k3-kW5)GE6q%z)1b;>T9mYwsFE}IX-5hmDQewdIsGhZN|PVXgAalvBb<I2E&>XZdA2W5W2gp238fzhQ%t{-F|^{zh*DPCRxchmr3i7cPrJe4oLbcz6C>i>613;bSw!?^Y|Q6Lf)6wQUS~<FZRW4O-hwnTN;jLpzH`cWmHMSZNH9zTf$6Ev(^bMYJulq`#z@wQWtJ-ZppR6K$~@FdIjG!f(3|TF&mytv!x3?7#T$>6t4~@S30O)$(wF2QhE!FZ<-D@-P@XrN-30mE)}aC$dc2%@>?`Tig{O9iiXi`vmy{#-EO1mTM{p=a;!ByHkzaPQA@N0>j<t<As{U0!X~y8glXsltT34$d=Y)dZR)AwL#!m`!~*2WQ3i1i8hqH-Vq3@5u=6EYrlARz18Nc`6IY4m^?`MipAT0}{Ue&eU_@Y43@jQcDad42Of3|`NcAi{)e9L}w(?s6&5|t2Q;ts+Bco}tI7kqoGvH|~eqMuc+i2Hj`-Rc2FTe`hj#r~9ba)H_3{+fREssRRoK1ok6W_K|&zdp%I)#fzv7IVk7450IdNWPBvEj`@kX1jcOTmf0Y!yCdl|8e2rn+@{Yx?O(&YD-%vX={;NaAO}kmncIuq(*7iXVK@7f%F4vVONNZyqRPh^hy*lv*?MGSB2Fos*R7RYt*uLE24I#3i+uRam0xsgz^Q7-^j5{!LDOQtB9#C{#&)!M>%#Z>w+#VPt#7m`-%2Gaf|<<LaWi3M`IaRiM6baZSH`VsgTZ(l3R~`yL^hXzLVe<O=;NhCa(3V(f?f0t(=tjjft%r&>YIt{I)Ims-@&q9IZ5TjUI8;!ccYlJZWnGdUme%L1)PmU|T^CO}NUk@MLSX{u6rCnXb}NmNJ)vcqa)5QOTWE>y{AO!#LL7$ef0UByw-UWXCugEKQ0+;c!P0gYJANRoct7?|c20I;^}str0srTxyYTaS$Cj-ukWf8rC>W!Y#Ybls&Mafem|I`BGb(vKv2akrv4w|7x-=WAsy9`$gm$bzR=qn6E>u`LuCruh>sr@gwknSv}m8XQq;TBEckY2q<EI^$WF$EUmqnm7l;EgniPy$*;2lL3!`GnnA#RB0}$FzJ?29WIA+Ct((0)^^I<i}G1ishR!U$QJAp8x&+D_qs;E(UPj?s2+_dUB@W7gei8f_!_Q&kZv6V3H<6EQd-!7LO|>Eu^O*nI<UD!WgYd9-XLv>vfa2R?rYy%HB*^bWvRGS9GNa5EtJ)cKYpJgm}2FmVn>iupITpj{@bBbAvNdP>CIDfd7VI>;TI<lV7JSOH3LD1c7Mw{ho-eqpA#PRQ+q+K;<2Bux~`Q`hID}r{jcbl2UP3{Vxf9jF~KbUDSiNpfUso_4X2a&GzwQ;k#;t;o2zUXp98^RXghb8_<kd>#I(&fo#r7kGp=>&F|bVK3XlT5wF*DK%SkO%fg)ftEMulT9f|w&AcyM67E0GaBLU~dd8mGo2|(oJlwyWM^E4g&nlGp9?uux;$FJ^#B7Qmsv*(A9ZFoT)k&7v$DeysID<t}qTp3T58_JM=tSiZp7K^=3y~%NYBk&5i;PTG#d-+i`kDSmbZ?vH8%_1&P>hN^6t-+B*hnLc;!Os>^NmD@L^U#9G(PfVW&y042)v;eW9XcIx?!Hh{-RCh;GK?=;VlAkXFrHKX4D4aE<vcW(FH5_C_R}Udy^FZH?RXun+6Km8Az<s3e>#di8T-W7fM?17yHdFu1K51!P6n^yW;B_U*7I8YbWF9{6+NkO?doKA?(%FHQ%;){{Bo1;{@&t;{{gXWV(S')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
