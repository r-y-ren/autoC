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

_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['HIRE']]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1], ['PASS']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['PASS'], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP', 1], ['CARE'], ['WEST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['BUILD_PASTURE'], ['BUILD_PASTURE'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['PLACE', 'COW', 1], ['PLACE', 'SHEEP', 1], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'MELON'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WATER'], ['WATER']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['NORTH'], ['WEST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [[], [], [], [], [], [], [], []]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 1], ['CARE']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['DROP']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['SOUTH'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['PASS'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['PASS'], ['SOUTH'], ['WATER'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['PASS'], ['SOUTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['PASS'], ['CARE'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['PASS'], ['FEED'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['SOUTH'], ['PASS'], ['EAST'], ['HARVEST'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PASS'], ['FEED'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['PASS'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 7]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'SHEEP', 1], ['PASS'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], []]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PASS'], ['EAST'], ['WATER'], ['FEED'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PASS'], ['SOUTH'], ['HARVEST'], ['CARE'], ['PASS']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 2], ['DROP'], ['SOUTH'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['FEED'], ['PASS'], ['FEED'], ['CARE'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PLACE', 'SHEEP', 1], ['WEST'], ['PASS'], ['CARE'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['PASS'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WEST'], ['FEED'], ['PASS'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [[]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['FEED'], ['PASS'], ['WATER']], 'market': [[]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['CARE'], ['PASS'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'STRAWBERRY'], ['WEST'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['CARE'], ['PASS'], ['PASS'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'SHEEP', 1], ['CARE'], ['SOUTH'], ['WEST'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['DROP'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['PASS'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['DROP'], ['WATER'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['PASS'], ['HARVEST'], ['PASS'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['HARVEST'], 'hands': [['PLACE', 'SHEEP', 1], ['WATER'], ['PASS'], ['EAST'], ['PASS'], ['CARE']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['HARVEST'], ['PASS'], ['EAST'], ['PASS'], ['WEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WEST'], ['SOUTH'], ['PASS'], ['FEED'], ['PASS'], ['SOUTH']], 'market': [[]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['PASS'], ['CARE'], ['PASS'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['EAST'], ['PASS'], ['SOUTH'], ['PASS'], ['WEST']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WEST'], ['FEED'], ['PASS'], ['WEST'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['CARE'], ['PASS'], ['WEST'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['EAST'], ['PASS'], ['SOUTH'], ['PASS'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['EAST'], ['PASS'], ['CARE'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['CARE'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['DROP'], ['CARE'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 2], ['PASS'], ['WEST'], ['FEED'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PASS'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['PASS'], ['SOUTH'], ['FEED'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['PASS'], ['COLLECT_FERTILIZER'], ['NORTH'], ['DROP'], ['FEED']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['WEST'], ['PASS'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['EAST'], ['WEST'], ['PASS'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['CARE'], ['SOUTH'], ['WATER'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PLACE', 'SHEEP', 1], ['NORTH'], ['DROP'], ['NORTH'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['PASS'], ['NORTH'], ['PASS'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['PASS'], ['NORTH'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['HARVEST'], ['PASS'], ['DROP']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['NORTH'], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['EAST'], ['NORTH'], ['WEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'SHEEP', 1], ['SOUTH'], ['CARE'], ['FEED'], ['EAST'], ['WATER'], ['WEST'], ['EAST'], ['WEST']], 'market': [['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'SHEEP', 1], 'hands': [['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['NORTH'], ['WATER'], ['EAST'], ['NORTH']], 'market': [['SELL', 'WOOL', 6], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['EAST'], 'hands': [['BUILD_PASTURE'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'SHEEP', 1], ['COLLECT_FERTILIZER'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['PLACE', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['FEED'], ['SOUTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'SHEEP', 2]]}, {'farmer': ['PICKUP', 'SHEEP', 1], 'hands': [['PICKUP', 'SHEEP', 1], ['EAST'], ['CARE'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['SOUTH'], ['EAST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['BUILD_PASTURE'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['NORTH'], ['PASS'], ['EAST'], ['PICKUP', 'SHEEP', 1], ['EAST'], ['SOUTH'], ['NORTH'], ['BUILD_PASTURE'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['BUILD_PASTURE'], ['NORTH'], ['EAST'], ['EAST'], ['BUILD_PASTURE'], ['DROP'], ['COLLECT_FERTILIZER'], ['DIG'], ['NORTH']], 'market': [[]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PLACE', 'SHEEP', 1], ['PASS'], ['DROP'], ['EAST'], ['PLACE', 'SHEEP', 1], ['PICKUP', 'WHEAT', 2], ['EAST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['BUILD_PASTURE'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 2]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['BUILD_PASTURE'], ['CARE'], ['PLACE', 'SHEEP', 1], ['PLANT', 'MELON'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [[]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'MELON'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['CARE'], ['WATER'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['CARE'], ['EAST'], ['EAST'], ['EAST'], ['CARE'], ['EAST'], ['WATER'], ['EAST']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['FEED'], ['PLANT', 'MELON'], ['PLANT', 'MELON'], ['WEST'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'WHEAT'], ['PASS'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['DROP'], ['PASS'], ['WEST']], 'market': [[]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PLANT', 'MELON'], ['NORTH'], ['EAST'], ['NORTH'], ['FEED'], ['PASS'], ['PASS'], ['WEST']], 'market': [[], []]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['WATER'], ['FEED'], ['PLANT', 'MELON'], ['NORTH'], ['CARE'], ['PASS'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['CARE'], ['FEED'], ['PASS'], ['WATER'], ['CARE'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['PASS'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['EAST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['CARE'], 'hands': [['PLACE', 'FERTILIZER', 1], ['NORTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['SOUTH'], ['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['PLACE', 'FERTILIZER', 1]], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['SOUTH'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['PASS'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['NORTH'], ['EAST'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['FEED'], ['FEED'], ['WATER'], ['NORTH'], ['CARE']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['DROP'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['CARE'], ['PASS'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [[]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['CARE'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['CARE'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['FEED'], ['EAST'], ['EAST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['PASS'], ['FEED'], ['CARE'], ['WATER'], ['EAST'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['PICKUP', 'WHEAT', 1], ['CARE'], ['EAST'], ['NORTH'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'STRAWBERRY'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['SOUTH'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['EAST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PASS'], ['EAST'], ['PASS'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PASS'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['DROP'], ['WATER'], ['WATER'], ['PASS'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 5], 'hands': [['PICKUP', 'WHEAT', 3], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['EAST'], ['FEED'], ['WATER'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['EAST'], ['NORTH']], 'market': [['BUY_ANIMAL', 'SHEEP', 1], []]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['DROP'], ['CARE'], ['WEST'], ['PICKUP', 'SHEEP', 1], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 3], []]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['EAST'], ['WEST'], ['DROP'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 6], [], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PICKUP', 'SHEEP', 1], ['SOUTH'], ['NORTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['EAST'], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['EAST'], ['PICKUP', 'SHEEP', 1], ['CARE'], ['DROP'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['NORTH'], ['PICKUP', 'SHEEP', 1], ['EAST'], ['WATER'], ['EAST'], ['WEST'], ['PASS'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 1], ['FEED'], ['PASS'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['CARE'], ['CARE'], ['EAST'], ['DROP']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['CARE'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['BUILD_PASTURE'], ['NORTH'], ['WATER'], ['FEED'], ['NORTH'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['NORTH'], ['PLACE', 'SHEEP', 1], ['WATER'], ['EAST'], ['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['CARE'], ['FEED'], ['NORTH'], ['WATER'], ['NORTH'], ['FEED'], ['WEST'], ['HARVEST'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['HARVEST'], ['WATER'], ['CARE'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['BUILD_PASTURE'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['EAST'], ['EAST'], ['WATER'], ['PLACE', 'SHEEP', 1], ['EAST'], ['NORTH'], ['WATER'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['FEED'], ['WATER'], ['EAST'], ['PASS'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['CARE'], ['HARVEST'], ['WATER'], ['PASS'], ['EAST'], ['EAST'], ['FEED'], ['WATER'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['SOUTH'], ['CARE'], ['WEST'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['EAST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['BUILD_PASTURE'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['WEST'], ['PICKUP', 'SHEEP', 1], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 5], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FEED'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['PLACE', 'WOOL', 4], 'hands': [['EAST'], ['CARE'], ['WEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WOOL', 4], []]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['EAST'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['FEED']], 'market': [['SELL', 'WOOL', 4], ['BUY_LAND']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PICKUP', 'SHEEP', 1], ['PLACE', 'FERTILIZER', 1], ['CARE'], ['CARE'], ['EAST'], ['NORTH'], ['FEED'], ['EAST'], ['WATER'], ['CARE']], 'market': [['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['DROP'], ['WATER'], ['CARE'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['FEED'], 'hands': [['BUILD_PASTURE'], ['FEED'], ['EAST'], ['NORTH'], ['PICKUP', 'SHEEP', 1], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['CARE'], 'hands': [['PLACE', 'SHEEP', 1], ['CARE'], ['DROP'], ['FEED'], ['WEST'], ['BUILD_PASTURE'], ['WEST'], ['WATER'], ['WEST'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [['PASS'], ['COLLECT_FERTILIZER'], ['PASS'], ['CARE'], ['SOUTH'], ['PLACE', 'SHEEP', 1], ['WATER'], ['NORTH'], ['WATER'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PICKUP', 'COW', 1], ['NORTH'], ['PASS'], ['COLLECT_FERTILIZER'], ['BUILD_PASTURE'], ['FEED'], ['WEST'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['FEED'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['PLACE', 'SHEEP', 1], ['CARE'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PASS'], ['CARE'], ['SOUTH'], ['SOUTH'], ['CARE'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['PASS'], ['COLLECT_FERTILIZER'], ['FEED'], ['DROP'], ['EAST'], ['FEED'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['NORTH'], ['CARE'], ['NORTH'], ['WEST'], ['CARE'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['BUILD_PASTURE'], ['NORTH'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['DIG'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PLACE', 'COW', 1], ['FEED'], ['FEED'], ['NORTH'], ['PASS'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PASS'], ['NORTH'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['PASS'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['EAST'], ['CARE'], ['HARVEST'], ['SOUTH'], ['WEST'], ['FEED'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['FEED'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['NORTH'], ['PASS'], ['CARE'], ['WATER'], ['WEST'], ['NORTH'], ['PASS'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 1], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['FEED'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['HARVEST'], ['NORTH'], ['PICKUP', 'WHEAT', 3]], 'market': [['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['DROP'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['WATER'], ['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['FEED']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['EAST'], ['FEED'], ['CARE'], ['HARVEST'], ['WATER'], ['WEST'], ['FEED'], ['HARVEST'], ['WEST'], ['WATER'], ['CARE']], 'market': [['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['WATER'], ['CARE'], ['EAST'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['SOUTH'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['NORTH'], ['FEED'], ['NORTH'], ['DROP'], ['PLANT', 'WHEAT'], ['EAST'], ['FEED'], ['DROP'], ['WEST'], ['EAST'], ['CARE']], 'market': [['SELL', 'MELON', 6], ['SELL', 'MELON', 6]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 4], ['FEED'], ['PICKUP', 'SHEEP', 1], ['WATER'], ['PASS'], ['WATER'], ['EAST'], ['CARE'], ['PASS'], ['FEED'], ['DROP'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6], ['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['CARE'], ['SOUTH'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'COW', 1], ['CARE'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'MELON', 5], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'SHEEP', 1], ['WATER'], ['DROP'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['EAST'], ['BUILD_PASTURE'], ['WEST'], ['SOUTH'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['FEED'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WATER'], ['PLACE', 'SHEEP', 1], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['FEED'], ['CARE'], ['BUILD_PASTURE'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['NORTH'], ['FEED'], ['DIG'], ['WEST'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['PLACE', 'COW', 1], ['WEST'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['FEED'], ['CARE'], ['PLANT', 'WHEAT'], ['BUILD_PASTURE'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['WATER'], ['PLACE', 'SHEEP', 1], ['WATER'], ['SOUTH'], ['FEED'], ['WEST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['FEED'], ['NORTH'], ['CARE'], ['CARE'], ['WATER'], ['WATER'], ['FEED'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['CARE'], ['NORTH'], ['DROP'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['CARE'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['WATER'], ['PASS'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['PASS'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['PASS'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['SOUTH'], ['PASS'], ['PASS'], ['WATER'], ['NORTH'], ['PASS'], ['DIG'], ['WATER'], ['SOUTH'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 14], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['CARE'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['WEST'], ['NORTH'], ['FEED'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['WEST'], ['HARVEST'], ['FEED'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['EAST'], ['CARE'], ['WEST'], ['SOUTH'], ['WEST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['FEED'], ['FEED'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['CARE'], ['CARE'], ['WATER'], ['NORTH'], ['SOUTH'], ['FEED'], ['WEST'], ['WATER'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['EAST'], ['CARE'], ['FERTILIZE'], ['HARVEST'], ['FERTILIZE'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['CARE'], ['DROP'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['SOUTH'], ['WATER'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['FEED'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['CARE'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['EAST'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['CARE'], ['SOUTH'], ['WATER'], ['SOUTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['EAST'], ['PLANT', 'TOMATO'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['PASS'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['PASS'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'SHEEP', 1], ['PASS'], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 9], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['FEED'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['PLACE', 'WOOL', 4], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['CARE'], ['CARE'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['HARVEST'], ['WEST'], ['FEED'], ['EAST'], ['WATER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['BUILD_PASTURE'], ['FEED'], ['CARE'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['PLACE', 'SHEEP', 1], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['PLANT', 'TOMATO'], ['FEED'], ['HARVEST'], ['FEED'], ['FEED'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WATER'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['FERTILIZE'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['CARE'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['WATER'], ['SOUTH'], ['CARE'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['NORTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['WEST'], ['FEED'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['FEED'], ['WEST'], ['HARVEST'], ['CARE'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['NORTH'], ['CARE'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['CARE'], ['WEST'], ['EAST'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['NORTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['PLANT', 'TOMATO'], ['HARVEST'], ['WATER'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['DROP'], ['WATER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['PLANT', 'TOMATO']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['PASS'], ['WEST'], ['WEST'], ['WATER'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 14], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['EAST'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['NORTH'], ['DROP'], ['SOUTH'], ['FEED'], ['FERTILIZE'], ['WATER'], ['CARE'], ['CARE'], ['NORTH']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['CARE'], ['WATER'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['FEED'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['CARE'], ['HARVEST'], ['FEED'], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['FEED'], ['WATER'], ['HARVEST'], ['CARE'], ['FEED'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['EAST'], ['CARE'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FERTILIZE'], ['EAST'], ['NORTH'], ['WEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['FEED'], ['FERTILIZE'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['SOUTH'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['CARE'], ['WATER']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['NORTH'], ['FEED'], ['WEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['HARVEST'], ['CARE'], ['FEED'], ['CARE'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['WATER'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WOOL', 6], ['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['CARE'], ['WEST'], ['EAST'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['PLANT', 'TOMATO'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['PLANT', 'TOMATO'], ['EAST'], ['SOUTH'], ['CARE'], ['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['DROP'], ['PASS'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 10], ['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['EAST'], ['SOUTH'], ['EAST'], ['EAST'], ['EAST'], ['HARVEST'], ['SOUTH'], ['PASS'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 18]]}, {'farmer': ['PASS'], 'hands': [['DIG'], ['PASS'], ['PASS'], ['EAST'], ['PASS'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 14], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['FEED'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['FEED'], ['WATER'], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['SOUTH'], ['NORTH'], ['CARE'], ['CARE'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WEST'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['FEED'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['FEED'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['CARE'], ['FEED'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH'], ['PLANT', 'TOMATO'], ['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['FEED'], ['FERTILIZE'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WEST'], ['FEED'], ['WATER'], ['DROP']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['CARE'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['HARVEST'], ['NORTH'], ['WEST'], ['WEST'], ['HARVEST'], ['PLANT', 'TOMATO'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FERTILIZE'], ['FEED'], ['PLANT', 'TOMATO'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WOOL', 17]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['HARVEST'], ['EAST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'WOOL', 5]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['PLACE', 'WOOL', 4], ['WEST'], ['FEED'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH']], 'market': [['SELL', 'WOOL', 9]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 4], ['DROP'], ['WEST'], ['CARE'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'WOOL', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['PICKUP', 'WHEAT', 3], ['FEED'], ['COLLECT_FERTILIZER'], ['DROP'], ['DROP'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['FEED'], ['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['WATER'], ['WEST'], ['CARE'], ['CARE'], ['FEED']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 11]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['FEED'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WEST'], ['FEED'], ['CARE'], ['CARE'], ['WEST'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['FEED'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FEED'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['CARE'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['CARE'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['SOUTH'], ['SOUTH'], ['CARE'], ['FEED'], ['WATER'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['FEED'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['HARVEST'], ['CARE'], ['HARVEST'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'TOMATO'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['FEED'], ['NORTH'], ['WATER'], ['HARVEST'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WATER'], ['WATER'], ['WEST'], ['CARE'], ['WATER'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'TOMATO'], ['WEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST'], ['HARVEST'], ['DROP']], 'market': [['SELL', 'WOOL', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['EAST'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['EAST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['PASS'], ['WEST'], ['COLLECT_FERTILIZER'], ['PASS'], ['WATER'], ['PASS']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['NORTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'FERTILIZER', 11], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['FEED'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['HARVEST'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['FEED'], ['WATER'], ['SOUTH'], ['NORTH'], ['EAST'], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['DROP'], ['WATER'], ['FEED'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['CARE'], ['FEED'], ['FEED']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['SOUTH'], ['CARE'], ['CARE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['FEED'], ['SOUTH'], ['FEED'], ['DROP'], ['HARVEST'], ['NORTH'], ['FEED'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['CARE'], ['PICKUP', 'WHEAT', 3], ['PLANT', 'STRAWBERRY'], ['FEED'], ['CARE'], ['WEST'], ['CARE'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['CARE'], ['NORTH'], ['DROP'], ['HARVEST'], ['FEED'], ['NORTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['FERTILIZE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['PLANT', 'WHEAT'], ['CARE'], ['HARVEST'], ['HARVEST'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['FEED']], 'market': [['SELL', 'WOOL', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE'], ['NORTH'], ['WATER'], ['HARVEST'], ['CARE']], 'market': [['SELL', 'WOOL', 6], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['NORTH'], ['FEED'], ['PLANT', 'TOMATO'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['FEED'], ['CARE'], ['WATER'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 6]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['DROP'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['SOUTH'], ['PASS'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['EAST'], ['NORTH'], ['DROP'], ['FEED']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WATER'], ['PASS'], ['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 5]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['PASS'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['DIG'], ['SOUTH'], ['PASS'], ['PASS'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 5]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'MELON', 11], ['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'WOOL', 6], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['CARE'], ['EAST'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['DROP'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['FEED']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['NORTH'], ['CARE'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['CARE'], ['CARE'], ['CARE']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['HARVEST'], ['FEED'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['FERTILIZE'], ['WATER'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['CARE'], ['FEED'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['CARE'], ['WATER'], ['NORTH'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['CARE']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['CARE'], ['NORTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['FEED'], ['WEST'], ['FEED'], ['WEST'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['CARE'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['FEED'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'WOOL', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['PLANT', 'WHEAT'], ['FEED'], ['PLANT', 'WHEAT'], ['DROP'], ['WEST'], ['CARE'], ['WEST'], ['EAST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['CARE'], ['WEST'], ['NORTH'], ['FEED'], ['WEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FERTILIZE'], ['CARE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['PASS'], ['EAST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 5]]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['NORTH'], ['DROP'], ['PASS'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'WOOL', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['PLACE', 'WOOL', 4], ['PLACE', 'WOOL', 4], ['WEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['PICKUP', 'WHEAT', 4], ['EAST']], 'market': [['SELL', 'WOOL', 8]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['WEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['EAST'], ['PLACE', 'WOOL', 4], ['PLACE', 'WOOL', 4], ['WEST'], ['DROP'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 8]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['DROP'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['DROP'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['CARE'], ['SOUTH'], ['CARE'], ['EAST']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['FEED'], ['FEED'], ['WEST'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['SOUTH'], ['FEED'], ['CARE'], ['CARE'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['FEED'], ['SOUTH'], ['FEED'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WATER'], ['FERTILIZE'], ['CARE'], ['FERTILIZE'], ['CARE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['CARE'], ['CARE'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['PASS'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['FERTILIZE'], ['CARE'], ['CARE'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['CARE'], ['EAST'], ['FEED'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 14]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['PASS'], ['SOUTH'], ['NORTH'], ['WEST'], ['EAST'], ['CARE'], ['CARE'], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['NORTH'], ['WATER'], ['FEED'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['NORTH'], ['SOUTH'], ['CARE'], ['WEST'], ['EAST'], ['EAST'], ['WEST'], ['DIG'], ['WATER'], ['HARVEST'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['DROP'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['EAST'], ['PLANT', 'TOMATO'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['CARE'], ['PASS'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 5]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PASS'], ['EAST'], ['WATER'], ['WEST'], ['EAST'], ['EAST'], ['DIG'], ['HARVEST']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['DROP'], 'hands': [['FERTILIZE'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['PASS'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['SELL', 'MILK', 6], ['SELL', 'WOOL', 4]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['NORTH'], ['PASS'], ['NORTH'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['SOUTH'], ['SOUTH'], ['PASS'], ['WATER'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'WOOL', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 11]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['EAST'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FEED'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['CARE'], ['SOUTH'], ['EAST'], ['WEST'], ['FEED'], ['CARE'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['EAST'], ['FEED'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 11]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['WATER'], ['CARE'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['FEED'], ['NORTH'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE'], ['FERTILIZE'], ['CARE'], ['NORTH']], 'market': [['SELL', 'WOOL', 4], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WATER'], ['FERTILIZE'], ['PASS'], ['NORTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['FEED'], ['FEED'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['CARE'], ['FEED'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['CARE'], ['CARE'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FERTILIZE'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['DIG']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['CARE'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['DIG'], ['CARE'], ['EAST'], ['SOUTH'], ['WATER'], ['DIG'], ['WEST'], ['WEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['EAST'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['EAST'], ['NORTH'], ['SOUTH'], ['EAST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['FERTILIZE'], ['DROP'], ['DROP'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['HARVEST'], ['WATER'], ['PASS'], ['NORTH'], ['PASS'], ['PASS'], ['DROP'], ['EAST'], ['EAST'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'WHEAT', 9]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 9], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['PLACE', 'MILK', 3], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['FEED'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['CARE']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['SOUTH'], ['EAST'], ['HARVEST'], ['FEED'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FERTILIZE'], ['WEST'], ['CARE'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['CARE']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['CARE'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['FEED'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['FEED'], ['EAST'], ['SOUTH'], ['EAST'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['WATER'], ['HARVEST'], ['CARE'], ['FEED'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['PASS'], ['WEST'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['CARE']], 'market': [['SELL', 'WOOL', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['DIG'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['EAST'], ['CARE'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'TOMATO', 2]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['DROP'], ['WEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['PASS'], ['SOUTH'], ['DIG'], ['DROP'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['EAST'], ['WEST'], ['EAST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'MILK', 3]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PASS'], ['DROP'], ['PLANT', 'WHEAT'], ['PASS'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'TOMATO', 3], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 7], ['SELL', 'TOMATO', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'WOOL', 4], ['PLACE', 'WOOL', 4], ['WEST'], ['FEED'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'WOOL', 8]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['WEST'], ['CARE'], ['WEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['PLACE', 'WOOL', 4], ['DROP'], ['WEST'], ['COLLECT_FERTILIZER'], ['PLACE', 'WOOL', 4], ['FEED'], ['FEED'], ['FEED']], 'market': [['SELL', 'WOOL', 8]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['SOUTH'], ['WEST'], ['EAST'], ['CARE'], ['CARE'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['SOUTH'], ['FEED'], ['FEED'], ['FEED'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['FEED'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['PASS'], ['WEST'], ['FEED'], ['WATER'], ['WEST'], ['CARE'], ['CARE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['CARE'], ['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['NORTH'], ['CARE'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['NORTH'], ['HARVEST'], ['FEED'], ['FEED'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['CARE'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'TOMATO', 6]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['NORTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['FEED'], ['WATER'], ['WEST'], ['FERTILIZE'], ['HARVEST']], 'market': [['SELL', 'WOOL', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['WATER'], ['FEED'], ['WATER'], ['NORTH'], ['CARE'], ['NORTH'], ['HARVEST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['CARE'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['DIG'], ['EAST'], ['DROP']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FERTILIZE'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['PASS'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['PASS'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 11], ['SELL', 'TOMATO', 2], ['SELL', 'FERTILIZER', 10]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['DROP'], ['DROP'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['PASS'], ['WATER'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['DROP']], 'market': [['SELL', 'WOOL', 6], ['SELL', 'STRAWBERRY', 3], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'TOMATO', 10], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['PLACE', 'MILK', 2], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 1], ['EAST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['NORTH'], ['NORTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['CARE'], ['WATER'], ['FEED']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['EAST'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['FEED'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['CARE'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['WATER'], ['FEED'], ['FERTILIZE'], ['SOUTH']], 'market': [['SELL', 'WOOL', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['FEED'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['CARE'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['CARE'], ['HARVEST'], ['FEED'], ['WATER']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['WEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['FEED'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['CARE'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['CARE'], ['NORTH'], ['DIG']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['WATER'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['FEED'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['EAST'], ['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WEST'], ['EAST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WEST'], ['DROP'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WEST'], ['FERTILIZE'], ['EAST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['DROP'], ['PLANT', 'WHEAT'], ['HARVEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 12]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['PASS'], ['WATER'], ['DIG'], ['WATER'], ['DROP'], ['SOUTH'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'WHEAT', 5], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['EAST']], 'market': [['SELL', 'TOMATO', 10], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['WEST'], ['WEST'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['CARE'], ['EAST'], ['NORTH'], ['WEST'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['DROP'], ['WEST'], ['WATER'], ['EAST'], ['FEED'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['NORTH'], ['WATER'], ['SOUTH'], ['FEED'], ['HARVEST'], ['NORTH'], ['CARE'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['SOUTH'], ['FEED'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['CARE'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['NORTH'], ['FEED'], ['WATER'], ['HARVEST'], ['CARE'], ['WEST']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['DIG'], ['FEED'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['FEED'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['FEED'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['FEED'], ['CARE'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['CARE'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['PASS'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'TOMATO', 8]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['CARE'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['WEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WATER'], ['DIG'], ['EAST'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['WEST'], ['EAST'], ['EAST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['WEST'], ['WATER'], ['EAST'], ['SOUTH'], ['DIG'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 7]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['DROP'], ['NORTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['FERTILIZE'], ['FEED'], ['DROP'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PASS'], ['HARVEST'], ['DROP']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['CARE'], ['EAST'], ['WATER'], ['DROP'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'CARROT', 9], ['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['FERTILIZE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PASS'], ['HARVEST'], ['PASS'], ['PASS'], ['NORTH'], ['PASS'], ['HARVEST'], ['PASS']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'TOMATO', 2], ['SELL', 'FERTILIZER', 10]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WOOL', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 6], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'WOOL', 4], ['PLACE', 'WOOL', 4], ['WEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'WOOL', 9]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['WEST'], ['FEED'], ['SOUTH'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['FEED'], ['CARE'], ['PLACE', 'WOOL', 4], ['DROP'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['FEED']], 'market': [['SELL', 'WOOL', 8]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['PASS'], ['SOUTH'], ['WEST'], ['EAST'], ['CARE'], ['DROP'], ['CARE']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['FEED'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['CARE'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['NORTH'], ['CARE'], ['FEED']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['CARE'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WATER'], ['WEST'], ['FEED'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST'], ['NORTH'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['DIG'], ['EAST'], ['FEED'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 2], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['CARE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['PLANT', 'WHEAT'], ['NORTH'], ['FEED'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['FERTILIZE'], ['CARE'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['FEED'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'TOMATO', 10]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['CARE'], ['EAST'], ['EAST'], ['WEST'], ['CARE'], ['HARVEST'], ['WEST'], ['PLANT', 'CARROT'], ['DIG'], ['CARE'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'TOMATO', 4]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['PASS'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['PASS']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 6]]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['PASS'], ['WATER'], ['SOUTH'], ['PASS'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['EAST']], 'market': [['SELL', 'WOOL', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['PASS'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WEST'], ['EAST'], ['FEED'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['CARE'], ['CARE'], ['FEED']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['CARE'], ['WEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PASS']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['SOUTH'], ['FEED'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['PASS'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['CARE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH'], ['CARE'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['SOUTH'], ['NORTH'], ['FEED'], ['WEST'], ['FERTILIZE'], ['FEED'], ['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['SOUTH'], ['WATER'], ['WEST'], ['CARE'], ['HARVEST'], ['WATER'], ['CARE'], ['WATER'], ['CARE'], ['NORTH'], ['PLANT', 'CARROT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['CARE'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WATER'], ['WEST'], ['CARE'], ['WEST']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['DIG'], ['DIG'], ['SOUTH'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['HARVEST'], ['HARVEST'], ['WEST'], ['CARE'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['PASS'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['WEST'], ['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['PASS'], ['NORTH'], ['WEST'], ['WATER'], ['DIG']], 'market': []}, {'farmer': ['EAST'], 'hands': [['CARE'], ['NORTH'], ['WATER'], ['CARE'], ['EAST'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST'], ['HARVEST'], ['PLANT', 'CARROT']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'TOMATO', 12]]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['DROP'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 11], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['HARVEST'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['EAST'], ['EAST'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['SELL', 'WHEAT', 13]]}, {'farmer': ['DROP'], 'hands': [['WATER'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['PASS'], ['PASS'], ['PASS'], ['FERTILIZE'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'TOMATO', 6], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'TOMATO', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['PLACE', 'MILK', 4], ['NORTH'], ['WEST'], ['EAST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'WHEAT', 11]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WEST'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['FEED'], ['WEST'], ['WATER'], ['CARE']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WATER'], ['CARE'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['CARE'], ['FEED'], ['WEST'], ['FERTILIZE'], ['WEST'], ['FEED'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WEST'], ['CARE'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['CARE'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'TOMATO', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['DIG'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['DIG'], ['WEST'], ['WATER'], ['HARVEST'], ['EAST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['FEED'], ['NORTH']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST'], ['WATER'], ['HARVEST'], ['FEED'], ['WEST'], ['WEST'], ['CARE'], ['FERTILIZE']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['SOUTH'], ['DROP'], ['DROP'], ['FEED'], ['SOUTH'], ['PLANT', 'WHEAT'], ['CARE'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'MILK', 5]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['WATER'], ['NORTH'], ['NORTH'], ['CARE'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['FERTILIZE'], 'hands': [['PASS'], ['EAST'], ['NORTH'], ['WEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['EAST'], ['FERTILIZE'], ['WEST'], ['DROP'], ['FERTILIZE'], ['NORTH'], ['PASS']], 'market': [['SELL', 'WOOL', 9], ['SELL', 'WHEAT', 10]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['WATER'], ['COLLECT_FERTILIZER'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['WATER'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 17]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WOOL', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['SELL', 'TOMATO', 10]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'WOOL', 11], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['PLACE', 'WOOL', 4], ['PLACE', 'WOOL', 4], ['WEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST']], 'market': [['SELL', 'WOOL', 9]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['WEST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['DROP'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['DROP'], ['SOUTH'], ['FEED'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 8]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['FEED'], ['DROP']], 'market': [['SELL', 'WOOL', 8]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['EAST'], ['SOUTH'], ['FEED'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FEED'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['DROP'], ['SOUTH'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'WOOL', 8]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['FEED'], ['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['EAST'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['FEED'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['WATER'], ['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER'], ['CARE'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['FEED'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['PLANT', 'WHEAT'], ['EAST'], ['HARVEST'], ['CARE'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['SOUTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['DROP'], ['WATER'], ['FEED'], ['WATER'], ['WEST'], ['FEED'], ['HARVEST'], ['WEST'], ['EAST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['HARVEST'], ['CARE'], ['WEST'], ['WATER'], ['CARE'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WEST'], ['DROP'], ['WATER'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 10]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['SOUTH'], ['PASS'], ['SOUTH'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['FERTILIZE'], ['PASS'], ['FERTILIZE'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 2], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 3], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 2], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['WEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FEED'], ['WATER'], ['FERTILIZE'], ['EAST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 5]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WOOL', 12]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['WEST'], ['EAST'], ['SOUTH'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['SOUTH'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['FEED'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['EAST'], ['EAST'], ['EAST'], ['EAST'], ['HARVEST'], ['DROP'], ['COLLECT_FERTILIZER'], ['FEED'], ['EAST']], 'market': [['SELL', 'CARROT', 7]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['SOUTH'], ['EAST'], ['EAST'], ['CARE'], ['EAST']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'TOMATO', 4]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['PASS'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['NORTH'], ['SOUTH'], ['DROP'], ['SOUTH'], ['PASS'], ['NORTH'], ['EAST'], ['SOUTH'], ['DROP']], 'market': [['SELL', 'CARROT', 7], ['SELL', 'WHEAT', 18]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['EAST'], ['SOUTH'], ['PASS'], ['SOUTH'], ['PASS'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'WHEAT', 7], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'CARROT', 24], ['SELL', 'WHEAT', 29], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'TOMATO', 3]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 5]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['EAST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['EAST'], ['EAST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['HARVEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['DROP'], ['EAST'], ['WEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['NORTH'], ['SOUTH'], ['WEST'], ['DROP'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['PASS'], ['DROP']], 'market': [['SELL', 'WHEAT', 18]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['DROP'], ['DROP'], ['PASS'], ['DROP'], ['DROP'], ['PASS'], ['PASS']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'MILK', 3]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['NORTH'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 21]]}, {'farmer': ['PASS'], 'hands': [['DROP'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'WHEAT', 20], ['SELL', 'WOOL', 4], ['SELL', 'WHEAT', 13]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'WHEAT', 4]]}]
_PROXY=make_agent({0:_DEMO})
def demonstrated_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
demonstrated_proxy.telemetry=_PROXY.chassis.diagnostics
agent=demonstrated_proxy
