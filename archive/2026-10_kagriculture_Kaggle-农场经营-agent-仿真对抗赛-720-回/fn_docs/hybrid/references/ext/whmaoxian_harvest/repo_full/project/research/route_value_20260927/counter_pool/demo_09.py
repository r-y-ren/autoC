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

_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 3]]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1]], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['NORTH'], ['PLACE', 'SHEEP', 1]], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP', 1], ['BUILD_PASTURE'], ['PASS'], ['CARE']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['PLACE', 'SHEEP', 1], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WEST'], ['BUILD_PASTURE'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 1], ['NORTH'], ['PLACE', 'COW', 1], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PLANT', 'MELON'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'MELON'], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['PLANT', 'MELON'], 'hands': [['FEED'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 5]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WATER'], ['PLANT', 'MELON'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST']], 'market': [[]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [[]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [[]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [[]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], [], [], [], []]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['CARE'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'FERTILIZER', 1], ['WEST'], ['CARE'], ['SOUTH']], 'market': [[], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 1], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [[]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['EAST'], ['EAST'], ['WEST']], 'market': [[]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['PASS']], 'market': [[]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'MELON', 2]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['NORTH'], ['WEST'], ['PASS']], 'market': [['BUY_SEED', 'MELON', 1], []]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['EAST'], ['FEED'], ['EAST'], ['PASS']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 1], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['EAST']], 'market': [[], [], [], [], [], []]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FEED'], ['PLANT', 'MELON'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PLANT', 'MELON'], ['PLANT', 'MELON'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WEST'], ['EAST'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PLANT', 'MELON'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WEST'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], []]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['CARE'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['CARE'], ['NORTH'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['NORTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER']], 'market': [[]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['EAST'], ['WEST'], ['WEST'], ['NORTH']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 2], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['WATER'], ['WATER']], 'market': [[]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 1], ['PASS'], ['WEST'], ['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 4], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PASS'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['PASS'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WEST'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['NORTH']], 'market': [[]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PASS'], ['HARVEST'], ['PASS'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['HARVEST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PLANT', 'STRAWBERRY']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['WATER']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WEST'], ['WEST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['CARE'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['PLANT', 'STRAWBERRY']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 2], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['FEED'], ['PASS'], ['HARVEST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WEST'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WEST'], ['PASS'], ['PASS'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WEST'], ['PLANT', 'STRAWBERRY']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['SOUTH']], 'market': [[]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': [[]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], []]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['PASS'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['PASS'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['PASS'], ['WEST']], 'market': [[]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['PASS'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['SOUTH'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PLACE', 'FERTILIZER', 2], 'hands': [['PLACE', 'FERTILIZER', 2], ['SOUTH'], ['PASS'], ['PASS'], ['WEST']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 4]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['PASS'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PASS'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['PASS'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['PASS'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['PASS'], ['EAST'], ['PASS'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PASS'], ['PLACE', 'FERTILIZER', 1], ['PASS'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PLACE', 'FERTILIZER', 2], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['PASS'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 4]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 1], ['PICKUP', 'WHEAT', 1], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['NORTH'], ['FEED'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['EAST'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['DROP'], ['WATER'], ['EAST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['CARE'], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['NORTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 1]], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'COW', 1], ['COLLECT_FERTILIZER'], ['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['EAST'], ['NORTH'], ['WATER'], ['PICKUP', 'COW', 1]], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['EAST'], ['PASS'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['FEED'], 'hands': [['BUILD_PASTURE'], ['SOUTH'], ['BUILD_COOP'], ['PICKUP', 'GOOSE', 1], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PLACE', 'COW', 1], ['PLACE', 'FERTILIZER', 1], ['DIG'], ['EAST'], ['WATER'], ['EAST'], ['NORTH'], ['PASS']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'GOOSE', 1], ['PICKUP', 'GOOSE', 1], ['PICKUP', 'GOOSE', 1], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['PICKUP', 'GOOSE', 1]], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['PICKUP', 'GOOSE', 1], ['PICKUP', 'COW', 1], ['BUILD_COOP'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['WEST'], ['PICKUP', 'COW', 1]], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['EAST'], ['NORTH'], ['PLACE', 'GOOSE', 1], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['PICKUP', 'GOOSE', 1]], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['BUILD_COOP'], ['EAST'], ['BUILD_PASTURE'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['EAST']], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'GOOSE', 1], ['EAST'], ['PLACE', 'COW', 1], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['BUILD_COOP'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['EAST'], ['NORTH']], 'market': [[], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['PLACE', 'GOOSE', 1], ['PICKUP', 'COW', 1], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH']], 'market': [[]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'STRAWBERRY'], ['EAST'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['BUILD_COOP']], 'market': [[]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['EAST'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['EAST'], ['PLACE', 'GOOSE', 1]], 'market': [[]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['NORTH'], ['BUILD_PASTURE'], ['NORTH'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['NORTH']], 'market': [[]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'STRAWBERRY'], ['SOUTH'], ['PLACE', 'COW', 1], ['PASS'], ['WEST'], ['WATER'], ['EAST'], ['NORTH']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['NORTH'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY']], 'market': []}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [[]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['WEST'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['EAST'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 4]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['PLACE', 'FERTILIZER', 2], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['PASS'], ['EAST'], ['WATER'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['FEED'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['FEED'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['EAST'], ['CARE'], ['FEED'], ['PICKUP', 'GOOSE', 1], ['CARE'], ['WATER'], ['PICKUP', 'GOOSE', 1], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['EAST'], ['NORTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['FEED'], ['FEED'], ['EAST'], ['FEED'], ['WATER'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['CARE'], ['CARE'], ['EAST'], ['CARE'], ['EAST'], ['EAST'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER'], ['FEED'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['BUILD_COOP'], ['EAST'], ['NORTH'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PLANT', 'WHEAT'], ['CARE'], ['CARE'], ['PLACE', 'GOOSE', 1], ['EAST'], ['WATER'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['EAST'], ['EAST'], ['WEST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['EAST'], ['SOUTH'], ['PASS'], ['WATER'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WATER'], ['PASS'], ['PASS'], ['NORTH'], ['WEST'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['CARE'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 6], 'hands': [['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 13]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['FEED'], ['SOUTH'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['SOUTH'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['DROP'], ['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['DROP'], ['CARE'], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['EAST'], ['EAST'], ['WEST'], ['FEED'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 2], 'hands': [['WATER'], ['FEED'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['WATER'], ['PASS'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['WEST'], ['PASS'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PASS'], ['FEED'], ['PASS'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PASS'], ['CARE'], ['PASS'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['EAST'], ['PASS'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['EAST'], ['PASS'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['WATER'], ['PASS'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['SOUTH'], ['PASS'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PASS'], ['SOUTH'], ['PASS'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['PASS'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'COW', 1], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['NORTH'], ['PICKUP', 'COW', 1]], 'market': [['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['PLACE', 'COW', 1], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': []}, {'farmer': ['PLACE', 'WOOL', 4], 'hands': [['EAST'], ['PICKUP', 'COW', 1], ['WEST'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['CARE'], ['NORTH']], 'market': [['SELL', 'WOOL', 4], ['BUY_LAND']]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['DROP'], ['SOUTH'], ['FEED'], ['FEED'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['FEED'], ['WEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['CARE'], ['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WEST'], ['FEED'], ['PLACE', 'FERTILIZER', 1], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 2], ['BUILD_PASTURE'], ['FEED'], ['NORTH'], ['NORTH'], ['DROP'], ['WATER'], ['CARE'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['PLACE', 'COW', 1], ['CARE'], ['FEED'], ['WATER'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'COW', 1], ['PLANT', 'WHEAT'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER'], ['FEED'], ['FEED'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['PLACE', 'FERTILIZER', 1], ['SOUTH'], ['CARE'], ['NORTH'], ['WATER']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['BUILD_PASTURE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['FEED'], ['WATER'], ['PICKUP', 'GOOSE', 1], ['PLANT', 'TOMATO'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PLACE', 'COW', 1], ['PLANT', 'WHEAT'], ['WATER'], ['CARE'], ['WEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PICKUP', 'GOOSE', 1], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 2], 'hands': [['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['BUILD_COOP'], ['PLANT', 'TOMATO'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'GOOSE', 1], 'hands': [['WEST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WATER'], ['SOUTH'], ['PLACE', 'GOOSE', 1], ['WATER'], ['EAST'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['SOUTH'], 'hands': [['BUILD_COOP'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['PLACE', 'FERTILIZER', 2], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PLACE', 'GOOSE', 1], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['SOUTH'], ['PLANT', 'TOMATO'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['BUILD_COOP'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['SOUTH'], ['PLANT', 'TOMATO'], ['WEST'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 8]]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['WEST'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], [], [], [], [], []]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['EAST'], ['WEST'], ['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH']], 'market': [[]]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['WATER'], ['CARE'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['PLACE', 'FERTILIZER', 1]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['CARE'], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['PLACE', 'FERTILIZER', 1]], 'market': [[]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['SOUTH'], ['EAST'], ['SOUTH'], ['CARE'], ['EAST'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['DROP'], ['WATER'], ['DROP'], ['WATER'], ['NORTH'], ['SOUTH'], ['FEED']], 'market': [['SELL', 'MELON', 12], ['BUY_PRODUCT', 'WHEAT', 35]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WEST'], ['CARE'], ['EAST'], ['WEST'], ['PICKUP', 'WHEAT', 5], ['WEST'], ['CARE'], ['HARVEST'], ['WATER'], ['SOUTH'], ['CARE']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_PRODUCT', 'WHEAT', 32]]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['PICKUP', 'GOOSE', 1], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 6], 'hands': [['FEED'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['DROP'], ['NORTH'], ['FEED'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WATER'], ['EAST'], ['PICKUP', 'WHEAT', 5], ['PLANT', 'WHEAT'], ['CARE'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['EAST'], ['DROP'], ['FEED']], 'market': [[], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['SOUTH'], ['WATER'], ['PICKUP', 'WHEAT', 5], ['CARE']], 'market': [[]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['FEED'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['NORTH']], 'market': [[]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['FEED'], ['WATER'], ['CARE'], ['WATER'], ['BUILD_COOP'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [[], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['SOUTH'], ['HARVEST'], ['CARE'], ['NORTH'], ['EAST'], ['WEST'], ['PLACE', 'GOOSE', 1], ['PLACE', 'MELON', 6], ['NORTH'], ['FEED'], ['WEST']], 'market': [[]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PLANT', 'TOMATO'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['PICKUP', 'WHEAT', 5], ['WATER'], ['CARE'], ['WATER']], 'market': [[]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': [[]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['WATER']], 'market': [[]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['WEST'], ['WATER'], ['NORTH']], 'market': [[]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['NORTH'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [[]]}, {'farmer': ['PICKUP', 'WHEAT', 6], 'hands': [], 'market': [[], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 6], ['PICKUP', 'WHEAT', 6], ['PICKUP', 'WHEAT', 6], ['NORTH'], ['PICKUP', 'WHEAT', 6], ['WEST'], ['NORTH'], ['NORTH']], 'market': [[], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['PICKUP', 'WHEAT', 4]], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['WEST'], ['WEST'], ['SOUTH']], 'market': [[]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['HARVEST'], ['CARE'], ['WEST'], ['EAST'], ['NORTH'], ['FEED'], ['WEST'], ['FEED']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['WATER'], ['CARE']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [[]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FERTILIZE'], ['HARVEST'], ['DROP'], ['FEED'], ['WEST'], ['EAST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['SOUTH']], 'market': [[], ['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WATER'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['FEED'], ['EAST'], ['FEED']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['CARE'], ['EAST'], ['CARE']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FERTILIZE'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['DROP'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6], ['SELL', 'FERTILIZER', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['DROP'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'MELON', 12], ['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['FEED'], ['WEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['WATER'], ['CARE'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['FEED'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'TOMATO'], ['PLANT', 'WHEAT'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'MELON', 6], ['SELL', 'FERTILIZER', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 5], ['PICKUP', 'WHEAT', 5], ['PICKUP', 'WHEAT', 5], ['HARVEST'], ['PICKUP', 'WHEAT', 5], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['CARE'], ['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['CARE'], ['WEST'], ['EAST'], ['FEED'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['NORTH'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['CARE'], ['NORTH'], ['DROP']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['FEED'], ['WEST'], ['NORTH'], ['CARE'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['WATER'], ['CARE'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['NORTH'], ['SOUTH'], ['CARE'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['CARE'], ['HARVEST'], ['EAST'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['HARVEST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['PLANT', 'TOMATO'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['PLANT', 'TOMATO'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'TOMATO'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['PASS'], ['WEST'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'EGG', 12], ['SELL', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 5], ['PICKUP', 'WHEAT', 4], ['WEST'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['NORTH'], ['FEED'], ['NORTH'], ['WEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['EAST'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['CARE'], ['HARVEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['CARE'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['CARE'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['NORTH'], ['FEED'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['CARE'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['FEED'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['CARE'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['EAST'], ['CARE'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['PLANT', 'TOMATO'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['PLANT', 'TOMATO'], ['WATER']], 'market': [['SELL', 'MILK', 9], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['FERTILIZE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['EAST'], ['EAST'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'EGG', 10], ['SELL', 'WHEAT', 10]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'EGG', 2]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['PLACE', 'MILK', 6], ['FEED'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['EAST'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['SOUTH'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['PLACE', 'MILK', 6], ['HARVEST'], ['EAST'], ['WEST'], ['FEED'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WEST'], ['HARVEST'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['CARE'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['FEED'], ['SOUTH'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['WATER'], ['CARE'], ['WATER'], ['FERTILIZE'], ['WEST'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['EAST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['NORTH'], ['CARE'], ['WATER']], 'market': [['SELL', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['SOUTH'], ['CARE'], ['HARVEST'], ['FEED'], ['WATER'], ['EAST'], ['CARE'], ['NORTH'], ['HARVEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'TOMATO'], ['CARE'], ['NORTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['HARVEST'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['PLANT', 'TOMATO'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 9], ['SELL', 'STRAWBERRY', 3], ['SELL', 'WOOL', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 11], ['SELL', 'EGG', 12], ['SELL', 'WHEAT', 4]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['PICKUP', 'WHEAT', 5], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 5], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['EAST'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['CARE'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['CARE'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['EAST'], ['FEED'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['FEED'], ['CARE'], ['FEED'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['FEED'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['HARVEST'], ['WATER'], ['FEED'], ['PLANT', 'TOMATO'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['PLANT', 'TOMATO'], ['WATER'], ['SOUTH'], ['HARVEST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['WEST'], ['CARE'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['HARVEST']], 'market': [['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['EAST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 9]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['FERTILIZE'], ['PLANT', 'TOMATO'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['WATER'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 16]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['FEED'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['PLACE', 'MILK', 3], ['FEED'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['EAST'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['FEED'], ['EAST'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['EAST'], ['FERTILIZE'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['FEED'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['FEED'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['HARVEST'], ['CARE'], ['WEST'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['HARVEST'], ['EAST'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['PLANT', 'TOMATO'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['CARE'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['FEED'], ['WEST'], ['PLANT', 'TOMATO']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['COLLECT_FERTILIZER'], ['DROP'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['CARE'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['DROP'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['CARE'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['FEED'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['EAST'], ['WEST'], ['SOUTH'], ['EAST'], ['FEED'], ['WATER']], 'market': [['SELL', 'EGG', 16], ['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['CARE'], ['EAST']], 'market': [['SELL', 'EGG', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 11], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['WEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 6], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['PLACE', 'MILK', 6], ['NORTH'], ['FEED'], ['NORTH'], ['HARVEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['FEED'], ['EAST'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['NORTH'], ['CARE'], ['PLACE', 'MILK', 6], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['CARE'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['FEED'], ['EAST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['FEED'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WATER'], ['CARE'], ['CARE'], ['WATER'], ['WEST'], ['EAST'], ['FEED'], ['WATER'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FEED'], ['WATER'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['FEED'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['CARE'], ['PLANT', 'WHEAT'], ['CARE'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['WATER'], ['CARE'], ['WATER'], ['WEST'], ['CARE'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'MILK', 9], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['PLANT', 'TOMATO'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'EGG', 16], ['SELL', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'EGG', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['NORTH'], ['WEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 5], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLACE', 'MILK', 3], ['FEED'], ['NORTH'], ['PLACE', 'MILK', 3], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['WEST'], ['EAST'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['NORTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['NORTH'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['CARE'], ['HARVEST'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['DIG'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['PLANT', 'TOMATO'], ['WATER'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['HARVEST'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['SOUTH'], ['FEED'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['DIG'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['WEST'], ['DROP'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['PLANT', 'TOMATO'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['FERTILIZE'], ['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['DIG'], ['SOUTH'], ['DROP'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['DROP'], ['PLANT', 'TOMATO'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['EAST'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['NORTH'], ['CARE'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['FERTILIZE'], ['NORTH'], ['DIG'], ['NORTH'], ['WATER'], ['WEST'], ['DIG'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'TOMATO', 8], ['SELL', 'EGG', 12], ['SELL', 'WHEAT', 13]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['PASS'], ['CARE'], ['SOUTH'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['PLACE', 'MILK', 3], ['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['NORTH'], ['CARE'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['CARE'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['FEED'], ['HARVEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['FERTILIZE'], ['CARE'], ['FEED'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['CARE'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['CARE'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['FEED'], ['EAST'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FERTILIZE'], ['EAST'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['CARE'], ['FERTILIZE'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['CARE'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['DIG'], ['EAST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['HARVEST'], ['FEED'], ['WEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['EAST'], ['CARE'], ['HARVEST'], ['NORTH'], ['DIG'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['DIG'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['DIG'], ['WATER'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['EAST'], ['HARVEST'], ['PLANT', 'TOMATO'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'TOMATO', 10], ['SELL', 'EGG', 10], ['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['DIG'], ['EAST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 11], ['SELL', 'FERTILIZER', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['NORTH'], ['WEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 6], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLACE', 'MILK', 3], ['FEED'], ['NORTH'], ['PLACE', 'MILK', 2], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['EAST'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['FERTILIZE'], ['EAST'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['WEST'], ['SOUTH'], ['WEST'], ['EAST'], ['NORTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 1]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['FEED'], ['WEST'], ['HARVEST'], ['CARE']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['EAST'], ['NORTH'], ['SOUTH'], ['DIG'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['SOUTH'], ['FEED'], ['WATER'], ['SOUTH'], ['PLANT', 'CARROT'], ['WEST'], ['CARE'], ['WEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['SOUTH'], ['PLANT', 'CARROT'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['CARE'], ['WATER'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['DROP'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['WATER'], ['EAST'], ['DIG'], ['WEST'], ['FERTILIZE'], ['DIG'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['PLANT', 'CARROT'], ['DROP'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['DIG'], 'hands': [['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['EAST'], ['HARVEST'], ['EAST'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 2]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['EAST'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['DIG'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['EAST']], 'market': [['SELL', 'TOMATO', 10], ['SELL', 'EGG', 10], ['SELL', 'WHEAT', 4]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['EAST'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['WEST'], ['WATER']], 'market': [['SELL', 'TOMATO', 2], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 6]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['CARE'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['CARE'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['FERTILIZE'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WATER'], ['CARE'], ['FEED'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['CARE'], ['NORTH'], ['HARVEST'], ['WATER'], ['FEED'], ['WATER'], ['CARE'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['SOUTH'], ['FEED'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['HARVEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['PLANT', 'CARROT'], ['NORTH'], ['WEST'], ['WEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['EAST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['HARVEST'], ['EAST'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['WATER'], ['DROP']], 'market': [['SELL', 'TOMATO', 10], ['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['DIG'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'TOMATO', 8], ['SELL', 'EGG', 10], ['SELL', 'WHEAT', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'TOMATO', 10], ['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER'], ['EAST'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['NORTH'], ['SOUTH'], ['PLANT', 'CARROT'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['DIG'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'MILK', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['EAST'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['CARE'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DIG'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['FERTILIZE'], ['EAST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['EAST'], ['DIG'], ['SOUTH']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['DROP'], ['DIG'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['DIG'], ['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WEST'], ['DIG'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'WOOL', 1], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WATER'], ['DIG'], ['FERTILIZE'], ['WEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['DIG'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['DIG'], ['EAST'], ['EAST'], ['WATER'], ['DIG'], ['PLANT', 'CARROT'], ['WATER'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['SELL', 'TOMATO', 4], ['SELL', 'EGG', 10], ['SELL', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['WATER'], ['SOUTH'], ['PASS'], ['WATER'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'EGG', 6], ['SELL', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'TOMATO', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 6]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['CARE'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['CARE'], ['EAST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FERTILIZE'], ['CARE'], ['NORTH'], ['EAST'], ['WEST'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['CARE'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WATER'], ['EAST'], ['FEED'], ['WATER'], ['WATER'], ['DIG'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WOOL', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['CARE'], ['HARVEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['WEST'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['WATER'], ['CARE'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['PLANT', 'CARROT'], ['NORTH'], ['HARVEST'], ['FEED'], ['WEST'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['NORTH'], ['PLANT', 'CARROT']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WATER'], ['WATER'], ['EAST'], ['CARE'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['DIG'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['DIG'], ['HARVEST'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['DIG'], ['SOUTH'], ['DIG'], ['SOUTH'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WOOL', 1], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['FERTILIZE'], ['WATER'], ['DROP'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['HARVEST'], ['WATER'], ['PLACE', 'MILK', 2], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['EAST'], ['WEST'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['NORTH'], ['PLANT', 'CARROT'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['SOUTH'], ['PLANT', 'CARROT'], ['FEED'], ['FERTILIZE'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'TOMATO', 8], ['SELL', 'CARROT', 9], ['SELL', 'EGG', 10], ['SELL', 'WHEAT', 3]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'TOMATO', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['NORTH'], ['PLACE', 'MILK', 2], ['HARVEST'], ['WEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['WEST'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['NORTH'], ['CARE']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['CARE'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['FEED'], ['WATER'], ['WATER'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WOOL', 1], ['SELL', 'MILK', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['EAST'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['DIG'], ['EAST'], ['EAST'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['WATER'], ['CARE'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'CARROT', 13], ['SELL', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['PLANT', 'CARROT'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WOOL', 1]]}, {'farmer': ['NORTH'], 'hands': [['DIG'], ['WEST'], ['NORTH'], ['CARE'], ['FERTILIZE'], ['EAST'], ['DIG'], ['WATER'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['FEED'], ['PLANT', 'CARROT'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['CARE'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['EAST'], ['WEST'], ['WATER'], ['SOUTH'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WOOL', 1], ['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['DROP'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['SOUTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['PLANT', 'CARROT'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 6]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['DROP'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['WATER'], ['PLANT', 'CARROT']], 'market': [['SELL', 'TOMATO', 8], ['SELL', 'EGG', 10], ['SELL', 'CARROT', 2], ['SELL', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'EGG', 8], ['SELL', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['FEED'], ['HARVEST'], ['WEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FERTILIZE'], ['EAST'], ['CARE'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WATER'], ['FEED'], ['HARVEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['NORTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WATER'], ['EAST'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['FEED'], ['WATER'], ['NORTH'], ['FEED']], 'market': [['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['CARE']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['PLANT', 'CARROT'], ['HARVEST'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['CARE'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['DIG'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['FERTILIZE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['PLANT', 'CARROT'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WATER'], ['NORTH'], ['DIG'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['HARVEST'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['WEST'], ['DIG'], ['WATER'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['PLANT', 'CARROT'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['FEED'], ['WATER'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['CARE'], ['HARVEST'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['PLANT', 'CARROT'], ['SOUTH'], ['HARVEST'], ['WEST'], ['PLANT', 'CARROT'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'TOMATO', 10], ['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['EAST'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['CARE'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'MILK', 5]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'TOMATO', 8], ['SELL', 'CARROT', 9], ['SELL', 'EGG', 10], ['SELL', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS'], ['NORTH'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['NORTH']], 'market': [['SELL', 'EGG', 8], ['SELL', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['WEST']], 'market': [['SELL', 'WOOL', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'MILK', 4], ['FEED'], ['NORTH'], ['PLACE', 'MILK', 2], ['HARVEST'], ['SOUTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['EAST'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['FEED']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['DIG'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['HARVEST'], ['CARE']], 'market': [['SELL', 'CARROT', 13], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['PLANT', 'CARROT'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['WEST']], 'market': [['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'WOOL', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'CARROT'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'CARROT']], 'market': [['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['EAST'], ['HARVEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['FEED'], ['FEED'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['FEED'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['HARVEST'], ['CARE'], ['CARE'], ['SOUTH'], ['WEST'], ['HARVEST'], ['CARE'], ['WATER'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['DIG'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['DIG']], 'market': [['SELL', 'WHEAT', 4]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['EAST'], ['DROP'], ['HARVEST'], ['PLANT', 'CARROT'], ['HARVEST'], ['WATER'], ['HARVEST'], ['PLANT', 'CARROT']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['DROP'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 6], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WATER'], ['DROP'], ['PASS'], ['EAST'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'TOMATO', 13], ['SELL', 'EGG', 10], ['SELL', 'WHEAT', 8], ['SELL', 'CARROT', 5]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['SOUTH'], ['EAST'], ['PASS'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'TOMATO', 5], ['SELL', 'EGG', 8], ['SELL', 'WHEAT', 3]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 3]], 'market': [['SELL', 'CARROT', 7], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FEED'], ['PLACE', 'MILK', 4], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['FEED'], ['SOUTH'], ['EAST'], ['HARVEST'], ['EAST'], ['PLANT', 'CARROT'], ['WEST'], ['NORTH'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['EAST'], ['SOUTH'], ['FEED'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['CARE'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['EAST'], ['FERTILIZE'], ['EAST'], ['WATER'], ['HARVEST'], ['DROP'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'CARROT', 9]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'TOMATO', 10], ['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['HARVEST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'CARROT', 13], ['SELL', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['DIG'], ['WATER'], ['SOUTH'], ['EAST'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['SOUTH'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 5], ['SELL', 'WOOL', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['SOUTH']], 'market': [['SELL', 'TOMATO', 6], ['SELL', 'EGG', 10], ['SELL', 'WHEAT', 1], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['SOUTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 2], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['HARVEST'], ['EAST'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FERTILIZE'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['EAST'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'MILK', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['EAST'], ['WEST'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'CARROT', 16], ['SELL', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['WEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'TOMATO', 10]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['DROP'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'CARROT', 13], ['SELL', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST'], ['EAST'], ['WEST'], ['DROP'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'CARROT', 9], ['SELL', 'WHEAT', 1], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'TOMATO', 6], ['SELL', 'WHEAT', 1], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['DROP'], ['HARVEST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'CARROT', 5], ['SELL', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['EAST'], ['NORTH'], ['WEST'], ['EAST'], ['HARVEST'], ['NORTH'], ['DROP'], ['WEST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 6], ['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['NORTH'], ['WATER'], ['SOUTH'], ['DROP'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'EGG', 16], ['SELL', 'CARROT', 2], ['SELL', 'WHEAT', 1], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['DROP'], ['SOUTH'], ['SOUTH'], ['PASS'], ['NORTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['DROP'], ['WEST']], 'market': [['SELL', 'CARROT', 13], ['SELL', 'EGG', 4], ['SELL', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'CARROT', 16], ['SELL', 'MILK', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'CARROT', 13], ['SELL', 'WHEAT', 1], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['EAST'], ['WATER'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['EAST'], ['WEST'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'TOMATO', 8], ['SELL', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'CARROT', 7], ['SELL', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WEST'], ['DROP'], ['WEST'], ['DROP'], ['SOUTH'], ['DROP'], ['EAST'], ['EAST'], ['WEST']], 'market': [['SELL', 'CARROT', 13], ['SELL', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['DROP'], ['DROP'], ['NORTH'], ['DROP'], ['NORTH'], ['WEST'], ['NORTH'], ['DROP'], ['DROP'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['DROP'], ['NORTH'], ['NORTH'], ['NORTH'], ['DROP']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'TOMATO', 2], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'CARROT', 7], ['SELL', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['WEST'], ['WEST'], ['WEST'], ['WEST'], ['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'CARROT', 13], ['SELL', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['WEST'], ['HARVEST'], ['WEST'], ['WEST'], ['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'TOMATO', 6], ['SELL', 'WHEAT', 1], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST'], ['WEST'], ['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'EGG', 27], ['SELL', 'WHEAT', 1]]}]
_PROXY=make_agent({0:_DEMO})
def demonstrated_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
demonstrated_proxy.telemetry=_PROXY.chassis.diagnostics
agent=demonstrated_proxy
