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

# Modified 2026-09-22: executed public episode 111910412 production orders.
# Empty unfilled-order slots are retained; current prices and stocks remain reactive.
import json, base64, zlib
_EFFECTIVE = json.loads(zlib.decompress(base64.b85decode('c%0o`U2j}ha{MoRo`)4F#ooNp64w%zHVu+mV<QNLf!!cLuz7Iu7UaK2B4_T$>FTQLzISAM0RuZbBi?&Hy8CojSNHkwzZd`h^DqDS`!5&&`r+b->xYMnkB5u@`1!y7_TQhr`1J7~KmYQdfB&CPpFdoD^Zu_t{cwNx=Kbr(i^Ii_Z*Q(Y{qL)fhv#3ezkm1L_3fu0Uf=zAad`3Z<NqC2kAC<1&+mVjf6iX=aC3V*KmEn$r@wu7e{&%|pb?B;KfJxU`80y7acJMXe|P)lr%!W#eE;;cX=IC0AOH60q5RAF<?-L~sg5gld;R(bE!c;P@9*v(-#*P7efsg{;qgMe>yT_`zHi5WaJ3r9^Q#Vv5A!gFW!-5!f4aGOv)-d|``}<si)n6!J)GmKmLfC0DK5of(zFj3udn0ce17%A=XoA3zPq`-`~Ko^xn+T#Ux60k5O#1m5INO{yZ0-RgEK|ah$bkfF-qbKyu-8p9e*QJI<5@VtWVGT{&5=M@UExbE3MUWK8u}CUr=7F(QL1b!S&<K{qRY>=eWS}J;R8RAsEfjVxrHF^)zoil2<|Pj&oV--LRa_H^&F5rHE!REIC@}@{&962`1ND=+?`ICyoj?{Du}&8_ao;(kEgwl8NW(&*7qtJ0h0N5WMNxvpMW7&1pn*{TDWOn#%FJ_Tr2WLZ6tii)%t2WIgir-R<qo>&Kt|baVgs?)Kfkt)IUZ?A$9{{WrYf&HddEnavEJl*vl}(>pv#&vZ%?_ieEpgKG?ZgJ8h<vW78~+=J8h!WGRPOr94vC_aR&nQ&t-*H1?4l74-2eSH1%2XCjm4FUo(tIhP@!f=%@VYrWA0MiG<Dr2km<f?^5YWxs9u`mGbNnWm^wdI%d(Hh@_w)$%DUowvkD9hv^##KfyM_Xx&8F)SLCQgnj5OeK0Ow)1AstP>U8aqg!ihqGEj*f`u`y1zBj0sOm2}Y}<6d=HP3=zMH+o#>W>G{*ZnJ4S}tm#7Zh8JB&8cbDu_~<ZpHlF)Ia%Y&HwjNmVtC~n$^uk)6SFS0}aUTQw%x74B<N1B-GpG`Z6R^zpi{cxm@q>wguQEVJ9~&(viY;@9l$*+>95v7EZa~<?`?IA<%}p_c)-IYbxsKBWT(HZY(?+0@;=~~)7!MgIoPqlNa`5LK9`CPz{O0EV{;w7mJR*kpVBw44zdnZH5p+b>^zHTiUzlvzBbXn=?H^c{ae%!6oV<X=KT_D)>_M#ET~{Ol9u&2Dxx!HrreBHmW5@wp&N+qvOH-X0kfQj;08r7lK#{TDGde;R`jrXB^i;T0@K@u+A}a_7L^sfg!hpL7T;&B!3HD3}^z1FjDb0T*Yj>QsaHXfk>7k6{>GAT+zOaVEqe@FBrwCR`M>%?vD_k3&=mpoDosuB9DJHn7bI#IzhOda1xR8Dw#O+`B{H)hWL>CLq<QSlZrb!q3EM^+410c^7#drAg^_=g7lQAejB`86vJ&&d73#86Du#ng*QSJc+wjFs8xprk&z<C0_WiZUk$}kDo28@O2ziwSS&-(+T!d}LvFe5I|EWM^#kuViG8Nm^OG`W5Xfv4aQDOps*-3Z7H@MHi~N=XD7fMVc4%Qs`MKpVdg=nE`aoW^pW8n`zwGBkh!E7-%u(SaBvQ~e6yn_H>)-@D@s22^sQ;onE<V+nCap50QK)QP8+gt^ji@;d_E1Yw7VHUjDfXt?K9qri4LhZsn(k0<S^@HTQ~JelHg@jT@k8lk4dymLi1=#WQYEL89sASn?0#p7c$lMj@%=9z;vB*(C;jw8>Y4GaU*l%B68xCZSY*z$r)z@|ZQr{P2Q_>68$3Vt?$tqQ)n^%W$9(QlwMCE!zb-oY%!P7CF2w+5lRJ|^}k$<B00c%1qwBE{AkqVpeps!%J+9%oLKbjyiCA~+NdZSX_qh2Q36#_al>bRN9D{V-W}T>1DiIB<MHXEepctpTr*ey4H@=LBn->+UeV*m3GmWa{pGTu)#m5LzxFQyZg&n2}G5DIl|yL#1Z~PCt(+%q6_LQPh!UVCe=}S<QEgB4?@3Lp;k2=(oUi%v3lRoYKKhQrIlW@x+29WdXCHki<5i*!bL5(FhBrLpV_rWDh=Wc{^;>6-*6{8c>9G8~1)_U>G@r058kFSk+DQXi0Mr2PtH{*0g;FcL@3BYn=qDWa0uU*a4yiFp21}>wdhuyZxN{F8KGzz|1TKMXdyXyA`^c9yu*c!KFDax@q)J%XJj?Pf^;N0EfpTbb3c9{qB%7kpOCFESo~or2zt2{|vv$fCzMsP+1DlV`Bbll1`XQ8veb3H2UhmGIL;51{r%2mT&Lw9&S)m58Q3U=@J2w6Lej9GQD^p12G8w3#871;V#!nXmI!wviwk2Q%;!(n$6`Vk_{q*zJy1aDheA#{bx-e^ND5NnXm<~1<tatcLmc0T=u9{NYtMH)$6-(@S#tRT*gUgW?0DTL`93=EF~cd-MGuEfr3F<3&^RD3Nxlog<d3LS(ainjv1+;7^t^m43>({h_uyUob#upl&Wz>^9_Uoq^P}BK>}Fc$ibqdQtJ$GqgaiLj12~}>a4~Q*@P>wX&}fVMnMvP@)b@yn$Tqf*#y%4gZ4^M+gU+7QD{oh2%g2?lJt>X<F+Mz+U%p8S97TLmax5JI5cK1W8S3^6K><igJh7Z8TD6*K_YHiq}(t?CY}7505sL759KF$zJ~_hEx{E%s~sryQkS$u)7(!Peb2k`y=>xI%(p}X-Bb%iC7ziORnOcc^z&)OlU^t0Sq4BWMhw{&P6cJ-p;APL{O?z1Wf?XhLk177JoeT$@U>0%CL*pNU|c>))vWEI7(ih1)Fs$BT4u$}P7>N{YZT=P^7RQ)!PbBN=T&dLR6G_NB}HEt)h?p`PWjI->w_i|5}hyFY6g|7@lrhBg0Ogtd5dX1N69S#+sHyf)GZ;fFD3OkZcHRe#Q+ebkU&bTz$MC!IfCqoJD8U5l(qtb4rxru;Dc?HOE5tvze=5@8u0)*C7i^FhB_n~yV-bhbnKV12Ptuuuih_~wta__K7RM^_Rmk*LmqEK>n;NaJK8=j$21tpL5TCAfj~Zym)STAerzR1_sMPXJ*z57=sV|(p&glv(OKbjsapbX8`5BH6%bCgLuBoP7Ye1A`2=cI)*1$VDui#bv`aSs%G+^U%jmVjdI7x&A6ly*UA(J!uX?XKu#{$=toUe*_Q&Ezi}MN}qVS&;(d+txGrtD}SHvVi1SJU$^fBw?L|l=OXd#yneKsX12J#G8fg2n~w&L}zc06t87-s=u13QqTjB&NVSW^13GO*q{B2Ogr?xdT_PuLbEm%eZQ4m1kG>(t7>EuTKm5i&7Z3UMd4FM3G|79{Io4#k2z%!H*C>>>%`7NR#me(JDD5cshjFaS)C$Gv>-T4G%cZ_gpi(n>vrV|zxzf?H;C*8yK=g{z}4DagXh5><*^*sS!brp*5$B^GRIhAZ(*PEN9NV0lRdOX^}qZv<m4r=bw4H@}T-3ey0}3V?ffU_`%OlKICbxu5>>{tl%d8rTBsZ4LYsMaXB)$n#{JhF}tTQL!nlPLMHV1C)TMQUu=Vr468Pp#xH6!qa8nmP>ROH2V-O0H+%uvs5)ob2)5Cr2-&HVNWW74-#peP|wd~mNROEmwz-n){5kw_)2`a-EO7dpfANL2OUm}hie@#rP@jZR|-cfErNh~3FY{A%frh$UOW5?R8^aDjTiE_u#h2QMcYOa*vUScG<Y-tUMk`<+IW1xkA|`$Y3K*_sc<N|;BM9!8K#?8pGaK(gr(#b8!;Zds30!#PBs_~Ac$#INCIilfRlojmxT?xG_?p6h%mwPa2SiV?-I4nv~6*;enA{oE(d!r>)A@W#QDo{LYM7s;#Fy;8yW;+i&Tl2We|6SwLqr`a=`Va#9aGAJ28XJ;mRpqzb5-)sm)(K*~7E;O+fcOFE|)i*o|NvQ}Zv=_6sTB0eKD|ol93aW)cCCQb~buI;WLuY)2^}0tkkA#vDvXY(uF_nSDQ&YSz!(XsVV4D4Y=_BPJsmMYw?m{&s||Hc&Yt(uiFr3ZBuVf}}SB>73Cx(X9gpbC6cF2v1^lWwEgbX)3Hp4>C#u|I(=OSR1#^)l+dP0h%`taQZ4*j3}V9i96mtn-|4gy|S_zQHB|78qzp`bRaPaqMV_2T`inm8vD^>?V6SzM(2js=*pS(c0F+z2a;#0exqj60d_p&veZ9t=`LV;TiYEFe-;IvbQ%C^W`V8C_ODEb@ty&OWu{UL6Nt}2UNmLI8#pxz!UUQ+%JX?77}vMuY}~A{AHqMeX_@gzNMV?IK)6jBsdhn%ETDn2z8zCIv#=44DbZFDW>TlkNJZwL?WxH(YLz`OObSxXSi*u~tqif)SE?*~z^LCI@Zcs~EZBtEWzL2G<AIXMc1cqu*rEbAm*uwE>Jr(ji8Tsi^3YK3D`3gX1Uzs~Ino2XvQ@rnKiZMO=0l#f_2qD(A^f=ypagFfuN4JbWJncb4-XDP%-$`K$~3i`Z@;}bd>!Zic?05qZZ*<|(AOv1uz;t6&}_Vz2SOqilh~^@sbL}#LGo!GYX?KS>FJG0n4a@2J6{*-t$b93vRqYMdq99u3E~rEI0A&^!P+6h55)l7WyMH^h!T`Wsh5dlV9YH>4_?O(iL4ZufdoJ>FcX$y0_c&|*(32(v+bisfkDnDgI+-}3$tNCD4lyy7Fm_0jUvsW4;e~6Lq{H|vaEF4qcovrI4N2iK`+H)M`Rx$v5R?2O*@nQULK{1(0SaS7&>F%c=_@`{9F;9c>N4%-56q*bK@fGS+SfLI#mgQAg_ZfZ&55L;o0&;UN|`;ldU!tOUM;$%(8O1qLhdTGGCNhjH@cmeD0o1QVtI<0R;?rpk?>qlZnjq<QJV_SnDYKh|jm^;g(55HT;y-i(ym}E-FAud|{x>F<NcLy&KNe(#o`)KTX|%jgITeM+jx802|3m?gVVKZd7vC7N{HPK&*4fI+3PxWK*#5@b>2B2UL8q{J|~HJN}K)7B0pm%lF|gN1~NNEVH%BtNr48OHn_$#}8>F3^Qd$(N1T<MU1WH_5qU6{31+9$^b$489COdVI+m;Uxp(+nK0QBe}*tO<en}~K*_1844H_rTsr`R5U+-M*|ZFFGn!zBctDCpN{P|SN|G{!nalDEaPTTPF_D++$&iolnEs##8=ma->LAgmWn6fM4&*g@;oZXo%ig4oD3Yd)X`LFAvP|jomEOU%SHL@3Vcqh{Ba9C#+0z+zviO`@9+ol$`{<=~3voelw>lgkp$_;%BB|J_*aT-II^&I8j2FU=TUDMy2TV74)tqO*Zk%?IvB$gbt{?BJ90_nPQ>IFfjj)5=p&TZwnm75i&KvZC;<ZpKR}TBh8T_C9n@SHE3W6Znwg9H16s~PL^NaRSP=z7oG)2a@8JezSSJ4z`zmCV71sSTY(?r;p#E2(sz-f18lSMg^sf_c=K(9;{T6rK}@RFN8EvWcq3T`ZZEpmnaP?)(B)#e={xUQ;uJ!?ITh^s;{0-Lo%DfmSqOcQ!h&Ma^cMJ;deoF$hJS`L=5_lff`nofWj1{o|fiZP#UAW14B(kKn{r8>QsYK$01XPr<}G~rloH#p38#hpN|$fqGl5FwlN9-FZlX0_#$AX@pV)isFrYfLx?5f;d@*X3R9A+kQImKUfxe^Ubnt!TS2&S;IHFI-dJ3Xg`BT-H+c3>lzW+Y3ODqkuEuj5tRb_YF<-EDqtH6@U*K9G3R3Q&Yhmm|*C*o5OerwRpN9ovP<C#5JNu%7}>xuak8-ctAu>Q6^)HJSe;>gKiaK;p`LH<*rF!u|60Ah>{~=BJNa|0h3@>T;5m#>grDttb(rcs;{NPE2Xta4C$eCbR=7Fpr<~qPpxGHE0)rE&?v~((+<;x&gh*sI_ImTV$E_Sy~XZ=lb6PtkVxnd=1z~^UleX@61`-NWGMpdYZX=F6@L8E8PaQX3Cl#s-cCu;tVE|%jq-9pdJt?>AsfrfZqy2^z>v9&iy5F@!Fyoc3n>$wP62rAA|<l-km+R|xH5cZr7E`UD?~_M^@YSfmU2uVhLWq2SnYwWAXT9pwzPf8)owyX^8IRiK<A~rQ<&X5W*M6qC8a<qLR2nqODh4xHczMqNw{6LW0>ZjZE8h!sFM|I3Jz@1O@MWlll&G-;Gw;d#YP5|FxStekOwUVPJ9CJb;@xeO(;PPYxx(F1Yi+|ta9^FtkJ-h25Z(p=BO-;w)t}JACTr`2-P1D4B7CYU6`##w_z9sYVWQvm27<mY1{+Q;8}hXU_o=(Ouzvvp63KnKqaWK8Q>KSX-O|Vlq#Qz<?t3$ISKqCwKD@ybRk&IK2#<&C$>DdQ;aP?B6ic$T`t8)J#2eLCRG6ysPlY)c*awkl;1_Y6Z}#(r6cmbT#~h$&ZnE!B_B5Ql3_iS>p9&jdnQ@ndPKtl%NRr<PgUNX>tFhNwmvz2G@$Y)#>@xF*y;rOoEsPp5J%7q5R7s_J5h`}ejwtK5oNUFgedZaKvwM2!}1t~=zyVbH4#UW?eJTzEg(47ij~-6Hvt$E2FS=;0j+pVZismzC->;_p3kgvGx$dkbOYe~AiYwb!<B^ybcci=h$$w-c9jo~8n(gg`@|nJ020M^+v0m!zC^OOoR5gKT`TF=nT{U3$`!`Q%6KtB9%$k>^UJd?=go=O=%PxyQ!XV6Jd)12Ugxnb_uRQaFewZk#w=-roR?%`3xzpaxL`p(p%?73RQUM;0^7{M76^k#^gtnyFzWk)Qy!(J#s|V{UOJ+^EhQF7cXE>aDv9Dq#e*Ix*zqy}tHZ8Sm$b0jDj*VwMI&$~&{;P4K#|l2e3=~FW(fv?!z$m$WdN;nI`fRbOfA)}%%E49FH_t6NDK<Z+cOY@u2zTLZ<82wmCn?!tL7vjFaf6WXp1-A$L0ImS%9gPone2i+BVfRD8|Gdtr8=5d7lQAX|QhzYH)?n+|mF*sZW6eW!*>a>H-YjBR7b`VCCzdo18QS)%t}o=zIsNVPeC*Tt7frlo96P<pBYNHg@ED`hJV?2oP*x)n&7fj;akD$lc<X;T2gXs7?fU3atEM6Ko*r?jxuyide*1lhA}zu7TxDm02^10rG(<0$Nd>S`|l+2qrov8%I!;yaXyI;)%dIc!Ky&#I1R0!fvVo_6q5!rSMoSrZbfmT+tXd51~Bt)2`9M+hE^ut@aKYax*gWk14c&W$s#vviWF5oqrT;v_zoe(M0?EZiJ>h8^GEV%GCy7%V65c_&|M>$dkA+B2v^mhgS(y;-=dKX6bhzi!0b@px`an(xo|CVpu78>ct;S<Fp8}uOA-PANa1wydITGgKIEMGv3!;rBkhP11}cO|1u?WCatQ6kx{U*V*a}obF4FTtirNU0mWe1K$1$XAlt3(2JmcRQK-VizW^mFo+sE72HV(ULzUSU+cWBQ>J*qQZC^_W0XuW4NDKh(phW1C1Of_$ErdhG1gpfLih6I$QnzdC5QlWwV6;;wmD3X3<yF?Oc#(HE<?%zH(UzkKzv_ne0RVskS`ckTRR=Vdo6fTa9pqH%-e{1JAOoGTJDJ69|EY-W0uBP<z?EUk=GFQ}7n^0J!H1R(c(eC&4AP32kzWa2X_oqMk_GZ}j2t`svs5ojhZiu_yo`%E1#jMco9WM%(mQenxCt1MxMWOD;;E$_tPYz1G(%1mSsz42Mx~RK9|~$(44TS`LYNMc!$Pa*FmQ;!WsQ2g!a90tsXbwNE~1m!gGJ->0Z}>xd9UDhPX8Y?qyxfc#=XlqPtU}Aap4gF^l0BA&N`sbsJG-8@(KFZ=RZ+wqx8Yb0V3qyM|UVYhGb`Bxk3i9Eqs;ggasJvaiWYF<{k@>GLr<A!lg&dxxkIsg9W83=$NuU?_khu001l|1#)J+G%22Ip%h6nkHX9}o_a;b5CdJm(A?%6$#9;L)nInN$lPH0h6<Ca=R@;y(FleL-f|BWCEjwguTK0hsgclqv!hrd@KIQJp{JlV!at?~l_bs?RV5V6W28pF!j`i+7dp60pC-~DZ2Ax)NFYnK_{3+pC7u3&m&bf@@Dwli*Q_fE)&<oo@p?+PjMu*(LcyX*;H%^fVV-et#XHf*_1ef~RL0aI{LpIBMKe7}AhC$QjPSDq)hP#t2}liX1llqYwU>gVW1UO^n)Q)I-Z>rkD#83|2Y5M`<WO>$AOIj!k}P4_fL#!R-abHUhIRqNkrvb#Cjp_bjA7N&hAsn;(++!ZnBksa{Ymjwrw?A(FG@J&6gU^LG#q^fbnlE^A=`vL(bf`dW3AplQ%|13T!k7w+P^y^Rhw{det6Lea0ZBy5WNp@{fay$7I*u1xDztNa-!MwVFU#8z^?5Lp^#qK1Qg)&Y+KS&3~x6TuE!0(8FEuCT=Vy1r{<p(3JRx)13pOIxA*x;<YY$Y_b$OS-_;&}DKF&=yJO>31J-d)FoF~t#lzV-6qQTD4(&9i^3giz`tUYlj5;)g%q2pyV0Ns(J~gidedsIcZe?}sBtk;4h%r#7l1${3(J7E{?$9=NS#uyFC+#QmV4cOh+sTQvwIp7elOi8wEL&nxP}m@^+Pbi3V<qlGEaygWQ`vO|M$$e@kwFM_;|PXdMg!uh##b?>G(a%DfZUGDi?pMrhMe~x1Fh_P%?mVx<&4{Rf|fj~FCl^~#McL1s{JJ|w92j-6Mk?G6c~XK+#Y@Ckz4^Qa}sHrgC)ayM#8e9A-L8!x{5HG@XCsU?w~~(#F)4lT#nfi#NSR<w8nyRZl!Uldo)jJ_1`bhpf&+UdF9*LT0#M*-a|4j(U&=5M7cv1H~$={5RE3$C)<yg=?1UxE#*ROxFblghA1maWR8oDrB86eT^+dxozvH9%oLZa)at*JIRE92&a}s76#NR0Nt4TX@d{@*FtLAiQtl0&wRhPVJ;9Pqq@{<g*05(&AIHl}W?2E4sx2LY3Q<EtM2TfZDK+ZwK_ILkFWm%5b5|@jSX#9Wia$}j0=nL`K__sSct<*?!Hz7NWT{OH<1{%x#;FXhD6FAGjH)jqXTmx29S<$+F4U=*RxktubUBDB0>sSl{;F|~7$fv(krrqMukFCfI24bW@Wf~>2spx0R!8|<ih~a<8i;*DST-qZBd2UDde}Kh!2Bti;Xp?$FaWK}H__?NE9VddBSr@&k$!AZN?H^|j8?#J3EOb}|A=GC!u&*1imnbgS!cYKM4lGJSmL8(+@p9i+H+Z(z+LjjvAGMa&1$3Cb&jJ;l~A+gI#uyeauMx)FORoY<=hGmdP2;;e1+U*G7&qq7*7b%%T65MN+%>B1$GAlzb1@z$IiZ7<VS*A!bqE;77m2Gk|!j7hl*kn;0eSXsDZ#CLsDqdiJA>S@m>$D18R(|4l!oAgJv<2(Z@T*<cpvKM2-Mg+YVu3@D+}_TKW<)tJZ!&yz2&f-=$_88e431!3XIvsFb|fXP&s$rD2S@z}$Wd1p%zgamFN~-J>K4$O6gR;T-|9=m>+@Ywtd>qWC6R?p?VJzKbXldpXgJ`=iXWcxlQI^p7&8g97>+^+Hg4^Kf@VaBC)9Q3)U0QA02(6UV(wuD~)wRYHvF1hR$Qqd<k~V42yl6Gj}`kYTj7?7STgM}$s<@F3`Sc{T<Jk-<R;ks<<IZZ$20%Rw9oWBu@uE__bi0&Hk}xH_rYl1oV6Wu!h6Q>$gFwu-!}s_uME*p!KvaTbtMGZyR$EW75=7;tGKO6dUA?CcF)vqNAQ=i(IYLKkf{-wEppyR;_-Xc@-RaQN_hp!npxA0YL;s<4IZw>w;yDLo*K=%?LG8qabSLLK)WRGwm!d>2viA)X?NpdhG7{9%cQWM^w+rTv*d31*Y=ir2r8l)sl^v{WPFHLUo%QYp5zl*+H58jqlazE6wfsXUed6T2muRRX5$52zNfO26E&x2_ae{g8LoNCCBSy={gJZ^eW1kVJPng<D{;POq@A9nxDmQIdAaW~rLO>Ca1pSOyd*is25#JMU&@HD}s!A<9&)(?&<h4S0~tDxgsvAm9TVmTz?*^(tY(71mkaJT*J|Yq<hwrD!W`1{<z^j&`b&ash@46s7@ZBd9hz`O18&YT#Ug3Pt6<UDat=4$f}q9@|Ptg?sJs`(#m@lIkd;i3g`30Jw2YT+I?!V7gStYf8fc)tu*ni-6SgM$#TXMioZ~1%R_V9ZFv<=JABREDyUCA7tQ-Y@m*U^9e0X_UC!HL8PyYAe|QIsZwGW4C!E(Q<*)7R^F$LDaF9lVu3A%|B6l1FY{mb%Dzm_wh9EGQ={H8acuRR?Sv>%l~m8}j|Z?`LQcvNCT`B!LdeDiO6(I#xO6%U?bAx)JQt>wisZ&=_s|=V-bUybW!&%BhQw|>lw^WgQWd0Ltw^X>0!B0J;784i0O_6`;UeS^D)uLrV4p0-X@EqTS8hQoUhqk;)CM6<DYPhSRZ$)`b$S93HokCxRe8j4X~!}-8f+Vs4=6_dxm|&s_PTT}qgZ6lw}@t)M|d;`1tzB{YO?x?3EvN_QThkdJUEjsPvcZMx}07i&En@QZZoqd+s_WCP?7p_ZlRW6Ygz0D$Y3(>`hn<-cz;*vN9-Pa{tlt@DY~pQ9_kROApDLUA!NWKGQ+F?EHsj<LFC1Z^4z4*0xnXvwrL%L$#+DU(ol$1=)0&OdQgORGk!xmHfkr3%<D+KIz%1XicVRTTBQ%?XE<Sn0+n5X*(7rlw3m|%q*?!-HAeN4oyROCS7ke03J5CEoo($~Or}ph9SOyp4Xl!6r_!HMS3inyTCCH=u>^mEqa`vfqSEU@zuY$iZcKxVHaH7*sN5x~5wpOXzO&d=ZJ;h2JC8c>hy>Fs7Rr!%Tgj`-G!f{U!C)i;IXMlGXWGVyj6~)}fKsQg*$KYIM%YAp9(<krnN>0PW<DFoad3>8$RKzWjfzu&OED|IBbbPe=`LkBQ6{lPEL#wYyjT!^BC}&?-d1$0RvSgp4F?`j_8oytvFNr#D27-UJ6Wihc^Q+U={sJPW?BOhvzc}Q{4-Va2{Bbi`&E+}&fJlA4Ok?l*r~lsx02$dKn}hgSUGl}14WJ!C?3+yZY<RZ{gta`RXRx&ScQdcoZ&(o^g!I1x_lP!B6-4jYD=4^Z95n$5(J{NLd$)A?VDnbEl0gXf4b@_(-yj~UN$`l63R(!$FGcfwCV@Ut%_*kIk{D(dOeSE`=w}BE_Sn=+fJy~=~({bIha*4dnP9H>tR|flNqZz><O{PrUj4+^xd=SuDXHU9#^<g`~x>arziGqfg2HYCI!sTZ^3_2gKEiSyRMTqib6~6mgDUZ*4I{!^WhKqIUeS_M_xQ}RYMU#w3EE$04f^5d05GuLLieHRw9v8^a)WcNy-aEm-=6WLnZF(;aOf4%<=lZHvL63vrrRZbIU`$op@D_dZ9BBEk6X(gBjFmd!IkhW(z>PL&%=s2Z6Y~CSCJmkui#F3_#`sLqut&+L^~%^=bIg=d+0g?20s}ghghNpgKak6PH~z{PYpgn4AN({^*d?497w`mo#qIww9)GB^V=#if%`IvVgp9jRMa*HD~H!KhnNp<izWiuVA1PM`uNUno)F8h__6=IW!LgpagtV+3hYxv13DT-y|6~!_?6v(#!hkwEvwjr0i?nev?!wx6pa_9#AtKuaJZ<cYNaT{BM~0#QQwuj$fBa1Fccaktu|()7;iC0J1_>o9&_Uhy2P|=;X5~yIb;Nbw;+@^xG-fovZQe9#AqBi<H=H0aQZrs4I_fFs+$hKdx>F+#>t%h|#0-GjN~*F>OF!fP2ZX)<Wwj<!0s;LSC@9k*S5V+PHTNHM`2b6)F)oOf?B31=E259<<dR3@!E`bO3QgULi0mH2F<=32l@K017IG1u1RLHV{b;$52brKqymD!38`voTgnk%xaJmQ4RE)Rd8FOKlGYIDf*p;Zaf|YFj5WfSbkO@0EMu|Kp{q4eV>Ms-TN+BqKW6qpaFWS=jav@_$pBe1UVqt<>=`|ISUYF8<|QLOLsa-Zr=k6Z?ydLlXCT<z0kpkU2(@D#Ki<oFca^UHKI`ziwo6xFOnJQW6j6>W`4`zJW!O1nj#sgM0Hwh3B2D`P@Q&SIN5lcM|`qzD||yA>4&1-Z5INudwHWn+CsCw7#ziDEFe=SQJY#i5g&O3-vH-{gayI#iq_c1o2ZYSq!bO`RcJ!quc_v`io_x4)R<p`lyPHyxDpUTvpbT8LpvW84QLAcBjE1C=<C_VS}dNB{7>3A#ixnNiU9&zb&}Zyu9wcr$K9lSF2_k6Z=7T}gib1(#NMjWER;*p+%l(I!GwK_CbzkQ%q9}E2wMfT$+H6l(IR{tKGfl*Qint;pR`p+>24z)cI6o-C+`*ML$Q<hUiV-D%`A5VCPWqrXsC=S)Opc6&})fPDmgumoS#-1l1A9=6W}X~X>-oYPL0ku`%U)okvNiGJb+}F`%S}53n`#H5Hk%htr1arG&Okf96Jn&Q?qp9ip`%;5P)rh$)*L03}6<omB1h4A#8O^%39mR9@#vu(6BLpmsUu~>1Sl6ZR(d{UwvF|4KAGnND7Eavbq8$lF>V<@F)hxnY75M!mw{_^%V1HloYeloTzDr>53GljhA`VP#TJ!$9Uu{?YbS1-uY~2n0Kz$LugWI6L$G}r+``%JSdb=9z(SE*d{i<DCetx0`{qkP)meGCo-MSo@1xvos&6bZi^YjE#7`jP(e;jr;}3#wcC2A)qNLbfdzj8nmuit!FXhu3i^uS-k#&m8&G-Pyf}}|95tE47Xx212~+}+!1pPqrjD`*YA?<CBkQIcR~QHj;WGG~bJ&n2Si8+dYz6{_<rs`guwc$3u22Fvk<sG5Fk@CjCDc_G)^MOjH9Ua0<LXeK`6l@Xvc6UPo@*gbkE@iq<8v-?0fl$W-%um~$N;E#H}kXz1IeYa%A;8}gm((Nz|?5_pX$`cbFw%$=UzCEH*@;yY-Q+;W2F!6CKlaDI*)9GQ}nDbSILSX>WrS-3FBBx-GTg23DvkQp&Oq~vvi@3u8^t6?r9_gr_&yKiJigI5NY0ckI<Dxcse*~5x37268fER1T6+S4V_?65t&86=OqkFLSS&;?VhQ7<8)$sY0eJ$KD@@=j+mraf-_yE5XEZx{N|b`&75HJHaDy;?l*Py0lvd`78};^FZT#Na6pGX87*?91R4z|X_T^P!a5;kZ1lp=d)dO(@!yL)X{f9>CI#Zkc$E=E$BrCvtr;@N5jSJ}r%d89B}+25Hc38CjHaGR$V(UvWM0oE_p8nhRFe}P>*aaSC8bp!afp9e?-_A;^NGb>@qBuw9j{zbI=&N^=0zJ{M=rd%2x4LEFUxXLG`-5i2nZV+G*a(p)qs~#nR4dMjA*bou^!4I4Do42J|`1C{y!xSRn-')))
_EXECUTOR = make_agent({0:_EFFECTIVE},dead_stock=False)
def agent(obs,config=None):
    return _EXECUTOR(obs,config)
agent.telemetry = _EXECUTOR.chassis.diagnostics
