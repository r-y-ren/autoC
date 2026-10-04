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

_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['HIRE']]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1]], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['PLACE', 'SHEEP', 1], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP', 1], ['CARE'], ['WEST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['BUILD_PASTURE'], ['BUILD_PASTURE'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['PLACE', 'COW', 1], ['PLACE', 'SHEEP', 1], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'MELON'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['PASS'], ['PASS'], ['PLANT', 'WHEAT']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['DROP'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['CARE'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PICKUP', 'WHEAT', 3], ['WEST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 2], ['CARE'], ['EAST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['CARE'], ['DROP']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['FEED'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['SOUTH'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['FEED'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['NORTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['NORTH']], 'market': [['SELL', 'WHEAT', 3]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['PASS'], ['SOUTH'], ['WATER'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['PASS'], ['SOUTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['PASS'], ['CARE'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['PASS'], ['FEED'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['SOUTH'], ['PASS'], ['EAST'], ['HARVEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['NORTH'], ['FEED'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['PASS'], ['PASS'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PLANT', 'WHEAT'], ['PASS'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['SOUTH'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['DROP'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['PASS'], ['FEED'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['PASS'], ['CARE'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PLACE', 'COW', 1], ['WATER'], ['PASS'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WEST'], ['NORTH'], ['PASS'], ['SOUTH'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'STRAWBERRY'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['HARVEST'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['DROP'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['SOUTH'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PASS'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PASS'], ['EAST'], ['HARVEST'], ['DROP'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WEST'], ['DROP'], ['EAST'], ['PASS'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['FEED'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['PASS'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['CARE'], ['FEED'], ['NORTH'], ['PASS'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['FEED'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['HARVEST'], ['FEED'], ['CARE'], ['CARE'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['CARE'], ['FEED'], ['SOUTH'], ['PASS'], ['PASS']], 'market': [[]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['FEED'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['CARE'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['FEED'], ['CARE'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['SOUTH'], ['EAST'], ['CARE'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['FEED'], ['FEED'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['CARE'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WEST'], ['NORTH'], ['WEST'], ['DROP']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['WEST'], ['CARE'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WATER'], ['EAST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['FEED'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['NORTH'], ['CARE'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WEST'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['NORTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [[]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['NORTH'], ['FEED'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'COW', 1], ['NORTH'], ['CARE'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['DROP'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['BUILD_PASTURE'], ['SOUTH'], ['WEST'], ['WATER'], ['PICKUP', 'COW', 1], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PLACE', 'COW', 1], ['SOUTH'], ['FEED'], ['NORTH'], ['EAST'], ['SOUTH'], ['EAST'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['PLACE', 'FERTILIZER', 1], ['CARE'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['PLANT', 'MELON'], ['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['WATER'], ['BUILD_PASTURE'], ['SOUTH'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['EAST'], ['PLACE', 'COW', 1], ['SOUTH'], ['WATER'], ['WATER'], ['EAST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['DROP'], ['EAST'], ['SOUTH'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['DROP'], ['WATER'], ['PICKUP', 'GOOSE', 1], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['BUILD_COOP'], ['PICKUP', 'GOOSE', 1], ['EAST'], ['NORTH'], ['PICKUP', 'GOOSE', 1], ['DROP'], ['WATER'], ['PLANT', 'MELON']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PLACE', 'GOOSE', 1], ['EAST'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['PICKUP', 'GOOSE', 1], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['BUILD_COOP'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST']], 'market': [[]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['PLANT', 'WHEAT'], ['PLACE', 'GOOSE', 1], ['NORTH'], ['NORTH'], ['WEST'], ['PLANT', 'STRAWBERRY']], 'market': [[]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WATER'], ['BUILD_COOP'], ['WATER'], ['EAST'], ['EAST'], ['FEED'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['PLANT', 'STRAWBERRY'], ['EAST'], ['PLACE', 'GOOSE', 1], ['WEST'], ['NORTH'], ['PLACE', 'GOOSE', 1], ['WEST'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['WATER'], ['PLANT', 'WHEAT'], ['BUILD_COOP'], ['FEED'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['DROP'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PLACE', 'GOOSE', 1], ['CARE'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 4], []]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [[]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PLACE', 'FERTILIZER', 1], ['WEST'], ['FEED'], ['SOUTH'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['DROP'], ['SOUTH'], ['PLACE', 'FERTILIZER', 1], ['DROP']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WATER'], ['WATER'], ['WEST'], ['DROP'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['FEED'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['FEED'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['FEED'], ['CARE'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['NORTH'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['EAST'], ['NORTH'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['WATER'], ['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['SOUTH'], ['PASS'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PLACE', 'FERTILIZER', 1], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['SOUTH'], ['EAST'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST']], 'market': [[], []]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['DROP'], ['WATER'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 6], ['BUY_LAND'], []]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['PICKUP', 'GOOSE', 1], ['WATER'], ['SOUTH'], ['DROP'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['WEST'], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], [], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['BUILD_COOP'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WATER'], ['NORTH'], ['PLACE', 'GOOSE', 1], ['NORTH'], ['WATER'], ['SOUTH'], ['DROP'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['BUILD_COOP'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['PLACE', 'GOOSE', 1], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FEED'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['EAST'], ['WEST'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['CARE'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['DROP'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['DROP'], ['PASS'], ['NORTH'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FEED'], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['CARE'], ['FEED'], ['NORTH'], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['NORTH'], ['CARE'], ['NORTH'], ['EAST'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['WEST'], ['FEED']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PICKUP', 'COW', 1], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['NORTH'], ['PICKUP', 'COW', 1], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['CARE'], ['NORTH'], ['FEED'], ['DROP'], ['NORTH'], ['BUILD_PASTURE'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLACE', 'COW', 1], ['NORTH'], ['PICKUP', 'COW', 1], ['CARE'], ['PICKUP', 'COW', 1], ['FEED'], ['PLACE', 'COW', 1], ['EAST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['EAST'], 'hands': [['PICKUP', 'COW', 1], ['EAST'], ['WEST'], ['EAST'], ['PICKUP', 'COW', 1], ['CARE'], ['PICKUP', 'COW', 1], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['SOUTH'], ['FEED'], ['SOUTH'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['CARE'], ['BUILD_PASTURE'], ['FEED'], ['FEED'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['BUILD_PASTURE'], ['COLLECT_FERTILIZER'], ['PLACE', 'COW', 1], ['CARE'], ['WEST'], ['WATER'], ['FEED'], ['HARVEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'COW', 1], ['EAST'], ['SOUTH'], ['EAST'], ['FEED'], ['NORTH'], ['CARE'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['FEED'], ['WEST'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['EAST'], ['SOUTH'], ['WATER'], ['FEED'], ['CARE'], ['NORTH'], ['WEST'], ['NORTH'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WATER'], ['CARE'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['CARE'], ['HARVEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['DROP'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['EAST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['EAST'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['SOUTH'], ['WATER'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['CARE'], ['SOUTH'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['DROP'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['EAST'], ['WEST'], ['FEED'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['NORTH'], ['WEST'], ['CARE'], ['HARVEST'], ['WATER'], ['WEST'], ['CARE'], ['HARVEST'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['EAST'], ['CARE'], ['HARVEST']], 'market': [['SELL', 'MELON', 6], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['EAST'], ['EAST'], ['CARE'], ['SOUTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['FEED'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['NORTH'], ['EAST'], ['CARE'], ['EAST'], ['CARE'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['NORTH'], ['SOUTH'], ['CARE'], ['DROP'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['DROP'], ['FEED'], ['EAST']], 'market': [['SELL', 'MELON', 12], ['SELL', 'MELON', 6]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 4], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['EAST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['DROP']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['SOUTH'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['WEST'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['FEED'], ['WEST'], ['FEED'], ['SOUTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['CARE'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['CARE'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['CARE'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WEST'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['EAST'], ['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['NORTH'], ['CARE'], ['FEED'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['FEED'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['EAST'], ['FERTILIZE'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['EAST'], ['WATER'], ['CARE'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['NORTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['FEED'], ['WATER'], ['WATER'], ['HARVEST'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['EAST'], ['CARE'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['NORTH'], ['WATER'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['FEED'], ['WATER'], ['WEST'], ['CARE'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['CARE'], ['EAST'], ['WATER'], ['WEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['FEED'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['NORTH'], ['EAST'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['DROP'], ['CARE'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['NORTH'], ['SOUTH'], ['WEST'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['FEED'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['CARE'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['CARE'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['PASS'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'WHEAT', 4], ['CARE'], ['CARE'], ['WEST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['CARE'], ['SOUTH'], ['EAST'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['HARVEST'], ['DROP'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['HARVEST'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['WEST'], ['FEED']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['EAST'], ['FEED'], ['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WATER'], ['CARE'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['DROP'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['HARVEST'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['FEED'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['SOUTH'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER'], ['EAST'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['EAST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['DROP'], ['WATER'], ['SOUTH'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['HARVEST'], ['EAST'], ['WATER'], ['PASS'], ['HARVEST'], ['EAST'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['NORTH'], ['FEED'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['NORTH'], ['CARE'], ['WATER'], ['WEST'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['FEED'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['CARE'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['FEED'], ['EAST'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['NORTH'], ['FEED'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED'], ['NORTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['CARE'], ['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['WATER'], ['FERTILIZE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['PLANT', 'CARROT'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WEST'], ['EAST'], ['WATER'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['FERTILIZE'], ['EAST'], ['SOUTH'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['PASS'], ['WATER'], ['EAST'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': [['SELL', 'EGG', 2]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 8], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['CARE'], ['WEST'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['WEST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['DROP'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['CARE']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['SOUTH'], ['CARE'], ['SOUTH'], ['EAST'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FEED'], ['HARVEST'], ['DROP'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['FEED']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['FEED'], ['EAST'], ['WATER'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['CARE']], 'market': [['SELL', 'WHEAT', 5]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['CARE'], ['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['EAST'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['FEED'], ['WATER'], ['NORTH'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['CARE'], ['NORTH'], ['WATER'], ['NORTH'], ['CARE'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['EAST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['SOUTH'], ['FEED'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['EAST'], ['HARVEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PLANT', 'CARROT'], ['WATER'], ['CARE'], ['WEST'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['DROP'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WATER'], ['PASS'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['HARVEST'], ['WATER'], ['WATER'], ['PASS'], ['PASS'], ['WATER'], ['EAST']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'WOOL', 1], ['SELL', 'STRAWBERRY', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['SOUTH'], ['FEED'], ['WEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['FEED'], ['EAST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['WEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['FEED'], ['NORTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['CARE'], ['WEST'], ['EAST'], ['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'CARROT']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['HARVEST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['PLANT', 'CARROT'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['FERTILIZE'], ['EAST'], ['FERTILIZE'], ['WEST'], ['PLANT', 'CARROT'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 8], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['WATER'], ['NORTH'], ['PASS'], ['FERTILIZE'], ['WATER'], ['PASS'], ['FERTILIZE'], ['PASS'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['HARVEST'], ['EAST'], ['WEST'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['DROP'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['EAST'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['NORTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['CARE'], ['SOUTH'], ['PICKUP', 'WHEAT', 4], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['EAST'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['WEST'], ['CARE'], ['CARE'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['CARE'], ['NORTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['CARE'], ['SOUTH'], ['NORTH'], ['DROP'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['HARVEST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'WHEAT', 3], ['SOUTH'], ['FEED'], ['NORTH'], ['EAST'], ['WEST'], ['DROP'], ['HARVEST'], ['WEST'], ['EAST'], ['FEED'], ['EAST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['FEED'], ['PLANT', 'WHEAT'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['DROP'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'MELON', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['CARE'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['FEED'], ['EAST'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['FEED'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['FEED'], ['PLANT', 'WHEAT'], ['SOUTH'], ['CARE'], ['DROP'], ['FEED'], ['WEST'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'MILK', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['CARE'], ['WATER'], ['SOUTH'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['CARE'], ['DROP'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 10]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['DROP']], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['WATER'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['HARVEST'], ['EAST'], ['EAST'], ['WATER'], ['EAST'], ['WEST'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['WEST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'CARROT', 7]]}, {'farmer': ['PASS'], 'hands': [['CARE'], ['PASS'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['PASS'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 8], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['NORTH'], ['HARVEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['FEED'], ['WEST'], ['CARE'], ['WEST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['CARE'], ['CARE'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['HARVEST'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['WEST'], ['CARE'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['CARE'], ['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['FEED'], ['EAST'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['CARE'], ['FEED'], ['SOUTH'], ['WATER'], ['CARE'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['CARE'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['FEED'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['CARE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['FEED'], ['NORTH'], ['EAST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['CARE'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['HARVEST'], ['CARE'], ['HARVEST'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PLANT', 'CARROT'], ['EAST'], ['EAST'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['SOUTH'], ['DROP'], ['EAST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['PLANT', 'CARROT'], ['SOUTH'], ['WEST'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['PLANT', 'CARROT'], ['SOUTH'], ['SOUTH'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['EAST'], ['FEED'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'CARROT', 3]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['DROP'], ['WATER'], ['WATER'], ['WEST'], ['PASS'], ['HARVEST'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'EGG', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['SOUTH'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['HARVEST'], ['EAST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['FEED'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['CARE'], ['FEED'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['EAST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['DROP'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['DROP'], ['WATER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FERTILIZE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['FEED'], ['DROP'], ['NORTH'], ['WEST'], ['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['CARE'], 'hands': [['FERTILIZE'], ['HARVEST'], ['NORTH'], ['CARE'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['DROP'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['DROP'], ['HARVEST'], ['DROP'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['CARE'], ['WEST'], ['FEED'], ['WEST'], ['FEED'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['WEST'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['DIG'], ['SOUTH']], 'market': [['SELL', 'CARROT', 13]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['FEED'], ['FERTILIZE'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLANT', 'CARROT'], ['DROP']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['DIG'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['FEED'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['EAST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['EAST'], ['CARE'], ['NORTH'], ['DROP']], 'market': [['SELL', 'MILK', 5]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['PLANT', 'CARROT'], ['FEED'], ['WATER'], ['NORTH'], ['EAST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['CARE'], ['EAST'], ['HARVEST'], ['FEED'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['PLACE', 'MILK', 3], ['WEST'], ['FEED'], ['NORTH'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['FEED'], ['CARE'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['NORTH'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['FEED'], ['FEED'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['CARE'], ['WATER'], ['EAST'], ['NORTH'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['CARE'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['WATER'], ['EAST'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FERTILIZE'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['DIG'], ['FEED'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['PLANT', 'CARROT'], ['PLANT', 'WHEAT'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['DIG'], ['FERTILIZE']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['SOUTH'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['DIG'], ['EAST'], ['EAST'], ['DIG'], ['EAST'], ['WEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'CARROT', 13]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'CARROT'], ['WEST'], ['WEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['DROP'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 5], ['SELL', 'FERTILIZER', 5], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['PLACE', 'MILK', 6], ['EAST'], ['WEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['CARE'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 5]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['FEED'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['FEED'], ['EAST'], ['WEST'], ['FEED']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['CARE'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['WEST'], ['WATER'], ['FEED'], ['WEST'], ['EAST'], ['WEST'], ['DIG'], ['EAST'], ['SOUTH'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['CARE'], ['WEST'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['HARVEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['PLANT', 'CARROT'], ['WEST'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['WEST'], ['DROP'], ['DROP'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'CARROT'], ['WEST']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['DIG'], ['PLANT', 'CARROT'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['FEED']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST'], ['DROP'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['HARVEST'], ['EAST'], ['EAST'], ['WATER'], ['EAST'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['DIG'], 'hands': [['NORTH'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['DROP'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['EAST'], ['HARVEST'], ['WATER'], ['NORTH'], ['PASS'], ['EAST'], ['PASS'], ['HARVEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'EGG', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'CARROT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['CARE'], ['EAST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['FEED'], ['EAST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FERTILIZE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['CARE'], ['SOUTH'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['HARVEST'], ['FEED'], ['CARE'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['FEED'], ['HARVEST'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['CARE'], ['WEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['DIG']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['FERTILIZE'], ['WEST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['EAST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['NORTH'], ['PLANT', 'CARROT'], ['HARVEST'], ['EAST'], ['EAST'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['FERTILIZE']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['FEED'], ['PLANT', 'CARROT'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['FERTILIZE'], ['PASS'], ['CARE'], ['SOUTH'], ['CARE'], ['WATER'], ['FEED'], ['WEST'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'CARROT', 10], ['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['FERTILIZE'], ['CARE'], ['FERTILIZE'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['CARE'], ['HARVEST'], ['WEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['FEED'], ['HARVEST'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['DIG']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['FEED'], ['NORTH'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['DIG'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['CARE'], ['CARE'], ['NORTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['CARE'], ['NORTH'], ['WATER'], ['DIG'], ['WEST'], ['EAST'], ['NORTH'], ['DIG']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['DIG'], ['HARVEST'], ['WATER'], ['WEST'], ['CARE'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['EAST'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['FEED'], ['WATER'], ['DIG'], ['WEST'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'MILK', 1], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['HARVEST'], ['WEST'], ['WATER'], ['CARE'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['EAST'], 'hands': [['DIG'], ['PLANT', 'CARROT'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['DIG']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['FEED'], ['HARVEST'], ['NORTH'], ['EAST'], ['WATER'], ['HARVEST'], ['PLANT', 'CARROT']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['WATER'], ['CARE'], ['PLANT', 'CARROT'], ['HARVEST'], ['WATER'], ['HARVEST'], ['PLANT', 'CARROT'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['FERTILIZE'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['DIG'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'CARROT', 8], ['SELL', 'WOOL', 6]]}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['PASS'], ['FERTILIZE'], ['PASS'], ['SOUTH'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['WATER'], ['PASS'], ['PASS']], 'market': [['SELL', 'WHEAT', 6], ['SELL', 'MILK', 6], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['EAST'], ['SOUTH'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLACE', 'MILK', 3], ['DROP'], ['WEST'], ['PLACE', 'MILK', 3], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['CARE'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['FEED'], ['NORTH'], ['EAST'], ['SOUTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['FEED'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['HARVEST'], ['CARE'], ['HARVEST'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['FEED']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WEST'], ['FEED'], ['EAST'], ['WEST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['FEED'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['CARE'], ['DIG'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['CARE'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['FEED']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['HARVEST'], ['WEST'], ['CARE'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['DROP'], ['WATER'], ['WATER'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['SOUTH'], ['WEST'], ['PLANT', 'CARROT'], ['EAST'], ['SOUTH'], ['EAST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'CARROT', 13]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['SOUTH'], ['WEST'], ['SOUTH'], ['FEED'], ['WEST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['HARVEST'], ['DROP'], ['WEST'], ['HARVEST'], ['DROP'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['EAST'], ['EAST'], ['PLANT', 'CARROT'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 9], ['SELL', 'EGG', 4]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['PASS'], ['PASS'], ['WATER'], ['HARVEST'], ['FEED'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['NORTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['CARE'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FERTILIZE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['SOUTH'], ['CARE'], ['WEST'], ['FEED'], ['WEST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['CARE'], ['HARVEST'], ['HARVEST'], ['WATER'], ['FEED'], ['EAST'], ['FERTILIZE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'CARROT'], ['NORTH'], ['CARE'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['SOUTH'], ['PLANT', 'CARROT'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['EAST'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'CARROT'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['HARVEST'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['DROP']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['HARVEST']], 'market': [['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['EAST'], ['DROP']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['PASS'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['EAST'], ['PASS']], 'market': [['SELL', 'WHEAT', 5], ['SELL', 'CARROT', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['WATER'], ['HARVEST'], ['SOUTH'], ['DIG'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['SOUTH'], ['FEED'], ['WEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['CARE'], ['FEED'], ['FEED'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['EAST'], ['NORTH'], ['PLANT', 'CARROT']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['FERTILIZE'], ['FEED'], ['WATER'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['CARE'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'CARROT']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['HARVEST'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FERTILIZE'], ['PLANT', 'WHEAT'], ['WEST'], ['FEED'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['FERTILIZE'], ['CARE'], ['FEED'], ['EAST'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['DROP'], ['NORTH'], ['WATER'], ['WEST'], ['FEED'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['CARE'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['PLANT', 'CARROT'], ['WATER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['WEST'], ['DROP'], ['PLANT', 'CARROT'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'CARROT', 4], ['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['WEST'], ['PASS'], ['HARVEST'], ['WATER'], ['PASS'], ['EAST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'CARROT', 12], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['PLACE', 'MILK', 3], ['HARVEST'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['EAST'], ['WEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['CARE'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['DIG'], ['EAST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['FEED'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'CARROT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['DIG'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['FERTILIZE'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['FEED'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['EAST'], ['HARVEST'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['CARE'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['PLANT', 'CARROT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['FERTILIZE'], ['FEED'], ['WATER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['CARE'], ['WEST'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['FEED'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['CARE'], ['PLANT', 'CARROT'], ['NORTH'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['FEED'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['DROP'], ['WATER'], ['PLANT', 'CARROT']], 'market': [['SELL', 'CARROT', 13]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WEST'], ['HARVEST'], ['CARE'], ['WEST'], ['SOUTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['SOUTH'], ['PLANT', 'CARROT'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['DROP'], ['EAST'], ['WEST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['EAST'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['DROP'], ['WATER'], ['EAST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['EAST'], ['NORTH'], ['EAST'], ['HARVEST'], ['WATER'], ['DROP'], ['NORTH'], ['DROP'], ['HARVEST']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['EAST'], ['PLANT', 'CARROT'], ['HARVEST'], ['EAST'], ['NORTH'], ['EAST'], ['PLANT', 'CARROT']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['EAST'], ['PASS'], ['WATER']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 5], ['SELL', 'CARROT', 12], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['PLACE', 'MILK', 3], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['CARE'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WEST'], ['FEED'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['FEED'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['CARE'], ['HARVEST'], ['CARE'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['WEST'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['FEED'], ['WATER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST'], ['CARE'], ['EAST'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['DROP'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'CARROT', 7]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['EAST'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['EAST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['FEED'], ['HARVEST'], ['DROP'], ['WATER'], ['EAST'], ['CARE']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'CARROT'], ['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['CARE'], ['EAST'], ['NORTH'], ['HARVEST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 7], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['DROP'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['PASS'], ['WEST'], ['DROP'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'CARROT', 4]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'CARROT', 12], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['FEED'], ['WEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['DROP'], ['SOUTH'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['FEED'], ['NORTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['FEED'], ['WATER'], ['SOUTH'], ['HARVEST'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WEST'], ['HARVEST'], ['FEED'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['EAST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['EAST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['WEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['WATER'], ['HARVEST'], ['FEED'], ['EAST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'CARROT', 10]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['DROP'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['EAST'], ['EAST'], ['SOUTH'], ['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['DROP'], ['WATER']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 4]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['HARVEST'], ['EAST'], ['DROP'], ['EAST'], ['EAST'], ['EAST'], ['EAST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 3], ['SELL', 'CARROT', 13], ['SELL', 'EGG', 8]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['SOUTH'], ['EAST'], ['EAST'], ['WATER'], ['EAST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 2], ['SELL', 'EGG', 4]]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['EAST'], ['EAST'], ['EAST'], ['EAST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'CARROT', 24], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['HARVEST'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2], ['SELL', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['EAST'], ['DROP'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['EAST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['EAST'], ['NORTH'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['EAST'], ['HARVEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['EAST'], ['DROP'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['EAST'], ['DROP'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WEST'], ['DROP'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'CARROT', 7]]}, {'farmer': ['DROP'], 'hands': [['DROP'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['DROP'], ['DROP']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'EGG', 4]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'WHEAT', 13]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['DROP'], ['SOUTH'], ['DROP'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'CARROT', 7], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['DROP'], ['SOUTH'], ['SOUTH'], ['PASS'], ['DROP'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['DROP'], ['DROP'], ['PASS'], ['NORTH'], ['SOUTH'], ['EAST'], ['EAST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'CARROT', 4], ['SELL', 'EGG', 6]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['NORTH'], ['EAST'], ['EAST'], ['EAST']], 'market': [['SELL', 'WHEAT', 7], ['SELL', 'FERTILIZER', 5], ['SELL', 'FERTILIZER', 2]]}]
_PROXY=make_agent({0:_DEMO})
def demonstrated_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
demonstrated_proxy.telemetry=_PROXY.chassis.diagnostics
agent=demonstrated_proxy
