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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-qxn%Z_7La{QNCbD=7h`r%zqiz79rr4ssKVk{H{0UpDEF<!{t8T0S1sV<V2HzOk=^Bk6>RTC`sz2|*0BO@b!`oF9H_~qBX|LxbSfBEU^$2T88Ufpl5{_~gr{`dcR_~PN?-+%e_zy9{W51)U!`qSsX{`}^Lci+Exf3>-Kd$+&ZT;FfLeEs8xyKg?f{q*qt{=40qhkw7mzyHVP?9uPu{^j$Ji~pFs<m2xB`_p3{U+~?#54$Vzfwb-T^~djayN4ER*G>D==XdYF`T3#mpFTf6?bxzKtDpYw<3stEr<cdy@vg2%?ERa!J2YTFUHx$P;nR1I{YIbmyN{o)?&Yw;dAm;M?db>Gvxa<m)n@VG)Qr`z#<iqh{^#B9oAU`-&lP<0VdTtlx5wh?Rm=6Ue$xgu@o8KAboKTP9*K|t?C0j{``!DyAFehxev9G&eR;(OH*Gat%ZA9Ve!Tm9w!Sv`WatjcZmgHxHJ;(qW_$V@>C)54BxCi%r(^q8uX>!k(oik7;+s#q5BwG7!CF6Q@#3d(#4S+odm8ERzQYq>2V=L6tK;yeFVFS%;CWNxC9=AomMfZ!^wZx|&#(3C*g`3fwDG>vGvi51$G7*k<k9dOFsSzMg{N#{S4%tY^q)`1R9vKBq>{aLXdpcQ=8O*5R^ISDHH19+&{Q!%;ZyCA<U!UW-`>4{zkB=X=Rfa0e0ul(-M^iW#`$t~Ou*HL)!V-LaQEXCH=;;e55Gm51zqY-$J?T7D^nI;@8Rg>L$tWS{EHn-<Y^#Q&m)hC!`W!d`jWpne<14o;yt@JshJzb-5YK&%cljMH3xh>!TveD_e(cne|7T@c2XFS<5Tf3$Xm3nc9TDsdne1^-mFZ5)EWwx%+Uxsn%(9rud`Q<ETGe!ibkn3r^o&kHd<~n9v8x?q0-<5H`igPSB)!O;>U*^Kj?#*^ejG3w~3m%$LF2Dvv?7o5A&cQb+SW`kJA?~Gcya1p(eqs=lr1!3XD!Lphmi^E30FJzM+Oqa`MR~0=fkHRydNv8;<SIJ0f8&@0f1c9bn|w4xeZD6J#ZMbv&cjL*E$%fE|g~XCnig)S+QmnLHcl=1=W8vR1emliN4eXh`%IT#pD6TitDVs7(9kHUrZArUCH#^i|q2>vRWqbG%E@NyJvn>K)&``S7n1TgYzgvrni0+Pl$#opJgK+^fj@S=g>0KYe(!|I_Znhre2<`?B?*n<sDKGOs6)c{~d))P@KtTLTfT<&j3j=L6WC`ZY7(z22R|u4|%>(O)~^^1*}`!%bpo8Lo#6{P-b4e!Yf(Q!F3c^XVT006AKBocr}xlg#aARQETqz}Ib!nA~q>lT)j8wta3}ho-e2QPK;6Z@eY#^(^euXwfKOP;c3~?aAzA8!k;~2rJW=k^ltwxBO5=am%(TXdSTQh#kt|$#Q$p;snMruqWrBwP3%3dp;V3W%!huA8ek0TfKy<A1~s?!!KxsEk^+~W(}LodOtG!!5pm&w)t;AT4vEck4D=_BUnH;L@G{uB(oEnfxN|ab9itJ`c7PU$fG@WJEHujZ^*JMbeCBSYn!y_mjnMeUQPUn(f*p_r8suGaS=1S99ig{mssKS3nJprWTLa>XW6OIK;JZM_AFWrt@w+Z?CC29P4>kbl%;$^-x>T}J8Bf3j7*{R<vPV+Pwi2OXs_E^!f;twe`NrB)-%D8JH~Rw=K$>mcACFaycQ<S;m|X<y;F32ZfGnLR70l`Kh5SR_zXU9et@{u>;**{q@rr^!_hu4LOk2<$qSYU7`hRpnRq(PU7zyqcmT0&jJ=&N&nQLmqPxHxONmnSdkZlA6jKS9@3N&Go{mJZbFU(f`MAd&Z6Jz#<AxPXTr0!{RzSh^u!t;4Pk@)(vD!h<B-##xL|e|?C4VhYFK?gMFCd2^y1A^oV-UrsICgq$422SEqmcfsZa9G6mjL!!o8&PKHVO|WjDz`Ak3jlQ6`H|Qe+jo^n;?C1KDt(IoRs6S_~gU$ut(cPj$;9?2{00NoaMs)$LW>_92o5c6ymLBC;<=$sxctrpo)ma^1`)T$R_KVSrKa(VcI&dJo$`p>_K(mNVa-hVFfTS7@FnK6fTFLK*0RiXhQq}3wcT)YBR-sB5WbB8XGyJ(QUVl^pUq^ah;m&AEz8)^QD=tn8_D=1v<B#;6P<l4)fHtP(pxDUf$P;kjPqrUwUTjkP!{02?H5LhD^btjZuzhrW`j`V#47zYqOIK*xlX3KQ9iG{%}@&bEO@DqqP?UkeYS^V0?z>XH8W`8I`19fbi*bi$6k9eYeBjmE@Si@n}}IKk!?RbGX;!h0c6*uh&V}at&}q`XGRt4uTmRIjW^d`aq=I{3IKsgY1`7GD<!(^5*@3TSjgchl6zdtyG2ML2>FsTw^{xsh1=?v?aiqtS2%qQ#3IWtOwzlNn0PdFxI>{ANtPY`~xjc#BoKI`ZQxbCK@f(c>?PYQQ2^V)!+4+JRTe0-rarNxzQt{ZKD{tL60VFa)?Gsx=TOi0|Jc4<L@{!#yk}6%je!rbnS5#=jh_=CdCjf7_j&{eL(XLiQOfF3qq6t_s?7+n~e795-$xIiT0{uIQ3fd?(N;d{*I7@znJD_7y(_O^&(jAeF*7V3x627K~E&AR6H_zNfxH1r({88b&6(K-_MH;6=EVHCCJa-DN6}$b$D$hB;>_=CkA1o)fXX`ZZxtJ&K*!vx~&U3ZWZwy+;U<2l^|#Zq)ZA4HxvWvQaRBZfbv4<M1tGPL<_bB{ZX*1j<^&>XMACYZ6P-^9sP(2o}t>4WFBaEm0GMZD>_cTJBn5!o9`e2L~UtD<WyG&2=aW?&YIAhXDd8z1{D;Dfq={q{)AFYhnew&fy$3vKb{@!<yAJ>$w($JrnCJraaX-GfT<iXvgLwKnZX;$;BoUx9gaTDpGdRB1WHnHcNTk;a^?~Vk7n)_12n-)eX@y>V-N=ri12~&ZgVCa>D&USPQ_)Ko^(sZn8+E^^*Y2hc0_^jw2csu>;7Yf%L4-RMFrZC56KSt{@we(JcbRqF9=OlaPOGR&tqSYug{uEeZ<V1=d=dB33s*L*r5T}O@YbmAnVa<elz`0<K;%O9`d~l=3+1U32qw@9CTY`qy0rXCdp!r^j(<!RFIfJ8!ly-_&PF820FzKwOV9!dp6<^y4DS&zeS51%**j_CniT#%<tN~t|uhXa*1O!LC{@X9|hAal8P>NP0N}(OK5YAPM+6cg1#*WJR%?Puhe`?t0Ig559Z1xyNm}nflY!^g|&-0xVISmNeY{sT!74z?#3ZOVhW27QFA)pC^*J6Sj8kZnZiz>$zaU6Lsf1gjWc=B_vPna>wKXGu3AA44Y&@n)m^2dxb@3!gjan!6hUhNbA?0fJ|x_}$^aT8b@SMnLW0HJrPY!4Bh8?;-@t;h2|);hF>gs^2zGB5M(&|7L|Pfi3$iyeq+LLSsz(hcRKTd#rDN!?E|6bwlm3!FM_?%&=@H2m5f!D06*j>+J$Pb;#O=MGoIxUL%U(^27hCD-kHq`i8gg}X5><vk>}H&>fdtz_<843LWC@f5^C5@^gn8A)*bdl`7&MC?9VgM>9wu)TFDWm@_V`sACBG?V$8%q}8HkQ6JQfpyo?zoFl4iwJ;7BcT7i3ga{sB#>QD$Y`O9t&<`5{<67eVk{n-<)JakD@|J_#$IPJ?&fI>zymk2%HRyA~CBQamzag9dAI*zDzZq1@2o7{IhsTpPwc)GGeoP}T@Iz|r<c6ah0N*9Q5f_7f=Ct@b~Y)&vW-g7@^{+G^H<cY5$hGEExb<wFYIydt$*vX|UinD5PtVEis4oyr{cY5u&QA9c7dpl8kCl5VMLR=!JTHY6z>ObpKxtbUGu$ZVD@=`I+l`GP7Dn`_N5ihLW{f{Io%Sfj=~)Hr+;0IveiLZ10ApC2^Z`-su44I|x3k&F_PcwGN4TG4w;%LDcnt7=4Rr;)uu%F#u;naJESxxp_4i>+OuWbu0w9fLq*H;)7yY+#}|;hw*{#8{<DoX4qAu3|j4sq-jX1@Tg)4ukb`^*jN|=Utik8)3A#t~sPH8+tw{Pk$<E?&zpj7<RBOIGjy0kWSn1i-N<8n(G?P{fK6P3>vVc0YQzP8i(d?hV6fVzZGbek*cQFb#Xqr^qCXFZdFOpY}e%~GeQj(H7Z+mtYDqoD95e1p+H>p=GI72t;sGVxJ0VYn(9Sk0VcwytC{EnUE7_JdPBo!Q&2#gpNZ`1^Fap}B#3GlLG;!p9+SoJ7Zf{X>9P~j_SppSP%-y=3dbi|jZ@Z{+|mq#G0Q93^&Gko4NcUfKsa((2-5=PbM??VQu$W2lc8Pok1OkNhJpo+SS`;Z3jjBhHi(OLV=*VQ&<AQ$UY$j31OwafDzrh9QtdJuvXMEfWd!E>_Tmss^p|<6wyldQTwe&%Sb)rz<@vG##SkDPn)6)IL#M^w@{VqcId2GbiQXMJO}oH`p8$<?ZhEpF;8cqacy!VWC42yOQY$3Y%I5dW(v@%ka7J=|*XeDs<d08W8$tqZG(^Pg&LwF%wJFlD18n*3+iyLk3V;r2j0b=g0Ih=<9jc8q!Tuzwss&!P9a>%wK+Ulv^3uriQ4lApfZI}tEW}*nx@J^3>2em4u7X%l3N>lkgmfVVd}Wfx#L8CmP`V<xoZltjDv<FE(+aKly!Wex<~f9(^>I#|EGt=x!6S5jSjy!L$BQ*g9xJf2An*P>P6``HhC#tJdG;S*h$~q~^Bs1yK`nE@&@!2^fM{wXu_#eiUKVwl!1}=RpB~_TQo1ntDfU?tSjcC(mi$N`T9>M$bIT8JbGaMX0uXwV_#qc1H505V9F%(I(nJWv@wLy&K(!esJV)uaNOpKp=oG1Uy<kp6%e1hGU0oFh0F}I5E^P{qcDEo6I1gB{y0H|dQCvm^I*b@==M^QI9u<qQ*P3L4oO3h=tAJI<YI$8EL(uo2JJLuI3{yVvv7`9Um<%GX8<tzO_`qZ9OC>^Lc;{+(gY|F`*vPP?MymPw5E#yICsgWFs{nF}HM0h}rpjR#)HEZoDU3dkVFgUNLb4fRx8U6tK7ejhtN65tgj{7OM9vIrTe?6;Y;G#rq^6+Zo*!srgl72Pbh{+&a9oh&+-$Ndz$HTA77Lwm@+$`hoB4s%jfylqrtv#Ev`BavPF;2lfb<tIvN>I(U4+7NlOtR$E{l%(E%lG_^?<7x7=<&s%h6O|B6a{*YywU70OrSowbWdiA}uaA0Cah^7AqxK>E;-zQ{o99JO%|{Dc9~+K^TVTK7w872*PbBYHg>=z%O0F$=H7c>RjtC#w*}>q{rf)AU4PY-8N=Hi$#4^DJ@AuJV4%IhK6V*k3-t*0zF_H4kivtpIb8CNfw8Mf_x`$HD@I>yF0twZG)5#WQml(oQT(8lQx86WKwKS-C(=z)qRIGK!{%SDlG7G$TWlOCpWzUa(tFkI*ir<K(4@VDe%di+yZs_<V#x~eG8wUnm|!Q!2Gzd?=S*NQE4f%QpybeZh!((^sA}wSIU67MChHxQn@3LB|(AHvpUfb65?^Zt|+2Bvo1l#=xiasQ~^Aa#`Q@pSs*u&^nA6Cs)NwMuE&J4W{!)5uq@}ah`KNS74NXxAup^Urr<@hOp+COc7Wb^nNxKVkTt9pJO9ytesGL7f@TYrW3hBh-SsC8zHb(v`Qqokex9;3+cBzwt%G5~`P<C5|H|kVfm1-O9qd~cOjICo=y5wJw$YRNWYr^O%tnOE3@1M?71$&ofZ2j`Ktv%bqijbOqf;XeY|xQ-eiH71YB|cD?hSdNEE;Aeb#hjktUXW(64(%8YPi`pZ;5-7$kvs*rtOa+8z@5~58xsL!)6k7T1*^IA9{nq>mq_zS{QO8lmL&j)sy9)mjF##2U0{{iK}UnBUnzYxQNJy6o;z-2UU+eqa?xpbmmT7ONERX&tKoWIPWk=pyOU!tbh^ZAjkeGUnJkKJm5Jz|J;SuVxXL%(TH$w`gAi~Zm}v|C?{oBA1Gj>)tj|-f`?%guc6TmcHna|B~#|q2l35)ABS`cp#VieD{`NiCNAfsobG_LeKppg!I4YT4bC+DKYq8{{isXl;{Vg*B^<w8zPs_|5_h=8{{8t+C_Qlms39>xR<dt7DDYV2Dif~sL>Q+F@*KeN-;8=U#4VnI??7nm6j6gtrnIO=SP+$*gr<r`BwDDs9Eqk2dxLKvIn-{&>t2lgi+cZ$53Tw9fmojwf0Wjsni_Qvvi!?qIChEW!!Ut4WEbi!OzJ~~B8SVCBfa%#mUEE~ubj+Mq;G2)PmH~E`lhu`7*f>EG>$j{+<;~jxt@~@77^rIH=!3=3*BH236r*!+6&5lB^g~b{m5l>b8-h=<1kUopzjz^EcYtWY{|s;8E}{<q>wiS98Nm*{dpXIU;Kx17qYtm@A`{@8$^bpoV}%~M<_)_A$MSdndOEGhqbGE!bE&C4hTIcOA;a%!FsZc*$&I>{D0MJfNdt$`0)Zl*bza(%xS*ZtZuQ~T$=ess)y%TuiywUh32P(n+@EXwW`pjf|G>}r}bpLT<Pm2nWJ!YxZs|fm?M&n8qnGxvFGcV`m1Gz&k*<%mqhl>Z$k1(<)3ZcRbE~uyj<R_U-$LALBz0x@~}RQ@)Zq3+K<rNNzGk2i{5X!N|ub|;f5C^Dv6-Jrk7wROdCzhR#T0`0f;9S{=im|I<LXW(~usw6%&nR&8}Lp(HK|1&dLW0Oa&!!P>@!wW|q9vP-TE5G78<Xr2ArFm|-DeCr_{`Ta9NV0*J87laiqdXf|vQzOvXsKTXKj0)n{LM%5jpAwTF$JBfc@wjnJtc42-530m06iZr){!ADND<ufOx2Ld=~B1YqqAU`b%H>xp8)lZagCvul#)v@F;%vW66$}bWRxFot|mL29KjD0^Ib90$IKd{k{;~yu&AMrwCeTp>)u1OU%r6Wz-p4drA9(xGCh(_~E*(}9%a{sNB!((71kASbMT$oaNh7QK_`o1I@<nsx{6|Det+vd9%p(-497X^VXD(6CypO%o$wgsR>nCLtjIE6t)^j>U|j*n5WiU(4zcsr^HLyATe^qgs}410I+j`iqM(d8<o^x-okEeO<9Sye+G&3q9?2N%GQ08EXdn{F&p&YP=)F#*Ae`8l?KuC;A}#Rw3L*^YWlf)bFKRo#dY4u@p|h`MaFSrD5%6H4-!Ke+<2TIWQU-##^bf`gMsJtFB!B-+<>5y%8{Lfa5x=u%)h!bZB5Y`Y!;mFLkq$qgCclt8dcX{idD;z@8a_hQdgiEU`#<vIC|_hz_C>Iyq##T(t`(-lW1tkX40ROzy@i}Pe=Z9NBd1%1Ldr6*79@a$+V(bE;PnG39DM?@x+Z`R4BpSrYOKcf{FT!KAPq)eh#c7c34lc%Qp$1*YtobhJ)DN7H#ETJnTt1EiMoCYP06Yh5ue^(+8eU;E(Zb~_Z&-jTLM65c^?-Bw_*-yoq(}P5)L$RL?22|VVR&)&+!B)1tkl`e;p4Y9?DYQm?gZM-~T{d*i{A`;5)oZ;;zi;WZX5sxg>xc4SIekZgxpkpEN%oaQhPYq3o|Mo;z+G^xjuKub9oWJT1frP@afz-d8I}aSGev9Zir284NQ)jws@W%EXgK6q)_D-?kSi#7-2z6BD#T1O;wYj*X%-HLWO+Q@>dRR+zvh=?2NV<m$B4CsiqamE>fc=L0+0{=cob0aVpcfqK~#mMsBOlrRgLF<#bo{C*r&_|5_cS!9G<}jR$QqhCwGp4MIkxCL_;jA^*pC|9ur9CRT2@UB(k*~m9yY#jY(k9`e867n^6+?yFQ&8Q;fwtuxdyJ6^F>aD(c)8=~uE~gQ&SEd1V)6x+zKyN0d27k8Cj$gyriA;7cOc(+V=_)Bs|jm_0h+OcfrM3fHJAUh$l+7RgHbag$|>-T%?CsKHX;{J$4fthScOQ-iH_Gl#7e@vL}b?k#7yQds<gidOYHIbGdmG#XRO?)K_}bA=^cG2Rw%8Bx1pg~r*s%kuUUYSbj=mGmi+BpEAZ#tSq0AYVb9S}5w))iRh3-YbMuaO`aAGSe*Asik7qLiPq&Njf7W4~A2H%gUMu=V*njAUJsiSsAgdWT{$iB7@TgL<>CX1r(k;m;Rao*D19z>vZ7h3M##*cK`HiG%?~3j&;MsHr-m5=&?~DqAw$&51dlHxf#?acfn=HRI#cbZ2mXzzAcg>FV4W&yJwewwy9rEPZ4FgX2SEdmEd>27&@&KFh<#uS8+!gYH!e+NLplhiF&2qGmQghcN!IbY66U=NVg|!h5qN^WT0#BLN^Yx7g_MKSWU1L5TkS^uLPg7b_?a&yu{1|Fe{5w0sEPH2+9L^4gwaW>O30;X0S6xNLl+`RcSObvR(`!SSaf0P_jg2cN6N#SNkjNV;xR6-js;L`N}ytP&eS&A|ogj(8xe|R?(uZ<jul6wmb$(j^iRrY;3*A4z0!3L@RMyTY4=DIGo|=`Vd4xhR9WcB{wyh(qx|(xQvt`<48iAvKBQPj=8B?o0`&}*7tVDKMfqeXdZZ{3n>I=^Xy7YKL&euOB9WIA)9uBX;JPSlBf<>plR$~B=9dF6?i-I^AaF}XajXTV!eB*xNaI764jkNk-JOg5GL1ID7L`(JxOv}RXT!R<)XN^)T|>#HU{+S%dRnzS#PoJ%u<*w!Jp}?iY0d_OC!5pn6$+>J_O@-GU~-}y!e!QVmvvDvJ>U$K5%z&3fIgoh=S}JAMHIc4D<f!;_cl8wu<Onx5#2{AiD*0?7Ea%S%#}$HDm}VE9LUkCZ395;WsxLXsAd|5x6J(miG;;VN!IyLUDy&5*@U*UR2~-g91ui*95Y3pn@dHyP~;}1!U9639%ye{px`^m{sW`BE8g6A5PEDV=vW-5@p9ix(m_IQU<%v>}T3LV-yp=*_z3_cQhv|i6G6SF{BW(GfsjyF;r{941$fLj0pq*?-4J%#LElGe8-lP%p^TjAly^7O@*V|R3&f_f*Vj5-}At3765Y`K@Zr{S+<2#ylKc5Wrp}zNVcx+8t{$)`kej1S6)H5QK_xOdYwHmq8^c=Aao_L0Lgu#2I0kOq0uA|7cI8c!lp^pi`i2lf9ObiHDFU~ptQRtNribQ`QB4{GpqlwxYc<_9+vlqyH5?-Z%`(cmV^Q+$?>YtL|;Z7VMW>iuF55dDvb&U>(Q>0;@QF3IIP&GiP1GmG*G&AmC@Cl7pgV!J0c4NF=PC7<dD2{bJ$RwoHrjoCN_9tj8pQFxIWFyyz@?&dRD+J7YNqrz0aJQS5fh{zTEaj(;a7a(}lN~&sEcqqJ^v}oH9fIJW=ih=PE}_B;K&#bN%y37}24zO?DVDDWHmA-R0&+r6P!%x_IQtR&v-4JJxhNy2>odh@m+->^6<OVa<9AOTNV~;-Lq#aLeRkfoX!0%o6qdh)O0<l~>}bzL_ISiT-}fzw3ER@n@Ey#>ntV5uTVNdl`<ru~kSoF*71#hX<(sj&zCVT>``W$mGpeUbxN1RGD=MmAF301hIB{ExD)TPp57uScf=oteBC;i77L4&@90d>Kh87F+^U=XhKtJ_EGGVa$8SR=Mu(ekeX;prUswD#&->~8Udz}ema0lX;{7hgYO*y`}8QiAgB*-8!)4^M2Md$TE^d+69#&q(uResP+lT<CW$cK?EqC-@18{`7opRqACdavrfXj<7HEbYDBr3lNuQq*X94TwdVATd8ki`pNJmm;4!WX}TkUYxfv;zyZfRAjt;)x{QG6w<be>tYCV{u6l>JMX%pNIiQvJJPVL#xH2_rjqHRnq}MRHt+{vz)Fx(gozJ0-Cg&!d;6#;yx${<iQj!{&@4H|#KaIlFERC>Yq|@)hN)6kDUZ_5)^xAXvajp#0AcKS!++;F3uYnPsZgHCpRMF-t{(#c5bc6CG1x07KqLaW$Re{+@)qZFXr>K`#X}>l<>+WKWP;hQ1t)0qUlJC~66cy%70}8}r(0PH~xwIEA(lF%Yn4z(!;+T)6oL$(oknuwzLWbbx_&n<}%mFu=&7t-!()ENRoHe%wsp%0^fb;wI7j)1uNv*;hN@<vQfjsPTxJdY#v`&eHfTt3*+|YHN`HV$$Jp$B0Y$(<){TB}sB|1mG4$%dwb+iZGX@X0*fIv1Io$pal)@fz_l18$2`p50MjBb8vjNkr3|Q);LEx_EJuni+4kpTvSafEL9+}#3AhZ@iK{tq|s@i{M!o3*i+6nXC%`%sogxpd;mwF#&lsufRs)4t2T)_EhQ{rCzgwNR7p6|aH6_bmQ0}18)XEL=c4cLX{tm(Hw-b(9WDV=Tkh=UYzpD?2?c9x2AR%Nb*!m{XB?~G^EDLPp)R%n&MH-#O+v?fu-(&*7h*z5YSHLX11=Id`qlwNQ#m*y5MxU<u3S;hltN=T@`~%5)Iti9hvk<?*poXVhqp&PJ+tPLx`{vo%}o3DJvB9<t{Th7_$*6Kf2K|17UlpJKmDo#VpdtN>K?<QHinj2YmdbAABurQkBcD+R9ABFR5aC&wH8SMCGf~IvDE<cXOd=-Rj?-vsJsLrb-ih6v_c3$o4701&jG99ISnB_O{2aqVh3hrja~n-sWX<SKS`g;Q|F$WDg$gk4&AH>GQUF(O;_^x8HqM_klDwk;zi;ivn+#*l*1E2ONeJx%i>;8=(+}H)e|MV<-YcWEa4ZDQ*of~$`DYLQ2FrgYF7BXSlvowJ`}{|^MsE^9o~55*Vb;xexS5HbLS4pSdCW{^14vb(~+fXCbM;#&b(micm;80C>)KaP66-A3k~n>LIWmK!P$l+p9<29Bw*p!i?n3yu`^t)M5eC4cqSuaNuot8efbww*tNh5ESDJLfeoL%Ca>H*LmO}xhz;lDM}ArFw*wg{ly>e@@hS-%#x?V`u~Qcz22rH30idp2<+_W*%vAAiuF+#~#6|cBZ%Y;uSSf0d>d6e|a<Zf;5>Yg$6YZTn$y_T}BM}K=QEupP#ctD#nL>RAmVmB7BPx;I$*rQgNoA1eFjA1u^2byc8qT&Fz>F+f4_Fcd$yNUGX=wd2PAKq#{0e7Y6|U~tV+#j0^kF6`%n|rQ;$^%-#i%*Iz=^AgSs+TwJisC`zs8qs2?OaQDIiPglp?43!p}wdAs#+r-<B%TS$@F;`4?PKJm(CVadLf0jO`T$!SIMRgC8JI3ugc6%J#3Pr{rWH1-HKeY)#VzQRVm1vOM6zqWYsHHU2h#i1CLZj4CP$`9Wkyk-^vmbj*VuM62Yb#|+_#(ia9JQP!4EW)ymF0WMf$mE&1p2nn+ip|rd+&EYuqF7JY!@nuo*fmAX}-7o~L>oE&=&zCAfL}vuj9|`BhTlG=wC5Fz~AbaU*Y-|q;;H87D6QnKAMAus~&rhml&k-_?2sQeJ*BK4A#){5*!A=i4$_XrroM(DN5a;-GT&xI1b~+e@*%c%PLrn*6k-D0lg2zvj@#4Of8}^Kl5F9?q9`aRbSV6H$t+d0Cyk^qhZVp)F6~$9hJI4S|s9BdF>no!NZ4J&4my^a$W}{NrKCiDA$v<(V<+WLmwVhaN+}5>WwZznIq({5u*EUsaWZqbyQ{XjJT=jmXIl??_fg>%6&)a@VJ))^GjLt04Srmy5d_2?JJBxZkgoB0AwU*kgvDA5`S=Eyix~L>lk<rG9)uK_z2K0n(1ck}RzYz{rNados{@NzG8T0F9r4btXa4JO2$VKD~1XZ#Lo(`G)g$AUkw2|@UYuH;(`Y{=fA-0kG$Ar@gye-0V@N<)CL?T(0EIW|w6p)gDmsum@IK%L%rvuShp5<~<X(*Lw_GCPwxlR*c<l2jlzQ^m}1=(0>c70BIjyz4ZrAjXhe93!HY}c)ZPw17GX|}6X>VoD67xERLsf2{4S1$hG*VaJ=8w8N0Qv0kLV0!<RWmcv@4-bp%?QUrfUQFr&oqj#-nZ?Q6=G<5bRrE4tYA9}H_Upc1)ATomn)-Zo-4a4ypws{}DZMF&5@j%*uc61`JMOiw8yO)xN2@?(5;)QwqC7^=b+W^@6^Z+KKuRU+z7guA$8Rllyuh52YAl8qRjdB_qA8>2(n|ab-lAQJbHtDdrKJ-gZKk)gXsuuEAiF{n9`CvpWarFj>7%<!l-^;=T`4B9QJ8Aj55w?`{tMKe3QWrUYzKn}j;<KfVU4YXs{!=SFI!uU)Nu<R-I6${d=1bVJ;01K(Mg%^e``eHQ~^G6x38ymq`gZwM?n9e6V&hbkQ9bo$^4dAr8ZIsn4!>$tV(D?haL8{wQ?gCNzuuA)m)1al4^py9!O_l+Rh-uoJ~UdD0zo`4Zx3Ew^NdI1PW<Hx--CK4cVfqp0Ewz{NChx{rG4TBr)#<hZ;~T!*14jd<2EU^UNzMJ^U-8!mVXv9polD(y5HZ@DI?SQqA!^FjZ<$*=nbBJM+Yg5eP2!A<X7RB2Cljut|<0W5-%O6_IeE^D2Zr3t<^yG%D=@p(^Ue4ftYWbm5NHDV+62wi{i#*(h@FR<;5zB8@-U=ae7E<(9g|tq_*E4By^XGMw4j$CGzFy@6Bg%cnRKQ#=i=mvhFiw=D(4SZha_n6BtF@dvN3T|+tcfttGXkI2e#nJQ;3M)6N-;;{IwG8rfzC+~TUBpz0CWYls{Fwsx1O9iCGWN%zsnB60pIMy+Of1s{2#$>6CkXG}w@_E4MJ53~LLiEg)7kg76&@u>w8ubOFX&aZw{Xg#iAKIpFGX')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
