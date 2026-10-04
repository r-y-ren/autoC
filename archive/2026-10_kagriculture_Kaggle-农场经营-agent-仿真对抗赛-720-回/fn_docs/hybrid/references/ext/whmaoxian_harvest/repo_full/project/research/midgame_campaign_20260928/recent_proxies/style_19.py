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
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rk<O^;kha{Mnm_d)$JL&~>VvR5RQ(h&UE##$H%0=$L+V||c)GyLC8YWm~#%gBhxtT!SJ_@vQr`t_@-tg6h&$jG1n``N$#`rAML{@b&E`uW+ryAL0pJ*=Mn+pqueFaP=Z7oUIp$FINr```cT^Ups&d;RA9{`0@mAO7^|Z@;{IfB)*!%a6}i&knEmcc1^edwBSt)z$aBdHI)5?=F9^o_y!e&kp+!AAf(?`G@0s#Sd;Du3z!X*Wdm0=Eu9Ypa16N{o&bab9$@uuRpxr@85m-&g`Yme^7m?;}?=wIzD<c|L&je-+z4lto((S$Az!_u;0J>{1-p&-`@WO1`EFM-P^mLKAt~<zxhv}-n@PF%jf_7`02}nPrr8d1+%}r8rj{){rle^cY2HI*xuf~+@I!hoe%76IrCLKex5JlX{?V=xq5*=e|diWdmlfB=JWC$mw}(Z?d6@A$Hzagr|<Zy^6MXGX7V+Yhv$<;>;Zr6%CgS6DOP8d7}0#(#}B*n`#4YK=>^+uf2VEn8=v0GN!py?%Nz{uzT<<c<{Nk4*PPZ5_n+o_w=$WR<*A?6z&_F0Y#G2GHihxMqV<eTpgf)9u?Z&Y`UmnfHu{0bf<ccwF4zk763dPby9@8%zTLn4_{*R7??1kI`{tkLqk{i#JomWq;OYESF9j}YX<M(}-@lt49@i89VgL4vi#hq8=x3^zJ+Fm+y?Eqa7Baq`p7Fw0ALjvXVs~n`;pmygKKzZ+NXI<qW^v3eJCd$Xgp##f4sg95(R-a=(&Y#vI<CRv(W64g1zT!4tjVOvjZHjn;Ra@N;<zbbQmkj^0mvkvlQYH!UB4MZ2>B$VlJB+bpgd5d6X5HU&w30x<hwpma(g|V!19nSg_(1Q(>QL!{ni=F{4CxSFRs^j@Biv7rDgBPSIcpkjuSCI#F}pN#X-8v?_E90IPUMu#4cgJ$NfHiHyvBCt#ux3E5O*-X9_r1F=!s2sLPf+KU7bY^={??u}LvwYisYXzD@3B&qoH1U<?tZA;hPEfLhvt^%UWZeE9hO?(nDm`}coCj%fIT({VHT*yzYRxF>kAM&vs?{p@^(m&O3m|IGews>gLS^79Ef<|dra#Bkvj&sG}FT2Ez0UGeVeb8Ju{KIJ^)V}k;>P-jdO)aVWHa@UT%8o0b0Z}YVCH1ulV>elxonWq9mV$D<MW%N8X-VIrlhCB0#DqyDhJPkc0i4_JO8Iv82hg>|J{2|cIxp`P7uJy0Wt&?-U_F=Aa&LP!bcX_RE1eZoPyk*~a`5JkJE*k$vmw2Tw75y&PEQ@u)H9CG^MGz2YZ-7V~T->u5x0x;hNAF}gug{xWFn)TyDTr`+^yOG>Jo`Li5ULkuBRuy!-t%*(FYnI=3%C>eoMmO2s~PUk7~%I0XZ!X2Nn*hic>9s7Wx9&zYi4eN{)J;CSmqp|m<t~q(u@Z(eOl=voo08Od%*W>p2*i3oj3Kg|9`Ce*m(Ocghs6EXv7ZPjkT<xIN=&eH4q%BhcI}foo=TTm_g9wJVyWRd<ZY%vGImRpx&|z-^eVc?%J|T|LV;T9YQ35n<tmkH7Ti?h^fTh%xjw8+V!9ij2hg;d`79U5;t|qE~^+T^VcuYo}5_V=n4!#8mmRT>X|2qejrWHwNB?vJ98MH(q<@IEH-<@&V64WumKsYir7lkF9?{x#jl6F3<M8=ydVgvm*dERhr4+O{I>Fq;-xtaf6iyp`9!^Z$5pT^;yh^UnN@hJ8M$xCOI*%CzQPg@wnlTfzyJK7+kSw=3=Kqu=Y?s^bpg%3yiB~Nz{N-@cPUJ|O0Umzdi?XT_UhS#j}BiP&a)NZv~HR?-;xh$Ls)MTONixIKiuDc*iW{=HLz%)2(z5>3Z`wY(Z}u8ucmJxh@=McNnQ{Dap3G?KxrjVs7zh5(4k&x_V4F+rh!H?r!>EYr)GWmRm6}UfAjMGnk(H)03!4r1y^&F>G+$eWf^A!ubH?$7>3t2^KL_#1%O7GwT!MY*t~I#7s?sOWYF*4_-e+>ovkkNJlwjlWtKD&#OG|Cu!@&g1*ogNX@`hK=`CrFXtoTDq28Lxn2Q8PxzBlW%k0)PrpeA`xh+RFMj8~k+j3-Wz?bjSGdFsRW@Nou#Hj6cn-S@rE_!7q-T_E>5cl+vZvhAcUR6vT4&lw<tI{xZwPcMO{bG+RW}(<dg;pg`TLI9!Wq$Fr_Gu19VhO7l^p^u&gqqS75daWZ%xP~KcR>u>%j`zjFK)YYpqWg{RTTxTJ##qRq;@jq%Hu!9RJeSF+X`Np<?Hdn*>s@wcNIcX3^=E0LWmlH_$z)`N6f2nz?b;9AbvhycM;@ULdt<fs*!~g-(8oPlc|^#&fLx2upDq$D%GgGop=y{tY4?9hRu28*^Ct_#VrFsfC%#Rq(W+D&p1HynduTG;{@lzGf!a6ge7DbDYw0PVbz3S#DM7`>?_6%g@twkhj@-Olrfg17eoIarnM@`nM`17dC!#PHpUpQ%Bw1V;n}nK@y*-66w*1-B^600RH&1>6q}I*+O8(OpqM%!$YA$am{6ZxO9Q>aeb(mk&^&PYS_3uskxs)zoBSGFJA|I=sjP6BEf9$UCb;vNdaMo_NF%}n#7}ic12FtU<ul6FRYxJJ7y=~tx}CX;FO8o#>@9Vi_+V0p*X4qN6-8?sN(@T&6P<ecwPUIy@F!F@(e$@{ZVK9bA#E{Hcx%W`(Nt$X$<5>cbPRwXB0?bxocJ0UW9KkI$I<(29Lij-DHmBzsfJ%usS4#jQ9i6$Zc(PDZO4dcDWL;$SD^PU?E_LapsNY5QFKDMgK3`{7bhc7?h<-{ku)ee!3K~sJxL)TIHy%m_tZ{z*mSmOmNRfGX76_XTPV##X7iD}WS99UBLHB=6?Hs}Ls8jn0kVSUiM((0JIV<yp3UW%RB>)Ro5B5Q${x(AY^gQaoK1A|phGLwR9f)^#ijcv9J`GP$j80fNCak-ybX1yd?BG;t|8<MP-qs27Qot&Z|{pf5I7)(vhkNv2fwKZ9$li#_W>6&;<o1Uwq6csk$7l1p?8gPA}R+uJe<6QXs=uZP@4fFbNMMQ=VG4ue4(&<UjW9as5YUC8T*i_xa~>w9?!cfaJG3UAPM9|LT?9ES_apS^m$-uIQGIUxoeQwW-DKcKld8OP;3q4KJ<1dI0y(ViuSC{R!qV2d}ktuge<S^xb=O2-NTsLI}OdBvM6k`SW#GkxP}!+JUSb?g_eA`vEr}1bg4(lqh@qAel?$2nU)%A=ef}0_CNekh;3zhwFTy-*J5qa8|8g0g;FZ+lcNPSgM);-a=6@?U2tnqXa^;VB-xv#u(_WCO8?|al=c>(8Xm=(Z&giOKmu+WNWdD?CXx66g6V+u0a&4`)BD^XB0~w7qa14&VM(GmdGp!X(6!YCiw3iR=#hdui4h*APBUU%p%3H^V08P;dQuLev9lc1XR+Y2$;BjsNIGo;Nr_;1;NLDsP|gjQ9vYrLA`uirslV`k(PBXKoNtir;v%U6tpYTJ{4ikLn%PX3jYbQ*;2o@@$V{#-a_pK4aQvqTTmr+0Y{D_sV+4=H4iy2_gbeM-Kb)V1glm-q-X*zrn%<A0A)xi!ad0eRZ<Oste`Y2688X&zwA#ZcJ13W$M-!W?3Jd0Srq^#7&aQusfH(Ks*5O4+y9S8l72O0K3N-HsnHLt)MWnl7v4URkno8QqdC1eXA6QThXj_dPu@DFfHOziGYr)4Loa~0w%&w=Iw6e547;!Ud1~DNIiq;~owl}Gb6mZ6Hp-Oup7ZX<yjZg;UDvcbeGwBud@&3oVkN3r1+i@7VTEg)Q3~+n$mz-@equ(`KDJc#+&5bc<zJ!xaIXO-BzG!AKRVn4G(Ce2uM$*bW{8UB`F<MeF2Cy;Yzs@379#94RV~QXbS~jtEhfGf{?U#{Jf0e|Uim_;V+$V}NLM<&EX|Od`i5V8uESQ46MW;Zd9$YYooIr$Y&5U^w=0z$Ml)>NN?_g9~VH8jcW5gOtiDqmga+f$3^?8)<@5@vYVi7cDefp#0x61U9O^8X)XHc>hPg2%Gf&T=h1X7mRP}V^$7$cCRf;~#{lN^3==})Vw$tCR}NgtD*W5ig2WybC2Yg$yNAhlmmiqE`Fb2nMrmR0Gg`>QY>na88FN1FbM#sJ+X^D@rN)}eBdQbc+t)(jQdfl1zGm5%%d$y(eZt%0PcGhRI`72|Qsa+@D1D5W($%-sWjkBU<L9QFD|dWN=Fhw1PFt2@t<kE9{d8@orm$MSNDtX8IsTE%ui94K%5Cj|s|qk!Ozh3P;T5otT0{w|<YX4TW}Sdp4^3l*9IS|zbzUWpCw3;x5tsB^t3^a&v$xR1>NLZ|{SlH$^_+BVwAMNK)Vx1oe@h|5OOPK~6uQ6)zMFg2s#5QcLGxS+C$Ir`CT=Yp^K7(-o0Skt?QI*8o8OntuWK2054a6JWX%H;MGNCWj(0e}XbCgs<b#|VxV1)8COIBXYCQyF}Q$#mL%=nGApSU*K5q(QpsncyOG8E*We5nwk8Xa@5=H6^@B;i<?HT>`~PfdJaC2rLRSmC7YNs+VGK7<?M;a~LKo(^d^e6+TgoBiIItp(l)SVRwO0Gi_w*E@5SXs!ZG^xoMf0X(rt*)XhsvRJekWuS$>v5S@aohu1gVf;GF{#41GzoQR8ePCezZM6o{ay^Hg+q)3ng_ud^;q8XuNuZXHVei%*ipbv=EajMHiUoA%EqM@R)Hy@u&DG<T=;v-<303->_d{jnJtfR)jpkia+T6qr-KfJuVR90MPsuJ7D?~?{mG6md_{0!R-CBazXHN|874$A`##4O~lAh6P700ulZRhpOu_J0&f(5=PHoP1v_oVOU1ycS2*X+w=^-5PkY>~C-80zsySFy$HXj|sukJp%@NewnP`0{&B8!6U{nyHCqis@pyQ#%ZlUDn9L>xXt8P#DxM?sbm-eZaCye0LGDWg&Ai=os)z-mhp})$rgn%qgaDEC1|R&K6$Rf1HJ-8QgoyEmZNRMZCR{L6W9!MsO>g0L#pg3tb$6XOh;H5GK`}tc^Rqzf*rU@oDNJWp3t1dmZGA@88N}r>s9IuZA30vI4DWD<{b+4fPzIvhBY+zA7$q#{<T){r6_5H%{ZM#)R@82&z^Cq_@~{#J%DWpDYi=gM386)xCOwToYfT0v9#6G2FrDLWSWYD03Ex^O_Ca9bm7KD(9{aG2#ktOPbc7+dD?&>ocXRFy&QPHhNcPqI^#jU+`6I*=MarOY@4nbOUEt(#M>)FS;p+#nhceec6Tx97|=3)I^*GrtHr9}Z4ebxm=q$su<Op0bpRkVvq;A(wVk+0%`>e;ZJWbCr3zV1kDF)Nz7g~bqFm5CVcd|m*4x^@+*Oih&!?zyP%XZ0MckPV6(%$>GgXEM?nxEKb?}t)j*5*SefAp=Uttcs=~b;`^<AOH4qTErxfEmRI2<GT=}bPyN_^2WWGm6bw2_vGB`-)10OsX|_ZrC?>ls5&x4ipQ7ia1B7GaEr3SuSvUYJJL)aR!Yw}###Vb24FavzJ}(JK$qD;Zml=17}$F%AkeJ!8jj(j<i6{uuH_YT|A1O1btpxpj9-C#X;+_ZY3Hxxf2q7YjifCat4Hfn&D0m=W#z#27z)gPV(J(YxuLGc~9APOJAGB9|jHA&-F0qg^5aP}>0$fNeS}$yG>7w-Yit*w!vOxEimeWYMMtgTfdV=yJ>!yyRS&Nl$R#Xl^nikQcI@&3aF!qbb~p366tMEQfDOdRkUippMgWw?)N)r2>u2rZ8R4X(?E5{TBt@tnGlwl&N_IEAa5qv{aK&+3{wJfR7&C=EcKe^_xZ^f-Cq|fUE#~^R2^I8#Y_8Sc8=?LZNEr)z<K<$Irh=0IVq@a#fQM_(Ocw?5fwmKUx;-^0f^V!_1cBgUgZTEMf!E$P7D_d#>{wzt=p+E1A@tiYd{{9-|*uS8{ZOX!ZNJx9+%URjiO)uZjFY&J~*+i7VL0Kyi-)wv*j~#3RLLfmL4gO!<!+XVfJ4Vkl!K+W<}?1lY91#1oDHFia-rr81`liNG#TgSyKA4KbPvXV-N%F?w+$SCA+@swNlB?%JZ{?nre*aD5esM^Tx-FQ=UtqfhYV=mlm@;2{?(=ox^)PiKa8nHAU~E_3t-eH?QoI*Cy1F4z7On?<)%=OH9iycDra4m=(9RYKWntg@dqamTa=1Uc%Ejh9oQ$dw&=dLo97GOi?vh81PHW~UjoS(|v&YAy&%2kI*e(=2&`LM;ff8(y(i7gimpa}06dwjNNid@9Yoh)g9UuQfMJc5={-6i<&O8mw7;F_V3E3HC^lyVF;}Z#c(Ea2^HA(SxN{IE7Olhp;sXyIDTNmwD3%Oc48PbKBZ7Z{`Op(r*AT`>H@;%u^52(@O0itqulTiYcyXquq53Y;HPp5%^cOus-zE;Bz<WIbD|wYtTsIHRHENwrd1yH7fB|Bw=$ejdZYWwHVlNC)uS9A$6#@JkVCUDpxQk2CPI%Dx+;otAu3-2D}@W5QGPB6N#Uc)dHX$lh3&+aEIbLz#|l%B8HpQJah(><4tR$Wt=1#4$7HQNTBAi(^fdbkUa@`vA<hPE(Y8}z69N{X+o+bp@pH^W?ShQc%*bA9gh;4=o0Or@m)_U2Bmg9%7G5lT2TZW>^hW}oNrRFBNGN=_KD$rTF3`TkUa(EII`Q^wZMh&P6@L{v7{@I5k=spOQJlUA%uTh!)8r3tF_k*_|nt1JH73$mylJ5B-n;V-;OeXsB<Ii_9hB+E|qLwPlGfQ_CkOc_!j%(k$r@az5~hJ+d-`_(pzDItdlYLbQG`IsV0PNi$pz82OtU*0gRIu6Tml}f}AfBn8D#i^BCo8U_w#vo>9YY6nAV}lL#Y7kJ<L(Dm?ryA&cD1`C-qOR0gxl8A0k*(o7)jId76$sMaQwZ8Z?qB>)`bHj+gvADs)7O2X{ZxEcjWwq{o6YLZW{2vwqlp%Q2UcWq8dnr@|?!$4vyBL#Z%RuohxPwhf;e5Fc5CcMIwv~>4RWglL6!Rik(w218v$|9+1>t4<JrZnw60%m1W6QL=oV<bGDP>JtwvkHqEWx6S&M|<41hjb<MKRLBu*hQ3<l0T*y(!9RlCFG5|YD^{&3Nh_AH_3}%x~ty8q9kw$5`L^uxMzW0lccyYODWm@h#rhzv|kiGZuEYvwYlV}Azm&A(Hcvcr>=Pf!?{jwhzlU?ot`YLA!!9mWS1m6aZv<diWfG(FNkC$;9Q+_(&$`MYLQM4O*Y9G$L&L5<6>pmRL4R(f%}PmQMu~hA~yxcTVknW<u>T!XuHghTC{*V?@<otK(;8QC{=RPj5DFYV!3sZ73vgkeDIC4qyQ16SGi}wU^|VX1ym&emvHNQ-7{yq2lSwLUYJ0}hVi0wNd(#AJHS9qYA_`4FL0yD96~lX`Vk#Dtg6zDd~0JK83uwB3N0Ozh715Kk<`%|ugXAqI9Be*m|HV+wS;?Kl~NBf<co};qGeKF*C~61ZBENNS+HZ=>@JP&2|(y<=@!!Yq;_3vEd$Wq)BFJPIMX}C6!ERBhB`xtu@Nc>O@ap_T?F~1SxCr*U>RhkPg5U5);?+1Nv5zKG<CWmV<m8~!eEAs%fB#nbUC6~d}s1Y@L0uNhF}TWERG)$ZllUnU2~Cb1uvdX<8g=T>PeY5dqNjhizSaRk{1p|NXJXqir4<g5|Vqyre|8X342olOl+qPWyVo?0QO|d2RDJ+W>ZunJSL3lyiAK15uz%}%D4-~_OIUjpy3K3k1On_crGs24c*h_!bI3k+PHJX&rz&p0YX|m!G$-e9uO$=B)VO5<+1NU9Q9l`mW)ewDEK|eI%CxstD=%s9LAUDYa-CUI&^8Y$o%FxaR4t64ek8~nZYY>poF22kg(^3#t@mBys@O$2|0h=isQhTHKM^JZ$f&5fxlU?RyY;UjVC|6-tXTHX-<hMK$V$RbQh3ogl2jkh-MhHXnM2@T%M-`Zf}<WR3Y0zcc6kN3So9pI>9>|fb3wkN_bnf*Frs3E@4xO(9kH;>VgukZB#~3T`ld;V590LVX2|f7H>{l5`vL}CGZ%BY122stjn+zB%&tOvr_eW&B=S7v|lImq(l(JPN3V$^>pc@Z^{LC28a#>=&e=fGRBz#;5}iXG3#_rHeVCY?VYfM^oiNQFTZ`WUC3%AT^Y}b%5_)R^We~iJhl*@qRYr*n^a1&@hmSPV_DR9@NX!qd1`h#b@Sk9yQI#Jftw|Nl3fI>e!AK1NcwDE3kvERunNXGJds>I-M*3}wJ|xKWqRKgbQX=pW*;aOEhr7mL`_ua+R{SR!OBx{(X%et6=2A7i~H#@u4Ks0SB`~Kap6+E!6s8Z@X499CYeg=<@&bpFlQ0%n3VxY&gZrJW$wAqZH?snH84F}K(ffigI8|t5xl_yxi^k~c58@*Uutni%7J@G3imX@36Rg^#sQ=X?K&2!#I)O(in@z=gjWJL4g^0zR!U{7b%5GYbc@&~_g$0FSY=#PdV};-I7$+%ISg=V7`+-Iutlb9eoD0W9-&g1l@hX9l+{zTnmn%3ISQL6T4n*|6e5J&qFEEUvd_lVbwSAJdS$%$1ly0kr_>Izm31o;Tb>xTLWGwIIDMZ?i^?SdL4hG)pk?!2QsIRIb~FXWIM(iFIj)eTb?O+&jT9pqo<y65BborIaRPozq1}^VXc28gU9+;di3Q_!UXBT{;scSzAB*AGR&}j;Q}J`s6w=c$qQUoqce=P2IPz)s&ZyMST0#oani$h7q2wZf+r;Eh?&q=*OQo$8hK6}XsvAIlTA<`SH!l&_kkSj$WAiYYIIRQL3g(oQDUd_W2%q5hHMRlOVIksfRlx$m136j$E~_D2Kpr65(V*n2z#Kl1g6cX4W(Q6LU2(y<dZ4-lV0?y}UFCG}`f}d120K4is6DNhL<4gg+j@ycs(E>;-&-Noj&M;w<k4OEh=1UW9c-}BXt*GI;PGhtu&>qiBEPyM3N9#plG`%eBUUu2XLV#~@U$6aNnHqI+eDbh7faM#MnzQY%*xh~86p%Mz{&(Sm>Oy9MLUn59i=ty(q<WiOyFzhc#yo;Xrwzp{xi!rCY=#j+O!&Gu@0o9fEC7I8M~>jow<P4q^<uME2k^n)AGDfi436jh^=JI1Kenn)AxR?UZR^0?X7^(G;0Wx;8wc5wBR;Ld7ak$G-SjfF>#qnke0>owkRWKcv;d!I>jY|7df2DUZF+q1h=VIt%|lCOld7mI!(+)wJ*dlU{a^otT^_wJeiP3fken!e$)bgrtx2ByMAyQkhC&u{#45@ElP4k6?Ny#{w1X?Y|ac(BLwx!d}s5$FhTr#H3ktlVvu&+7lqy^LV`f8RI#BMy7Ds;7rP<IQK;9nRK6*SgfLmqf{N|N<fZpjov#`9|3H~TvR9U_|DCo6IQEP*g#vTY$GBonfm0IwSlJKMHc1nDEmLjO7gOjFZ*BS!26N7TRe~=Q5H{j_UzMilgG$SFS+$BVO$6=7{oDJWW+=m{&5H#kug4jj7rw!=Wun&fNEmqips{ZUY-2<dfifTL)~TGuMbPSMZ%z-P6BRMK!|E}Hodx%LL7b}~(q%Y?kPAQa7Uz?*eg-==ic7*^B{K$G+^1>vgDMKb@J{vJ<v9@Xuc&-J4OcmV(e-i`(UX!@8o>FZgL9&=3)m&wTnzM|41z#}K0uvadz9TC1$6(c7SRxg%0U7)Vf}z;{KlRu_TG3CzWUk0gP95K@XM3S0VL||VKAwM)L$o=HTx0?dwu_~%%v;XZ87&EHI4<}rOFegSYNz_iF}h4W6{IrWWH9N=Xu|3+w}pow!>>)?f@H(3d$kRkU_OJT=G`q%Yut(nMy|~OK5h(;`~WxOM^{NFOTOEn|Nb`u$=PD&Zh4mFhY#B4ON0-m6k|eD!rEPkv3a5XF44AMlpg=2^r|r6I?Lc!?(~n;Ftjl4A|6~_;iCUXj>=)X0oDGdBwi^2}gX9oEF%?qF1g7z;WM<Uv(L^<TeJRyE0mL`|Y815PE@rkqO{!6V0YnP_RmRJ3@9~L2lFDeSYthe)(){RBMA&02^{!2x}KiI_`{FL;or*t?AaARRr4#6_7B~eC=MA$yLe+947g3v3Xi>Kw=TVifec1I4?S222zO<N0Wku-$HZRq=RnyKxynsan(%&7@nPLHh|Ox>TUtx$B3-a!$|u|mlcl=?%sm3-;jNwQhOHK&fSFXO_4p*#6YB=NT^IcP_U|jV{3+{<2%OGJ>L_lM@_~kw9TXmgNlSfTFOT^Ic2|9!F1s4pKLnAeJU^$yK7?B=CoCw`|S?x6ItC%Zun=(Kk`yp*1VwCoTGpySVE|EGL4to(m*D`^5PGfBfu+W?1D?zvchpdFb)w(Qz|J{@zT_wN_7Wa|I=1+A;CE2C%iSXaw_B!TPO%JA<j@*z}d1Za4VuN1=YQZ`WbUXC}~w`AtZoKxo~>i1EC->HU@yEG6`W-v@b1&GR|58d99A`X6f)Y>b8C3Eprcf^M|P`V*PTv7;~%96k_MbD`jL1R`JA$WR3vDA4pZdO$lW1`g)h~8sK=VIp+|!fXYb5IxJQ9i(2DN&HrKwX-!HY4t?^nhtjF%wN5EqlIJiWEr6khRpHBYL5*05SwI$fWa2e3Es@natyD?Zz&w;Us@!T7vYwK@E!0@JjR6u`=m0=#4k>s?)q9yDa}KeVIgDIYs4$6PCnpQX_XhUqn>G(T<-jnoa;aH3uBDW^-twk;3tBh{O`Pja)dbGemk9`eO(z(<0O<jsYh@g5hV^qljNxq<(!`;vx}`co3-tEj4S8&}DY!bxX;zDBO*XqU50K)aqBu*yo4!H<-;*p#x2T3p_2>6`wURz#-BhSvbzVkKUwE|yDUUK6qi<x@`4{Y68ITRj6c0bI#CZXYKezNU+{kfS!=JdP`K2T4yh`(?#;V_HQF~cM85IrSAK9cqc2OuPN}Y9|&0tAt&S~$U2x8PuE98}Ll*DyYL$4~37IQuPqQZ?2SLHfRLsMooY(11!xf!=hYvfr<AiRwukpF0^kTJfmXcp;QmWP3kx|Ed$0^b_k)fI6iWZj6EMx70nK}pDOd28BcP1vZ!0JB-(bzittwl;u-0P$2RJ0~1xiFdJncT7$v3;7LY1>UH=^!CI&eejwWP-R5Mf<m`tSdhAW^6^+VNaeK)ovM1RWrYkTEnXd>1>p^uS%$O+-l^e<CIcx^MyD{QqCD`S+I>(aPq(e!<1X7ANda*YQ`7P-vN7#fK>;F5Ux1Y3F^}}%sj;1{@&?Hc)WkMh(zj+P0|`7cu7FW8;Fhx$i@<4-62Gk!BI$R<xjfHpPB$#izc)+X7*~lVbx7N*Cv1`}0U^SUk#`H&5A3d@qt@-u*Mof1m|M>%)SgTOmINlBV-miuY^Kpg$mA~4(iHm1LQr}g*9?H2R3Ng#)z17O=RhhZC)DgfEns#)suL+2k)zy*+G)H<$|a4%Hci#TG6=vkl10++@KH^dty=is;on;a;$*>01G_ZhT#Ahjb}9cFI4CC<!0R6zT$cXaM#-s>YpI}5e^njc#X9Zdu!)WteSs+(g?Cs03^)!MgIes0GI@*}qbwh(08sLwW~SB_WT&OSy+Tz2U4ziF1h}D#$WWj!=fiy{+t!1~<EsJoBvHKs&MRGOBrQVgHYg1(-*vlEH$H-c2v@u$^IU>=Jy?O4eRX+11MyhQ0Ykp=NDYYqAmmohBX;j1bW$p`7rOTJsCR5tHH#WA?jM6){pccY(}B)zRjG)iT4qA6>^bzN6lm%B*<b8_LlFuQcr|vh8UeW9u)IGLGwL=M6()ujllImq_hgR;!4uYDS@Hr|fG&H+GyZI9G`=E`!kA{8e5Cr{$0aCg6PVMAHc-CIuLbHeq^(db%!mh!%L=G+))8Nz<FoQ$c^Of-THe+|N2QbY<!6lO<rCvb(O6?|w~E}#t+Z@uvD+5Auv!kaGZFk%^g6uJ3c$Yjep>Y%^Kgv$Fx2RIj3UpDhiI_^X;)d{sARl%mF58sNHxZ3`y`KcZ0c<h#CN+()IM)`(}bewG8!mEF1Z+oSVf5n$4#I)E4<^(c@T@$bfcdx-u=wB>D|6_b+m4*SZ4djp~ZPWV52FjMWtO+mc^#Yz7157u*Eq}_#Ib7T$D8{9dU&N`rVeTIo}nduVx410<ud_<y<JQHVo<^$GckfvrS?H2CUVqo0wT~QA%6?T_~=gx(O?nlTm`eB_8LTIZB=0uSqSeG$TU)6e@)b9%G`=g*t6gNsjv2#+hWr&bU};U&Xdg{h^Arn*JKA!>N?^O*jB5sh^=9O$Inu`(v4TR>++g8RNp1Y){p*acGWKbu%`9oyt=V@^ttMg1EfTW?E#nw5}61EovS_D8p=Q<+q)TAR?$}+LSt*ie5*uhyb2_c`~nlttZD{p;-pi+owwXj*xD%eqA9WR-JUV^90v(pf$pw%uuG+JVOyoAlklO0SI_f)72Y>bw9LE;lw-66Uelt@77h}NOln276=7$xtO9q*HS7qqGwB`3q=8d)hP4r!xCkRFidsWc%r#3;e7MaP2sq>hc<2vI_>PXPjdh$19e(+*~!DNSg#%?S!alylrCg<Lkg^kzQA@%lgBS$P17T~x^qz=*yQB@43u}<D2v~u3@84V1eo(bxN|q~ab*FTclEog9BgX}KR>Q8hk;CR+4Fk1S3z7lt>C5=z4{E9L@<dhKnkQe-3}g^`)ANGI=*WS(xm8QL{pkQap+u;ZE!QtUK&sy0o)g9zF92<QOrM7Y9ulgG4cN>#tS8kNlRVX-t>AlDiY+>36$WJoOHRHXd!wJazxl|E%NKO0m_?XR^wO^$|%~P%H!a_bjpS{ibR#bBp#0?5s0klrbEY-8*;78i*4B)Ku~i}jwzN#d|Z_0siW*2R#Xy)m7AkLHZ9ZJFSjLx{bqBUH2T1veKaKVrjR{UM0s~YHl}P;xrID&zS?o;;tqjH(iEJvK}4$?o4yH3(xpV=K#+#9x11j(g}WubX8skdxF|EP0=DW_r=~z#9E-ueRGdztX_L+R7{bO_Y&yMj*fXFhKcK5JUrZ>-G1o({8K*~ft6kUGbyT~mDS;1kQZ#7To9_e8xAnWD`UTjElAgJ~GdxSe*0#v(6zkm8QiWwKE)GHlw=)NTQ|UM1-hN@UB0hNtAii9$HMlw3uHQy47GFZgD>N>_=jZhR{e?F>jHe@QtLmUz%(6nS2sV3#_+VWbiK<OwK^Z5~(Kxe$4Eeo>OGT$jc*7<gRn9aK-6KfBCi~GWolttKwy{L6pyXtGEVY=6>>7?v=?h<7jku61SOSR?bU7w|QG~ba<LNX$g)h&8y-xR|$}mva&6_8a_>XHZ7Dias?d3r<UkL^eam=MII>;kdaV`t%0@w~1noi%kZOWMG;L~0NoDSH97w*vyHUX@ugT5*DQ0P+d&HhL=UPgP=HxHFoH3d=#--nF-M8<MW9w}`oO3>4Wr>~P(I3<T*On#L6DPGJq&5TRtS{c+9s)(8Ag{Pi^e&Y9!nwtqRB8;y>-c#90aN+nu)q@6hju4%Ct4)csNWcavbZ=7<G7?+G7#EN#Vk18Pz*~Sv?Gn(MHy_q<5HIHIwcfZ}EDH3T--HZ`G)j#h&;E&x==qD}B6<PNlkGOzYo7mm_+Mu@+Xn')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
