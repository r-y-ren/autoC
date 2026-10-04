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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rM%U2k03ar`fQ=EHLMAt`UPG|mdvt`_>pz*!Ir191=_a2}kz1^(|*M9$2e+tpRoea>*THeg`s5jppsuRh(?)zv@$@5R6W>92qJ^ItFi>F0}|?mvFKc(}ayk3ap_zy0@@55D~Pmp}dWKmYtcUw;1i;&-3__{;r|Z-2OdcX4^~`u*<W^6KI8@#CL9ynplg^`|eN@4nyOfBEn2{$CD%@bUZY_NT?46#n7iZ<i-;`S$f6KL50Mhva=fZr{B-zR}n3|NiZV?S=Ru8Rp}^uU_SMpWnWF^UIfM`}FziUmxCN@s`W+@ehv=!@u`+b@&+9Q}yot^%l+4&lf+w|M2PiuLDLu?Y193EkBYo3wJ@jbWgu<eez0&hpwM~8D~0qGw(HC->+9Ie*J#xmMd_4ou`vR-s0nS`{v7^|FC`c{>O{UjXy_EgI{hX@G4J3K$G_PgMOpcbASK;|9tY?_>4GBaN>Uaba>9md#s+gy<d;?<NMEHE3Wr2o{!!Ar|kza>TI_6&w(dnHI%{$F`gXf`?!LSgIPW$zRLcS$M3JN_kONVH(EO0)#FazvN`#2s~^9UKF{3h2P-3=yI9wmbN}=L##xKc2#>dC{?t5gwDt35eZBX~%e{6l7G@O8db;(dJ~yA_bSlm??tyu}9DR+W-93CHCuHU{#2?0uOX+dv+}miD<KzbCZs-Av6Rp1Z_4{}4wy!_^^84+FPjBD7{nxL5m$=lK+nl(ai?8&(Px7ktvZh~jFp8^JN}RHAWAI7xyfA(L!l#@ptNPM6AKw3zxm5hyPiE`O=kb4zQ?YjNH_5v^xqkS#m6po5-kv69@dKI)<v<w@92kB4aN)koVQ=uX*Sy%{Pmi-+9%!7=XnNvT%h>|H^y31NZ;75;3{ps(+}u*}sZXOhvFTy)OXE0x(c!!0X<s{y)WeBeZv9SAcLx2I$CoRO3|zAMwlhYy`k^^8|66>A;veTrD$YX_kDKpd6uk}*r4pbjxn+Hyr0977D|+~$;5bAqCK*Wf@!kv{?pQss%vm`&2qO-jVaUxVf*?eGb#yx{1fy}|A>fDr1JJ`*L*9l7jkxvk)uxOT94~LE`sE?u(|Bp>c^$sy`}+_7(s^<I?T0Tyu<7BEsk`^_(}(-r@3tR4{Lx$Q<sf*-`E+?N9?*OXFn$0ygLhd?cF{M8i1YpthYil0>eUmD^9JqC;k%E1-+EyUM`=0N;yDLH7Z<dS;KtcIe0>}k@hh4jOZL@gc^G>}1ufG+z;V^U`c(`_Z4m$1Zr}P<Up)NQ9l_&A&*%xRg86U56ZF{ymWzlS6Vu@uc@q!F(r$phWeEWRU$h8CO#MyFwaDgyIzfjE8TmkkT~A%acy%6a@ahI?dRrtR31)qHaUUiid%gj0(Xk^;^RWN&i>kKYqE{Dh_QNNu0LVXbO~)7V4T2|pcq<>jgP!3oSy{@|8SoHS&>r0G!r%_f?K)A#{YI4wq)!KaR`gZla;`AYnj;4%AMKtr16q6DaXRDsr&-UEGvND=))+t%#rWQWu^I7zzbRLEhEELq7SE<gQi%oLxX$r6;3gLg?AaV<FH8wb(RQX8YGQ(iV_r3&!1z&A2ajclc?0o{$ZWRc0J=*6yRm5}s4ZlZ=AONSbXi7#JL>uw9+nF>)nVCX4ih-2=0H~N!^CLN1DZjqVSQ=V<~BO!(RYEsaGd1934qQrp#nokmadQMNJfJX;%)x;-2gOiJM;`=X1ij@p-1O~IMoe40XXE0$au~GDV_!6Vq!s17IoAf0c-`hZrP;iWg(P`?6m#;`qk$o8&HQ;`qA2zzZvH`=7?Jbr1^E->M<u8<OSO#1zsdYUju@5g=wn=>iB>x(dpn12cM~hS4KAg5-$_-nsW08eQv;(q+mK=9f+X7_qu_J2Xi2O?l>gm@hVe9{BL*Vd9@bW1i&B>&gy(0o!iLhscOr_h_r{rjhQO{YImw5QNY-VH~_v#>n?#UFFXyb&tb-*a|a$#r4|Dp+Tg1nCYNOZDq)>rAb>d<n^*?y!yrj=zm=bE&@)yr{8<>pmt^d}B2FEa$lJvYKiYS(dH(CTNuxuQSbOH077$&KSXpk_TIoFdsN{eGe=m*~zo+#A$H3tI`!D~w+Z(YjXXnjDHAqklg@d_W6Y21Kui-rBz55CiaqgiDw<xU&xnF=kg25yxkS~F8d>yn=WbIeV+QwKa%|@I~e(>e)bbObKFa)!t0CtRW<KI2P6@kPzpI#K*8{zxFk)%$1mcuIZ!qX9LYI_mB{^4DZ4o<evd5*x{m=t6%3+I#(i#r$j#eyv6lvlFd!}v;k8PJxALlV`4S<D75(^Sj_E^hp7b-BEG`_CL>@C_`)VBk4D^<!6dB|p|n_k~!ZGEUJ~d&wi}Yql{iRZ&GX+!iB<aTD1w!O)zn1(7{L1h+J0qU*?Eyc@+uNCXT@Y(U{a+(4z0=YnQUOkKni9PK@Dk393zwcy9_J{5BT(kp27&oq&lBt%kG6}`%X-EotQsn&s^4}*>hFaxAK!+p5|bu)(0l&?#MLdbJ2(K%6N*%)Oe(fDtPfla;ECL=Gt5IEy0HPc}p&dvJe?DD}M3i)`ED9p1%EmB-5dvaHk=%6XBEZCA!+DvVhTb&M4LE+N4aK3_C5q%jrQAoTEK)$9r`Dv6?@?h?a^j0NygKJP7T0zNX`rd*AK#9df5ooOg1xDyQ`P$)(TPv1P=<}<8gRO9b#7h#6{HK`o6)ESj=~XZ&gE<#hINDQyxY*(A1Lsj%HCE>~o!7_MbjX6lj2+|+C;UFWq!Ij$PqZ?0T2rnJLu^EzP{E?ee_U^n=i;nZjXukAb0Dy#L@G1rI50c>nSD-r{AQvmrfB{n)K^q0DoUK>iX$Eq{>~|(ceFQLgfnh358RTEWmc9+MaDc*6FPBTDW^;cb>M05gl0Pe+z6>5^OH~u_OI`;TD6{MNg<Ewuf?GwRiXG>%&1dZ3dqe%V|H_P#=!n|_~GrlKYZ;npgeOy4~u7syO#vRetf0703qlggC`qS<-|BYt~jv1%jY8tx5njgbWuE_GW;QR39zhEhe8*PJO<TE@hIGoIe*vj4=E)h1WkuA5JoP~4CaM#74YNnXk7agS`k$pz3u{<K=1Z$4d&v|AJ=7ydn_0yF!s&%r^1lx^Z<V?2>=liq!C^Kr9QNN5iDOxnWV|^X1P;*u0Ww;h%=}TSexHai2jkIhvJTy4Om*{7JU@N`$U%!CvRdn6gj3Y^PF_+0E>ToEyWweUI|fe?*eGPWDx20f<_3|XG97|*?t@?k|NM}qw|f_opL5G67yz!3rC-?pw(9uL6HGEfH|<|1%8n-uglRPRXkw{4?<cgKxHz0$@T!l5zr2%teS$9cEmH$J|i`?1>kt@Y7<KQVW;7Z7=w1|*Lx>^(`%@bAR`&O<UTF4pFfLWClbDsVIZcII}nA}ksqekM%@0&wGnH#;ig$90lm~Q!ojUZK&~HZ1sDA04iFBU9N=e%U*ibjR}1|}bH5SSJb-GJ<B9K*``m<VfAc&Q8Zlm@1sYqO0C8SlvubczZHm$4Q30)=Tsb#nJa!+hYLA>+-8;aAnJl{v;;a@e=>*%r1Bmt`D{)`0`iUT>@6VM90iEJ+*1U6763v4z)*dn|sdl#_Xb`JNP|+8QycQgh<yq)P?isf$KvImcU4dW4PWC8RmdRvcDiD6eUU>OCZz2l=J0_oNy*O)+Om+|OhP}+_#FmYD<7Bl}BIwRy57NY83Iu`D@Bpvc<^=t`LuQo<RNv+lfr=wjH)b5dzEX%AB5%W_8RXDTBDz+Lz{aTFqn75f+vS0tQFUVo04`xX%o+`m>E-1zc>4jIgtn{cUe);qqs?>ErZ)IJ*Xuf?BS^F^w6RYfQk<!(33go1KpTiW0opG`db>?#ojuSD8@$fXo`O<=*pf<T%BIi_HS1lK&~mjoJI=#2gCLM$k`1nWN-y*`L}5(8bY4{q!LkTTu{~*l8Jr;@hM@@R-tb)QeojiFcADzDI*m8>yo-`<ykHWslmV|(LrZ1x$}?S$Q{+J}S>zT%P%hGYllE<4N=|-nYavKYJreS=vWawxZNW)U&<fsok2TwOvp8_^_Lcq_A}kp&5%6nu7~G=9se3vv+se>nKM-2O2NUX-0rLj9K*u8G+{20ibaV*`T(sPK>yLb?#-)*p5Q~tTM$TBGd|c~F-Wa0Y4uNUFi(5>_-K0~fRapHry4$l>p2#$(SpJCjNR^_(*zZ=+?WgxY+<$uSX*6uLqzcm>y;N0?4zcN4G)1(`4v;3;T4V}HDu!^@a&I#D$rtlU2UD*dJlc#sZbe8qqQL5S7EN_HV@S{`j^w9h<>_h>$j(&v<ZjD&i-S847!=rr&E1ax_5~RQv(4ZbbkLO5W=IF9OazGc8cdjhHPM2Cct(I{qQ;F>LIyWi1fVQQA0BQ+goSsy_BPh0cI5MR-PnQ1xzCt5wR1b>X!$GU6u?%81T+JMW8}A;z0_sO0$~dZS|3ZyLUtr?M?4jFJAWaW7IwJF5x5N8xe@%LWEZ*lzUvMOmz$O}b9|#Np<xFaGOm&_SBlK;)8stkR(p`BzI$pHsY)M5EOFxZx0{k8ZCShP*_P-{#)w{`cX21n9f)%pPrm~GpWpb@FKBkQD`Y>SJG8sX00S;=uUzt&wf$J_>Iu_HIiV5QY^1*gVa#}IM^of<<N2VVk>KUHLJ5gwo;_7-sj=7EWo&l(0@da$7vS^+o-B>BR1|z-=(~(TSTNw|tY&NOH7+sWb1rL(F!|NZQYCq$Fqq}|I3X1>zgD}@CXmif7}I*h*($t+o8lax@U?UbsnPNcb4s|J4#5#FidEs`QMZ~o7}itwbh)$7feAuKly!=lrgn=S=kF3!zc!5w$^>!4<DLwX3NT;`9FVD`ssoPazDTR#rO!TRdl%7nrr{P$^oGGJ5Z+?S1``x-uBI!_+8rbgq8c`a0p;p}XHvx|7V;i-){u>4fU!}P95@%tV^?AW2+EQ9;as?bDT~Sh!BErEd+b7~fE=|hs;e*;?6NhjKS5dv$VeN5XDPle(j>Y$pPMvHyuiG^Eh*`5fC9xpF3+|yp+(W?D%aGT;Jt9^35C}&mjN!HwWXV$4A3@JzPt1x6=F0kZ)Rb^NRpW`^|c%ZbwQ_~81cY1^wR{AX<0_1lt#0uPO1?=ucwiA$zqpSe!?NA?;PXo0dvh1G!ckKeDWNyax`~q=kT)61_5IMsf0w<!>UmLe>)9TB4~bQAZ=WOq9a*n-+6eMozKeUZ<DS>(BV#UAEgA4>%*G0kDmHbEvdpbFSmY|r3LVEZ)ZFQGz^a+%i-5?85M#nttB8A7Oi#zEEC|KVY3v+LdzIB=o0wo_{Ko-frRj2WcYQTw#0W2UHk@=vJ$B#fbqCAB`1((@WF4Lkm7%cQgo@B%OKd}$k7pXP)2`kWTI{gT0xBNUUEufG=hSEAA2gW8pv8!)pmRQl`eq8#D%<QwLnGVgciUKg?&g=JiPk8%I!c7NMVCO|A=+3Xa&J_8YVe0QnNUgM1oU51xus*SfxdY>}$%fyEZsJ+*_8X8h{OP;E@EOdvHX7LRUP2cbd`OD7{Hg{6bjBl?FM!7jE`CsV!TQ!SnoD-p*iUy0!yuHa%$>9-(uOv~FPNO6Gmi&BAPqLR&4B5`&NV^lA$-XNh{>IlDq#CDUR_A0y)?(I9f6AXO4N&PYiT*ihC|Nx6<JG<AU3*{Ip_+g+1kS9{Sw#_kY;#0E|xo{gh#!E$_rOT@U5j90Rl*GlPVqY0Y4*i30NHsp$=OtPcEWHJAqme_MJWeT6JBg7%&CsWiJv<tVofIMlPez!OvOTX;;p(BZ&_UzI~A&}hmdVlN}<)s$P-q%58O}zv|$*aGb<0~l4=Dgt6G^$eX!*ep2dTb=(g!xRDBKOEdtE}WXll_T9!rm~Wk9N645`1#&KAPX(#h(b%$VUdL^UByoj-+^(Z)D>&Ug6c?J$TlA4}QWszYwUhfZE>dqSd(6yO>9iu2(U-!GEeDSwek%(NYAPh;*|Yp@TP4Z39+S)hKYILM}6eWeXuO>6s)Vd5#YFJOcu`%l;>X)De&3B1*9-b2jtO1z((Ac7-FGB6`Kz;3=Fc#*VZ3Ub$0QyJQkZXMP1*l~3%V%DUavOVaGVVE!!`FNXN9CO|{uPqM*X3h_y;4kv{$KHp4DCFRz#eHF?dm(UXN?uX@z8-gV~$pVjous_oLv$8tcC0bOlF@s_NE-wuHF{}DhU5Jdr)>hw?n({1qrdJCFN5$JKpG@xUFj)vS|8^_BV0LqaIFuDRHGmXT8t!B^D=-St5e3CTTyd9o*eY|R$OvCGg+!yEDaj5PR1WA|dPQfC19{mF_qiaXYE2cTGHt-6!J*kzBng#*CHfG#xkhPMI5)$NSfRJG?mSm1^TNQg5pC!oBd>x2o(c3YXF^51td0OlfmXau?ppMQVVVr%mw*hJQ4A(na3m_P`wtFXw1DGK4VxmZX@-~vsa-1&lXw*t(D!{dZYV{Z#A$XXpyb)(lp;6>Ai9=Jxm1Mi+`KpD*u&$PU?Hr3WK%|t7S^@;)nwHfF5cvx-Z2|XWofq`3$ihE3g?rvcnu#qGoo=XKHVT+;1Z0NOHpzCcomg%Ge~A^zv3LSTd=h%)$Q}R-qpaJB8wR}IiffL=Y%SjjB7$M4+)kzV$6k|Va{zqu&srCZp_20Sj3b!L~*P%|3MizOJYh|bw=rSW=U!+NK=g&)_<!yBRfv4%i1|LZ0D{&`v$l=wL-K7*o0%xZ;8w!#fWMJX*Xr0r>CRLvP;w;)79;;Ax3#XM#UiLI~3y;hAJ1p4xbjWEeGdL9=uebZ0B2Tr<=FxfDjv-2c<g1omk+_#;qU-KDJ;>y~mU9(XvJ>tQ$`jw*q1Bh>|)e!sv0f6_vaWA1p#Ctp#E8RYYhI0H>fGen?O$%mB(mv%*`Wy9Je5GPOM?=%d=I>Pi)@AxG+5dbFltfkUE84LcJ;CCCBc<c0CF-$lH^T5~>Ou@@DqidU!8khG_c<RS5bTEj6@XpLqy(VkS@Cu>A0oePAo6?)4Ao8nc`YpNX6I`j*^LZL?;AFyw$yv(xEmClt^2ch0w4S$XO8a=(8LPv%(;eWtUJpdK7&{1{W0zMM4`l)BiD)3ofG72t9W|z|wcDY?{A3B;KVxm<ln$5mYjXHp2db%ltiu`bRm3^Tbt5~xm7`N54CRaUfxJO85kZ|=)sWGwo$6Af@a)ZAd;$IQ8D}o@<*)Son>q0?WohjgC*GZQkY9vi5)#2XEKKVl3O#^%@b`jt<1YQ|AbHh6n4uS^Nc~+>Usd^{IwA^&NpFE$;k`vIQ`$Ytl<K-N7|1nAZ7EzD|m9}DpGWUpeD3W{$`ygyAO1XOyyf(W9-PIbo2Q{?IH#rxlHRbzv^Kj2d_#!oBY5_7>i0NxLDQkrqv5Iyf>NlGoSgP{Cp_=hj2TlwyH@~CxJ1X=>s(<4@m1yeCg2W+!g)-CZR7@WB*Kb&tDU4}5C=^cXoOvy4!^GRrYoWX9&Tg!OdMnP?t2QB_h&o`-6(a=kGDf`|0!ZUd3>Zp9!zn=*2hr?IWzZ%30{JNG#Afk{m~%>+rUjm?O}ZD@XOKydB#OdAo{%<x`T!y~uUXnt_2Sj9%3mrK#QCzs1Q8gJ&TcT2K&c$7o|BFu^jTaLqUAlQpsz}48n7@v(&pN8O|fNKc9A34fZHO<R$N}yMVRqjd~i3ZA2eXM*zVYuwMzfwI*G1R)xVhxs43b~Vnk^n>vg$Fv(ZD3rx_EiDCPs~@}fB+OD$a%+AFprV@wZ6jv&+9fqkb|=XWI1ZOIle=}A61QPZ`gjcG}SA7k4&V+IG8$|K}2w3Xs(wg7e+;L+^S{UhzDEoqa<UBJ9*sAQK(s*}r)@ofUcQwqqk=_rClNrlEM0e&=TY&v{3Uwp%;&<_23PaaVVONAsJGj`=>(V28=iE2#6YDrgyI5yyhRtWaeqhaYe)<>db=H%jfaTUF8Kwh8@y#c&uyP`~B5F>)V#T3SHn~F$fC%rzvodH;MYa=#8_nIp!#m>=;jp8?jk3nypKEwv2k^|~4XO-M>Pwuy3s}0@L_DF9%u6VWBO8a-`y+v%%1xl<ql7M(*67e(o>S%<Xz&8N?tP;Xf>$+=Cjq26kNzXd?VJ>*Iq0#cDtz7lw?f&%P{hQCPKP{}=U{gCKFiZVOU!#bVsv0m(u_>G3C9t}x2`<fG1tEZx5J@#Qqp>xhYt8AVfKD{0>M?IB2oY1c*4af0Pglf08Uk0o;&sGtS)GknHD$798j4(A88BCZ!ES;ehLyC@Ast>~Clx6@bPy;<48j$T!2ab~C4Z<^DNz)j3zNCbx$#P=RC!wUxB||eVD~h2zK}PN7S5P0EU7FIiPL+PUWJC$OaPrZK?-Mb+Qm0HU!t)mzabfklNu6nwHAb&%Jp{en6w(cURtW=1!2jr5p2mrGVxzh5gQ#^^2=-3Z5r*3b$ciiJDtRW1kt++><%}M^toHm5TD=-3Vt4|`Sv&*!=THjY5i6`WV+Clne4scZjC)fCEoMS)s*FvM2`H^cL_E<-p#bXAJeL-7oi5wCcd}lVrJ7FwUZ@3Macpx$t|ST&izH;R7F}^EJjM}E!q3Nngo;G{-$8EYm37M(6K<v;wV1Y;;-hE6P|=4r<A=)l?lkC+Qgb!$QPV@!1ho#L0Uup{BYM0`@*X(EctgdKc@gk#MRTPpJUl}zdDoVSf$T5r)rAeSga_P3dT4JExet?gfNGpwZe7g;wwnCqu6awQnO%$2D<#2Xu*_1z(`8y$RTmfU%%;GsYeo{<T2n3;h)SFk{2X#1lWNB`S6u{qu}XWWR6LG)HR3TCWpLq1`?_KUJr1rXzdFhneg*Wq~uwsdAvln1gS&IJFe8s8a0M}6s1jQvnv9XcVCyemf}i4<(o-7&9scflzWMa;zf)lLdYEg+({?J!~*qwS>VQ~Hf?4M&CY2a2GB=;lT=w00uco<qGKG*SrlcAVsIS&$4Io<A7>!qr4CDmSDD)0`)IX-rbX<73{oHMoPq1oB$pC#`_pml3YbS|i&P^rB`Pif27PX}xn6)lZIVH4hS8(vm1pmF`MWN3`E$@Bo#P&B09dScldS+HucX%^(G;n&>*N}>j9Qf;Ib)`PRbR=|tyzid3bZHezb%PZB@5%oYrDMyccf;NaQr3tXjD$Sf!rbc+$L9zLR4r=lg*c9RCvG8nI|KDJK0nPot(@sp08j9t*p({%U}qrbtXyOY)TTOhQOI$m=?)>Z3VZUDvsS@&(w|9R4)KmYXL0T$O<W<RhzO`ntSL1K+44s{6<+;%gA_ODx6Y|O&{$^AV*7BE)4@~@e6Y&_fGs>i7w+;k1JgVMM|R=U{kWIBb7(tA9l61Ue#-gSyw<yOs-eWWO9*w`KxH@scogorVJIWW;IH6xF8GWkWcsE$_h5Bl#|hf$H|Q<QsM>CF;x_3)jKwOw6;iA@r))&)k%mN!7zIM`T0p4DOS{oXi~P;S9TkMQ${iBL+zCh`B*&#V<W~>Reag(k%@2RXRqD!(FX1QA&LmE9TB-vkn12a_}#gL)=!C1n}Nc5bRWY>OF2!$Y^k&q^GfC4GZ)`g1^N|=1!vUcb*cC%r(s&jA;AsRrn6dz*V$G!)Y$QyY5y`#JQz7ALX1w<IoW!y=PNRSILdmZydowebjwK?Gh|G`79-_9O7Vg43PevuRa?ujF9j}oZ>j_Pgu|xU1}-y)*ef6GrqCF!BThA_YoRkM7<UO#e1-V84bv`RhXA}QVgPMmmg1{?HG3YNjzVGLKJb~5Df&5h@-2hIDn+v-gQ*!>yIlqfHEUs(S+7Z5A627BkPpsx(A9>z(W6Aa^Ubx4DsN_>8#-7{t_z`@4^~Hu1Z^r^TGS+iu6C9f__;dWCTSK{2a8@$n6Q|d4~&9})e^#N31Vb299FgdP$H<-{vqid1xCSfxdnwS=YomE1Ud_B1x`?~64_tKWdpP;>fwQc#Y&yu?U@m-&2JCka+?WqRtjM~o*&}ky##lpE_zZM!E^NsWaOGWxA)CJRfH)F3}&{#&8Ud_UAQ70&{CKhbfaY#;1QL20jj{xQ-FFFp&dtS987*$R!GWX_LO#}brJ*)USaXMa)aGyVYGfnvN#G|<S2H611yztys0+5_Cx9Dj4-8q$^vs8^6_#x?gV<OxPDu%XgHsPlSb)(UX5i20x=1;)(yn!Zb=6#M_)*X886KZ#l+qVlwDnVVrLoD##%X;FDor3!TYG-wV^O}rZxy%7`|LHidNT<QFe;vngz1)&I~jnv^kwJMdhwaJgXh^jx}Fp;X&m7G{w}DjU|$Vz~YhRQfQH>AoJp(py$T+FzINb;u=Wsv9xefog{>UDq3um<wr0UYkzw%+9r=^p|azgkiljIggu$CsgND3G)=r(4(-eHKfM3+L|+<NzYN4yHz{Q7F?p=`2P$3KroHhvX+R%+94ZribbED<tcluCq2t}y$Y!@~jK3**Hkzcb)u>-p<L*XjBY+!xMlcSX0F>P$MiD{?D`-Rs3ol*QD`Z5O`jo(;ZcRiw&huicRx^V=1Ofi)7M@iiQiGHZO-{9(u?JF-{)y2U;u)yCF<~ueW>PT}LCdqflsPE1wiJS7>&9udkGiz;2+lc<E)7Z0(Sj(CfmyP&-L|DpX^fF#Ze$H$3?|a)4t%Z|cdfpX<rwoZG_;v4IbBYZD>B%bD}W><4~vV_WPZV&l&e@r_rU~T*5#f1(B`gk<4Y{rR?qQ&ljZ_?0CNtO1B0X#&bh`vs%V-)mz3Jr(cMuXC##{*So4jG2yg_m(~__tcbcl|D*l3R5lAC|=-1HG|8zv5h`o>&Z{G7YNl{LA_Noc%&0QIHdqh)|+p~rqdN>yQ?Q~P7Ln9~;{gh8DZ8EsVk<9TdL61A#D^YejSVNn*#FG|Dg2su@)-EyBQ~sT^!Fp2gGqk<N31QG@{H8czej=N89-XN_G?yZ#R5P}*s6CNn8dr3-_#6^av06OU%N2J<zPFQ8k<OCYV7MkR<}kqwDt4a7GWY&uf}7ij%V~b-sk;I;SX)xquEXpW6$_V&Aw%owsvI3whq+^Nwdi7jc~@J&3p$HthsxCH*D(bHQ;5~uhaS%nRoF$0%Hu60L}b+^>la0CZH((+i9oW1yK>)kM&TN3zqwRN4&vv9a9xh+szTz@J$u(6&mx*e9|6G?yQ2E+bS}SK65bu4A$_9OR5}q9_6O9Bt;ClyuY{YW9uDO*Qw->zBh>u7q$niEq{4un(xn2N278}g$&l!jKtCm9q*hI>aCU_vD@}Sv6LVNYS6)Nr6m_??U-5-US5-DQHunUZ2TlvSG7g_?3uzuFX&CeVpQdnD+JqpUz=GI*UZWa`UkTINs)szPVV<`j^5$EGz^;puU(?uLCmj;bFZgw%D8q%Yu1xVdn8le=U)Ls_q=-8J0Q$xhz_>&fPgP{dSudxu%R7kqmX=6qh!v`fcasydbBifO-x{mG6WxUD(7YV0r<5mHW#$#<yaB7#6lvq=Xe~jZmB7sYi?-wvWD@Yh9CxhMhSBdSWRoF_^~Dr#f-(D)q9I{T3*x^Hy)dPcM>l#(eQva9EaOds{08HY>g!DfL!zB4>Gy#{!=(Kf_P~UIP8&82w6P;>FQAPsB)TbqrcDtsnyM+mvWm#Rv72jUpi<Fjk7$-O7Y^Dqrkd7jKh}CiSZzjFsh11%fP9kEqf3|KwU}o9*<PF#PVS_A+rZ4DNkv-T;gTWexlp~qFp0;D{?@n}0c2<D>f(jqev82UvdX#Sm>y6LPaj9UW?}C2#&;55Sv~w#lHimMep35b;Bi?MjS=z(X%g8pnq?$R#e0*(b@f7?i03LxlnhcVLn&QMC_z`ptk}-JD!@}heeZ0gi9V($sc5e>imUJ>E|7*%MWz+9+geRGvYsgfuU(i9zYr3eSWuCOoKW@pFCQkiB^3ENIa;6|wyLrp>(EKJfWQiT0hLwywb+`;$%DeO)vtcfB0`eFjk|gmEH&k{#t>2SY#7s;7yl5Ih;x3EO(q>Ei^<eT>KZ95s&_iFr$$AUs>+>T3f6713;>a3*M&+eHPSX4wX74nTvay#)6^80>CN`B2E1EiOYQ=TT9~96;xa(n4IMTB^j3>bZ6TvVVLWMP2KlSJdb1!ErSj_08gkt#3W25onlMErhCjIA%4Nkg)nQ56ER=~IOC7g#J!Dq$Tv}A4!_5RJ2k#7tYCCgDtyUwI1k@0+am-4YSulNt&`u9K)hoy_Lz?`$Rb{aXn_#U4cZ9I!=F@pnR6`NY3&XZ@tS@7>BuTBG-#&*DfB;lMQOPsWeL_1s9kFnj;B?TXCZg~=HU)cJWj2Aje^;|kIYzA}KkCZ1`HVytm9`3PRie}!BfkW%q86xX7lxJG-NHIKJPDQ5TJ|{kQ^5>jya-w6S!d=Lg?J@j(k(2PcDu57WiR=h59_Csiv*uOPsib86wt@phsnBHx@z6mCh!x36$Ff{dI|K@PWlyUScRhUt`aI$wIu9nHKR*97m3cHXqJoF)Y3*~J<3kEyzGYRj3|e1zBJdP_64stX(~0-#!$>N0S2gQASp|L27kF0pV?H)L<opq>ihuHM_wCZ`1bp1nir*3h5$qXz$w5kqR(o`JYPSQBnc{Iql`~e7dlVXX+(~f=ChzKG3PCjS6tLJG%Nf#F9c+&K<y;bJkRrj$2}Se7cVOa9GhM6QK5!fl0`Q0-CwxXLpujK*iX{tCO&EN>iO!2{64KaCWBY8z1Mx)+sJ)T|IM=x*EN?!Wh*IC-pz81tgLO@^jlbh{<a)3YoaJ4?b|;8$m`l5Jja?qyYl#ou(RVJ@@u&Q@DSZU8IZ&apwPt)(Ii>3v<j(+-An~?jcVT3m>|9eK0UOPcQT<9j$b;v6Sy+KSurv*On6;3Tf1}bDkepMrXZ5iN^f@xDPEe4Z`Qea>jVb7j0)#9#&*1?CL9I4Mo}!VcN-bQt>d*u!u;w{@SjRDlu6ZF+=Hn&r0A*QyjIjdIN5wxS{^f-h0+gf;Wpnbo$D}-X}}s^b>t046gi*qMUtfcv%bP!!{Fg>5B~><$!Vz')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
