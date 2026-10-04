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

_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['HIRE']]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1]], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['PLACE', 'SHEEP', 1], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP', 1], ['CARE'], ['WEST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['BUILD_PASTURE'], ['BUILD_PASTURE'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['PLACE', 'COW', 1], ['PLACE', 'SHEEP', 1], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'MELON'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['PASS'], ['PASS'], ['PLANT', 'WHEAT']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER']], 'market': [[]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['DROP']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['SOUTH'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['CARE'], ['FEED']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['PASS'], ['SOUTH'], ['WATER'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['PASS'], ['SOUTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['PASS'], ['CARE'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['PASS'], ['FEED'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['SOUTH'], ['PASS'], ['EAST'], ['HARVEST'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PASS'], ['FEED'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['PASS'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['SOUTH'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['DROP'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['PASS'], ['FEED'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['PASS'], ['CARE'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PLACE', 'COW', 1], ['WATER'], ['PASS'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WEST'], ['NORTH'], ['PASS'], ['SOUTH'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'STRAWBERRY'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['HARVEST'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['DROP'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['SOUTH'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PASS'], ['EAST'], ['HARVEST'], ['DROP'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['DROP'], ['SOUTH'], ['PASS'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['CARE'], ['PICKUP', 'WHEAT', 2], ['FEED'], ['PASS'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['FEED'], ['FEED'], ['CARE'], ['PASS'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['EAST'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['HARVEST'], ['NORTH'], ['NORTH'], ['FEED'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLANT', 'STRAWBERRY'], ['NORTH'], ['FEED'], ['PASS'], ['PASS'], ['PASS']], 'market': [[]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['FEED'], ['CARE'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['CARE'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['FEED'], ['CARE'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['SOUTH'], ['EAST'], ['CARE'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['FEED'], ['FEED'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 2], ['PASS'], ['CARE'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['DROP']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['CARE'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WATER'], ['FEED'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['CARE'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [[]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['NORTH'], ['FEED'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'SHEEP', 1], ['NORTH'], ['CARE'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['DROP'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['BUILD_PASTURE'], ['SOUTH'], ['WEST'], ['PASS'], ['PICKUP', 'SHEEP', 1], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['EAST']], 'market': [['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PLACE', 'SHEEP', 1], ['SOUTH'], ['FEED'], ['PASS'], ['EAST'], ['SOUTH'], ['EAST'], ['PASS'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'SHEEP', 1], ['PLACE', 'FERTILIZER', 1], ['CARE'], ['PASS'], ['NORTH'], ['SOUTH'], ['WATER'], ['PASS'], ['EAST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['PICKUP', 'SHEEP', 1], ['COLLECT_FERTILIZER'], ['PASS'], ['BUILD_PASTURE'], ['SOUTH'], ['SOUTH'], ['PASS'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 2]]}, {'farmer': ['PICKUP', 'SHEEP', 1], 'hands': [['PLACE', 'SHEEP', 1], ['EAST'], ['EAST'], ['PASS'], ['PLACE', 'SHEEP', 1], ['SOUTH'], ['WATER'], ['PASS'], ['PICKUP', 'SHEEP', 1]], 'market': [[]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['EAST'], ['PASS'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['PASS'], ['PICKUP', 'WHEAT', 3]], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['NORTH'], ['DROP'], ['PASS'], ['BUILD_PASTURE'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['PASS'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'MELON', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'MELON'], ['PLACE', 'SHEEP', 1], ['EAST'], ['PLANT', 'STRAWBERRY'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['DROP'], ['PLANT', 'STRAWBERRY'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'MELON', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['CARE'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['CARE'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': [[]]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['EAST'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['BUILD_PASTURE'], ['EAST'], ['EAST'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['PLANT', 'MELON'], ['CARE'], ['FEED'], ['NORTH'], ['PLACE', 'SHEEP', 1], ['FEED'], ['NORTH'], ['SOUTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['PLANT', 'MELON'], ['PASS'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['WATER'], ['BUILD_PASTURE'], ['FEED'], ['EAST'], ['PASS'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['EAST'], ['EAST'], ['PLACE', 'SHEEP', 1], ['EAST'], ['PLANT', 'MELON'], ['PICKUP', 'SHEEP', 1], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['CARE'], ['EAST'], ['WATER'], ['PASS'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'MELON'], ['WATER'], ['PASS'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['WEST'], ['NORTH'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['WEST'], ['EAST'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLACE', 'FERTILIZER', 1], ['SOUTH']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['FEED'], ['EAST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['PLACE', 'FERTILIZER', 1], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['NORTH'], ['DROP']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 2], ['CARE'], ['EAST'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['PICKUP', 'GOOSE', 1], ['WATER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['FEED'], ['SOUTH'], ['NORTH'], ['WATER'], ['FEED'], ['WATER']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WEST'], ['CARE'], ['SOUTH'], ['EAST'], ['NORTH'], ['CARE'], ['WEST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['NORTH'], ['SOUTH'], ['DROP'], ['BUILD_COOP'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['PICKUP', 'GOOSE', 1], ['PLACE', 'GOOSE', 1], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['CARE'], ['SOUTH'], ['EAST'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['NORTH'], ['DROP'], ['NORTH'], ['EAST'], ['EAST'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['EAST'], ['EAST'], ['EAST'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['BUILD_COOP'], ['EAST'], ['EAST'], ['EAST'], ['DROP']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['PLACE', 'GOOSE', 1], ['PLANT', 'WHEAT'], ['PASS'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['CARE'], ['WATER'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['FEED'], ['SOUTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [[], []]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['DROP'], ['FEED'], ['WEST'], ['SOUTH'], ['DIG'], ['WATER'], ['EAST']], 'market': [['SELL', 'MILK', 6], [], []]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['PASS'], ['WEST'], ['NORTH'], ['CARE'], ['WATER'], ['DROP'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_LAND']]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['DROP']], 'market': [['SELL', 'FERTILIZER', 2], [], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['SOUTH'], ['FEED'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['NORTH'], ['WEST']], 'market': [[], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['CARE'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH']], 'market': [[], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['CARE'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': [[], []]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['FEED'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [[], []]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER']], 'market': [[], []]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['DROP'], ['COLLECT_FERTILIZER'], ['WATER'], ['PASS'], ['DROP'], ['WATER'], ['SOUTH']], 'market': [[], [], []]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['EAST'], ['EAST'], ['PICKUP', 'GOOSE', 1], ['EAST'], ['SOUTH'], ['PASS'], ['PICKUP', 'GOOSE', 1], ['HARVEST'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 4]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PASS'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WATER'], ['SOUTH'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['PASS'], ['FEED'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['SOUTH'], ['DROP'], ['BUILD_COOP'], ['FEED'], ['SOUTH'], ['SOUTH'], ['PASS'], ['CARE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['PASS'], ['PLACE', 'GOOSE', 1], ['SOUTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PASS'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['PASS'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['PASS'], ['PLANT', 'WHEAT'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['BUY_PRODUCT', 'WHEAT', 5], []]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['NORTH'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['FEED'], ['FEED'], ['NORTH'], ['HARVEST'], ['NORTH'], ['EAST'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['NORTH'], ['CARE'], ['FEED'], ['EAST'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'COW', 1], ['EAST'], ['WATER'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['PICKUP', 'GOOSE', 1], 'hands': [['SOUTH'], ['NORTH'], ['FEED'], ['SOUTH'], ['DROP'], ['NORTH'], ['BUILD_PASTURE'], ['WATER'], ['WEST'], ['CARE']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['SOUTH'], 'hands': [['PLACE', 'COW', 1], ['FEED'], ['CARE'], ['PLACE', 'FERTILIZER', 1], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PICKUP', 'GOOSE', 1], ['CARE'], ['COLLECT_FERTILIZER'], ['PICKUP', 'GOOSE', 1], ['FEED'], ['NORTH'], ['BUILD_PASTURE'], ['PLANT', 'WHEAT'], ['WEST'], ['DROP']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['PICKUP', 'GOOSE', 1]], 'market': [['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['WEST'], ['FEED'], ['FEED'], ['NORTH'], ['NORTH'], ['EAST'], ['BUILD_PASTURE'], ['NORTH'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['BUILD_COOP'], ['CARE'], ['CARE'], ['EAST'], ['NORTH'], ['WATER'], ['PLACE', 'COW', 1], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['PLACE', 'GOOSE', 1], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['EAST'], ['WEST'], ['EAST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['EAST'], ['FEED'], ['EAST'], ['NORTH'], ['CARE'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['WATER'], ['BUILD_COOP']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['EAST'], ['CARE'], ['EAST'], ['BUILD_COOP'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['PLACE', 'GOOSE', 1]], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['PICKUP', 'GOOSE', 1], ['WEST'], ['DROP'], ['PLACE', 'GOOSE', 1], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['SOUTH'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['WEST'], ['WEST'], ['WEST'], ['EAST'], ['FEED'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['FEED'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['DIG'], ['WATER'], ['NORTH'], ['EAST'], ['CARE'], ['WATER'], ['WATER'], ['CARE'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['BUILD_COOP'], ['SOUTH'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['PLACE', 'GOOSE', 1], ['WATER'], ['FEED'], ['HARVEST'], ['EAST'], ['WATER'], ['WEST'], ['FEED'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['SOUTH'], ['SOUTH'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['WEST'], ['CARE'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['PASS'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['PASS'], ['WATER'], ['WEST'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['HARVEST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['CARE'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['DROP'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['FEED'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['NORTH'], ['SOUTH'], ['CARE'], ['HARVEST'], ['EAST'], ['WEST'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['WEST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'MELON', 6], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['EAST'], ['EAST'], ['FEED'], ['WEST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['FEED'], ['SOUTH'], ['FEED'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WATER'], ['CARE'], ['FEED'], ['SOUTH'], ['WATER'], ['EAST'], ['CARE'], ['EAST'], ['CARE'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['DROP'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['DROP'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'MELON', 12], ['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['EAST'], ['NORTH'], ['WEST'], ['WEST'], ['DROP'], ['WATER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['FEED'], ['WEST'], ['FEED'], ['PICKUP', 'GOOSE', 1], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['DROP'], ['CARE'], ['CARE'], ['CARE'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['PLACE', 'GOOSE', 1], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['PLACE', 'GOOSE', 1], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['SOUTH'], ['CARE'], ['WATER'], ['NORTH'], ['PLACE', 'GOOSE', 1], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['EAST'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['PLACE', 'SHEEP', 1], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['FEED'], ['FERTILIZE'], ['SOUTH'], ['FEED'], ['WATER'], ['CARE'], ['WEST'], ['PLANT', 'WHEAT'], ['CARE'], ['PLACE', 'GOOSE', 1], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['FERTILIZE'], ['CARE'], ['WEST'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WEST'], ['PLACE', 'GOOSE', 1], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['PLACE', 'SHEEP', 1], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['PLACE', 'SHEEP', 1], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['PLACE', 'GOOSE', 1], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['NORTH'], ['SOUTH'], ['PASS'], ['WEST'], ['PASS'], ['WATER'], ['PLACE', 'GOOSE', 1], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 5], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['WEST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['WEST'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER'], ['FEED'], ['FERTILIZE']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['FEED'], ['EAST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['FEED'], ['WATER'], ['CARE'], ['EAST'], ['FEED'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['FEED'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'GOOSE', 1], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['FEED'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['FEED'], ['EAST'], ['EAST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['CARE'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['EAST'], ['EAST'], ['CARE'], ['DROP'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['WEST'], ['FERTILIZE'], ['FEED'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['HARVEST'], ['WATER'], ['CARE'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['CARE'], ['EAST'], ['WEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['CARE'], ['FEED'], ['EAST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['WEST'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['NORTH'], ['EAST'], ['EAST'], ['EAST'], ['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['FERTILIZE'], ['NORTH'], ['FERTILIZE'], ['FERTILIZE'], ['PASS'], ['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['PASS'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'COW', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['HARVEST'], ['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 27], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['DROP'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'WOOL', 6], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['EAST'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PLACE', 'MILK', 3], ['WEST'], ['WATER'], ['FEED'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['FEED'], ['WEST'], ['EAST'], ['EAST'], ['DROP'], ['SOUTH'], ['NORTH'], ['FEED'], ['EAST'], ['CARE'], ['NORTH']], 'market': [['SELL', 'WOOL', 10]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['CARE'], ['WATER'], ['WATER'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['FERTILIZE'], ['NORTH'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['DROP'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['NORTH'], ['BUILD_PASTURE'], ['WATER'], ['PICKUP', 'GOOSE', 1], ['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['PLACE', 'COW', 1], ['NORTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['FEED'], ['WATER'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['CARE'], ['NORTH'], ['CARE'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['FEED'], ['WATER'], ['HARVEST'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['DROP']], 'market': [['SELL', 'WOOL', 6], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['HARVEST'], ['BUILD_PASTURE'], ['PLACE', 'SHEEP', 1], ['FEED'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['EAST'], ['PLANT', 'WHEAT'], ['PLACE', 'COW', 1], ['PLACE', 'SHEEP', 1], ['CARE'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['NORTH'], ['PLACE', 'SHEEP', 1], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['CARE'], ['EAST'], ['FEED'], ['PLACE', 'SHEEP', 1], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['NORTH'], ['FEED'], ['HARVEST'], ['PLACE', 'SHEEP', 1], ['HARVEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['FEED'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['WEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['CARE'], ['WATER']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['CARE'], ['WATER'], ['FERTILIZE'], ['EAST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['NORTH'], ['EAST'], ['WEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['FERTILIZE'], ['DROP'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['EAST'], ['SOUTH'], ['CARE'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['CARE'], ['HARVEST'], ['PASS'], ['EAST']], 'market': [['SELL', 'WHEAT', 7], ['SELL', 'EGG', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['FEED'], ['WATER'], ['DIG'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['CARE'], ['EAST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['FEED'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['FEED'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['NORTH'], ['EAST'], ['WEST'], ['HARVEST'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['CARE'], ['WATER'], ['FEED'], ['WATER'], ['FERTILIZE'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['FERTILIZE'], ['FEED'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['FEED'], ['HARVEST'], ['EAST'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['CARE'], ['CARE']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FEED'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['FERTILIZE'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['FEED'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['CARE'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['CARE'], ['FEED']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FEED'], ['NORTH'], ['CARE'], ['WATER'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['CARE'], ['FEED'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'MILK', 5]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['FEED'], ['HARVEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['NORTH'], ['DIG'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['PASS'], ['SOUTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['WATER'], ['PASS'], ['EAST'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 4], ['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['HARVEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['NORTH'], ['PLACE', 'MILK', 3], ['WATER'], ['WEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['CARE'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['CARE'], ['FEED'], ['NORTH'], ['EAST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['HARVEST'], ['CARE'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['HARVEST'], ['CARE']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['FEED'], ['HARVEST'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT'], ['WEST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['FEED'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['EAST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['FEED'], ['PLANT', 'WHEAT'], ['CARE'], ['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['CARE'], ['WATER'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['WEST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WEST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['DROP'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['HARVEST'], ['NORTH'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 3], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'EGG', 2]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 14], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'FERTILIZER', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['DROP'], ['FEED'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['CARE'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['FEED'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['DROP'], ['HARVEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['NORTH'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['EAST'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['FEED'], ['WEST'], ['CARE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['FEED'], ['WATER'], ['NORTH'], ['SOUTH'], ['NORTH'], ['CARE'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['EAST'], ['HARVEST'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FEED'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['CARE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['CARE'], ['WATER'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['HARVEST'], ['FEED'], ['FEED'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['WEST'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['FEED'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['CARE'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['DROP'], ['DROP'], ['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'GOOSE', 1], ['EAST'], ['EAST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'FERTILIZER', 4]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['EAST'], ['FEED'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 4]]}, {'farmer': ['HARVEST'], 'hands': [['DROP'], ['PASS'], ['HARVEST'], ['PASS'], ['EAST'], ['CARE'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['WATER'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['FEED'], ['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['FEED'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['DROP'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['FEED']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['CARE'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['CARE']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['FEED'], ['DROP'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['CARE'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['DROP'], ['WEST'], ['WEST'], ['FEED'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['CARE'], 'hands': [['PLANT', 'WHEAT'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['DROP'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6], ['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['DROP'], ['FEED']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['WATER'], ['CARE'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['NORTH'], ['FEED'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['FEED'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['EAST'], ['CARE'], ['FEED'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['FERTILIZE'], ['CARE'], ['FEED'], ['WEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['EAST'], ['HARVEST'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['CARE'], ['FEED'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['FEED'], ['EAST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['CARE'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['DROP'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['DIG'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['CARE'], ['EAST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['FEED'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['SOUTH'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['SOUTH'], ['FEED'], ['FEED'], ['FEED'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['CARE'], ['CARE'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['CARE'], ['SOUTH'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['CARE'], ['WATER'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['FEED'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['SOUTH'], ['HARVEST'], ['CARE'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['DIG']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH'], ['FEED'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['FEED'], ['HARVEST'], ['WATER'], ['CARE'], ['EAST'], ['WATER']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['CARE'], ['PLANT', 'CARROT'], ['EAST'], ['WEST'], ['EAST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['HARVEST'], ['EAST'], ['EAST'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['FEED'], ['WEST'], ['WATER'], ['EAST'], ['EAST'], ['EAST'], ['WEST'], ['DROP'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WATER'], ['CARE'], ['PASS'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['FERTILIZE'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 6], ['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 6], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['DROP'], ['FEED'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WEST'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['FEED'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['EAST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['CARE']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['SOUTH'], ['FEED'], ['HARVEST'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['FEED'], ['CARE'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WEST'], ['FEED'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['FERTILIZE'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['FEED'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['CARE'], ['NORTH'], ['DIG'], ['HARVEST'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['HARVEST'], ['FEED'], ['HARVEST'], ['SOUTH'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['DIG'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['DROP'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['CARE'], ['WATER'], ['EAST'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['HARVEST'], ['EAST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['FEED'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['SOUTH'], ['WEST'], ['DROP'], ['DROP'], ['EAST'], ['PLANT', 'CARROT'], ['EAST'], ['HARVEST'], ['CARE'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['FERTILIZE'], ['EAST'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['WATER'], ['NORTH'], ['WEST'], ['EAST'], ['DROP'], ['NORTH'], ['FEED'], ['EAST'], ['FEED'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['FERTILIZE'], ['WEST'], ['PASS'], ['PASS'], ['WATER'], ['CARE'], ['EAST'], ['CARE'], ['EAST']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['WEST'], ['CARE'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'CARROT'], ['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['FEED'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['HARVEST'], ['NORTH'], ['WATER'], ['FEED'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['FEED'], ['NORTH'], ['CARE'], ['FERTILIZE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['SOUTH'], ['FEED'], ['WATER'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['CARE'], ['HARVEST'], ['SOUTH'], ['PLANT', 'CARROT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['CARE'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['EAST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FEED'], ['FERTILIZE'], ['WEST'], ['DIG'], ['EAST'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['HARVEST'], ['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['FERTILIZE'], ['CARE'], ['DIG'], ['FEED'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['WATER'], ['EAST'], ['PLANT', 'CARROT'], ['CARE'], ['WEST'], ['WEST'], ['DIG'], ['EAST'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['PLANT', 'CARROT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['FERTILIZE'], ['DROP'], ['WEST'], ['FEED'], ['HARVEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['FEED']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['DIG'], 'hands': [['FERTILIZE'], ['PLANT', 'CARROT'], ['HARVEST'], ['WATER'], ['CARE'], ['PASS'], ['PLANT', 'CARROT'], ['NORTH'], ['PLANT', 'CARROT'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['DROP'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 5], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'MILK', 6], ['SELL', 'FERTILIZER', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['EAST'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['PLACE', 'MILK', 3], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['FEED'], ['PLANT', 'WHEAT'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['SOUTH'], ['WEST'], ['CARE'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['HARVEST'], ['FEED'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['SOUTH'], ['NORTH'], ['CARE'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['WATER'], ['DIG']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['NORTH'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['CARE'], ['FEED'], ['EAST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['DIG'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['FEED'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['CARE'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['DIG'], ['WEST'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['HARVEST'], ['NORTH'], ['EAST'], ['EAST'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['DIG'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['SELL', 'CARROT', 3]]}, {'farmer': ['PASS'], 'hands': [['FERTILIZE'], ['SOUTH'], ['DROP'], ['SOUTH'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['EAST'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 6], ['SELL', 'MILK', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 3], ['PICKUP', 'FERTILIZER', 4], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['CARE'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['SOUTH'], ['CARE'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['WATER'], ['FEED'], ['HARVEST'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['CARE'], ['NORTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['HARVEST'], ['NORTH'], ['CARE'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['FEED'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['EAST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['CARE'], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['PLANT', 'CARROT'], ['EAST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['NORTH'], ['NORTH'], ['PLANT', 'CARROT'], ['WEST'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['EAST'], ['WATER'], ['DROP']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['DROP'], ['HARVEST'], ['EAST'], ['CARE'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['EAST'], ['DROP']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['PLANT', 'CARROT'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['WATER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['WATER'], ['EAST'], ['PASS']], 'market': [['SELL', 'EGG', 6], ['SELL', 'EGG', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'WOOL', 4], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['WEST'], ['FEED'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['PLANT', 'WHEAT'], ['PLANT', 'CARROT'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['CARE'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['FEED'], ['NORTH'], ['WEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['FEED'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['CARE'], ['WEST'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['EAST'], ['FEED'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['EAST'], ['CARE'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['DIG']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['WATER'], ['FEED'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'CARROT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['CARE'], ['EAST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'CARROT'], ['NORTH'], ['NORTH'], ['WEST'], ['PLANT', 'CARROT'], ['SOUTH'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['FERTILIZE'], ['DROP'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['DIG'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'CARROT', 10], ['SELL', 'EGG', 4]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['FERTILIZE'], ['EAST'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['PASS'], ['WATER'], ['DROP'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['CARE'], ['EAST'], ['HARVEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['FEED'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['CARE'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['SOUTH'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['SOUTH'], ['WEST'], ['CARE'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['SOUTH'], ['FEED'], ['NORTH'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WATER'], ['CARE'], ['NORTH'], ['CARE'], ['HARVEST'], ['HARVEST'], ['FEED'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['CARE'], ['EAST'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['FEED'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['FEED'], ['FEED'], ['PLANT', 'CARROT'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['WATER'], ['EAST'], ['HARVEST'], ['CARE'], ['CARE'], ['WATER'], ['PLANT', 'CARROT'], ['SOUTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['HARVEST'], ['FEED'], ['PLANT', 'CARROT'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['FEED'], ['NORTH'], ['WATER']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['PLANT', 'CARROT'], ['CARE'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['CARE'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['FEED'], ['DROP'], ['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['PLANT', 'CARROT']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'CARROT'], ['EAST'], ['EAST'], ['WEST'], ['CARE'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['WATER']], 'market': [['SELL', 'CARROT', 6], ['SELL', 'WHEAT', 8], ['SELL', 'EGG', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['EAST'], ['PASS'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['PICKUP', 'FERTILIZER', 3], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['CARE'], ['WEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FEED'], ['FEED'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['CARE']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['EAST'], ['WATER'], ['WEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['WEST'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['EAST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['FEED'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['WATER'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['CARE'], ['WATER'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['EAST'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['HARVEST'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['CARE'], ['WEST']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'CARROT'], ['SOUTH'], ['WEST'], ['SOUTH'], ['HARVEST'], ['EAST'], ['PLANT', 'CARROT'], ['WATER'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['DROP'], ['WEST'], ['PLANT', 'CARROT'], ['EAST'], ['FEED'], ['EAST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['FEED'], ['HARVEST'], ['PLANT', 'CARROT'], ['HARVEST'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['CARE'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['PLANT', 'CARROT'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['DROP']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'CARROT', 5]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['EAST'], ['PASS'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['NORTH'], ['PASS'], ['FERTILIZE'], ['PASS'], ['DROP']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['WATER'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 3], ['WEST'], ['WEST'], ['CARE'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['WEST'], ['CARE'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['DIG'], ['HARVEST']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['CARE'], ['SOUTH'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WEST'], ['SOUTH'], ['WEST'], ['FEED'], ['WEST'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['WEST'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['FEED'], ['HARVEST'], ['WEST'], ['CARE'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['CARE'], ['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['WEST'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['FERTILIZE'], ['WEST'], ['WEST'], ['HARVEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['CARE'], ['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['WATER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FERTILIZE'], ['WATER'], ['PLANT', 'CARROT'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['CARE'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['DROP'], ['PLANT', 'CARROT']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['WATER'], ['EAST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['FEED'], ['HARVEST'], ['FEED'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['EAST'], ['CARE'], ['PLANT', 'CARROT'], ['CARE'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'CARROT', 10]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'CARROT', 12], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['PLACE', 'MILK', 6], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['DIG'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['FEED'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['FERTILIZE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['DIG'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['WATER'], ['WATER'], ['FEED'], ['WEST'], ['HARVEST'], ['DIG'], ['WATER'], ['WATER'], ['EAST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['PLANT', 'WHEAT'], ['PLANT', 'CARROT'], ['FEED'], ['HARVEST'], ['EAST'], ['WATER'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['CARE'], ['SOUTH'], ['FEED'], ['NORTH'], ['WEST'], ['FEED'], ['WEST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['CARE'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['NORTH'], ['EAST'], ['DROP'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST'], ['SOUTH'], ['NORTH'], ['PLANT', 'CARROT']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['FEED'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['FEED'], ['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'CARROT', 5]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['CARE'], ['EAST'], ['PASS'], ['WATER'], ['CARE'], ['EAST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['PICKUP', 'FERTILIZER', 3], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'STRAWBERRY', 2], ['SELL', 'EGG', 4], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['WEST'], ['EAST'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['EAST'], ['HARVEST'], ['EAST'], ['WEST'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'CARROT'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['EAST'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['FEED'], ['WATER'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['CARE'], ['WEST'], ['EAST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['FERTILIZE'], ['CARE']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['EAST']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['SOUTH'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['DROP'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['WEST'], ['WATER'], ['FEED'], ['WATER'], ['FEED'], ['WEST'], ['EAST'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['FERTILIZE'], ['HARVEST'], ['CARE'], ['HARVEST'], ['CARE'], ['WEST'], ['FEED'], ['CARE'], ['WEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['CARE'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['NORTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['DROP'], ['EAST'], ['WATER'], ['EAST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['CARE'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['EAST'], ['EAST'], ['WEST'], ['DROP'], ['FEED'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'CARROT', 13], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['EAST'], ['EAST'], ['FERTILIZE'], ['CARE'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [['PASS'], ['WEST'], ['EAST'], ['DROP'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['DROP'], ['FERTILIZE'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'CARROT', 4], ['SELL', 'EGG', 8], ['SELL', 'EGG', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'CARROT', 24], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 5], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['WEST'], ['FEED'], ['WATER'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['HARVEST'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['FERTILIZE'], ['DROP'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['DROP'], ['NORTH'], ['WATER'], ['EAST'], ['EAST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['FEED'], ['NORTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['HARVEST'], ['FEED']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['EAST'], ['EAST'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'CARROT', 13]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['NORTH'], ['FEED'], ['HARVEST'], ['NORTH'], ['DROP'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['EAST'], ['DROP'], ['EAST'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 4]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['EAST'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['EAST'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 4]]}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'CARROT', 20], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'STRAWBERRY', 2], ['SELL', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['EAST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['NORTH'], ['EAST'], ['WEST'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['EAST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['SOUTH'], ['EAST'], ['EAST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['HARVEST'], ['DROP'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['DROP'], ['DROP'], ['EAST'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['DROP'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WEST'], ['DROP'], ['DROP'], ['WEST']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'FERTILIZER', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 6]]}, {'farmer': ['HARVEST'], 'hands': [['DROP'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'CARROT', 6]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['WEST'], ['NORTH'], ['SOUTH'], ['DROP'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'EGG', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['WEST'], ['NORTH'], ['SOUTH'], ['PASS'], ['DROP'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 1000], ['SELL', 'WHEAT', 23], ['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 2]]}]
_PROXY=make_agent({0:_DEMO})
def demonstrated_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
demonstrated_proxy.telemetry=_PROXY.chassis.diagnostics
agent=demonstrated_proxy
