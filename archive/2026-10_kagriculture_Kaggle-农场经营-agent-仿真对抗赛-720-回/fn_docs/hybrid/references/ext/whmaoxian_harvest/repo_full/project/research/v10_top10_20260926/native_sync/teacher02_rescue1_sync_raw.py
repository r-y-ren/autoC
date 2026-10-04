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

# Locally implemented, observation-reactive executor of public production intents.


# Historical episodes supply task targets, not hidden live opponent observations.


import copy


_ITEMS=('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL','FERTILIZER')


_SEEDS={'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}


_ANIMALS={'COW':400,'SHEEP':500,'GOOSE':300}


_HOME=((4,4),(5,4),(4,5),(5,5))


_STATE={}


_REPORT={'errors':0,'seed_waits':0,'supply_waits':0,'weed_repairs':0}


def _walk(position,target):


    x,y=position;u,v=target


    if x!=u:return ['EAST' if u>x else 'WEST']


    if y!=v:return ['SOUTH' if v>y else 'NORTH']


    return None


def _fib(n):


    a=b=1


    for _ in range(n):a,b=b,a+b


    return a


def _tile(tiles,p):return tiles[p[1]][p[0]]


def _home(p):return min(_HOME,key=lambda h:(abs(p[0]-h[0])+abs(p[1]-h[1]),h))


def _command(obs,actor,tasks,state,needs,seeds,stock,claimed):


    seat=int(obs['player']);day=int(obs['step'])//24;hour=int(obs['step'])%24


    farm=obs['farms'][seat];tiles=farm['tiles'];positions=[farm['farmer']]+farm['hands']


    pos=positions[actor];inv=obs['private']['inventories'][actor]


    pointer=state['pointers'][actor]


    if day==29 and sum(inv.values()) and hour>=21-abs(pos[0]-_home(pos)[0])-abs(pos[1]-_home(pos)[1]):


        return _walk(pos,_home(pos)) or ['DROP']


    while pointer<len(tasks):


        task=tasks[pointer];target=tuple(task['xy']);cmd=list(task['op']);op=cmd[0]
        if hour < max(0,int(task['hour'])-0):
            return _walk(pos,target) or ['PASS']


        tile=_tile(tiles,target);distance=abs(pos[0]-target[0])+abs(pos[1]-target[1])


        skip=False;replacement=None


        if hour<task['hour']:


            return _walk(pos,target) or ['PASS']


        if op=='PICKUP':

            item=cmd[1];quantity=int(cmd[2]) if len(cmd)>2 else 1

            # A historical pickup is additive, not a target carried-inventory level.

            key=(actor,pointer)

            outstanding=state.setdefault('pickup_remaining',{}).get(key,quantity)

            skip=outstanding<=0

            if outstanding:needs[item]=max(needs.get(item,0),outstanding-stock.get(item,0))

            if not skip and not distance:

                take=min(outstanding,stock.get(item,0))

                if take<=0:

                    _REPORT['supply_waits']+=1

                    return ['PASS']

                stock[item]-=take

                if take==outstanding:

                    state['pickup_remaining'].pop(key,None)

                    state['pointers'][actor]=pointer+1

                else:

                    state['pickup_remaining'][key]=outstanding-take

                return ['PICKUP',item,take]

        elif op=='PLANT':


            crop=cmd[1]


            if tile=='LOCKED':needs['land']=max(needs.get('land',0),task['quadrant'])


            elif isinstance(tile,dict) and tile.get('kind')=='WEED':replacement=['DIG']


            elif tile is not None:skip=True


            elif seeds.get(crop,0)<=0:


                needs['seed:'+crop]=needs.get('seed:'+crop,0)+1


                if not distance:_REPORT['seed_waits']+=1;return ['PASS']


        elif op in ('BUILD_PASTURE','BUILD_COOP'):


            if isinstance(tile,dict) and tile.get('kind')=='WEED':replacement=['DIG']


            elif tile is not None:skip=tile!='LOCKED'


            if tile=='LOCKED':needs['land']=max(needs.get('land',0),task['quadrant'])


        elif op=='DIG':skip=tile is None or isinstance(tile,dict) and 'animal' in tile


        elif op=='WATER':skip=not isinstance(tile,dict) or tile.get('kind')!='PLANT' or bool(tile.get('watered_today'))


        elif op=='CARE':skip=not isinstance(tile,dict) or 'animal' not in tile or bool(tile.get('cared_today'))


        elif op=='FEED':


            skip=not isinstance(tile,dict) or 'animal' not in tile or bool(tile.get('fed_today'))


            if not skip and not inv.get('WHEAT',0):needs['WHEAT']=max(1,needs.get('WHEAT',0));return _walk(pos,_home(pos)) or (['PICKUP','WHEAT',1] if stock.get('WHEAT',0) else ['PASS'])


        elif op=='COLLECT_FERTILIZER':skip=not isinstance(tile,dict) or not tile.get('fertilizer_available')


        elif op=='FERTILIZE':


            skip=not isinstance(tile,dict) or tile.get('kind')!='PLANT' or tile.get('fertilized_until_day',-1)>=day+2


            if not skip and not inv.get('FERTILIZER',0):needs['FERTILIZER']=max(1,needs.get('FERTILIZER',0));return _walk(pos,_home(pos)) or (['PICKUP','FERTILIZER',1] if stock.get('FERTILIZER',0) else ['PASS'])


        elif op=='HARVEST':


            skip=not isinstance(tile,dict) or int(tile.get('yield_units',0))<=0


            if skip and isinstance(tile,dict) and tile.get('crop') in ('WHEAT','CARROT','MELON') and not tile.get('watered_today'):


                crop=tile['crop'];age=day-int(tile['planted_day']);low,high={'WHEAT':(2,4),'CARROT':(2,3),'MELON':(10,12)}[crop]


                if low<=age<=high:skip=False;replacement=['WATER']


        elif op=='PLACE' and cmd[1] in _ANIMALS:


            if isinstance(tile,dict) and 'animal' in tile:skip=True


            elif not inv.get(cmd[1],0):


                item=cmd[1];needs[item]=max(1,needs.get(item,0));return _walk(pos,_home(pos)) or (['PICKUP',item,1] if stock.get(item,0) else ['PASS'])


            elif tile is None:replacement=['BUILD_COOP' if cmd[1]=='GOOSE' else 'BUILD_PASTURE']


            elif isinstance(tile,dict) and tile.get('kind')=='WEED':replacement=['DIG']


        elif op in ('DROP','PLACE'):skip=not sum(inv.values())


        else:skip=True


        if skip:


            pointer+=1;state['pointers'][actor]=pointer;continue


        if tile=='LOCKED' and op not in ('DROP','PICKUP','PLACE'):


            return _walk(pos,target) or ['PASS']


        if distance:return _walk(pos,target)


        if replacement:


            if replacement[0]=='DIG':_REPORT['weed_repairs']+=1


            return replacement


        if op=='PLANT':seeds[cmd[1]]=max(0,seeds.get(cmd[1],0)-1)


        state['pointers'][actor]=pointer+1


        claimed.add((target,op))


        return cmd


    if sum(inv.values()):return _walk(pos,_home(pos)) or ['DROP']


    return ['PASS']


def _project_stock(obs,commands):


    stock=dict(obs['private']['shed']);seat=int(obs['player'])


    farm=obs['farms'][seat];positions=[farm['farmer']]+farm['hands']


    for i,c in enumerate(commands):


        pos=tuple(positions[i]);inv=obs['private']['inventories'][i]


        if pos not in _HOME or not c:continue


        if c[0]=='PICKUP':


            q=int(c[2]) if len(c)>2 else 1


            stock[c[1]]=max(0,int(stock.get(c[1],0))-q)


        elif c[0]=='DROP':


            for item,q in inv.items():


                take=min(q,max(0,100-sum(stock.values())))


                stock[item]=stock.get(item,0)+take


        elif c[0]=='PLACE' and c[1] not in _ANIMALS:


            q=min(int(c[2]) if len(c)>2 else 1,inv.get(c[1],0),max(0,100-sum(stock.values())))


            stock[c[1]]=stock.get(c[1],0)+q


    return stock





def _market(obs,commands,needs,target_hands):


    seat=int(obs['player']);step=int(obs['step']);day=step//24


    farm=obs['farms'][seat];prices=obs['market']['prices'];stock=_project_stock(obs,commands)


    animals=sum(isinstance(t,dict) and 'animal' in t for row in farm['tiles'] for t in row)


    reserve={'WHEAT':max(3,animals,needs.get('keep:WHEAT',0)),'FERTILIZER':max(3,needs.get('FERTILIZER',0),needs.get('keep:FERTILIZER',0))}


    if day==29:reserve={'WHEAT':0,'FERTILIZER':0}


    orders=[];cash=float(farm['money'])


    for item in sorted(_ITEMS,key=lambda p:-int(prices.get(p,0))*stock.get(p,0)):


        q=max(0,int(stock.get(item,0))-reserve.get(item,0))


        if q:orders.append(['SELL',item,q]);cash+=q*max(1,int(prices.get(item,1))*.55)


    count=len(farm['hands']);hired=int(farm['hires_today'])


    while count<target_hands and len(orders)<10:


        cost=_fib(hired)


        if cash<cost:break


        orders.append(['HIRE']);cash-=cost;count+=1;hired+=1


    owned=len(farm['unlocked_quadrants']);wanted=int(needs.get('land',owned))


    if wanted>owned and owned<4 and len(orders)<10:


        cost=(1000,2000,4000)[owned-1]


        if cash>=cost+20:orders.append(['BUY_LAND']);cash-=cost


    for item in ('WHEAT','COW','SHEEP','GOOSE','FERTILIZER'):


        q=max(0,int(needs.get(item,0)))


        if not q or len(orders)>=10:continue


        cost=_ANIMALS[item] if item in _ANIMALS else int(prices[item])+12


        q=min(q,max(0,int(cash//cost)))


        if q:orders.append(['BUY_ANIMAL' if item in _ANIMALS else 'BUY_PRODUCT',item,q]);cash-=q*cost


    for crop in ('WHEAT','MELON','STRAWBERRY','CARROT','TOMATO'):


        q=max(0,int(needs.get('seed:'+crop,0)))


        if not q or len(orders)>=10:continue


        q=min(q,max(0,int(cash//_SEEDS[crop])))


        if q:orders.append(['BUY_SEED',crop,q]);cash-=q*_SEEDS[crop]


    return orders[:10]





def intent_agent(observation,configuration=None):


    step=int(observation['step']);day=step//24;seat=int(observation['player'])


    farm=observation['farms'][seat];count=len(farm['hands'])+1


    state=_STATE.get(seat)


    if state is None or step==0 or state['day']!=day:


        state=_STATE[seat]={'day':day,'pointers':[0]*30}


    if step==0:


        for key in _REPORT:_REPORT[key]=0


    daily=_PLAN[day];needs={};claimed=set()


    seeds=dict(observation['private']['seeds']);stock=dict(observation['private']['shed'])


    tasks=daily['tasks'];commands=[]


    for actor in range(count):


        commands.append(_command(observation,actor,tasks[actor] if actor<len(tasks) else [],


                                 state,needs,seeds,stock,claimed))


    # Prefund imminent seed tasks rather than waiting at an empty field.


    seed_need={}


    for queue in tasks:


        for task in queue:


            c=task['op']


            if c[0]=='PLANT' and step%24<=task['hour']<=step%24+3:


                seed_need[c[1]]=seed_need.get(c[1],0)+1


    for crop,q in seed_need.items():


        needs['seed:'+crop]=max(needs.get('seed:'+crop,0),q-seeds.get(crop,0))


    # Buy upcoming task inputs before the unit reaches the pickup deadline.
    # Only our own demonstrated task plan is used; no opponent private information.
    next_inputs={}
    hour=step%24
    for actor,queue in enumerate(tasks):
        pointer=state['pointers'][actor]
        for task in queue[pointer:]:
            if task['hour']>hour+_INPUT_LOOK:break
            command=task['op']
            if command[0]=='PICKUP':
                item=command[1]
                quantity=int(command[2]) if len(command)>2 else 1
                next_inputs[item]=next_inputs.get(item,0)+quantity
            if command[0] in ('PLANT','BUILD_PASTURE','BUILD_COOP'):
                tile=_tile(farm['tiles'],task['xy'])
                if tile=='LOCKED':needs['land']=max(needs.get('land',0),task['quadrant'])
    upcoming_stock=_project_stock(observation,commands)
    for item,quantity in next_inputs.items():
        needs[item]=max(needs.get(item,0),quantity-upcoming_stock.get(item,0))
        needs['keep:'+item]=quantity
    orders=_market(observation,commands,needs,sum(h <= step%24+0 for h in daily['hire_hours']))


    return {'farmer':commands[0],'hands':commands[1:],'market':orders}


intent_agent.telemetry=_REPORT


agent=intent_agent





import base64,json,zlib


_INPUT_LOOK=1

_PLAN=json.loads(zlib.decompress(base64.b85decode('c-rlqUymf$apk|uJkP`Z|Hp4MHMR)TCNZQ|*cAvtfEUnW0ee@rfn6B>?mO~IVs&>$#5oaJUDY!MKgbezS=m*YH{(W}^E<!!_jkYl-9P=~zr6da{{G$X|HmKx`)_~$&;Ry^Pyh8d`Td{%@2B_g{`GhN@<0Fhzy0Rl-~FHe`{_U1`}XO7{pbJn>HmHA{Wo9#-LJlX_x|12-~IaCfBw^d{5QP&tNi}m|Ngh%{o@~g_fP-&>A(EP`-7!_{i|=j{l#y;|LTVyfA#UhyT7a~_R8<S{p#xvFF&&aEB}1Czy9TiuYP>@zW!x#vloB;)#Y{e;|29%!QXuN@Qa@pOz9J<upp=76-E4r-0T%k|BC$V&-m&6pMT|k^tJu)%MTyEzx>Xh{95Jkj}m_8Zhswr{+(ZZ>af>7{WGWZV?Ft>fB1Aqy!-nP-+uQG7hh1em;U;zA3uD&SW=`V#r(8pFMa-L!WWqjKJEYC^*{f3$zJ;G(@K`^m-fE1_e(u|YQ$e1c;cS^>O*=O%wK)mE1&-i;=^kG4AT8llpnoHzg#vyZP-hnf7+CmB=gg@z4ZAlmgFs|n=hUx-(|bl8j7_ciTiW0UOY>>G3_5C+e^XSr2wDS?4{uDl7LTJ_R{B{w&mT0ej6R{5W<fSyg0errXV}ok{*s`z9^Et^!b;YrQgH;v}!MX{%K8GV(*93Ui$pgmVD!6>#q|ZeDOYA(h7S&O!iXncdNjsReLG;yA|NmhP@Pgvn2b|q~awhZ<go9%TIq?^`{e1eRcx+^zZr4f0K6l`TDzWzy0v_kH7t!4<CR0=G$-n+vSHP{2X(!+&)58@biJw&@VoI_dQUM%g3i;SLA`y(9>dWpLKl7K+)gqrSOZ={<LW?CHA`l-5xD^d(O!1vf0D4v<WIF+ZsJRUw*0eX3rdSq``U|K!yA4JIwZqXWwCwzC*_`4cq7z`=#d`xpkl4S5ICd{pcm~c#&A8>E_GJ%-4vGKaUK1$uGb9_+LK!0F|#VE72c*{P@+c|N6tnkN@>*=cdzM2Ty<G$?jZ>c<7#;ueW_je)%gjdy#OW%N;t;A9VuqV5=0l+kx(XXZ>{Y2EF+fXyzMe)!o-9neJ<p0=?_M0(u0>IdRh6oy~V>fIt4_(^2ShYS87>q>H>AEx-!<Eb#sI#W!pDHoNruXieHipNEmt_sd&n`H$?GKe8*&skms+U5~|gE)w0?mVZ?3>#lh3{ji#7{B`#Gt8kxH@b^*C-t9A=)xE#tv!la1>dXOBQLc02gUzGsJbAkL`PR{wJE>F>H>l%%SQ2-<eSLVlO}>ZCZ|8;I&P%<Q%AIbSX1)whp4MmKE05x-Jg^NRZ~8jr)7fPWul>f8ez%qTDT3+hr>dn4FzkMIAgK0=XUCMr9&YoB9#ib2P@%imXV$$<`%xy{;Z5gtkt_MT%i|=qW*t(^`smB*ZJc$Y3@Y=DpTxd#in{#_e6r0HBE?gP<WLE#HMX*SR(ZD7)Gx8<Ew&&`mO>P7(OW!&1LbYE**EI_w41?cTcO|1d<D?YYHb#{$~YD%p?$1;rNL+o{ZuXb(zeetnHSNoFRG_p)B{wu3&dyN9#B%Ezfb|UB)g#0+B6CJO-EES@bgD1W9?3lwI@IN<$LP#5kK+s)Pz<~oxjcz@5wyG8F7_gy$6+FA%$VeakS98V5fJ%ac}y(s}y=Jg`h)3nfXp)#?>;wE-Sxr4m~M<dT`qDQ{I3o_B^kX^a+bCVS$5`t_8G@qH-$$duR~R4=Pf~WWP{5lP7*2@fuxV{qa4^5v#pgC`%`F|DuN@`Cys&X=_MfL1_72sklXEJ`Ru0R%){?w`i3btt#~@`z2JMR8hY4ep5aDVhgj)KHPHKzmnU(a=Nd<XPOqc7g~BEcS|qd%`a}pvziD<$5Xf!JLzRChbs{a?9VF)>tsA$s-Ag&UNTuH<MC2;+y8mV0zPfnOVy3_@&c=4WN^G*EpCh8y1i<xQGo|H_Qumce-lsJ-+uSq4<DW!;gj^hJs&ZA{oRw-Zj&Cjm-B^}AKInG$>B0MUa!8uFP~IW`FXrlt$>R~nt0icwn-CD-&ge9pvPJ_H$1Un7nsvk2M8~3Y2g<b)^jA@m%wxMe82qpHk+WVXh<7wfx5hxE3m2XwwJ5Zg3I?1DETb*dbP>?^OB8zWVhF={o>0diDOk9F9mnQ<=+jLXE!Wb*-5vDhrjHc(p%6(K}ok~KVU&UAGBwnWR-WEDy`1?jx+6b@|$}}&#!&s6nm*U5h>W<8R>UlQ}al^H@fuR(0@hg+Z@QRD1WbtI;zLoo0A?apXc0De!Lb^4GenX!;4-D+vJr``3tNHrnJRlB7n<R5U6fW_ImIfy}`4l{En~eVR|1Nrfu`d@p|J#4UO&_J-Q##CPdOk%HdLVP<DBH)zIm0DIfW)-g(l#om%_$^B%A3pMRZkJ2?~i;>PW4!IH(=)lpY<xrc6-x$w=XcV~f{(WsU60o`%4N*OU6FVIE|1%jVezQE}e!4&N)$&(Y>%g|WK>tH)qlZOW;9???xsbb@&ii4NTE#8KnJo=Af=|8&olU94HPy{2w-XaS|3PQ7xO<%7*axbT<2Ct|QE_b7;uS_2~3|}j6O#4-Q+Apw?9({2ayWIp&8je5z*^xf+l|nI(l|!y7yS+lI_=FX3#RqlmGv9ZY8@-vYD{rma3@K3xkIPqtg^d;#20L$g(89t^_ned(!|@tHp7Y5+=GE#~b@?knwlPHzbljmucalu+B-yo-Jn4)4aU<1rZDzvCi<!<@w4B?EI~t&zrcGt%Ayo^joh!6<4%~fsa6+SH%{^G$54z2>*)~r}^Z`QFQ9If+j_1Ww?bXPx+}JkFWZN_=R*cHEWrmI)(0ii<_w+_ru!F8(XRv}@?AzX_sH(SDR29}=R#=b#T3b7Efihj)R=T=v!Rog2sZ;cf|4J6BhIPb{VaSL%0OplMsE(wuU{1mLUJr-G4(ZB5<dQ3jqB@{XS<<fAb%{~3*U1tiVXH3h2bU3byi~oVE|*L$>gRZ=+N`}?vbe~Y<E83dSubue#h*~<d48is`-2|fFItfz%SIC``<y7u3DSnk`a4>#Sv=dzt>pvx=_X(YP1VDtYN>L$WN<-K$4k}G&gGKH1x+0<RqvR~CFZX2^v*e6s*VdUmuybrdAwA;PwSJ)DyS?dy!R0~iL8idcT0oIp}$b8G`JtY3$;m$m-iLd<l9Gj#WmpeN%m6s6{pOCTTE~>UL&(71C!?t^^uRuFRhP!xng>Em@4mQMJx}OcZaFUekSfPif^*g-p5XBJ0~qb-6yJK9p)Fh3fef*l5@OF{t_2I&CLAFv^wOvgH|Vr8X$LNmH5gk`75i$S60biStY)*O8&|!@s(BbS5}FrtWKHjy$ZGBm9zpu5A1ve<2E{r<E1SST(r{t-x=)YuD434Xa~J5&16{hR-A^YxLi6-e`2<mO8!K#*xHzY@p8$4=Ay^fr}>+zFct+zK?TsW0z*+nHT{|b*ue_g2Q6qHuDL%ZQmcHIuk+^a$u|Z8yY$OFDcy(1I_L}-h{*eRfs#NdEI|7-+~zs$Jqa>*A1{T>-N&0J&Jeil_iz7TVzXTvt#g<7lC;P>H!{R8k`tjI<`P67GHK0TqBVP&pE5Lii4m1XS@rYaFLBb1hLY)a1|~3mU6RC$yL8hi`9$XglxRLYV1wvE0*}ZD>KxIe9xhd1(b#wtsv~dXjX>0;mDQq6R*Du>%WdAJ#Y6rp?Y9lK|B*~UP=r!&k}ATF&+^&1^Xkv49&G{aE?1-h^_@_p4g9JD2l5vc^R|a9niLco%M@u-D`bL&D<<%^6WHNNiop~Z$zEdQk5B+XS<y>NQ93__Q8cxQ=84J$n4<KnwD7dk(!fb812=C9&%E`#^2Sg{MDgMki|N!jbEIA=ED@x!BG?`i!O~`$#hPh$&`Xnet#f(1_M3v=@lS_a*&c2kj<=LOtl0YI8y`DoY?`)cM0%nT={fd%X5dGFl)*06%F)9HHQ=!4bVV(<M=M@7rE~02mEQq8k1T5~o6bHvJ7UyCOpfTev(V?xn9)VG3&_q!x|op9;BpW_0z>fFGdSjq1pPR#I|6JmH++piGX^cNA7GR=G*JZ58ZU3)5*$OmK^Okf`j=nKd4jg>5wtbl_;%c3Q69A81<HdaEI=PLq>D4yCe8#Fpmo{t1X6o25ebIem>Q0{46|J|+jH@kk3!57gEvo1^^-Pj(~yl5OZz0*G~t?DgzTsTIf)~~{vI3l4_gzYoWv0k(FPX4CvnUeQD}FA{FKmx{Nx$ryYAcMxo<sgjePyn13c?2^mMh_?l@3em!7<<UhZUzmwazpw_P$VzLxI>-ky4&#*Brc6(HBFY)=iPim1B*=;e?rOLr{9_TY<C$Yt^3&$@0F#7ki+FSlMaZezy;+R|BH8E8Zg>xEU*HdamBZ^s=f5hX=ePtNIfjJvL$Tw4&r)NNe}-I!%jh=qrNxZL^$<SrbKRj*bU<%7rz)%=A`OM&DHNV15HbNQLEmT!EfJ>_ju2P;dis%*q>4W|DUhoaIwTPhx2^qC+ddB&glceOIR0tRI-9tqw=FOIurgzW=%ixe5DY=B?vVX1oEoZf+Vrr$34)VIsE42>Bg9YWfM8Pql`zJ5r2{ScJqWcHO&*jL7NyuR0u6{#`#M4?6hO3Nr;t4USJFrxyZ?H&GKJ{92xC(^e%KAv>XYkB}{pcoAUn6%TPbQh|5I5u1!wZM7C9MUOs&0t}l3O|CZwj1Z*%jvX-XV}!YgU?wsD{i02K<TJ-p;DNZ%3osRSu4X{^75~mejLo=FLCo@g?y#qD5*e@B?L5{Yp~|*&CY9O;$rpo)U>ngvO6yjBMxfX$iAoqB1(@x=7e!U4IO`)l-i1=4<nkb5~M&BkLF8e83fC->JO|_SO&a2?=f$<;=I9=jiApfIxQibw1jX4C4}1{A(Z`J*@GDwF^}nt>Gf1K*Pt1d({Ab=d=B3V%skdxmfJ1mCa!MsxJ*@FZ0A+cv>}jVLj-#(GP0(4Dzf5fLH%?{DCPjZBwktu(4FD?4xmYU)Nh?uzscvB&EIzb$x%MhzyiJdiFi$pVmL+msTFl~9}^Rf<Z+dc+-<aX7D;+GwR>1V^ycS;`OO-83zx0bu!0!^k7OD=B79Gs2R{w;PQ%zu%Y&ENZoHIScfxJc%enN36plqV91PmoFlmRvwpSR3EiUdN^B#)AXI20S8OBNLR<RnIJYd^PjAIrRF;p^ri7zV7Q-lJq4t@qhB9YN^j}<@bW)Z7Ftb-xEg!B@f)=P|_UIG{Zo0B+fZk%~#Ms>;m=;xzE<bRdba<nT^Q!+{3d5u~NhP+k#{BcyTJJ@i;K7Sa+7e<FWQ&sc@x$H6QHtVa`Y(9xM6P33c`K!DC_o*G~&)Kmq4}%9g44$m}cC+r=oPze-OgHp%wU-zb6PJtC`Ag&jY~+^oMBRFN#?GhT?c;Y)5Y2pLx4NvaXso^h5M<~Ac3x98S**jRsSYVfb;$fMtJzE7L;q14+#x7`@Ygx{K~A=p7(#~n`WerNjAZg;w8R@;c<phcwZ}cEJs!4@nCQ`GJYhWIe4ik94f4tl+AF_kue>LixjXV#WErqKUvTj~beGdUD8JDChdhm?(oJxnZLSXtso3{LU*G2QrHj3U7=CyE@VoPNw}wu#q2`n_E#xH)i>|O5SQqfo#ft~@0Exv0NnB4zJ}h_~Afd`9xpiJsGNp2-Xyr~n&kEX5HGYONMf!<x=BU%H#C&Ki<`EmVXWz15Ku&)EzJ63{W!~gpY&itc$W1)AJ>e9`puoeC401yP%WLbS`3Q-Qaoi!PbEc)vB`9@16U{O}M>QmMo<XVe^3YPZEu=XbD`r}M^P)tjVwa`qJMxq!*796fQ+2)iy9qLJ7uLjGo@`XQY8z{3B)XkZ=ypa8wlkXDmw<WUS^oy*9!TY1V?7qw_LxV$0nRthDL^NMl{c_=o~Jl@YdOz`e1#FF@*?0Tl9e5q-fV>VD&v(7y#k>8w;CHV$<7@bGF#L>*R&U1KkC!q;QGRc%`xQLIs_pm(LtYL27QVd!BfoeonmO!ydDWS{gHr<)IvaTPaI*E4>)q?G^xrW4l9Q^y#FjXE!pQyXTc>rt^rdwrnfbORk%u<$13qrFw$1M`MK@(%x#ZY;?LDdateLO`~;hkZZL&K<viULxU$Z2GbJO~CG%(?Ab&!<PdY6ClErzUEDobnsauO*i1QNfEza`5YQ~Ip%W-2VOo7eMBeT5(rgjx{I$QbcbQs+S4_H{IB^ojIvx^yU<M%menAjcpk^|?Oo8kiKA{RfpOpeG3WJHRK3$W{~JVzZEuNud#(`KdSnd!uEY!{=U#t69;_BTV~Pd?gqJMiF$B@*&ChuoCKpfhwnw;Bj{heZO}bGQjk{L5LrD}6^sX6lO_sqf%KJ$WYT;?OCv2Q3x1BBui<l7+6ADuYay3_x8B_k1Sj>B*d@zxcpJ%h4ik-NH7e+BI5V9((WoyXP}HE_`dPFxR^xM`A(@Ym4-P(XH^u19HU*f4o3OMO<qf4+ZHUdVvue5iM4iw^@OKJpHH5$eQK3eF@AW#JpVZZ}P85z#ishf<Y>e{~ey?#mn|rB=ZO+AQq(iy6I~?wG;KQ9p69~llU-rJ%^zCa|i~1iIcXyBMI_m?+I(u-jB@~zV}$_*J3pVo7EIZ=ZFqklo7>E_B2KiR*M!33~4rZkn^8nI-gQJ{PHU21XOSii=073IT1U;pR|v9q2mF_tS#p+RX%^I{6vS2hw_)e>U#OA>kz#D!63aIgEaB}O+B?~_*0uEe~HVLc~uha4wvhS=D{7#*l}-><N(Fnym)Ifz`i$0;n<kI@nibo$w8QS4#JDm*y68oO9iJgIIQ-l@x|W-3^j#kvD1UiLA$_~BY=JTW2PO{oorjk;MVwCK=pX273fSe7(LXbp<X5@?M*9*m%T=~y*4i=PV~sJ&?Cnh967erfUHIBEH4MeRUW(~eDH#3Q|eXn9b{v1i}{56Nny{jv3Rk@;vI}$PP{+1@>nqkv|`%YEkbUur7$L1SoUJZcoND!V5UDYa0i5Nm+MgN2fKG~dh1TXtvfqXhmeewqx-q>DxK~kN+6ywusI_8^q_9s(>Y*1w}1B~TJx265<l9X?4&-J_$iCq3XQZWG}6Xl?C)S`1;pAJ9%bJQ$_W>(g?XUO->y2K@Tk4arxs>UYGDSfMe;OrvorgwJA+E$gE?J<@%mOr{R27GAhY@%B!nk=G9kOGh9|pr{N&EA9qiMn2L&uVC;)x5DsIerGY);lgfZE+<EFcgDcE)76QdkD<GYF6s-6U*X5@5nkwO=jYabSrd3>ek@!b}&9{hQemcA~V4s~>jbYui&8!KQAy&xJvZagGwoCaK99s%$I*a9V;rctnvE%lE00_dohkGtXHH$CZ_*`L0d`Si^%D=9Vcf?Yi?CHs*MrSR9t9UFj`Q9CJQ!vZEiYOigJy-X4ZrV%T)MvQ2>ZXVgV4WsT1E7C3{4k15xiNSI+?aa=a90B0Aa`WQMLvwW?ZSfeUn>~#^x=jY{v(A&|PUY=_6w5>0Gb-mw;;V*d%mkubr%iITAkG;7HQD|w)5n8hW2;>en|y)eij&&yXtv<S<qI6Bt7JYdsUTEB$Bvw6g;#PYypmtxm3W0$@+iEL4|kDx+(kmqb(l^-+!||)U|e(+Zl}?;gO=?sN9@%0r%v&@;+%PBRCk1yBH^eQ77)9}6-TK(k*gF$u5w+$3fR)Ee(0*BpbZOFGP!vx^29`ITyjw3QhYJ<4pn3Ks2b;q+4Q=qF`oxx9U6e5vO{-(>42k*qz{=9%Ee-}Gn>`U$l{RZ7@R=diE5uzpx|u`S@D@TET3)gg;s&pFH>M55Bdi?=zqJp-UbO+Zc`7w&Ktay3GwwW-q$bEb{kK63~?o7kyB$uPCYgV8mvZYu^Ooz8#T$PtBak>G~T;cc`9$^sk{yriYAaMh+agebwMtx2nw&VqLjvpQhE$vF>c7RbFfQeF>#9BuhYUCfO<-}OdKpbR0|`wl4eL<qB~myM}%>}b=D>|kX%OYjGG^p`GgF)JKnstzJ|>J;x%C1$krAWAY+4InxMVRLU$#bBl4@e6Tb$1ebbfqC4;COz0AQP+7hqbP9E)c3TU?zuiY-5=yT6_v4XcAvUM)LyHY4*X0Y|4nWW2G;81}&)9qnAC3|#AY@!|@nhFy3FnX7V%D`i(J70_!KvY~K!Ui~)euWaX;(Nx9>=}reE}Gr`8lE>?HI7B2I~cm+(0@8!5ldS$ZQYwbX+0L@5s3ielRQE<<BX*_(kbzc#YOZOF5)Wm2j%lN3y+Y6Z;d_GXG2oid1%D26(mIByT+Q>9?rbN?WvA2UvlWq9Pu90XK5C90HK7f+D22vAe@etPW9fH8+R{ZfWS0z18`m`Z6gG6@+cT|N=NlL&blud)}hd)l_Mpy$`R5C_t^k5VtxfU#kTM%wmFhwtG0MBKilScwiy}M>r<WM8M-pn;fL<P%wDcu8!IX3tfXMD(22#)W4En7G;29bv^YG%${7$=uG6siZ`c_2ws{hofFpUZ(AkfLF8n1{R&bLCt+<)=j`?=^41q&B4P|tcvV{$N;E&}6bvhoq-Uz*J<`Z(WCm~l6Y*bGfTJ18lBKc8>611_?kiiZ^W=xp5Y3*pDwWFCgw^crct@BWc$<rY=-vquV9zxYVvd5&E!<7%QXvC2(naIO7s61P~d-(Swz`vjTHLfrZ;W$e{mkHeol*2OLVxWw~=hPKXPF)S;)HVJZJ5T?cJpFGw=zk^o>3?!~$mS)dikPuEqT;(dDSn*AD3fVkn}&G>1&j!z%)~rlXtU-aGdK_niwE8(WM~A7==cGCi_O*tO`~2sRXW*A;BnWm19WrYFR`+gC)xYO${<Ei2BFa)HmmL^#la`ms^$<cp~eU{RX;29x}!-S<F_NY2k90-95F~@UulVb3)%o2a0kHXYX+R2NNX@M(|Gm*ALq6`fpf_pIG1^ev)B!<kysJ474;f0g!)MD;9&@vCfNXCQnIQbvm_e@*HCF(Lko%>gr9BlW8LW?D=l0o3E@!X5@Eure4yruMj{|GNnDt6Y<nW0gqmBb^OmQ{`<AxHn_nN^e88LE`H2(^iIN*#v<*q4FjWU9O1AWO&UlAi;;_wCrU?}CWXYYb`N|Xj*D&=<uKdZm@)zAKmQfUw*9TMpU0nD}<n;la)(4Crkz?{96@1721)l6ZS5x0mlfY*7R@mo3WeP9)`gX9HTj=zNN;jMvZL&WV3wF8a7vKCXV&!)Poo<IYY&+aSN<CXcCLTI}E)SZyHEHANX0;Y21u0mC)lPg)VG0W1X3~6{ZR2fBJUm9lDLfUY*^YIpR@{6}!S={ecR-HnaMr7aMi1zM&Lqq&w5@g4#(;Psv2AUjS;dH^OZKT2mwP-pBHmdec;>^J6(6ByXh|m;vt@5}4fTb(i<g9=6Z*Bx);{#YWuq_CMb3bm#vt+EVTtacZD-IE*u?tlkwoQZpK+%H+Y<9(D=udq^^PF&P3a;=)~~$5xjPKb(qZay(UWtLtcS@Y2?(0<mgK=X7hbbdWfVxJ3l^2Jm6L<!l?%N`Z3jBKBsvuu(BRvXpR3!v>ve73=vfSz=5}_PJ7UvZ!1Rq)fz_ZkIQWwJc0DM#Pu4wtav=5;+ITCFcat~Y%u2q5)%s-`%jGWBj1~Ng?Q!vjpiCQrO0110yMu}+kZPiM89ZcbohGX^Lbk4FqW`oPeEs3mBlh>-eEWBo@4v$P;VUy_2M3Lv9W?eBJ^b2sdU+C>Gdl{Eap9A<np_%*%v&AvA8p=$#K$!GX5!@@T=0XhyO7cFVkg7f;UPp!_b`O^<ZOn4XEWd#T!XjSsfwGzgMWRq@jLVDLx&jI;C~g2p8PaGGWbHv;H$?r4|wgLo&<)yK$5Ubp3t`(Mk~34FSL~;gjELGN~Q3i{(A%ucupM^c{d>~<`o+eY#IQY9Ht_<Q=f2qA>?S2<}8XHe9(IE>4Dd+pom=928Usr;r(-1mH;Y!I5A80*>!eW{ssu<^p4r_8YDmiljkL0#+HMy(Cj6~3-5T5^!^(BCGz+r?&JYvowq|(zLn_<Y59jO<+q?6kO2T-O`Cchh{Gr~mo@`A!uXAy=QmEC-w1@8E2R(_Y+m?ab7h+j&3#LB?&~q?7Kc%{#JJnEr>vl!^JAGR<cYx82507@XZ%o%O@6r&9oU5-J5_b0`ZjksR;RCT*m5#_zaOA>{21Ux?DrFe+8uMhi2Z(f2xA3DIAfHt#nW_COk;I5`A(*H)U1vEm%Rq5gE5L>;&nHGR0jr%CjidS_)9#)5P!4?)cKTv&Zn^BW;K;aens3?D6iO{mc2sPG#;;kjPMv4E!)&Fv&DkJ${G(V8#V}xnsLF5v+FCA$^#$4<0BFTIfa^W`8r7yB^oLLwf+lmJ~%IlLKk0Vd(qSLZn;t~{_Z71m1PK5jv<Ur7Z&ZjOLXL;E2*e?!g7a4Uc2l?Pai}el2>>TOQPFOCujLSkR3Ngb|~imM4SI}(EML``Oowql2-tcyy<I17#!x5>om>LYj8M5OddB`dE8_*N7Lu)ov+~Q)eb4cLw%kB>ht2S(V@pHo*0~p$dq)gst^SHM5{U&of4>3MO0CZRYlREB$HJ|@yrj8$Aag4G}>d)gC2|FNXJIZZN&M-<POTdGsl!;(ld(bm{Cmkj3PFZ#sJc4sP?wkKy5LMf0sR3%cmu+s-``}>8AxmJ>>;-=&n0f)}R3r#YVh!TF1i^cGs5_Nha%E@^ZwvNfovtt0{8%Fu*M3H_NgCyX;ltzQ{Mj=HqO(C(dRE;%qjrv)?|Q{pNM{ifp7gXzkq%Yrl%D1x%_dbW&Y8EffTvsTL7T(Ch`IbVk$mjMISinNi+8ZI2g61pU24h@dQm&oe}1vVtxssxA*3!!3Q<IxRDLGYJe2&<v+saYQRTa-NSHT;{!bSs@ItLO2%Jq2RGWRtS)kZ?Z%H7ewo{SW%cFQ0RQ7M&~ni2ZQWdp-!@SE7SI?;;~=7*ts8~7(f)0$;!RKz$q#eW%HRRiI&|IT6R-C9=Jv~tS8;DUcrX-woR!(wSP-5>z(Uoj3|{sOY7%VqO{?Iag4n4y6-%ERD-@Vr+xeY&JsswB$HD0kj7j`8iRUZ-+~@SXQotFa(d>S$Fdxuh2Ba9heE;*J*{!|5Yt4&G&%<=*}51)!0*E3ufUPsA#?fsLT6+esc_7Y#l({p6E6qQb)RPYo4C;mBLH?D<p+c+!wO>RKn<MRMbiJK^%#mZemOE}HgCwx_7a$ctl2ReZO4>5>5d{cNCz;);CzB{aU~e@nR|mKp)E&(@%9H8^QbmC^EiaZgToOMpc(1>B?4vTvlm@v@oQu`NKsXSVh}}TJRK2(%bhT|Ps>0o#?+_q#?Z>6cRDT6Kr)nIEfN%nlzACR@d;KG`E-e(<P~Xew^yL4K-G3OP5Sy4&16ipdL;+dE5$}8ntTe3wAdXU`0T;=ODFmcCrklZdt#5RduBHGC}F{hX4pXtBu*0HGBrjSa-f1BWeG+Z+CIvV!h^V_vZT6DRy71(A>ubOdO~~s<RaMTs{=|vD}3T9xGEQ>BsUkP@L#-KU^l$LF1B3Sx`WRWSs#4Prlr|(H`F1tzFhQFds^)U5C8}hk9QuNGJW8bO{=+O=j~#gw}{8L-W{T)vW;Q%#Znzf<K3M!e%cF35o9D<kdd#SW=^Qk3yFbN4k*)8_R~46U#d*x?lCKasoEgHCqiK)W-ApjTpTZ;rR|kZa&ll@CX02Meyq#nu`ct0b-9gpWgvoRNQRPvGL+0qL#l&HFB37`V+NOcW%A^hf*1!j-R3UI1u*$6$T4~=m>0-QRv@$Kq_h-s2g}ddj6h_LUgLx3y3Es}*)nd5JvvR2(~LWp))eGDf=K>njDyKjEi)~zFF~qh<(tc{G~9uQ+k(x!%5yD?p&Cv!LGyVV@6t~u%5{nZL0{bn`bO*IJFAmltjzst1~iu#A4{5sr1dQ*t*2wX5HFc#d_icSg{FaCO~O=k2~#^O97+*AO?w5Z7|FJTY17x|3Hbb?f}vcl;^|SR%z!#&qUw}KdKIQkg+UQZY={9#CerO&dGYL-aO5R6#DMS<nkZ2sA?mP*dWl)1Med;0m`or-5z-zFUbeJsqzxevaHL!*j#XKIl6li__Va!6xqP2Rt7;HdKBaT%9wp&%#fB0jZ-4~qQk1~9|9KJ#sYS#BAR!`*cJN`eK@t!cTBTVLlD!1puU|diu)R*cVYhif2e-+*24#rY@e|5I#dKuN5fvtH+m$;GV3+8KM&FLOcR3opkjDY&8f8_Oimn|t?)J&fJMDj7_^B415W5}bG@0K^7W3O*%x}J!*P>{LBNIg4<1?FclI^=S(RR2yBn;K4bhyArX2>!zSgF-wl~y|_v`VMN-WCr9sQ9yT3on4r{FouDf7Ny;0LyQd&;i7S8`4uCj>TP1Qy?lMBm+|*5ZPK|WotbqTN|uwZLzYo?J)Gq=OGbY@A#PtfXc^&mQV)So8jsmO1kt%3L>!E3%~~n(Tz1$H`ZgivBB!b7ONZEG`}d*!m$z*j#Ur8sM#YSGZ-72BrPA7weSf?_00;hCPH#S)KSZU4{})0Gfxh3qy=|R5Z4F<aZUaj*NH)O3w>X3VR~m6ZLXC2Ro{5-SHlD_h_Y-uOx+G#Yo+yM&4X+0K@r-Zy)OBYs`ZvrwUkpv51lfGWYMqC2_OrhMGmDBs!(pUwRX@Z*=1W$&B;M1_DFNC)-N{n2rLzJG)@knaSDHpVyU2lVQVaBxt*02r)Jqrcb46vuMc3F5mYCQXI6PwSf~3A+2K8rZ>175O)Hw4?#TKY?yRp#U*8+XB_#uw)OjSwun`$YpR{<S2|!JLCW%&><Zl>$gzD6ng8;v6FYMFFBw(H;bG#-hSvwXPiseB+4L`b#r)bk-WO+zSz`ajY)u0m07V};WI}ODW9zz)_o7Yp8E2Sku02=HP`)T4xHHsU-fRVG%glZ4+Bl`=CBze=mD_TIQXG>0hwxlEea?`R<Su2n0Cm*3-R43TOSH;SHmEyYH6jvF|R9Ho51)pJv|I|GErXJKXg<H?>5pj&hO8vaqOodIYC~Rs)Cd0crNFW2X9Y|uAdIvU7npU^1SH$sQ@yCb7#N0tgq6hcri{>6p9JY;NT!54Wf{3Z~OP}}cA4(K@2zI6@WqP=;0BWl8*Vt^~3_Pc*{H#f5;BFjgs|)|3YeXnS#E9U|8ALT?`&IU6sKcLv9sca$mEJr>L7OB@4}W~&{BfO22VJAw&<ZN`!50srOs}jmy~Tj4UlxdH8jp%28xJ73nkYMr-a2`{g@@T8A4e)_u7s{pn}TSg?HE?kmo__STqiH@-u4POuQVSZNMG!u`Iamr4HPu^cvC<c4_9eO1goqkT5Oe;Pt)O3I3gnf{xq`P)<0*{4(6PAhj8H?!hoq5ZXIo;tQq_@0+E^2pgTuc7382hl-i~Yjk~=9ohmeYR66PF<H4ng7MkavX1w^qwAyLB)6Cq#5R>Tn5#V#d{@{c+g~r3rLS+?D@}wjrPH2H$V&^G7(_R8&Ar^q-k?ZsjHi)RSZyD`YJTC7D&gafE-YU;)NNipRc8OvmO_fkTuW)%XZFPlfkFz+lDI_X~PiIKFcIMUSqJX`zWT~WD6FWWDPxcDKd;xvTb6V3wY(t4{T$0bkb=H-lH3f^->~U8*@?V<=(ck@u{=r}3bRqg>rG8=?>zO$hVz8Y@0^2Jju%Qsqd3JtU@yDT6{t^M_G1a<n?17?#@5+Z#=ZjM6=%AUxXNEOTtXcQRn(=cInG{m-qXy*vlVP53C}qsSaFUfsi&Y}+U|?8sFm(_@4xwtRF-i_Wa&oY49MO7e{9nob_`g#4YkWwG?n+XWamfQ_U2C*cVbD&688jWNFDW$aVO@JfhMg7}hDvRM&D=*|n1KiZs3I_hGWoNJ6Q4z_P)vYhCLvKa<uBDP+m~acppc`cy#l=x721?sLT|o=ZU&>OxWaAaGJ3Q3(}MwZxl;@25x{I#c=D^g5>4VdZIG)!Bj|`q)O)*}P|4$jn!F7K2{rTtFD_cOiI7!^=)^Zn?NL-S%NJplcvb;G>oIR<jMU?x?ab4X3Kg}zMtKiPSgIppB-5BN&2*C-Nk}>4Nk}Te3A@C~hX6V_H<PyM$Y!9#r${9vM9mTUAvT^@NKK6$`8WJ>)sv^5e-SqpZdYDrxB(xFEc>qPp1Dz=6B<9YdEsC7L=2WYWY!eKHHYY6g6OjonKiG4OH-8PnHK4kph%~F7THm{8|YT)wGSCgOa?=?#{2bJ<5$AoOrDuJjl<01W%+>Q-5mI1O8N4T(p*bQ(|MFFl=+lsDNYVbaf&a#sq^O9;frrN&uN<U#_c2Z>3Xc4jgR6nEKTD@C({!GwE`hfo4&@998;7>#1g9YuR#9v@js7*GaRqP4k?|U`geNjU%{z8BvV-)pk^=}xFnY^R}(%~aQe^lWvZ=NvHGo$(q%X(GmEFaBzp;*n?BhdEp~~O)%@g6i+;wLdiGbRyeK@mLC?sxy@KGi%mA-t^1PPC78YuzqFfCxl6!$&BM=!y;3qRL8OR>VKn_R-vPUuySIO{NEhA-VooBq&y*k;J4S?AZRwPd2?bT;e_A)yf%Xo^z(Gp``ke^6aDwG#_JdM?18pmspyvT^`o9E2GcDxj9afRjO^|Xi+Pv+=bq_bo&2QR{A>FO*a*^40X0Ca`9&_SetEfVIeC?B)0BpNA_7O&g?y!7TD_EK%&f2^jnfNKy;#e+pD_7XUUDFY_p#$RHm9fWzlN|th?qksnu-(0+CE7?on6YxTSc!j^l$}{u;^#-QJ3@JYr&)!>VQI`FYduQZJJTxOf^{FC>=Xps-nXEu7nBwAa=ath;hs6_Jghcuc{t|iJqI}YN$Uh8kq~+Fu9F>!mnaCw|r4x^8NCjd6#yihL87C&67XGD#;BgC&@Wn!p^ts@%C<B@c3QMuMAR;$utlXr><R*ian=DptvSV_SoLq4CTu%e5SOG|rw^}aR@AGCelVn}cWMx6i0od6=B~ju-jEW~{sRn|U8h?$Q2dPX?Hq&yYmm!D~*r|5sn395JvmmYH9c&6GUn0?Y&Z86yF)}=vuNTV=b%d%7o<p14)3yb78gn=3j@7bP==<~W8Yq<)y1<-ye^WipJG5eHKqvIh<>J|c3{mFD&0e90z#p$cLg1n6n>6!d^U~n#$^I!Ugd<P>d{WF8w5+}@nU&wlm=H{Vt4Tpa${`g|*Uy86Z1SekB*NK~Tv>Q{M{}f4%G`t<$#{Z^AIl@(Sw8i=V%cjBX7z|!@FtCu=CRPSP{G0CR{V>d_Aib*QYPe|LOG3@|GB{g^u^o9lD&kG$7a7gHnY{)9Vf^P-q}4UXZJO7V5}@Th%>~`=9j%fKTsU6fesXyc)*bq<BI1H53-$ovnn_@@nxqd^_#8j*GsG8HAtm@J7y-_M1kb@H)LjZ5b_E+bf!Z(cN0+N6CFdcbqt1z;l&@7{3bM@4e5%UsgA8&F?<DsXQszzm4YgT%tx+NPby4vF{xzlS!K20M3~Z{(m)@cLVc!~UZ7qhrWRA+Zk#}P+zT`t<X8)_dJswNv=s6V9-Y1%{(?Lx9WhtiWE*f-%4^W)c-5Dp(0N0<!#TD*?zZhP&dYPjvy5Em+`h5`5>#%{?d5v&3Yq+`*ie4+(hh#0EZ_2zCw6CpQOg@uWxM3W$MMI}-Fhm*>*sYRZa$9oOhsrx!aayVD~)*gYM!H1kM$(w6Q5{yTjx~|K5BvVIn9y%F;43gWC+dYK!6oT-`CS39iANUd724Av0BKA(TuWW;<$q4m>O=-K8SJhv%|rjd2qd~h$N<fXIj@kyUggp2R{$KOt%pEoyX4)4<disLJbpj^E5u8kVDw2)j8ea#GWzD-Oa(`)e|R{`SC^r4ZWGRRLBFc4i~kj1rrRI8O)CsrcDpBtid5H(qeR=A#0~@KW*pXiYh42gsj`0Het`}M5ll|M&hmB$z%0Se5iTCC+irPIXU3bFH|CzbE9pIjShxJ8IB$V$HFHDS@09}ii&2Bm%xJ)<;^jqafULw0!C!$Z&T?3nTo<0x79~9Uij5K!Y}^Ud>s+}3Q6HnD2zre$PW9ZgVVCF<)BoCfczYW51Jef(fNr&aL4&iQFRL^Z`fzN&McBTxHa<QhUT#J@p<&iUV$11m7h!;Jc7z09z>Jm_g|u`2DEQJVmge?lNhoG7Qw%N79t9MrE_G5CnbEN-=iMh!OnH!rM<<YKCWlJ4L!Z#3DzAEey!>xp7g$zV*-X;gMx%kUvY4L{Ctf6+CtY!%T=fLDK`dRcd(*=+L=pat*xRFr=uAs594BaKE&7Y(|`Q*{{XI~uVn')))

_TASK_ACTIONS=json.loads(zlib.decompress(base64.b85decode('c-rk<O^+N`a{MoIp2M<dIMVt?k-ZYJlt$o(8*70O1b7Vt#`+-pX86CG;!IapS4Kue=6gMoc70N-r&;yBUuI-v<PZOI^>07@{I|dUeDzO1Tz&uI-Mg!g*H{1k(|`W!e|`Gm)5pL4^z(oG^}j!T{^9DY4}bab#doj2eeve%`s(HV;p+O?$Loi$zkhrG>ch+TpT0kQvw!jFzt4|<S^mMhZ}$7|SO28&hmZezeb&m?FaP}E`&Ao~_P*P{d2?#f=jVU(`tANod`P<a@b^tqzWVU`&8r_j4cq$<pa1pJl2t3${o`MrUS|D{_jWsIZ(h9IqcQv8>bv{5@4xxnb@b`5fA@a<l^kQZ9`Z?i{K3sxla`lm-+mp(JZYKNjF&IA^A;a}9J=*foSH-a8XNR(zkl`Vx8LsH+<$j<z4M3baU9m`3%vKSH)#AGKIj&0-utIt{(Sb{_>MSYa16hDzr5$H9h*1qUu=8&?*2nqmD}Zv$K&wg{r)ZKbvD|^_rOiE=}KX<7;lc_eVW0C&aB@On{xc-;raFXK92SILQDI*dEI#{n}Z*h`stbUedbbM4jlR3)x6Fedw=fZJHqSjkv~7FclsbaJr9k;cFmW2yR|iV-{LheI@;v@WVXX_Pk8U+H}<}oHQvj6+1pNs@4WYt*PYswH16#E#+<SzA3uPpln*|Q3;MKqN9oC=q5flE-oJUXfBF8$KkeVXfBok5zkD8q#7@p^;lzSmJ<>NMNmJRmOP{lxX`2=$HdQ$A`53J>Kl~xu5Ym)Mp2RlU=9#bF-hZF1#K*raU$JGkF~4`oBNuD$;e#Ch+@#%E*Bx46&{=RTTF15n2QZqbfwgB`w_rwA!~d|9%AF<V<f*Um*>Z<IK6ll?hqYIF$kLSMY4KPa9q0JgrNyh$It)GAIUAb{jf#IxAMYn<2Ki6P$F^`2<sDlYCL=v-+++Ur`2P>Nn1Rp)(&k$c!<GfZm6E&JH#~~w1waj!4+Vq3HZroW&rfg<=nJ+KGfN&@IA+%wC%gGZZSBWLFJrTOuy6<eG6H~|<<3LfYl~hRCv$|LPfeTBQ?TK@uIk1^n5NNaiux^&`R2vjf9^D#KOOknr@t<*OzppS@87;Se6@f3_AlOiuRF2a8LLAl0B)-nG+P1s4`5=@md#)nO^%2YA78O7@PZ|L8aH_EEYDsn!7#Cg0k$4%@t)<NTTiI)6;j+ajvhEiqm8RO7O$w~DXC?NA3PuFB7f2y186ziL>r*#cY+I@U-@4QnSIed_y;!gPG3EtowvN5*?CWG)jexjb;y=5Z6xD`(bnTjCcB{Z{ReI!aPPrmaKQXS02nd<kU^qPMsB8^-&AJ@<HOC+go}ayw7wW4hS_TM7G^cBs;Xs#EW>DA#IfRVS<_gIW?Dp-w#%hA641PgCL9=((^SX>q|7W7YmBc!Q02fF!$ygo%F7;@C#MHO7hsu2`D{2<AzZrYPF%t^Dw)m}aQRO5)_Di#pp~`elPGt1tUvnAK<97AJe&a!f{mIJ*h*vw3%+no%HM!-$p+)8%*@f?Cdc#$NHEjz1oRg>IPA3p7y|%&WPou8CfS5}Nw;#KY92lrO#s4>J$;qi&Ym0TgyN8UUwH{<7E)Me3q2cj*IkX+h$7Hn7r@_@`58?^DK7nGTuu!n#GZkXigxhH4j@CaZcu{cUSOP})x2zN3cgLld!d0y@2dzc8pJGN9<Db~BrR+VuBM^5th+eE79;EjgM^#4w97gZ!<I1_u4j=Ph>_Zu6vSH2Uy$PH%rK689UG3d7V_^Q9)G$HH^<%WWjKF|fOj#oI!m8;TEsSHJA?~j5`-I1#&%eq=k<VhpSC+9`6(XW0H-kfL+(jUvLncuy1h8+<L?|)IqqDuT;r3`F4m6*vlbAX6o>5{+L3#Bc|R_`985%qrC{<`MHWF}QkJL0kc@mTnUre!p&v5c#utj*4J&6Oa(N~-xy6%VPma&4xUg26JB(2$<c*sAYsJ#TPV^9v21x3ga~zgW4Y->OPTNb+t!9>=h2u=vR9piT>D4@h6KYT}2-e-GHfb^6@9#hT=kDm|fAYv)T~*LP;5aXRp<wA2&U9Lr<o!b+p!>I?kq!_*a2UrSK@p?PJyu3%GAa_-0Vl(^<P0PcHLx0<ZlcSsWJJ(%o*%||rwm#~kki&Y_iiHQwhc?;>7kJZ)L3IhZY2hs35+J6J{(W(8y;&&ZHfCXo04TYetm!cZa?#MiDqa_=swQ&`sLEHW{Z4fwD?Q&LbDC-mULpS!BT*Mm-KAy>^8C<!7fTh6r@L{8}B!^{!X0)X$Np|!Y}2b>j&_xQK_uEht2cy{;|8TKVT8S-=RUvWk{+$*1ZZl26jT8o1KZCr@g^eCD(=E@xtQOEZQvrUC=)CX|w!zS3z41`%iJC!opZ_)xkQV-ja;weUy+j>iA}q*sXDbTPQ=rnd0=oBm)?R3k!+lKN}YGp&Yz8#Y_UkW55gr%XrR0XwhaNG(v;XA1{Q{lF4fX5F63AV2%yKInX5fC9qa^v(k{t&cJ?JWVVkZnjX}D^B|e2(hTA*QF*k$(<`d!(ZB-JM+2{x(^>GSIiWx-N<Ei=HIX~Z7x3QEzKD_0l{N|<Io{HeX3Fyte+xvDK&nDI4>6oJ+S=&9QLGeB08{CJ|7K<fqRj#98A%c75(7~Nb_@zdQmB3zQyB~&T#{R#jS;2iA{MAlU1X=qR1oTl784Ym{37r^j-A9zsSVa&o8(lz4~IxMS6V5kOW}5KX3_a=TW&B=>#r_~)enbtna^B^vRT3DJcb;dw9$@58gm*XFR`Z>laHnWjRc6Px*q@%Td9#npU3VOhz85!`T50T)Y0eT95BH)bP|y{vi|MsH-CN%fx!khJpz%I6c2eC!}CS1?>=6@IEVTtEiZzOLP4_dwqU)RQK%f{^FzZs;IcDAn32Yf@Y~1${{WgAZ*s)P4VqD4HT#Yd3s0~1=7}W{n++_hNUD_Tn~~0jj(;x2%fN?D6d@)n0GH?ty95*|;0Frr1Sibn3t7)YdLWC520@CRxY@_JPxMwi7t9Cvd8$EkovPsH8rTE06?NeO5+%pexzZInMdm5@Qx}n_TQI)d&ftd+jDLhrSwIC4XB1Me|BW8`?pdHbc}E7G2LMWkTzQ|%dks4BV8sF4RvcL~w=TQu$P@r+=rbjWK~?@L3}%!;5ZxG1_V;#xod!hB&^*(-a_6-+EVqG}YM?pZvlb5l5{=u_JxWQ}b<L6P`R`noPq|6}h_N&bz)#lE()g1H_V?suEeM9o&*T@ugoL8se71oF=G+K<e?w_Rgdli?{dxMAyN|VW29)$o`!(Ry=ZUx_t_8_l$GHv=ic^gC;3N<p`mL!EqRbq?i%<1lOR2UoGB%+%20$07@Cw%8-L$Fos~}0S1c;?vL2f!QVN0LE{HApQ)micc%Q14M`BVfv987zBX0B5-z>j&Z?OD*u=v_oQsMlY0`a61mVsimU4BCrsg1QC_*ruvDpfA#bixK@~fC2YuXRaPzcqsNm;Dt!9o<y`0@%CP2vx6a3$#Q%UTWgz51K6LJKr%QW7O5aKoZO|#Qg#FwNXA$&gob9ck2s7QR&vy#twnDb%VfB$CZUd>7NBp2qbbto%3xrj>9Q-S<L24m3pdi3BZDZIt3NOQgJMyX<il{q2GIn<jT}}5yAz-%9mN9+&a#jfm-GYg-J43ju?t3{Px(V?i3Tw(+e1=lRRx1`QzgOt@#4@4yG)>$?SF|9z^hmZ2Th*sDoTyS6y-M^>>VSbwDqc4klh>3jE~!u=dKZIKmaK=7W{~<pAt7u2x5rCoBwXx?k2<~My@~(VZ_bY159gqNZ7tBY%!j_5L55KQbxz9fG~L(3bX0T8UjPBri<>+c+If-1TD=K;DiI)Lan~#pAcI2cFjCn$2698q}997R<}7)(d>j8#R{`0IVM?87$J=v+rSJ<4K1<G+qS)-b|hDPyjbEjYRLv>1I()XiY9?gkl!sg0^k_-xwemVIY5+&E9(APRl~XwRe9MHU$Bs6>6V=AK_n3PSXyACNiH#H`qC+DDq;tjwB3yo_ZAVp=`o77o)p43%L^`bmG4(C6AOb8r{SW}%FB6@pXodMXL!y&uevVaz$LV|?3%XzG2vz3OiGnV=KuWv49=E>AzSN|!(8-}%Q>wVCDuWin~Q@Oq*8}ODa^pxtri|99BHz2Z#&(yqH1<_jAW9M!Dyxud-;|)=AP#@j~54Q78!~kR0rjlQ{%S{Fr^3Fb{Y9L+MJ|HcGrPBX1y%%*^HLN>bGT+2GD0oWpZ5jF&BOALrn<XR^hzF!eWq(S{P*Ro5M@N*|=QNZG;UuvvjM`@`&}JY2K%h5G~}MEP4~vD{&rT%jmjh*agsR7|ZIY3i(MF3FE}T*I?fH_5hgSrV>F(1W}x710%%x{78X&-a=}wX9jJJ0L#wM(mj)-o9W74cc+eL`EtC{(%eXPeJ}gT5_MrQCyJH~?)Oivdwc)hLSdDmLb8IedC7h3LbC9#U+%}^kdRmp-TPV+cVMGao`wQ+YkM1Ppt(Sm@Aj*>BB~Y<9@5|5bv++jafVu9=6>f;4V{9>&%l;7?_^HetLMMeq-P3c@|wl9>-jj(p8YxrIWmD`h+5J^U+z{h%;WC5$%Qc;a}+paF=XaZP%u)iMGR;*j@pkv3KimJ0m^|_u1w02xD`!{C~*_i_2b9-J$4~|UMUhl@Gb1F19Ocd@I{o#_qk$tgcTDumVcuNW3tjc_e&vp(0PGYz7mSI61pB<^5sB<_9|D^<1wEbOMZUSu|GrgLBLfXk6Lb|Qi4?@J0?%ExpuuTL>G1r$K%!JhY^~^fEb(xPZ@+dH!H-O$>xlhPf{azwqa91!q2kcFt#8sa{HhiIuHyLRLwi*N1zTC{GYDoOM(UyUrcURsACzSwizN4taxOyrjs=%XtHVQ+WdkTagfQ%*4b#8p*$^DX<s#GGwcQPAkZEw?&1S=y!dNb2@QJ8@_@wt>#u>yvK|?g4(1*9fLKXR(%Qun2gFYR0#>ddJ{5)$M9v66^N6gbZW_Qa;P1Seev3z~$Cuh)H5dhsvRIumSaw^2SZvLc#OB>SH4Vo9k|Hjw&M1Lbd@39xhDeH`IJ`?LCM2YyYhA>=0CAmks-euG#4$e##YBfXQo7b46e2pI2Ao1X#fzA%5SDV!c)WQ~2VTIwI)1Tgj4B>xO6@d!e_ATxus6EHsGXQ#B)rtbj$w6?U6*2CM<T%0$_`IE{-biXCIE=!XvZ8NZCTHZve^=%alE-rYhZ-qsupqcSEL{)Q`>FxWvJZhNQb;S&dyFxywd%|p&5{<6isyKh|6Q&S`QHH;Xz(wfL-pnJXC2?a^}!R=xH^U6mp7}NBzL(6*ILugGu?DC1OJ3?i$t-g&6Y9RB&y<B4CUvf*7s$ly??S0E<9d3khclRl8E+g>E8F2xPuK$2*#^im71A2qB~(&G|yxeQXw}IbKmuUz(;zp5Sp~6B|Rl2bjl~X>WMNlt^I}(IoA<>6(7GrN|jDR(YKlcsQo|Lw@RB$+;V5Ih<yu^rWORPp;aTj5-S6gf?2-2TI-R)g9Fsr^H*T#E8t_Nr{%zxDYa1%PXv-hz5F%_aH1-I}J)AGtZl4>XcBRh^WO6%%<V~E!k&&c~Ow3N2m*~B*CZ(Uz?dv$m>?V1<iUpOpRGHH!?9E%UTj!FStqxV2hJ!n<TEQ$fPNdf2by><B*O3)E)&0_SzBJ1j}%WHjGJvP`lj}rI?loQcX6(66>VHDT8tj(xPHjG#v$awJ<8()_~#MZRS(Q#p+oBBdNKllBtz9Q_GV@E|kncq4<WUg`2g4F7wD3q?vx$D1<AQXO>743=;AX)xaSZ{GmdIh(rN}Trz3_5lH(y*|)=lf^{71?$;0k?GpuV^e@-Y!EIujhu=g2j`N?8T!CjR*g`Qay0y%RA{soO)k);h14bn{4ut5~Ne`PBF7E*tG&!gsqgAMV&TKzgNMz1PE8^ICz2A(lZWuM8HQvkGZ*x;mw8|LLt97WF&Ao^0Ji>d;9jBHcHj}T9v1?C-EE-&Sqd8gh{Mu`yoUXu7-po?QtC<6vP+rCh;JV7E{)~y7?zwUbTw9LE==nV5l&OkT6jz#-sSyIVF>^oVcDemnr6w_CobGqyNV*tAMi@@GskD}ycDdkHQCcj-D<(t`EK{MJ!FC!=inS!GNb%nb`A*qoob`4KK@92*7=bKxG0=1b@0K1RLjX)hF#h5B#eI7k>X#X+te~$al>q@K6x_j(nxUvoN>icJTG)y(?!<^mY*A2FtX+mO)z+nXaj>yYF&SwCIVEwy!UuTF>To#zF*{X~AJjme^ZGZ}v%#OIVw$jMnUDW);2c;4WMBjA1qS@C&_fn5iuUueQ+$*doCkae8&U-(dpD17-^!?<Wy86d26oz~n{?74nWhyEn^iYRnI7l?NEd+x18c=8#CSsvbTijKEj5t!*xX4aV}eZ+t(}AfN4zxLg9l%v<t;#v3Zdoz8e%GZOMm##7wWp)Riq9HTtsLTP%;JZ&J5O{)1M6ZFJ$z&Xp(ka7?E?wxosC@|9Q0PLU7ODIpfR)51s=Xix%QxTK&x^db}<;AC4CIvdf@~^9marD#szStyLJqtZ|)JbFI<KsWz-qDHi3mP_!?)QA&JnkQ0`s2qu1+JbqXiF&Br7ae0w#B=ktAaaWeZ+sR5j0zk@jl)Qo<cE3R%&zBgfV;0<~VHCa;m;%s2A>f*)n9n$ceO$5;7UaFzcWUg=RBTQx0L_jzq#v70b_6NsU~=(dgDsLNJCKfW_7@-hn$9N(XzwSLCW*YqN7*-aM?+_bROG9aT%1+JuBDqA?WmvM6tbBzsILk*ExRE?2`V_{#&vCmP#tNqbHk$#Sa28`1R}2%c{6DQS`DC14n=^vb(A~glIZJ4_qCKzhm8{}oww*`b0zzFaacRcD~<Ekv{!Ro6_)cyCGWTh+A#m0R8_2%#^YHiBV;My&;aLA8kI?*t71r&E@<F)a(#(-P|{xs;e+n5iVS`RRv0HnkssBkgG@<vk!kmq8fBxH)b)%M62={@aiVh8Or_8XP0kUe=**xwB%II?%Ed-MiK*K~I^Doby*8&vbp!4frZ0%3H62xxQlIb*Jg-zpdW?Bn4-4DUOd*IzbY}T2NqqF?l1@2Yo@ywix>Qe{4$G3NsnSukMY2^Q&zBWKfujE;aUe<xDx=H3ooWgufyU5X7_Cc-7<62$HyW{_dStYy#32AQc+QB1Oh_MEFPEE2O_JYc-dD<Axv720G=-XojM=FH_s7iGqAc!q4!Nho0W6*lTZv*X&YiwJ1`SLhj(2I1*g13EJbhy27`<a`DZ-2!@Z%v)!qX+NS=THz)mqYE{X(9XV(H6-Y<rlQU8g7?R+S4q)T~fbHDKf^O|h>OtC|e0at^oSg~nW~@*W6x9asYOngvzF2N)d~SIJ5yv8XS7QavrGP%*g-sUEzN2r@D-OXrlJ%`{nPnNKe+p9_cArw7U3>m<d~fdu&uv6hsajKjnwCmF#sFOd{Wq+}MzBupuw(|8ook4<ZeLDQ3bBZ_7Zh^<mYz|JaVssgt46mJ@G!Q2)`pK3%}MPu;pfA#unn~(79W}pZ$6QLteq&@P$tv5MFU$zCNSJ(C9Fq-oCz>6CyNE8<iKi_#tAnv?G|ALJ3!$N;viaU`s98rCHHTP6JjrF=-SJ_sYL!v`KxFmSSaKqG$?cX1iQzqN&YGfNF$kWyAIUenoAmMyk=P&o?DRwR$XH>AqAo9Dav3xpgDh?|YeEH(QL^;W~NlWw<Jp)V~B{FJQtq+yG4iE#I@{~B&4BV0~7r2xv$~ivU!<IGaxG0pf>k*4BTC}^Oc`jqNMskm@69#tle1%ou%J_;b94G9$%iJut>?==Q!H5<u&B7SVX>XrG?}RysMg?Z6QPb5ttqIS`DqR*Gu6eqb7~Y9&6qmP5Oi)fXv=4Y9ZcW4S$&7C_5whL?RP3#6oJAT&U6Q<!@7LBN7aY8!8%)xQxMK7$4=tsQD5sv#12U<4O^Zrz!uCb7Ew}P{z|&Qy3ol5jH262CS>^`;^_s&t+k~D%2|!v}J12saxGA(WP(cS#rp)DQtwc=H4?WIrY+CqB8dxX-i9jib!<!KD@g%q4J!7>W*IQOr8<*Mw;f=8hc0zW#s`s<|-62Ij*Jo!)=kH6jpCjIh(VyoRRct;-hwfxCR2z@bidfHXT4uCg)TUrFjqre)y3LXU0+S?ac~v@bro;{+BoI4bE^@#<hk1DY`_X)+(AO%fRg=zrKDb9f29TM4RRCaYiOEI<VQ!95&QzCqNFhSCL&<>4GG(`Y?H+Q(n-1aLDc0R5rZ`o%3Tm%aJ7+tmGm;5)5g<^<lUCuOp!t)O6Fck;Hi5qr1ws)XR3Sd_vOTbtbjrp(>@#O&dz8+pheT{ftE7-~0iW+CR4A{%Oag?^G+el@2M>ey&mzLf6v8K>76kJeVGqjzur`LC^@25daW0vRV7?T?Bej>=I-!nxmL}<NyWgx&PHylN=?TrXZegx?m|c|M)FK5ku`e&uKV8y4lj31`;{Z)L97-A#BV_<$-klDDbcDhIiUkK$r3XX>9+>jwH5S(m|A&Kl{C{pRgFG<koK}2|V9=+n;8hT{DSE*Lf>fYG{c=%!|MvdXhnJ`AYiYSMXF0Oyd@%@cE=~;3Hj029W{E0w<X8b0H!rZXF;qLcc`i|ZXQ}-{2^BwXB#e#`ah?j5nxR2d0oIGZK85B7b}v1+NIDY!HYNT7MU66>n+wN~jq9-}ZdvWeSqvN=0bw?-+EKFp&}4do6uH*b=WLy;SxH@r#-^AfS>l;DB?7E(p@G>}@0F{g{@iCjVFnBf&nyPON=S3>s*YWXe3x@6Ic3fUFP%A>)f?binT6Z^1!gJbPOMGFR0!y;4i9XR?riem+8jQLoN-tI=qG4k<*8_Vg%E*vNKjsgvI^X4><xi({7<y3R)^KyjSdA~A(gC3jo*rJRwe+JuuhLS4Rc9Z7z46gIhiVOdcL%*K-lc~VXG^YL?f;x;gun2cT?f1+l#|f013VTIt6U;K}3otr`-)Dr?DJxyU2z_WZK#}Zgv{mxV%!4od6~qTkvdbFv%~PEbLj?dY5TUi^>;j5I5>8;V3l022?7PgT?p})V?!@_&eoNP-fARw6w?8Cu^_ng8Yh+qE<?mAx>FG&>XA~Cc^{_$YW&m;Lv?1aFE~?FGy6nAhmf4O#mUfL`%N{z#zS$>xU4U3EH?}-DDyl)e~K?gw*gd3Z_&jc379iJpcfP<It&|4nfzdn)Y3Xg}};zmAH1ye(+T^Mlxb^#oBC@nDB?1nad{-65td~7n7GVwmaq21}}I7HkB+ZCc5MSj<QDJRDtOlD~V_M&^+uM&dw+&v9W9bvseMNp6qJz+hHL$2{>gbG6q(PfET?cjug$HxoS$s3N4PXXPv466cbw4fI8gYzX7ZKkrS0{TUBTtS?03-#0FgAfY3E6ISD|Eab}Y()qEl7C=Dmu*=kHR)u>TDgNFp9iDJnx@FTm%T$Ax4QGlDN)H6GyEh$k^*1)bgrd5rX+E{nlV>*J6fbfnu3^j#4jb<m2?e^pBOe(I-p?r;rS!`1o8UP_<%(tZcZ|;j+tdNm|d`Dtj$+2)r8<Tx3C!I@IxnWz01@mV3?iH<hu>1MaO4Vl4<Ult+r=mAc^(;LSQ!q1&;&>oi<9Ne^pa~N^w{Tel7OjNHL4|c#L|j+p%R{!53lIYa7vn7nB`rW}BfEoy)8{6lS=3B1uv9|>L(!}n*PJXT!ojStiVNx$#)=$59Fv&8R}G4BH-I;3>IsxYsx2)xDORNwz8svot}TqprR<X&R{;f%h&7V^%80Yn{AM|4nbkK9_!Fs?*cOdmF8nJjNoGX>j_^l;^Cfp>&Xs~&H$ir+N_3Bt@JA^;M0K=~86BufLSnu;@LayEiZaopufL1rxm^N)T!gFiM5%K^OuHaT*C`}zk&;xvx{b;--Gph0aKv8C&LP8!(h|?jDr+4bqSQ&MM<s+KV3t@*!WVsH$xMFBZJfByX<SN^e_dO+p!Z10zIjC)X^)L6eS_(5$Tn%7pa9*RDoYOcj#TK;#rIUMYCDeHqT<P7L@oGsWxN5N*#&jK+i<Xy^RxZia(YJT3Ih%*Q(G}Kwyjc;N<YQ|M<cvjNY?aJXa&SVNjIg#x4=Y07o7lqJ+yxMNl~Z%l?3uFC8O;PI?bsDYzdDQA!KvegcEnP%Ix4+kT{)GnOCdDZpAN4iAUj{IeWT_DRfCdeBBnwJxaolR4&U-pvarytUX6>T-98w$SOs)3|;bS9kH_EQVxm%e6ncVjZ63uDpycC$-XAi)5W4OJqM~kH^WfU@d*CAkzuMNx>>}gh#gI&I@L1X@Oi(~iyR~~O~Q~2|DN&n^TX>&aUx59r6^;00iZ~jID4-QMBTcXC#}u!D=W5tkqk+)&|L=ALCY`H8kGsPc(t!Is!_`^B7QBw+ek4VMi<BppUZf)u|loNbF>q8ga<s3)m2Ky>GB7aps&c^nUeAWYYQp3M9YC(PArF9CNhhHCWX)$Fiv%IgHSy=4eoG~A9D?h`yRWuaFMChOSepP%I)KK!`u}|0dG;rE)OZFlPq=TE=i)$>y9W&9*SPRE6BRjM*wws)#XCLYGRp;7oMVLE=}C=<nbI!1FV9D3X@l|#S6d{<McRtevyP6LK~_oQcOilvQ(0}M`LT%KU-#pZZnn$XxAM(9v#R%|AWKZCB&b@o(X0HP$*R+E6A*u0h|>^_d70@2Fvmx+~#J4^t14$cCG%}_0n#v`Vdp(XU@l_AP{QSO=~*c7llSfE2|Ot3pd?-z)iC%sg>!#P~Sx+EEc6p0r97-x9Zalo<QOkjQe8`k3+~(PsZzw$(vVMh9WAiK!;g%-N3?-cwZ^Qz{^`pV?I@__qZPX*exJRQM|2(u@M<+5zb7!C3c?7XDJMx>8u1Z7yEE28W?AoK){fY6+nIpMKx?))vhC3xcN!qMh5e+$WV_=(x_;c1)hUnsTPx&CD21Xm>oe$d@Mm~I)X!Zq_j+?%i;k^dKOezO7T)U_i(YJO$*QH?L}C(^95^x@(dmMe>(6RYq|!Rga#S=QJIopNq{9!*5OzxaMoH7%o0Vs0Lm51zK!L1QBH~w%u|}|pr6*(Jfl}ou%xD^4I2q?pNI*izb-EJ9=3D)o56OZqL9hR$x&r849_nB<N(-)pvU;AEaYv~1%wEKBQ%3hKzcu@jD7GUy9K6rE^F(v><R>zcFhJNT+7{X>>Wx6d7$K_s*+#}WHG!6yBf0SlQeI3?lDgyK8KM!4_(TyW5c5aDyH#cip&g_x990kICAgtp-qjFZbAFn+}TllCV$5^L$CO{ub#w~gT*ySCvmv&eWBKvkrLV{h^H5RD>6%0H$7m=%f8RUA&Gb>M(gFfLXLu3CQ0Z(aQKTy2qn7q^hM~AEBI&e^fZsZ+I1np`{**#bSSF~_|eAxqJW&Kvqm})O4QP|j<C1R$}1p)9?rgi5cU-gz{%Auc<LU-*i2d6kalZp6xw|}?L31|8E8WmY2r5JO4caJjN(LbXA2z<W4^yg(vhB(EniY>>m;b>r0AZIjZAK+!O77##IH(e3EqDuU~N-cI7@C0q2)&4AVuqKndVL+fkDY0luNd&@M3U=ne#P;vSceNo-jZ)fR0y{H`9$Cb;9#fR>6v2jK}0-dWqvUq#=!bIZpwL{J6D(yBr;&M%heo)iEf})=rP>rU*#b1;OoHK4^o)#V|=H$<~cZJT5m$>mp3F%vGn}7mNN>HRUnwtyytM7b_Wz#;cdfvokZ62e4l)YqDqVH7zM@=XrU+E)s7LrOq*yo)2m6-xWnA)DEfSw-Pw1*EmngM2{T^)fs`#n`&HEh-*?wL<Wbe+Q!D#=Ie}Ryig0T9{P(uEO;j>+d>3zK@+_RR*`sA@h(smqGShbBx|-qdw>qojVx>(#aI|oih&0sY3m+Zl&P7hX?pbXIdmuZDd5l9hng0m0}UMKbN6f1<yOQUFITSX>t_*z7KRx2A#J^D;i)sNAh}j5C}}b?N)8eiNb6E4x}jS^@nbS*c*uw=kGJjT(r?BsWs6Hx2Z`Yfg+RBTmsM(AGn3WH#Zcx3pTX)DRQV0YsDL)Idu@HP-L=dhZo|5K4$(~N%EV^U$R;x%py9*~pQ@K7RZ)Eo7KapTn}Hczz^1MsEo@?oGIzd%4G6qw;8KvfX$8uq$%Oc5o`8fkor0oYXv^EPN?13RCumv5XJ1OY*(*NhqrbFUuIj{{V+493Z`ok5`@rJv1+Ttv7c!j%S{)?@MT->VitAO}jA#jLR`0q8=qM?;UC5VLtDhVoD++8Li8guB6|r5e0D&b==5?dv?`Es~IaxU${|^_d+4c')))

_TASK_RESCUE=True

# Keep demonstrated market commitments while repairing physical prerequisites.
_TASK_PARENT=intent_agent
_TASK_PROXY=make_agent({0:_TASK_ACTIONS})
_TASK_REPORT={'errors':0,'late_input_requests':0}

def task_market_agent(obs,configuration=None):
    if int(obs['step'])==0:
        for key in _TASK_REPORT:_TASK_REPORT[key]=0
    physical=_TASK_PARENT(obs,configuration)
    scheduled=copy.deepcopy(_TASK_ACTIONS[min(718,int(obs['step']))])
    orders=[list(order) for order in scheduled.get('market',[])]
    if _TASK_RESCUE:
        # Only overdue task input purchases may supplement the demonstrated queue.
        seat=int(obs['player']);stock=_project_stock(obs,[physical['farmer']]+physical['hands'])
        plans=_PLAN[int(obs['step'])//24]['tasks'];state=_STATE[seat];required={}
        for actor in range(min(len(plans),len(obs['farms'][seat]['hands'])+1)):
            pointer=state['pointers'][actor]
            if pointer>=len(plans[actor]):continue
            task=plans[actor][pointer];cmd=task['op']
            if task['hour']>int(obs['step'])%24 or cmd[0]!='PICKUP':continue
            item=cmd[1];q=int(cmd[2]) if len(cmd)>2 else 1
            required[item]=required.get(item,0)+q
        for item,q in required.items():
            planned=sum(int(o[2]) for o in orders if len(o)>=3 and o[0] in ('BUY_PRODUCT','BUY_ANIMAL') and o[1]==item)
            missing=max(0,q-stock.get(item,0)-planned)
            if missing and len(orders)<10:
                orders.append(['BUY_ANIMAL' if item in _ANIMALS else 'BUY_PRODUCT',item,missing])
                _TASK_REPORT['late_input_requests']+=missing
    physical['market']=orders[:10]
    if int(obs['step'])>=718:
        projected=_project_stock(obs,[physical['farmer']]+physical['hands'])
        physical['market']=[['SELL',i,q] for i,q in projected.items() if q>0 and i in _ITEMS][:10]
    return physical

task_market_agent.telemetry=_TASK_REPORT
agent=task_market_agent
kaggle_submission_agent=task_market_agent
