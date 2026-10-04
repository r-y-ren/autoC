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

# Public demonstration plus local stock/budget/weed guards; a proxy only.
import base64,json,zlib
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rM%%Z^;has3yrxsa{djCa&bNkfPl4oHp*@?ancunYr+ypX*!{O_iwyKhz9JaOVgWMtmF^sdp5>Z-h%k?}Z>pZ@37zy0}dfBnnfUj5TgufBi(;nR1oet!Mx-~ard|N38_zw`OazyA4e|M8dq{`~b%uYU96AOG~``?r61^X}E_SKqw9zIy!+KfiwZ_Q%WR+t1(p!{y!k@BMFs7y0h(hs!Jc#lv5G{O)r3VgEPyH-7%#*Yv~v^y-JV-~9f^A9k<Gzj=Gd`){>t^}~nv-~RZ`r_aA~{qFMS)7=7`^C$bqwp-xq<>RNv_5IC{Z{L0Uryt&Y{Pg4VliC*T`L)0L`!`>n%*#tWuH?tdyLWeQ=2v7Bp)KdW$sgXm`R1~F+|R#t_r>#jY#;LT|9gIWzuvu#Z3%a8<MTiL{?o(BK-=>6$$tCymwR|aZ2Rp$^P5kX504-Ew&b_3+NT9Rw123;LkBDT^1a(fY@dB(&9-%ES8Df$$bY!Ju{Ou;ZGL?J<MVp8?`Qj|@F{MG3qF=_KfM3p>0>-UJo-88Q-V)(?6*r^$KR88D~qDUZRbBe6E*IRT%r6rfCB_JLAz;;h*a~orI_}QKSy@<_Vm7a^Bfg!8~f?l#RAwqFr%-cC%swX?Y*KO>S2X1%(e`7*WmU&vezR)ep{{Q&n-mTm(%Dh(fz4xe%Kie`O>(bfbAOe((X0{OLB`@x7WFS&wq<eHo~5n`vz$+*}pC6`LyR`dpGFdx$p3s_wU|azWMa0-(Eg^di(C}zdSym$5=*6f~POqz4XgjxqI!`Uw{3z`@Cq}*n;H!tL86E`zP=tfoxStpkEsctwct)CBgsMeUX0j@>}ouZ0&B|9|hwe`!6kjI&cj2pxl0dE#2L61&}_(_q9>DFIk-?!oclf=f?>rqEB~6|7wcg_JjPkfwtX%YLjMT$8M7CwLu2QD)>NrxfMN4H5bZuofV{oB&f8(THe+mk%er3d^`BtO5VbQ|BygFV#Q^;H&S`>{c3EV<M!_Nn<TU&_DLSTdi(_fuWTe$uiM1NYxOkS3fwO3=dkOR&{No_T)ak<{t4Pm;QfO$pLq~>xB1IXxw{$n$050UX!4s$g}_EfrAhpy`!ZiI`2dHfC}JC_SYVO8_ip?LknWJ?aeFP}F~h)anR}$smhzUDx2KQq^0lARP3}Q`NotJ6nw(vWm91YvY@;h?o{63Xdw8|3KWyHGpPGVZxw)9+Rt{wJa2^@h6v^4-cW*xYa~r|$zsve#i*5g!9=SQSGQMKf+tJgL&}`uC@4Wouerv29G$&1%Xw1ZCtL<o>?_#-qGCHP3`8TLg*I5zm)8j!#GmyT0`umN5zuUhAD=*k{qX1RS+eLd@7f=#Kmgl*q{`l#`o9k~bA3prCZG>6##^=IO9Z)r$6{BW;`izG^T>mZrc}&~P;Q7GupG)dtwM}j|W9!;%fv#)&KDSoJT?g52#D+@lm)B|DJFf#GEeS9#y=|WDtF}M7|8Knmn6^C{8N?V1<<wBDKbIObw>PNSXiQCZ{SEInk%C>2e4J|5)|t8lmOj}%a=Q@yb5v;|$QQ#pXXb3B=hK2P4(_7nLw3PY+JDf-rby%<i6ZDCw6m%Ppl0_TGM$D;m}_;7@ceN&3e^nx)|ocSPi0ujE@}9)@^)PNf%yDF>qNMro}}Nj`q#%|ZQ{&ZCbzG)1NQVqZuEBBGq`cJE$Gu1xpV?Flpp?E&k&Io%4VXrPocu|MY5#e)1q#WyP)mPfN1WfW}<Vk%n}25I2e(q);jWdo4Qw9)iKBfl#QdJHjqL{gJoD@^c5CD`yd9SWS|&64`ywPO!WdjN8Mn!JJ0v<hdL0^0ZF0T<FH{dLy?pNGDuGEmK~|GLLL%#V&=WY_veuJhoZ97kp43am5Gi8$?pBF-log<FY{F}>a|IGTik&#j=E@L>ykrop!@noOq@72bia1<vEqTqOnOf@G@uA^O<lM`HfmLgf&WJk+c+`OsXMfbqks*-o7^4E)DE&x6M>T2K%aoq!g4g$7<O}Su)28Q#;&j(E;)&p4fWSsD0B)@-JZ%Fte7>!ds#&+CkmjOrQ(<-9$h^^){#ONexMISSCRe`5OLh20FZKTNEgZeM7gKt4=2*hn86iIesZx|t+NgSAb}_5vz^R%gVk7+lGa~l>P1%gfqQSXtlMeLShNmtXPs?xO@p05TI@;OH{-1u^;f9a0_l(#p$W!ht!gV!Q-SBgl8sx#ya^cHWdO%S?%!za-+@*z_;hXBM!LkKsm0^=1H&!j_)p3OlE0i9Ue||Wm9kJ$E^PbNnmW;U92?P20={iq2hR_|<pVdRTQBZsUnn_e9ZutSIC#k_!s&>Q5e*X)u-%x~jjj7qB}s<`#9|*um776R448edcTc&*)>tYr0uKwk0|~Dicxd!Pf}63A*33Ro3iRUu>qxzsty~j076s1_+hx*JYM_u*3jgb+?yT6+v|O(5-@nuDr+06@|Mu0)ybE?D2sjJQCOQ>VWCF}?8MDZ(%+JapWN_h$-U{1$`oLEf9e5BKbWa;(W0o(oy|<$YqBx+iu`y_lhu5AxH}P>rns#-m@`$ASai0V-ZwmOL?Lh~!<=;X>CS-F6dg6QXugI2P(yXV|_X_^LkCdmxz%)rbwe)p+B0<f)H8gzo<RjljBO}x<tj_))in;DllCWDH;5K0FKWpY&09vnLqD2HG9O{!0H(+LI{x(N#-UB3L$th55f};gGiu76Uk75~@#q91&pzyk#R@s*9K`GlC%lbhhOxFAcIM{5L?b68JmU~^QmKH8R4KdIyBW+GYGARuE8}*^JX)hUS@?NjGwXCEito0V(_uj_U`>#1RBG^;3xl3BzZU-^P$|d+kFi1kg6h9;cM5FB|>HY=)^Vr?)AToi<ac<wE6c({<ww82$5D3n-`y$F&N3TQwZ}-uFh}?vPMqAW(LE9kkdLh?QFW6=jT#oa7+Kw}YS*Txyb=FG2Dv-cSO9_|0p+f$0Ak6lF(eu~?{NyN>gO`Doc3z)1VlSes3c?q#`y(?{rDsf1H1v5##;cqim^4~q$(trPz+l*ZqQJM6^}r|=1vG0kZt~iyXe~9KV+#S518*S)M=TsFEVPtV*OG&pkO+W=?b0L`SnGufVvx>6sygQoR#5YS?he^c;YmsN>?N)MT%QqYLS10rIlGNe(5gP{yhRFc#`X+=jT-UKT&HkOZ!0R2Vgn~>lsV5`$(%6kT)=2H>=x@ht3dtdE+Gu>f&ICocMc27j17Da#qaT(sfDBO;`LNzaQ$)9IKfmyz5c^8`rQFX5H{^*4emvHuhY0O>`Gxcan`N<k}O6fF1BKpQ`l<O3@1HLzV^W<tmfA(tl`Q*9zX_#>~IIdE9pkI`+sNy70q@hX^*#;V*BAHBSMZZP&BhC^u3p-@Q1hWeh*}>h}@KX4L`kf#(}8Ruc*QmDZm&97gVb%bH8=BpQ2VWDUI%zmoQq&`Vs>hMTH!qmM}}@TW;Ty^uNHC-am#}V-L_?G4urB6+<Yn@K&H%J5ZD+o{z6ZE_vM*Zmd=PX7?V7U@8{iOp0@d*GP4jo`nYX^nknyO}B#faqg1}<zT&%8~T|69?H@&0nL51=DO<Sw!=F4k;a24`F498{7nzSIa(-S@{H{Ez$nw!6+DFak_%h2?)E^Xhb{u5tdEC&kwDk%38D0#w~#vHt>e;YS0UiL%c=!*f81nMQQ&Ilndajtiv9DAP3vx`h|?j3!{hN3kxph!_{LRl7LuWIr8891NK!_wVh{1gGO(6Q&|Y`lk7H(gtQ-8vVjC3)ZqI?{fq}l)JI2)A5q~`*GzFM>Jl_Jl8F_HRVW=&&+O1_(l50f|lA9E{dj2d(p!p{#F;Y~Sfeh@bFcivg?DP@=e^}bWSC(w+5#X%RO^?o7k!LH^nU_=6RMkg8dN;96i*kvaM1&&Y#_uPZQ(S$Ky&QD8v@V{n_>mn`TUr}{5y)C>F~ybkKJJH`r>W%w!%a@T1B7y}vq;I7;EK*fo$2{_6`rAgEJ^sAylE7*q8pD>KBQ1e`3Fx%ez-b@qFI#7%EUbowS_n`Os>U%VuMsiWkS^ECp6m5NyNEVUQ~DlPRERQ1*-EJS<F!?AP!~sq5$YUrd~?uthjeJRJ*L6??(YwOpvC<9H&&sN97|!Xn{<uN)rv8k7S;7+Dp~mv=FG_e@3^)7b3j57=c7cy}=p+K{Q=Ergz(+9J-9Wf)r7!qr^d?r`_7LPHoOC=-SZhUsKc1_zc7<wY$`~YjkikB-*Cii_>0L?+53$Iq!zwh3V)21=Ew-rpVgigU%qFH6-d5j|&{_B@Buv6SIwrpq9^+EU}-@B1&Q<D3f}mkDElW;*AJT8lj>ZbA19wE@7YmMm%j6jkZ1wCle8-hs6>arrYA0^Oho->fJN>5lx^j^jR^NmXF;*e7TR_)}5GB)m(1!<;DXhG!qe1r@40XgzB!wWrDbnVzm3q66s^YJ_7Q1r9nbnjiH@<Hksw{;6%nSu=q&gYp5i<-Q6YP0|WNk5y!gDQUy91!m~}!v2xr`2EsU{h(pSQ&=p#i$8oDU0Qaw>&gWz;JN>B~p+h<0zxa_Is$qofn!=N2m`Ce}V4XleZrBO|L!hnUo)9d35=5W%I|P)abcguT5%DfwoQo#N59h$qAt9A}ukyn98GBqA?1su>^&xr+k0})Z2pMNbRM9y~=AyEg@~wWLECp@g-7g=d&@!LyGwkwN_l%35qr3-YO6ei#Y`Z!9fS%3LXm(mG&a;M$A*#r%fJ8m~S`1K2Cw#adnny1koyi3A!2n*)k7C9eE{JMd^QW!-yy#}DBY!N$w8{!;-R=<XahHn}SyhTJA_cRg855;xGKqZ<PdICbAc&{S1g9xdl@S9?l-ujC%}TZ;hDfQX){WiQ=GxU&Dp-RJ%~zUEmuWII_XJesGW$~!Hk|a^Xk`1hUj&;yQ+m^jf?CFeE#|+j>UHp10f>vmlATeZzBC54SvL1bVFq#{eVJVVWuasZAA6eWaJ308GQsjkKM0wCqydI4lk5?gLpVO)@rb}hc^PYBKzulwyq(ak;ayAQa30QI)+ahllf5F96puHWBPZ?QFSg$&j1kH1C06h}$g45UF2JVTv1tY68Ssg4kBoyx(IB1v=|G*)<s4L3fTpN!lNZg&wF0S9^BlL2UHho>%Su{2j6CM%4RoCywRm6YXuiN}9WAX}b{Xt{X6Gn5ui0bGV`=}BwFfD859%lART|KHgs3I*4^NvVyStm`vJcinh<HY&E!^r3Jef$rcPyMPgnAYeP&%wZUj;-Qx}oJW@=XX@W3wz8NWrhQ4v*%@d>rt3gkInT?6earJ>iSn-w2Loz{Eq2&uAJpm_$(_mppA|$+Xe8Gq61X+V;2^6$Csc7zr-=B+F;SwE!O+&q4wa`T#+{49-dI7zV|KGKxAz9bL@esW2O(;i?i!C+hPX{P2F{-~pgR`3%uZ^7%wRNhx4y+ii(zT2jfX%70+hbunBt7}K@`gxLaY9NZq2cHJL;9|$j;&+R?Yghd;l&Ge~~h(q*$jEt)l5T!khz`!32eDH>+M(p5+j8PS6kPeIKexh|3BxMqe7IbyUqHW{x@M_W&+Z^kUjK7B&*MLn=-QdN?h2@HtkRF+E5PDXhbHOgr0|a{4<owi%zz??_>TKe*%oulr!k)5-u)b4J#0pZ0@I;`%on>@K_DEw&yBsPDNz_rtp(ohdpMbdNys`sp4x}~=_Jt#CBwn+WEq^?vf^kM!$ZbD8rDP>!iDD<WBE0(TL(m~%6kCpYvi6;cqUy#7knV`a3r+O=R)BW2cN>>@A_Hw`XDfPCc)BC(d#2?=MP->59bvhcarFeNM6N!&A~dtM0YcFM-q=YiUW}o(0n#xm!UDj&U}I_)*l^rHL3f%~gxlnHJGC6!YOspMOz40PU9T#FB#6dvU;qLDijG9fZvJ5(Bm@G_LO7j8D^6$AQodp*8m!&l8C(uP*wbzXE|>*L73WeFUSY?~b)V7U+`xLvtd>6YSh2BW#fIiP&!C~!8vm2wfzflhOAI3|xpf-oxh|mkJrP_$>A3^-wDk~I*V5*2F>3WIpqC_$M2WC-C|ew_UCtHC<r%V9K!NUn(sznH#WNG*N-55;*taeKDBXphVd%<-PnQ_v#4hh+l399Iz=NQZe)EY?5gdG2Ky4wA@knc8tn`);0+SA#j^1ftcp0E8v{1}`Bl&fXK&ompcOT>=u!fHpibzGbjtyt+iu>X(jBwjL5@!B{=6Z(4rX$B0Yrs{tlj<oV+#}Y&FLDPc_g)1JqyA_TR};y(w=v02zbpl_X21hUOor#WP=K|%-wPI+Ktv@#0Gcg6e0+DYnk5I8*W6l;0`r5|qYEE*GhWK1XZ^;QFx-Ofc|C^QA`Ne=S3pSMh?K{}=U;mx=6BuLl!^);%$WTE@*2V|Xt57axCeUA4<B|iNf|b*<gG3H5}2LphL@xcS};~S!x2CCM%RwI#z@G;_EEE;zhL!%A*!Yt!&J0DL$_4+;sj2rVIBl^x+arsP|dMvb%1kncx(G$(@@<^IDpZ}{sOK;d5<wuJS@-KDwRZmoiN=`3H7w7TA**gw>bMKms@y4DNe#>EqMmtQSl;!wU8$2dDkd?-(4;DJ&sUU{>C!Z>D(a1)p=Q!j6VvvXa&{{4yptkraKNydxFfWWfuFonCz8x_9RVl+7bc*AEU0^{e3P#amRJgxTw?U&88i#Hk{Mb%Zqg^lfx9dAyJrYBrVMv4&b?BQcA0%XqlmlLN8vr`CDa^HmWx=LYO8j)CDIQY<G7~IU0?nnHO8*%<dqnIGQ7o;kk|N;?6GOG>oPwknvX*JH|H}#{D<~ZEA~8o=B?0N)<!182w>_Y`c32TjOM1ojC3lfesTMs&@P3^~$i%qg}+vUZR$$L`r`6YEOSTEdVp+3&GdRfh*HK9TeM@n+^3{>^YWjoudf{qDg?_0tk)X_lgTh#1JUy>4vI_j3<z!d(K8REuzZjY%Sy`8G(_I*%xiX@R5k>kvv6nZ2?7X(u&DDn5x>VJ&qI;CX5H!b-G2XrwwmNH(CzYn$^4Ph*y6-jY4={6#<c<;1&y~;Ykcgnj#x=<$e{uiuORsGCbfkf29lowwPQa69Rgf7tsZkwGYD9c>+vm5;|p~KlWbH!U$0GqQH?%e`I+w^J-GHMFW8SV`{N&j<>V7&vo};@GbDTmun17^H53{LvYtnQW8I2_zJ>^RL(W&+PM@`dI2tS_nYzRRK>=nnbsq2BT8!`941Ii;KhqoZmajt08mOvQ&n4NZ<|vQ(8tCOM_mJ}J+Zxg?B<_h5QILqBa92sEo!-L4vQ;Qvkyf`blLofPTt&}mElQSaqp0G@c}@HLuu@e6PBClYJgHIRXDqYb;MKcnN8Et4+vfkqN{~~Y4G5uznklNd{h$=L@v<~kqcz>!o$`x#~KRR7;BqCpQGpx-WnI!j&z+V!6ESY9ygl!+*upQu^H3|6O^tMk7!xR-ZB?yfDDFxZhK<(m0N$YR#3)4_=lRrUd0>Yrb$!4j)HkS0Wi48Hb0Q7PsH~)w=6zKPt}vzZkLltM)(3AVVh_@IESvgaVEC47olirOE9H2dyJ~(jFZ!jGeH^QP{me?z4}(v5guc6<{FBbwVQArd4*Pv)Y*vU#zE<iaLqrrQ&#=F0|INT@Rp4mZFEDi?#yxMeBMXz5*TR%#3c2V24#Y>dZ?2c#i<y7(6wxj$dtV>%i~Y^pNLE8jZ&ziiVyL5N$>A}@SNncR|dK_%}dYsH6PMrDX_l*JxC@TB;Y8#rnGn3Ca3;$GK4O@bGF+-BgUCaqN+?)6`k;GN=Gq0Pel|O<@zZZc^yLN{DL@Wy>Jw}Gy}5av~lTBY$BA*MF@N&^6!)mAuliuTU!g{9flJX!@Wk;M@N8PDGY!Dk3ejrI+9EjyhP}9sb%hZDEHgljC9)UK?du|LiXpmIa)})Bs6Gp`>cBg69nO(E$qS&2@JZX3J4q-3H$8by8wDRbGBVcG7-t3nS=zvShZTnvj|Zz9RwXaOT1to74UBvD0SzaJ3zd9S{NaZVcUvrUE2Z$jk*e|trUu<ET^E@3AKTvp)dhf#fPd>$wDirPL}&JD7O$iod~&W@eEHijU=XAUv6o}jGI(Sy2U~$BV`f1z?<}`(jRgv4xmftPb3WmuoN22^9)IRyKo)=#|j+KpcFy_FLN@WGtu#SsTUNZ;*bQm>WmXZW(@r2;LxKnOsm>Fu%Ib)|I0k{<-&LYEHX%vb#Y(QIMKmkP;A;<QO!B$gl&HWH-rTTxWvZ|0oIFCRCiG#+F?miu~R|a8)vWbkf)P!Ez*)L^Op+|G;MZ~R9xWxMIvd?Q^xQyMdJW6;Kmnih_({!;ZEl+Q65_`rtdPzRb{wsQC19-nWSCpal&o60UMt(>|@r8D_%0iV!ybA)^SX&Por0qb7rml*k*y1sxP&y03Q<E4crb0#N3=d$o26G9&=VIKgv9f=Lq}Ao&(5)J-vD-Am@B#gJ-ZM#xa~nK{SodG*EJ#_9TsgKkDNk=N+Fhhs&tyKL2QzQLRCbjOq;7;$gRYWBe5?V29Imk5D_IM}c-;Jo2LKkHq)?$;KmvM5s9G89B;$m8axvGS}6r0A?s3($IN;XT$4i;w-`XnhedR3eeP_k=o0HGSt{ZfQ<t{;#PGHdbG%9{bbT3p=ZZ4gKU_chTkDSb~_+r?m<jcf>;FFtTbixl7yxWNLI$<J&%`<iMPa5B~_S!wnT7EDlWEcsRA!7DHjVO2??>gSB7e<EZV!xFxWPMA!w2`_25BFBo?r)FV^Y!Wht-k-@l`3GoqQ>%Ub>Nax3HM(L9iKaWp<WTYWh7K2{WIg~h&#?G`tuSJObjWV57A7QP4Tf^tbD;mHJ%If|><)-k0H?&j1h-OwA%Yhk;hs(!x*ss0p6ozzPYOPijjC|hRd2sgt5Mp$JkaZUg}u`IGKy)5E~`hka4i<}t5nVK@{^%Udjj8jrzGmP*|0#s_B66Tfw6kJ1o+5@+VXwmewOI0Y&#q?S7I{jCp`+`@wQ8nTCeh-whvS3D)#SaQ`-mcbRAV6;bfT&|ViMfKmBe-7x6NB<6+tVe`j*uMWs}lWcBG?#Oak3YbNn9OJp#Vc1`n(o6AWSFJBF41dzg}t!OKpp7lR%<XJdo%lCHnmufQ!fryO>QqDhI@rG)Z@V0+h1mSr!_VI1bvON}AJPVlC;FV$(3tQV>qz$V_vU1X-s8{Y@m6EyKb;@~kmWaeg{b*O!{p8x+oSyUNtRJJU?gwjM{142qOe8aa%x&iqa;Tt*-&%8#soN^sKySmTJ4HV2WJXxfju=}Yh%13GVQICJU`O90Rm2Bcz~RP$V0jkYaVd=>ORIyW#en6RUez%ny2d@YatuCrS58n%wJQUDE3pJXXQY#e~Bu!+*f86@_q0_;7I3{%Ubt$-t{$6-AGZpzpVmjv%?or4q=E!|Vq)oI5`j7QV?tDN`{R0-$&`vTaJD<i%vhe(Bu?0)$Iu`&#TN;&k?Bxa_l$zc?$9$3lk0l+=;D0s*M^Y>Fb?`9!bMk|rJ9aG6Ap-ImZG$M4hu6SpOlr1_Yp7tG`Y>C2n3>Y^!;TeiuX1e-J1&mH;>E*CLEtRd=Ga8Dgbb3^`ribqxf+3PglwkX))~DXRe~2s(a&}RG4!V#9YB)N!Jc;hq0(jo^=JVmSVApxZ1?Y;AOYk|ucmw`R94QUZ4FL%c;fZn>JjS6El7P?FJIM;HdFgMPCioRe3z8c>wLKlxyGCm4Dp?5&(pLn{SaiU?fD?4R$R_~gJzg8qcrwkI96eJX4e;$o42dSxuC|avYXgD@^^V6yMlrqJKR(>{R`>of{L+!X&&Z!it~SqIt;03y`#9!W6)q(TiX)49Ri#v5-9T-XHj-3|5LJMZ8SpG4a*+(dNdQl-5ERp29g(=M+zjzWBPgZ-q(NIm*>7LLQ#iKK7aW#WQN+Vre_L#?eXAMS--#K-2xIeWU<9eWnEh2p#+=)}tegE+kg>0lo-#$S5|NmzTK(`@S*?o9T8_Ut{eE=deO#U67)ANpWfT3Q?brHb!|ZV)*NnI_+ny^D8f&G0Shk{R9iK*{hMQ1R5QK`#GjEQ?d>*?m7X!W3lr^$th{FMLer)IKz1j~4%uF0D6UG^^ih55)gBJAgh0fGA98m4Fi+Hbt^7eOD`$^U1aMkTw=>hF_&BXNM;Juv+siNMzMI&%zY`jEt4>mrHUYQZxA8g9Hyr69SK;|~hXo#F?&XJUA+ImyJl;B@^Fcq&XA0cl8`e*m2*HlnJ7>buqdEdb{UjY4?{Zd`99s`*&M&m{oyP*d!i4Owj)$7xNUTX8Ox`8l9NKkkCOxld!HcNO=AcaQ4j!_sLEm+r^#%l^{oc4PWA2xzu_)L~QfUb$^KcO=6hiDcZt-tQglO+KUPsCRSMvXZR!A%+#v!0QddqNZzr<ZpoTUZi3M>g|snz6@R`ipy^h@E)<={ROmca<tEu2%3*FO!}K(CNI{Xhs=z$5LsU4(%AL{mY}C$7DEPkVNOgW=zJl)o_leB9Tz2sd@~g8cp;Psf%>ziCD^R;OYQeNc4)<^vs$Gtk&g^q;e4=u}1Q`D(c!eydi1663vx0SWCg!_0o@)N{=utn;wkg5f0rIg~Q0jfgi>XoG4jA!ur18!LXoC$`k>5K3#D!#Qd5Dfr)E@p3R?RxM3ajW4LNK!G!8ZH(g~)Z=??TCm#YdpLD7=3goH|`6EnS+$q;xBM5F?7x=-XWW^i^uDOb@EX1#k1&v%u^Ue`ldX%&D6qC2D`jQC2n_&0FSc3~|O=M}j8&a|X8_;?MF05YM_8UMg)g&v*N|@@WDb|VcH=3eD%Fnz0hKn<zruKB6LBx(jmxo4U{bdd2o%ORce-IH=$iO1HCPRLPVnu9RAMvc*>yo-fECSXM0l2|Uv4enDfk`GvVP3AFENt9MsS@Hd|8LY~0yKu4R7#hM3c}PNRKo42-g!>wc!-1}jCP76d&Jdp<@vcwS9okKs-ZD?nhGe#h&(Y3&mg)Zm`Lj&LRrpstb5d9fzDSlk>o`p<T|jIt=op!8FgFUjBLIs6BrbZQPhBY-<P7+*wwJy)DcQ;cjF-a!^ty;xE>Q$33dFny{^`=4ZW$_JZOdnE(clh{{D}kFD@9yjZ(g<@;N$GhL@j{D^cwUsPa%{-)%#zBH})l<XWLYMu$2{hwYZw8f&ghXn~aJil;6QiX!#^d~`+!SotBA<%0TFVPrnZV7Vj&US&Fx@MshvW2cdq@BFr6_&RXmk{-_EA_)dn4V&kPkIqBoJ?(Qi>jUyWyyweAw0K|FA!;TSLn5s4Mbcf4qjAO`)Cr1SARts`CW@&d;{dl$ouO<%$}I4`D+i}*Bt{IP%6N9U%xEl1GvF!g_}?_Mc}o8eL6N1~1&n2fwEMcvA4}XFnOQdoULN4jRbIGCMunn>)DahWC%%kJdGnjwTl_5*5N@3!;zRM2q8Ag@Zf0OmW{(#z{0CkUTm`A3z?<GXsv~Y0mNp(SUgMlP{M}9V@)6lp<lK0m)n@Mmj|L+v(J?f1i541entKM#qK?`sthwsI1?%yQqo$K(5$mlWfV?QtJ;>^`!z0ZD(>rF&u(Y6N6W3y%?|Q@`4XY!;_D1OJv`FhXFvrOzMDZ9wxvBG;>5H)f<pdW5XJ4k=jfXbjm1AFHWx5ddVcY{!G*Skts<^^oK{<_<<K4RRn(yxDwZ&93fE6zWXSze=+kw0X>uo9sPY`AC1=M@R4y`BB9j`9H3Us`ZFJ+u*kb<Fxc6ojfvtu~Kd_T|k)D?h-yM;SfyGZLBjCG$4T`fZ;!30n>DqZOmHNa3&EEfa|I~WnoAXT>Y?o9QzvuEayg_=z)H35A)5a<as`8rSp>riu{fB^z%SpyK0%4I-bl|l9nXBrLCEJw>s3G5EWIA{^Q0^v$a?XH-2-XeiCvbM?A9Ru1e60eQS3uS@_hBvr8FwQk-06|~2yj|1>NECr|74BJ5VKd*SP&$Va)ra_Jwa^m}kVTwNshM!880tZjr?!H*!IU*~SuU*Lv&fiWh~$4a8pYA3w5kaVzVCf{w?yAB$NY^EP7DCU>_wvTAF>)5Wy-JQIND8OXf%6h^lB@#Hs^AbQxAl~kLly^Bgk$MkoR+dm!o}p&^fP+myj4n<dtxr(y3bo{@-AOvY{$TRIASNU=sEG9XHlFAhzzKe*nO<$0n!*s*v*rVmkA1-cEJl2!uYxOP>+L($Ei=QqJ*HVEI7HgBX`~cls+y2a6EbTn&b8i8VS77?@u&^OjNt&V|@$Z4M6timYAX3djh5Bp;YMX_0C|Xj;*EKgSBFUp8QA>cil&qF9KkpL5M{AmOsMhHRlN!UttTeeDs1hY+1C%H*Z0sZ1lBHed3P`=s<M^FVMKnlGcok=DlFzdSx%^F5T|hdM6QfxMIpybV8|RuV(2JCh7PKRMuLpI_NT#q?YvLW`xq;&60Kf}SP#>keb)Sv7sc%>^up#bNTaiysDmkHe)20y_&hU<)minD&G_^6;ce4sD;#lhjS%gq)b8!cb&8j7D$Qn-Ek`ojOIQx=MKwgj$dXTlIiXD&z-=A3fV2E~Y<HVjp@Ck1ZhCju!I<y7NnHS?0<{Ky|9Ojv8OYb2_&l!Y}OGS1c9<5+h;sF<j8<@M(zS&C`SnqdairJ<Yc5%AQC=v=99!g2qZ4x+LR|x2-wSee+^i)vYjYD1C?kOdGsRZz{((T6h@n?A;o@RFd*g4UEA^S;dj*>ZMimhNqKY-y&i@T5}S<mP@Z)Oc)JyHZ&QRITey405UyXU?52dr0Y1Y<|4WWwCd0uNJ9HIkdo9Oqdp#)RoOFzx(88S3gmMl9%*h)33hUTuWkSqar@I!CL~PxBk^_#S-D-0UoQQykIW=B4=6yP)^fo6<x!m?uWG_Aa}E*m@cMV4Jsn`Wdc8Sc*U^>s9NZW0RnF_wRTydalOns&!392nhM@P^IOk=TQHYfcve|ZG_uyp1#6&g~hK%>jq@G5V&44nnrpgL&&sk=d!C@l7rp8fIq$0g-$h}25npRs-4Nv4rPwjyNS4l@Fdu<Ju8fv*>XJ+f^9e+Ozvvty?00J&<pnpMK*!TDMSgY@$mQ3kpw^%AV7%`~f+*IPII&^Vt3Dei}c)NmqAF@CaW#riaf)DJ{Li2}u#1xbb+*d}0((t3StNmDj@=REd7H#%&Pp`;!w9^Ed98=W+B4M+1rdGVC(*$SI`;PcdiViYN<0{{QI@9Cn>#>KbY}aXt7KfCLw1?45MWOZLn9?GMQSE?>q6^?fN8NS9s5N)Z6m<eMqR*&V9C{pKMMyKn;cjExTJ5}90*2I#!RH@_a$7W_@ZGA`i`5y(aLPGVCdNO4?Z41!3wb-kQKvKWY=6%K&pR!)^DJSD%e^``3e6ibeo-L0kd!_@l|161ICmgb&Y-#&vd)uM;qHKL$M0rm;gFWA=^sO74-yjUTxj7$u{PIb2LsqP8+d#i8x(3ky1>~U`z^xIkdYiC;zCcCa2*JWj-9Z5PJobz@@Lm5nNohhS&x}40Oe};8QtL#gThtFtCr~{*GkdmB2l;2I^C*aDI#!3Otf^EFDM*PB=Yidl!?eEgg=a4`<=?=jjB<&E1c-rsm^bZJ1>V1F;E}r7~_pNR9A1RK<27kYgMSA7_^iuQ#J5F8s^a^i)!tCWq`Gv;7~@~{b<77xW*y3y}GOI{X)$u1uQ|{JpxKX+)PDQF306^L}|Fmj|=j^HoW$qoIp8c%u_;kS-QTH7V-@0_Qmdro`rAct!^ux46bNZ2i~|7U?fUR-bOIr&ti(DA)qidmt+3hyW!*w`?m9GG}kP87ZATPItY#g2Ll&Zb?GNMJEH`gci987Od_{5Wb#{oxE(>!ZZ>2tVPp!Rltj*d?UK#lj~U^YA>tidCB>xI-mmaJJWZ$_7Eow;sVP6hjG7~{7Sgw!%ezs9&J}+bnBHB7E3s87rcO<{S;SGShTPKfPGDhgz+5<(T^QBdF{h>GIT}(xwTWrfs1n4FI+N@9S1*&ISM@OX@7)BeBsDvU_qvEiLmNbN%{iWHGs$K+ugVGI)X9;OX)-q_V9jk;%)PEk?)0T`VGz~Oh@@SO#}@UUPmC}vRoHtWj;MY|9`GP)l(^sqqh-yVfZ9Da%X6bdRHJtg-*!E9p%Zx<^QN4vq(QcRVHI+`R5ZnAx~E`kCqKQz=jt!yro1P@S4puRRK57Qt|O-EAi-Jt18^ImY)O&*$!QsE&XoSK0#xVo&Rho6g0W)#z&URjcpzXQ>NP`<V*nQ$Bb0P&-h1epcIqCgD)O?-0-a)EAB`~zo;AwkGlYUEjRFZWtMzwQH@L#_bwxavhs#pTiroXiIc}nD06074Befyg<s~hwQhFkvPw=i)6RWI=&@3-Q1(7?dBgovRsc(hdH>akpO@k*%1`TKPgC1tcU=m3QW1s|&;8b#6gQ%+r2}n>m0lJ5?7)2T$wH><(9=cx+pyw)@(&3N*HY`jZWpBuldF9H0OB9@mw@rw}0`e3;IIm}8r<-qqrO8zMl(#E7k{{f8N&dDz6}nP|*VX{Rac)wj{i+1G;4QeOwx82tL`$4Nx+-Y5Q&~JEn^u~KqT=%ByB%DqarhDq+Z7Ign5n3k5vLtyHNFz6(?_e2b&_}DmXz{WHa}>9&C1Gn&il~d^-3;^P9+w*auh?CB;<s1Y<Mbzn1db=ho1C<LAS410j7rDU-git)$c|73AWya^n1$mFM#~eF$r)a_>ioc4`VD&bXfDUMh64*X=xkMdk!`wYpf9a5h{rYT&w9r<xx*eKNsCEhqD2SRJsE)E<04Y#8H00Z0uUY+<$8Z+;#=|N~1%dO^6)xV`tZ%u;YyqaZ}f}J>^@6Mq;s4>1MBo0Y__m5qa1&NpB}*AxFbSMf!%#D8n+8R@X&E0vFfvqtT>;tga<IzuH9cGB;GD_LcpsSN918A>O(b0lt|4vkqx<6pk9i`bZQ3C<y3Qpxfil?WfmWns8gIQ9?}U6y|2cU3}sFuFgMS>WT)0;^f2DqT&rNw-SYR+iX!V%+tOof*b0L216e9cifcJZZWU$IKGch;Z=pIHKJ(zI^xJOTypp-QgB2`L99kl=nzX=y%WI|PF1vU&%BWpj8i6ID_QF$YIH!3a`9;@_%AyZTeFGOA{>An8&gQ8S0Ro^lVquj)#C_mnyOZqM5dP(8^`4|`IeAZ9gEs6BTqUmTeJZ|U3(cyZ9G9^ZP;&E0OZQSO}K6UwE4p&!g^sra?zLwGGO}mZ4(cbb&98k{X0QDM&SCVB@!jV9QF@OCW7uSz-EQ}S8gw<2R}c@*tgc<Au2_a(aPso%n>xbnZo#Lx*xH54~zf;_RRVzxQfObYbqP0Ck1Lev9vNDpn%R<kc~KI7xcyadfiJ@#l+H~*D`SLzCsesy8ZsL)!0`m_F89>@loP9t#eQ1RrBSJ=yqIt6-sA3A-6p8$sFR2)nvZQf!FIbTdC9YmDsZyL~60K=Qwk<Wk~|gG&x8IQw9d@M0FtqHKQJ3%JA$Y`LUZSz*TaGF={HY?`w~RG|xExZQ8JX#+$ONj2w4*QBb%j;L%q_X*javaIZMf|Ccp`IaVfQEb&FS6f^l{xsYIO3pF&Haq-&F;Gb$Xmb!`o!3STB5;B{6^f|!5B}7q=TCQdde-kbH6uO9aMLpj`=#uAW`07AaT9Kr^KB}QBV`r)5l;EPh2C{s#b})N_JwHpjq;=bxZdV$BCs6+|S_Xj;&dTOuWxIya?%kqq%P5V8o)C)GwW~c0>em#R;vE4iA@F<wP=bt)d$`K;u#gwQ9>Hjvx{6zD7oQ2pkXvog_RtYC0|xcJeveP>kB#Z=KkIf$bPrN}c2+d34@~9bCK^a<^Z@Utl74_QIIwW=OsYN&l<1tf55pV}^5@f%7#bCd5Fw`<mStr>?Af<TmL@2|%;0vy!Wa03u;U#<F$I=t4hFsOaD#G%b_!rKH8v+mdDfh@cgnS{oO%%VOa*Gom$7z!ICGU|;R0)VFQfSKlQr`K=UuTuclutcg3nR9M!nX1$jXlQ!K^td6MqWZDfZpatK{)*o$0E-w23ItCNV^zE(`G0hwEjIatUx(7fck|Hkl24>7A*}%wPw#fOy{S2uiuqe%Z)!MrJo0XWT~?$L-vX*&vGd8Kp&PZzp@)deA@^izM{@1gAsEw=u61CqD!^J5;ulv(HJR;u#}m4mr2|Gu^MQ7Eo_-E#K-o9B--?1BT@Rc}HX!#%K+0wB3v1JP%BwTZ5c&3LR@ow93RCX8L-y$E0XBcwqk`auQo4H=NIBNJt_c*#~mUD9|IkDWEjGW2C~^kX8b=!p54Z7S$NHpJb9OO(@APg?vJXFtbNCucC`cu6m<eYGO{;<V4PxHNopo+NYW>e0lD*fW6tcyH}RT78ON{$IA1sf?;`GNPf+gkN%P`-+^_rII8CTz<#Pq5nG^0hxJORd#a>jO(C3UZOvx$@mpR{TQobM=UJq=SCps{%8&M!sOF`dZH05{ZBJ^mQOxQ+2be;0*>R`!@a{o>pTnUX?iR@KIy9N5DdxT$TN<0Q+Teh9fIJD|1qEqpo|MneaBbft-iAG!UrX9&SQQlYcEdw2DIP9$i-+{2xnRkK0>kz@Z2AhtCd79FLr<n>Pyhef^=v1y-FnLbBA9&F#=4pr56mUN%b}-qzx=93jQZ6sK|e_cG@B0!^D2jX3ar<f45^FnSVCMKLIbG;dD+b!DyR{l&5ZB}oO>O$dIs$Pww=wk-+2im_y6rVQty6QRWAVFl1H?I2T=jiGuwOMw~*=LrIdfZ)LoR{#6SNZxwbhF')))
_PROXY=make_agent({0:_DEMO},budget_guard=False,dead_stock=False,sell_lead=False,clamp_sells=False,room_guard=False)
def top_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
top_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=top_style_proxy
