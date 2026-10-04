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

_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PICKUP', 'SHEEP', 1], ['NORTH'], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1]], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['BUILD_PASTURE'], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['NORTH'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['SOUTH'], ['BUILD_PASTURE']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['BUILD_PASTURE'], ['BUILD_PASTURE'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['DIG'], ['WEST'], ['SOUTH']], 'market': [['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['FEED'], 'hands': [['BUILD_PASTURE'], ['PICKUP', 'COW', 1], ['SOUTH'], ['PLACE', 'COW', 1], ['WEST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['SOUTH'], 'hands': [['DIG'], ['PLACE', 'COW', 1], ['SOUTH'], ['CARE'], ['BUILD_PASTURE']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'MELON'], ['CARE'], ['CARE'], ['EAST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['PICKUP', 'SHEEP', 1], 'hands': [['WATER'], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PLANT', 'MELON']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['WATER']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 1], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['WATER'], ['WEST'], ['WEST'], ['WEST'], ['PLANT', 'MELON']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['BUILD_PASTURE'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'MELON'], ['WATER'], ['PLACE', 'COW', 1], ['FEED'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['PLANT', 'MELON'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['CARE'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PLANT', 'MELON'], ['WEST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], []]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], []]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [[]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['SOUTH'], ['PASS'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], []]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], [], []]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['DROP'], ['DROP'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['WEST'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['NORTH'], ['PLANT', 'MELON'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['FEED'], ['NORTH'], ['EAST'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['EAST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['EAST'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], []]}, {'farmer': ['PICKUP', 'WHEAT', 1], 'hands': [['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['WEST'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 2], ['EAST'], ['SOUTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['EAST'], ['EAST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['DROP'], ['DROP'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['WATER'], ['HARVEST']], 'market': [[]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['BUILD_PASTURE'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], []]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['PLACE', 'COW', 1], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [[]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], [], []]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WHEAT', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WATER'], ['DROP'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['DROP'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WATER'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['CARE'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['FEED'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['CARE'], ['DROP']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['WATER'], ['CARE'], ['EAST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['FEED'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['CARE'], ['NORTH']], 'market': []}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [['DROP'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [[]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER']], 'market': [[]]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST']], 'market': [[]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['WEST']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['WATER']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['PASS'], ['WATER'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE']]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['DROP'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['DROP'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['CARE'], ['WATER'], ['WEST'], ['WATER'], ['DROP']], 'market': []}, {'farmer': ['DROP'], 'hands': [['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['FEED'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['DROP'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'STRAWBERRY'], ['SOUTH'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['EAST'], ['WEST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PASS'], ['NORTH'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['NORTH'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['NORTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 4], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['DROP'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WEST'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WATER'], ['CARE'], ['WATER'], ['EAST']], 'market': [[]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WEST'], ['EAST']], 'market': [[]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['WATER'], ['DROP']], 'market': [[]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['WATER'], ['WEST'], ['WATER'], ['WEST']], 'market': [[]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['CARE'], ['WATER'], ['WEST']], 'market': [[]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['EAST'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 1], ['WATER'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': [[], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['NORTH'], ['WEST'], ['PASS'], ['WEST'], ['NORTH']], 'market': [[]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['WEST']], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['PASS'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['PASS'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [[]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['DROP'], ['PASS'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['BUILD_PASTURE'], ['FEED'], ['DROP'], ['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['PLACE', 'COW', 1], ['CARE'], ['PICKUP', 'COW', 1], ['DROP'], ['NORTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['WEST'], ['EAST']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'STRAWBERRY'], ['EAST'], ['FEED'], ['EAST'], ['WEST'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['NORTH'], ['CARE'], ['BUILD_PASTURE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['DROP']], 'market': [['BUY_SEED', 'STRAWBERRY', 3]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['PLACE', 'COW', 1], ['SOUTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'COW', 1]], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'STRAWBERRY'], ['EAST'], ['FEED'], ['PLANT', 'STRAWBERRY'], ['DROP'], ['NORTH'], ['WATER'], ['EAST'], ['EAST']], 'market': [['BUY_SEED', 'STRAWBERRY', 3]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['WATER'], ['PICKUP', 'WHEAT', 1], ['WATER'], ['EAST'], ['EAST'], ['BUILD_PASTURE']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['PLACE', 'COW', 1]], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'STRAWBERRY'], ['EAST'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['WEST'], ['WATER'], ['DROP'], ['EAST']], 'market': [[]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['EAST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['EAST'], ['WEST'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['EAST']], 'market': [[]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'STRAWBERRY'], ['EAST'], ['WATER'], ['PASS'], ['FEED'], ['WATER'], ['WATER'], ['EAST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], []]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['CARE'], ['EAST'], ['EAST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], []]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], []]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['NORTH'], ['PASS'], ['PASS'], ['EAST'], ['WEST'], ['EAST'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], []]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], [], []]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['DROP'], ['WEST'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [[], [], []]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['DROP'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['SOUTH'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['DROP'], ['EAST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['PICKUP', 'WHEAT', 2], ['DROP'], ['FEED'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 2], ['WEST'], ['PICKUP', 'WHEAT', 2], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_ANIMAL', 'COW', 1], []]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['PICKUP', 'COW', 1], ['SOUTH'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['EAST'], ['EAST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['EAST'], ['FEED'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['EAST'], ['CARE'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['BUILD_PASTURE'], ['NORTH'], ['NORTH'], ['DROP']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['PLACE', 'COW', 1], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], [], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['PICKUP', 'WHEAT', 1]], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['FEED']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [[], [], []]}, {'farmer': ['HARVEST'], 'hands': [['DROP'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [[], [], []]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['EAST'], ['DROP'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['DROP']], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 10]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['DROP'], ['NORTH'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], [], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['WEST'], ['FEED'], ['WEST'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['BUY_LAND']]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 6], ['BUY_PRODUCT', 'WHEAT', 8]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['NORTH'], ['CARE'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['EAST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['EAST'], ['FEED'], ['WATER'], ['EAST'], ['EAST'], ['SOUTH'], ['CARE'], ['WEST'], ['DROP']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WATER'], ['CARE'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['DROP'], ['EAST'], ['WEST'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['WATER'], ['DROP'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WEST'], ['EAST'], ['WATER'], ['PICKUP', 'GOOSE', 1], ['EAST'], ['SOUTH'], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['PLANT', 'STRAWBERRY']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['WATER'], ['DROP'], ['NORTH'], ['EAST'], ['WATER'], ['SOUTH'], ['PICKUP', 'WHEAT', 1], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['NORTH'], ['PICKUP', 'GOOSE', 1], ['WATER'], ['EAST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['PICKUP', 'GOOSE', 1], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['SOUTH'], ['PLANT', 'MELON']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['NORTH'], ['BUILD_COOP'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['PICKUP', 'GOOSE', 1], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['CARE'], ['EAST'], ['PLACE', 'GOOSE', 1], ['WEST'], ['BUILD_COOP'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1], []]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 1], ['WATER'], ['PLACE', 'GOOSE', 1], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': [[], []]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WATER'], ['FEED'], ['WEST'], ['FEED'], ['SOUTH'], ['SOUTH'], ['BUILD_COOP'], ['PLANT', 'STRAWBERRY'], ['WEST']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WATER'], ['NORTH'], ['CARE'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT'], ['PASS'], ['PLACE', 'GOOSE', 1], ['WATER'], ['PASS']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['PASS'], ['SOUTH'], ['NORTH'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['FEED'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['WATER'], ['WEST'], ['PASS'], ['WATER'], ['CARE'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 3], ['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['NORTH'], ['WEST'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER']], 'market': [[], []]}, {'farmer': ['DROP'], 'hands': [['WATER'], ['CARE'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['DROP'], ['NORTH'], ['DROP']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['WEST'], ['EAST'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['FEED'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['FEED'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['SOUTH'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['CARE'], ['SOUTH'], ['WATER'], ['DROP'], ['NORTH'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['NORTH'], ['CARE'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['WATER'], ['FEED'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['WEST'], ['CARE'], ['EAST'], ['NORTH'], ['SOUTH'], ['CARE'], ['EAST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['PICKUP', 'COW', 1], ['WATER'], ['WEST'], ['EAST'], ['SOUTH'], ['DROP']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['EAST'], ['EAST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['FEED'], ['DROP'], ['SOUTH']], 'market': [['BUY_ANIMAL', 'COW', 1], []]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['BUILD_PASTURE'], ['WATER'], ['WEST'], ['CARE'], ['PICKUP', 'WHEAT', 2], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['PLACE', 'COW', 1], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER'], ['PICKUP', 'COW', 1], ['FEED']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['WEST'], ['WATER'], ['EAST'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WEST'], ['CARE'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['HARVEST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], []]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['BUILD_PASTURE'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PLACE', 'COW', 1], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], []]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['DROP'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['PASS'], ['WATER'], ['WATER'], ['NORTH'], ['CARE'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['WEST'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FEED'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 1], [], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['EAST'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['FEED'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['DROP'], ['WATER']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['SOUTH'], ['CARE'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 15]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['EAST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WEST']], 'market': [[]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 4], ['FEED'], ['DROP'], ['EAST'], ['EAST'], ['DROP'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'MELON', 6], [], ['BUY_PRODUCT', 'WHEAT', 13]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['CARE'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['DROP'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'MELON', 12], ['BUY_LAND'], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['DROP'], ['EAST'], ['EAST'], ['WEST'], ['WATER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['SOUTH'], ['FEED'], ['NORTH'], ['NORTH'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['DROP'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['EAST'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['FEED'], ['NORTH'], ['DROP'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MELON', 6], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['CARE'], ['NORTH'], ['PICKUP', 'COW', 1], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['PLANT', 'STRAWBERRY'], ['FEED'], ['SOUTH'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['WATER'], ['EAST'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['WATER'], ['CARE'], ['WATER'], ['WEST'], ['WATER'], ['FEED'], ['WEST'], ['BUILD_PASTURE'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['SOUTH'], ['CARE'], ['PLANT', 'WHEAT'], ['PLACE', 'COW', 1], ['FERTILIZE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['PLANT', 'STRAWBERRY'], ['FEED'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WATER'], ['CARE'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['COLLECT_FERTILIZER'], ['PASS'], ['COLLECT_FERTILIZER'], ['PASS'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_PRODUCT', 'WHEAT', 11]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['FEED'], ['FEED'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['SOUTH'], ['CARE'], ['DROP'], ['CARE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['FEED'], ['FEED'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['CARE'], ['CARE'], ['FEED'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['CARE'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['WATER'], ['FEED'], ['CARE'], ['FEED']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['CARE'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['CARE'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['WEST'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['FEED'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['WATER'], ['FEED'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['CARE'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['EAST'], ['HARVEST'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['SOUTH'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'MILK', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['SOUTH'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['PASS'], ['WEST'], ['EAST'], ['EAST'], ['PASS']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'MELON', 6], ['SELL', 'FERTILIZER', 14], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['WEST'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 5], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['FEED'], ['FEED'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'WHEAT', 4], ['CARE'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['FEED'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['SOUTH'], ['CARE'], ['WATER'], ['CARE']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'TOMATO', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['EAST'], ['FEED'], ['FEED'], ['WEST'], ['WATER'], ['PLANT', 'MELON'], ['SOUTH'], ['WEST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['CARE'], ['HARVEST'], ['EAST'], ['WATER'], ['WEST'], ['FEED'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['NORTH'], ['CARE']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['EAST'], ['HARVEST'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['FEED'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['PLANT', 'TOMATO'], ['WATER'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['HARVEST'], ['EAST'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 6], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['FEED'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['WATER'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['FEED'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['CARE'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['EAST'], ['FEED'], ['EAST'], ['WATER'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['CARE'], ['WATER'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['WEST'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['HARVEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['NORTH']], 'market': [['SELL', 'WHEAT', 14], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['EAST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['EAST']], 'market': [['SELL', 'WHEAT', 18], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'MILK', 9]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['EAST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WATER'], ['NORTH'], ['EAST'], ['EAST'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PASS'], ['EAST'], ['WATER'], ['PASS'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['EAST'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 13], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['WEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['FEED'], ['FEED'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['CARE'], ['CARE'], ['EAST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['DROP'], ['DROP'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['CARE'], ['DROP'], ['CARE']], 'market': [['SELL', 'MILK', 9]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FEED'], ['FEED'], ['FEED'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['CARE'], ['CARE'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['FEED'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['HARVEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['CARE'], ['FEED'], ['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 7]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['WATER'], ['FEED'], ['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['HARVEST'], ['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['EAST'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['FERTILIZE'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'WHEAT', 13], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['EAST'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PASS'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['HARVEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 5], ['WEST'], ['EAST'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['FEED'], ['FEED'], ['NORTH'], ['WEST'], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 4]]}, {'farmer': ['DROP'], 'hands': [['FEED'], ['CARE'], ['CARE'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH'], ['FEED'], ['CARE'], ['FEED']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['EAST'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['FEED'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['DROP'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['CARE'], ['CARE'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['FEED'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['SOUTH'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['FEED'], ['NORTH'], ['WATER'], ['FEED'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['EAST'], ['CARE'], ['FERTILIZE'], ['WEST'], ['CARE'], ['WEST'], ['NORTH'], ['NORTH'], ['CARE'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['FEED'], ['EAST'], ['EAST'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['WEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['FERTILIZE'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'EGG', 15], ['SELL', 'WHEAT', 13]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WEST'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['WEST'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 11]]}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['FEED'], ['FEED'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 3], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['FEED'], ['EAST'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WATER'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['FEED'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['FEED'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['CARE'], ['NORTH'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['HARVEST'], ['WEST'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['DROP'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['NORTH'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['DROP'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 8], ['SELL', 'WHEAT', 19], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'MILK', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'EGG', 10]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['PASS'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'MILK', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['PASS'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WEST'], ['EAST'], ['HARVEST'], ['PICKUP', 'FERTILIZER', 5], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['FEED'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['DROP'], ['SOUTH'], ['HARVEST'], ['WEST'], ['NORTH'], ['FEED'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['FEED']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['NORTH'], ['FEED'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['CARE'], ['EAST'], ['SOUTH'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['CARE'], ['WEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['SOUTH'], ['EAST'], ['CARE'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['CARE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['EAST'], ['DROP'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['EAST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['FERTILIZE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 19]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['EAST'], ['NORTH'], ['DIG'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['HARVEST'], ['EAST'], ['DIG'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['PASS'], ['SOUTH'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 6], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 7], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['FEED'], ['EAST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['DROP'], ['NORTH'], ['NORTH'], ['EAST'], ['PICKUP', 'FERTILIZER', 3]], 'market': [['SELL', 'MILK', 3], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST'], ['HARVEST'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'WHEAT', 6], ['BUY_SEED', 'TOMATO', 2]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['FEED'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['CARE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['WEST'], ['DROP'], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['FEED']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['HARVEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['FEED'], ['WATER'], ['HARVEST'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['CARE'], ['EAST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['DROP'], ['WEST'], ['DROP'], ['SOUTH'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WEST'], ['NORTH'], ['EAST'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 18], ['SELL', 'MILK', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['FEED'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['DROP'], ['WEST'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH'], ['PLANT', 'TOMATO'], ['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'TOMATO'], ['FERTILIZE'], ['SOUTH']], 'market': [['SELL', 'MILK', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'EGG', 12]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['FEED'], ['WATER'], ['WEST'], ['PASS'], ['PASS'], ['HARVEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 10], ['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 6], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PASS'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['WEST'], ['EAST'], ['HARVEST'], ['PICKUP', 'FERTILIZER', 5], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 6], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['WATER'], ['FEED'], ['WATER'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['EAST'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['NORTH'], ['CARE'], ['EAST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['FEED'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['FEED'], ['NORTH'], ['CARE'], ['EAST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['FERTILIZE'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['CARE'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['DIG'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WEST'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['WEST']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['WATER'], ['EAST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['PASS'], ['WEST'], ['HARVEST'], ['WEST'], ['PASS'], ['PASS'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'MELON', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['FEED'], ['SOUTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 4], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['EAST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['SOUTH'], ['EAST'], ['FEED'], ['NORTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['DROP'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['WATER'], ['CARE'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['PLACE', 'MILK', 3]], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['CARE'], ['FERTILIZE'], ['WEST'], ['EAST'], ['WEST'], ['HARVEST'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FERTILIZE'], ['FEED'], ['SOUTH'], ['NORTH'], ['DROP'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['CARE'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['CARE'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 26], ['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['EAST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['DROP'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FEED'], ['NORTH']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['DROP'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WATER'], ['SOUTH'], ['CARE'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['EAST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 8], ['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['DIG'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['FEED'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['DIG'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['CARE'], ['EAST'], ['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['DROP'], ['FERTILIZE'], ['EAST']], 'market': [['SELL', 'WHEAT', 11]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['EAST'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['DIG'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'EGG', 8], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['WATER'], ['WEST'], ['PASS'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 5], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WEST'], ['EAST'], ['HARVEST'], ['PICKUP', 'FERTILIZER', 3], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['WEST']], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['FEED'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['FEED'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['CARE'], ['SOUTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['FEED'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 11], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['HARVEST'], ['CARE'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FERTILIZE'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['DIG'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['FERTILIZE'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['DIG']], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['EAST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['DIG'], ['HARVEST'], ['WEST'], ['WATER'], ['EAST']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['HARVEST'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['FERTILIZE'], ['WEST'], ['WATER'], ['PASS'], ['PASS'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'TOMATO', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 7], ['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['FEED'], ['NORTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['CARE'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['PLACE', 'MILK', 2]], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['CARE'], ['EAST'], ['WEST'], ['EAST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['DIG'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['FEED'], ['SOUTH'], ['NORTH'], ['DROP'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 13], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['DIG'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['EAST'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WEST'], ['CARE'], ['FERTILIZE'], ['WEST'], ['WEST'], ['SOUTH'], ['DIG'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['DROP'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['DIG'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['DROP'], ['EAST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 8], ['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['FEED'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['DIG'], ['WATER'], ['WATER'], ['HARVEST'], ['CARE'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['EAST'], ['EAST'], ['NORTH'], ['WEST'], ['WATER'], ['DIG'], ['NORTH'], ['EAST'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['FEED'], ['FEED'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 16], ['SELL', 'EGG', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['HARVEST'], ['WATER'], ['HARVEST'], ['CARE'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['DIG'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['DIG'], ['EAST'], ['WATER'], ['DIG'], ['EAST'], ['WATER'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'TOMATO', 3]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['HARVEST']], 'market': [['SELL', 'MELON', 3], ['SELL', 'WOOL', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WEST'], ['EAST'], ['HARVEST'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['WEST']], 'market': [['SELL', 'FERTILIZER', 10], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['FEED'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WEST'], ['EAST'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['DIG'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['FEED'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['FEED'], ['SOUTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['CARE'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['EAST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WEST'], ['EAST'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['FERTILIZE'], ['DIG'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['DIG'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['HARVEST'], ['WATER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['HARVEST'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['DROP'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['FEED'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['SOUTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['HARVEST'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['DIG'], ['EAST'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'MILK', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'EGG', 10], ['SELL', 'TOMATO', 2], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['WATER'], ['WATER'], ['PASS'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'MELON', 4], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 5], ['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['FEED'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['DROP'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'FERTILIZER', 1], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['DIG'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['WEST'], ['CARE'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['HARVEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['FEED'], ['EAST'], ['WEST'], ['WATER'], ['DIG'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 12], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['DIG'], ['WATER'], ['WEST'], ['HARVEST'], ['DIG'], ['WATER'], ['HARVEST'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['DIG'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['DIG'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['DROP']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['EAST'], ['DIG'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['DIG'], ['EAST']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['HARVEST'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['FERTILIZE'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['PASS'], ['WATER'], ['FERTILIZE'], ['PASS'], ['WATER'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'MILK', 1], ['SELL', 'WOOL', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'EGG', 6], ['SELL', 'TOMATO', 2]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['EAST'], ['WATER'], ['PASS'], ['WATER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['PASS'], ['PASS'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'MELON', 2], ['SELL', 'STRAWBERRY', 1], ['SELL', 'WOOL', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'WHEAT', 34], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WEST'], ['EAST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 4], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['FEED'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['CARE'], ['HARVEST'], ['DROP'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['DIG'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['PASS'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['SOUTH'], ['EAST'], ['NORTH'], ['WATER'], ['DIG'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 9], ['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['FEED'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['DIG'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['CARE'], ['WEST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['HARVEST'], ['DIG'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['DIG'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['EAST'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['EAST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['WATER'], ['PASS'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'WHEAT', 33], ['SELL', 'MILK', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST'], ['DROP'], ['NORTH'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FEED'], ['EAST'], ['WEST'], ['WATER'], ['DIG'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['SOUTH'], ['CARE'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['DIG'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['CARE'], ['EAST'], ['WEST'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['FEED'], ['CARE'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['EAST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 9], ['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'CARROT'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['FERTILIZE'], ['PLANT', 'CARROT']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['PLANT', 'CARROT'], ['NORTH'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'CARROT'], ['DROP'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['PICKUP', 'WHEAT', 1], ['EAST'], ['FERTILIZE'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['FEED'], ['EAST'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['CARE'], ['EAST'], ['EAST'], ['WATER'], ['WEST']], 'market': [['SELL', 'WHEAT', 9]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['EAST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['FEED'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PLANT', 'CARROT'], ['NORTH'], ['PASS'], ['DROP'], ['EAST'], ['WATER'], ['WEST'], ['CARE'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['DROP'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 14]]}, {'farmer': ['PASS'], 'hands': [['HARVEST'], ['EAST'], ['PASS'], ['PASS'], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['PASS'], ['PASS'], ['EAST'], ['PASS']], 'market': [['SELL', 'EGG', 10], ['SELL', 'WHEAT', 4], ['SELL', 'MILK', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'WHEAT', 28], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 3], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['NORTH'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 4], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['EAST'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 1], ['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['SOUTH'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['FEED'], ['FERTILIZE'], ['FERTILIZE'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['FEED'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['EAST']], 'market': [['SELL', 'WHEAT', 3]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['EAST'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['HARVEST'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['EAST'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['PASS'], ['WATER'], ['SOUTH'], ['DROP'], ['WEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 4], ['SELL', 'TOMATO', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['DROP'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['WEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'WOOL', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['EAST'], ['SOUTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['PASS'], 'hands': [['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'WHEAT', 37], ['SELL', 'MILK', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2], ['SELL', 'WOOL', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['DROP'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['EAST'], ['WEST']], 'market': [['SELL', 'WHEAT', 11]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['DROP'], ['DROP'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 1], ['WEST'], ['FEED'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['CARE'], ['WATER'], ['NORTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['FEED'], ['HARVEST'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'WHEAT', 21]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['CARE'], ['WEST'], ['EAST'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['EAST'], ['WEST'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['DROP'], ['HARVEST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'EGG', 8], ['SELL', 'TOMATO', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['EAST'], ['FERTILIZE'], ['FERTILIZE'], ['WEST'], ['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 1], ['SOUTH'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 4]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['SOUTH'], ['DROP']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['DROP'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['FEED'], ['NORTH'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 27], ['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['PASS'], ['SOUTH'], ['NORTH'], ['WATER'], ['CARE'], ['WEST'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'WHEAT', 6], ['SELL', 'CARROT', 4], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['PASS'], ['SOUTH'], ['NORTH'], ['PASS'], ['PASS'], ['HARVEST'], ['FEED'], ['PASS'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WHEAT', 33], ['SELL', 'MILK', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 3], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['HARVEST'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 12]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['EAST'], ['WEST'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['EAST'], ['HARVEST'], ['EAST'], ['WATER'], ['WEST'], ['HARVEST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['EAST'], ['DROP']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['HARVEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'TOMATO', 5], ['SELL', 'WHEAT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['SOUTH'], ['DROP'], ['HARVEST'], ['EAST'], ['DROP'], ['NORTH'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['DROP'], ['NORTH'], ['EAST'], ['SOUTH'], ['EAST'], ['EAST']], 'market': [['SELL', 'WHEAT', 23], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['SOUTH'], ['DROP'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['EAST'], ['DROP']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['WEST'], ['DROP'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 7], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['DROP'], ['EAST'], ['WEST'], ['SOUTH'], ['DROP']], 'market': [['SELL', 'EGG', 3], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['WEST'], ['DROP'], ['WEST'], ['EAST'], ['EAST'], ['DROP'], ['DROP'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'EGG', 1], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['DROP'], ['PASS'], ['DROP'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PASS'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 1], ['SELL', 'WOOL', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['NORTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'CARROT', 26], ['SELL', 'WHEAT', 24], ['SELL', 'TOMATO', 4], ['SELL', 'EGG', 3], ['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2], ['SELL', 'FERTILIZER', 2]]}]
_PROXY=make_agent({0:_DEMO})
def demonstrated_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
demonstrated_proxy.telemetry=_PROXY.chassis.diagnostics
agent=demonstrated_proxy
