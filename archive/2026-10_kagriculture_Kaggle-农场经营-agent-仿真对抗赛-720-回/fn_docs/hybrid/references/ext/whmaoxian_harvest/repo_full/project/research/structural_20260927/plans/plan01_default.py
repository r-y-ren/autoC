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

# Standalone observation-guarded reconstruction of a public production plan.
import base64,json,zlib
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rlKO^;+rj@*B#a~<-1#7F8@)15nA*qW(Ee{5nkXbc9>3Ic@HVWpd}|6Mhe84)iYjYcEgUqn`qPMsYY85NICr_)KJ*<b$eyZ`>T|M>TR`;T}3<uC7k{P6S7?|ys#?tlF4fBm=r{pE!(KmPmQ{^NiC+yD9U^IzWm;n#ot>yJNu{{GkRetGx)-SZDmAHMu|`tAK+-u>|Lr>A%74}brdpP!z-Uwy`(KY#ww`Tcx)`NN+-{^`S~FTeQtho`3>-@PAx`|Us9Up>Ib@BaDMAD3^qJj`F-JwN^Y%e$9<>!)9SSpD>eUq62O{;yvw@XN2SU-aee%m)AT^wTdNKYjeKPd|PAr&bSf{<hzJet!MEeYWUj=|jf9zx?ylr%$Vwf^Vyt^wWp$o;-`5?S1)nU<nqMfAui*Hr3FReX{j4zgp){PoF;j`SlxITZftVyoRrTvi!G4&r_HG6nc4O)RWtB=LFV$`fxJj>UY9c9i^uu4}~}Xl{w5?2L7A1)5dnP`_$XHSGM#vv$O5!w}l%?jS7k#=BvM2FPUeoFFW<mznqutdY`^-;>9*K+ZyfCI0X6+F*RF;n<2FdD^opx_~py%S0-A!3U{p4udXfRE?BVb{D7vI5Jb53OY!bPC!=+qpFjUfwpF-LeARa(TnC3)5c2wLq^n<{S1y+O?gI`{*Y*O>$}KcX#&teJGhAEP2HWfO5<ck8S;4idN!x0cf<x#~uKB@X7zOmqK0Eo(%O5+huy`Eq`&4|XM4qHMQripo&C*+zhGJ$Jqk|(%dDOr=I^HH)YpU%f;4`NLarwPo|1z{xL)ZzdmJW9I?0$J>lsW^${L|mpbrEgCy;IBn!W+jZMw}?}H|-_gTikfW>^1fB;`2|JuW?>C!DT1$)<ryr#pClS{&M+}Zd%SVojw#S)8*eo=J1v-+{snPq6?Ngz0{y%zp8L?Y7QQYT=x8Y=UevrrIu&NK3>L&E)Q|}X_YjbUy*`8s4s~IwtjQA=EZF;WsJyw^i;X=hjJ=+@sYE|FN?6warxt{{;|`?1PgsJ=IP%DXWi<fzx({@)6;jq{B?1dxpm*tzI-Y7I<>^*5&HNDBJu{O^i};isASn6;N!3=-euFR^00wE++6;Kn*Z{3cYaTvW{RIi{?6*nbp1##$Mf<?HIa{aRnJV89SHuS>h2xKhjT2TNsD$#9{JbiX>Ybh8dMa%|LLn47f<^7itDl@-fE6E<x01$51h{jtmCg1UAMwWF0_09@uQej3ET;1KX32zbH}I0AvW}0ewcns@6^9Dg{1SEzgns(+WEzdqrZv|DR)qBZR;av#y((juBMv&z{}H_i%INB`Zd){pm3P4wobH4P`a#cp9{1)m;XYXGEa$IXxFwXuLTK|W|*c)vS<<nh<)j}@YnSiFU&cXT*@$EWS#BT+(q9!bE8PK_v~6-qQg0FczILuiRMxbbIhjUAgad&h}ns;?bqOasZSK9D~nnM+Wx|3n)Q~?B-iDIBQfe*uO9t%5zz))6{^|8?)XEM`!f%Pd!&7$#bUl5Qm=peaz3%7B=BGT`I;Z%9MYv^O8Jt-8lhHI7wRdtIAoVceYjvJ71k+N5(w{vYg~dBMEo3ZZSEC35|w-GIoYG~=D{gLizr_(s+pCrYaDsit7wbymVf;G`RAt%ieKERx<3=NKCSr#-=D7uEDPvm7<;0vyRqRvH{IML$W<${YTB5?&7Y3#RIqN@<r;6lTnx5%&LPi#{T}w7SUYml^(tV3EuH}^7dzta`9K=T^6ZG~xbbZ*P~eAjwK8`5;loe=;+*N&baBKxf3+8s;&-2&1xaL6BE}#tbS-V@7@-Z)l(D@%;#}}&t;aW~Tn<I<^-rC?$Hm}_Z?as4bDe1U;w2qFzuM{hq+m}g6z<u-*H8)e-S!!{@<iS&z-+Af&~CW;?edB5@ffH%b9TkEZ`dD%+w~2<^2MZQm$5&zf8{ce=5mEMKPU~qp5KmCwCs0E)G+&)ZWXG+`bK(wQR`rKD+jwbQ1N0PK$G*6BX;>Oz1ZlwRIUtcRtL1VTIV4m%z<<#3`%CHwwdjKFNRORcWkyb8A)yF4cKRNEW8fGrR-FC+<a$Po&d)6&9M)P)y{3%W^u+zT0yQV+GP2L*)yQtxLlwz?G)|mHm#4ZO&e^I5`Y%m&FVm}p?SgD9~<0sE|mdW23aS`64+zNOp3{|Ah+Wa%kG}>kq1j%PBw@dY&!}=LW_0Ti#R0RvDD}U7P}hYGE07r$MeD9c>_$H6KE(ah>+!W06IWftvv6+`(8i)^3#XsKRo^P)4#ei2j$sRTH8x(KLDmQgV4NYo;V)Y;5uff;IYeaVw==ocJ*c5*LQcnx)VL@UIbf|=a*vyV%XpX18KG-keTj&5WC$|+ZgFk8XmGY_VZI~li9MP?;U7W&G$PTv9>m~g3_~9Jr=&+NFH}6$Nr>OFi<t1F*yGagO#T2AdC9vV^gJt6fW$-Q}Clc{yle~h)K+oT2v|s*>Qbh>PW+p%dfl{mX;~Zvcs?);uScZGOXnD9dp3Gh0-BcD6LjF{W{_M4#R=HW>tC)2#U4DD*MNftDz<*0fsvaBSyv9=Gr)Ce5>p{C9I%iTlN<50V^~)`5I{Ih|oS)fK-Pydy~bqV-$gHlG7S3EM~TE!77F4#31iNnU+hUtTyM->p|Uy%@}}u7PQ*qf_Uk4k?b@lxFFU=ZC(RMr|Q~Q!j+#nQJ+2)BUJX1<F<)nGBO2%_=q61IUOSB&FKF6MHbp~WCh-{{i2#sP-V|0ZPi-{c}n`cerHXcy`A#uKN-PJ@ru^5N(%87faXEkhzy<5P^x@BHjJ|8`Ooq*z1FQj-nXhc#-+uOW}?D(F_EctuY9HYWCGW-ZbxuWTr-G)l1Mmh#~v`#WmCo#)j{NS7Xrd(&$-?y)wya;T_d#AnZp3A(C>o4c>?@GY2ttb8G>bvF)US!e>zzX9UaHd9cf-=ypnvAB}z7@*^XNkRcZVhGN;p=I3$l%E)wcO5EBhTxO?4{9Op4w`#gCC<7nE5@)eXjF58XelZyW&=zIVdOsz1V2zF`;GPf}QQ0h6r30MVUr0l!P_+jeJiHQ!v+hKnImJ)Cd`^}zn*0Xak%#KejL!a#ZKEWHgodu@EP>3DRCgjl)YvP-H&ddb)CSdom%<D*r5yxc7K2?v}?#(S#DTe1SSNiW}mp*ik`A#7ij_q2@_V;t5;-_BkK&q7MgDC*;P6PSUg+|O7=R!~cbz588mm%);Cm-fCT%~Fi5JVh50FXV26{VL0$YkVsv@u}w(mJK7x~y8EIV4*?>m0T|<N!t+>{^RAr_@2PU1mSTq_cfm9KfyYeD|eijQ7}Ew{1-`DX#u7ti?JgZ`DG(Rnjw7lOAD`4{)2p;y;b>T2Q<H*6tPu;^9Fs4QU4lU!3?`35*-;bVa2F)O108Tw{gTrX6>0)+cv*H3k-kF@cH29jn>dw`jux$;VZF3hi<`reu-B8BVL;uUoPWZl{~v>(xKJ8K2@Qg7Xgw;qX7U3xag}^aED0dupT+d6PEeh>Eb*ec8u$03@Lwxqs`&L;^2jjdbxVwFwe;XukoAg?6!>FraD`Ly+ExDW*&fL3bX~H(dSjP1`8LUhWM(_27DXgO&hUeb|UewcD~|RSMxVtT8ZB!{q$T=g*%OYxyOde&4El7!C1XV_-V=kCxXmrdr55FBO4MvXJ0=TJFEq@kK@yQ*5yf+TaO|nFf%uSe*Ilqhn54sM>X7v^9oG0<`8Bap(13!#W)y#%UdX!LFL3-z8Csz5^Uk^bR3Btnr61{GLV}-aRQjp96;-<|a;4*TIqYq(aEpGT1rxS&L^YCWGq5$ft=I$;vYRaXvms2s>rUM1Xo<*VH>SW?cg3_$+D<<8uL7I*RIA+LVN_(a%r5s-obbque%6&w6o;|I;7;sG1?IwiFohG2ZQNt$uWZr)ae3ox+}<I6VyPWQDT;%SBPWRvUmxw)nK&4xAZ<RAlNTh(iT8T--UP7-+}{1Mq{52o~`{PyT3zBOL_B%A7@IGWgncrK^vHg<F6KpoIyyG9p_|?E2*cB^ABWjA2ursxcv-;!y+PO^r|z`K^5MgC4A%43ZcG%PHfFHV~37od<PQ)iql7wn%K7<XOQEmbe6^>l%QZ@X5tQ>WBN9mZ?cd9LR;I0kd-(pi;@(p^vSG{hZSq9YI!+VnyH8B+orZZd%~L66$V6c0E>YT*-5Ir7cO~B)IX74bqJD(j=OKqdGSv**-D95dp6RLQLPG=`(vMu}WpcIzaA>ez|fl&>bbs8^xdM5w1*;ZTp$P1YAcZoDyp@N<UdH8huFR0D#58oeZY9tV!H)PpJyU<>63s0Qo~$*ZG1qg>CeyF=ogSV|hI|#-tHZfB|R(nD|Ub&s2LOF}hk9^fM0FKJ7P`#X4Ls+gAn@hWM*ag_B<3sO>YjrpR%`LO-qWG5Lx!wb4Sx)5(YuNFRf2Be5H^?8L3y)50)Yg!Zp8qiR_86)|}uWqXB^#hzOh#S3Ky6CRROdTAnUo|`heuy+|1Pc)^5<umP4gjsDAKixJKONv37Cp6%>R;8i(#9wo4xjA`txUgoQW+fBg;MPF)G7n>UY5sCvn<41xn73w~bxN=>CFc1d=n6PydRT7aZNn;ort%l2e!r$DqIi_oB`Q^oh-!JpY{4$^{SEL)UEVCeur8yY>%%|)@bvU!nJ~g)<<Fld5-52chPfp_o{6kay8pw;O2I?{5ude)p>&l@9ve-~HrI}U1gEL(1E8Ez9E%)TJPy#d4I~lzEtPpifqdWMCUPq4{(z8ejMc!JZHf`;ME{Tyfd->JuL;I7T1i|?ZQb=e963RQ%c8R|gLCgEW2!8+|78niZ}`zj)zB(?+54tAyEkN}-J&35r%S}?%RAVYajyX(z0BMU#amHwnAH#$@19k^0b5~&{nAj2`R~zKES@%>RcS99&y4Jgl9BW%F7HB3$#i*DLnuHlfm$^g0Tlr2%|^A=S#S2$>&SaywkM{J>sxuBHP`sl$4~$406JcNHF5-ze@)oM^F{#cuTMS&`1QO)y*w|Wv`5H)^7gB_g4YknuVe^+9mU$fhl8;r+kB<uQ^M-FLtv?ywS(`MN9U@(<Fhf=R<k^<1j-4g?UR@u0(m-B9k+)!aCqX-k5$k=nR*v2bJ{brtU#n{F&`6M9FTFt;N9ZRaxUefYWK#YcFt6tfWzZTa_3oDk%k{6yC7<_Qy(EaUK5E|2YrO_PtAmjL(1!x=wk@VDS0tsvKLQ*t{?+I1$&;IHV6Uj(l619c7B#?&LWo%am@8G$d|iV2m`l&LWA@Q_Y|(hA!SktBcBjwo$3T{VGO32WfViu5T^^3OBt5><j@);&|Tu}z8MWpBn@bTCqfMZM^uBsK~P46V?jRtDWj9}*u?8jb}5Lh_Dz(lF^ia|1B9w2gI;oai#tj0n87so-sS9WD$k>C;C;$5$%THWxFfx}+A<P&E(Cr?KhgcJ?%JYp+N-d;GWUtQv4TUE{SK(iXLoJx048p>4+;Unq^}70{NSq4(fpE1OG@nhg=6==j%o8jYbxfG6sFI~0$X?SAf6aw*{>c-A&%A}tOX(CtesJ7Jzvw-a*o|jw(TcNLT)sIdQ`ADVpX;CswC6sFf%%m;+8I8W`=GSCzB;7q*Gw&%lNHM@*w}i4IhP~(XbtW5Nc6%V(W85>tx()&SpJw84*oVdNh~?45DnmGVkEko`1Ll`=EzpKxN*baffC(J)Dg~EHxNDxXIdm{T51g;_)VB%R7f`(Y@p7ku@n6@J5%X^4vwpfe_%>=XfG1RLbRZ2jNQ4`kUPsYhOQxm(P%h3B6TCJ7CU$SCYh*k>w%rdB@Du<RRBY1sHNb(1?<=4(@&R{IiJHm!QvM38*>iP!rO<0|k8K)JSqOqzrt*OkrzoD4Ew!z0e2v*F2q`$AKWI(gH`d7u$;=uJqhRrVPf!7}{DmtTYpjITNbP3qmz}ZAH`&1d)SRZiwJ=v%FqebGlWmx_C)O+Le+XBSgU?8;7o5pE`5O4h4X`X1zmR3KKYPG#$#Y>EI@r_u)eiWyCu12kCW2q_)iCB3^BapU5hyAN2A-=V|?r_zv)2Md&G)cy+}|hH8~oZ@efcR*10qf%njQnB~cBn=oE61VC9B&McEwg6KIJpls1A;w3(gWhv`0Y&Y7Tse<38lM*{GmczZpAX{#+KB`>39b?QHv>@qLP<Tpq8tD#?O|t(G^$R47(DXg<q~$(*i#vmjJEJVy7P85l4<SKoXscv+JP;6r(fy#3gf{=R??y%3b1A{#ldUaKBF)uU-VN<gX)X%8o|4W<UXo{d+1My-1|tEW0IgJ9m|iup?A7NR-7Pkxnf{;cb7EU*W;kTKcrv&v0>y<RUeS%Ns?>upo^49o2iQ`obwD$$#{16Gpf_k9>Ut@erXm|_^b!94c*C3^N*rb~)D(i6Q-U7~Wc1wTu!;%5O8)F@FguwP_-Ly|j!l7A(L0Az9k9~@E@miw38Ro0rdkEte3GNE2N$txr6w^C$!019!&nj(HlxSqc+gLLmXD4w%sGjqa6R}4nfJa#Vg6zh$gT*xNNk?GFpTF;H*5ZV#FM;Quh3`xdYv0lHG<~Ue2KmLtd$mE8Ye6cK_k6B(Ls_&z0kcmhM5FZW^h>;?Wc~3QS~S>ME9%UHDu*rviEhoh!8u^0*l@-3r)}EBwpgJ!CY~$0P4K@lb>**2)wi~!+vuG5|WAeHuL!Wkp1jDu-f{Y*dQ!Q6Ln7ea8eRXu@h`4-xGuo?qsB$M!aAs5w(L8?UqT;nP0zTh0=_xW&$KFzmu?4fxVtM>JZECboVqt=^P7^xP*x<u9>v2UkPo&kme+|`uqBTFDOX1BiI%3v<O3L5ddf8BCu$-T?RFnQqGAJCe@!XQJxaVfNtegm%`EzEZ0S_{k~qFjqmXZ%;F#{!1xgI;fnMbua8lknrDz|jMeTm$VWkP#}cr5?|qV=#)@NDI*EkTwG}T?eCS8Z+Ov^g$tM$<)CMr0=??KLC7bern1RBmz)o<Mqma?>D-p&Qzz%4o2ceJ-W-3S}g|y<yco7X1@j<w_TC$@~V5o|kF!B~jfOwG`vo5Ew|HBBM(sj5TP15`XV%b_$Me<k8_`2r$cRD^di^)(*AiH1E727?dP4i@!X~5<z>dT})Q9QJ9ghy-9sR7U3>ZOzcVYM#!8_?%WW(~VAqXX6>EYTzi^Qxe&-LkBCm#mNOVK~g*<M&ckW?z}1n=`b$*ZH%he}-U;<)5H@1Px?V(q#}|;~22q*@V(EU2b2mOkCk+0N<sFEEhCG1gBNn_so1TA&@`G;vavbvL3KPtLJSOkW29(i<kz&%Vb&)TIO`29*@j^F{pQ=e2~_%J9uLF_P`Uzn2i&S028Wi(&#gL?ol2p8@$4<*s2EmZ|3{9fppz5v&CcR=wA)xTvs*>ZuyB{4~2PDg|*F_?qk9?(6Q~k%rC*044%JYjseTBAIf6f#UlxnkB;3BS%2r<5nj+qg8KjzTBohnuqe3_u@BU!5M6320O5Jhl3U2>aD5S}6d%RtdsP!>mN--tHje~rlfavr5J87gM13h{RE_mB&e#J37HF5z0Zf5g4099#H=Z>Hk_hHpE$^z+loch1>sv|ywV0xYgES-+##k~>;dUk^{Y<~Way2fCEf-uGP8ZxfXYG|V#l<DBnrf_8Yi^~Db2+=1-crFt9I!4!;G~mhzzZQf2VPnOff~TIb@S3kmWhAyN>ax;q47?%SO&G3uCe*rri&y$p#j*Lfp&tA?8;Ip@=Z#=(E`I*ZBNFH*JV=5)QQ97Xkp5#Ff_oed8Ii;r4Sb{S;S-brs((x0v}a@9;MvfzjtXjvQZNH5KIkfnt~is1ndnZzsepxYsF>}Zl_?G#!TIRj8QTY!#w#Fg!^)JlziVcaaG!7IRSU+YW_hA^I^+7q^TAJXb_hJS-!^h>e$8GGosg{GT|2x-bJMsIJ^NXE}6-WZJb;)=9CWlVeCHWL%Be%a-m$jCU91+3ochhTQ^HKvg2uU^&kzak^BDq2#T&nFLSo4GPS=H_q6$F8?qJy$0a76ci*TDK~)M|WdZkJ$Uz5+u3duY9c@=KCm3k67#6Ns14e^>$2M%`FOPl?1`E9(x?9=9#@^b-6$bU==572_?)*X(yehS|HT1`jO<m~Xk0G=1a+!||)32lu3>NLwnYn$l?fE&@b;OtSsErYbPs_cFJ-J_?K8-@xT`ArvjiQH4A=FkxLDT{ss|!=BCcXj<x#L#`$71({e~XzCIQ2tcB(!a9+887^GM)Mep2HxiP{foz4A}JP2D_0=mdve>i!y=U5QEo%z5;RHfdPw?;MToupwR|`b`miwxRGY0-A$3|(rk*`em+1#-v+h;kspH@gF!Y6AiX*p>$0B+mVuym!gX}T&=>S*FdkdbWRI|gB!xh3rP6o{x@Or)x?zL<m_#a>KnIBNY7(dHlyUJXJzFpq2Gsq^)#x1B8u^+Ne-N4o4kBRUt!JsIOP~l`c{#*kDJ~r17>_mmjJ*(h7&L*j9k7(?a$P`KNJhu8r?TVVTEbn@9-eFESsSb=QJmaSzU+mXS`@7|x+8>B9gSII+!uzDg7Oy?H)bN*t-$5LmdA8gN6Qzdhe|>}2n{sb(18<mmYtX%pQ~6=9tPc|ctJ~GoILZ+p%{x<m}RsH@Vs-0FBn!izAaw&&9pRb7k^M%c4veG|B2}a01Jy1es%5~l2N$##95~SnxqS&N;9XTD^h`(fk7hB4)$mh-IGAbNr@3DGzh7Qj1eV8*e(u%>&mPHgF(tyA?d_iwW~DwC@pJXW)r|6hFM4?SWwQ#wQ1m9-~&Et4>}~j6#><=%WM(ySL`#HGAtboO&QRT8CYjt%YfL<MG|C^jfx68VSs&-7(;Zi(K*$8fPH^_%L4@{dO&hCVOC{(SEw|F?~7?kiSr*hKTpQw$b6XB0!AFjD@S0Sd5inw{oYH`*zz&W>^CJCH5IyN&c%8LEHkg>YGhZaS<UbVAxi|-N7(ubX@(|Us-wP>5bt=rAu7zGHT8<M+KR}u8CiPxR4zJ+qsr$2{&xO`1!(=-B5s&(L)>t+VyH2Q7?+QbMo6s-YwZ{ONh^Fv4_HVGYeU%kU8T~vOP-!#Q93GvPQAhMt+`2=nIS{Cx}C<|P=eg}bsxEovrBgUW(`55RZ@qsh#v+vP0#{W7>0Vb3j>6@GUus*Bw`W*;nJO9b)Y>Hr(hiy_7dY`bB+6Z;+!OT*ocfL+>wyAOVmGj)dStYsoX@O>KBlcL?azqReMf`DYvzj6e$Doh;#U26sFils6Z1!xfz!act|6qf~!d|Jvr*shzzC1O)d2h?3*HP%CHPa=Sj3^Z3)`63GQK6J%4AZucKh7t_xMs<(rOOl8UxR4IE$lQnl#4#!;E25Ijw=O6MzKWCnU1q{4)tIB;Mkh~w<Ay^i5psxutZU_ws3GV94aIY)yTRWfWXvk5mk_>j@93;SM!f=Zblr1ra4rb!&GSq=hrec~M<Hnat3NpjkkN*c;5Q9&hrPbcHAnTt{ru1^ZI1iYWsVwpPAg#<`TrFA9}TAaD6P?H$%!K57gqy>&xtPTU0gk>61BrQ%9(i-YxP)i`R%~42^;F1`04ItbO{)Qp}#ZfY)xu{Sy$D9r$=h2CPLX$wS!<t*c02v@IQb+>GqXyNgh%aQ9EXd9Q{jzqi)B*wF#@B!z5=vE@4^6Nd?V11seEcjwo|hxczv#Z03=PBylor?cT->1!rRF_1A~bZ(gS^7^UJ**N)TBxS@kyKu=XAU<)_0(VND-j<?>jbVsXHu{Ixj4t?F&abp3CuOUx_y|!@hS&Zc1Nr>GBxK2S^dkx;?xFk@DPFr$AtqHG%i*l&eJWr_gMiEoM#U)r&+nsLEcK`L&cJIq2{fsm`<!Uc2j)yyQ`*%xZbS>4Pjq)FHLmy;T_B6!pm)VCVq%dEp3#J!=)D;f`D}Q~;0`ozpo9)E*o~0Hy%eEP*l3xC_q9p@T6X-Y{Ykcj-(C8aURBofE)%w|J7D$d7#-+FH>jLx)X-(r@m9rpY?ISQk;@bLJI#m6ga(D2qFY5a+#NPWC>Rsh|u!>2DpSslE()d9Fk2T)B%VGlFq_1Fx>#?DGn}VYMj8t8xs5k>~?u;9!HuAqhGa3CqeN%}Er6P>s{tmVm0nmn6^>H>1*`A^}BP0}uHc%j_Vx<V-{FM<Rt|czusc;I7({U|eDF%SZmCz-q&>p*E?|lxUnVb(wUvCO%4|E!wSR(t$a1xBB25_ZyUWfYOJ6US#3nJ?$HKruNd<(910A#zweHN?fdWAJf#^%0aa0tzOC}6Sjw^UIGZn1|UJzTV<9l9r#<>f6l0((HjXn7riM3JTNIn@x?)~{2VS=-E|>mp=)_-2JZk;6UH2;*T#TUQoF4s;N05ILws0D0wJhxFQp^Vnc3pS!<+MBr!DW`Rehp<lG%Bm((h1w11!}_5B{{3Uv!cmE0gMU0a_2iyL;!X=NG7p=Bw9894$g(4fycekG$CI<IUY!8AGRCU8K6K%=ueu7nwuuZNC;z#?EJ(!%U?S=q~89<8RTVwOnBdcUt+}*`AuPGGKrHeOWUn&1OXzvB%M=)Rmy)H)+Ylp%wK<L0hOG2olck($DO$2J>6+=BXQ##O~W;lJG$a=NBy+?Go19_gJcll?1lf6nlhvBXVPX3|KDnK!zKtj#%>aXi-gdH1h}1H>zj~7~D=}rt(;uJRVfq<PU%T_@@tl|L~uGczXIV*~UK`?EJ^xiy&vPPzp}-U87CjJ3|mcH))@my!Wmxsb;gZB2h5{gs5<R*h!fSvV0;g-(>EDp4N!QJ(wX!Wri!JfduTav0Ndq#6)*bf^<BjZzH}x@kyfqK{GVXn<snYj0zwc1*M%uI?hP$=ss18+)hmlkdKLjf8;u~=yXZSLO{Z60tj=b@mv{8X7U5O713)_9yXwfa0~_DjD$aMgn%NFg^-7w)u<_R?^LD54uJ|g{a+kgun3U1<qyAp{Pg`_zueb<`8C%d1mT7@&BNHuN6$q_=N_4UAp(2#m&?~PB_~5RzC88#q`(@x<o{o(Z#4;5_L((R6ww%;$US+oAsk24N<BNVbzCpsfajcxxC?px_(M(%o*!@;99`dhFOxhrp_M$ey_qdtIy{ARFx>;;z&lDIFvz_`;)#do-X&h2U@1{S(Oj&?f^s6=xL(4m<B)DMH3bn4rEKav=S4jpQk42fCC)ERg<Kw7SA5HBa#prc7OsK|GB*S%K9!%8u|EU|V2bCNQaT<M>@T$$`IU#zqa|H^5?C!p!NXI(CU@2YCtqF_al?Bh=%<sCSE#Sl9CMWWVK(In)Ne-ptrO;bY15Mc16%<V)iFMok(8vbg2Koy`TCS<@+H=Cs-C!@#v8C!A`7AdWFo0NU^nv8jwxyNgD@|*85$L!MFN?1?~3mXedwp9R%mtiad71yrfNxW=j!7q>cdANq=ZHk!R}RUTII-9B7Khip-5a1lzCQg`k<N!AV4@Xv}uo5I0RdU)OO4KNOKpPwvxU8zrU{KWHeO>6ipJA#evHh|1G%pq*2pRTUwHhwZeA_#R3WeU}?_36EQ1tQdr>G8QvJF#)ACy8=%vex1-Z=@1{$Cw$#+4bRiCI3^Ly2ZBuE0Q)IOUwN|T({qWCP0m>6nv5OqlV~PouP-$R9<SKY6tr5lOmh>5#uSnD@({>L99f+jw!?GITe6Zep-aXjaqc|qcTb(tn%u69QW0%o$XB-&kC&gthy*npW0+xcDYAl!=c?ou@#($>BD3e?O_&q0!rDC4RD{A>9YJGE!A0t00Y(W))j>S_z3gry1t}jX!-{m)#IebI~`h;Z}<**{v7h)@s#$1;Ad`>v^kwHt{=(^0}rYz&oq@YNn4sI!y*dHP?V@k-S4x(vcSi`OCq{<ViQAQa=;_O2LXZ9s{<iRB1IwV}OY@s&AU3Bh7)wPQ@fg;<f<FaNE`zBoeq5|TDPm{_pTRwWHgaF?t1f)j+d)OX+5c<RI)f#M4IVOeV-F&W|&3mJv&nNl1i2BEejzm9`lZOZBuO5IIa1KD+jCOl@CdX}r0*l&1Kp=dt5-1LB;8_sCZI}<T4KOOeI(4!;dQl)iyZB1$!eODgY8xMtUU>+wg}B&pUO4Y4RjYYd&%C3SWXj)h8^Z+l%rsehfFSgL<amU+3_Jd6K#QwIct|4j2fZ{xgj@tzWd>P6Z=M%7hW16hO=xojipf!5x@5(N9^D5oyL?>|@X}DoHRrbE1jcc@NkW7HB!awxF|~qRfZ0S6wuNznQ=zS`1ZytHok1@z8uLelRe%;`RjL$kRKC%6Z(-;>BSb70WYNtgJdGjkLY3XP%N7VD$4(|f4)yJe{B4W*(tK4BmTWAV-R=HhlYbQ&8TBc|ef#1_chIS(bb@@D3&0QwV%GPt7ltxOVAf4{-(X{*7zIL+0C;ph5GvdvRXraCz7b@a`IFb;V3Op+ef3d>`3=#Kuv<n7(eeD0L3D6v(%vau<dwz7bpO)E%zkttmmDljA@W=+$lBEtFC~KL^;o(<clnK?EVX_qF=Wq?IFwr~k<NLnEn#mm3&S5%vL|tzpoFYd&MI_y;O-EX=mRe~<|zH!NgUusfZ)4IUWG2c86^C!-QRXiB5@8R_|ViUvAtTW^Fy84XB>_oTzS41pwu0ZFV&!6Ltdt;0rMfsC`It=u*fhMe9YXtgxaLzr^f<6h9ZU{G-auUrAA<Zr!_0IVF(B=(CbQGkY4&AEnrk7MByITnIhrk%ahm3lt-wGm#tWd)<EXT`Jppy$O&<cdq+i?&kd#~6B_EFsQo6gyW-q1R8!t^)-zexaUw3x7V7ur!PFXITW#EQg>#J9&6md=1UBN@4mlh9OH<3@HjDL6>ezKTK!f`<Y;r`LG+xNDXREEo6)xbV1(U^}+lHY^Qe)z1aDMo-dtjeC%$0Risv)gDNpFlY04lR7+a8j)w55Yxk_&Mj3j^_I*kt;ho0(#%1A#%N^3!wzHb;S5hJ`o=_!tV@nx^+dDTn)qGG>zQz{S!L#;9!~!CSJl6K*YrpTi}t&?!Ek`Q`zkN6?+SMOZrK1G?^N3!g*;4^ptL$l5MdvPc*eARa(z!lYaXMil{T3)(X!<K31KAw)D->6l!@sDOxgermxk>^6)AZ<Bgrx(85U5#eP?4h~ZA)iiQ66sL~tgIPV7$z{+B-N#z9XzWNu5%m=aY(d|RsC)cGNMPRXj5LkB6}mNPJd%@BL?KWf0R9G-qC$D!XNTwwIl?2QfiEoTw6s#Iw(>QWVycCr$96ujkoZMlPpAPgY@b@Yy3q}FzSIzQtEj<W95*g5pM=^jPZsCs2w59St*&_)13c$dF_}X~d8S`{3$aRVM6|4w3<n!<aY;_XBLeJi@8I`e56ezSIKmtr9<S$fz(%7%bA1&)jm;p-axe<RQEjg$iQg?Y%#tthL2V4}i%#{hp7NNqcy}yqr`^>(K1BxyRMTXbb+~P!O6^+?RGDN*r*uw|H-qV0QT;$ljy8=U%{wpa=D0`*)Ddh_#G(`&XU^+4d0{EDQ1?8Fvt#9fZi}Ni#%MtBEI%tCi=CpE3BxHn_|yy7somw0exT!g67=K|_cjdtR6agM=GkKKQ5fP>ULVu%PvCq|=ZH<uJQJ1%f7m9bwHTAZdr|<!<wUCW^iQ&1IMj$y4_Y|oVF05|u1(voc7wHCGGw-Nfjf;OWWm4>t#iO4;LAQqozySK#Ly7wGn6medOaKbM{ewnl;bEwX8v_DVQZ|Sy~k#!r>8-sVZljvLTOeRPlGE>M6-(3TWbq4w=Bpcu~Ic&k2x|fzT6cODChU*(>vm@6XuS!rAW}Mbw9aVZxbR1GKg#uvLqt-q1<_fuSB^Qw}4a-&1|Fy+(*j_ZGs5iOXleSN0Qf@c$P{ZEx@$#{%j`nm<BLQp_`BhR_t~mLa+8!q~4}4CHUD22q449@kR(sB>d0hf`T9xXuksFx$m(>oK>~8JeI70LA6r6x#^arlZSRh5nQc!vcg9fLBmf91B&?r=pS)?-&?gS31YRE=2CAyR@DV1(uyn!$t`)k4<$7L^2lG31VFQ*_&smi-b#qbR$wr58mvSiEdZ`k0r7Eh_f2$S_U$;MjhrCWZ8IPXryL#Zrpg_yLJy<V{d@HfO4o=6k4O;6@B#!X^m*MPU)WQ;59HB$+n^|S4IkHIxIWqe0n*iz{{%5^yP?f38bsIP!pYlnkDi>&>C9^3Amlma#OH5yY2xkHUu~X<9V*j{-ll1!qMz=xHZpTjm3=P3z$exNW3n4A`}Ou?86E!<cSLSkoTgrgPi7swfaAh}AZ8`hZ@ETz6tkS0RT#LUxptR82W$>ixbb%J#bZID3o_(SlPW&;`;UL*r}^@)f&#A{a8mIdTVE>bYc}`kSa>7z76;3ez~~`>IN7gqt299H%^VP$E=@&%Nj;e3i1mE0a5bmG6@JH%r){i=E<GdQ9#n*+Ks24QXN&e|pVPQ@*_f*eOU|JYWkmj6!<CS@`*mU}u0tq8P*hk#T~T|hqx3&OOX(I-W@~znW+f#@6fX+(NH7f0!791W@5j^(#+}kD4YW=u1@Bf~y?ax<D|C(ud$-euIG>l%-AkbnbR{yoqU9U&MlQzSoRWYz2;j9O(2(CCX!GdZHl9msotrWVMH9zSb<#^WWMUy@&ObXU`+K1hT5k2-?}JdNs(N&aB0S=KUBx416e?&+h=7s15eVg&RkGYdlFCkb&?nzA-58^A(5bUKa1Nn)FI|qhyg)qx07OE4145g9PL-@iXhX?|N+Lsv;g?!xdE=QmEFzu)RL<>vK3A;R18T{$!5|&iG(}YTp!^Qnw<Aro_*d4c#sV05LLy$>O>P}0_O&XWl_kdK9z-K4a1ZNfkZvkEiWHgO)OP8-4Z7gj{IIz1HoYWG-&=qQ<r}{IM6@%^33m4a{M%e0);hQ1K2`~saf=itnEwBQJQM1WE*Bm+_~JDXDKCSH(AwrcbVx!=hi&tR7S0|rDhMi4_D0-equqUdrdlpuM%sroJpy|Yx*dV4?DN}e2ag?t-)00oE>#lj76+&~zTv*&lTxcvBgNQaoqDbYC((;qmjqqpfmL8Xj^J7Ej`14usEFQc#3?kM)OjBs$NC-pTQ{R`F_7*6>&Tt+gm~2G*&JCxO2=>m^02$xU2H}pP@*djd-Z3It|plLkC;h#gL=F@l(Y+5N!+Ur5Eb_F7#!3Wss%`Uc;m=3+<OPu<~4JBV9&4<{Tis)R8K3&XnG6m7p-EX0ruq*$WQ7-<a9W{hYv#+9r#U~IAk<J-6vLpx@?ED;ZHwk#6=$dvpvPXlZjuSAF}5JqpbkSg6rbeg9(zQX5rl%iY8%Hh7&3RFVTg!G>Fs5>fd>vxHsFZsqaP(Rf;L0A09SG7QHTQL~f(M2;yNGSoE^<T+q;i$zYFyD;(R|gG5|Wl5$4ah#{<@t<FBDxwt)k&Q8=YMQlTt5=MjyV|7??LPe~F?#D$uhG|sMcuT&Ze!M_zH_6nUl+8Q0d7g9R_2q~&N?nD6^scFZY#2A7Zo<VS7>)2iGoOtn0$dsv!cG0I6jwH$gcEj6+qfqMNk;rjhMZUzWml+85>sVbJ~rj3CKLEEMS;;(j$5A`DV9)2d0DBrM3q9h!m4EGJri<2P)$uOBw1AhTuz;;xhvcr-1WQrK6q)|uKB0;grZ~HGSzcQ_h+AeLBtu1n{`j8jy3Stu>a-Ze){}N;~H2SL+ofI{Js%$(il$S4{rd1wM{EKU`V8@p&GjSW(*5MbzWR~X>7VfSQegB$L(eRzx3Kb^gq4rN|EF-P@{p1n}rXIci~&msj0T#4yX@}nZ`(eZqZkA51Q0k^zEX~?KCjtfM}D4V_7Re0VbGvR_DzfC<Ep#V^vN2%}!|eAo6g0gAYV?H~9F*3@&R^S`2HXUj?du>rK<$ywh7VuO%Ca=x+js&eINg4Q9?u9yIUe!#n2v)1AY3V1G%XKGuVAX&91{N@@je+X%B`w}>0#!N@VmM3KN*x(+wp4LiIw!>X|b)&>lsZkaqrHMLcOcmr7DaMQq^5Mtvcn5Fs7U6-pD4d!%JtSRVr^-aQW5T#*)4R-w*z;d<`IQrP{z)N(Pv`Y-RORR{)2e|yFL<IqwOV>rE5SlHO(suWa*#&ByQ+H<i255Drm{!LT)uO+V;4#)gJP6xMp>#-cD^E3{nsIyP9U?LVY4V;_*`HhS>x|nH<+Qey+X|^fg8?*)!!_y1w4-)(*D_5@<X9@d>dq=r+%S|sN1>?g&7za1L8`!A_S?ZRic{9~#39T%=K%<@jMs}4#Fj+51T|#{`z@+vW%RzupeahhSG1(B>&-L?8h6!L!Waz>jD{)O?Fu26qG<wBW6G(cm%i+}xyYK^Qq^xf6R$%C3z}JkNGDz-Ne<}SU5mT4RSAQR(-)yK4-#$fZ4fteH<q^UdYJ;sPaTQ$GBzKCpo>3jCN9v$`aOXm!R-8^d}a?9Pu+^0HU@!k`tQ9IvZig}hC71V%tR}2&)4+I2m`;nY?~T?10zo|EIctf59YbT770$QghDAB14~XFZL>CW5|tVB0f4=Qqk%9<;DR(&>9{FGVJolKf&Ceee<oBBhLRvA6%=s^Z#cs2nrs~@@llFdNjU|a*ZG_DHp_5}31l_b`5G+v)%j$u7`>`--S~~j#(wV>LhVDYG-6<ug_GbluHY;4a+3f<VsJ7;NIl0hDsKuKzG+{W@dZ)sF}w@1UHEl^bz6wwTP0Z0AW+ng3zVb3H#1ub5L`CUiUpi_Z+*~`Fj9-|U6GfzdEOzN2V@$cfIx8~b{yro8e&K|sbNcQt<qE>5ds&SXr?(zX82*yGo767Z(t!)`Nj}EbsWzagL^b?h(vSZiqr;AJZ{XVlK8APa1Z0cX~OeFi()<E<~mIqGu&*W@nc~LTtTa<a^}vn_FtwzY)m6_?=&voygqPn8<TNpn1n7QQyVYcu5k<9kWmU9P644ZV?fYhjXq0`ILH9NA8(~|zVF={4|w^(w3?=4OJPD{mR@3Cxdkf=EDS4mehUKu#Hh^qBbJ2iyW8C_`~40Hg2*Ab4~s)oiH2B_eY?uyE=3Y@CyHiwxYZ{z2-<%^P2s$cp1aP%-c!pwD9fDUrO<YAg>!V(ZNhGFRhzfX@J%-Wwc_0eVaXMOaT~B|B^*rthq7~6Ot)6&45VE36V%JLKVR=YJ*a?NBP2MQgAE8`Sx;4$>Z*Y(Pce3C;65jdrxn?Y<Mk>iU!0>2m~OT}?VW6bUK`65`f0;y{D1`roS|T()~1&bd|8M)tp>f9p&e}MAAbG#>HEKa_ZiICQ}#D|;6@FQ3b4Mr_tF3}ZJDzGlCY~$os$n6M3^H2m_y##UTJ&t?z9l-wLxWB*)_y)0J&fRSwniEL(>&xw3A$$yLVwUf83Hg#g?di6+L|4*|sxUvGI6M8#{p-24QkMUM}u-g&6cYC7{wT1l-DjZD0oM8o1kW9<Df9)~RQmeytLt^h>elU}*}=&@VJU`=vhvH*wG@M)m5Vpoi8(EEK8^{q}B?0GMSAk`T4ESQp^St2c=XFOla;_MYz#FN_}d#wtr0MV>%s$)}Nt{t=T?CuEsWdvHgyRO1OJcX<@KIYv(XpGF1|#uC_7YDS>QdP`+and=34%<#zU*~LLvor$;T6J0A^dC3w1AzHbJ6D2Leq>>-SfCUq716;{O=xK)d-&P<AvGkacxAbO^t4I<~{&T$+R}Ty@B|e2umZCxh83bV}xkAxqAj}GZpc1ON(UE?h47*}UM+wf+fk|eJh(yNT@SP$f3;=n9K8sU6lFy3?cWu?+<wTi;mdsdicjpeRk-K<}K~x#?l#(4;q|kpC7Pcl-$!{vT&rl6%30Y}^5#d(G_wn_}{*B-{8}R0=_Eno6TQnbQBRq&G3gf}`$F|1zLu>B@CN&&qGQ}tUEAS`9g%b~mxWR_;dfRfe(lD&+9Yu}X1cjPEWIxACa9YFA&sld0L>kBRkz0EKC#7W?U1rBbK~)J~?#azoCPC-zvp*uFtBbY4DtD;T6h6hJaExQZltE06%+=SQe_6vg^`o3LzEOiIZ1`(Yv|hpO$zWndYypLtEWBebr6J02BqE9+s#~2E(qj7lNo)fsVAdkdf1vXemYo9x0VXcM>{ujVct%rZgQfao+UjxE#}TOnOBPHYFs?CmWSd@7#eonfnoQn-$S#v%+`d|;@ZGP+M;unPDQatIN;pOW)4E;R9f&O~N=eqYh1Z1P4%AYV`WNf^{D#51(!)jBVE3LlXjafU8hp2bX-I)XqZF3Qarzd5LlhY;&dbo~a`pDFvmsyY@%WgRgUGG~vgu7)=voahAT-bM<!KWHR}fVV2QnqI@ZuoxAnuR3FVb2&Gb5rf)Ma4mM=4>bpwrV5x#ul|4ZULqH$*x+AHh)NG!S%^y%58!xKq;YQSke_DHF}#fHIL!UQ)y?m{a39t0;jSWSFwvu&g=@op$GfwuvqgBQgPrSwdcg)`CzAoW%LD+M*3gYHdWU44)Gbx;Q9rWa+rN!7T09F3UO_Q>Ibq|9VcUs|={T-DekEx>FH35<k?c%23G~e@!^W%Pd%-qt@otG;}iO2fU^L5>YGFiSFcUpvXqTLZB66`|K`wA!XxC%Mg36Y0Hw~P1+)8cJT>cKDgY@`#vIFFI;Bilgd2xuyAcrHF^NDf()#opf(B==)o8)P`Fa+i91D~meKQxfC-q8UTM9A-T1elkU?7WD%1z}HtWI1LUee{p=9f3IT~x##Uh6c@0sE%_^=Vb8r2xHC#c3`Ar5r)(l;Chib?T2aq^$BF1QnRAuW18Vn2_{Dk3WF(7AVx8Uz}DLjH)Zgd5I>2AT_IBAWN#^{)G4hbs4cU(yyk0cK$iq{(}J52NEE2X2nLLN9PD!z2nOkPp0H?H&pEKex(E@fjhtMR|+RLRf=6^Cg5iFF`5?CP9NazRc|top&yDBKMhoNi*RG@5PPX8Hgxtd0wBEhv_=G_2ULTnXw$krMQvmxdW;jB|B7bgDh~kJ+Q}QQE*peTIc};6b?wQx(mx#epU!PnT{@`Xj#;&NgJ7XE{?lB<OlFshj<-4gx|SUZttQT%;So^5TL_eZ~5+3pi_FS@>4l}Uo(y~(e<78JF<8}CeO9}=0~B!;OvcFalgC%Q*eQFn4n<$FVOA+3}{_|Cgv#2cI2ZjJ;uOxBl2SeBZxmv;4f1Vf?rLSfsYJhg1zO|Oe0RA1qEclgagP(0%`;&+a!=zdz40r`;ZxSGP`2G9Z69EQ*z!h58pJXB)V<*Bqa&Xkuf{bd`Jvq9rYyYa(JC@$D80uYz|AuZWDNtXgM5!NusaioeV>|jd(P@bM%oM3baqbO-OBDXwD|UCaZg5vY)F}eHkp_kz=QlTneMwSgf#)*qLWe0V$(M5;#b`ue!!nc}lT($y}cCnKjwVj5Lp_gTgKZljlI2!5vob(`DR|1v#Xn&mn!qQ?7D3;t)X^OW<m+b6cqDBMFQX3oU~;Z7zMdQkG_uTh^_eadW>|=R@LehE@oP6LQkl{_9SW`uyll{Q_`VWYjrTdnYP-TL_64i55};YO0+vLv7k42Oj52LbPk)vhnvQjLd~je2dgp3n42TLSqB*8dEkqJk*#qC2O5ir&u;9?I4(*$=onRj+qLg1QjgQU|YOT?WgTGfVQbafG$|2r6kC4oz8(wdD3tXUz=I$qT`&kXQ=`0y|K_;MhEvQTMcO;BKm!nyDBWj`jvprl1;aWPyJ|6=<Nzl!Hb|22Y$Y3uG-S>sdLiTv}{<o!CmNhe%{?IDbjO}>`8WXK(NTFJ+=2G#8jTCg$9SKK002;vy3quc`V6(qCk>h8$OS(W`Yg&a7zLlxpydzNJ#%{LJNn+I5gj2#-7P7Xv6k|GR*6J`lmt4<y|s^$3((@T<?sdXJL=_8pXQ3aEoHj3T{Xq^P?U1QpbZ}JCj2PkL6=<Vqnh4^Z?#IEq-HtlY1^j<4Qw^#+|swI6kY9VxmKq%-fy5$sUiyXS8p$C_ylaiDV^{lY5Um=nbWPh-%(3ueNZNU1L~4a?O@0CJ53@*O0&@EbNV9+)(R#dT5au+LX7-(Goz~8<b#IznebCf%(x3l?F5UK2@K&wH&!BhjWfV`^~W^r=9eY!To(F#m(SLVzfe_Oe(lx5jERrO%}o({;|2I2uKj)2t(X3M_sc+Rh~t`MnH>4%LI{PA(w~VU`UCw1eWoco-JY;TJa#arW>H&NmvmPSqI}d0<^_6qSYms(y~JsRuK#9sX&<2Bs>K~c!i(yk!FEKC1ISDyStezFBcF8m&q~*epySE{6km}ge^MNW+HRbXX>#<T}Z$d!7f%zeVdOGtcT)udY2}LcjcOfmP87-R|Yqh0VfYY)XopQ0y^H!XM$lwVx-Vtr-&(Xm_&FrP1#JdHa#4@0yB`;G+p#qNC;GsOM*coL#OMfm+#xYGKzQYi!W;oAPc56yiU_|h)l}|VlOlg!fp282A)}ODTW0GP~g(>f1YFN!=lb~{oqt_T|N&&Ve{Uv94FPlB1NRDvdU>=BRDD*sS?>%l&A=$7@16?=VfkfeMs@fQf{A+D^}wzC~L6HaUM=nEU>k~WlU!}K{HWqSC{tI;a^olTV?!oSKuhDO}|zoMzEnS<HG_HRAq}~eJx-sDyqPP*H}Yt1~)1?f;487wLky>oR6}EA|*(E5K;L-8OAxLRE)W<HKL`C0GqnHeGZ;J2(aTik58ffa5rSu<LD?)Z4bE_p$wV)>BN>$mcb-@Z+iZ6IZ-RrrcoQmMC*#!)4QiXJHULl&1b1r<iTCEOM9@X2N~=)H>L#V(+PT{g)c&|4BP6mPN@~c)76!<I?JG!`eHbX?2I9RZdFGmUDAo&ssq{5Lyb0g<^?D3GH^@}i?LbYi(*EcLaj$D`;<TfE&B-0xx)@#4#x6GDr30;#SL(bgIH>@agooeJn<QhL;ZxQRz1cnc}<YCpFJBeQber*b#@|6Mq}R8+NK|3yl0m_AZ_&@@4-4zR3KT}?U_)Jz~25;k}Mf>!}A@e{C6d(6EOCa>;k!Wn#m;s$@KRD4p87uAEH6vpqn{0-PRK=pUFi4)s%!a{{I~NM@vr`-ROs-3|mcHOoxn*)B3CPo8-Qr3T2ejKyEjOy-xQcp1!%uW1Fc$*4{-cH#9=|Sa@P%JU2{xG?ix+<>r!zfRs4<?@U#~{r)p``9gLETT6M8lsSD*lUmsi>YX?z9v{KsMBJ-3w9OqOXstxmz_~pgQf07c2_h=qMv)~<b?8EnUSe<d*MJeqC05ZpmY0J_Y}ZD$3ncOhAoXEmQbrEA)X44_!W4A2^}=oVsn~y`8F<{EQPr{ofKZfJ2dFlmM|&7!nMV9M5@K^`)^3JPg>W<`-0m)2v(SVMe2Uf;)8koe;CX#3fzFmyPubTPiYSnY5Mr}pY!G2__$b$HsrLbc!j_Get*ZBAAyIwdCuNq~=@uQTEM0M<nzv`7^TIrjH(R!^;!F4HYzG+z*{K*vTh)#*F2LsDRjZ<%L<M5Fw;u8XnOZm@7C*usM#9><?kwgf2wsils)Jc>&=f-x+Aht~9$$`yG-7UOD)1xSa?GiSw_Gh?nc=`3Z_-EPM`>Tce??<c!YC@+K@?~XHTHn(p~75n124%WFJld7<lSvpXFHrXvBeXnAnVt|cWS5pC?O~J!8ou=sJgn~3KSRgW)ij#Ajm=?jykQk>FYf*!}8kpUOJAH@!t?i<DNXg#NIUq?*DV68lYT)8)Jx9PRvQo!MwGHE*fh1wv0JZF`xCc-Y4M1JZugj>`&nYAbHHBMS-Y4?gh?QmkP2X&qa~79V5rKT-{;Z<FugRF{IlsSTrQ4V$jE%?jj)(5n@_G(o>3&lYLsIUo(aYt(JuML?VvYgMcBEg0tRX1nDW`&k4INv8sTePpxI{>flQb@0l6H79ej?bcQ5~DH~R%7zs^~N$E)Ja#D~4$E`pBkTf!3r3^qHNmWuix1r6+jM0o+rEUc}q$=`__EhyrqFKWU7xV+&X~97#GMHpdZkW1~5y_m(lnF@JNSPwl=%%fAMr^-x6h6YzQ)HD|zr%4ssYkODz?5V5jNoI@I?zA3n5Se+G5`~itzVY5JjQh*m;^m|1udmA$D^PJI>)7?_I*1_W3*xNQihNOW4y1iC4oN=o4=_ooRfjs1@wuLuRuFP4@_K_(2<r1mH|3lu`(1`O`>tUOU2-cJh?=G6oR@FswKl*=#pq*fJ!R|#GkOdmxT>`XZbAL@5Tpu(M(7Im!rwlQ0t@FB<<#hxCUi1VtB|i`8-62lS_FHyIBdg<)FOG2vLQ*6G!|)rNi779RibtSE%^Ivh5{cQF1jxWe~NLkMq8R&OS8i*oZN|4#TWA?4w$drmKfbrC?GG*|$~gTqdj>F!wP})fR`J{7q8j{b!%P4?z{tI-LKKwMAb)Bsg>YF2JCTV?N02iL^ps@lLj^|E#dkTg7g)?<s4?g?d#m9Jc0B%W99TO$ctR%MuJOH7B>b?aT2#)R|TH6=d*;O-@**AyqVLo6=dzL)1i$i9NMg8#<*`GC%(SY<i*a4hE@Tejk%Zs~WyTVn(`BA9Zm%^2x;T5AZg`_BWi+9As7$d(Ssnp|=%_)H_4#R03n>0aMPvde(2(&3Zwo@3;T_?f(G*EB31')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
