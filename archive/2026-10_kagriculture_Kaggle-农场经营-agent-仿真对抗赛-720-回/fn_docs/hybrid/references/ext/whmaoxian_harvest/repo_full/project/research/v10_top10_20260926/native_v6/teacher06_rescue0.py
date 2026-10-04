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

_PLAN=json.loads(zlib.decompress(base64.b85decode('c-rlqTaRSdai#xDKlj7FU;Nf0+ZLggn`kyocmzTa-~nV9uxDf&n1SK{KBPD#v$A$XtQGrYR#sI)54u3XJe9f6IeSN}^{qer*PB28>0kfp-{1UAdHd$i|NNK#`Nu#1+kgJ$hyVJA`1Y^=`u^>k|M=6t|I3g6%OC#h&HwqoKm2=nTYmUo|LuSM@E_lN{nZ!0`}XTMZ{K|J@w+#F{eS;h|K@Mv+c*FFKmYVkfBDnD{>Kmh<-gx9N`Le1S0BFo<Ja%L`TXst_iuiwOm^khAKrcO{{MgGFLfEH`}tzO`|bO8pWnRAzZ4g{_;268|MJ&QtLuU+7W8#N5(}nX@Ws2+FD{04MSS?p{rwMr_?zFq|M2nePfC+r`rW(F??0WC2;X;DeA-W6_piTjuuIQAEuF2W@8ABs80+fy{pPpt-+z6&93T9B>E!p#)^e=U%E*tF<4>RZOJ%bwAO3)yU%}B@E`?q$r`PvzMM|qAzfI->t9I%60&CI@kgNq3hh2L9X;WHY<!xmbSYF<(!UAjdeJ(7pF5R@*{5gVMdj17Psl@*Avt4@rX+?TOMDxe*cIo-24XGsgpJmDOEUV^=^}#|bCwFbK7TS>R_oTmA#V1QNfB0yZp8pi$Gsgb3VwawOT9s}-_cBZTGD~lRcbT1*!pp4iugvuhM_6dZt`weVz^>}yORPyx7W?<hb}9H!iuUgpn_YVTY2tIt{<LYAp0Ad(1@`^-KUN7xgCG7mZ-08gX-9)EK7RP{{)^9l{M+}RK7aM$tN(HOalziLeEI3)$;ybpW=i?I%zj?w_hO0J`90iO0gvXht(f=)2JhRrC`(biqwP;?cB!%OPaj;;);Zf>;KPCn6e#Pd;fK_da&EgW@AYG3kE_y;o`Jn$w@Y2Go`*k3VjuklI3Hi}7yR{aluzj5ZX<hdqp&E2Uj`X|8T|6MW$@dryWei#dHxQzITHihosssbiMT6HU$JfZiv8=qZsIjd-nQ89^khvmrPCz+u%{)zefQ}f-hcDi*9`mS^QU*;{pS6rPydJ<cME!SIeo?^?vaVU^y=Ootoxn`>7aM!VePKdF4E(b(4a@>3w@KJuZMoIOP05YiS9*Ix}U)J1SWq9jrLK}d_bKp%S8VDN*A@$T?)Aq8Q3TE>33${ms+P_`GoHL4>jyY<fH49`-#|frbKr?lejjN@lT~2$enHiPr9`#-5Xl(H`BcmscRV2JFwyH9A*J(*Eue-;gqMSfjz?|cE(xQ4d78*Or;eQ@j2D<j*awV_WUN_IA6=}%W|O(3AR}ryPL(heTFT&o0PVrNa$>fXVClGz&CaRv{k%hV_?wdZf&%SU3A>N=)|@s8$VnMcFE(HQpD$9%a>B-ud~R%hWIAqo5<s^ooG_u>JcC5Ex*9TUuVXrP|J_3{Ek~Z)CPLLcUtl2>l}EObM>e3ozBRQ@8t$j@-&FjW`ij4yVL@o1TM2-EYEPmxY>-!{A(M1x5PjXgCf0E$OmpXuRW4`q75h43Xh3CcPI^Dw54@Rn_}r4GH!MErfC<Ic3UJjIgxH22EKV1@cqWEwuf$GoMt?$cTR+fea>fgm{;~5p|tF!Ur0rPk8KSd`Qyj*T1QULcJfZc>Y~G-vD^Pb#z&hIucMm?(0RtucxZHkC5{6JTj|Q3y#t1KH`)P+{48o~dH_#ol*3%3PmGgyO(f+VJmhz<_#Rez1CiCT<Q=&H{oHQsQMT_r1LyW$gpuz2-N%pLynj$Fe7pUTJp7A~4+KVi{RZue>;CCOg=gchr4w+RMY~j;u_WQO_Gp#TLStq~aApM&R#3GS`g8qtRLf)e@ChjtN{-Md)tVl>hl_1py1w2bt+tG*k55a$PTjQY)v3y_B?FxxCc9pJqa<)29Ibt@yi2SHO+e61O20;1?U(OI_(#O6KBLd?w=6v#OsAN14^+!4COx7XIGd1Gazpn<$ue&0D>+~FRDGqxPTO9{{bGkodl?J+oMyk|qPUo>w_KKX3)mP+-l%{x>eCXBh-6(4Z*b6lPr0wm<;ryLXW9|_8FghgX{WHavIoAhA>}FW<ZaT+F7lJ(v@BPf1*gBEZ9PqPsoI1;{o>>14<Ff$@IZA2)2;_M!hLi5&^_CSeCRQ+((3am9k4ypoV2W0r8%cB5z-C6E>&BdrzPNz9qfA5ft7Av=^Q<SylW_(qsP5_le)_r*jD%r!Y}LqEBqt!_C=I~yVSQcE#5X`X6u!<H>rF_l8zv4lss3Q{ERM28^;XkZq}RkGtyQ^nr&w_cE=OuUFZ$o_1ddagO3&<7v9NL0U(a}1qJ@Vd&`c1a#2UXHWDt<ase9EA!%Q${29&eU+T9ga##^h4h>vRm%2$i`1xb^^W~8a^1?x;I%mI<_~<oT+UKVQzT1^{Z~pR}CK``_t!PghwL5+NqSWtO;YEpRJv~c05i5HAPuRYz3-Itl*NN+{4$ki&a}S2aMP#!_##}_+zKC*Mzd%vyblSFZoHIJ&B4z{<$|D10#ar`?Av_Dd@4UsPJ!I0hOzVoX*Iu&U^Jkw?fSrN*YUQ1s`9hoHOy35XzYQ|qHp_h5Eb+8QO?x=^g@mV_kg0b<Ocea1COOdn`TbWPe)r~W+Y!na#_Im?b}8&Zsa{AZpZt7Cs1bthHDlOzLuEv0e~q38`WmVBTj1eHXYB3M<UJBS1#BqccwJ(!O1Rl(=Pz-{N3)IFU2a?!wsBe6#${(4m*d97zy_0C_r;X;p5~HUxaQZTcDtvr)?!3j=;@is){6}8VUb4BT<sSXJ3mtDb#@#w*oNucQ|iV2iBH^fe;qI@tI&J<R$4In6bm^jHTI;`FVb}FD5C-sUGa)=>Bu;2cZIC<DX7xt1u8Kjk8p7@=OP~<;NUw=&}as!T?Z{zje*w}C0ZYZ2%zB2GNPIq{9pB?a!THAS$MmpBORup>>@}LC?80aUR0%}2c7PfPQFJJ593P(yoc)vbUW=t{kSspR+P|;+Ov=Tye;|e<HrwxGUgdNJ}!#FaZVZ^TT8_?TXkz`l``0>X)SG1Y2%*Z>r(X@o>9$lVozJ;R#6hjDiF_N#v%~?T=pVJKq+X5KCSNh1vk4+y5PPp&2I;nC$=tCpV-;5jB0tX2^sE)^1@05-Q{Ja9dvhEXFmj@U8-(nPD{G^X~iy8j}NC$sm^tD*QM%y;IzcOFq3CtY7WqBIY6)5KR%QVF{Be|^)BSoQg9(h;I=7tDY%fMe<4SHAxHm0j=m=>y^sqaMJTKip#lZyjsg*c4OVJB_hx{ysV_l5v314SlrsYr+BFth`5cE`^7z0sS;j;1gp9oS-b8Wzu8=T#Uu^}n5IoVd2|>a=T5*Lv;PjmXhPWu2^MKL(2MqIVBE9yC{5Fvf7SnsCJuNlPw7=e!le2QHOVtIIuP)3q_ff*P5tMCIkV+nJqdtH9{kzW}?S&PTeN>i8y8Ut0t_2rkSS<ZVA2;k;a5aX-YCQiqX*mYZa@^Xub<BE)3@zK<(6ZC`G<jfC&@=^#@Fq`t3aiGLsJ<DSTy@^29(XfS@@S}zXA38mkC<rSYUI-#BA@2483PZJV2SW9B*={qvq&x;a%Qv|%DPz>D6<ryU{BTQRF*-!dS1mk?Q$)~DIxaAMB5|trq<Od@Jj%a4#IX1=`1UKt0}UY@T9SDfBed=iKaN!JW^txFU+F9OYGGcps?8^h<01z=MB;iSNrMXXG9xFzv(jaagBG{9Or>aC<F+4eW&bsOBO~FdG_>S-;#OnEm_#cY-by@W3MqgpH>1{xsFL$ma0p)oE!`)*D+a_svErm4#|p*Nv+5dUKc1!SSUc3@VYIh97xs$%1}-yK!<YcIls2CTUVTI(;`rzy<UVLtuC5E`t!alYt`rdY00oZZrZi#@#wT<njd$5`>bl!mqr1bLgm>{^E$?(LAq9euKbq^v%5%&99?!;SFST(mZfSp;IyRK>weg^;ESdMcXf((E&QfYdh><u^)$QU(e}Hu1E#n|R72c2nr|PGn#Q{6S!%Y->g*b)Ew4H|83&+3Bkyp^Gkp7<*(OzHn^c?D<1OL~Dkzw?W0!c!Hr|oZct-|6h?5~;;Xvo43|@DD!=l#esqDjR^3Sdcgu|oJdbTVs=1sRF9qt<&tHg_&Qao93As(E9En`1>zDA%zd%h-FK*_3bie{DK-@kFoNFd@R86!bi)<H&s(_Oo}h0ypGLX$UxNjz3`{vhL#b)_eI!aZIc!QMgIt7BaUtqv@pe(*EBupj)6INl09(QU`saa~Pz@iEhEvx&0JAJXHq?+q!twjF4+k9_dFioo+K_y`8M?HYMeg}!H<wBJ@v8Au+^FfVG2Pj#GyBOj}!m=xQ5wqkPFFF3Jv5$rde)L&0>>kb(=Cw3xV*@1kc*-_#IJn*c%z_aqw#=tPK1H%Y>T;jDt^5ihOfO`jt0_4U=pfwEaSU>Mg=?gohZ|s!5?+x4sudoLe$?DZqcpVxLB)$5i!E4bbKQfQ6b!1M0h8hbRYI~reMhnT5V2ikEw@S3#s?c_;x@os++dxB%xj5a-#T4jEOz}!VtCWI3c^M&+gUcug&?!Z;E#Ql%@t}?4(>8yb?Rv~Jo@hpZWav%2O(_9WdD&-9`;<<v@G*HK;(m5rIe;13v&T+iDhDd2)maxP?@plrz0=ASl>=%=Mds`QWBDTKzd$GZsfY{sxNg^~FQwCx&b?pOrAC_>YA9wK0DoQ2=%a)Eu&)pTD?oI6savC^nE^f7$Lk(wXrJxEx?OR$3j@qN>MjgOcEdC*(D&%G#k?%V0VMd9J5-x=^l7)Nq&qG1ZvVn}x&R8n<2$X}MbLB*yTs$P@rmegop}8#&+T6$XBHdUN`q<|?a3aztvc}5=)~Kb3vE%Bw%HMIM9UN$dYkQ{-}Jqf%%IV=L)#{HHz#?}*EelbGa=2Iya0BhdkxGB-409%cl1)Gzn3!kUdr_KQUb}ZDB2sR9i_O@kX+rScs>4!22Ksrwf_({Or~*l9_nyiOZ~Mmvzbjb$vdegS_>M|=ZQO(hL2k?YHQ^=hyXefzB3S1<D@U~{Knuzk@KEFQapT`uhVW<Vnm5xyiR#Nm9#2@F$8o#{@a1HZbvQvCXq_4Ij^whyt-%3YpgkMu-?46Y0V2Z0Bp6Q63-3GHvG$6yBIU9(crH*>=I);$g#-+&nDw2o{wZ!Kr>!$P-a_dr6`Zq1&Z=WC_ud`r=l#t@)_+~^;mN{X&CO7epf!ON>hO0Zs`x@<3!WBjvSZz`NKwzd;Eas^6|qYP<v?)56?Y$$LL49_9`pP>Qe5>?Ta}&-$GFIADz~Jh>hqfECt!`prUx_CAZ}*rLCofmG(U^f(|U_$-D}_@+$bwOWNntdJhki<tZYbqX2O)P?p!ho(PoX9`|UUNZ$P88#D8Wp2j13_~<yfqnkZ6&DSDzgJ3zb=fCfX>4xoS#b7zIYc@u{1(@xU$2UgtXG>N75*wdHGiYfb5+Aha5hPwwh-u;AJlZv%WpSy6rn*#`0M==W7k~^ic1#p!Eb^Q&>BOzg9*YMRUHz!&#*atE{hZVvlz>q~Y!GTTYwW$9_B!!pPof2+%`Wb<$vdI}%CXrA#Tw<=Zu}c@u-LQ!$QghE_sWwX1-ppMXb32AFyA$Fx1yn|Xk0AD%*mc?p$)80<u9@E+@V3+*yTv`1BGzfo?~61OF}Xe4%g}H8+_tgv`Zc@r-X;XJrcKN{u&D{Zj<GA1C@*F>2tVd&k>peYxa<=6mdhZfNm1axhXW}rqPp)VOKo*O*dGK(nh|ccN0d7%yx<KJlBbqFh8@g{LF#Q(#2!cV95}xQW&39_V)D(7@^s=b<2ym6G$ID_V|Q8-#N~Mw26->2Yl_thxh%F=iLWf+v>`N!P=SWm8*BqjWq=34!jHpQ0^E_cs*fI*E?X>=+OLhy9Aa*7Q`bw>1&h;jMLMmZ2aaQ!lzf7fZl0{`LrwGhU1E}{>|r4@4oxZ`%j<#(cZKuml?$k;&khLn(}eto@KgqJ{=Xko$hz0n}Rh^0UM-5()KucM@5WsdMcf5)9HAcX?x>LGY%GNlWgN2fe=#sezNs9@SB$4*|Y?B({c;stc>A@5O2gL`?wsIzgRfQnc|wBw2wT}KJv8bBhUOUz44;_vAx_^ccM8_U6(zc1LQlK>rx^hX{k?Iju|%Pn32|2W?EZWHrZO$7d_AqLvk6w*pzrT=;bk4HyX56L9#cZH|nh3Xzb~YCapJ$wB9J~QTpXUh3<50v|0AzhTccRiX#oZl~EwQ7PMByV(<_HP^V`xKuQ7JL}<W7A<|bU_YXRL;)143vPDRY0UWH7NSbe;^AWjcK&bn+`v&w*6mdZ$)~S<O+XQXxxe1>IZau|<gOej21_>y}nt0eX*24mdRZ721Zi-~{8oEa5AXz<I*5;W|@`i)r%6V)wPN&=XzLrE0i}npX4KndW$6}Wlx>=n%sp@92OYAf`QXbBCRN2VEEh7)NRI-#Cf4{8fosa&;Obh#~U4g2@GO&y9^ab+9gBa|R$7>#7AB#tm#9w2!DJ%p)LF3Cb9=ALk{9^=~Oac^=2L#6}#1y{<;PBA<7=?)mZuIqa7Lq(^pJ4F#{KURu<@I6BpRe5bd}Z14EvG7He$$kW11F)l<4Ek3AW~ANO$_3Mukql^&Vw&$<!#_0Gm)2!XuL~^FXzw&Zieq<-LTVWj&-Nyi_;MvDF@ajk}QKoPbFI{X*>q8IH79G2Vl-{@{BB%zbEmYD&Ooe+oQycXb}-tP~CF{HP#h0SXa>8a|KCn{o+%X6kc7DjZf-4>U!AH7vs?A;$uG}C2i*>ZKxC$P}1rih#mQC<|%erJ?9j=h_vcwerJ*m(B9ywd6O5k#v2l}cCcTuu94pQoxZ?9D{f^i>_CrL>mpS^oA~R@JX^2we7tU#82xjd;ivL&p-YrIiR1c!JLMn<WL*D@@caE&AAa{BuX=|&_FSpf^1!aM1G~Wv?BoGjBB|E!$SxhWS*y%u4YOkpK6^0mc5EPsd^N;|0BJh>Z!K7Scsn*GEL!hFu0QT!gKGfSC*Jdu)q6@uj7lTR>Ve3zvumt$yR`9yvq=-qB&grey_-H{S$_7i!<UXMgB8B(dKi_U=oWb_g>)DS`k-CX9cmmLF`}vP2Y;ozouVr`K+BP%@5;N}P{0G2nGG0KAo8M(Y?r{Zuz?6=D}RmcISURe>SB4Q!bqTuf;%|1or6=~8`exdJ~TSwRAcfdoM!$K9rKXRH*EuLa@3yN%D0#Nr+~7vL9gskq_abju{RW%>`+8L4<yK5;TVf#+AmdUzf{}wOF4{B4y?H1V7j`z&B*a;G$6OrDy!)U@e2MBugL4b(o-_b(%#?!##AN*cM$nWN0Q}c1zfL43#RUI<NKb(deUNPBt>+!^Uge7xA5VkjSn9kyq7cZ0Sn14q1uj{YBELR1tjmGd7{@$>x*FK4TKYjn>c}V7+fr%vAGx|8OZo^p~VOdP{bE}JStr^v-vlf&1gaa9nCJ+qoon3$E4#@15Ndim2R2$awXs#S@=t=hw0r^#-DtW)Yp2Xp(FAEv}s>^VK*h6KXxYTP}u0XP^0HUO7K~xNgHL8v{Cs;sX<3dNqdojE~0e_wHLYhu-6@t8-kNK5D*C;8C{IX$)5Wv8q<m)<N|L62i)UC4|r3h#&e>Z_S<&5MtB<z`uZlX<N|_KjZQI{<mynHIVg?oFw&wHZyIflnfZ_{SHaumJKm1kYs1t2%}jX5K3cV9cw*!Ms^hBJGY<pZsr*QJ2Yoo^F5fYCF9CDcjWnooSPbkyhn4FtrFmCvhFnIzQyI~FN;(_p^2oLJOUXuF7l7Hwh?cFeTDH2UWoxXKZLnIlxu<1Aq-kfz?hDcF6kS^3b!iS3o+vP*(R2YNimXe_O{7G#)9*&a9uKI>ez_aJ`R)7nKm2>NPgrb{W`k3$)-}KR_NxzH{_*Q~-+cZS;@Q<lqK%*aHv4Q=k+<WzKzlnv*oc^T<y+x_d5snR#lb57BvqL*+?Q{NJ5TQ7Jh{xL{%EYV%)5XAzcHNKlYuD0<BZCMKQI-~fvMPkRpPxv@=5Dy0dgwHM(o<F_=|2=X=CiQYs3^VV`h`cYdo@D0*7}FAbPp-m*_}q7L^{2?c!+^xctm1aGjLM8R71eH^2wp$)4;II29|?=|I>uRvI59pE3?54nZMRx~f^&xLtz-@N`L>=TEUCgE(nRe&5TbGB!Zacn=ArGSo$DXFWlcb|r2m*i;LWmb!yGGwn0O8J*5yJW1v*RWXqT)<u@$o{cOex+QU`RMky-8tTw*G_QKtTxVh*d7TjWW{i(2AI#op5<ncb1!DE!3A}S6@_J#2H*n{nU7v@h7=IFN{K=cfpTZk|nq6Xm1J^~;rf3}IP3nxC5);p*3rX7K;%JYf8q)GZ^l;BO|JZ@;E)O=0vi5Ubfen$8zA26UFz|NpfUvR23y%R4jsl7VaX3<{r(Gk=Y7mX2FszYR(_|TfdRBGW$f|baX$$v$Lrr;WDIJ`!uu5146BZik$-5)fUM*7XFgOB{%$#{IOy>Pw*`wftVAhSl#%^;M2=!k=bxLc)+?QYd9Y$g}lE;=W!(&5RN9(h%;SpG$ehsBI;tGm$Pn74|ZkIcZ?8aeaiZu&jFGK+H0B@)gkXTjuOKiUIp20&KCJk+n=mycFh<Vw8rwzLm5fK(35QA^UwS<cTm{oqpR7kI+!oVzhLJip~*?3P*<A+VdBLQe03BZ*RWNBxkT+m?vn&g@ABu|hcrd?v;#bwPC<k>fZJO_V`)1F5XX7l7Rn;%O%%eG!i`M6;_Hi-RlJaoSdXuJq31*)0P4*n}Ins0W6ezsZHAbwZq`X&#JjdlqP&J93>UFI*b*tUb!uA$Lx1sS?a?_7yiHX?A!m*R3sPo=tN$7_3lufgjalU-tn;nqbEnFYJV%A>uyU1EfUtSxg!PkZg?Gk8a*kL>`fjUm4<4}BUuSt>Y)PciZK;_NW}$~NY}?&~72$d7!)y3P)YuM>DBTlNQQ*`IrseT03rdZ#9yN0n)GU9~G<>x#m=>zlm0;mV(tZx|T3zX!l-+7rFe+x@U7iP}aLmrXTMqXm8`*d@jzZ(RhLkg!X9zSyd^;~IYsDxX2R#udR1BJqLmovoZkhuA0aevY80L1LbcdrspyG>d4tH{RCKJhl!xX>p<pa9u()&7~)d3~lQKwCxJ$t8zzQT^fCrwBzrzkG~IOAMzQq*daNYXLE^A=Iiv$I#0t7jBN_*(J8MI8lG_HWj!xmmg08EwA*3#eBuD=^1gh;ec-YYJPG|OJ$w39!mv3GwA6vpCOS_g?VT%(AvBiTGHE~hq2rpTV^Qh%2BKyvteUCrshMc35=~W_JnJdiB?KP0apO|#5(|HHYqp8s6#8M_|H-pOl3hXtBEEX~Ri-`sGB9h>aqeL=&K;mRnUK@16nG73)jia$;iqm*`Vu_}kT;678v3NA(R`&&bEf!Ab2&;Zu|$ChNC+#<!j&OYfrm^5w8OT=6d3B{MLeivHBuKicOdztykDWwSgS!}tz_KP;BiyKgPR%~xT(S7rZhrTe`QIIifTUFI(vP}ysi<RO_f&lH&)a?SWUm!gTh$P5XUy}c_`$}^vXdx*QN0AWXn8YJf%-J?20g=I8qy{JGHUV!i~;KUnVVL37aC8XnRoE*}`VvBP{I+l229+@JJlF1=9^qN0vzf0#M9J1|)>U!X>W{2UDEojTV^=+k9>KAt1+gj1DZG9REnWcurAz4_AD%3rKKt^2kI3pBEX>{NQ-!f!z!bOe5wcn|(!u&}hgk2QjbP%m5;Urt>1f)4a)taEDhb*=w|SN|yP}J(=IZY%Wn8m}qfep~Zo9QykcA{t{vSFZ^-3c#hL$<2YSB$LR_a%6VLLp`m4+*5FM~-euUxyL89|6E71ic8OuKSr=iXA?zBv%>pwG1Q<e0oGee|W%N3kV|O>v0dAs#zBc3132btbF#~aPC5j;u#mfc}90~PGl++N_$n$5Ox_2V!4!YR1{WB&K4?}+^567(7MGp`Az_~{{?6->?nOw6y*djIYU|as!bjPc`5WL#z4$eICtng|_fRYAF7ZZ@U@+5dQjFpz}thCFs(rnRS<YO-r%?Oj{kWzC-PS@#>M_Z_XJ=&lrOSXOuFWz}5`@eK7H!bZYwnSJ_1@Xu_t-70zgvS`%36F@J5C$JdR!S(VJ>z8Mo++?dN=LKK63rrzxdMF;AT%%I3{s(NGC?v68+iczM(X-Bk5BVJ;{ej!!@p_T1=7Pa&{iiT{=^BJL(?YH-abC+-Ht{h;5v=PojfNk+9d=uuJgd-z*~ue$4V6Vu|@EVEuv4!SLi2h_v9SxiKh$Au>{g{Cm)_0Y+{><Ji<V4nFqa959qBqKyL^g4tk<b{}X-kPjsC_mt~1}hQzLGU6OuNt!ogm>$O!-nT8Q0U<(p>7FeWNVA;b0E3}NVZptVdz4wj|ch>D{`4XHH4~4J{UYZwpm0fb63+1&Hk#7CEKvdW^n#U+>UnAP_0Fjikgf+17H6DnqioUB3^j+TrH8>(4gC~_T`co+re~I}h{CCCjnWw#L)u>B|#pBM#^RV$`xxkSsyXU~hqn%_~jYu4Jk*GPE^fjKJKc5hhr|<~6U7;T(*EPsd65}NV9(<7O5~HKIE`s>v*d<mLxFJnSWa5S-UQ-w+z+mtuuzLB~WA(DbHz$kGIx9jO^x-hl=e)Fe&U0Aas>3XUIBb+A&AI?;(qKS{xM$3{)A3#i9S^@(;6!_QOci$|Y9R1#=$b$TKyl~fU5}HusZmpq8ZscG?*KADxmnbKrXKL!uq9xo+2FQ<In!Ni_Hu$bhw(|7Csz~+Ls1bE^}2urYs@{c2DD?_VsZ>$peMb_dua&0#5r#YX3)k0>Z4r(=Tzmz5cg4=Df8D@JV1tK7eSnlg#1yC5z}<gACL%A$CTvyu)RquKc++ZG2P0K=}~@UpYkKK^O9kFQl-Izu{mN^V`qWqDYC%xV{v<%>N-`>SC7-yRdAtG@voD<z8H9KWb)*{W`F)`;V-fJ@?SfzYaAY3qr)Z|4-KSf;B5s>Yl<V#sN#V}8dD9rzD_d{rfq&_VFgv00t#Qb2EZshg0kB>Qeve}bOVFo??uIG@_3BlXvInc`Wl^%GaRrtIayXR1^{$8NaO(#;^d4VdZ-aZ6%-&#qLF-&NAd;E!L^Agds<Z<>ILInU4u731-k?$L}XU$gk55`S?cEA9izkpv_2E9gpv9tALx9C?mYwO9&uc)9(iA2jS6b`EfTT|byl%U95lfG7BzwBc~#aCwmlu;9lm#S@V$mA`_@=6V{^YQ5-EC#=a7jb1#HfjSb<t$^=Wkv*w^f|rp1$c&>2tjDH(bS;Gxrihp`EGn4ZwxU?)mJS?pMT)m@ADG9!Ms_(rhs3gROrTXI35^c1CrY_4v+#{INNQ8TU!pxHRo^_4qZ)tff|ioktcA8ieqQvm=Z2wI<(lbdX-F~sW_K(0jPgTk6k5Qkc3>rzk<ImJ13bcd3qM2C|34ru9)`MWgcFB=Ti_>?lrjMJXUXtKs%BcC&dM25lhnrKj^?~%oqi!7FPo`cnS&du<!V50#E`DN$vfL5k(<9%!WQfJ74djYmtf9RGG0i!2IQz@SvZ$e+`IGU;8#7R%PWJF-(1(#*9JwgSSg-?vKQjr@^KkWRxYdTVqQ*fsur^u%w-vA0R?eWtijkZuI4$-47Y`luGd$3oN)@6D?RElq_@l*Y^>1c6F7TT&*Y07oCD^ML{vRg8fr*H=zah+(Rl5D=}{HY=GJAWNWIPIc`=kegcD<*)+s072@V}(V9JsLtGb82GP)A7sC@PcpkF|wlA7Xu?%)_yKSzRo2d58gjE>9cKqof*dH9$O(f1e)X!H%Si37CjPbuYmS(A(5#p+e*(l<`*Z*D_G2KQzsXnGkI1e02E{oaGR084jG~G4CRu7pICp`_U2s8K}&9XnnIOPxXBxw4#Xis93+&54sc*&#I#sGRrBOiji=864(PTV!;Cy%s$oX}Qi!r|?CB3DtqY8_E--EC0yCekTOH}TNcb-#*u^e!Y;z0`opQZw0ix#RSkn&)@`naZbOirqPdIVe2q&)mH9CTShbNqP;^D*~FGRV-^WoNUqQ$&5=X!YH&ir&MF~UPw9goNYC#~wckd81is2$9AUJlIUE!b@XyFycNbTBYa-}&Myw*bFMoNiV|)AS1sX9GWI4W2=(eW1<!B??cC%FJ0Y7gOhtLemjHoPs+|ScZc*Xoz=m=!++Zb{?G5@tl{Z%FmPGIdRhPoUqpvO1ughYaHD9q))>qt>BOaQ4GsSQ#N;7Gl&4561d%95q^d}y%ybzVVm0XS}3J*cca+_dfOZ6h>X3C$h5(i6mPWgywT<nyecqHnKs(lVYUJ&mBp%gZ=$FS_lhHvuevk&E;4+?;;f%Ts6k+$g&1k5@ze8Rmk@boiF`3Y*O=mg<NBwid=8M61?IbUcfRYOuW$O|T_cYZb#Ot8tv@B&28wJ|R@4Sw91ExaZF~3{O$N<c&0!+i41x&P6}X7D??_=`C`tlyqY{6KnU~&HkMy=3n0nxl-X>sxl%ib=(-IpD%!MX>#jZffp3PQ$^OML<d(5U?VQ661Mbf<yc^6z_MWnH9I{b#c(_c+VAZyywMhjz`@vMuP=3(qY4Hcj5Of3^x3`KFt`(yBZ4*@mrP{8K^1qAo04OO9H;aiOl-x|EU4cMcaPc<GJ@jA19JsP==zHuQ$U%ZS=P7CjCp77qj5#Gy--sFwx+}N1H81GfdzQ*q4_d|qs9R`3yH2Fr;<OffL4>Tw-CSG1w4+AIYnZ$#o0!s2TozWLrl%Ry>LopC{PTvdV^cC8urm+1EWAi0rEL3>cbah2MBFT{8izwpMO>E+t?ub1?cXKI65lBW^ml%S*brB@kJM2UQlPo$GZ?P^QS$&;n^>t6fUN<7$v3s|Q-E$-tH-2J}`L@4006|E7<{)f~w`W8v%f_PdJso&FaPr2Tw|5|KPgX1qR(&-0)JM|UuNvz;)8|r|w?{;YZ`qeL@LjM=Tt~pOx5uR-i={SoW`TEQZ%9&E(?@4bAA`^O4W2yWxRFPk_-oAk2&Y~s!dU#XI)9DB=1dTdC<RY(E^&GaKAy5+Z+6Xt{d%|m|C}yK8N*E8`V&1FOUa+H<cNVPG*WPL049%e)R5nNkzC;j!o<Lg;O@={9`yB1UeX^ulK#Y}?;hzQt^Cv`uoyAy5~sY;?<6r#Y5!NdLVs$mYlQEi)7Lk6WBrk1lZl2|>ls*Tm^F5Zm7gDVy96H7$TX8g(@eCSUsmFu91{QJmiQ-H;vX@4C8XC6n|l37L;MhlKdjZyJY5V4E*|_PPFu)iib62`)8*)TY46|{H`H;MRmIA`<zd^>0nW<5bs+L8FQ@}Fc*fIqT_mmhNnfH&w75Q15A~Z=+L%1-3LLU)2Q&pfKPuW^i54UZL4d`Ppg5tXBSqq7rbr5OQ(6%l-(`81k>z1*Ay{Dtfb5K&_8JXG#1s}@&8OfAfKerkPcI-Mni9ulYo^n6h5un(^r3$aPuk|a$&wReqFZ1zYN8%!z)L)jbm;y-87>NXRl#JBM>2rBG!C+^6vvUaaFZNaPB-@Cbd#r+-vClQ@;;g9@sUT4xriMyqiy9eZq0ZHY8?pFa_CMG9v6hyQv47OAXjo__ab~P^}xM;y+F#j!FG(Wys5eU!hDSqILA>ZVUd^oMD9S0YWHAJ)6s!a&6Y(w*;lY?d+<k`DCSV*J0<JIP_mj~Qi!z4KPF!QZQ-r=l}C7WyToOP^0dz=d(>e{x6AX1uNfYzym=5Y+}s=5NQ1tDdbZK5*}Rc8Tlj0NzO32K)0PJx<QhC#v(cY5oA^r<k8FK!7Gos))uWJKN|$Ze73k1r+K{jqczD+n4sFzYNEt6&A-pg$=}BR8(i4x1MD#Gf(D6%lCGS?+YSSD}n@;;Wrz5RbKJ<{3Bg}c49Q@)~+2IL-TTq|1dwI3W1f$XujBZ!x^tg2m62Xj3SOSlwO?C;azMH^8E&L@`o}3H7cHuL@1OR-KzQiQ{R)gEVtV`8f>h+}D(yBk>q5PC7w+fjyia%AuqY)upxeNqoJP_b@q})0vby+<*M!N_Cg<_ZJh{dgT3E{$u8!oKKyRhI>>Yb-|D?B|V%_XsEE;6nHyvE`S(RCz80eQF&yZpf}AXB3{o*D(l^}fzbTogJjiv#DL7!lDHYPS{?q?<SOi-iYD01OI(5I8mnfrBRm()5btIaKe97%OdYs}74>1rmZfeSyP<Ho!P)jr8!kf^;jW*}V+0@6opsfXvwka4{+r6x6&U6T8e#>;N`}et#X95t_JTw>-j=XK;Z(rUX`ym{ikHw~I)#TtdS^AuA-NEqw9#J@iNcKqV|5J;wD8Hm+fHEJ!@%A@e7R>d2s#XJ7W6aO7b}w~a;`)Q926@7bE$*_x2TP-gVaJqe_bxCi7KJygm9Q%y|efnfxz2k!@jB0c=0hFu{3QIlpCra+52@1VX{4eE198JnTpEf-<CV-0PL3qNSFWeSccrWD;#Oeyh~s7O%~2#{JIqaNPK?Klqk{+KWGs=?P0`w82%5^vXvo&(i&D0)q+X|~HqZ!SX|xLq$(*&M1gn;~xcEim-BXf_h4gg1-0vqstwc&<Ara)7Ad;dV0E1*GgP^0K!m?sfr#kaT&KPiX-1GTGTfywdE!Mb7r*WhyejVppJfncbG?HTwF*ja@;Sr;w02>_LBIv2|u!PMtB4WB8s%dqELQgRv`F7eTv{!}tzxE_2=!Ri!<CLeT9Dody($drI|97X#1yj6D1_+a++CLI7TOmA}NsTTTI&DxAL@fYYugWGLRgrcm=8tO4j2m<Ph9Po78~ZNaH&w%*jKM)n-)h}YF=fYVI_l+k{HN3%Dr<&fEfTiwHCblQCu#kXH&TXI8f)dGGG(t@B}B4A4<aym3O^F@*x&m3iO)BJoV0lrug;AA-&MFm;|6hQGb+xTnjhsE=%5yJ9BYAcu5;6xp**&B4euKlC&LA%qYu~QI>$wMp#Kf)QPE@EB8&waLnov@8J777(@@0qFUzD`bWy65y>I;S`4r+wKwSJ<;i@Nn`AdJ4Y{xW3-c-J<Kup2!qge`88}gU>tt@J>HGgnkI820LKE9Y7g2{t^LjqUqDc`olaL|DGHCLZOKf?Y)4>XHwfcvb`7V5-Z=z@1BIQ;ZGQw^d%xbdNT&+4r+u%ipsl_*BlNHZ4iL05Te6PRtnLmoV?y}dIE*JW8-+|CtjJK7<m3+@bC}A2LF%_m8xi{6q@Kd{E4o7=xhqKkw(_5b;snX?;VMFjN#BO5*Sx;3Bk(s0RTj^Z;8PV6AeGCv}ULsl?;q3I<>>b)ft0He-AgBt=DPC%Csv8USRk00{gMNKswV&HWw9~1$(+JZnV5mv5yqH0+kmwTkq58>+3cvRFM}#!E>89(ny=EV%~9Cd7L}Lk;^QDT|1{Afi6*Y;dI_gqllKWEpyUc4C@+cV^=Sss=@??8IGu2*Fdym=mMn?h^FAmb_qNJNsGTqM}=V5*m$|vuuBLb7aighJv{KI6(FJzk7g6(aW!Ib<P%3<J~0j9&%S)(%pWDwUXU5=R7-p44^WqN2NWI%D6HtZ#XM@oE`bMK4WNcL{t`RQ-H4M%3`Q4gad*)5iV%a>7A?ZW4Or=zZ5|&HU+h8+&JAkd<ehu=$9eF9fPT@u)h<UJ#G{iH6kv0p00DfU#gD@Hfx%|;nf$0t?BHalPEFMYH@k?{Nov<9{8BRDG|_<5N2~oN*@k(CZI~I2r1BO-M3qk%w_G716tC%!`>tZYE!h@#;sq8xR>8Jo6$FJ3(MNN7MMy(bI@gaQf^@V?wJtGsbL%4M5R&;zEc_v)*(HX?cU?rrAz%NT<PrnkDTptYg6PUw&V0`D3x&5w!w-{aR10>Lx-$)3Ov8rVk;s5_Zq7$Vkz8i+y~FVD_XAlf(T_!mJQgM5_f~R@X5!vxChv`ADm`TBj{M=_j~||V`f#|&JO`vpBx3~BcrJUl2ZpAP1Di93r=|}ovx{a|pc=gjth+&9;O;ml(z3V$96DvKitr$p^}}(n0^$gyF%bHy7n}&J==+8v-FN!KeFGov3-p;_UymZzYx16y*WD?t`QnHXs{R<EMqgm3JNlFF%tuckP}&Ft%KSAJo?yUd2&H?P?W;_)O{l(Mt(P$mL7SNC!i#wd%1o6QVU9jDYT5v71SpQW>$t{2b5y6z@FK7=4mz33gxC0SD3Yn(`AZxJ29|d|Ex;93{*nVgVaw@O7O0rz8R;y~3+Zx-!F{Sc6inFOSL2g-lvSK|iNO-nX<KS2FLa6W&Z+X!H^iP@SbKKevu8IuVg%RYD8VE#@Chx6MLWu*%8qV?5FVuT>Op<kGUjsN-7t(k1^~-k?;r!cR~&rpyhq%sbn;`jE6^@*vgtQ`GNp9(&~)?JE+Kp^kppaFm)LB(iTQfLNXXMR5ttE(nD^lP<nchq77-oWQpJ|RF(s1Nly`D@%ig`&9cfX+#mo2L@RA3ImwD7&Wg8Z;)6Ivm*?gETvN^)UGu{~SInhZHN12q_A^jrB(#dGyIQ){y(_t!nC#&+^rS1t)8}1M_B!7*VN!|gDcYq@da5Vjx7*w&+bVP*12%~)ldZ&QdLn*q_l<xS(XMt~wOow`l;b=u96`rf;$RFx_{?K&f4<WV!N{89^beMMp<JA$2&2Ypx!lI)uEIRYZnR2NXTt{DMkc)1=EtY7+OK}Bf@nD!vYZL*v1u=oAyI|4N1q*yDE8ymr^_Kw6FQ9K6n~9@x$OGwx)(V7}f}Mr~0u(}H1wuf<OaldrLpu;FEw>zW+L-nPtF)9cgQ&Q5g|0V(Y&G4k@PHp+)?fj#ZKwpX@wU~;TWJ9I4H3rVi7-a(AemOiRC<=#=~3piD~uI{DFc%ye<?dK4zck>hEB^Cfvvxx0)svV!el=Mnk=~3Vu9X%1s1KBRity`{ULx81y(S|Js%3(EKb}U@lF@J9lBV+kE0M*TqcYK-Z>vwH(|$fde<;Az!V5D%$_kO?3u-!jxBbIrv1yF(9&YVxJ(-%#_;Mihbsc0aH7wdh(6~*B9J3dM#-9<XE@W~u+T;itT=;y$+gbP5;ShAv*;<hP94s?#H#Wwv+ik`d2quic(fu{iBNn6L?qVv+wj)x8pdNX_ArJ|reO&3lslrwTBOw{51$JZ2l}L>AeWiA@+*)Z26tER$mD&$f$yIIfH_wLAUHgZo_?TAP>PdYSP>cM!n}~fdVI=YveE;_?ufJ)KICXP(AYe8D5b{E9-Wd-*0v!#<(kLz_ClC7i>1<OkPP1>jKLF5Cw!Z2uVr$;#OwV1{1iNxw6kZc#FBs*FN5!H1y8Ua&w>#)Uy1}lo`@%pPy7ksENCyNI%bf~!H*w%J*WAkQ%}WxA-j6AXQe3fL|_7`KRO_reX}d{)=1e1Z5+FD2^e&%JT2;;Mn!I>H$FtH;q%B}*HGFsMn+vtQ)!?|bNHY{A4O$PTzb}c<b|}^E`eLw%3&z51X`KSy@@GN6<uY|ozNVN>`prqrd>fiZW0?Iq&#f81e$X~;Cxvga2!jgxx9`*m0*{^H*(@<Qpq!u((+onCsKCM4-A(aJ~KoKbbBEy)Gq^-P;hX*SeO`i6%x+?kp)tY)`=3^Iz4KqaGa>BK`AZeY_J*Z!RBJDscb{CgF9CoGo`jSQgU$6g2$;!8~x9xatF4?9*@0FUs}=D!=*ix2Wu=y9%DfP8x+zM5&mZNfg<qD@^it<>;jdo*7Ss)gw2y(-t9cCcWUqt3ue7<PT0zEd%QtYcy;Z2+Us@6Dx`+ChN0F|zf?d3tQFoHUN!LLh7k^f2g1mQ(|37r6G=y#%ImMRSE@VQX@h=;h=U_+YaJWC%!j<pv2PqC)mK{9F&yDhyPDtwUk-^jGbM+aN$rHs&3L`TTuQojg>I{zKg~}UZ6`bLD)hWK%rA`|*bfJYd^!&LG1JfE&7(f=>N!8>p59LxdIy56zUGlM@`r+c1?n{VtQ{Uh8SI(gf7yTk-{1c~N|8zL')))

_TASK_ACTIONS=json.loads(zlib.decompress(base64.b85decode('c-rk<+m0Mpa{QNho(E0$a7g-Xmg*IWr8ELB+gJ;PAi!%FFxC&U-wgk|xifvKs*H??%sNd<_5uRb=xJ7+`^k)qjQr`pum1IyU;p;kU$6e@r>h_D-@m{5bba-2zx>C){O9K{K7ah%FTei#U;pd#=bx_r@bND{-~aID`}?<7*H^C|_E*<8pRS+2{_)+zw;x}9`279;_3r-j|DS#O^gq|LN56UXr;k5Q{$cWx_q(@m&yRV0!Rt5gc30v9Y1`@R_pf)m&n?(4oA!r~Z{B|U^XI;Q`1ts=Q_Ci;KK$Fqhw?AaFOR?DU0sgY+xu6$!vklH+V9?fc<l7)!w(PdKD?fMC5IHw*-biUhaYTb%~-y4){e!P#)YKc{>R<!+j+;A6E%I|`O|USo<@DtSRDE|T^sZFT%-0KHq=j7ukP_My#ISAudlw}y?yxM>U!h1Cyvh3E3Q$)7At1j4B5^14<DD)9Q%ou9qOL!#B#~q;JJO;6Q{qB4jo1%8K)mUoLaYd(c{FG25Pb&?mz6_@mG|GYWbweiw~oSTcF-|80YZ5;}g)i6MGf@^z>M7^UYflZ;r*K<c{>=Z>r}v`hBFo<$*R{7oKSkaPM`=qv1DbQ2hZ6&zXOUhloCf&;R^<P|ePZbhNS^c5LJ&hluSiG&J!z3XeQ?A0FN06FK89@W@vWZ{O}-efas0yLTVnynXY}^HG?u=G@$y{kM3-x9=W)Oh%TONsFf(e+o~X(+xtbtw{$LRxG^V!}-exDzu?=$%A<Xohyu19P`+`(>JJR<k?G$U^9OY8m9E?-Tk34PanLA^X3aInDf3ky?1($JQ_0dw<)W@umZtLPey1QN`C}ILqPX&7q8hLjtxaOLEP!UdOY<se0ch??C%Emw_uo~kw8XmY@*j|^!!q{JC<ek24*0~D~_}iU2xaV^}ky#a%RI<`o4S)v@u(wkUZr&^rm)%XA8=5lYq?@=O`LKs+rDXnUzzpmD2}z4V=?+hM7#QCyue0m@(Bipzv4HT!=n7*lf{ouu!hWg<5bWC939hExzGw_uLcEDts~!v(2XwrcxYd=$pyC#E>Ipj-_Ki1~*i%&ql@@2ji9kMp^7TUjl~l1I(%ox3{uCKm?-Ib8h+o--V$8Xpi4647T?l-rev2uzUCJFBXW)4xVLO3`~i?J=y{%1B=-)KE^~}|N8#jpL6>uHsJhwey92^I2sU>9|>cQd~h}i7;$9Qg%1<VyM=ebp^G1;KRbP1Yow)S+icYF*Hu{0czf;WY`()bn|sfX(>Z>UY`<#gBDfp|cnzT00?M-;9UxwO@EuEF1u9EQ2Vo=JN5WKbnP>NQB@VnDb#XGodA-R_1}2#XaKaa$%xG7g|FJR{O>=(n#=}#!y_!z@xn0qO*Y9T-BG{JHY=`E70V~qQXAjUBu1XEtXxlj#F9ml!r&wOMtB1*iU^laoqEV++#vVau!48F{P-gKOxGlFsM_!@pT!QE@bsLZ^<)2o)6Zk-1$Z#wS_h?HMm@9+cL4m)@JHS!nf$IJ%kRdnLUPZC{&KrbVIoAGWaSaOft^)U6o11#B!sfm;ZSKwQ!{+u4Nqk+eH?cPrGur($&X7h=A8OeWj^cUi$1pXsCaWxo#FCy|GAa~Zu%x4*3JwGVajZ|Sjd?E!scy7zjj^uJ_F|+VnKTOuH$Wr}R+NYbR-6;g^0q-O*oe**7_Q6{HYTuV8(8q{8skG!8omS=_mAiQ|9Jj>D58(7yf0%*{sveIZU|i84d}!i6#S?8GSs>q$8m_qcE%934a@>0o6|nmk#A4Ow(<jjon<76^vuYU=_>8#ig^<!Fp>t&F9iOj?k{4Gtsn^?q+kVsL+@c=C7j&|7yC6Z#SVP{_%jP%XT*ygGiJ#;xu8XB813sKyG8`D^@4&uycSiw2wAdb3^;E9wDI|$#`oYK_T<;)HxxF3#XANbe}xMWuK!CA0DK$swnn7Fj5qWpvC9fnf*T_d%rpF0NWYN+1j2aNFj@8dY5Gt0P6%-S@bLM6cZvvmgUu<B^d#*!)8;D?WlzskRxS!U9|qnuGmZmxSnO}_fB5!Fdl090gdFpAoYI)s&GMme7ZTM6fK|TGkT_6r$bi)2FXITLe*tS}avS1*)>}xE6SzE4pp~_GinCJAZj1^8fRh50HYQ)GV0mfeJu^LG-%Gs$J?Lk04Lfpr(~xA`8yG$tbE7Y;ch>07`tsew!}}c)csVp~jXRmm50f5=c~PBw&+H02_m=Jtyai^956E@|`Gj=4^fyVe=2j8FmR*YrEd2$#hm7rXk#2yUUEDlgB<X_9EU?S*Jb@m#Eqz+huO33a+G%{)wnf89bSk`T(#K`=v}MH+Gr1B91BfgKHkQ^_qB8|=Ox3t`P2#2^nYXMDg-l?e{(<jbLZ`>PO4=G<hbm7f_Er$WUsP{=fCD+7U;$a_0yS)_5`nrDgiy9TKy;)KRM_EMLb}ea+*|o-4YD@^S=k=g)^zD)o~!b$bITU=Zng6-vt%_V%^<7M2v#jHAYB-vIp`W&EN9=c)QBBj^esPl8JMU+82u<yq-^T66p3l639I*k1fhM53krG>v6Pjkibs$H6Ay{fC~>B%NC)EK=QqWW`<ioNx#*4f?Y5M4t8;YV(7`i#J0J6NQj3g6dN!vQT;AdoESR5cFGk{ooktK2RQxL$v85?pbsYkk6g!A`$j;kl858IQs?#aJai}E~*`Q;#(X+W4(>0vT&<$eMX&jr(47K;{ME^$bNo3iGZ<ls+>75<rAm^1t4tOwUFu)ca8g1|0=DC^E3|efZn%CIQkO7h2uj)vC|K{zV9z$Q;g@hExG4ABC$ETL4==qKG-fmmAu3^B(4plgT!01u~hXdKz6eMjM$NX#rmKoMt$%O$V(Zo9m_AAoOq=?}9JRu;1ldY;#ES$=2TRKLQO=QHeXcBrf`#_{_dQ9a~0aEp;xfmmfAX;oP{S1w8+e>90pKOVvx-LxY;v#Kfgt?MeaYKV!Ska>E(Qnk;%7smpjg8muNITXnJu4`^QOcGR=f&SA-cs!9Cq@g8-Wx0|VqSZjO8f}<71=7_Hf14wAvOr=fyJRiM(T_bM->XJ8N|$gDC>G{sjI>s!RD>3g}|Iu#5~m{2g=QJ<cCRk?c5Z!)K*d5smDWeG<)e@?G`Zfw4_~NoJ8LH$IJYd9nsz#cr@t{F&W8~78a{Xl+G>Ht@fXQ<sN=d(+~B`Vj{El;NXwUE*k0YPdwNy-UMx;cXSzva{j3agiRcc>@#C|hu?)ojZ_y<iLF^XZ%qK#cNQa<%#d&tsbE3r`t_;#2Fm@HdMlaTHtoBJ@zg*Uz-gwSHsHg%q9)E7Pg$rd7gd3Is?_g56mr^F3a?~!>XzN!nB7M9CTi5uRg8-YbK52HR&Oj8>gmq5-iiG7m%9&Ikl+(Kyq)$N?BfIP(kqIE-1)_0u+QUdQbu-7sJb5>zQ6zQP^$EJ<aM&4hQ8+cA09{M@OI^?G^dZ~u;Y^eoUNSSfba!T<5JFpE%LyNY#6JtMwH=<6n@Q=r!M0(*Cv6E!({CdysbZvJ}Y{00s!xfRtTUV-RN!*&4jqUy`#|N6498%X6Qu80*L&!VN80k`e+)QU!yFsMK=C{0vJpDeokCMx-^%Ix_mTv*qu|Ml2o{`&Y2NS=j+EP=9!#mu_Nv!YIE>ehBcP}HFpoQ$2$d^L7XtxjcEf?E?Z){ckeEqzW;)gDYjG`>NX`Jz%Nq_>ekQhcPe&G{u@%tJ>oA6NZMO)49I~LM|-=zB12yy#$-Zc9%<yKwi2iB#Z$P0-#N9mN2tyNUy`oiOA=~4n9=qj!E-4kW`s`hS2$J&+#;{6=eeN)1DU=_Md7EvrKi5q-T&mv`>MrFl3QJGtHfQl*+^iWtMrN!;CTMG0E2Yxz#}#2P-pkihy^S|3Qk3O`7<jt6S04$Jhwc~pCwsT)7H^wwgO^Lgu-hNll(k`?;bi>Y~&@Kei_WE>G!8S6(by6xsUKM4h!MV1GUmF^Ar+w5Q6m_31`!J237!gn7RD%T2GwU!wA^5ieNkrz$xJ5WP4&Z7#ZCF#>;>&3JyJB(aZUC)?kapf!E+&t1c!0>+(wX3;ZYrl=I7_6Jtx)Sp*?ZzcQvL_B_PVW<b;88*mNf?HO>?<oG!QQ(y#x#8aaefu6O*5nX;yws6-(3R0>MSQB7{+KWTv8U_;PBzR$H%6VZfdREar5G@QMB0G2ErZ+An5B4%E!Hva?LIkKVx+54BzBzl-P+W-80swSziZfNXT!2>REh2yWxP>ZHw7yml$W2dj<GEkF($6fOdV6t<?ygbk;xf=2&wrlfZQLZTSv9#U`liwGr>dEjK?=!poQ!rhwJY+Y1Qm$=0vAG|0+FB9#G%JAYVftMX9!MI%~yjE|H<+qYO<{2Vp3;ob|Wi$SLK6A$S<xmwIG18!I4x5R;pQ&F&k1qfhxR42peO2Q@<g#0&HT`)GbKNL>*ym?y33ON|g^b$)Q5~PtG8uK(i`hNb4sPDG$xpr2bSmVD#BQN)5>HH%aaRi*r7=yr(tuD}n6@#()r!`9F@?i?Dj-2tQlSNQ)ilWT_?x&;sQgr((k+&Y|Kg+QyVklgAC{wQ}w)+6Ja`B0gb%77fTH+(Uq=@jDNVDOzRA1G}|wFf6m_!!ivryGu{uj+=Xt^tK9Ef2UPCokglUPHzzJJUhEXM&FX{W$vmjy)mmV-YI)tjlF>Vr{Z948L6ezL=G;Yvr`sY@9F(8H5!Al&wgDc9ZrGaad8ZWdg7Ta-xMs|l=92T?liKd<G4?kkyW#s@NiANp;NPW-+h-rESFWBwLv$(NU@iwd9Vs!Ou9Tp;chRbEd-eWOur__*rb4|0ll%YxdqE%n~c}9&RBr86zzVS7(zWGRaRu`*;0Olti!`)0tw^Khu46aSO9&Tl+9rb$0{4o@KKpD4ZzCEY%+x!Pqn1rD<X8!PHrjC*=lT4Wv#iTl6oZus6<e#da7DQkU1~X&8R}t{oS(Mnwx}V0^>Y6i0Ls}oNPJa3uG^r>n34yUZTM3^i^?p;D(qEVVslb-<J*`AljAtWCC=ec3M)EU^0tkXT>M}`M7Ha;27-ZHNL0b5<2eWf`inv25XLC4<pd47@AW4H2%Bot3jZpungP4RZ^^IvCD82$f1A~cj~a7Qh>{I?aiH(4o{gnw2~|aB=NmO1AtP(4aSBo;tmumFeNSWyTJ@G&?5%87s;IWxL<6y(QE{o17aMzU{d1Dj!3a|;a)bZV^&xNvk^jC#BgTBurxSX0nI?Wp}G$=aOvuz8gXfYW{#Wzs3i0zLIoTU10)4gT8{jcMij==*uIcpHxc0I(bu>bwt1@^IzM%I?=ncu<?=aBG$HDc58Y}uiacQ{ux+eeW?YHUOCmrbyw?kaIG^3~H7IYs0zJ0f6sA&Oz>(6)f>Nc@K6CDkRdA%cj{s<kNifI|nP!~i;d>u2=~3Te%b`99^F?_wbO7H_RJ-D+6te+n2ECb;Tq8pHsm?~GV=!aDzXqG9zRUrCBOvU?xj-9=jb91yH?X}r5{%CCjKAPve{tCA(3t~-d*OMc*5XR%AW(2P4Cn{Ggd<J^$HY5JdsG2b5Jh~tw>c+)yWDfYI=f#a)y}W6!hMOnIi~iut^hp(x6Bxouv~nJ`C^c8zXI(J(*G2oK%>g}M4Q?42hE=@qX))h(24>X^Ewvh7*H&C101j+HUoD%JjMWYvQrh)hobw1pc}VpSs@B+ybp`Q(42chNatccb<(MTf>O?N?heSbA9~TjVP6!IU_F@9q#j-IsZdJF#KeO1<s?jAW`&llV29JO+0U1KbNV68?3W2q>h4k)7}Hsk_0fbZ2i;Aw;?@?dmF=KxPEJD#h5QhFfuqGf$xP@0pucJ`_D+Klj2VOP%gn3s3+?q0uX^n-on;zlm(;0%wggQ<!)4<%HBR|EBI6@ZqunN|M=Ya_q@t-M=T*Q9swtCAFD-Cm6`Cpd=*;nQCF9NlS&L`Gj?z0Dsx#9eh^eOuf)JPH{4Bj~$CS?mTwB!$pghbz;n}3r!gY7#O+(-ysT0}_i}(c%)vFvE=2qG;UQh_itKkb06gv&jvWrjV(s3lf<HL{y{G+m;NR6!Nsx%`$aKN#aL3H<9H7W~`rJ29OTxctaT$v{hB@jdkRwsH|x(*o7<IEj47Af{S0t+BXw+KbfIrgO_jMa4v2|<~Y^*tcnp^McMoG0fe1=gAZgH&T#BE=L<1qW*#HKBw%J*cb-DVShaz!{q6xkz<)1WVyG!MgRy&brZTR4Mu$ptT9^iKT>~J5Z@H4v()KF>^sAMOUtJt4^lPc4?x$h-Ui>6DX9GYYDxON(Sg4Q%b~M^!KiU)JQZfOVfPu^%!MahN!swF)mJBt_%A9^=|j0<>H=B?vuY4eb2ta)(}qE{L4evZU{Z>g+an34u$#tu0T95f3SS{jYq6%>pU%ePoFFX6Bxy7DrHRwSBz;$snZ(g2St}vH?XdQ1|2qvsdvHA0(FM$goWVqv>2vPDa!VQun#4TtzK>7h(<o`+XSR@g`3iXxjkhs!of?tg6y6F*@0pSmRhWysyHvqlTCW6-n3YfMWr%vwz*6R=EuYJzgUe;!U0&p+}+~EJzB>zjOohb%I6cAIT3}82y^3SOD<k3*r}qD;=Vd^jM9}64-r`}P)OurPu(a_v}%|txOB|W`N(-elz#%VH!4IXOIeQy!NNERJYA4C?U~7E;Qe~wR8jJ>1N?|(+LU>-ST|NBY#|8CqF*gw!&$xRhDxG51hF1-D&+>BM#m{sYnmFhfRl%S6{RvQ3kU6iMY^94Fl9pTQhh2LRQD4&aMS%Wpthxh5#9XO7*~0QVWq;ONw~6vyJjL#7w2JZD?BV#5c49;tL-J2R~5``7452=FgcorwblLNOsvKXwFp-_n^*UZaR%0KlxhMV78R>Q^LF5@0^CsFXmG4)eO9HzOL%vd_-@e2EKpaPoFeXvYMMke%kwlt#sPoka>{J5ZeLHn_KZY%@Dd*>*A*6q6Ev^IrRML-D2%BhaVe3Q(-9~s!kh?;4zMy~2w${#ytN#4ZUdXKjT!(2<??cpTE6Mcn7?~5AwJ<uqG5RoHmla{JSv+7UxD+aBdB<BMJnifF-aOf5{DdrLUVVqueCGp74LLqp*5eQL8}?Tn&S#eDs>SNH}ev#3f!|y6IK~kp(+#X8<apTiFn!>*_n_|AM*n+g-z7tRaB^&zz~F)K*r3u!TmGvo(kGfyBMr0O<7y*EK{BYNlTzV;vrV5<F{|VvqFuOORAJ8ti<*Cna@q!o8{Eq^(5GQHX^qX*JNs!)yig~C^s2+xcSPOWj%&j2{c3y;R+~lDA|lJ|JC#|DLM9H1%Yg%vz<WpKTGJgFPFhIF@VwL`EARb%#uyu>C#nH3>`jMq!l<vEoMB1XF7o9^=d`3cGXYA*Y%>ZE&P}rNc|+nXh17FNK`1bl*NY-*dj`<F3RvTiulRY59p?XZJ9A~aMe$Af;e0rbRn%2HB<3do-{)B{hN&G8Yj<Ve%5M{6iT6a)F@UmXK5-cvzOY;<~Au1V?)LpFV5;|yF;K0<kmrZhwWZ_gIupKUMYPtTGOnQu*)Q!Rrh=9-F5i^i>0KLc{*f36L75hZj@03iDyq+*)t1=7gZH{T0$!*Ox&?AY)UIJj1BgtdW#cKr*eXL5kH4qu}Fy<J7sH%PB337!?U`n#WtnQg`;HZo(f4_s!{=y?zh$Ktc1{Z$~0ZrZ3#^wNVe0F;us(Sl{B|KEk55};n9=h@pgK};}-?$kW0y%p=X(A`#V=bTMe%Pp5B+?-fddkJ3lY2&%Qej(>Gz5HlJ2IMbKMQ#lw`((-uRcjKUGp{}qN-HG8!{d;q|Vn}9`G<F>Yz#WSGp#QH?Ugcy`XT&ewPZoi>;0&xGlteV_FT}1^Nw|M}rAd58F_;s&3!%C8vZA+6(XeWIlVhsuS-q<e+18S$VHRRQbKy(6~!d%1H<_4pa9u_P&X=wE}lhr~jaA!(63e@UC;_q@1FI<##Sr^6!cr5tNDUGI1tmq49W2hwRVH_MCNHU}F96C`2=xADTe5gf~<Fpsd8+7mzcCfJ$NhL}gtp&*iYI^8{K*bfAmxcq1F8q9twc$CUEMKZ=;?jOj1{fF@M=`ax;~Ze+Nc1@DqlwM9#2=V9zDcV9r<|ssN*_`H*Oo^BZeM<x^HdGA#F3SE|86%#4v|-0=4T^l7hHa6xPx4G+sfXebwA9g{c#n>3;XFw6q$&H0;X8SF${y~g891a<~hV74pJ&Mfi7|_t0J0(Y2rv|z!{0MTwG-BeM#K0p%-V-#kP2B@oRapB4^7q+L_hjtT<!wwnGE7tB|&B(z?*xSvl@<q(D-WbZ;jQb6Vi#wd1;FM^{&r&5GDoNllUQ6U8#*NtzKLFh2-f=nJlSK}Af>PrkOs(fBB<s#dr$uU)~@0!+qi7cm`|G7t0K{q!K1z6-;`{u)A}RTYGaiUM~Cew)4!k(P+@(2){fxxsFgnoA~LVAnq7%gRvnDnUkFrUlz)H8jzpmZ)OPJW6!AiVs;_s7}GKG^^Ke3Rmn^v;Ki~Veyorio(Hd=DMw|KT0z7(zWa7>Mbt%izhNmLB;)&A1DPL-P(oR<{Y6sm<@MM7<5je6CP$L0TPgF%zhM{Hg<l(YS+$om1@CFtSgYoU1`+4uMI(^%yfEEAyNJ~UOGm_Sm%^GK@TNW1!$1`gTAjJsO;9C6{O`A_gy8n0S5Yb3gmUA)Vc%v&<VRePS|sByWI%@Gn3J;Qp<Ueju%GAM~0(bZmQ5Kr12$&LB9;dDAC01Z0pu@jS2A~pu0X>m=P9F$RYTVVJFxb#GJ-xVud-Qar>#ul&d8hZzXjGF@elP7@CATtXQgFWFjm4rqd)0(AkF?ZH67eNiIn5k`UxgKN%U6gcPf|Nb9n)l^bH2(>>IJDhQP9D`MD&kj5;<rm88Nl_(4-A9*L`oJn7(kp<$I7*ORKrmX(fNopVByD|1_A!1ajt&k4tnyjSS5|tcjphe}MJw>!A<GO}Z!N-|d9T9_(4}r^ukS?J}7H~-ka_wYpSd*?hBn28AIFZg|Rx#kmd{@pT;b-wPj+X|N8{De>blEgtNC?YM2|u!C78x19IJP61qDA5q$<W2_#e`hzF3?D_bR1<n2KN-@Q9T|Z!V{`xQwT~~P~NB@l`;m}ukzu5m3~|`Amc0#*(~zWJ7_eX?}4uS0?JZQyxbVU3$nKgr=1&&S*Vi|sQ3=-otFZ7r0hVMAfDY^2w^-<JW6YmQ8>wzd<oAIHJ3i2@4~1fKEs`gCLZB&-&4DZl+)EnB(VD;(`;mwTqiffgCD0~PWMd#n9P+;pLz_Hv^<g{;<$TOsfRf}88Ejg=D1ae|E7sJjwqnfP(<{|MFm?lqF1(;D$42>ixsR^uX2Rz#4vmMKjfxu(OyL@_3JiNsaQxc&AT9?Ol=B#8xPg%(&Wt0QSLSXAlE7fyc*7fbkTx{nzUV%A|g9yI@l#;(i#e^wmOb~?5?fxBX*ajkLJwt9LykR4;av43Ew=~i`9=QNvdgmh<*km6$&T?0BF8h8N_XvxSJY#_^vIeN6AyP<gku5m%^w7-I5Y^9DSuiAgzL}89?fA1@n#1vmI$=lMZu>vLo3vqvin!#Hy4f;r^`wTxQbXB;7XyyU})lx}N?;4RCEM2lKf(kF2IG$OKWwy?GC?^;pk04_PUb!J?|O;ArqfP#F!kRuInu>I%BcoCk>labWY+7oFH`wF>n#tDFAOJ2rU|{q!_^Y11N?D8f_bwO`YU;@PKC&jb(CmPw&LiljLnmoplSC+O%m$Z~WUa8?3!1zH_LYZN++z7}3eV9de7?I+20ea=$+3*{L)+(xBU*^$e$pys5K@-W_FrIG*@{K~SIFGE(;ju8is))y>k0g2;CjA|Wnm%Xq`jm)(d{Zc7nyg{vC6e#s1`0|M8aQ;|h|J4$nnFEACocwIL?Zdm!%F?{pSYMJd)dV51v22y2c0E$rykJ^WUS#w$CgwYX+veIKU7}}&3B>0!-4UiN`heVSC5g}66DOh6?{znK6f8b2*T*SyLbMp1J9OsjbP`FauuDu>ol8o*gm~}>W)Jg&-4bB5c8gK1a+Ox(rdo?0vZcqMy2}wM*vuBQR?>?rbu+Bl9Twp7qYmCVU6mCSc^G_MB89eOS@tTvkbtVkydt;m((CAIAXIbZJunKmXrfwKf%0#9L3l^<b42Ya=6cd3^yPdL!10b&&7e0Ly9tE0xLqSK6?{MvnMV1GXUi$OEzl&bO4UL+8d&|{);z;YC)^U9U&lYj(Qsv0<^Yw^y>&3>SCoeIs|Rz9$WBK0=sM5j1CeC7jGm(baVq&AxE6g0NcLf^MB-Nxfm~f^qfy+#B0`pQANS<YW0^&Q4xg4zxlCc(x*((_G1AVu_Rshh48n<uV5xN&i-8Sl)U~y-RjY=w=$)Vmj;u)C1nOPQaaI}H%4N;4#9Gl!wyy$7&n`e!v8D$UkH$$ht=_``fTC2f<UF`AJiZk~#|LRqwKOyLjml7D<&${bDvlo$UNkVGJ(ZKEfS7gjsf}Bf9rQ6IaOhaEo{@XB2(GkhqLL~^5;-@7VTXdVf^;vA4OupfW&i4x7SdE@f-S(bXn2DN6^*T5W7QdQWRuk3^D{Ij@|EzB;rZztlHCV<mBF<V1{7%ex@>He;3YHGtk5t?-!`HG1Hfdw;EbSjUfIf(8zzNfiufeEp5Z-A0tqxTja?B-w9ZdFew<B^nuc^HZ(SHg;O(G3n^%?e1Vv^w?iaswaiYgT*g7fRZvE^@HtYPgU#MpGZ3+!*HOb3V$X;6yd!u-mr<LRKF#9~ValFi!9yI+&cLp)jE+F7T)18a~B|>D%O**m>ECVrx7pobVMNBs{C~EepUB#J6kq~i@>E>9YFec9T+StJ$o04p4Wa()!ILGx?3ji1-svt~KdT5P+E4s1QGN3`eG%tUH+_nU;=peNya)lG4q1TL6BS{|Bn)Q`|BzaCUks)jzO;IW*i+_{y$AlP((rymUo!(YdWeHGB8mU*@<@LB2cl~6s6%xiYUx212HI{1d$7^g}>hMLwU+J0a6Voq{-d4?&IFCXWkNsB321bFLe9pG*C_zPfjzO)y&RRjCk*FP=muhcevZd2a1NOLpI$v`|z`zu26ltfNlK`;WwZfuSQo*KxoB@1GE^nH9Y?ir_r|XOUl4WO-I$g8|rNVuiSw4WQ=Ap`<t`cE5=&~wVpxs)SCEOFr&~XV*Uxk>4hSp0`QmuA2NfF^w2_gmERC1#q(Yoi6c3G+K#`QRORU5{xO#E6oF*g-R%ufEEAd~;6c#>8w_@wmBS0qX%a(ioGy9(}z^jih;IEXB{Hb44z!H`tGcqs+b)Q)r#A@)5QB?lR)DN+}atTDdGwrnsdCG5DalCY^1dDG7Wcgk-o>(DI4+Aa}%nTqv9`m+K_^77t8rfpw`&Y3PBNLWwMCBavBH>O8vBE(BU?<J}HlEP(iwGZ=x#37%r;2?&*CuPVQD5jP~A0`!9DrMmM#;#jhs!G&XOXR#Y&Z7iWg)&*Eve5+5$;IPP_1_7qrvk#V)O9C6ZbcFDN)3%b7iDltLGMwhf{dc`?Fm>ZDyJ2zu{-sPY~Gz*F^E6Tx{%|kOgU{i!;-MY^Mfc+$t(Kn6u{k<D>2t<>zunGOKI<<;NnI0JQKb&$DRc(Xvr6+IEuq*4f(x2?HEEbuq##aPend&0?KoSjxXuUdPn1)ME3KHz%O>1L$>mz!X>g<sPkBf&mj&(?GXPu`PFkm-?mI&EELNuAcfmR)N3u7aXX64C=csu4eUC{b9%Pjw!I1;=InxRzU-zOpP*>Krd1_E>0`3<9918fF|{OKxLL0>=qpR+G!BQDYrW6p_b2`q0ZY5MuzBUWH9#Bn2!ORRQ%UG$a|^gz)%++57%m?-OrfhNc^CJYfW^6xm6f3%U6qy9Pe8OcI+aYgUEx6>Ej}S0(sGblL8(-Lp~hQdr*l`|gZW(?cp~%&&!|PpC)10608USX-}^?XqhwVKR26g;EKOa(T0%iY?o~GmVLU%;k(R4g(L8klS|@XT3-<^r=-NG*)0AL?3Bt=WepEdp!F#2u`J8RyaAq%1gIB4txS7_1BV`49hL{0dV9!CvQ%K2(3CU1`s(k>`5N~=2G^a-fyT}XsWTkmjJTgtvET0ca;s~t)ZC5p^)tn-F4TKe*Tu`bU5W{aPC@hhj^;3f?s;J(=*t!{o=nTswj`3QB6{(4OBqe)NT;T;v-ahs`%hZ0R%imCBfd*(!+1a#@u9PNDSMy42Bi`fFQTXhuR@mOwfH<?%_Tn4PQQ3~JrES;dU4i17qa#uw8zr&h2U=xN;y>YNHf)xQSHkYPw<cxVCN`ET+*Hev3;Q@FELI2_BMMhnubbBFt|7|irKTx2%_SN()j(@&*e?nsWcL%KqOqR$HX)pPuJn&}tbD?k?`0O|E`bOC%lKBK>NU13QW_(44J4;!?`5^}*}ky;QUSnZ{Zgeyn_HR~I=N!tvJ@X&Gd_pwXgq9-M6|l@Fv#DssFJkV&pMU<Oh5;nIi3Uw5t1qFSKyEm7#*F94Z@S8NGIA-n@VA*f*dIyXy<~Uf;=VoT-URT%vpu17XS)nxOnO4aSfT`3&lKkx-%(O!RvYR_-gDFHI)m6-jmzYjdBst6W}SCRZQdFfzOlZK=5Q`e87v6!5HE?q9y5FQBzsDEx<sYpi^e%nsz6wd0!1|(ydS>ucZOf%M;o**0I^8m2|3wY>V22P6#q(u?cpnS&TkOaD|u}T?n@hF=Bw9IXZoGb@t)<L|IyeTZsTl0j@pGxa$k(jU7+rnCl!Z!cUGNJ6=h|3L&8>@`>Ut1~XSnFI9LcCdFlUvmyTm{$Uf9^eehn)Hba<Gd<Cy_`EQzYG)KTiriWtRUIcI?FiWMl?orOg|;z#Z6+Qq!~#U^JH4vxO!PWlplc9Q2gFWcGg1wo7qcjZ91rkD_LXwFra|V@H`xkO>zl!Q@~|}cr+1(OmddsXL8+R!!TX@Au3ib(rv-rx3L#3*K{xo_H@6jz1AFb>KoRmxXr-m8SV_V$HS@x3y%{ohWL<nCs(XThN7S#S5Cr6!^Q)Twbuo*AYIWVS<-nBXyxyeoAQj4F!)JkWMsSFShMDmzu3%Yt0<4@{&o@1h^pDVzGWJs(f;`E%b8ntI9HnQ43KK8N<n&!$+Lp8VOimYJ2Oy@_S-w=<AvT{WsC9iAHMb$2vR!wAF1BDbA#8NAr@DaF{H(qvf7sjEsMJSy2wkL1%Vq`bQJomH^f|TFZH%A_`Sux3qCBAR(BtH^@hO`3(-muVMXO4&c)xBerz&#vcLhFK3<5`6Hl>p_fgluRw8?1X(yA>ywXAs_iFRw8ViZ*<M?heHKDY0`mSD*ObU}_!igK0+`JiENHzK=+HLQ^vAStnGrp|U&p=gW~{F({9HM|?vS0*6i*SPfLDI$#^MN_OM+bbn1Q+NS*H1GxWY$k{y?|;x#!li9iaA|eR8)39KPL7T0GjTYPoQJd`zj4-FB-fWcEYMX``<M0)0W@e5=aNl&CQpqdA3&E*AJTrap1l-4G&<QX(XmdSb3pBx>%he9rIn4%K8UI-qC~~lZ{^?dlTZH(fc@qN')))

_TASK_RESCUE=False

# Keep demonstrated market commitments while repairing physical prerequisites.
_TASK_PARENT=intent_agent
_TASK_PROXY=make_agent({0:_TASK_ACTIONS})
_TASK_REPORT={'errors':0,'late_input_requests':0}

def task_market_agent(obs,configuration=None):
    if int(obs['step'])==0:
        for key in _TASK_REPORT:_TASK_REPORT[key]=0
    physical=_TASK_PARENT(obs,configuration)
    scheduled=_TASK_PROXY(obs,configuration)
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
