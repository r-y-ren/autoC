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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-q}vU2j}ha{MoR=7Tvy%5vUlY1S52HVu7bun`EuKsE>vY#yAv1^eHlm1geTxu?3Sy3e^odI13%49R=X_vx;#uKx6YSO4+b?|=L2?^plw>FSsJ_wTPBudn{|xBve4|M~pI=Z}B;?f3us>;HcK{ORiZkAL~~{^vJ8-M_uMzIyerzq-D8y#D(2FYg{+e|+`f^Y{B7clV$Fzk7WA`}NtQ-@N+s$6scD7`){D?(N&tW4^rL$2aeGSK<R{+w}GOA9uUYE!Zxb_Wj2<Z(slVx$hr7etFu|vRSJSfBWU3{L9nJ+u!3|U5?n>`&T<OV4tpjet7rc$1nXxpZ2@=AFdwdu)=w}3Fqzb3){1Xe0|mR?8B)Ui(wtqo<Hq&ug~XbIeoA($H6qG!fwvtRr4jYeA6{*;$f$Kx_Wir4$ePb{r(^QyuSKr_x9oEtLshA0DXPMHE!Bs2ImctU48%X@odRm$CIHuD7&#-i8pwLPy6riGt#BQ$OL2c^M|Q@i&uS_ywp(5cIW+v-8=q@^k6NYG<)%39B~WO`wk=Byzlq~*ul12)9N_>=<9R6J$T-f_Fh?BS@RW5M*8qG)$<$uI<`>KBW=9z^vw3~rQ=(BTkvT3&G<oWo_*a8K>Bs<?mRv6bfmQlx;(0j&RlwU!ET+M++bV}KTW^r_*B%v(;J&l<RAr4BoDG4`Rd{A+uf@Vzy4|W?!%k6Z~pCkXwLiWSf293;{C7RJ^XT&u;wba*fi?Xb+-5hp1iXWAtum9S%{nS3l$AFI=iI((OLwjX>a=}A9oyKV7fH}(T=CuBGPVah7q*~Sv<jj?(UCG1V0}+-R(3?qeI&;{XA{mwCj5^YNj_%AByHCKNZdoYP?3`A2imY)go~8O-=*Ya`PsF7lJw8EG(=_LzYfwqPzb2f(LfioN4mgbx|Dr)*_jn2%H{sz;B`fFCVoLD$wpock5k$n*TGKMctj&7cY34r$3&iIC3+{bK6;s;S=lTb-V%M4iy@V%(c_85F4t#p}*KV*zPQh1G2HTwZ=wZ1(Py1R|i>?MR*efo*E4Dj7_jd6T7uwekubuI6f2GnE{hM`)_JL=m_{KvPRans!>yxCr1(LQ}$=Pm@2~n(9DAUdyQce;ZGkfMFT%LjZS2cihIR+FMvdWX|$<XsSsZoHbBsmIbATjaI8oyW8Q_^g=zKv!@K+a_q%uR{$e$63GH4(6wwDr`0HCZW-@B%N&MseyMJ}p5N*NfL9WRb4oj^8N9$nrOM$nwutD%wU4sFp1H5cL_VCM!k<@k*d_Y4b?Rh@><lZDLIgQHH?~A_wbjYGH8Pyav6~_;!v%PB*l-^BG#&uskU+!=TWGw9wOFr{H;J+gf-0(<9Kzt2bUk5LUg{$mDW_w2_83~%U_I_w@WatW;QMWtu3akcEe}oMTo`<CGAnn1^A1iaX<mnwAs*Uk*)=$lvRtmet6A^&rw!9TaI6S%y&~Co=nyq0E&>Y1QAqR2o>L>yVX|gjz->%7F>TzVy-t{~c?UNkuo6}^_n=S!Wqz)`{88ZVBUy^HCB%~!P+J(Ly^mJC?2`|0uj98ZXXh+p~JB3br?(vjqt~pw@-Yq`VPMjgn&#jGMaqisVqTxvVaIhY`-bd_pZr3NQ`P-3PkTfi|O_=d1M4lR&*ak_hY-&%q(NW)=26nDoP&Sfmbs<R~fH1uMbYNBne3zjE5yu)kMgqjz62#heB*60$tqtr>$1-gkm)h93&@XF#0DfyH04>0ty#r{){^MxiuCnOb2Ttv?=o<dbif)<b`MkucbS#N6&0F2f=`t%yoweb>fpPxLK-1zrNSY}|{MDTrQpZyEMgl*nypS1Ck*hHTLL|vMp;?mbnr*4fY{mfP1NOZ%xQQ(@eE<|Be{tI8&D?!q%+2l&w)hf(GwN&@Nt2B4nrdI$v)KypETb~{&SuEla{Akz%TN<QFr&M}kDfanXP|;y#^Air@vb6HB3L9fepfgAH24i`7%#aOppEbc>%!_UpwN}`hJ7K@?O>FdrP@sNO1x6j0{zzF6rC&;$p7LAy$(M$6}V>UY36GSX-h2y7eth<aiT7YK{?d8{lmlO|6V9g=}Vm9(E0`vAOe4zgDl&7txf6(T7g{N!=Up!y&0~<Vt;%8^Xn^ZnNRO%^6M+COSAwrFdKEjl)^~pceE}Ml);FMEk_+=zK&qN{Nf?fqS!wAs|+xO;Q1tGtoainp>ooq$V*(DnhUfg>LVM-V;H%=V0{3!3AsZ~>!W2-gD!;3&v2!yZV30duKj{S#i!ivC8cmW_lEdJ?GVDX4a7Ux2_GnzREM65N`Nhf)|ENhg;aO153Tdxj%oW%d)2Wf7f&1WCOGfl*5L$@eGaxWh;x9&Kj1`a=b~|Y`SA%FPd0AE$hNmbf-=;0t=-sadxZKHK@i4PFzM<C8DOep6Wtc+RRhx7+m}ohAKA;s79McPl6<3f4;lxd((S6LfV3}e2W}~?5VY=0)Q3rWbqc{ytt?A}1YY44O^fye=diaIbD8uKF+JB1MrmgwP8N+ljRfBr?n2l!#<T`ei@Y1iV2F~8naU5%vcl~Q`G61GpJ3{@y-j6jl2IjY@{Kp)x>Ki3D|;oQF*Is9q7&f!v+xy2jcy=^+pI4ZIy1L{w+IhQb0_52II}+$re#cAzFS8A_4d&Z*Rl-<*$067wuE2S2z!E@lLp`fi^U**h0dcMSLUQ=b}e(A=3{@BJn4dp6iaIlO5nz}0moLN=fr@^65lp?T=TZ#f}8+e<Xiz$fcdf4)LC1{Uvd0b0D#6w!*+!4vb2*K42HiVysvSt3IQV9^W(Hse1aPlbppNiv;1O?YJJQY1$Sx>@r%LgBCuB}0Ny;MJ^jwyIxtF0Z%Q6drIBOM0wqd=U0dKzbKyy_J&{9Rm@}~L&}&g(kB&-$F<ccE&3__|05S8YbH9%}<EJ-o|NJGA$Zb9-K`6a*+YLYTd}@qTzS=$}K#ss=fM5E7*@7c)_XZquZRWsqDx9g6piYf&>TfbA$<$at%pc^r+b9Ub)4*vTM^4A4!33?HXa*3RF;%hK?PNuwGc?O~Ic5j~+2JmS(s83CgM*nbcC@6H^(GJ1wr$|To*xNZzs72%3(YvjvlofdFetdw$<WAQCBk1FAso<15P}T3%yHn!w2bO|$<LLWZ!Lv%(Z4}cK$V_rJM7d(f(L=++O?<B64Z)~7koW$q+IDqsze=&)AfR6n2TYDeolrBz(N2A8ZpjIOjjrYUCDulY$o8@Rz@o;^8<Dbu={{~UNOT4<Xix-8JK(RdY?C{3`#S829ZvuGdKntL6VNN_z3`aGDpI*@UuPc{Cq~g9ZjHL(y(gmdB87B_^&A8zWEE9v#KZe%=3&Ya;ZqO(a^1#1Q1#=UkTH<BA|F`I@qMKYHet367KdbrJwUMe3OsZ4teW%W1j#N@wg`y+!jsO2ait-XA;{iKEREe*5Ea1{+YOVB~L=So(13oBznwV30xqWIZ>e|M2owVe%*o$t$_h<esGCpR(F5)1lka>E2nTP74~UOh0-P|MO@S2N=jHgoeBvm4LBs)RWgo(3B8nv;LybuDj{NHHXg(%WW_oZ+7G6C@t1L4Tw03K56AJ~AXrVPC=j@q7MSudj`)X%pYA_ASX~3|S7JwjgH)jr!|2ydMOL=ps9AaZ^~11PDTURVi$o#?tthZjtYn-59%(KiKY#&OR7i@QuW-idj%ZiIItZ@hR5eb`=v*$`*}98$i|-P^(WahR<>h>|Xp>bqv}503N0`bzvPRM%W3hZJDd)-}8EnJ}KMO1#oDDv%I4p(VMeLCw$-54`)+8Z|nfDgz2$shB3JiepaK_-+QjhS?29fS?On3g%WOBt|-U{V;v_@Devmx=RCB%>r{5GD}7a89Xfd7q`pY7%vT3bp6AJOf0al$B%aQ3LXu?lKNfDOk6{nQniFlGndO^;upYv_=L*;p#)j1ibxYjHk$?HUI$8dV@5DMv!w5Ve$<5llJOZ0(Fq{)&T%6Z&^*DF6h~@*rvj$1-sRy8iagG7#-m4^kA+g$B&?c~fEBe>v}$!)C}n0=#t8q0=1ie9eSRt?|PWcwzRKU3qH%on(2GZ_h0q<^@s8>Y}UFS@&Zo;KYGlLs%qFXaN_(l8!iHx`7XZww0Lp>4U|MLe3Xl52^4GQL1Gzh$aXG$tJX4puB0#y#<p&AUGK%QnMD5-!M{y_?NYgg6Orhm5^5n$S$Z0?crP~Nt*?^EUbdjVZeStc_Ea6zNdVeDn@abp@duxHXBiX&(V>d9b+W8Q4J-rd>~XN!hn>l{5}qx3_RDZ)n}O;Cc;E<AXd+Q>@u8Tb>X?30I){VkD26&T~)`EK?%IHbV;6XQ^4EpTKQ2Z7ou%x=F1p6`nI5YIs=wq`nKOwhahdCOGYB`o%%5)cYPD|HWOA1!?YQ9l9AXn+%1{kDbvc~fj1x<%gS9qiaC&{1tv45{rq%gv<@bIv|KeW%TyJ6IhaX81~p&(N)8x8<#`u(=;YtE(=T8*rk4#Z2wvp3iiY@5GfZK{=3tmlj^r$+MN1%{A08gw@4CPMUefK@wfTEovV#CItL76!fWd(BbVua9s02zz=g%S*u~ymnp#{Pjn10&=EGDZo)18x_c->V7w5nzWj}l-ti!}3GY`M-mpji-Kfs0oUC+4-`y)csMTE72TRZg_|&R1+xT4{cSpc8@{7Bumw8<1jgL#PYE<VEMBU{EddM?_87j;e1^)+>NMMvOjv(=-o3cGu1^krvZ5VC=!QVq~U<*FF!1u0hISOWw@<gJaNI*z2uyc~z5aameMKH-6menLpQ-sPWGKR5ES`GyyAyLbpN~0IcOWzdV=z$6G_eG4ZFF!euQC!7(P_w_FBxYBv`Xcex9{#JTFhHxzUU$Doh~X__)|R@SWUNgD`k2yw{`xThLA=9eV1=%pUXbgI{F5LkqQoFqRAvzlPgC|j1LgWyn$F#-yUWOcQxY3Z!eiS_+Ol6VQ7pZUaKl3A=9PNm(8II0*vU%kes*ozIE`+AXTR^$za31+HZK{TDj+UNyf0bazxK59(LAY_eZr}q5xbKFp0Bpevl<C1>-OwM*r5Z53wd8NVKAB0dzr}l)2Tmn=XkHq>%`iAYAh<2ym9U^j3U1DU%Pzg0c;lZa4r6N?JoIF<*F~svCMqKEi!*d*zOcyO2Muul>XXSccAeYWWtt^&9tilPwyb%CKD;2ajdRx;Oa@O^svHt1{@Qj4)-Fe^VY9mcTZFrkrAaTutj}W3{NB7f3oqT_9Xu5ZFphO@y&8wti7b0LI;)DD;I`0fl!H3r{TOL}=WHXz^ugJp2$t|YGo0T_7=OI+qBR#okqwu%p;lZ|Y0=?sOx0Lo^wx*TXlHXho(5vTW-sUjC9NgzZRDRb9qlSEl<0=Lg0CBIhm{?LzlprvKKu1%;T-lC%^I_zB2(m&8qd+gPF`pKrG{Su)B5ei-E67lUM*GsIrzf%RrM8r#nv!x?_C~;QT3#mCy-qDH0VpKxSPnumyyhc2E}CqKkxKBC=pA(I6^4?jJiM&kFI|EDeUh6h5dl#!7-hm!C=@$sxs3okGAa=OU0Q0$AEsl@7&{|#o(#((&!M`nFmBSa29*9Vgjm-^O2Q1{l#iMqcZORqv+-E551;4ZQae!sCpk6zga*SEB)1B8T8zps9eL0c?nV4ckhuoZ{cTZhcob|}k8*1p0U4AkiKQut5zGCK_sDz*?mEF7a3(UdPTZ}!%7u$g1{6Xt0ykw6waMrbwh~q6Clf3Yax-DUoM<6+w$CkZGxvm$uH7{1`Z{LSANGU^A1#YC3#@?Kg#$&})r$Sw3S~~|flvSpkpO8-$jv~t2HM*-caOcmU1WMb6(6q?zEh-+8di5);7^6#3F;j+OC?dr8Qblk%+VCOCrU31kC@(Iq`Z1yp<g7cG??%gJ~`UdM6-a6JxSqV8peK_CNvfnpl+WVW#bo0IgAkN6853ar*#c{XD5L?Ks!5wyI{5+U!K%5be{!4h9VqMV{b^7hea*qO#`!wX?#({Gesq2B}W6?2>6JEIECyZbOH?88xrC&xb2yolk?N<iMNFhgwb?Ta2=QhPX>^R=v~BW3ECwQ6XwFp4kx|YP9~)jo@TJNcY==5gEhw-e3hjwZY8JyM5S>C^w3ufR8|g$nP~o}0l}>^nOW3_v=dPe825%lV_z-e@BAQ%39x|NI(kZo05AyA6J;(dR#X(>BSlzw>TwM!?k8nuC=_hnnf)a7=K2M~0vMj6iUG|orbtBbl)n1UF8o!E8!#$moWQ^d5_&uEgb*yaXd<L$edtm(&8J1_cs<Q<`7Pj^7ozYZF|yi2zlo5Pak)TPcvCFTIjeHlia!Ylnrr6@*|%1F*aSCqCh}q=4*jB~J|$2KZpdJC@{ndBrIgpbXlD`^UQ_bs2KOx%)+qFf)CZiyO?H|fF<n^V>AhKr(Fl0leDj#eBNZ>?5t~Z!PGvP^X3tLKrkGIcn!`kBTFxXA&Cc}3D!f9ZF-tk-I6tEil&)6&wt0L(R$$Br1XzXCi)?qh;xkDalv^gi5rPOhJBn$v0Q77Ub;{47eM^N>+68Ws%goD<;V{LNcd$6Yd4mI!9HRD#>48I)A)TWF4-UVH%A~CzO+_jdSZf`uqSQ7`-DD$$t;j*0OK#7Qv?BXu4156>yDJlcx7%3`>6;%ez_z9CG}|V}=0T@NvD6s&J7#jMMT1LEFI#A;?y~@2wQFAo8KO02y-}ts7?9ih(LPeufab@Fd;*>pD!9lwR1AuJ^LiRFmdB$&j05828H7$0RhH}d)CCt`gxj`xj@-74j!})$)~i2PCba>rIYDo$p+WVO-)*HNM2Upp=hG@vMka~SGm=3|U0QR!d3~mWPEvKQm-AL~`{Og8;tBTxXW6X6ffI`2<0_XWzOEH#Xx%B0!pGKDe&ck~zj{HLeImQMutUiD@{;de(_zGBz_H|3H9*)al3_DWL-7JKc~rxi#nE}x)4NXQ!N38$Hy;%?RTJVPn{gb+<@sdv^hhw3KwI7nI}wYn{6s@}FTuBx_7ANeVahJGogbdCMuio)LCg@~Rb@Hb6$)AatOyjWGK-BX-oOY(trV^EZm$4B=@!ds5`{Ziv{C1H0=Z(+C(38=o7|J+hg{#3$SXYyhs&qZ=pw?f+&Uoh-#fyu1~@s2;O5c1jt!%RxO0JJ`C?)-m6o1~T)P%AU&*jryB~glck)O<J)ETxAeaV&&PadnEjAG;Dm-fxF!^P%2E~c1_SC4LjZyH*8$DRyHh~4MAYlh^2A1JpQ?$QG7OV8hKz3`w@Ed~aIRbV7`74);7>(dXB6&);$hl3ecxV~YSTEhxO_y}jIYw?Qzi<cjg}8)wVP{aS@m*Xk%z#P6N*%dB3T#1VBT(wk<&i#!7__jk89b?;={Dfkhb5R?VOmNJX7>pBo1V+FMGSm72AZ5Iygn%)iuV!N`<N$(j?NZ@r1}qLa*P&u$jF*0z`_@=H<(N9uM8F8XMQxvxn#Mxsf?`wbU*h7Hj#Ro-?z80>)wj3u_KZzb>oo4a&;lSa;u4wN2XRDK0xZEQA$jTH=s-ZIwDX!e|g=4NoZnJD^zF_Kv3q&Gl2q?k(Y%D_YSB@&#;gXCBVQ4HFNafGzOL{0cDnP?M^2Z)d)7vJCXFRo=Cb1zBM8<bWc%*MARbA5-k=_T{Zbr-XZvS%lR$?(m}T(9ki&94wgnf^Ae^(2<5cyOi`3V8SU3?CU-s|oK|u$i&PzAP#by;Zbyqi4WlUHG%L^^Vc>PAUO1?Y+D1onjVauDk|1n{%tb9%Az+be74zb6QoD;NZ!dpqL}VJ&RxT7L6(#;~s5`k?a`JUxIub=)@Gc4cuT{kCjF<^zeL^tASXRTyHk!W0Fq@d`rVbQVLVCoOaRnI_p{AV^fPQqlrcN?yQOZs1dXWS*1}fhN>Bd5i(nkp?a8;zKk^HzIvZ7gPZU1Y94HWL&%4U~HYfOkrF1O%5Avz1dn#zgqRXS-(RcXM%xTS>HY4?(41yo%O*rs+&zu1t;g4HQa1q0tVGAk&Pi!#J?rG>4_Tw~feX8lux1i4pbpO^!F<VPbG(p*;l0MljQVf)Tv0AsYz&evT(jm@mEdix9sY%!aPp?J5!S(_xTt(KX3`_ybSgLoG8ww!y4Vz{0fInqaHbfzxGO!Ijl$;?fglcu5iT&ii#JW0qO+0_<CW|~q<IRgvkzRn9ykvvi%=EzwPZh61UQqH(uD{y5Q_pGu52+T^EKNJGs{4-<S_m$iOD5tb5OF3}8o1yBB3E#r7r)f^Dcdr&T&5)zW^B#bF6WHI<08V68GiF#Qebr)wJ4rCj9RB2}1l!W_lN9nmtIw`ReYcAgpfgkYjFxFp$~X2I@ZtahTgAc8d}04i5|*UO@N|CD5~*YeBbV0YyVLqWLT3rgn9v_}lTpjaD`UJk>4~Y>OUVB1*HnwoF{c-bq2`r%TR~|pSI~oUu3Uf*tVnY!rE@jS0-b!@Qxk=rK@|3SISTgDRb6c%fn1q~jM2boH3aW`@f@+OMETKB7eRR)>(>%}VX?3{wP!>H(UEyz0^+g*%vu5JsWUBIowP_ye3&8{F!__f8nnqWNn%yqnS2T|<4iHm(H|$162QQGg@J|0t8onAj1<M~_acY|Fw(-Vq2<JoJbFS|#$}hSxM@5B9&|Cm3c0j4piQjv3h}i#D)YwJ9(E_hhkhN!cM%=M4~tV6vs!4MNBiBw7fCoD9zIUO;csyemyvpcg44Jr?5JEaR-RARf1}546}%c(Lo%0{$!fBSNn&Q%zDK^B#uXAubKIl!SScc<1ieCHjbvX0Zi^(Mv}HJlq*d}hMWqi6{&ylj^rpV2X=*xQ1I-RI#=(VF19h(IT~UjUY3cf9N&5Mo!Re#0VF3gq>?8`fAZyZK2iA&i76Sf>>{zFk@+4~sz^ag;lrP5NN&K~0ynYBkvTU?$LY1QQ^qG{ms_v~Ue17{J@+4sfHK&_-72RPs+6+jO=e5<et2#-kbwZTs#SywxLL{SsBpBMN#R!ey2VcrBWYXi(>Pr}d8B$@Mm8E>c-ULW~dB7VLx%`TXWmgLWr<Ol!EaH~P0qagr;}TjHGe9f(YMuVnc41_~yx5vdU&-$T871@c7->*M<aV`NBA1T98F;{KHR`@&gU>T7SBm4blvfM{=n4%%iAgGNJsh2m@&^2SvGLcDe+Yh7@f3kOpPbM=A$<h6nym+AJCbYBSBN-`;@B`LIzkLC9ubKI7PBA%i2$W;3tv250$Hqni|gUdqTf!o4qM%x-~cYsiMF<4%tOb{Af-h**mDP|H&YSMs8XxrmcibrFJR<fm2pY0HV%c6_pxo4)UM0Ldc9>!fZ?eAC-Ibkw`QVYE~>{5Cko4TXO{3V4TZ{H*htwoDe1A<8FPe7Tq+y5#R_!?;^LCCufjSwZI+lq*5(>s&xjSaDHrZE`H$<SI*KBkz7dwioi>IH&#)}VO^Cq>wfDr)5whi;A^{RBkPwr_nDkI8zb3(t$YXAeL(lk9Hr2o!uyF4sM4`<jeOV~7ng!|VT!X#=lbkAA`kSen_QQx>Oy`D*b;q?7Yk7};?M9ZDlT0z{$^qs{k8;)X(r@i~UftzG)Q~a+Dp@K)FMXpd?SMou?7czH+p8WDiwi|o`q0cUMiP^8VX*e-3Jvd{i_yh6pTgbwUR-q)FC(GXPqSauRp;Q|BbFQ|N2gAOy^nKCwwn#r@I5Z=m5|3=SX8asQ$=lqSdW*_76>LLFs+>{W8)qNO){dHu|=zQC|duB++&h>7=lH(D<V~yk?cg#(HsT}ZygbIg_}HDa6(96Ktl3Sn=eCWWTjpv>`9B&b<`ap*^`lu|Ba2ZfxbswkoV0m_wV0l(kk(V=LGFu1W>*s=Kjxxz4?5ro^qM1C1zekYiyH1;P`H-Rk>^%UaD>IN2zof#5!|oVx5I80X{%T=$th2)Crl1<kEFi#5%>p7>-kbHuhn7VGQx1I&#!yHt0EI15`a{fK^h$Aow991lG$~CSX=LHtG7|rP&-o(WHKdtR$*7b#=uHB{MBapDIz$k(U16P+vb$p`Ak}W?iz%y<jGV28a>|>13%KLkndnMoABx$o~e{FrxoiCT$UZ^nvP#3FIcMa#3k=Dv671?_pl__>a88<(WGG*=j(aXe(19Xd<OJ-ai9E4QY*`HmO@k33O!uyYLd=*>JPFyly315Z|M2=DQQx7@^A5G~BKVt1_LznV2NlOvI#Z#D0zdrsEy8sfP}^An;=LkC2jBrr_kYd1=Qk{UMPemg%^$7+XkN`}j9=G-NwmpI$iwOq)KC_Szb#^W{lfK-kh2v=O{5oq}hF-dP5$XOMQg&KbbS=L9Vvpxi~NPzYZIOjW+}sat-A686FwAEMo1=)87`bw#=sC5Pt1RxQ@Xa`+<m(Jd62*ksu>vrSK2xGI=VjU{TD<+2Xzjwa*00jtOY<vl1*Gnn&v%4U5i=12&*$v#9%g7VPN7Uf|JP*dyBj$-MU$|Ft!s;xb1Nl#2x>NW`X_M?ARJ$gZu;M0`_&Tcz_Gq7mcJPE`^`DGkNbaL~)OKIbHSwA=lFX$HqqPuHtlE9rn)3mJBwUK-q<3%}}ka8I)DCL!%Gl9ajNM!K5MvGsTcTi6<_+rt<a7C1CM%+@&9?2{+Z_-ze>aG77?R3{DX9yk;n34>#4y`qsLCWI<44I_6k!q42c8{#?=}D(Bsg)?rREamtX6Q@D+05L5WW=rvOb%DlTuhhRXy=$tef%dNcx^+dE~B$WC|-`UGM3|Ii*p4*$S#uCIdDl0>hB(V3gWfj(6r*`!0QSFtO*KUraWXf!@_daRVbS>jTT{)(FGyRz-r1p9>m{r`8dGiZFN2@AF#Fs_IaL`Q|eJf?BlNnI6rOD7~l+<Xj{v)X_Ia)Q0~z=;aRQFocfz6PInxr6|*2|@v2=^q@9XE37MB#88xkw*O?t}Xg9B%N5_~?;=16|FmnIc^gBVAYpo8-kR(Pl)uIu!qQG%!Zv$BP7c)Hreryhyrm#IT1Z1vmC4XlqEmM_FKrR^B4^k4iE9z9JZm9HCy_`8CerSvQkxV{OaSnE1njmEXCb05cfY8k4wF<k~(5wj9bf}ks{U01m?2=NEnfN^DNk#lFC3=-A4cf8@6UdTV$<gJC*$Il<w4N<KC!L8)&@{aK?Jz_0X7${}?Q?{#v<S#^z^U@GVEY2^BTFhf=DA)-{>wN}Dq2NPf^Ja}u$_^3wh!tH^cIY?mA>==9sJ?Z^uB1OVoBO7ppw;9xeFV`RPah@>va3P38tt*U6JSt1(-lsu$YSIm+JG`lMV?8@8X0+)<_|iX`4j$2hU|RGaYRf;VIlvHmkv!QL7LJ40wqFnCz3sF48$KEv91ezT(jIFb@YVu=DV|iCAcg34R*HMOI9BWVth*l(rynQR0!OwB3#TaYw_~4`;=@jm^}XXX_@^$vkHaLO2j0<9I8sJ<WbUZnAu>$jIY&_dKiA<Z*ivxIs*Yvd%PE7cZ+W<+0ET#VEWGuz{~_%QiC&;xQbvPt9>8sh$$G6p7d?b-?3xSy3-#gF@0PKXNDN7AUxh@{&o^i1V^E;>krjnM{|%E%ea!XV1#&_O*PVrM;p%QY<$EQ!K$YENOF9O9ghbxWe_;J-dYT1%cr{ehV{UOo%PX&(a>iIeRGwwiF9S%5{V+vfuz8mM%GD6QPh%OG=ivWgk<@s$t_ua9?ADBdPz6RXwW3X+)M)jD4kAtp!FL6LdE7GIzqb5Ip9L>GWEJjNqWl)Jrp6;+EplQT5Tx#$w5Kw{-x`(qpF5YXM6huAAO;EeJcg3f+mRi0g^DWgEZjf}5(k5U+S2ZBJGCkR}GQqSG<mMAVMlh2;Ops1MLt>o`|x&{FFiG$XGspidb}4<lJQG{1#Q*d+4wHUJ=!xkp+xO_WF3>l|bc5^2qDxh`ZP@d<o8j`sAyPR7kjPU&$>R5EIrH|Sh(XhX+q=nfHR3=wmsxX!7*phuc(Sb#(~eZ*fE%6CN0jC0UJJ?|V^)Lj7hY|7O~JqH#1);?rV!LB!?ri2OcG+0l==qdZEhG)%#3qvKeoMfqUg3~s>Xa%6#QkWX-Y6x;uaJL65n9FK%0y>d8Q$9EacBZyXnSMuBqS0gv_X9po8Rfk2ZW4vS+kqQ-%4$vMswMP+gpm(zroEMfrBkkNlZhgJV7N`{Plz2<y#O`oCp*XUaXqekAT=PR^>l?9u0-I4Q(f0PSP-UkKu|Aiz|G5j-`q-(8PGHysL)7}X;w=RNF31`)T8?&v$nZ>DfT^7P@k%QI07>bBTFo8hU;adZDj#GQ`)nj7FPG!E$~KJRaE(e3(X|p`ROg7N|#xJEvdQE>EE)NHMHsYtl@EmZd8Zo8qxM@jAeO_S2pg(GExAz*Df5es1lVjGL}^e)<LI@&~@Lrf?Z}F&e=lWrXvUvIJY#O_Q}g>4mL0_hqG`PE-QyOU~#$HS5{%iv$LNGpMU43r!`lfJ-+Ao){_%@d<X%CHXU2Jy$#NXw$hs;lG8jXlMm|j$PGV>na)X5xL&r`Y&JKvjlia`Ge(uIzt=x3k`aW`Vss$s-xvb2C}4!4)Rcr$beZ;MWO7g4K2PhUSgOZgR8p3<XI<@m?@UtzQniAzwuDlN@TM}SPp<4{T3xq_PMdKq8p_GEliKpe41}j&u0hPVpoN%)Y3ZPJFAZFPHMtFCb4yRGWn12)G5(|tOB+b-RIoUfe2H8|=bXu1<qvAjO!Ubf`nnIn>2;*p(T~ja&7h-=Yv{EdL)INbW;*+o0>BRKC`?1Uv0E6Szqw<rYr)&x#oKt{j;ForJGUo{!%Ul6`^t3S<o<rFs6wPZP+Z(Tl)mscwo0kzz^Z)w`{Vxuew7pc')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
