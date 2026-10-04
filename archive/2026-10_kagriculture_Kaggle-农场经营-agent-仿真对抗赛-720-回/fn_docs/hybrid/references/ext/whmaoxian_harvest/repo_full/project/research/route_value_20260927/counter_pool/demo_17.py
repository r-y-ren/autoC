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

_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['HIRE']]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1]], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['PLACE', 'SHEEP', 1], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP', 1], ['CARE'], ['WEST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['BUILD_PASTURE'], ['BUILD_PASTURE'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['PLACE', 'COW', 1], ['PLACE', 'SHEEP', 1], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'MELON'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['PASS'], ['PLANT', 'WHEAT']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['SOUTH'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], [], []]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['SOUTH'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['DROP'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 2], ['WEST'], ['CARE'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['CARE'], ['NORTH'], ['DROP']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['CARE'], ['FEED'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['WEST'], ['WEST'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['DROP']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['NORTH']], 'market': [['SELL', 'WHEAT', 3]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['PASS'], ['SOUTH'], ['WATER'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['PASS'], ['SOUTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['PASS'], ['CARE'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['PASS'], ['FEED'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['SOUTH'], ['PASS'], ['EAST'], ['HARVEST'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PASS'], ['FEED'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['PASS'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PLANT', 'WHEAT'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['PASS'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['EAST'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['BUILD_PASTURE'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['WEST'], ['NORTH'], ['DROP'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WATER'], ['PASS'], ['FEED'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WATER'], ['WEST'], ['PASS'], ['CARE'], ['FEED']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['PASS'], ['SOUTH'], ['FEED']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['HARVEST'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['WEST'], ['PASS']], 'market': [[]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['FEED'], ['PASS']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['PICKUP', 'COW', 1], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['CARE'], ['SOUTH'], ['WEST'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['BUILD_PASTURE'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['PLACE', 'COW', 1], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['NORTH'], ['SOUTH'], ['WEST'], ['PASS'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['DROP'], ['WATER'], ['PICKUP', 'COW', 1], ['CARE']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['CARE'], ['FEED'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST'], ['FEED']], 'market': [[]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['EAST'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['WEST'], ['PASS'], ['FEED'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WEST'], ['SOUTH'], ['PASS'], ['CARE'], ['BUILD_PASTURE'], ['FEED']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PLACE', 'COW', 1], ['CARE']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['CARE'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['EAST'], ['FEED'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['CARE'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['NORTH'], ['DROP'], ['EAST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['DROP'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['CARE'], ['PASS'], ['FEED'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FEED'], ['PASS'], ['CARE'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['PASS'], ['WEST'], ['FEED'], ['DROP']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'COW', 1], ['WEST'], ['PICKUP', 'WHEAT', 2], ['FEED'], ['CARE'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['CARE'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['CARE'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['FEED'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['NORTH'], ['FEED'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'COW', 1], ['NORTH'], ['CARE'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['DROP'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_PRODUCT', 'WHEAT', 3], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['BUILD_PASTURE'], ['SOUTH'], ['WEST'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['PICKUP', 'GOOSE', 1], 'hands': [['PLACE', 'COW', 1], ['SOUTH'], ['FEED'], ['NORTH'], ['FEED'], ['SOUTH'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['DROP'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'MELON'], ['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['SOUTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['BUILD_COOP'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['EAST'], ['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['DROP'], ['SOUTH'], ['SOUTH'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], [], []]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['DROP'], ['WATER'], ['NORTH'], ['PICKUP', 'GOOSE', 1], ['WATER'], ['PLANT', 'STRAWBERRY'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'MELON'], 'hands': [['WATER'], ['BUILD_COOP'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['FEED'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1], []]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PLACE', 'GOOSE', 1], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['NORTH'], ['EAST'], ['SOUTH'], ['EAST']], 'market': [[]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['SOUTH']], 'market': [[]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['DROP'], ['WATER'], ['DROP']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['BUILD_COOP'], ['PASS'], ['NORTH'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1], []]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'STRAWBERRY'], ['WATER'], ['FEED'], ['WATER'], ['EAST'], ['PLACE', 'GOOSE', 1], ['PASS'], ['NORTH'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['CARE'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['PASS'], ['NORTH'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PASS'], ['WATER'], ['CARE'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['FEED'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], [], []]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [[], []]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['DROP'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3], []]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['DROP'], ['FEED'], ['NORTH'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2], []]}, {'farmer': ['DROP'], 'hands': [['PLACE', 'FERTILIZER', 1], ['EAST'], ['SOUTH'], ['CARE'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['FEED'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['PLACE', 'FERTILIZER', 1], ['DROP'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['FEED'], ['NORTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 1]], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['NORTH'], ['WEST'], ['WEST'], ['FEED'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['CARE'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['NORTH'], ['CARE'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['FEED'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLACE', 'FERTILIZER', 2], ['CARE'], ['FEED'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PASS'], ['COLLECT_FERTILIZER'], ['CARE'], ['PASS'], ['SOUTH'], ['EAST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['PASS'], ['EAST'], ['PASS'], ['DROP'], ['EAST'], ['EAST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['FEED'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['PASS'], ['CARE'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PLACE', 'FERTILIZER', 1], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['SOUTH'], ['EAST'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST']], 'market': [[], []]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['DROP'], ['WATER'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 6], ['BUY_LAND'], []]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['SOUTH'], ['PICKUP', 'GOOSE', 1], ['WATER'], ['SOUTH'], ['DROP'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['WEST'], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['EAST'], ['PICKUP', 'GOOSE', 1], ['BUILD_COOP'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['EAST'], ['SOUTH'], ['PLACE', 'GOOSE', 1], ['NORTH'], ['WATER'], ['SOUTH'], ['DROP'], ['WATER'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['DROP'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['BUILD_COOP'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['NORTH'], ['BUILD_COOP'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['PLACE', 'GOOSE', 1], ['WATER'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['NORTH'], ['PLACE', 'GOOSE', 1], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['FEED'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['CARE'], ['FEED'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['WEST'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['PASS'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['PASS'], ['SOUTH'], ['WATER'], ['NORTH'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PASS'], ['SOUTH'], ['WEST'], ['SOUTH'], ['PASS'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['CARE'], ['CARE'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['NORTH'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['BUY_PRODUCT', 'WHEAT', 6], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['FEED'], ['FEED'], ['WEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['NORTH'], ['CARE'], ['SOUTH'], ['EAST'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['CARE'], ['FEED'], ['CARE'], ['DROP'], ['EAST'], ['PICKUP', 'GOOSE', 1], ['NORTH'], ['WEST'], ['FEED']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'GOOSE', 1], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['BUILD_COOP'], ['WATER'], ['WATER'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['PLACE', 'GOOSE', 1], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['CARE'], ['NORTH'], ['SOUTH'], ['FEED'], ['WATER'], ['FEED'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['HARVEST'], ['CARE'], ['EAST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_COOP'], ['FEED'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['NORTH'], ['DROP']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'GOOSE', 1], ['CARE'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['SOUTH'], ['FEED'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['EAST'], ['EAST'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['FEED'], ['WATER'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['CARE'], ['HARVEST'], ['SOUTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['WATER'], ['EAST'], ['WATER'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['EAST'], ['CARE'], ['WEST'], ['CARE'], ['SOUTH'], ['WEST'], ['WATER'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST'], ['WATER'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['CARE'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['DROP'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['FEED'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['NORTH'], ['SOUTH'], ['CARE'], ['HARVEST'], ['EAST'], ['WEST'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'MELON', 6], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['EAST'], ['HARVEST'], ['CARE'], ['WEST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['FEED'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['WATER'], ['EAST'], ['CARE'], ['EAST'], ['FEED'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['WATER'], ['SOUTH'], ['CARE'], ['DROP'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['DROP'], ['CARE'], ['EAST']], 'market': [['SELL', 'MELON', 12], ['SELL', 'MELON', 6]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['DROP']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['DROP'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['FEED'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['DROP'], ['WEST'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['CARE'], ['PICKUP', 'WHEAT', 2], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'MILK', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['FEED'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['CARE'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WATER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['SOUTH'], ['WEST'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['WATER'], ['CARE'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['WEST'], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['SELL', 'FERTILIZER', 4], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['WEST'], ['NORTH'], ['FEED'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['CARE'], ['WEST'], ['CARE'], ['WEST'], ['WATER'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['FEED'], ['CARE'], ['WEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['EAST'], ['EAST'], ['WEST'], ['WATER'], ['SOUTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['FEED'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['DROP'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6], ['SELL', 'MILK', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['DROP'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['FEED']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['EAST'], ['WEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['EAST'], ['EAST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FERTILIZE'], ['EAST'], ['WATER'], ['NORTH'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['FEED'], ['CARE'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['EAST'], ['SOUTH'], ['PASS'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PASS'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'WHEAT', 4], ['CARE'], ['CARE'], ['WEST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['CARE'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['DROP'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['EAST'], ['CARE'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['PLANT', 'STRAWBERRY'], ['DROP'], ['SOUTH']], 'market': [['SELL', 'MILK', 9], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['FEED'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['FEED'], ['HARVEST'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['CARE'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['EAST'], ['WATER'], ['EAST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['EAST'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 5]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['PASS'], ['HARVEST']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 6], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 24], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['EAST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['FEED'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['FEED']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FEED'], ['FEED'], ['FEED'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['FERTILIZE'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['WEST'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['HARVEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['HARVEST'], ['FERTILIZE'], ['FEED'], ['WATER'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['CARE'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['CARE'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['PASS'], ['COLLECT_FERTILIZER'], ['PASS'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'EGG', 5]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 8], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['FEED'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['WEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FEED'], ['HARVEST'], ['WEST'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['CARE'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['CARE'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['FEED']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['FEED'], ['WEST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['EAST'], ['WATER'], ['FEED'], ['WATER'], ['WATER'], ['FERTILIZE'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['WATER'], ['HARVEST'], ['CARE'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['SOUTH'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WEST'], ['PASS'], ['SOUTH'], ['WATER'], ['WATER'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'WHEAT', 6], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'FERTILIZER', 3], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['SOUTH'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'MILK', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['FEED'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['WATER'], ['EAST'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['HARVEST'], ['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['FEED'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['CARE'], ['SOUTH'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['HARVEST'], ['CARE'], ['FEED'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['SELL', 'MILK', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['CARE'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['EAST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['NORTH'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['DROP']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 8]]}, {'farmer': ['PASS'], 'hands': [['HARVEST'], ['PASS'], ['SOUTH'], ['PASS'], ['SOUTH'], ['PASS'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['PASS']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['FEED'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['FEED'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['CARE'], ['NORTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['WEST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WEST'], ['EAST'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['DROP'], ['WATER'], ['WEST'], ['EAST'], ['WEST'], ['HARVEST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['CARE'], ['EAST'], ['WEST'], ['DROP'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['SOUTH'], ['DROP'], ['HARVEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['FERTILIZE'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['EAST'], ['WATER'], ['NORTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['HARVEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['FERTILIZE'], ['EAST'], ['WEST'], ['CARE'], ['WEST'], ['HARVEST'], ['DROP']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['DROP'], ['EAST'], ['WEST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['FEED'], ['DROP'], ['FEED'], ['DROP']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['NORTH'], ['CARE'], ['WEST'], ['CARE'], ['WEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['EAST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['EAST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['HARVEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['EAST'], ['PASS'], ['PASS'], ['HARVEST'], ['DROP'], ['HARVEST'], ['CARE'], ['CARE'], ['WATER']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['NORTH'], ['HARVEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WEST'], ['CARE'], ['SOUTH'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['FEED'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['FEED'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['WEST'], ['CARE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['CARE'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WEST'], ['FEED'], ['EAST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['CARE'], ['FEED'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['CARE'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['FEED'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['HARVEST'], ['FEED'], ['CARE'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['DROP'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['DROP'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER'], ['EAST']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['PASS'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['CARE'], ['PASS'], ['PASS'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['FEED'], ['HARVEST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['FEED'], ['FEED'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['FEED'], ['CARE'], ['CARE'], ['WEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['FEED'], ['DROP'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['CARE'], ['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'WHEAT', 2], ['SOUTH'], ['WATER'], ['WEST'], ['DROP'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['DROP']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['HARVEST'], ['FEED'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['DIG'], 'hands': [['FERTILIZE'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE'], ['PLANT', 'WHEAT'], ['HARVEST'], ['DIG'], ['SOUTH'], ['DROP'], ['FERTILIZE'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['DROP'], ['WEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['DROP'], ['DROP'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 8], ['SELL', 'EGG', 6]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['WATER'], ['EAST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['EAST'], ['SOUTH'], ['PASS'], ['PASS'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['WATER'], ['SOUTH'], ['EAST'], ['WEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['FEED'], ['WATER'], ['WEST'], ['EAST'], ['NORTH'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['FEED'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['CARE'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['DIG'], ['WEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['CARE'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['NORTH'], ['FEED'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['SOUTH'], ['EAST'], ['CARE'], ['CARE'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['DIG'], ['FERTILIZE'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FERTILIZE'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['PASS'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['PASS'], ['HARVEST'], ['SOUTH'], ['PASS'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['FEED'], ['NORTH'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['SOUTH'], ['EAST'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLANT', 'WHEAT'], ['CARE'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['FERTILIZE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WEST'], ['FEED'], ['FEED'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['FEED'], ['CARE'], ['CARE'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH'], ['HARVEST'], ['FEED'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED'], ['DROP'], ['WATER'], ['WEST'], ['CARE'], ['DROP'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['SOUTH'], ['WEST'], ['CARE'], ['EAST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['EAST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['DROP'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['FEED'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['FEED'], ['CARE'], ['HARVEST'], ['FEED'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['CARE'], ['EAST']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['FEED'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['EAST'], ['CARE'], ['WEST'], ['FEED'], ['FERTILIZE'], ['EAST'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['CARE'], ['SOUTH'], ['EAST'], ['FEED'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['CARE'], ['EAST']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['EAST'], ['DROP'], ['WEST'], ['PASS'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'WOOL', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['HARVEST'], ['WEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['FEED'], ['WEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['CARE'], ['CARE'], ['FEED'], ['EAST'], ['WEST'], ['SOUTH'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['CARE'], ['FEED'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['NORTH'], ['CARE'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['CARE'], ['FERTILIZE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['DIG'], ['WATER'], ['CARE'], ['HARVEST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['WEST'], ['FEED']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['EAST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['DIG'], ['WEST'], ['PASS'], ['EAST'], ['EAST'], ['WEST'], ['EAST'], ['EAST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['EAST'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['HARVEST'], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['HARVEST'], ['CARE'], ['NORTH'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['HARVEST'], ['HARVEST'], ['WATER'], ['EAST'], ['NORTH'], ['DIG'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['DIG'], ['WATER'], ['WATER'], ['FERTILIZE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['FEED'], ['NORTH'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['WATER'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['FEED'], ['HARVEST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['DIG'], ['WEST'], ['NORTH'], ['NORTH'], ['DIG'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['DIG'], ['HARVEST'], ['WATER'], ['NORTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['SOUTH'], ['WATER'], ['DIG'], ['DIG'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['FERTILIZE'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PLANT', 'CARROT'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['DIG'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['DIG']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER'], ['PLANT', 'CARROT'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['WATER'], ['WEST'], ['FERTILIZE'], ['EAST'], ['DIG'], ['WEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['DIG'], ['PLANT', 'CARROT'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'CARROT'], ['SOUTH'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER'], ['NORTH'], ['DIG'], ['DROP'], ['DIG'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['PASS'], ['HARVEST'], ['PASS'], ['PASS'], ['SOUTH'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['FEED'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['CARE']], 'market': [['SELL', 'WOOL', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['FEED'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['CARE'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['FEED'], ['DROP'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['CARE'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['DROP'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['NORTH'], ['PLANT', 'CARROT'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['DROP'], 'hands': [['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['WEST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['DROP'], ['PLANT', 'CARROT'], ['DIG'], ['SOUTH'], ['DROP'], ['EAST'], ['DROP']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['FEED'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'CARROT'], ['NORTH'], ['PLANT', 'CARROT'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['CARE'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 4], ['SELL', 'EGG', 3]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['NORTH'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['NORTH'], ['PASS'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 6], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'WOOL', 3], ['SELL', 'STRAWBERRY', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PLACE', 'MILK', 3], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['EAST'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['DIG'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['FEED'], ['EAST'], ['PLANT', 'CARROT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['PLANT', 'CARROT'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['DIG'], ['EAST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['PLANT', 'CARROT'], ['EAST'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['WATER'], ['DROP'], ['WATER'], ['WATER'], ['DIG'], ['PLANT', 'CARROT'], ['HARVEST'], ['SOUTH'], ['WEST'], ['PLANT', 'CARROT']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['FEED'], ['WATER'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FERTILIZE'], ['DROP'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['CARE'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['PLANT', 'CARROT'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['PLANT', 'CARROT'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['DIG'], ['PASS'], ['WATER'], ['WATER'], ['DIG'], ['WATER'], ['PASS'], ['PASS'], ['FERTILIZE'], ['PASS']], 'market': [['SELL', 'WHEAT', 3], ['SELL', 'EGG', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['FEED'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['PLANT', 'CARROT'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['PLANT', 'CARROT']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['WEST'], ['FEED'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['FEED'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['DIG'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['EAST'], ['PLANT', 'CARROT'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PLANT', 'CARROT'], ['SOUTH'], ['HARVEST'], ['PLANT', 'CARROT'], ['HARVEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['DIG'], ['NORTH'], ['WEST'], ['SOUTH'], ['FEED'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['EAST'], ['WATER'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['WEST'], ['WEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['DROP'], ['WEST'], ['DROP']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['EAST'], ['EAST'], ['NORTH'], ['CARE'], ['HARVEST']], 'market': [['SELL', 'CARROT', 10]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['SOUTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['FERTILIZE'], ['FEED'], ['EAST'], ['WEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['WATER'], ['DROP'], ['WATER'], ['WATER'], ['CARE'], ['FEED'], ['CARE'], ['CARE']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'WHEAT', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WOOL', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'MILK', 3], ['DROP'], ['WEST'], ['PLACE', 'MILK', 3], ['WATER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FERTILIZE'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['WEST'], ['FEED'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['CARE'], ['HARVEST'], ['FERTILIZE'], ['CARE'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['FEED'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['PLANT', 'WHEAT'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['FEED'], ['WATER'], ['WEST'], ['CARE'], ['FERTILIZE'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['CARE'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['DIG'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['PLANT', 'CARROT'], ['WEST'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['DIG'], ['WEST'], ['NORTH'], ['CARE'], ['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['WATER'], ['FEED'], ['HARVEST'], ['WEST'], ['WEST'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['CARE'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'CARROT']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['DROP'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['NORTH'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['PLANT', 'CARROT'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['PLANT', 'CARROT'], ['FERTILIZE'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['PLANT', 'CARROT'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'CARROT']], 'market': [['SELL', 'CARROT', 13], ['SELL', 'CARROT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['PASS'], ['PASS'], ['WATER'], ['SOUTH'], ['WATER'], ['PASS'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['WEST'], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['WEST']], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['HARVEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['CARE'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['WATER'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['HARVEST'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['WEST'], ['EAST'], ['CARE']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['EAST'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['EAST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['EAST'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'CARROT', 13]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['DROP'], ['WATER'], ['EAST'], ['DROP']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 8]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['PLANT', 'CARROT'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['EAST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['EAST'], ['DROP'], ['NORTH'], ['SOUTH'], ['WEST'], ['FERTILIZE'], ['EAST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'CARROT', 4], ['SELL', 'WHEAT', 10]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['PASS'], ['DROP'], ['DROP'], ['WATER'], ['HARVEST'], ['PASS']], 'market': [['SELL', 'CARROT', 7], ['SELL', 'EGG', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 5], ['SELL', 'CARROT', 13], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'MILK', 3], ['DROP'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST']], 'market': [['SELL', 'CARROT', 13]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['FERTILIZE'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FEED'], ['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WATER'], ['EAST'], ['WEST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['WATER'], ['WEST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['DROP'], ['WEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 1], ['SELL', 'CARROT', 13]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['EAST'], ['EAST'], ['NORTH'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['DROP']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['HARVEST'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['EAST'], ['WATER'], ['HARVEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'CARROT', 5]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST'], ['DROP'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST']], 'market': [['SELL', 'CARROT', 7], ['SELL', 'CARROT', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 4]]}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['PASS'], ['PASS'], ['DROP'], ['WEST'], ['PASS'], ['PASS'], ['EAST'], ['DROP'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'CARROT', 7], ['SELL', 'EGG', 4]]}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'CARROT', 24], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['HARVEST'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'CARROT', 13], ['SELL', 'EGG', 4]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 6]]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 5], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['EAST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['HARVEST'], ['EAST'], ['EAST'], ['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['SOUTH'], ['EAST'], ['EAST'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['EAST'], ['SOUTH'], ['HARVEST'], ['EAST'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['SOUTH'], ['DROP'], ['DROP'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['DROP'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['DROP'], ['DROP'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'CARROT', 12], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['NORTH'], ['PASS'], ['PASS'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['DROP']], 'market': [['SELL', 'WHEAT', 23], ['SELL', 'FERTILIZER', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['PASS'], ['PASS'], ['DROP'], ['WEST'], ['PASS'], ['PASS'], ['NORTH']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'FERTILIZER', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['EAST'], ['PASS'], ['PASS'], ['PASS'], ['DROP'], ['PASS'], ['PASS'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'CARROT', 7], ['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['EAST'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST']], 'market': [['SELL', 'EGG', 1000], ['SELL', 'WHEAT', 7]]}]
_PROXY=make_agent({0:_DEMO})
def demonstrated_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
demonstrated_proxy.telemetry=_PROXY.chassis.diagnostics
agent=demonstrated_proxy
