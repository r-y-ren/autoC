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
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rM%U5{H=a{MpzJP#gnH1_6AD|2mOWsjkc5F0@-7RUwxg3W`Iw;=yLT4{#7yj@*Y-RInqHVYUKO>%h8_vx;#u73YNSO50s-~RfS->&}Y{nane-@Li{aDDaffBw&Z{jZO2e0=%WKmYb0fBEl^uisz&{@tH`eg5;ypPs+Ey1sgGf4sWB`EdRD?O$HsfB){q+mG)be>^<@`0uk1AO83H;-_D}_~W}@7JryL<jvvLtMku%dccn_Umvc-3(~gJ+i!k696q*Szi!&^-@SbG{jVSU{`TFcUpuvI(dvi4{q&>!&GW<K_jp&=Blha~ivt?4_g6pPzkd7Ur+%YX$HSYqS0CiC!g;$%=k4JO`-_Hre$@5i#km=)VV%^TKO7F<U(V5b`e0)o2h*GiyEzY!S}vLOlde${A9mXNs~6AX;QZ~;Z~oTL>#Ls*ukL@oy55Zp(C0^7<EE`<aM=*q)i?L=E|%PNJ{h`$vK#A_c!Ov7y#F3PBVBqJnPjYfetT-)>QSF2uQXJP-TD0O;Wd9md9c>Mw0Q8tIN}zl=RJ&cc;4eLzz)W4omR)=N1uP!+k=-)iTBFt%37{yGSUy9sh;2H$FYS{9%<uw=iiKnFCE|B(~_Tt@5~?6@Y~mM0LqVxyYu{$=OZmH==P|tI`h=S3wG<`<Obs!&o}Eik3Wj~cYa`aMb1(1i{yu_pL}uu>eb=J+h6~1c>VU}tC#<BIWm`hb_`GXV)gv*U*G@ov`>6o$lTywjE8S^yOw#dTEdM&Zen1~o!(+!N{?L7n(O!QKl1g`vPz5>_$D%5>G#N|j#=sU`WgRF@7$9mva)@}6ra8=P9@qUI+x2|dGq%5^W*OiuV4R(cx0=+A{;a3Bb`RTShiU|>6)JZp}f1%7{Kk3zx_BW$>(CQvJ=hh&}uvFE>ERWM-I;)X8iO*eet|Ez!%LmG4T^~%)%A3ypw5{^0(EW%{mvd&P#t3^zbx|@$?!z&!&B%XD&JAmMsV0*nz&07hmmCHgN~Pr^^@aakZb@_2E^*{6g7Ve<Wf{Zp_W<+-2oHMuUa*5sb(sGEnX7(@iFusPh4~au4I-Hlc$zO+#(KT#5KiZ*Lc8dpByEel6qYoCNGhP^d<Ky#C(SR2)eFXSBygHagm%@x{XCiGUSrwdqxljCp6(RR)`{vRw&17};;^98P;Rep+wVA<#nB`t(cbdNWUs2RrPim#_W^+U<dxaSxU8%J;-k`S9dmrWbQugPJr#y#eA`KKCX1m?4Zs?37<SqhJKXm>S{SGwhP#a^&Yg*ctonab#l%ybyU-PboMWHV$a_^^6DDfxygaZ;U~RLzW+Eq6536ukJ--JQe!jSyM#E!LBXAz&!e$d4`kQ5SGKqTLtlNHUHJ_#^dJ4=db_S-E#D4VDgcV{a}4Aerl6`f>`_Mty7n$brd{=kxnLcZ8>#z446Ld{ELeRE+3Oj-^Eu3o)3Q>xeBQ*J#Co#Kq!3@utvYqCv6|mXAH$D+)^H12W%1+upWtMHG=2SluP0L3W3xxPrLwV`IamhYHVQCM1at&w5g+Ec>ZG*0tDlwt?q{()s|>F>*r>jRtmA-DnYT;w!Fmwvh|%ecLCVrbH@6!fpRT?N@z5nb7kzz9VQU;GHmOdXF1a>BS>Ei&|q7}4Z96m;3bTAt1)44ys)~SvMqegOmB%bH5<)HJ21TMv)BIm)0w;%_MLNvI$I54{4;zBtAiS*9_*cRe1{BheM+fQWZd9K4D9e}!3nti(oO*IN-7RP!3K;*E;V9X_J6_Jr#4N)-1nh+gKyF^YR^eQipmCTXt{J1by%&C7;_qOAkd!FlrRPyb<y*-88zQ)0GV#2QF_=lleojNtE{>>3pKhEjFuZzwm$glGbg5ZJKRoeYJ2o5{|4_7)mEoO>GvCisDIGkx2!YH#VEK}gbDJGGaX$-8JO);K;|v8r2gT}%#7zS6nLEg8`oMf5jE~S4}hX;g@7C;o@8vO?$nH0Z(2#roTfJ1wEJBnyG`tBd~n0Y-oB#&39sEF8=J^ILyPt)ft}}=kZT&^^sX_ebP7-WwCg)&cEKF#KEde1niRTW7aFFQwT=oxCxgb_*D%f0ezbO*eukHVKL|+<*p-m5!xPMf8jphlmejBq|Jr=4Lz0z5he&k>)VFJ_yMxGbR$K1xKmK!9)f|Yyc4@|*_7?bCk&s+QxK59V%taI-e;D}KNIGN>Ti~N#{{5A{W>3#3&}I-<Pq{%(lM^*NBNy!N^D|p75NhoebIaoooK_=L>RNr@Ks}|;6`)k;^?+s>QW5L5;|m@laOB)7pm9hUA64iyS3EQvH0ip6(@oQB`8JfQiQek<-im4xplju&x(f%+5BK+P4oE-~uO>#<U;Y$-b2+?0ED<j<G>f$N)nnD)Hf)QWKMM+lnmKhyez#4G&NdiXTmX%#sD=%UxEE(8O^+`+c=G3oe{ug{9HbJbBmy8-@TQ}fBPW+T9rPt#uW{v`6M@NCk2IP|eX>Ohj{Ug}V;g0;`Oyjhe=@gm^10A?Qs>e}jg`+$vzh15b3A+UY(9f!88heMQC|wc029sSRuxFzUs^Fydy=_|+NN2@I%*_XLNvJZger};rgct=Pr8a6dFz#-+W2i14*~JYN>)sx-6bWu+jjDT?ghvr7q-;;twsz=?pv9`93i5bpC4@+E=f3Z_8248@m3=OM}2eZXL}Qd9Jzo)sQek)$bPn081H>uxNUFd_vqbJ$Psb?Km$;SmrD%T5l#eAD0C05TYoCRLW&NuHz^U<xcEDCtVu{}DA|G#2z}AV#3)0xAlRm8K*W0T93^Hr8O6EUQ*5q8Uy0WQgyP+VD493XIgHLX*yCuP*G*%Qdvf?b@yC%QrYwgZmyuz!Kzu>YoGU%j_3%$Ep=C7?+hnV}KT;?m&FE!(h3R95oaNLYP|8`8M~{L;jA)SWjnei*F(B&Hvy8J1$|;~r%275WZ2(k*ry)Zm-pOaVw>xzz3J1!SbrAN}sWDQ4ZC`UY@{ZirBG)RdOY``EacE~aT?oWL8-%bv+GNUjncIFTa?}oa@UDRY%1ksOQb+@$<B4l1X)0S(XXb^eWhQU?xTSir%y{LqU>~Xd)Dk8$79%08P{bMyWC_LUQR(HO30lu|vFtqd)U~!@!?^94=V6YozM~a52Jqx)`2k}>?{LtV$_2sTx5hg3N^K!ZI5bC#l%WuF1Xg}Z%$UL84?Kb#J6y2lUjE>2p&2}NtQU}?Xl}`~#3;3q>FZ`0IwFZp7*1?Se3`~l(H^Xs(?}s;4igPf5(+`18H~LxLZP_`#k7GiW42=r@P;6d9c<cw4Mt!}4(RA8)a&f+W;6YTb!*c60SQq8xs-Sx|AI#2_2jO!L~-5U>v}mh)-{8-`kBGKx0!*=(mkZ^;u@VGWb#|if2ZQ&C%59f2Tn#VfUaRqgNho;oQK;F<LE)u!lZ;oLkY0yXm~1nNiedLu@NH;(-NX#`cJg?X+Q>Kbo7+W@tRNh%!B@5SRjim1QOd}KnyK1Kq7rMW!tXXiT2lH<0M_fBQ`;UPXTFNou9&9%#$0=&D3=Vm~|DGN7v6~TtHSJ{KDqON6(D10%p?0<=b!Xe|rA*zOf<WvBO*osBZ;R6CVEbp<NX2nYJ#GJYPf}h@YG$#iKwU@O;+LkzShSETW#FVTUm%_(jHxTACw#9hX&M2e2o&4UP4=N<aWB)A*e_m_`!d$qFQg4W4J{l=o_8OjwkwvCbPOT}BR-?zY%uIdykA^yc!*SL<ToAw1D#Any8yBI^RX0NJ<gI8FN;H_%NNmm<wBH#QOz5M#uEYZ<t=Tr&>bxbe!cGMPwd!oenK>nym*4B=S89G7_!)EhU|qWF#zGxi3f*M5`p7r$uo2*+X~@Zt$w%u2PmxvThz(G83-bg$KNhuOkninfjn;6omMULjmf*}OIL*P#?)wGkY{DN1(OdLpK?u8=lhYIJWfupA@d7Sf1fD1Z5B@1!LP(ti3xY&Ihk4RP9GTtG6KY_ta;$)~qGWbd(3U|u<M|4c(9cw$-V@cLAKmW+TwT!>Izn}(t=VG>O^jXU(H!70L~<IWLSd}vvA!k;nVupuE+F_#G9Ev;h0*Y#?1k7gsyXI>(n%b^ia2*6--JSQ%`&*2}>*`n1gxldw%F6kv-@BvI;7;*XH1&(fG!bgY(jOL%g;2V`XcXPMn9k)U+%41t890@$TwKPU-NRM^3+!gDvk+t#b9`J!loq%Qm?~z2BnM@>EHC~NUO7#T?ZQk<5Ayr>H2dA`zhegGO-bk(S8%jVen!0ywrD)?`PT8A>3ZuuNtrNtgC)~~315Cv-H%OW(<yt`(ft=f|GE$7P*SD!%B+@!&*iyFkgrB;c*4X5Q5YKzZ&TCN=q#pHN?RrKpDfrH59Jj&b7%Vn)YW{_-mnR+oLDbc6b!%rT4ubsV$^fq=QpQwmhwM{j6HqlP%)K&TBdvVVVjwKn_;O@Voj4utOz@RDIM!)Dhvh?=VF*43i^Q^MR<4DE99(xXF}eg#H6V~HS}+tSLIe~JdR@s@n<TBU>^Hd~X`0%MWofC7vBW55Pe-tYPiw0~nRk9YR&$g2DC^S%qv5&C!VX`uBhC+|S~I>)!tnqY1h`WZoNbt1(15`%BpJ9$V!`QW@!AFc01jbsdwkI)Om?(j1h5ESY2CJoB@j_qu0qBZhw>qLj_L%Lo=Vro&?Sx)Fb9NdTlM_;_&gl`D}!p9K4xVMPlZ}ca*;aRX{KX0zPMc30??wWdceAkhTw!@c9s&_gNfxHRBX?`Lgj*-;@+sRhnb}(Ug2ZOuRLE}12_<pD<#!)(}uIpmc|=`3%=P3+=BKHlk+G-UGk?a=;U!feUr)?)N}9(Mg!OiQQW~1yG_`eP%SS@ORHl`u`~{Jl%ri>i%Uw(Y=I;{B);2@T9R;P60@4LBPK};u!5NBFfXHvE+PeV%85w?+d|<<UeRTMyu?&IHlkWZyMC4udE7z{=g#BnE`}#@Bi0qN#wirBhw-@UF!<E+OKq>J-_);aZfCE`KS8#Vt4lVpu`mqX33IT-$ilf(ic6wOyZKf^X6EBX<0)beFQz=MkZNJV1n#9tj1RX$X{QmSj0F-h#{{teJU?>TK}mPp2peMZ$f!eJAs$s}B*iYCq|b@-1iFTKPS}IfMKwkj>o!mzoo=SbBSS7ebXLiU15UMbQV<zBIs#7#)Pmk31=wOL(NPS|a`afy<8BfZs}Kh;C|=h~Z7qoM48ws`97q8yWmLJ3_wmq+&eqPtS|-8yQ<l`O#1n)W@bS`g$Mtdmyk;MM_~8MUsh9nA)8%-Ft-oNJKSLz4&2To506Ye)!4wFNuu-RXkW5w*)@Rvr;H*}~VlUVpz3MT3t%cYv@R1S*Ro<V+tl5H4<`bS^NUp?vLS9eFNleqN1{I*Ali$fLgLD8wu%w2IMW)fGqr>?GZG-GWn3zY+<)Zp{58I3#s$KMG7bcd}<sJE~Epg;8QNK_;zefZ1n8n(fPyt>N5`1zpdojUvSQH&&Ei|a3Ttg6)WvA=YIK3hj5OH@Lny#bh!KJXKiT6>cMq?KycY#vz9*qA%d9CMZHEWXgM*Yc4BzW2X+G*`$&#5|QcK11gFsTAq>v(Q6tq?}7j%8ErD@V4cF~<ZGGGUwuE~irfQQoJ%@9bJn7UIPZ@u3Tn@}xP|N)X3zi9?W}d$7Xw!SE}Aj}nT~5Y|}A#H8f8D%fwQ<)5#Ehj*4&^sW+yphqSK-{_X4WyEuYXcrNpUGaPYuD|U^EGhGpc4(7{KK07k0$(r>kqI#M7+dHn&a1<cwf$_l9zOAPZaPe@R;AuWAtB~oI~oYU3PHn`)=a&1_kS^+k>@oTEEx>YCtHUcC#sTD4_i}iq52%G1Y$-)HU!Ci4E?MEZG=E36z)ASyuj63j034$n{>w)az|R)9(zRcVBl!9p-@sM&eWiyHYLQwWDYIy?rhQ?GNlf7g71bxWYo*C@B|3L#Pi)DvNH`bNxZ><wHCRQCPq(HEu)AZlF1@)R|iw}Q@~keG<ob~+q4uzpstqYCnerM7|=$UnwYnhZIHUGKOklL2GUkOSvA>7)6?;uZfY)Zhqy<N%9?1(ySV!2nGRY;5jcYT%oSy5Xqy7Bc;8n=<4}-SypqpESG3DHd{|1_@gPv_jF+iTA25zo>X<^69+1*Gt-WkHR>qva<&-eIT&CUpa`#m>rR@J4^kct9Kfe3W&#UA0(*1~;Rr+!{{?8&1H7+Z~5sYVFo6gj};7Hx7lGm#6S0~f1TgM5Qtab#st83_KmRG1#9f59Op6SdKCPDyim34yQ6y2@TU}K9}f7h=eb4^xLQyV-WOQ?PV?3p7(8JEH;wU9tLze@rP`|%A}H<8%&r1qwspePGUMD9gVL~5)+;!{g#yqTYwt@~PamDKZQCc<~FVpoo2ancU!gHn?)F-d7a?8Y~TPnq%5pfIGMHcg-GU%Zj1*^DO;u`;dmZG^5tvU^}sZC)5Maf0ERCKYh!VL#M7a2*TJf-)mMbW0_U1a%Gz>8W_7Q6X`|^<-od<QXSX0FIhS&74jykGVnO9jf7~%o%lESSITJczkZy!7L?Ob%kf#B<s)OB3$m9>&g8k+#7bxspTzmtXQPZ>TxkiRU@mQZ!QC9S|)N!GF}5gPA#+og|(O0s30Cs+_OaD>q=J<f6UC~^}?J_1j1?O%hj?nZm^?@wYrR{3y%5?$Tz(Ef5)OaD#GhNwWqG}!Wpe)$M{rxm9S@kFma#M=v1|YK0b)!EGuN;D<eSJ*sSuEQ3G<AS!Fww65JwDc`v)KPNQ-`DfFJjB-;Z#i7vfyDphvL*T{TPG92)z{Do%h9gr4E!9(;O!AAjrzyit3(`AC>yyW|Ewke)3fHC?tCTnb*Nb~6=5AwJ^NFyDUfKq#fnqdb<=Oa8aOL|NBBR*l0ro=T9U<Y9ik`PSgQH#Ycj)du7%oCOcG1YQkS1!X#DV}UDh+)EJZN>{gY1!sbg;bIFWed$n|0^-8j)acuRVfob4o`HzF236}LcWR}WE)KokFB`elYr|9@RBULPyp40Gh7~-Ti-(>@MU#t3OTX#xvgO{w+5Z34rZ`YC0;|p_LQUOEflkAbd!&!A#)9$voq|NA68Bd?Y^WTmw`SqWJJvwopB@usdnE+2xMPUq@uAV6ZYc^&M{tqJJy8B7N*1(RI6fm*}g+R)0u|*l;ko+tBNHRR%EFMRjf?LnaI5RrcnBkLk5IhBhu$NIBHO_dNNjOuIySziy`LWTdi?5kfcKL)j$PaM~Md5_$*h&!&FCs6w*z<kmr=7tj;9G3CPI#ehqe7PbwN)O^I#bSfO;W;tI#V@=2Dvj;+LH4)WOg8B%fOrSz`)wm=@c62PKLFtq5ar4-j*_P|f#3DvN^1Jn#>C`KWV4uT1k&?fV>=zbj0Q7V$ul;#fI(F{PS$na1t8-~m<bsFL)uw<Uqy*4MM&o62ASYiO|(d0}jXYGupz!8#zCAC#hwlWjtdZLN6R)??FuG4r8uW&=nH@F}(xIi5TF0m#BdTRH8x%c_Bfm4r5rMG1R1*ObiJK5{(HX-cz=2gKXtfmkn>}UL2N@*24!v)P5b2CL{t=f}3N7M>(d_tt|A|Q1;6z$*{l$CI@HxS6j8;jV~0IVm;sO)mR_UW6n7~442>kjK^eKka{tgD7&HJjXpD3p`36-~-lAw|KH=$l(Da02B^nBjizWeZNRK@z$t6N@kc1H<SSf$bPZQc*oL=B%AlIemX{JA!HV57pP5T7TP4xisRTECIQjd&$(VO)XxYHGoJV1#zGm8J9lBO9gZV0Ri$Sr5ogG0x4ImQr;mu$|}1CQH50`o03vaeLfL69>EbN3p|a!!3tK<cAuKdHw4A7DgePK`^zt5AhWb!+3EU*rwd{#O)MUEf>5ZkMX7_B3&Yh*_fbI!0t|roi6?3FxcM}f^+>C~YgID}s3XhlwByQRKX-$?r-NMsLgjU2=)c%f4qB3B{!l*vfI}>`#PHiHIlpNUiXwi<*aJeARcOzHMd}#Da2aVn)2YNgvX2dVBz&`iw3W2on7T+Pupz<2)xpEeX4r+tBlK>a8HqSxI}IGVlrDv}DO8TK**2qreJ!;M_nWZ6B#d_Vlw`1dn+#?jy4$Od*;#hB?@u8Yx6HkbhFt<MzUk<vjT~)dvF*gpI+|t8oTLa*xd0B$7pay;DWoMyc9l;@?g(}FxK@mu$27*oO^P;B1D+W!V929aMDPnJJF-GYEOoW7<JAZ#Qr)FA1(s|9j|o5%y?8|{Kl8X#8MasGK=|THJt?W#fKLT^BDGMa1X}TRodA8e#(s0?CLjO)_5IsM?Ghp8LIW@H$SbSsl!<6EgT;|CD$)C=kvYtoV{E%W`d+l4+~YQSSQAs^0{!Bsq9(n;I7t~gZC(76lPl}ju2{?^=9z?JrMGjFbIU9nm@YcEf^F%{b*rvUIEabVnVJt<%`ZK_S|Su9Y$12H>}s8HJyV!tW`^|VNArY4mz;*N8!t7yTAg%C4mdz&*`!#4epytp&fGi2GeW6Ez<;|b!HzVS-&>a!(Ute>!;>I$&z=sLlNg*PK-aP|Gxi!FY-v7Q(K==L9M0ccf1QF?1JpKK^p8h%Tuzii?FukKIg7KzC^D7bizphu2Veq{D$du-Iz3u}<;*t$Rs9UQmn!hMa|Q80{yYO<R79O?eercTm8C}6D(FHong1KrcGTg;2ru=vCzx=#EptE85~kB!M_GS$mS(V4cY$XO(nhk9OedlNLefc>)8#7mMPc28sTv)PI{y?Ewt1n>S^_3KHi@opM&`65ShZCQ10ibRf~K<!#he^5;Gv5;Xq20ZIC)CCFk?d+M(e1K%#rdoj5|C_Bdt?ub)^L%@EkTouaeO=E8o(fr%1tKNAPM6rzObY(gBiMy_zV+)e6ZdtN`PfGNA~Mc=1b}>sIzv$ImOTTrJiA=Cu-Xon#dT3HX^vJJRgBLRekGpBLV4jwgM5M<2tEBr@F0>$r%Plv8u@snNHnYlc!8V2N^+>2lnrAW089`j^-D-@kkD_F}$z>@Snjv`dkx&8kxRgfHL?Hfz1lrF`uiG5DvWe36-I5x!2{U8&ob(;;oZOyW#kHiVBJf;w_^)(gRJo9YGWTFzaNNki9@Cav8_6;!EwW>Xam+$}Ro7f1qqL1cy3q^jhC2|WVz$aoZ}B3P^-YY$Qb>%`$4Abx>X(Lx)=^zswtYR{myARQX8j{bjV+pHjiDP=_M0w4?<gO(tn?J&jQIZlKpGn-e=C97QIY<A^)q;QR!RAF%w2YJC}ZZqX|8u>ZH2dd;ZHdNkRRh+KM3o|mrF!Gq3&=g^;q?yzcuLK`e3My-Ck%8&yig`Wd6rw{xY738uB3YG{`YLI`5cKo|lsT^8O2lzUZNo*%lk810JLwO|%pE&F_!%L{d-)&o)3GQ`SZ8>lIjT|)&HBHcs&N!|19(+WqfPO2(HwC$*Cd>-RIjCq&86~PrAm!c$X^u*uI3MS3tNVy%+0u99#zHY2R`XdMDB6Yzey-w`@(D@Nop8D;E}8;a_9i7b3iJetfO!b?}`?TjTD2ZF&@0~znkJyEBtK+?51E!p%|c<J*CpII*Hys5CCqV08(Jzdik&6%$ZW2GC*HNeu48EnoT5E74fusrNb#Hgbc0G0VmgY8h?_pj{Ibkg-*_cX%AR_fGKKJsqG+;0?Lqwub1IPp*<d}DX+i~F82$BaVNvrhy)mKXRm>z5=+k=P8ZN-ip;9Wm786R&(2iC`d<Ofh*>0$@35g7!ez8Roww#dT}19AQ<ch#Dco9bi&{l^TcAI&R`a07*4(U0BPrbG`g<z)B?jRfM3LU)NB35)>0)}h!Lw=s*zBoHb*}^OY>gZq7{Ak`v;tQE3jM`HW~@I(af~XYsBB3`O(L~ywof0e5)?}jr^_#=8Sfl%ymJu8Oy_V{Oes~wMJ8CsjdhRP|JdstfVyVlj8BLumX+Qr1i!ikxrwsdZClx`BI-55^i#MZEA{yV^gmbn)e2V3Vfbw&<AxdOBgH?bkYnoHKX~|a6IJNE%`adMIp7vMu#liT3c-%npaW2>%@;I6Wz0gWNX4~)N<rz69R*zmAbvp=j;$zR;!;6*1Ttr7x(%>#R?@4BZxy!3sGediFE+Ex<!Q!|q9gYQntr8BVaaT5#&2M7NX%gmQq&~Bx~Kx#kdqRxa^*NSAZ7^6tjw57<tdi534<3xv~B)M=i~?(l8P$U(OYG^tHq+yOA_H691_Sw%^-`^-?zgVir_Sf&x>9<N(T2n<X1#8OizEgd9`jCWX$(2P^vPKtrmGXVu+drRR~9AJk)Y;BLB-3U*qdaA;R2doI}}Xn2?I+(NuE{QE3}-pKc?)-mF-Pm!>Vmbg0ZHhYa^?$nd+x8;|$%?~G~?G(^#<9-U2O#(XR!WVi)YH>VX|LSxTtb-A6vmu{4J*i9($z_3=11%l6t3^q4IR>D-9GY}&Vf%CjixCdGQVAAajX}=^<7d<3NgbKkMDE6SPWL#<~#|(_p7Qul6di8?Phd_>o`rwB4U?DrwO|SK(`EoD8mso^jb8*47MghRI6wXq<dbCLCh3-dTiqpYtO5ljAIkSp0EYG%?Ijp|Di_jhFqS<vCCT~Yq(1@nfMb<8*>?3Dj%C0J=n;S)c%VK=_C#`DQ*llv_=J7&zd1l~tfiC4cW@m@R?dB?x8)p0)6qh7@n1;5B*_mBxQYFdU#hEawK!uyri(+y@zg8;qEeMx;Wn5P7S|h^yY(3NqEYwx`+iu~_Aj)sU;AY_rB*9t5#->y*VxhDn0l3`~9%2bk5Z9n}XUq&NQQ!kJ-U@XSdfmVek|9lVD_NVmU%1?b>8m&}V;S*8jOfJ{@kT^Ztc5>+dH&`N;}ozxLn~ug+MQ<_;wb6x3nVdbK{y;tTAq}moS=%kr>`r!Yl;l!b!8a{h4arzAz6tFL`0%mN0!2b$qCj(mt?=N=?Ly(n`PL)WLb<d5<m-_vSR&MOJHo4MsdYMr>8SbfN^Up)bi;`U0I|2yq1yzkhCS&C(c44rQcXYqKa->XLF8E=u%@f6|zjb-5l7fM@^U~ASbz4mh(8js4J=LQL7pvxEiIBGJ^#0ilz{=o47XMgu!QPhhY1W;BJx)`<ULWN(OGBU@1r{e%0say9g4n`V`JZrF>-&!%6SUNtZfcK1zG7Od&0cJTF<)g1wl~V}fkjb-S6usxCES?!+GQY-*Nz<Uz{zsi@{9?uV*(kQSIb<h9NUb-KE}VIGBnB=S&aZZrY+iB)vU#pAw1SWqQ(zMmAp^oY2UnQ`@b9+jE2TxIIgjc14B0C7BJW)>m9+tK>A{R((g`=djwM3k_35Me}zAD?&kb(Fo`ZBh0%-bWTxsv>ZHMcaMymU~B6YufI##=8TpvG|(637hB|222t5MDdwMsxlIW;eK-zbdk*yf;xW5TgMIV;gfM^`G4D0ZM(Bc@?{cXB)#a;zO)Qmv05mNg9eL;*MJnoPF?EiM)bc#!J85MXew`0v#>$xW8qhkYn9|6DJ1NR5&I;Kg@<ja^dH&gXF{JuE9E-#vc!s_n~coT6X$p8Rrs|d(hQbbLUyta#7$wQOIb4MUu@+M;0Q5M+XJf@NY~;tW&VUkIZU)rOi>5na&HU8nIuTQ^;#v?3!cc)RmnSU3Z}{W8Xj$ome%HbzLIMUYaJ97m(7KxiCG#2_UMCTiN!ozG?r_<(~A^#BACy1hqu^@q*PT_!lSb>Gng+mlRQ>T#f`n9hEnkc#F8ck?sbc?O;45ZGsR67+`$wBPgGuPHSdb-_OHv8yGz9kH-f`Z6mCn^zFzWf2Ok4HV{llDMCW5;BP=?Uwk|kmDb=Sg)TfdYNLXP;l5JC>Pk!!LZk?JRqg)HBz9!ZlBm2xS<_Q0diuNm^8(wO(jN+y4JuuDG#(-S2UbQU_$5u;1GM-JL5EFlIeb<sk5}{#%hva~SnZ8Ov*DWjT5|I8VY5@x(pA!MJk-T(2FyghJVOB0FkoUIilnu&1$;$!I9$YR6j2)p<Yn%mE(1lZ_6GGVwh}x8l=g*t1jgOUyuGJh>mnB}}AIi*AUe$sI8{s7MR#7#b@Vq=8=><d_xL9eiLY8TjPtsHhXr%*WAeSMSkpxE(B(PPp9Ci@TN)UHl2_w)!3Nygf@qy7w*`0jjPO5N`aD@u-sx$xQ;H9ySmBuZx;ldK3!ail$P=K5~n^LeCxtdVE&=M?y0Sjt@+*wSob~O@15`YLS`5-dmCY5X6R<-Buw6@rmnsmDw^{Xqm*1)^c`oBDvvW4&w_)C>%&+{t4eZ<VgN3Z0flS>)tCQnKsT#WB2Ot4k~+ByivNjhGlp^^L~ogb0bqcH(VerXh1Ku3C|l1gK;imWh}4*`s11$`)$g35%zYscO&r3Ir=uv#?SNNgyz53M7AJ%Y8zZoPd;QiWr3G9^fH;AGC{vpycIg<hNpwutAIavzoSzLL4(h8C_5&Yh`F79)C&XmBG9tcyDFrMvu_2pbUN!mBYV5-nP#7pR*m02?pTTsCyrDiIrA9eWho)FPd}&KccS@IY30xTOhhDe?&6JYRFuPgbW@$*CpMqa5MY!M7wtaS8%SyY3cMbwfbS^Bi$Wxrv&4bn6JiAMBh&ibycoD(g78*;n(&{mR%f;s03Opr2Rs?_5|E3_MR|<%*AC{pXjhy~01CC%bPGAlo_TX(xqi7AsGjq{PrJvG5?C{})Ru?A(q9FX`(-jZkQ`t>UgM#v^fq?4h_Bf`Y;?$q&+0!kz498co(Zay?tApfyF)fw{402jtt9UI#GY6^X@JT}n17)zQ<p(Awgjfz1eSfG5UtYJEBf#qtZCdTt^EOwK`R%G=Xis5Eu-*QB%_wUVQpQ&&WpOCUIxeTj7H$((v=+YOAqXP;FBpR3|a&e9-t*{!sU(yFhe_e4{ahAlY&(@06bFu(VsDi&VxTNg!Q?Jjxx6%70|A@WqPjr8N8wcDJtBYN^IAjx4Yr@hKB+v`jgT3R9YC%#i^FdtxfT!TcML!EKUuA@``Rxj+~N3I#QHhCq+qa$@fyH-z4-4){C#tQRVej4uyoq?;2;$h}oJv0*S`1pcdA?!=tko`@|+~Jq8cMWD0xyzg87T_6C-RT0}2{~F}1U~#9GDGn9')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
