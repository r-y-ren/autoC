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

# Modified 2026-09-22: public DSM episode 111910412 action data.
# This is an imitation experiment, not the author's private decision algorithm.
import base64, zlib, json
_DEMO_TAPE = json.loads(zlib.decompress(base64.b85decode('c%0o`U5{K>Zu~Fv+z+c6IriplR+_bh9eWIow8lm-3<KF9K(Kjm@)qR3N1o}veeYqhs>pj<wgW7%?QYGz=Y!-Si$$J~|8w<kKmGiVzyEyo&mXV8yM27T`r&Z(??3(Lzy8;!FFt+z$4@{1$KU_^)8~&@fBNvZA8)^X`_1kB)#2*Z!}nK*7e5@Hzy9vs!|M;P-hcZ3`!{#DpZ@=gAAb1X!{*U%U;X97cdI{4Uh;T%e}8_=(+l3beRp>yK9I33Uq8ONyZbbPn{jA=`tbJt^^c$C{{F+$)0UB~Mt%I-r-$+{&o7Vvj!$)5vHROscWA*rUVZ!U?){smd81F?-#xy+67S0PEso+eiQ_-G*$m|QRfpAw^Du^Goiv_5-`&05?$Nk?a4@IEG`GSY&hb@iks03<m*TK!+Q+L`w{dZPdG+Hj^E_OAb9evn?bYFW&jLNa0xiNJ?BIGJa;lFHA2uQfXNsf|O;Ao_l*AW!htK+V{EbZMxH3?)K0WW-_sal>cRlT1X|0a)S?zrKg7R98W_x1{Zr|U%8$PM`92YpgXBaUu1fv;RP4xM(p5|>w5>AuTT(){QET{9$@j+@SqFD?}juyJS<j#A7$@Lbx^|IlKqrwfpbr&;g%X#6_w`kKs4%W>h;o^=vH(_~!&@S&go6>p9dKx+1&y@{drhNQv>cWl>N1vEMjcZ39WIgiL!~Ol;tM@<t`R?8OxA$-VW&8Z?<Q*4Oei+{W`rX5Knbi)TrZ~y2BORQKa1sE~T10tqH;5m)TJvG}-uwC9g)x-;oRbW}jmaKNo)`ByK7_29@W-#WPe$vKetma)eEstWZ>QP<a@Nh|y@laUa3H||mJdxY6`R;6KQt^{<A>m8PI8^EH{t2}%d;;5-VH?JW^mZDF#)AoJmR<;?!;|z1g{6~)5$YO>d<n-mnqto-FXeQ0E0wJU|`p>M#s&IpN#W9#?`0Y0Ta`a9?*$A4vXJJiO{a|^897sEE@3r{&XRF!;7vq4M;0-P;{m{8_)ebxid`lTMw-Gjnf=85Bu?4%3OgQ2P9%9nHRJE#&c-5CtwBTAULG&sl_)e;|CJ~Uu6bXThf+W$Cf#O5KWy^uA^s--DLparFeg~G^rI*$De^tXh%|5XY0M-$O4Yyb<edVXw`%Tf>3Qdx18V%+J={d*ZKJV-R<{(x_kHTZ`SZeAQzui{=)FrN8}=6!N?N7xqbInSBB^a&JW_Y6D-R(z}^5(j>YO9DM<6|lx&^y3+x6k73-ysBC`BSOezCN*gBs>Ah2fBrVQjR4kaLi6Q$1@!04u3M);Q3!A*z18Ye1Qb2uO>3nCt+(+BP^aQ#>CGuVC}Hnv}nyzl%+vf9Um5;4QFoISXBJkwrY*y-0fl4wt)+g8MtrRyL4<4qz1`yPd0gPq+ViYu}qXt=?0!-n^Zm$;CtAH?mS`24KbNz@z*&El@0g|@SC)J!l9)*)T(<ss;ZFZUP1i!%~t&!8EV_zUU$c`Qv2C5<nD>BPR0bXr(e!4VX}*iZ%s95m3m0mHnm43of(z>1je_TIJgd{Qtf?6B<e3gZHurPs7K5~w3bCOA8gCfAQA@Dv=;C5vkKApxWUE)D>TZ7K@)rk%G(5h^)a<P}IF=HTJL#Kmc>H?WZs0M>`bdte27DFbwb#t2)#0(kQl3*-0hYJ&ll+-~^yky%?p-H|W2mL_!+Y9(RLH=O)Lu%BcZ;AxHk#{nMi`Qa!=UJfXRP|WeYJr&-^-Hk_9JV&0VTtht6l$bxSC?FkfGK`)I?gZqVVuyKrY-aL-lGa>yu!iIqcGYoYb+iF)V4BkNwFK~>9Ryoma0%EnC{i_i=pLWZjY%QdCKOgdefPeC#5Vd3lspD}%Fa8O#hA2E-gavQyz66PkCN<6hZ@Nl(;|dytsy%9(WeUQr0j9#1lBg2Bh;ns@I%iFzt72x41;sxeem|?p}6e0@)2op;P`^h$fJo{170KjPURGy6UAvBze9#&$EiaTs=M=XJ%N!x_`1YWZSWR?Nj^2G0NGM{nVu0i{XG6Qm+<aJQAe7gs5|gxHQzmooTXO}@hmei;Q|dbQ{h~2N(Vp5pR*vx6APBc1q_WsqTIk}<8xc}LM)UH;Y3Z4JzTlv?XXc-Ff}x4Ky{in?s;fn7&(IgugkvJZqh9zxSWGHNQL92%<VI{Q~qGS)=9ZaHZq{J9Uxi&vx^Q(@cV~{`(Kjf1^*rym@}_I(M!SK?uD+FM=lFfaA}T<ZW{g5avg>JQ<U~Pz~S)-UEUEo3v>vmNB}i7mQ5jP0s?`o{|~>(fCw}uQCSMm!sPtbBAqaoH2ix5Y4p{BW#+)B3_|)MEMGr7Jl>(6F{gPbm56;WKyrevE6=hQ4`d()p*@DwSuou7ItdL9e?pcY>T1eD6G5}N+(fcLWYCxJC{smYqp1H`6UcmG)qf^z!E1rDEbLvubODz=Y84W-=YRF;Asl?@lOvZqCK2I?knV{Z7{6JINR-BL`>VUNe;YXEQX$XWHR&%kF<k3)7$<|YT+HAC>&_su=ora!15E1tX{|9+ClSvbAhaO2?yWackcqN0*vM4foRMEj#K%3vwvioRtkM;kzfvw31e(PDN%B*^CuxJA-a>;^3+a?YdlD(hs6fFeZl_QUr#S4%h{=wP`!Zr}YF17<I#k=C*r5X)8nfRqDb)y=_mvueOqnVw_E(AFMQ+Zh+~Y@P<ouZcsM+UM<$g%Mhek3$B2Ri&6ABTeE@_FTiLr8OBJWP}vI+Vz{~8T+S7{ZMcxFOW!F#g|f=??Rrkb_D(j!_iVm!NcLl{*N7Ks`q6MnH<mVOj6WRL{QV{dH(U)ywVA{-5(>GhLT3E&LH00NWeb-~8bsx@YI+y>ae8bx`6#S8?-Ve5bX=T-l{RErmTc12$pm4c#HWBJc7>w_i|5}hyFq6iiF@!~??g0KjUd5dYWOUW$(+sJ}Q)Dk05Qzb7vZcJp5#mErk*Fe6oK(xw@Im%}ccQCDODs2S>Hqw}qArbrds9=Il@|ikIHC6_4N;tz44Ry%EcBu;F=$OZ60DJ+K%)fkh*XTGO_3@jx_kVdxt@3yqT6Y;Z*wOZJIhMglf=2L#cp#8Z<YhL_f*)In(S7D$e9xw~6#C9NooXVjGde50ns-m&Z9^KYO9jHoCPdagc%e{=Guc9o%38yqPlfO;*1gH@aCs|yYZ<*BXfL2Q;X`W`q>GnP_evY914}vh$%>E0Xg(G<TAVNNAqxLl5xuT2IP-fza79cKL{O68K!@l~vcwe$i57AR(PvYFVj$0eRsX?ZWGi0ZYRA)dj&T+sHn0OZ${1G*j3woED+BATBl1K-b62{l{Df`smFfG=-+@kTc%54LxAoJ{bA&WimO`9Fg+?z)!GdHx%%ND2hncXnf?Xs*+(PsQ$WI*>2?9U10|tQU@wk`oT}!Ns;q4`4Sz4*5aBOBIEQog|u^+IFHn=+al7cL}W>cleh0RK@Nz42%Qh&mxX1Eg1%<UvA2bPyau%u{c^hPk&avBQZ!SkCCmoN>WtN^%&2S)VkWu?Q|3Hj4szI#BJP6JzD&Ch|KqN){`Gx9u{W(#a|kD(j}6eAr&Hb4o8Dn;O(-W39>IyxXlCOlnga=CtaRf7<s1>kf8WR|K%X)Xu%>RRRuOTGpuoKLDRVj`^*>iL<>az>35Ega2`wIaDEz7bz;w_E8q=u5G(N{7?p;aWY}+(ATFs!0o0f+%{a=lFN)W6nB=J4_8!oSf36SCYE2r6IOO8%$E&ddH`2ESfDZ&+&<JJnY~nPFX)SqJ(;bIFw*;-Es^#)19tQBrbnKesT-E7~fx1Z5Qb*a|JQ2#7U468pl#B^t!NNrOv&?n5?ynNu-DSSOo_zG3-M78At0^Ct|I0u>P_FZp2QU_Z*jW+4Uwq7BkU7lqi%ZZ3pQ)!GOWtFdAsvL5|73l$dK@=<Q~(M_f6@>(^v^thM>eCqsGBCKjn=KBt9muz$hY*XCcQy)aUK1*y8&xgaG>CjvO7l80;}n*{vLob6*VDj-1S8GSGvv2CRmbM^&q>Iw$tyi+wUK=q8k88IWtc*5OJ@V6tZwu5RCkx=Y|QE-nYJtX}SNaq<X6s=ZZ2nlIVt2ifCm=?RTkdDxblp(_{@Gp%Tl=O@)7UZfJFs?CxA<rXUzKW(KO77YA9j_A1t9fn$3<uLOQMei18}d(p*dX}{GM+&?UG-dE8gCiEYPT#sjQ<UF(j`CJ?Rp|#4(!xY;YrQb1JL^nC{stn<>`Rw?QLQ~9AgyP(rEyUoQ2MAnL=ecjIa$LH8Tff*hYLn@@g+5aKSlU5O2_&SDuI@QGMw~$IfPj{Sc0e%_ogVLJIWMBg=i#NVN-cdjWr)HC<WaqLqzsOo_INFa^A9Mk+D~ZBI?2RI6Ttfm@Ix$1*Jp&1KNXT&c3`0pqND2u3MWr0^GJmpP3Cj0Z|0+a=BMV2cX;UzU_-t4n0BCe|pv$zw*juYle!nFGK%<&Y8Z$~Nh<d3-5@hKM|C>&xL{OZamiSqa`MUMq^i$dD?=9v)7FD9L-UmSt*pUw?gd_$to-mko&jb1|kJF|p4QVgXMDy4iW%62wX@3ba=wQv*vRwB++qwho4N)6;vfFt6xYcD^bUiurH}rRS=+_JEM2680xpd;|!|gSA71ABq9EOXraa5hW;%Qm+%qz+haA9=ui~5?Luw8VP`4U?wbA1<)g_B}w9`X4^-N0>h$B>c4_uR%XM3P&&8UtkNxO8%0`xA2Rs-3>|rF(6Z8LkJ7}T;iPC$2fgZ$9g%&2#I8avwPH>7dwrB9Lg%rIV(5&4<Mqn}V|7ER;)Oq?uVsi`E{%(9XT_3b=u{<4guH;SyhX7RhNs;VdEqRNOt#u&FCka3qs+$Tic%sX$b3<1F|I0+^VxwidpSJ31Qamff%XdkpG;(?C%@<f!&*n-M|{3T54X%ds^O=s&<&%Ka8UtL;tK<%pwTip?%i<GmsY0r{AubAY;;^#K0+u%1=vVlT_|9qZHJYM_HNzDD`G8Awuv;IBU^%v$2WI(-yvrH`UkhJ@c1`IKf4&0tlx*f92r{*vCP&gFH?-~Ek*t0c1EO;FwB%0MLV4Z7cut8n*$`F`9+wJ)GvazIdZH~!$=Cxzv4)GGGVeMVhv$#$UR+~fRa;F88Q)Lxpn{sAzlsjvT6P5ZZyFT@qiSIloI2el_X^dGuH(k;NVqoVj?fMiy<H1vHU>~Haywu%|W73%ee3i9mtCd!@GwGmc2<EQ6$|a(*iptWtr0FD?P!rSHL@3Vco0BW1bHy+0z+zviM|M9+ol$`{<=~D~Lf=x;h*np$_;%BB|IaH3erQI^&I8j2FU=TUDMy2TV5!*PLg-?h$v8vG)((+`fOPawNdHOqnV@Ho^qELpe-V8FKP#oj2$O#ap3Pt{nE0Gx$IIH<ji$6a+!CZ2?S2Dcst0<`>OSP=z7oG)2a@8M?(}m+KU0zmCV71sSSx)I`|V#E2(s!0FRwlSMg^sf_c=K(9;{+IS$J@phg*EvWcq3T~`^EpmnaP?)(B)#j}&xUQ<(T5HXhh^s;{0-Lo%DfmSqOcQ!h&Ma^cMNx3@oF$hJS`L=5_lff`nofWj1{tg~iZP#UAW14B(kKn{r8-TdYK$01XPr<}^aNRNH#p3u;!Yq}<kJu&h>%Ts#%An>S#9|wh*rL8bq%78CKJv<gaxwfb$M5Nh^&vQ<&~?>-_(FXE7~rMGg@Ql3)hsl!lPj&m$g(qLk8T7G7A9+aujd|oDt_J<G!JZp2Z>jvjXrzgTvC^b!sZO0}~7#cXJpIp%zaUq*FC(hPX!5NEtCP;dQbu2M>tIDavGQkq3oWWzelcES!BJyWBMiEY=4@08w%zOvIh)GGG$Sipv`-K;8UFf>qE}-ZbQNc%`%!i6K3dj*est4)oMu_NhmWV8v284;ls8dfFPh(9*rrkLPlgRIKZcq_^1Zbn?<z6A}rn#+vPQUXG?>d(D(+f@>s85nx}ds2cAc<hSLJCaG&!COY<ZN{VJBIxTFJmjlv+V517zSYCFcR#*jw%w=570PPCi1M5Odndo#1z+-zUk-djZFYCaS;WH~$v1MN&Lh_C>B=)hCWBD+YT$RLX2DXA!g>u-^_9Zvdgo@<*)%JjvOnD12yLZewHZw{}fl`F1Twe250)}m#Pz{oB+kwY0%|F}JicF}J6>AC(Y|%}CwVadu7E9ovy^+O629+?^&$W;TEd@?|0`PUpaUo48K@Ds97m@^E5r?dD^HHqPz?KGU)<EW{ER44Ka?cM)b25Z#90-PNc+f7)R-@Z6i~@C=SC~q+K7%yQ05o`(-vn6D9Cj0Mz>4QNK@?C4Dr^RLMMGNBOAn>WXJR?L#Z*oLzew%O02Eyama`9)3C)Qu&+Qar%a4fN^mLa?F;WlPUXe*vKn3bNA0VFb)F$P3QSSu5luhY~yswvJ>!$PRrgh1O9lc~&v*mhDx5}PL7PubKu)s0~QOHx3m;U;<6<@4Rjvo!E{E0F1K{EC_fj;L3h6BVAGy?>q9MDb_qmCblxMV~b?KmNdJRy)3`}D9pMj<+2=vz(1kz_mkR%;6gj<sPWw%APo#)JVf@>W1AUXvSQp2*1sfV}53>)Z_f5d_@;_&!Ll)aP*5A_CnZ;Rj-h39((}gQJG+F#A67#|(f(vE9D-UY0MB>@DXbB5l`7`c<Z*2d{F4F|smVOpphf_|5$Ctjl?GA~w3H((aT?i2{$LbFSBUY|piOE)Yx#gNHFo+92m8nb<;MjutLhkWc6ZyDSxcet^I>Gq451AQC-L2qcX9TyV;x)YSMuc+E>kw6~?iBI!;}l3yiJ9I1HFBLzENCSY~gb?WvOR$B!`0<mZW&ICHk1|KMr+JG;UgWD{@AaGda`?w6CZBFMr<Iht|HI*6kMdr)YHa`-B0`c|&#GsqaVfWi42Hm7H_3NrRNeE1UsXW@^ofmca{&p5%YGr5GU#qrFH4Ta}u}7=K$X(v2L1h~3TY?%~AvCu%08r{v;6PcI)VaC<gZIb{qA*zbHtHrPO+mGOVGKIofoho8a4**nP!?r`d3bq10HKW?`JTStVmtx_dsubZ?4zS<0|#=q_$_%wmI<m80iFUYzt{yEh`Rd-DvKf(an>X>A(d-jIa6iUOk#k1V2XfNRHs(O(IbM1j>*OmR3$Hg%87U)unwLez7uh4UYamXHNajW9kmo5tHpAr(t;}*!{#BBhkn{MI(QrG%d*wpK|^jvM*cB{_OHxcOHno-t*G;lf{m64bUd19f8U+ZlxG82dqTO|0BjjdI~gCSj}mzjH%3H?n&<E;flAzTo4_pn4rFl!8x0h^<yyKnM{5i#B~QKhgK3;rLH6zA<MspJ6`9wgQfY7vhG~WkEz_wsxq%m}=YO7(Ig?h^!^kMuSTX<IiaFL9I#yxXsDNUy>>x=cSCCDsy8%3#SQM%-@y|esisuRTguyoU*idD*#r}+XojL_(OWW5HLcnA$6^Q}B9h3-tl0ZPAu!V4_m|&F{R8jA3S?YFe9paD<8;o}9q;gt<yS&O87BBMdraXQKG}>|$;aA<zJ^%nvKntR+sOo^ma?^R%po5%B-5U)O5@et=b|<sg?LQT<Dc~Rw4qO?wZeFc#bg@}h8hmK!fH!+T#~`hU8Tpmam1e0ACs`mr$H=k6KTGwpba(+%&C9r$Q}Fuj*O~t8DZL|SfSZ63iA%=hB%WH@!RoLJKr`f2k@Z1TWK=py`Jteu#h|I2D1_-CIV`k_4g-hyTh^$@E3BiZmf91R=OQ|pJy<k89}uNOkoO91=k)(ULpmUAX571+^Yl!-7Z)A@K#%q<;;aJ-je1LtA)lacef|^0HcB6?93VpOeRPMiV@P&3mMdfs+sap|PFR4!9w*9}VeYX2DKkk>DO`HQoD1BD87wGOLC2K+c?W}L0{~z(DUdVkrAhHz3#CYsc@$=*@zfhKh8XDjh2}QrNQU!_tOm3DMdk*}H&mEZJs+Bvi$*Y1@Rob1DDjq?eRbl8MU8~+n;pdxfsew%3q1v`5&kg^s3dXDs4Agg9wRjZ7Pg$trO?4CeVRyru;oLDAb~8^;uD|YmUQ|9ULNzs!Bf24U$d?xSQk{U#Oo>DGG70F2nCBKfv=J`gn7on74JkJ*J~%2Q5jQ<@I$LfSIzVwfy5&IGQ!UUs#6XO6ObC(2()D)YA*#z$2yq;H0vXaymLD6Rf74`4)A&|$)V&hK>$FeBw50;0lOdsy*WT@hIRqNkrvb#Cjp_bjA7N&hOPsU(++!ZnBksa{Ymjwrw?A(FG@J&6gU^LG#q^fbWg^vkZnSrXln_!u~zS&r6<o|u0jnT?cbe|s!cdJKfGuKI0HmUh~5XdenlP=i@W_h+zFXsJ<;s?Fam;kVAuYJP)ILq0t)bX_AO~ChPRsv*W-rY47sTmuKD{hsrhGxg2E}{fDcml?R|a{IhoP<JtdgtyV~O~<)xfqcWk_Bz&b7oMv!8ocsM(UqH;;tp`FH5K3WG|AKpfcQHO?*xkN}7%#Q8Xr{<NQ4}B%wt*nlnL`Vo0F$U^Xl8Kx$It3EW9ooh&YYs%@r2S+bth1PRKRJ=Mmc&bQQskqIWlJmy3LE5ATNh?FR^mRydTs<am0ee0B<-^l8H7MLj$rs@G$5X8d=+C#0|e76$nChiNIPn3$axPk(8|8oyg)Np&bWOiXvvfM5+cY#e0|WR+F$ZQtL&OF;RokHfe{$N&FDjq<O*1slStbfEE(1_5|$MW!L`QGRfN%mS5_2s2QA7V#>CCwa?F+>{&upWH5Qa}D~(Itqj^fJ|9*i6wF@xHE8i~G5(+r=9+Gj5zRVFL${nh>`IkV2Xf%mF*?zoCH+Y3_DHm$T9YKOML|IWHb6j*ReS#D2>c~CloW53Lrnp?CR{x#E`7d{Lrad;J;8%D|nq0<<S2(+YiTxKR<=)|0dzX#T6D-+8T6)-O4SO;5alE`_mKA`h+R`DY5H&PJlvq}jQlkzZ1;PsQ(oK*wcg13ZrA^zQ_!Gq|pzBQ=bOMKoccgO~?8u@?mfEy1PLuOvoXX&e!Wv4%sQNN;CY&?h@zBEVLY<0f1w$}EmxHJxK+Fv9uNvowF+z_PX@O?&+77IYL-CjiPmI=rfFmqrb(GJgIQYP#f!HU6Ws|Zta>}-%hsj9-=1<WK2RdSb0ccgeiB5N3Ifoz^F*-Pj^ka)s(xM<@v;uxh*oNExB918w^Akxax;o%wJ>#_`^0Xkv5+5bw9>tr{p3B+<?vgi-&0T11RvXo>=Qz4l33awyrz$>5E~35f<?+_4oZG-bPl(y)uaMhKCSs=+;|U>p*@@#@>4XHN!0tfc*Mza|*x8q>{77(17-=)q!hw)i@`S|iP*F?*Jb}0aH4r#tND6H_QL_Ok-s_=tK#j50A;zqC&@3i0`go_9d=Yej$PwUb+aXL0zQR#gOJ71})z&YFcilkmyVQ(BV~dS0_#iz7m6A96%oEqTG>kD9nA>lmAb^!Q&X`2BGfI+xEReh%-Vrd1jxdP5_U;oaif@wTp2}_TT||-C%ZX;(A7!4!OH+oRf0QvD6wu$O7lPWGhr2t1TQlK`O8D508iGlgIPPU~1(q4A5@J**kS**U1u9er%glzIFyhdL45O`O=k0JfB6K2z2SLBfvoS!33=T?&6cONZt7#!z4&q1{>xYMQ;dAO1U_;}>)k)QsTtfOTBlVe>S}jwxRpeDwb?0lrrcAtyvw)nMv0ztV*)@m8fJ+lmN(ZQBXK(159RkBR7pG_!x@epEE?7_4rI{3<br?&-;luBN;*;}!fYkS@!d9~1?r>eE^nf&?pLR28JnK~mb=)(kJjEvYE~4T?JVg{iK~RzS!x9h4&eq6E^O-*hW|Q%Xx4)2-zn5aPR3qXwtoXZ9DYmzi%CDdrkD!FUPmAQKJeB|xyCs=b0;cQ_s1~qFzud65t`u1PkayNd0kv|yZH5eQ#e?#YM0YxcTVSzHuduKk(px%Fl6J{vshYy+&r5??1{5fY;RNEHcQdn^Gwrw#Wh&Qcqod>wJji7g(5Ma&@PQ4>x4Msdm9XFn>nv}cnjQVMTmiIFv=ugk4L3hWJ5@=!07C@|(}1%PRGXcAWxiE4a4tcGqH^D^>NG3|XE$_@Z6&0_z4rKhvZzf-brjLWgHsRy+_)yLW{E2>U8>_XrD1_;&db0>K<arTX^$VHilc)9z}cM+r7u_Wc*0)Rhuww`GVn%rP)EV}gcc_I^E})j(pN^1P7Cx@DKP~@I@sk@X3wFG_i1BFF)+1QU~A#OVbk=>{I|WbuamQ_0s-jMsJBcUTfJmEAxcyw)wA>Q0M<*$NjbvA%|%-X*|<Q7eL@MBPKTj6tt2jUVOpt3Zk%=xy#eWMgnm)R{lqpTcH^NW6U>sTAoXfRLcJ0&nqdb&YF-3L_e_L~kVB~0pIm}{vJ|HQ5@p`F1+93&C%sY|gfyklqO4U#dDzwI2}IcV!U0z05yPd4WpXswHYguZjQn%E0z1vRbS<M;WX`vUW}QcPGzSGHrzvW(`iTjj2i7S4gJ~X|NtdT_svKQTuaIW(a~8Lm*^~Wehf}CXeL1&K%dfR8b^~NEnRop_bVj_ttMnsw4?cf~(D@WyRvHg=h*S`M$Bqy(;1QYO)qfTm$<-k8Vn%sxQfL7eDO=mL4#DI*B1~y0#47Y%R1iHVLc1Hkp&c8w6G-NDq+T7O4(&y!tV*rYhs!gZutI^#uE1=Pxe40KNe0raf6o@9ddbdXmXfQoovsB0mFUjC_AMsUC!dalVlD<&NwQPv&#0>(MK~?iY2sLdzroQG85dFM^`Kwwn*leb!9^RK1v^yklGKP<;7#9IY^pX;myKOU9e6~7=@lzwNWHD()n%Fpbj@He5`mnY2FNpQV?;(Gb0a{h)7R_--)bXlB0UejPX5fM7<@OMjpH~t#!O@oJc>reslcU}mERFeM8|ZOGMp%r*dmrK2t{5j2tSe8F*I*4x>c)<qUeSL4=DSNK&Du9+aVM~tc#s2RLs1LNzwEjuSzqm0g2g6y8!-~s`-SNs-yj?$qZ-i$h!tCl2Yu{-lbbfaZ(@$-wv!C6X-yZqXdeFbh8^vH9~*os#%pz5(QRaVH;<-5C=UFca|=n1-wX}aGu)I=4ty5hKdA%=&aCkpI`f?m}BcvuhE~by2`YL?yHwg4}yepQv2~MqaLmL;kUr8D%I<GjN8vevvRSU_1q?*TBl?AkC$Lp$?Tb!%&&)Ou}o&H>aZuo8k-hCD$sY&s=Mk2b~CPUqxc7IgicTFX@MINbS4GN&u_thQG;s9WV^1DHi|+^?Uv(B2<vMr$NBJw{2UMSoskz$T-8tn5bY#yIe>}=a2{4Nrx3{GhLuR<6n#PzOOo;e(WU;^;82PCdU%#s1#`T<uT6gu%`DVJ*xd3^ZxXM{Q7?2RqUDD`dN6}JZSV63+H3)ccL>=N{2&mw*QD$GSY(VM8v~H}zz|WIsdnbER(%?N^!aRJ0lOm2DPfUWB&d$i?!;wR4L^NEG$!Xjtv@>CG{dow&Lxf8wXLOTTnWZVqN3XopDZA+Tcg19q~=UL>_^&HjGTDg@)Znp;^=JXPiGXJ6ymK@Zw}4F04M?9RCc>dQS8{z+c!zZ%`kN|iS)95I_-Za3@Q7Xx8EdH$}M!B-UI4P$15b^%N?IMJpUV}KJh+Jx#QPm(m-nzb7Tsk>om9Z3xKSU)n<FB{2{+G7CQMX%I=oDSe=orHvM)=c5*eI-2+OdVv!QNEr3c$9(Cmr4yHBJ>&Mj%fm>uB9x-}!eg+OSAf_GY3ve$P)>>#CrQFQCLdXmDb~3eaRvY(@p=MXvw?ZZ2j;SVLq+mJ_z=O8BgQ3L?LI)5><P`$5LX+Q=m(WI;0HB~^Sdh}@Yy*+xa16B+4TLfk6<ok$!)e-u!>k555!FDySp~Nh`a`cdl%n5h=*Htg03+4lj^$?s0#FER3>0F-)%R&A*}d<AC7O7y3>u)PdX8=pfv*ykK#&8HU5=hEl(PU)wvnl1v2>@S<n}$F@J7o&KPgu)+6ycjcEufs5LXj8!A!hY)`&(?EG|^%y+~%Hk2N3jJM&u(mw}>G)D+1`C92bEOW^&kg6cGh;bh}&9`VV>t?&(fq#ufQw_OOt?&XaRX$#HzY;Y8#v4BjSL~Uy6M115Cd;^>(5*7r{D_Ub4Z=ybSl2SB$SD^`czowe&DiVjFQ)7M&QpSz-;YvUV&F)AV4()tYG@vQ$kAS-mqpxQdYq5Aj@;_<g6rUz4D+UN?)k$U-xL!IdA9s`Txf~~Pym6A@5IU)B5__vgvrsNYbIY7=1rzoyn%wRRGMh-uB5W1VCeIEKM2qlo_*jRRN*xlZe9~4OrMr!I*p+9ToV-`055-R2v+ltHnpy4!Oo%KL&`=pusPm$Cpw|+oRC0P5IX|s3B#p4!C%{(})8?F)NsZ1p`%U)okvNiGJb+}F`%S}53n`#H5Hk(1tPxRqG&Okf96Jn&Q?qvBip`%;5P)rh$)*L03}6<omB1h4A#8O^%39mRIxZepXxJFQOB*EQ^fR*3HucM}uRbof1(z-XBn8AISzQ4W$>^O_coYNUOj_hrVc0jedWv~8N{ZQNPSiBRbVUl&&da=NC=Er=V?1(^cHIt0?|im1%#*A25SmolgehN73aCZFgF+eQF+_Wh?PBALa=!W}V4u1OwM1BSBGdWoId)3kIhj-DwwOWO<L%c3739=(Iyq%fyRC;>-FHzISnwyH+0(`uj7OHKpsyJ2?K$qe0hQ;?i}TpbQIk1*Ht;2rKqU|fe4lb^>L`n#_R^d`vTnL@g@LdTE`!fGhYeYRwcB09W*|^lj=`t|3+6K73MGIO87=M$GiEhZLS1EH4F_6O!vlyrt`7Ax-z5J)*0+k^b1mfQag{Q6e9kp4pzx0KHxvl~G5{*x%{(o_KyqoU@@Uo#;hn-RFg4o#r#iLqoGi}Gxfjmk&7A%^TN!%eSm{H%iA6V(&LbP)6g?}<O|l}0I-}=y!Z@~4cOXAhLN#tn=*DN$EM2IhD`e`idm72W>9mJlVrTF)M4C6A5xTMnPX{M0;`W6?LcbG^pv6F^p%V-$BC`niyo6y%2n_DK-7|GIPA9gP=IoH~!)x5_h)IeiIMY=MQLLuVZ?1XL%n2rMbHnQ5ep6Q;;5&S0v0)AWaz^NZ13L7{Xpt)=&}cYGqm)$>)&(hJqZfwW%NA~q|6b%tLuI`&DG*o2tBfEzcI1d_&5%KkxEbR=WfIpZS(3T6N%C=GH1$kEUczV~^LjS9Uv_q&nw;=hFVBN6DXsE|L;TBn&xpgDPb}_==hHLo_`(&X<2!L_UbOLb<ieYaAQr~ks#s2nrdOF50byf<M(X{n8t^hIQ_j4Z5e@bx)<ao@AwI3hFUf=-{tuS$XtD')))
# The generic dead-stock heuristic considers future SALES only. It does not
# preserve wheat/fertilizer required by PICKUP/FEED/FERTILIZE, so it must be
# disabled for a new production route whose input contracts are not modeled.
_DEMO_IMPL = make_agent({0: _DEMO_TAPE}, dead_stock=False)
def agent(obs, config=None):
    return _DEMO_IMPL(obs, config)
agent.telemetry = _DEMO_IMPL.chassis.diagnostics
