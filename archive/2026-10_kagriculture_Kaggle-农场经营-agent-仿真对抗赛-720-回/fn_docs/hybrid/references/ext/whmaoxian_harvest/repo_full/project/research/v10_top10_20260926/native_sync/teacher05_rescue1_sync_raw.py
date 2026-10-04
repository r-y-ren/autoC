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

_PLAN=json.loads(zlib.decompress(base64.b85decode('c-rlqTkj;vaoxYmJkLYkFM3-IN8*A*?P7Lm!X_330U4lSK(Z+bup#)ndsZSjeW{2zC$g$9GYvlQ0_Jx8yR)hyBhLAq-~IcWKmOsL{_$Vl{7rrP=8ym5PyhY*fBffv`_rfY`n&k{&;R=A?VEr7!@vB`pZ~Yt{rj8$^M616dwE+v{jdN0zdrrPH{XBz?pMG0{>|Gr@4ox(oB#NK|NKvQ^EdJBoB#c9fB45g{o$Yf_0xa(e{VOI{_StR{qT$5fB(%7KmO+9`!|1Gne3I{fB5Fz`|Holz{<Z|?r(qj{+l1)yv=`IT<pc~zB#?ly1gKuEcm<k?|<=mL6<%u3kzb{UXjF)h{axU{#V3{KjWvjfBBW`*4OsKFW<la{`5OP`?b>MA0_<G)&4sE@;hIBYO~j#|CwF-vCcm1A3p7fH@|-W;k$o0`GTUo^ta#q`2OR`k|Zrj=BE{V>E)*hUu4|)wEx`opO+4M>E)+QX}^@WmEA9S^R5wpb>NOW|J9pxH<-Wrv{zn!G2+c?{|w1qdiiNt`sJeeY0X}G`DtBR63kDV_R@<_OF@1lRrAGj_Fa~fM?<n6NaFK3SudU;ZA|;ei1t$O>5_m?EA~?G=@NiX8}?G-=|aDawx1Bfj}N>!xowk>Cz|;DE#`|N*h??J+$jAX_NQfg>E)*tX^H(j?Do>jPaE>aiPm2y-uU7^9nuQ>c^K@a;O~}!Ps{dF@OMkVr!{*i_+|<Ar=?&oy?nD=e3L)@^z*7epMc863Fy;qd;6bnVD0?#?z;~k-oN|t_kZ{P<B#8d`1Ze@eq6v$GAGNCLsW)7Kd*j%<quQ~HTq!BM`CG_z0b3#)OSUG!X)VDD62n5=YNi5*C=Jb(`S<INcmfB(zlwyn+*6?fAR6V@88(_68RQ8djy&Efjrt@qO_|kQazo2Tv_=xfak;c4rz9YeerDsd&R{jjMA5oz#Y}t9W__J!x-6*OIdk~)vLGIpa1oM?=kci&+Io;>DqYm^=;&f)WRQ#n!V(g-+cTp?|*>m=j&4VhaW$F^V`3D|MBC0J?!9?j(LuEwqZMn+w|gqKkZZc^{-IuMZ%FXR;Zz{)ryFXt)k?1OFHTmyw_V)>%m68gO}w!oY~i>c&Bu_;WPQBO|+L>@7F|^DvhoXJ6(lN=tog@XJU6J-+~`}|2FWQ_r&*Y3w=aJ4&>KcXZTO?kw3*Jc}s|k8r=vPd^01^y>9tO)xPeGx8pb8?}fk4>TWuxKtI3KKFysf-1BF|gH*Ig?b7Uqqf~}OsLi=qh9taa$!yW=*`oBrE_ohy3H{S1eVvJau%!I71-V=X$`9DgzXCIV=7Pr$TT8At(tMP{+cju*2of9v=E&cO5k2Nk`a0#a(rNv!{bZef)1=2Kfa%I7s}E9O_I+^}$o7hhCq|(U9D_a7q`)4WQrxeCE!tPy>F#NuJG7CV^TbRG;R@SmzM3nXR*+4qAYWb5+jU7Dij!jxtxr@TC0={zkof4`qDDWw$Jf+n%zR0uyu~V_Zb3U9SfMiLLM1Pa!T3i!Ex^8fOx&-OLeA~guGOV;J0?ZlJhw-_+y_nw@Ngt8)nylV%|xoKT_?fFFjsU;0N<nZgHK2TzV(AApb?E0ugWp9**g+1UIVE=Is3W6QZ#{uB~T#qzK_Y4)K}-yhbVWSr)7HO25RiPW$adJ9Dn$AG-3kS+}uNy`PjlbOc{{;L;mC+@@uW`v7--T$AbMp#bXR~NqNU!hSrdt^dVZFk>0FPN&Z;Pz8fyydB92cqEVM0vHpi#rAu!uxv1vVsld?!du=7TU@CS=iWOy%F3PstDa`CZnGwm4)5kcDT;Gz3E{-c*95=eipKOtz0zJ==AD;=VNst}McV8m!KUH=|RSpePJ~Svthpe3V*~`mo=9hZQ+T-uP`|gMLfU&P$+2Y@QC*QDXbKPIA`sy>I;Kgr%bD-Eu)vod9C4J-5HlLu~Ua!`$r%P;^S+bX^3W_9HQ?B;;1GES$X<AL2D-o~r=}sXntJ_P}?)vG^Mp{<4m#SKk&r1gIY0X}$9<@)GWJd|Iy<ROrl4KBCD}eQ<D$sDdn>XkBi5jFEEa{K&BHdmIc#KzRad5adw%4l%%+n>9k|sray;@-<iz9MfoZ1|b^SZIH4Z6D4ucXgn^n3$3yeSvxC>Rf!@F^Y7$#y&ut?_YPgbp4aoAhQ%kZI&}1$KW<d%1d=IDNT*+PY+~SLcYImrV2{tG!-TdY&#>d(=+;Q9D?x#P(A7DVww!Hs8Qgotc9c^rS58lTvBY@{M4=SyJd`iSSBluHj7DT(1siPM1Xf+@y$AD$vxqTeJGQM9b0-Vbq1<;R&e=r~Olar{B}ZKqh|@v;o$EH?gvOuBn%Hlw~QKNYoPzuo4iDfSA?r^o;}dt%JQDJcCd4oSN<R;6Z$D9K<(2vf1m6)A;A#QqjW}S`WL}7M6APv;l_L)~9{puJwgqauRMZSN3DY(vl$uStZd0OJ016^RC?}cHSK|j-xkR<<Y6#+J`r+-mwK>Ucx^B+rZlmEoDD$FVObmc5S5X$L$r`eiT+{`?2_bgd|pg&!(xN%~3LnqL3%4h|Z!Q#XzSO17q>kJ!Pt`L*}-<`4syDcE=~{2F^U*DACjZ1e-|g24AFwmMPM0$Mi)Ci{ky|uo})b?Z~7((hM#X2imiOz0=dmyB(-3lu^odC8J>fgwp35U_4!T<dGsI%CuXctaYhkrBQ#11oycbH;LyPYdD(BdqgYmMD44}^kos!SSi-#Zpjsimi%cRgQ4^nem(~1!ZS0H=4za=S8w6|A_@6dFHB`{{u5TVlxS?{U><>ey;1vD8BbT*khAE?jf>A_#3y)B3n$thn4#(iYmGSWH&1IMuN;)_Rt?>t`BKps5@<3gt4x!l9SGIM;Yn3SiR}z0o*_|I>bb*wK$))N2VKWcS|yaJNTRDFR+K`CGW$->>^nK{H9*%Np@--!)5(`>>n!u;I#6esky>}M4XzZ{&SIE1_CWnkWxWok4@u+43-&ts$BWXB*SHX@?WOA3@pMV&vW&Kus^_EAC4*zFZZB1*U-@K<DZ2bb+eHfP_TW{LV>g*&M~S_V3QzVG(8|PtwjCG!06UJ+T@gd^{2^c`Y30qOYNzRRN#l~VwwJ0u`{|O-C24IhRhw0(OU$Rn`Fm}9sk(DcmrPEKw!Ksxx979+YjJw+=;I*=k3pO$uU>9b>V7x<g(_^(a=yET7iy6f5AQ3k$lFJH#T8)t1bZp`ic<y(i@pBcyxI<FSK`N65p`WcLo=BIlX%CqV%W>H>8{ekz)q_d=Z+Ffhg%|`j$KIN*ytgvxLw?D^uWK-ga3^l_&0j+ztIE#Mi2fsdf?ya!T&}N#2bB=8PHAe14}a)s3*J>XrFjScO(U$%79~4@L6a<5X}u*9-@rp{DwQC1P+~6x0NQKxT70^%*dPTKxD@0;_huDW#xfhrP8%~ALvE?G*6+doU;~Yck**GvC^Z=4%;d_Y@?OVgB`X_TId{Up>v{}XR+|zv&Q$e23_eU-m-KUT%aP`a(jW28@N5VPzr?Y1xkS+EI<KNc{jMgt@NCUPnt>Ov=9}3%P)Uyc9^8uVM88y+if7_ktZxbXNRYoe_&?4Xs=hd%IT8nNEh2)508MRe*`qy{#d}9TuW`$2ciQER?aqAIh%Yi0-tq>4kE~O@>!vUnS*v?%*A1KxPk6nKY*k|+WgI<oQ4!pfTjPslM&n;fXLGvq)M{zc`}O1P&pr0UILi61q|xWDZoEKtQRY>`05PW?8RH>-j4spsA8jt)#tPqXwTG)$haCU<LZlcjKOnZl}Fs-ATp2x2*sT|c~L{Oml%QJ6pmAdGde^Rfj^&We^qw_nq&nAjf0xFUH$Z7nW0G;G%2j~ps>?(LY`|c9})w5NQ~&lahX~W1Y$;LoU$o1tw}x$>*Ao3Z~B^vV>|}#Jkbecinm>hrTqEwt+ChU;7hshlPxN^%lWSCo{6Zy+yc!;iEFo(gOpMh4Nv0iCUWhG2vzul73rryQ~Tpubtel-c%W0%+9CBwB=Oblf)JpfqH9TEls9l=s^9^eP<MNJY^JCKe1|~u9pc(pTi%P<m@KkmGGMND{ukyo2VPlY8v%|uJsl8|pie$<Akw3{LXYa|F{Zet#&7b6$`t66t8WZftTCM2rbuj?A_EK1ZJ&YBOk+ngeQh)|cx7&+RRgj#e)7_`iJg?Ums~4o7DR24AHgJ9K0)vI0*svtJ9e(X0`xhJOsxkywVrEJYmX-+9b)WII|`WmbL^(!JT-Fs^=m`+tw$dp?^`Noz*U<0UXepl&rarUCqY0Y{G#KTw*_|azy&Gzd9?4~`NM&>(#f{KbOT%9^eC>vo{B56ml>A41$Zd<ZE*xjQ?SuZL9ub(Je9_h?lSw4Z%U<s$S6B2qa16qet?kzkKR=?z9SieC(*a1O%6z}HALpN=vqT$W{hM9_}dPvG18*?CvLFnRS7vJlC1VKlkD?q`bxmdWt5=XL#=hI!_kPeMV|yTIXfPoniu7|$=_Axk%1mgaN3QVhN51UqQ?l-3ovt*YjmZ_UhTI0)!oUPnS=dC!F^yDqoo}JT5+7Pty*mdt7D|!nQ_;5CXyYf)Ekj@A~xEI*cY9MgU$uyvj^kiBSXQC(_<y%J(k#6eO`Of7WTc_*!N~%dvEe_2!TEw#$)Q!XLvt{vzzU@Zy9O**w;IWeeiSlE!>arNHu##s)e^)?g{yF_$T9QaC_^)t=v+XY)3`rCpHHod%MQoc<4&g-sG8=>7Ug2$z10rbCW(d$ULdnocD3&yjwde@#EoaGl{l7sq!czaYUT4y}KLFT|07!Er$S-Jh!KhJIr|w38z;$_eWKd*^j<hmFQs;oJbB@n}@$j8xs4O_W1gSEWG2W@^+r?aU2c5<7o1c@PVHPE9GEYvuAdwjRnzl8jTSE+J9R+iDxX!+}Xj4>IQlS;TW)$zr;ohln_mmq41_Sc(VR)cwnIeYN|t`$xag}CQp&zkr0TMlh}6CzwPFZQo0mr)T7MCDB81pw@!KlCU12&v04B=ZSYLjK$|t?`m*rC7Q`G@SZ`Qevxd>xS%bBb%|$0!c-|nzj8<k?F5$F|!$em)q6Jp`GH9szu@dRPn<S7dRArOr#Z6x5BzxHl6xfDxGe$3gKI^4OA1E=0{QB-rD`KL&_Cly@kL$kM`y}$<;D9%Zv4?cAAJS%{7<;xqu_6d|o#vP8luusd`Ch6`b+B!>N&8x5cu!{21C%Ljqo=TaaSH3mGkVP}pLuTCJ+m8)x1D)OAdvKSU2ilz9&Qsy+V3e{Oj_?PMSm7u;x93K2CMn$2dk&c^+^~qjGgQ-R_<umMI}K+Z86v^w%ALqKd0J@)SI*M*C{?klc(>M?u%+lwpcQ=M~8$ODIHqEazDLebd@&ST7UD<jadW$iRAS||K<JV;=2+*Tkam<=D>lQn~yRc4C<K{XJlHeJHU9-NnR7fRa(^6?G^fAkP0oHyy!0Q>Nx;~alI)so~g>P_#+?39C%@1Q2(@nhs)Xb8#Z<f?u0oxg{^yroUAfKnT|Jm1zPnMFjRsEA5ETn1fY`OvbUho6`8-z!Yc=OJ`;jkf{&Ls3LQN0peK5!AGI|PB44Z^ga+|_L=Q1Rrp6^l4_ul6!O}C{;Z@e$SIu_#Zxs52<^oLH+rQOQi#!q_(MSL}HPvx!4~xh4z#rQKpRpITcA=cq)6p{->mrVVL;x8B1=fU_SQBPG{1$~=qKS2hrn5oQ)!jAu-bbK&7m4m&<YW3P5gZ*syt95xe<ctSoUakliv(dRgUCS-6@$lU`7nM^&DvRcW5WY6d38z6_S{mD)L?l^nVFJ8bDYA?amv~pN1nqDb`Cr31qPlB8Q#i6)dsyj@@{08to~uuu9(Q+<j5Cw(Z}O^IYJ#H#Y1M8#;YW6D(Fpf=OQK65pAF_Xd*3Ab1`JvBQRt#s~*mN_3)!=@*^&p!L**4Ml)3!&D0jrOx+fi!uOIASrh5VnzR^M^JH^Zg;O$lv~lFo#+e>YeqEm4{uG|xqV>J1y+&&THu@qvpGNMZ?jsIgxRbhM(lz2?D95cMwZJnb73*z94q9yisZPG!UL$-FotCQ(K9oN4lf7&&fepS19a>iYIvZ~c9v<)VbbFWObK>NU$gZJf;iWOqG^sjb@EVT6-r6FazR1DPu7V?Q0GW}gdq45lnQfOgaV!lUKX~Gq;PEFqHG6T0yBKww_3yLMa@TINmGL=|7L*t~L5a!k4H!>;-oqwqYvBlPEU_8zY8&E&ctncEuJ*M<GBr@TEg})wGgG7S=e~yT<n2WeXal>%CMAUs`_bc&K9vPb3mjl*0<JC)p?-h(=H2^GU*WI6{qQT%n!{SGUsMmIgJ|4ZSpP3A_U4M`%~bElgO?wkGOqwb0-_2zQ7&I$#=*84KpDtxF8~L!J8BOK`=%?LSV4Z5K9?_B3!baA>SD42iWJra6e-dI3e83GvU1<g%I$#iDq@1@5d)+hUEO+zw)3RNLAQ@np!<G4xxs_^r14&B<>?%E^GU-RgZp6CcZemP9?A29tts-V?1W^{(YZLX;yJU5=dz}FuB_s@vx?`jW_xf*pQ9t|QEq81#Ma$99NL&2LkjCj)62sm2R^<m;(J)cHFZPb)eVg|qEB9R9C_7oK1^+JJd^o!I7fhqf`_s^_<5*fjvxJV{J8HNp9B7!Yz$jGi%Lx^&3EavwQTay9?71}nK1|0K(9IwA#!4yPHLRIF(=3&r{cGl?a|%Up9BmEg?pvagTh9S{Dvd86&Nf^cYok#lF{~+8Ssebg8e9{(7~#(A-Jgac65+|6vJEQU&$a2Gp|h~t29+xgylxkS6$R+BQSQ6?z{McudfXBqsCE>CPzK&Z<8*bn+cg97IuQT2%2tdy9SWo6E{+TvO=M|A=#95B2KFE((`6~Qs0f~?%;e4kAnOwa!jK)3^J1J>_~Dki8lsTPZa5qcuY3*pSr!`j&smK8_8V=oam^Nu<_@YXw&9T>hg&8ZZ>VjaUJO)Y4Qw79pj_wAR5Z(YZGZ0JAa9TcV-8=y>o-<szVqc4`(YooNa5~?D1@a)?4%f(vo#Gd1Rrg-__^qE|1{rUZOs!u~&`O83tNsxER{<U@Co9fSG6kX7Dku1J1lQ4ko}*;j}g^P|q2fZdO|#xbcm2T2%-HshBypm=-bGMsZW?0{P2hu?^;CQWWM(@4RDtIvnH32^^Bh+?lvtXajDdp}cBj36jqYwO=v8U*fH;KwPf5cQHpSkMWg<xYHx=ntplLUg}3`XuPH@u~4p%9%b5k6cgo&$ykytV<CDolc(WL<7wS_(ahlU3WD_X%xmt{v{uPR+GiT!AUY~%dh)WjKr7f1%?QnljL_mCay3^Zu&n5#=U;)Df9=mbC5z=u3j3O87zJ`eJ8j~eHp7#65_i;fx9yK1p2XerBo0j6@98sgF`q>Z{i`%YrO~*@>7a4T$e-@5F_kNn6^4V4NEv)H7s38?{t^c-7mT#>PF5K5{F4A4vA0*C@~i-e*8@-bh_)~gmS<_~5&*7F!1+WsYtob+$y9p8BaryAA3d>t^n3{LWLfJG9jO%_b=C3u4p{A!ec|U0kyP`ApN~6fs}>v|O?wz**4bXyWFBqB7~feD%V0$;la-Og$m&R<N69HeShAm|l38cVYM8j5G~mcfeA(7twsp$3uH}~(-suh)dQD%(V)Rja+18)VwtlmC??tj8ERJxsyk7S3hp~qfX?1r96Nj73%@y>G<bxYE{pU^Hmm~|iO%5r~yL|>g1`m)1BL@2~l8RE^oi6JZinjzFXlG?xB>|VPlTj=`m0MfE=1d;#9(`!{!kee-Zqt38cRk#^YXp@I7KzC--S>=>GMFrYJjlkHA0#eD;mRp?5${AT!Al1oR<u2=hrJO~?L;ZW#7O_%U0XBk0UHdol{Z$b9&YZiy|8e#tTfuiOq#KTZCSq^C*QYAE8eF}d!GvJNNThrsY~}lcRc%swx-(xBYniRt$u>@J(c@Mge@1IvLuWD<y&DHV^1?!5k-Ds75O~JVz_|!JJKa!S$+0!iOc<D@vwA%IItTC{mXQe0FbdPYl{NdP}?><qc3XZnE{+*4N&#Uqe&4Tq(~3lufAxKd+@c-!l8J0nXJ&)rtSRP93hOrK{g1MWWONERmzACjA*o=pwoha;Ry}NPmeuVQ>?>bkBJX^j4NVC(CyPb`tety`V%Co%Y!!ALtmj2A37=X3>~H3pS*o8yLV4Cd~L|siXZ$BcJ4ntV}DU8oXA&FbV*%Yj#*@gnxE8Pp0UsoWK7%Erl5lz(@u6wE7ggPiD@)uvko?Pr7b_*W7(MwLw$;iJjTTK0kpI7QdyZ1Q39e8ENsWLu?^F{rtzC}yEV}5RzAokW<CX|^3MCtTj;0VrQfmwrKdKVXGijP2m4M`KJ?_}fWenylX+A7e!@fLJQL*%@4B)n7Qx>}Fbhwu;-OWDy^J8yYu2*7qf)_PEsK6@S@c-T=w$BbN#<4t8O6czu5OMu&l&G5B5Bfuq_8;3i4Gi=3>pu7E@k9N$Es~x*6uB%xYHWxG?Fk31%Equj4eRKp=d&3g(d_?t<Y?Wh9;+jNyjO=la5p3FHv#4EKSAp8b0Gz;qJ;=dU_(Qf<MwK(qRah1|XJ2L3Q=mkO6l!g^tTd&R$Op=9Q!rC_eVV2lYiqP@inuu)zkIzr?~*1DXeH(EVV8!C&I!MX#5o<PGfX`DJGhTurMCg~Q^sJMwn%%=^Bp!}l#WT|Y1S#kYUY!Hyt>IaF}V@lYKOdjbWJjTZmJwMl$TOA^;iJI5>S9B;Pp-t;$N25`E&E0@8dUM;=M+mC48hTN>M-8<SYAi~m<`9_)6c<mnG>F@(jCw+;srDv~{$H(-2JH#upv}CZ#lDTN%-V>;=oNMGW03AUdJuwiSkAdiDBL&S7&tIFyLD|}fNMSB^6w*-~(B$b1XHO-axl<@6uke}dlPAVg?tx5)<!d@zNJ<f&mx^dw^$<Jl6I;#knjR;hqTjm17=MtRGQ}4@Y+tzPNrLR;ksle#4X?>Jyr!q&HT?}Qni;Pe(dC!xI>o)|5|%=9C92JaV3Iltozy`SFI2#TjBtn9*PvHB4n9{hc+xYX3@HBcQo`dJWhat!O~t*K7Tt@P2i@!&S0A}1W&q4mlh<DdSpX0nD4uYWCT4d0#3)>{c!&u6-!>g4&_wec<cE_Al4$z@D+Zodj)H{}{bdh_OWy&khzGg!7xf6qgQJazVR-D8&k=ZEKwu&YB7^~~wuFjcrUjgXe2N+hjv$GBp)lnb;%z4qy<brEhcJ>GIE~5EGy)xjnP{13K0cF@$mfZ?yeNvr;j|Y>0=qyLys{=q56*NMiptab)aCJZTPtKcI~*T$>u{A27wOhxvX#F?@KEKw_{|pq*Laz2XM$!SL9fQid^!Ig-uW+!5)i<<b|Ybqsp?~k4&Dwk9hylwYiV#Qa!51zk_dcJ5&=cXERR6wOey6|EZ20Emk2ll4PFq0n+gQ5!%CvVMDNduXITi(l@H32=@o%!bs(UdJHn{b*EehofH{`N=mF6eCYpJ)!5sj%cMX233^gAbbZG9mMbv(WEXZ&aYuk^fFhF4Nwh99-LKMG^Y<r(vas#IN0FF4u&bW8Vy^8Mc?idVS?=WrS29e1;(1FMHRE%hi3_g>2_*x?aZ;d=k)P15g5P^2x29N7D_+7V)vosh+9l@6^$h=O$!CfVL%~X-t>6n4(Qe{nAl{I~(+aeZ~DBUJsx=rJm(|8DL=OL`~Af$j1VBBcRaX&<%rISnmtLXW(D%lGlOE+dqEgsMc5Pf|9H+6dfDWzY`O9rI$+kh)Q|Csl;RR^TB?Zvc8+NVr=4U~5eU7#$^wm}Ak$7oew>}uzc2|SNLPHJ_at%?UJ#2ey;`@8CQ+@z^QG6FK-q&19YlxaPVd@u+cG!26w4Nd)XM2Lh*pvY_^Jg+puU67$dW7}>U!>T`pF(h#GaEy|lW0d(zT*VSKhwDu)Lc|jpojE0!9tm&rpXwST-9L|x{&{rw&m-MGcPX1AuWTM3M~xy14<79~osH&WTI3hg;>%!K(BM~<b{vZvcN}>hb8Nh(X1JKXyN>=f!Ag1wR=yy?O5;7dj&of{=adw!Pd*fO7Lgou!J2lKT%u?|$p(lopse`<s=ZvVoFX7z9<2I!((2<K)x&Ag8tACBnyb`D1p(dRvX;ZGqel?n;n{iog}fD1(ecD=FCl*7!j&1=B{o{cGHJ40aAcYus0|rpYKDT_=rlKD@+7r*@8pZf6KSJ|NE`h`T9*KP^7XBX^l1*H&v39f9e&EX!~tro9V&L#4}}<{FV5P5)dMF$attRwD<*7(E|hpu5HyRej!fL<j>PTs^$j|kHqaR2xQHQ6&l`9i8GF}rAT~N*v~;zu0)Rx&O9#6|QN>X`Dh}STDg1UuFhr*@J!41zb@B*5%ore90+Lv~cwV$`XODeb@uhd#mp)h<zx>X`K+<uY$afQQW_2Zh^7N6p=#_~)QY6zzCWJx)W<Nz<S(G?s(UvX?K?1xc{1mnaqI<~GdVX9S=y7p82Br%aXNBjvHU6#{o*awmj-`;H9RY=Q>=x(y;Pee6Ja#v~hoaV&Mbw$?Qcm8qajX&=Vs2hG8(&z87nVX9p>H)#>u&kKiBD<O!!D*f>>>p|>>@fmj6RmdOB!I`8sY2{;QZsTZ(v2;4Unxeyb;;9wA15`{r(5fx{!4MmDK^XwU{}&u`t=b!g9=<!_QNByNnA>5$r{079fOW0r8123`Rbvo`*y%AWWdJ8j;FsMCfdbLC@9$O^Aq#f{^49gk)dvUFC!C8czTjwA)=fGu%85<SDFfQJ0iPUQ&u!)(DkD+&6c(ABUq*SS8g~uvjx3NcS>q-3##}7d|vbC!A!SZ~|aT2uGquHyJLD;bnRIc|)P|icC}CDxL1#UCHB<M?wS-5(3~zoZF_ey#O-BE`r=6UphMY&9}+wuoVwl?U>gF;c1PO97zh0Vx%3sAvV~CSi*YSdF$;kKB@8^+P2K(0f0d=syM-D|NW2}dCfq}ryrr|fK)oups#P<kD;Fz$8i)xe+^rKx_PR@%+u_AT5ARcrP_+|b~NEh&j-!^e9*#Yz*L$i)oDoSSd@B9S0Kg}v-G8NcnF<?r)Exk&Ag}B;o=S`wA!^U3Mv}kejOeH)5L*FpZ>y+-~EVG#DUE;iKKw(D^XP#d8Uo_JoV>o%PI!OLK_(Ct}%n)AI7sUkZcn1?o52HNq#XSUd#xt+no7sb2i+2jrR$59*!1wgrmLm9rs2*H0(qM5)0+Nd-FmB6E7@@Yt#sWcjAISxESV7gnmG|ZnBYY(muXbormznsdjVObuU3!tGz(FI~w0E?!ExIX_r5WuH>}%88nG{z<5B4n%`&@b$3{-0n+~Yb_n(Yh@rk4o*&-gLmZe@djYw{wIG1*!PQNB(fI}kpm^e8BGU5>ZSt^N!pX*sU+7#EKx?269JU1jo{SS%88Ug0g{Cv8cr420){rq6lP%W?lEo^PqHNzIKt=$UXfhoRmyCLWw-+f8`0WJ{jurFM6bCLz&K5`r1b%ygxLXJB_?aG@6TpBve>y9V%e*$IT?BVOU33D7G1k)-9wI!!X_`;$h@gNN*>!w|u=}h1|L1Dr3T{9U?EwJhp_;e?+b8lc`?RBACGZ@P0St>|xy#Nb$Y?KuAH4U)FBAu^B!X#1+agF)>I!KmJ;_+v6W&$);a!!##CD9PA)-0++bTtJTAF!<?Me!3hecc4YtHUeAW2pDxhHR>2sZbK5-AowAH-2JceZBkKtp5j0kPB8Y8tdTNZ@%jusmGwlU~s!ujrCPqf6vk9I4)w>7)29iqm;z-uWe~ZoWJlB%F29775-H=q1Z7n7DEhU|ZJ;eFe)-d4W`(0Hoqk!e~}aM?_$=mk^lfPTpVGHBMiA%2%3&lG!bsSGKUhz{aFli3j@>AA8-w1M0hh%~kfgoc1%ww+M8NFS3d<9>Dq#fUOI66y!BW!9|^xX++~{RAF80KXu#4YwBnq|1W}cfiWwJm_0cnMzT9$q|jpfO80`g1MWTCZ12hUs`&JU>_|K0LltE~f9A&-%EwHHZvYd*+z7FvpfDQEv=}^{0#IFVJ%kF6UaQNfldUBNgkXD-SgFt5GQFcmw!Z4?)!T=>yt~m3-NA$Z0uTO6e5zmZr217n)elu+Y1i28Z{mE0Fzp3&>R>~K=dUOk1y&GAlDL8%h>Pff<UtRVMYn9-jU^roCu(|3rc0ysE^5H{a0h%(`ugOSH_h#CxLja+5uGkb<NNU9^6Se1i9A*#daxSNkJX4bfL_TY4mpq@k-2XXKe6z3`@}*|_X3#8$lbvrcPB5djGl0(<PUes{3RAgK2dD+pn4w7VY#|UAQ17>*ZA)Jr?2tX-+uVjoByag;XW(4)pw&~JptP~Kv@Nl=`kGxw=THp5th5h=DC4*)isnNqYt2kq|>vTAXCx{UNDGdtQPil(b(5TXN4Y<CW?dyf>C#)rC)hLU$fn`Tc0#&1_|QZHIr{BPD<oCDe1*Y`HDFy4K3%kB_)LWQfkCCdx6*}?7Zk@*v&f%Hc`=|$M&Lg`^K|ES!CU1XQ?W~(W;+zuibE;ZZA^Yr`rp}jhg9cKrE~RFAjSJ97UxF{erz|%v*u)2gNl3`67h2yRu3h{?6daQk5IkfpsZGK1N56tZaB>rT%>1trhN&co^0^J-J7x*&Pwx10+|#ahH__wE&<3JXUiJI<R%GIHEO^ZL~Kh{fmj5i_ih=7Q?P_tb3b|;HPLfBS=`<>=h_GB?DvbL0{nHVS+$X3k67=JRs4*YEjWM5#ZIFS8hNs4l8R>ltd{w7(6N2i&oAGRF+ZKpP+o07l7`v$|nq{6>MG=;dIq7SJ{S0QE?n`C60rj8^i^=0o~{tC_Ou!DY?YoH#_1qiaSoD?iKfe%A%*e+%Ql;0Qf`$;PaxSr5q#oj-E+{0()2&#N;(W41kWY@EH&`X4qI36Q6<6Tq4iN%=Qu&_fve{RsI?q?S-AJ7dC}m_1UOR?5GHw2Gs_b$0~R-*CU>}ezijqe~sA}UAP~B@SaiLsN;;t@&?uQa#@_#P!kdCcR;GK;Ye1R{$QoR2P;KaW+Z|>0%be_9pIullO2zZ)GK1_8XcjG@z#k?F96K(02o)jUp)1G_Du+uIA-vjnLT%AUbr(ee`i+H`H^Ug&ezMGIbQITY0ZD7SvB>zY^dzZ0;s$xq1licQ}Y0^ZDc-8dgU~|^hd`9*Id09_Dik_9x>7Fl555*;pr<#c#1}#S=|xkG;kH{BHw1R+g%NQcrj`qMh%)bUNAv9;y*%W6oij9u*Z*tgTT4eSR|$vJbpx<_-Dzd+w?PIIf9&wQev`$5_3a#vMbdo^Y({<9D)mfjg=Qc(S#XH^>YVUjPyk|nlsaFMGhXFG?4s-?FHi2h`eMdd4xQG`bP;R+g`x(K{7uiN%)XtPl1h*g?$K~3m+VJFn0lSTg4r<H36TUVW}M5lN>S@l0zIqnP4-2O}Gb!3eJxi+mv<n79Snd50dG`pH_lRqtW=wJjbE%9EWBvAv*YRp@Sd!5?W+UB$_p$)ZA%J3KYqQc!h~gRM^xZsv(%M82DU3ByTG5mzZg`%~&yrBSIi8x?o3^jsoXuYZ!yEoAD{*JB16jOZ+8fnpjq8Vp&@xmUR~Xn*s~}m4Oa}E>MRf@N_F&`tq&PY10yKKZ?O#LWG_c@562Kc}$*%TjF!-8u)sBg&iSfu&i5YtZt>#Vvy<LsmY~o=J9B0QEN`uywOwh#)X<U@-?qPJeRGeY0YZ-_`IG5+BBdp#`NUc1%FIk<ohfR4^y$17?!>5MOfnwyT<PGSxwr*l!C)&m7?Egl@foA`4#5$#9>b82qOl2Jz;R@Tnj!eAi5Ke=(aL=ChfgQz`*3oN`Pt{eMc604F@M`HMtB(fHDQmSa4K6L?r`?!qhk?Bm+u(j|4u>DI!uC{XK$!Ni(CB0pBREY$pzrn--&*3hgg$w7<A7PE^KP*DL|a0x$u{U_yOO=}-+rSR)OiNelWTE$F9F-;rj0`?8(dUAlN+woY18@gCzhj%P)eE__%C=ZQKtG6o({8Tle5ds11;LMm(BF`%b=@~HYk9#u!r4TRz+Tc?1cSF@GITLB4YR>=X;j3N-y#kw$}C+f^$fOj1%9f4(Ps2XD3z*<C$wvSiT6b}9mH26O*g8!2(3pec;7$I}|!lEJ%t$f&gsl@jQL5zK;-I>#-&kz(#4O)|EZlhG-b|zT@L*;ju=2LFkyHt+%ji$o2x)7Fx=U>HOFM&lkr;8Mj_VxlYCP@36L=9wH36msh)wWQpHog?8z8<$C`YyCrWY{b8HuClwh;M_LS$Lzmq@|f?j@tGTg610+Xugr9`OY;(Iy@<zG%(wzW#36)l$W~W=Utl2_r#N(wv{-|&vJNHqLEdy7!hh#gJ{at_BO16K>e&YXmVrHPFa4MqAN*E?rA@~^Ez>oIyL`rxZ@8U0gZw6K*;G0i4-G84`&V5?~S#*&aV@ggw7_B83kakCJv;1%_vR8D!A;<iLZ+iI>zUc804xd@wlb@!Y$nzw}gtjhHWx8Z!gH39uwc}FP=Px>dTnuyo-Arf|0#GtGsg9WLQ#L!7_uBOP%CgaFX+7r=aqe*m!~hpX`!?BYP&rHRYYW%~h;wIw*-Plj9}c;En2m9Jy`Lm)n+keo)~jKFyQc*6Dc<GFdXP;;<Y3CjM+Z4XuJ!T4*9P>=kJDwAtfSIqf;J-BWG8lO0jW$oL6*(qorM%dFPZ7SfvfsW`$?E3JL%j(F99hox%05G*P+&{$?9+Za@)=yAwIy7A=>-Y?u(G5YvZ#FCvNwt_1{-QeAx8t#TUGLkZ7R$SrdPzA3WFe`YWMWoZARZVd}N?d~F&HNC)&<^NkuRzh7$)0JBBOKaaama@QCKP#x^fHhouWa5$I!n>Ybm3d7K9y4CRZ5LlDd~w}6;BMid^0!x68mo4x9;P<b@dP?K7$n(J%ESRi_h&f!k6A?mw#tXDRe}ed~`|<5*(;7jET0w6xs??9sUuAO=W5#jbMv33<k{AB?iBNF+NP!E7PLtxKuU35kwK+wvM^*ozsX4Sin9nFr_*k+@00{jy2Xc4Akl#+P3nj>K;ek;`<>b$NS-d7$FDx{+d0W+9;0rq1N;S*904mK@bhnzC?rSF$*@{@Hae$KZhqPdOTSVi26VqwTtmMnWfyI)5PgOhsfr_jw^uh>>3BmqkCW;gAcq3p1>Q3;-MB*hcwYVQMrX~q6NK0I(Kxx&|`$4zG<`V_8>BzG$Tv%7+LzBLxe@2-z`|#vJG@DdOC#-)jdh}gHNL$_<SFZ6_6E<$J#~ioE_7leYm|s--nQt56}#HVrD?}gqmi9#KnLr!|YKRDvzc3B?P!6_$7y7LW7OqG|wiBDK4&j+rbMr25!f}ta8&~=kv(A(_`kas9vv1QyGpD=|xX?dR(M5L|(5Kd4pLn?j6VYb9nMz=3(NyK+5RUBoW~jzf}xH;<F?YUK*la#l^6rIQHv@-zFboE`>aJeCe>LCws<vDCF&IdN!@$*~aKBI`lRH{7FHWM5ARd@*_R-cdWdrFQ3S}VU-jWdv$nF+uGeeB$<b6n35e9Y-s1VwE-9(WqNh5-JIH)Y4&EOpPUVLH}kWsxtq#d)xkR+qy4CP*@43EJBzp*PYZOA>*b^UWn&XWmFBgHN^wj$+S*X1@Au6pC$Zw-_tmx2TbEj+k;j+CT?hSBdK@Tv@$AsE7rJ-T9U(M>@7n}VD$JfdrNno~6?yriHj>eKZ_?Hb-p?95mRtS_-KFP{YECM&1fuVEWvT$WuFZmkx?GVAPmicMcyya(jj}0=MTwK^PyZiNS~`#')))

_TASK_ACTIONS=json.loads(zlib.decompress(base64.b85decode('c-rk<O^+N`a{MoIo`X0&9Lc^>RIfxVr4jhCjkQ1s0=$L+V||c)GyLDp<xE#sS4Kue=6gMq)(Z$wqo-N*zF%f!WaLl(bM<e({QB3w{Cf4zKVAL!;_ch357$@!{>y*<>wkUx;^W7^{_^X8{N=wte*Wp|>-T^D`Na>fzJKxh>iX*C{o(5R*@x?guYY`V|IPcC?>>Hi_-_B=<Nu!@|FZmpx8LpeKd$~s;SV4F_xh}ruU`J~{g10QB<+2>fBpK@qEFBN?$w+9mH3c!^WpECrhNVW)$4D5{y1#!-hcYnOG{R*T=$QEd3u@kJKo#vpuK+aa*xLBr>h_C-@N<oQ`ga_!~X5N^;dF?;d;m?@$m<{vnDMs-M;-gj(O5DuNg02Z09XL{y22&xi~e4{53Y{?SB8w$KQUxe|`VM)%A@(T#w_hUSHt7kG(<T_wYftX!G7b{O!+Y?~U(>BL>Ithj+_+&f2kg<Nn3Ar*H4yhgG><&UicyFW&9nkX~n_eS8nxB%7`jHjDA*INqljeCW*jEwL%bZyugspYP*XpD(nuznj;cx3W3-ajBo4N#AEK_2s~k?_JI7%(3_9KE5No-X8h$lln#<gs11BaoDc;@^Ei$4c@nS4UCR9c|V!$Fx(T~8=q}%Fl*qQj$8ZdbPR(R>zAzl`RR2JzgmAFvuccFd|vnf=FNZZsS~G9+duZ6EI*LPzPx|^djIm>&wtpzdH3q|tAF`4x`|PIG;{y<Ut%Jz9)m4KIxG3z3D2X=%W})S)aTp+Dw&JU^#~i1e|>H}v9%&+<Fo`HZ6;_{=jTM-NWV$m|IM5GA3uF~yuxtzz4`Yh0<5xRz+f-dN9@Dk&1_t}OJNh11-UGWYE#aQxr#Blyz(>-50j`YM#EfN7D0SlJjzDL8d!_rtxJRAG>{GGbj&}ax27CDs{F?u?^5)*l@;MPGu%+j@fmq8wF2so8@WIK@wDIF)8b(@U=uZgLTH!RM%1<WsdPdy+$^z3eB-QWfdN!x`M`V$i3c?;uEj_(fXv{nKK^5FeVMZehu65+%r|NWCq8-^o8^OrtH|dvK+=LM&W9*L=k=WkAof$!rt}nSIIpX^@eqb;G@7EC%VWNK@#asRhV!Qb6yfyO<&~-N`S#tL7l*I+Z{Gabo9}fefb$*!kJSsBtpNQ8FgR$-X0U5(1K{AtR{#?~`WKrwoW>2FJIk|Amhg6B4HI}h*5W<OK^G^qjw{E}JNeC_W5jN0qHNitP55ib_Hxim4RuiTtF#h6KMr<&-+wt|^F`y}|FMmC`sxXdyyfl8$a`v&?wM(?<a`F$BxGrr7SuC<`ht5aT7!IDWmmX<({e{GAHc;3&Xd$WG<wIpk+681-B})enziM4e7Fb5g9)hwEyq*q*O%l&Qw)3=EIP2lmX#3hfacj1(Vr7`9GY&Spwv23wg(FN1w$&%+>nvV24irTL6{aidUAh|xewkduW@LEo*oHp`;BomV1=GN9{qN0^AMBN@k*oZ<aB5(5K6Fk%{iK3rLlqdU08ol2K{+hRV5@+HW`!f;efR>$)sfMdn)7d5@seqsw@WPIF<;mz-&O~AdGB!9edJ&8|CWW4n)h!WS6^P**eIKg*cv`7on%Hb;d!+6MPa-sDdAcOmtwsfZ^L*meY<X6Uqcwd5SZ4$R@NI;KW#S3(ip7sw4HxT;fZ&W2D`5sT_X|b|sA@;nh&V0yocruDA5Apbbm-1IwQ(9w?zO0)TFrq<A(+m$V7kg<}D1hB>T0->MzK9)AnZf3m>##n8?s?nw>9c~<N&&yZeOe_zHb2r;#7RGtvTa8O8kER0&s1x{Ip*&ozIQC_uaDuC31aI#SQv&GkR1M-9q2~yrpUoBG&%!(F1%a_b*G=R-M767M)(Xv&M3o_MK1cw4N9}B*ajTky?RAvuJ7bz|?F#aq&-ho=9F%^xwXi;Wd+Ya9~T3P8bzX3SA&&s{2VZeLmx@drq0H>gD6#@JzsRN+)ks`YRjOU@#c>>lobjXI#SURi(`}Qs3w8a1vAGEn8{i1TT<D8l~AFOD|-ZFw11vAg}u8~5{f{w}x_f}M)LD66hpj0r(z<bu6C^qQiW!>L@{NLU2O8mHyzqzUe+reeE^o8;fwg|4%x<tnTo{8PR6+J0n0D`L{4hbSfZk&X2EIDI!f%U(<s^+I9H%0EXH77b)6uV;BT!ge3(2N4ygT7ima%ooIvedu5zkj=D{F~(m+`QTb(64PnKiuBkRIifZ9U+BfA)N?5FE&CAo6!XxQ8GQ74eHFtqyq-$1a4E7;$*8h7mXK@Asb489GLHiE&1|(dozOLF@6B+SB_5KZ9Q%-xbwiJC&xS_dmzqgWo3d;NZe0MA_GK;fb+dxjhvlcB*abGSuA;RY3$juqqqVzaS%Jd!fRw5Em6V4k~AE=lxwfn-PqdV!W`((Dy*mvGhI_^&VVg~0Fq0ta0+E`izENR(!uT4hz_<5!PFKyxe_;R-SSg;pnttN%--~5mr&wRWO?Wbx?~$en#Fc#9nGFnNYKkb*}TofU(krhhF^;J7f~AI-aU~<O78>Mh7qO6BWJa+CRAhr7v7X;YD(Q25Ommq)+(exMbzNMw=qX<oBb%L)z#eEsG*`Iwt#`{EWQ*O12zj-sH;O`C~62qLrXDXh$Vn7z~6a<n^AR=81sq}hT+k1o1M~R@Y-oIt3(ixM~@&C4R&efiiiUWNL8raHZ_!M#F(U!5Q&VhH;v>@R(JHWoTPM%AVS6;<oX-Is!}``9Y*_<wpZyF;1Y{V28~}PcTk%?=n31GbRp49-LnY7q;_H<<C8^J=^2AYr^RSSht&;cv!cE-FkU<L3kyMrmH_q+1z3AFOSGqBX8eYvG6efIT>&eZY~C2eN$6y=4W&DkTpSQ7mIHG;Eo|-6MNi}ESRK0rG~$jE*&E-#di}@809i{}vJm8^0>Ts$^EE2(>M=VV8HZ{x^6JqfT%uhoO#fSL`sXG+2D4~Niy1gZ4i_`}S*C<$E({GY!Udv<MZ_DKHk2P0WSIVHYn~_+7OEM?mAgvVhJ=<3)myf*jIzKpb;&@)RYZ$`9xDk#PwWSC3ep(9&CQ8^-Maf|qRR0x6_WO=M?{_qZ1pA}zy!F_nw+PC?q}m7V1<Ut=)yG01VC_Ww17awR>%Unw$eMwL7SF96%`PUawBmaZI&DqYp5=!>+!J8wyw)5NTv%MBukJKE|^f0fmI_>=W^~T>+`F39Qn2?Q^!N6kuH)j{V+m9&q^hDUCK{_SsQ@lZX<*aEOSDRP+2jPN1hq5EMQ2pk46^`ksAOxChozaW3}B=1y$Jz$s!Wpqr#TC@Xs_dEJ-@!vrS|P)5EYNjtCOY0;ogK9WcaTI2##ZzX3RgrxT>m%uX92epD8M8)x<R0LpPaP^05a(}@OxNdb*9$2@<1FS}tmext*VF&o8G_qfRq?DAVOPbC}&(A|OGi)3=LnE*p>N2yiko;yGU9^E)gkpXE3BnLU=Hv^7+z5^lv6L2H$6N8x}x-Of!l3gJ=$hZ+I=3XI^r|$kXbU0V^kjXyzIGF(Ck?#WpQ{*0O?>Nd;0Uf4H$8jf&X+g;|INZZg(i5MD-PWe6<;!9P{E9Nok@J*A;i1IYD(0G_Wr|7wP;OJw0W6u{Ad(b_F!4NN5*cV4$dZbUDv$M~zmhYSvF>w8<QWAMJ$+SCBolm>CErW{sX%h1mwHQ&M5%g3{4UTU=Kj%xkV@IjS(eciOqHA+PTBk_o`l(dddum)iR`x*PP!(GM^^;m^sy>NkR>J1TeVqfnnwcD+#dR?Zm|W*KH^Qz|3R}>TYp^4K%F>ywSjzdaR{X%EOcA@66JbV@e>ZDJiDnFtORA?cN<4p076mL1CQKjVhzyZ2|+Q91o|Hs3OfUHl1H9@(t%J5_!V1FrBe{&N5IWm|1i_YytWiVG?q%BFg1|U!zEN`n6sMHt2!=`hm`HR!WQHp87zVnS35X!*Z%;-Yq&71+4gAjc^7liq<EJ^w|D#RW*AR^nE+Niz$;ZJqr?K^CO#I~{d9?K*OT^f(FuTZdOV<UmrMv0<fXmm`$R4%%DE?nzT=sceHb9g7dh%!LAoTO#Nv3_pjz$%jlLngfF=kLJZK)lfjMJvwJ_=;!#_L#a~j)<9q-JBK`U=FGPR_PI3}IM7|<9Jq3?#(NyalSA46H$@dCnpb$5X1wtX}!+e9%cu|^SZ?$LE<qcur)P8g(+KKjILgF-H$SS}JAX7z5_I&UNr64*zp<XahKmw|ru7_OG><4=qgOLGJpg-c*EIiZX&m4f_NQz4Mu#UT)&LOTY0)L0p}f*7rm3pn#e_BEm+!1%DUW+0)o!V<CSDl&A0xrQap{&+7HYqh)N33+y)L6!Ni9B86Y$RYR3@m(TgDG`@pYJ-JnCBOQo*twvHK~4`5yd{o<>qQBmIhAzFD!_Q2L^F^V$IXt5Fo9I&)@9|1L`x$a2lz~aK?5Ud>x(`jvo@7$4Z>~Ce}TQ-^zzCW3`ZADt3Xy^1+NE`)p|>Bu5QVLbj6-cal}HL7(VBQWgrMM?u1*IKppF@te=pi&Gz;h7-dqLD%nCT?CyLs<z9#$7ogx|3xw5Fp2+sFlV~W%f@XfF&fx$INe_9{F1+9w8E6`PMhuhH7`@x(rF=1B1iNKDBHXlfD$jbVV$3IC_3V*F%DiM?8PbhKXIfGkP&%s;Wsyu-=I1vG7HLoa+2_d@k@*zXmpdt#D;)bXro+_I1qG@p@Gqj2pGTj-9JhKNLqbvjLV#$R2xI^Q{(jz%ES_;&69DWAlF+#GVPC6<TmqO2<%n4xj68{Ah<3DYmhyj?I7nk8)mkq2M8Z{KXW311LuSTDC%_h2B?3mo&EUe``3+vE-$Is2bdzg5^PFbO3Yva3SRI0qO=xZa*Mn;;0ucl&p0LSdJR6RfzbgVx=J@i_!i2F#6fE@-t=e$LzS%11khAHZW)?v*BZy)_NR4-#$=g#sDAt~_Pc$x#Kx%l^A{6IK37*D&(Fb;Jqo-VYtU-A_wKPl~M?ufaVH_8#%}A?{-_A9T0I=>^=@Oi&j0RjK(QVDY28?l9*HoYi%&Bp_GJ?dE5Fs{Zsb(MkCu)_Dm1|&GR$dc0Ac#^EA?6Y4XqG7Gk2nY8{9As3LHH2wzy0>ngggJDz>S^=kR*rf%>~&JWfbL3!X(VYe!S^#b^8f1Dzf$fXG#<9iyG{=b2Zqx$VWUO{f1ZA5>0+o^svl;nQD6x++eVN^rGUWDbJHU(C0^$nwWshJkCsv^NW)TsT^HcKb^v1=a`W`QT*v?oNhv+;`9&K7NlziT1US82f_y^+j6}yB>4yWDZn#Pt>m}@z2<8G2DG!4;U*|jmBW;r0gyI@BW1Cww%-1k3Vu&2(2hRSx;#cOJ)MMs8_Ny}*cbo~S6iMw5pBp%Y?OQ{*1~3ITLJ*HRtr-ar^Iv5kgr5oS!zzFcnLgE686Gq3fCbOmPp^}>6VZzvo7<e!--&xRcCZpVT0{IN~7?oC_EH1rSc@<NmsMsd7>?Ke_dG(FK)s1J;4@m)0ln+(96t@#wf9AB`4(#eg2_Y7-fa$UzAgE)S_ClzDB4OyY!c=6kbSu5b6?VBXpbOP<)kq|EwtrNwO;ZSjZ(q&TuXq8aWl+am*W=T43|WY0hs=u!B?;0sID^UTLc<`HG*9_rb25ycWC*9KNR|1^j9_UZoH<*Cy9*nB_wDEpwamx`Dk6Nt?SujpkZ>1JdP`U&MVmhd(jb@`+Z3A`4SHXjt8y)WyJ*Iow=HEbo+w6hw=L9A=Dx)7a|ulw@2+W44*WYK50m?<_bQsXRrDarjVkAxUwzo*M@>hgzg~2&PMcCC|h6gwug`1H2g7rXYG15<VwclT^S_LT81feUxz+uRSj2R5f&Gn2JmYrNGKy=3^z+P9h<qM2dAX)Ln6PM(wvHQ~5#RRQTMk_q%Pl{I(x1pX=fl#1hNF@SS#sgFox|yfM2kdkmbDb>u5^iFfTXqfW>jnnB9i%)%XpI(0#Kz>KlW<BcgdUi?H<j)Q75ETHX67Ys4?RhM|&h?d!fhV*=<L&P+Fg#ceEqLt<BDP|;gnn)-ZsvTd?SBH#?jNaYS)M==mfmKQ`e=i*4m?5{OLj{ciyR5?snlOf%OE5lJY%$^~*oGyu0{Jn9$2_?p9|4U37Sp0jQrDuR%8LO4DB+LAvS^7V;I2uV=gy=YOLtXK!7PX&d5a-2?nT&!Kt!v$V`({XQQ+i!$+n-ST<B9inf!)RNkf=f7YLu4>Ft)ze8$SE7TVA~Vv$*2Z^>%|U#Y+tY$n?XeBBdNkrvB#RZLJnw`l&X>S>bO?L^<t{me=(jZ7^!OU<H7geW_oqH2=dA9NYcESm_VcwcdaNCLAwNlwCNsZfzt5+5fOfaAeCa<lq&W-mdeDpP}Y@e$<l+LHF2fF(zQsbnv0Yc40bo0FkX7pL=1!7M55+$Wr>`tS1+#1-az-uf6ddHlh&5iT=8O9v5Q{Xzixx?SIjvTanqnLq{UkA1AART>hXNK+(Yt6;qV3s<V?<bjmIGO2<=G6=haeJd6{xc2<ij%*?2Xp~ZtVeWlK9`NH2K76CMOhZRZdGqs1KETT)DZ!a%(l#_T8r4?kkTZlXl*t-mH9!l>?=AX?l{YPSQIeldN>9P_oOmu`OTnX@EHYI8og9nj-HK(i4}0_4g@<4p<EXO*r9%nG9+CBH&eK;F!AV9RGNBKt`CZ}CWGW4|?dd>zJWTAAXKO$`GA&k0S>eQ%Xzt|Hlc`#zDrbiIE^y$R*-S9<Bm^?|?gBs;x+Pbu7CInBnL57w{Gbiy<0?QNTGKHC0w;ha@Ot9qlcw>~5=a*Ysm?OFZ+;8Rpxp#!(E69v`WBVEmrF=$uoI%G=rBO{8CTS3@@aT+tI_OFTW6zKJ9~6e3Yad@+d%i1;iTq6UgA~xilwpTR)Idj?w{ap0>GQB2%T-<Nq~3h`=g9Cnds5c4e)YI>{Eg`T#W3kl^k#SK9Vp#!0Kj6yfkh%kVV0YQ;~v`YSCPruR{tuTFUU($u<^L0uk;W_ovY*?dL5SG8U8@)>`{sCZZ%GnTe5=Qi-;*s+6Un=N|T!{F<LNZ;tYCZ6ays&}Pw9DAP*IHc*0Q5!NbZzU6sTLy=%x#^^%)%tKzOE_xLBS{K5Zc~RkteuZ-%(IOCbm18$<QdhI^88slvC~PZ9mAFa5S~q&ANhJ+8{Ih@<0O%leCoNR^><futRHx+Rj*`l&j<7qcBtt4v7*O@^llil|kerADQG7HdIzZKIDH;%%$o8=U3I5F_ijNgUI|@NayH2aLy0aMWIM0gh1O_`OiW19QP8X9r8E!^m!qVwy+=W7U6Y2*R{eL6%8P7!KwRwSnW-H@i0th_Rfl%TUopSX6ks`&LY_pd#I~^3ox4;YfrF*4K@5+EUYeDTkT9CGssK_GWz%_RHK!zPYtkP}4Ney0*Mo<KW3M`7~5=l`WzgqiY-{kHS$3Fv3OvUsY0~SbXV?+*0{r2)QWt32GQCzW-UkA1W5l4lS?hh{EYqzDOgntRm8N3$_;f%^@|IMp!S^A$#)C&b`FdO9IZO{YPS%aRxHil2LK0+T>(WwZNEFN+~#}#?x!|@MG=9O|kGW*kl7i=<zh_Wa7q`Ga(EP#95;TZV2eGFc;sE2e(HetYZnSk|_-06-1v<4n-&{1RseL;#CSwU^-QjdiB54oM>Cx)3Z0uhx2byUc+`F9H!xG)LFC|;>qiceVH#xw(43S~uAKvRa51^dbPBCc^4{bK1K<8^X%RSBb1XiMAG_E`^A@p~U&(5B?fs2<6@qN$;TB|}4(ZatHJL7niyt_fAjvq}pdmy1){`7+vlcWg}~YJR~i%S!&JF5zm)`jld$GZl>pTIx}A(9%4*qzADO3y~s{B&unKzRHqk;15ToH7Ce-f@_tiJ#CoFCGrW5QR(gi)<V8OXLV3uQZ@;i%H|m2Xrv%&d-)MIb+(1j`FGs@bhA}1BthzInJXe)$>eP{Io1Io%*nbsrHy63=bjEDc;r}K0tuPYPf`nLUeYuroodN^6}<xMq-5qx6O0g<Jf%m_R<xqHVi1e9`4UH2)^NnS4*smb)G`2kRpM+z%%%tI_@dAj$sxB8teXn6Dd*ijReo5ihmSD>b;=i5O?IfH2vl*NIH~+vkm4+4D-~pE$K;I!l-5lM6Lx{GXk@a2z~$Bosu^MM3b{!KWE@E*Kb<h{R1&;oL^zKoFNjZ<Q^ZXxadUMw%JRqv+wCYg;XP40h@g$J@YenPYY#|i)@kO!dL%qvp*@gNN*1JMh-oc-#i{O{Bje8UiG*2AbhU<3-KNT(5$|J6=05XXj6^8Y;;9mXw0u)R0G7p7T3lh~ae%9xpzVMLAlDlk`HrfOt>g&PQY9L90@#qv4ZxmS90*%FgrA^EPuzCfwwT-mHy;W#U9-{#F(~{JnCGXRq-u<1(g~1;1ws!bFKtG;S;7a)pkVHuB*J6$yr(YKD)KuOas#ZRI7upSc3k-8(GRFsz<l7EwhFxhuBE1kUDr8dfJju#XNlw!h~>yRIKmgBAkM>N?mh#0Qx^NVspYGcC`ptac^V>K;p-{He|&oWnEKD|>D7OvRfJB48QB~*70K0Onl?2)1j=Mol%lm4m7D|i)HQ<qq&7RQQcMPNG=X6Gub7Ieg7qaOKv<Xz>VVi8g02b%E$wtcc8aAN#2kDnZamTHC2O5BI*i&qe4aYgI#xRYA@{TaZun$^>k6yK;UK-w9yFwN24$~&u7p=0XJH+Y;_Wlmv_BnCtAW;_*^3fRw*PxUjTOzi;EE*HZ@JLwybK+FNm>}84E2wm^IY-+7WKvx13LS#nP)h;GX`9#%%oU*J&Q%e4#it(aFD^J{3tFJdM7}+uO+Qv=K|AxE|t)%>jjbkxAaq@;B!c_s48R~R;kjennt%ZF9>8|B!<usLwX?XhE;KAm42d5^h`pIEvNI8h|Xu{=B!TgHcT^xf+JCli7G=5v%NI56(nF%`EQqXql+OJmh}junCS}X>jsSZ@eCh~4q8QlpmQUas$1$(W`OK3a(goOmX=0^MnLqfvL)BoiKVH93>-!dmsgVJoU%SY<16k|m_&qkMP<wS<oXf5f{mx12ryey49yzO7w9^ED4|O<S8L0Z^S0Q(c;ebw8uMYk<Y9XRD1G!23R(~#%Yh%32jnO|v>?#jFYcz|0g6D!ccUI!3#+&uEmMb<+HpCdWkoYCQlXD(M?N<1&HcMZeNjUr#aVX8ZywuGo!xf5(X`)wDlA8A(5I+UgeM$a#1<UYtWe;xFTh;IUAp>XwpwS9klYN!UV<n%3>!9hQjcjnP>O5~169PPXnV*Bm5OkM*&+uELWOAQtxB$;oq<Wj)}X~smv}VRP8v_!>EOYZ6q34)UwG!W($4}&6-2ZovxzNung|529zU<__V-Op@`wVzLGqE%NNMGe!9nVwS|;PjNV772auGT02It69Ytw>AdGM=Nn#9sOGS7JBOwZL;Z4!-q<G>P_@2NM{lL+uS@yfFw_Ln1%6Jeu6-N{pojdqF|TIMFESrhaiD}81C_i%*9$f7z_M6|=Cl{%h^4_L7z0!n(PxqcIP_(t*E>k>BQ@Dxc%+*a@=wgKfX*aeR^_WKx&RCQ5GVs@$af+xz=J0@8)y>Rq{1PjB^(Q-qx;Ii0FP2^!9I&$9#fyHvt+$m#~t^2VJQz@!Y-E!x~J{}hjccSTtyBT?$<wf;ZKHZ47ZdNUEL6u>F1o3hIi5B@L{l~@zsAGL_>IV7+U73b72<mkN#Z&Or!fohwuh#0zOI4U#s8KY&M*oK?dYIqf>MgCcoY&phY0v-+9AiV#ufQW*J!A(DR`K79!bu;O=F9!^zPp^5Xw#w;l+x1TUQIzkj5~r+N}jtwY1@w7PAHAoysHB#EutOVXS;r+2vm3zZAFsYm#QeQAgao01aK8)35$v^MTQwu&jNm6CR>NjxR_W!E8CL7R}n5L3ZqwU9jg0UA(*(Cp0;%&+CD|y>p;l580tZxPKVDwgAo#!L5;4itKulp${F-3YZXykMI}pQBXOZjp?X?tNqgScL@)}ayQ=z#0;!X05=Lp@1O&(NvoKf!GAjbWS^sHXq)Jo>0Z(TOm8F;qi>$I_>qH1xi%HVkYM_7Q!ZHFtq46>df7~g4<st#Piy*unT<SNoeOcgWjY8Soiv;e1Y=I-yI)}a@bOpBmq5>+WhZqGCcnL?7)dH%=dK6H5SLfRk%mlCQBQh(rJ!pZNta7k4xC>W`N%6DgvHhS0f@=$!Qam1Dv4I{CA9QCeI}k`?hi%F-@HSR^$g_(oN*g?EoWpdqS?>N$((quGiGePeiFwnhO-Osi*AX60*^^0RrHsAEKq&|$$)D=BUM7D}7fUMos)a5IY7@9^D7T4PaGtKPeb(1CeVB=7)M=}c5K2XsRK(MC;;GG3+JuQyZpwc(#9a(`-3GEqz8z1cDI69wUvsJnUrn})CISadsI5CQt1bpCs99c=xo;=J6w^8_WPzttbkc*GFkK#K26VFm*dev%3i3dX&{!ejPjL?63Ut^R^QfT*+kyA1Z-EmF`MdjK8F5-z$=e2C_%*1yxjNfq)`OdSqtG@@K2{LVvr2xHWQSRFB(V!3<<Vm66gY_@UocOk#+i4>d-JeON~w_eY$|L<6j5oaAtM!)a4}j6jA^%^+RL7P-tnr5E5WMepeS-swTwqt92>2&e9g5=(N(5OOL*^q68HGs-8e+^*_5wSkPdBVo=XBTnB8YhF9R$dAbK8uRM2=Y0S;ZH(vFkzWHgygIIf26YZo<~Nh=ZUP|pw?*SKtnVH>4su`y<1Z)2rG3b`SGts=mCH4zQa5?D6AhLnofVz2_`#a~cxn!zh9ZI;)0tAG#mMm929K>CyRqs&x^s;Uyb3X9A-pV)wEx%UY{W_?$>h^Z0GYN|<?_JaDOg%L;MH+HGAjSpYL<t&_vBljs@XJ&lWl!N`6@%~ssZlIYX#pO5V3hY3UJ(8he@)?L^^b93!GaD)%KW5R8>|UI&c_d_@&171)W<(Ba%-BZ^KH{`dl|zXg^F*IV9?4aFkwGs)2d)4$I=NLvAi-K#;BAE}#f2MbI-v<bl9K7?@D)XABNZ?f=195}sPeBDxpHaq97bDX5zCh)>jXL_kr9NMMo?sZ^D{}}%`&8PDv>cZ7X_=}jnF3)<t!tXl$C>82g?=VU4-!V7VO}H87BY7PW&qI79+S}r<r*OK-yUiaopB2ue*>Ql|k-uw%QC0iW*Q-k(7~^Ng(`=sOI1}`@lmByy76W0##~p6RgiFL_wqA1E6Z95IjQl%3{kEgt9BSNrZ$8Iwf3JMVMHmdQV78?x9oErtpg2NI8=YXk99TbI7Y=n-N<tv{y+V?8%y$ky};{=FlT75+*L4^m-;7E<EU--m~DOitG{omZoHFVUH?RMJP~`&=cExg208g-k{h%jmk*T)_vu=nscBhh1(^_VO5>Li;4;S3@!3Pq1!4t44h)tjg{->OJLP=jzD?wct94lhqC;~G||}um`TwcQ$C`A;gE=>uwIc711BinKLa*-Tok<gAsDV@1r#_$7Evg|GPjYI6LG)<kW%^kR&;&=W=?wCT=<UUf*m{cC6nf+gpryQ(cKeE5$*aEq=HJsXinHeTc0Bga92rzb2vzcf;6<Bc}4b8ei_V7v1+h!3P6g4tcs<q3ahJ_5T;AHMHm@gPb%F<m~&nRSV9sK>cmaXgbY<s{9&{@Ucx?S><H$Hl$w)ya30cS2>aI7n=kW~G?x&6#OZK(AqKtPbb_3lkltd8D2tEEu@TF!FD!i!wUtC!s|hP$L`{d=)I1L&d&mrO0LmJu^DZRAA)aP++A+cOG{|JE2_|MzJGz{TpEft7(ImKkfSD%`Aq)!1VWY`S*DVOZyYFm=nKD~yqL-|#CDmF1>Tf$n4e95)l`2ouR;fgnLLHE>gwG{+WLf0&rZPN{FTpy!as6Fzs8&2FiciqUiwZk9<+fy)oma^M87<*A5t8wWgM9@i<xAOvg9AM*bNo5#YAJPc4Y7(UI>b7F^dfH{@u{p#t72!Ro#1gdE4l0{>D%mK&G{;7{u*gvH5o87y-{Z0X!D__oceso&q}>3SH)~!K4ay*c4(|EKh=W?k+tQz<uFQ3#}YQd!2X7+2*p{n*o0jkgn<~Gq-zF_`F^QF@Z(I~>@#o!dNIB@g<#AGrL5EfVXWKI+*awY^+LMq+mEcB_)I4KDUmImx}BaK-m_cvSq6Lo5Dg=TKV44Awlh5h|L6r#O9r*Z9=cqDTVxcDbO^MZ71gB^pdIs@UD{N$3(S#cU2r@eCsE|9&(#4i8MPj`9zDvN$Xj!&C{=3AG5y1E6)PZw(_-?0Kn|ap^6ZN*fR@LX9~=1L{{V^I5-t')))

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
