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

# Modified 2026-09-22: public Vadim Vasilenko episode 111917373 action data.
# This is an imitation experiment, not the author's private decision algorithm.
import base64, zlib, json
_DEMO_TAPE = json.loads(zlib.decompress(base64.b85decode('c%0>3O^+N`a{MoI?gKd-%39w><g7$2r4jgHVJ!%P0Iy-dSRZ8H4F7kJW~QsFUPeYlX1yL!%M%;L>8|&YFFzt9^Zoe07ytgtuYdpBuNVLP<Hh&a@84hibh!ABU;gXg{`>C1-N(QG^6P*8?SJk*|9J7$$G`r3{oR{yuisuAE?(XKaB+D4)8XOq_wR0Be|+`f?)eYj++5%N`|_us{_n8)={K+b^6~rC7n7H~zj^!i^fUJ__~y;Kn+x%QjBR=R{+pYdyAiw?hxXOSH*a76d^h(GAMbx{8QE&okKeujQU37s^7wars^f~iy?%9r7VO81?{43H_~w4z=+h53?>}6KcV+t)M{%6Q;~%`(4CLWeht-GEFotEFG@d`-+`QiI(YSqZFvrC-x56II<Ez#pGrlP<#bG&VKVH1Lj*Ii#tKa`N&%?#HH*ashyEt6#S)hkkphY-@9b6AYPWAom$BoFrnIdUK6O_{!CGk1l;nVqh{68|K$CZI6>+biy`>+gfc-Q^zkslrv=`x?Y^|=0U^NzovyjXE-pkBz{oWAdIrNjHikwcBJylp&=*3sLJAefWmuWt`tzG312j!zz5AeSKO#jwMx3Fn{6?}=Lrv>Q3Z&B+YQ6Bo>RQXj|gi|1e6C`Qbrsq>k==J*TfHP*TYeY1Bt<2%r@Hs6a@b@|Pc(FmW2LOuR1v_6Y5Jw3X)7S`<5?c29EuRi?z=bLvQ-n@PDuiF7{r|dYO^26}{*Y9q>*D70^FeX}y;U^y9YW{<_4c(1k3ivvPF_b(Gu<56z$$pspUR?8&Yqa&poL?LLk<0Bbqjjl1M&~cvH*dRuxQvHp{Xr-I-+5ad)<-`rOknRz!PL@sfxTmYUEGGcYkQQw#Y<eCnD4&K-fc?;@Bz>wo$MA|!g*U4mSmPzTz+|Y!j8J(?+)VY{4B7OnE+Tn7h}=nM|RGc{cIjt7#_U(Iqd0as}X<r<d0}!a@LihFZ!T`pBsIfny7<ORSpkWz(u%w-dn}lY65^564Y>s=ZEF7fV1NfX2@K$^%D_xKm#O2EsYu7cv8M$89$f^c$7t~hQaFiUu>CaI9UM0)T=9jrCtVr_u=<1XP7}WDv*A(;6c(<7@$`NjD_Mx#-JW&EF8ki&EgPo*s(l`YpKx9)FUmgmf<qK|M2emhp%qlz58nohC((FEZq|gE4pD}2)`ML>v#Wh9RKn;-Bmh-c>Z{H2KXX7-VUrkaF|C#XJfv#vI8%nrg3?RT;_sL7}4w1!a%2S_<!K0`0IR{2~=ufHL(C{Psy^_QO2n==FgJ2rkemBEpP53?(~JJ@M>??dByS}A|S>b(0b6<#r+%2Pwk9QBox3q#+*pj_Z;rJ)TuzrNSC4#^F$Xt`mqLvRR{`L&Tg4)5OnD~J7Ga>vaOJZ&CYhs{V)W~NI1bfL8@({@9-MJ0(QRUm4v7uy1w#|2x|tkTwU@gFdY5J2-PVEoSL^nJU|Ciz>W;Z-!KnrKMJnEd_Q`$09Rs&iC2(_v4Nf!$4iwbh<LR;&j<ic?~Bnl^}zS|Y$vKo`YPbJms}|HgHV4EsrBa}=x)mhoDhRK*uXe|NAo1di>ttDR)RN%=2B}oE<$Nhqqu|kVDwg-+Xi%X)K4wgn;NGy3M=^4S5NC#Yc>BO^9feVjlL2emb^6p5pxH$leIy=vkD?2AgoCwIk3;y(D!VkbwT(}v~Q>XeE9nvuB`IcSxy0cw+XAGxk1trbh&B~b)JODj8HQaW7#|E$Q(b&-9@t#8_Il@;)YVb3G$A>hQ?!9a1<d=6#M+lRINSmvVg_714%IVsa*K{MahjO1O$p874Rx*R?(RzYtzN3*Sm-2wKF^J#jwF5?0!iZlWoc<&G77chekqc!luJ*&uy%{G7`Z_X3Sv;d6t8U2omin0R48H`#n<4I=jleDR3Yfbs50KIZp4D_d2h53e65cUpr_f=nW|4UH3*)x0!i}B@Zy8%m$Qrd9TmmjZ4O2<9M+30g5ZeemI%y=<@Gy=1XXF`p3yQ_n8@%Nv=CWsAx&phLhX?w<I#eJ29woy{VOVp<e?o1?6bSNC{yn$vwrfQgYIqkV^At!01Y7L-eGn&dmd!DHEpeo;5)>Ergpkn5@VY*Xk8I42Q{YVB(&7hP^kKpr}BweYc(O&n}J;gF`QCKBw=FLYhxn@&HRobZVC#yEs+t_Z#eF{Af?<)H<df!AAVHO%^kM^JxWcZ}0y3Lh*iIip0Z-+n|`I;JbU_%jGARh2gH#X5}6iU14FvavdJ<pSv^u+91{}?+9H2Vi}aSqP`R9Od)CL0g<hLg#VMl31~8sRSuGNB&SD|^*sK)0X_Q10hmHc*cCc+BQ0Ow-oC#<4PcHFQD-7Hu~@m~`xn-zmx((cx?9L&3I@1d83h>v>|^;lS$ud@v*H^WtXhlB)?c!QcgTAbFeQ0~!%v<1)0rVt2WtTK6i&9kqaaL(rwJYFhrfDt`)G|~e*(0ny9KjI7Yl)LJdW|nS}2&Wk)^rJjVMga+9aNTr?G_eSf+0b(Ru5iALr=Lf_0YIJs+=x1WK5*_UjMpV>WdT1W5(t4lqPzkHT^4C4^CRaIR}Q0zW5lt<lQUdzgj=YBP1h(vhy2K06E;QJ)nt5N4e9All12g_>s&o|u(IO?KG-1*fr=Ddv;{PCckVf~){{cb+hQ(AYX7?bI5t*nx*xz5-OB2HEp?o8di1ipVXNP-&?u+|*9p?5VbvV+XXSfh1i@a~S<?vcD)4N$XkZ3Krh{aQ`GI{hR<<u!<oR!e3Q`$rv=PbNRsJqhWVS%{&=rnNbBE8XH%iR`dqK9t6ZEPJ-!!bVpvGQwThldag{nRT+z5{d$0M=d418`?%}Mi6pp4K^$NfPp`K@6|&V~K_Vov{ZU+V1{h}jr$B$|1J^fhqwAoCnBUvQZNQ)B)TA$K_A0Ku^0fg)G_sXiZb+y?1#7`#NS_r=WYA&&0WCpHTVoSgOh+5IC^+dc%=vKp?e&M-T5&Lm-@s-tLYQ14g1uSWQjB(WP$lx)VE{A&S4|oUePjuP*7;D08_1qOyejLBb^v}VUX(&98|8)OJrIObq3HoEcfX@~nPAO6p1*J3y#334zLZD7uvMcBjXj@s8G_$}O?o$1$;lJcV8i>_899UVXV=nfDoCKeTO6C`@Dl#%VrzgwXS%h(=Cz>))_?+-*czHMvzvp$6&5}P*+sF2;cRIsjQ&G|{$e&f>mwkVVxpu2Sk(z<Bu}@y1JtlcPWaq>^5<}{JO;)VbNmB?x>|=iP!7h3_uK+d>E0Q+6<+IiKu$3x#97Oxt1LuafFYJfyMN)J8cjwrF|4`sQd7~4wCbkekFj!?V~kTi=z2W4i;v>tBqZFUDV;GzS;HrzY<R3)begNvEF7x`8{L5N=zyik%1Y!40Uh0H<w&bL!TI8SqFR-@KnH-9N68!UcZ|};{C1R0Bq48S;n0Amp(@3l(2J~<k@q%A>Wh0+bxOc{u&A3RT_3Q5c<+)!bkH}CID5{FgTtLxVAE0C0fYh5Ol(@eAZKs*P!E*tD}0>64v<JCe#q+zFzj+13t_<XOv)0yoleZj$BJPntY`qnS=BgPoup+y;-CUPj~kR12+lCc5}(lyxQ73sGqkf&5hy-ESUqiB2Fg18AU$R_rZBBTXuhg2xE?13(hick0Q3^N`VyaHO|U+(0=2(`*zj`vG2Y86FLE{^azF)zc}L8}Dsa)KLU|OB+vvTfNse?k%g(bTjq?@@Z61zXDwAfb7U1AB6WzLh%tntZXUQu3CihANjdw28C5}3f<2<Os?ntc|p*{oI;z!CV&ya=Ps~qGV;+oK9^0Uok6@@`sHK=4lBVAiq0L()VN7N5^&2kf9hjV4M!}>(Z=Gvv>l3c`RI4<nh4YW#W!Zd57Z(viU<npNhOsCbjmp8&SYx(p5QVjd-y;qnvuaM%%c68XR)0g1XMJtz``J6(nV_sDQ=j){px~vwMe#?$Mbw{1N&~|GZJxR<ogq{CwB?nw4%35`Qc`ug}(YZ+NNbUSXD*FZY&Ne;O?1yPcpVC4|1;@?>DG^#C@1j&bQU6591uycwba)4hv6%yX9<~biTAvI%d8%@%R!WVL)GOzi6=MJ<jLendlpDt@D@-W6*kV~uY}p-}<mQ=o9dMUT8G%D%eIru=_nVCf?LMB38Y8fGEY9^4@td%N-}vm?eAyQVdQ^&qb^1C$UD-Bao%wjZ<FjYaj(Stf6K1FYj=<;;P$Pmp?Yf*2L{*19o*G8pS&qT7BV}M|)@B|25QrK-0T}~M;Hl7sQbDO3%lKDd@^YK)Zj};qf*T6#DI?HFF=3>nxtp!7^z*c*Qc~2L;6+*8@DT*U6l|e(I@mwPdK)xCedIwnl|z9-tf;Bd0AB6hw0T&;?l8<)ew1gUEKE`K*PY*R2G|3VB-pACyN51AJ&n@t$DhxPH`pdxXu=SsB~E_OV_#(UZl?~cpc@H@WX_*97`A8DQ)$fU$e^*{n*-Yfrp`POPo5}%3aq}g$!2gRS<<9?AI&T9EVD@{Gzdu5tF$&b#TDab=Z6B}poeo6p^;35N7yIJ?wB);AzZYs6zTD=XcY{-Sl`x*qgm7vQ7mm-uvV)wb9(62+B;$;(<rB%6Lcy~3Yki6Hf=$W9AQTJrEq>09eI@y_c5@OVs~M3;4r4KL{5Nfi9oiL`tG<JqHVQJK-1kpE)xO3a85kb8HKJxCR4{S#`$ZXR@!pbT?{bN0HLl$6kF+NLh#}_EP13(ou_5<86a^5V^rgCu@izgoZ`Iq9QIRphJznv*+&dxs<b#i$0LSfa`@j}xT3&*j><SC5TX5y2bKhi*4Pz>#FJns0A}F<JEuCgz~l3kg*`<u(D;x#ll+9FK<@->g)6IQbG9=?p;@{K6Gls@0BZk}R0jAN?U8b*&1a<5D*}nv+{FTz1;wK%G<ao*DHNqM35mzgp*}2^{Hdr6gJ-Cam&p!Q1jggqZI>$I;autHVUl8Lp&=MIilU-=P{9-zVuGhZUTSyu<h5@+BWK|@@OQ4T6L|CW*P5DDb`1}9^Bqxj$Q%o-KampvR}Fj}uF$Ek-FD>hP9oCU#wijbxko!jIaV$edL@h3<d2&nPFxf7hWE;ZZ5kE>jIbcOAvZ@FOF&BmCDhu}%A<Iw{InFx+2kUPlcaI2_5pIu;rf-T;45f`c}!J;1$~?nMir&Q=nIrwYJ`D6PbG=t1{aV(X$`T())}}nlqRwc*w=$KBe_!0(+Xx$!azv|_{-JkOJl}Sd(ekaucG<ps9$xf@iAScUe?<M%F_JiWdy!DPe7@e2}sOC#H08uZX|Z_`n;k_k{m9O&sY$JXJ+q7e?pi*oCLablgRA0Ke)`bENe0BqwyS+o9MyvDw$a$#XAh%eO$iBU6jj>byk0oW6Yo~oY`(Kk|?^wJ7vE@*x{c*{7=WW`3lWq+%pR9asJ0A#fzdiVT6%RfHWcSWk8-7sU%*lOc#|AK}`tm+)S6VH6aE}#vRy5>7hlxLIP?|ErtY)+QQ1XQ1yr4OoO~y$>}F_7ORzu48}%Te|mBYa3G<1Fs4Pru9EM~qE!{#*$!_KqYV&Nj|4;H1^U!(K58D#C9Wqpg~&u#*=IFC!!86N6Y*_vaXD=u4(G)xg>b_24=9yZAEYYMr^W(p0qIXExvUzZ>|$v|0s^uxGUSW~h{SItJr}VSMxdmGv)s3uA<)Pb1QH;9b!1jLh8Z}ErBX{b#Ku?(PG^@R5G}qcT#A`?g%t3hk!4nEfI{IEGw6-OBWxEf=Efm~2gi)r)i9$fq5^?D6r)i?%dOdnMN85Ih%wi(=Yz9vc2rAeZW5vlA_b$(m_l43U7L;?8V$77<9DmDFC7nlBT*DW0i?%bZ)GGGX5W+$W84z*4snD*7MA7UlFX)aPj&cWHIGvdR*R^^YHZ^Na6KTx><H&<LeHJ^!7r?{P8JN?opKPIr2v)}mBG^nIpKP%!pO6!gXp|mZAB&@n&p6|#|Q{>dxz-Irb<JY6@hPx6~=AjsvZWvs5*l$wat51;rVJRc(0Uen_ga3#1ndCjGz$;=2v0@T54Ds3EXLZAV8atyik6qbfVG|%+GVTT)K2)DU3b~&@V{flR~H|0@kFN!Of+?H$`lE;3a6Tls}=^J+LJ`T`9Hqz+q|L`3_rAjf2>O(L3d_q5{Cb*G-SNAkPFYc2S55{@KM;YGN&!46NZ^bTfJomY*#`876U)Mhg7wkYXgNEIN|ME~BCef#?R!39Nvom5q!cPtv>plW8Nt>D-P2O-?)Qv}U9L9+!)**qX7lKEztof%6L33ZhW!kxMNvjL2(SOP7fk_YnEqf+RgyhXXv7qZNKBM?#*1y7>^?L`=sjFH)<Wrpt%pbv9bc{oH@21}w$eABYn$rky9N>qtZw0qt(d2z*`{^hy8Ci)WIh%}+)s^<hbOLR+8)o<%C1Xt&#DSa?ziaauqGLm<%2vF9Na%KNY2dB3~D5JJmi6Tspo$0&*oSF8}h@;9dz&=AI!D%TKT{+hQuhV5zKLQ|oPEGObJQJut-EhE_0Bgw^eLru07%S;|jeGGe23|6fR6??_cZ7ElgPOfTXe3hNfQC4bakajRMn_uK1x~v({jx4CcQb8*vCv%6l(>Fp2t>{ulZL}!lsI4W&uQ)UWyToZx-P>4()roj5d~Gh4!vct9+K0VY!t*hURi(%iqzI+?fslUR!6;#IoMK~G9fHkE);*p<YyYzRm~a)5<S906RQJ>71(XA+W8w$R>mfTbGNx(-Zo~Phr^KxeIqRWUKmchhaEYp=Y$=mZ1-i=BdiXX*!+PB$McLeuAh8Jnm@2f3-x0Fm4X6CFAi?+WsVtchs8C$;Td!C7d61X_e+9iH<T?wduf%96$Jr3|iBODS-KaTqqnmxK7q{hz1PLl=kBk`!H{WgHBO?YL6xf)}VUR8ZMNkkDz-<cTucv6w3&KU#rN*VhSGo){PyKo5qROIR*1bl#Yhe9%Vy!uR<9c5RQF5^xiRULmZr^%E<i(@TgB9N++Cuf)JP&lc0!1QN+mI^QWMA%vM96Z*!ZujQj;F<AndU-z)5$y%`!^YVenlnD2IV&)V|899%mdFo#U>735bxC^Vo;0gaiu|RYLPn=_e3jf!pt`(l@aP}*j=OOFfbHR>P|u&<q*!Ye2&*0!suIr(k8I_r9z0vYzV@=!!lyxItjY;vQ_%`=uQAWN?W%qFr@e0PXEGgm#m?L6v#p5S(rU<yp}B*v;Yk4&|Ol2kMwl0+c3bNJFvn1$io@~%g5oCO`dgL<<P-y2CI9z%;3(L9d_5?(+jZyePWHjI3&@{`cVjKbhR(cx~@ZFcK@`ign>|Od_1PzxZ>%0$AH2mpt>WsW*46`CcLF5Z3O;|V8eulk|>>?G5)f1&p{mrZK0j&H6r4L7N0(2tLjkL&5l*TO`S`6twYUIlT<=q$~iQUx}r10TA(Jh5ew3Il>(ohL=*BOj@PuGG=!`@<f5;^7#<4qki^$7XHvU1hqiOFsp82DHEH2bE02eA^`NqWdYEx&;gW+Lsgn<C_n#09!X!G8o)`787Wy7{K+jCAOh5oUHUo5Dy{l(L_)Y`Y!)^|Q+eE1hEDf&AJamrqNcCu%=(-CmG^}+m%^tllcZN2aF3=)uX@VN6Yzh)mO1Z%iI=~bvor5@1>ZDsj1i_QIO$5x@uzwy_`elGgV$<E=agjbRtf5V651tCeSz{3!G7W7<Tl%17K{j2056{A;d0>E1XzPi1G(Db4m12`rIc-GYiHJ61LlCmJp9q^qCf5W8QX<o^60?ZaVCsWAuq@AF(rJuHc3;sGNs&qPV<KyY^>4@nEQyRE@o*CLRd$SBf{_?k7g}vHXLxQ&C7db;(j?G?EKj#4DgkPT!7@i0eX8(hB4zl{>@WoIF0+eqenN1I7NC1(_YU=I)Qka}(OUClgDcu%bm7v2XgA26Sz7~XTYrB2=IeCm8XE+FPYEByfKfb&s=+a>%;RORvzattOL%1uI<@6S`*mnG&FK>WufPeWI9El)lejyTQcu~d;~;W2Q@aL7MZPfk82Ei0s#8K$MmwUskQP+tWjA!7qqix&1GlcQK^b$dMz*v~yRak{NjWeY0{QaRUjns9Cqa{S0KOBNcPL#1Qco4)7iG;UfJ$D}`wzp}DT6>so0})5=lC3)MTy$v1Q@$F`OF^f6E5incu>8;$--kHS4gc-SKL&ypB(d8*HZ{aeMjMg+z;eW*+J<6MW+Q8538*b%vctGlBPJ5`w-cO#Z2_YV`O!jbm{2P(y1aOBI4b<zZ^b>4Fh3Qmy^|6eK;s=iOX1+H!VRxeWvU{)_@8C=R$M0PS|3C#h$0Vja)kO60Iu#uN)DK<A9xUfYFR_2}4k5D9I4Dmq!n&-p&DyM{qAdkW8}_8rpIDsrpTI2pfhc(RsO<rl)aI5v?9TF_<J^9wU_k9P;oLQCR|(3tR3SoFrv!eI`PPqti%AhDeI`K`SCOn3G<+)WgiOFq;w-pthvR>Rwl4i&TmK0Bi>VcM2zw=xpX~!nN!2Rx<53?+zyBLgNr1EeVTfn;V}-#UEcPD$4v!OyS-H#W=v{$2*jOuq^)v#V7mhuJqX|st^N%_H`+J_`S(Enk!6u+k9#)9jbaJad9#nb{8fyiKCOk<?9chOvf9od}nmMX%cnNs_M%tvH<5vIXW_<g&F*%c>1ig9k7h{jpxipXI7-$EZx4QMzz@x&~odtL7ssFR3zZd1J`pOX=iOyldd<NaxtM_DC1*B#~V`e$QmJG8Ra}3rdle%BaATQLbJF4#pFrsTlV$sqz1KtOU_4y>?DrxM7$Rya+%~8yJgWYZ2RLuPn2y3qA$h$W0y;;cmQa2xt1~#h-Rq<%Sz}zf~3)6nv|~7auV(*<{C88nS_Bv(aBa<T<Bx*{7fe0XkDnjh9Z!Xo{;u+dBaA%RY?S(Zs0EwFdj8SZNgsi)}YN`$6cmIbkG`!kdgFY)y2sK5S$wHwLADr_kOB~wNPwdS3>Q;TrMk^%RSog$0NjCqK6Qjx!ed!iySipZE;vII6CoZpUg{<l#tkoW;UzEzt-w}J!|Z29p$;io`Ly?@%yEi#^bSc`=C&*JM)gDy^Vkv1)4IPXJ8Hy!v**W&ELw6m_cPA7g5E5WBro3dLkvzMiUeTr_q3<;G{Ff*twS?@o))EyVC;$K6SQ*Ix-BdO6dG2lbT<CGGYW}5JHf4iU?|0cj8%w#4l+j;U{^;_SIB1h&x!m)s5b#+{2PM;|B=S2?|?u?x!I_wDpCm+0&azDM&ini~fKL(FwgJgG3nl%k7#XQBXrJlTYaHd}>{SO(3e*)SH$#lRywVD2@RQ9Fd_oHtaCrMoVBCl+YAMF100a7l7lJyhmZlNRFVFQyZXg_j1cf+F3zG=WD!5Pe>$*^uELuRBVAb>e$6T!pD+5&=Wr1f)Vu#<>rX&pu*56cBYZY%yAjMTrI<f2s5vKX&(^=;xCuua(0O@zbn0k4O$^EDR1O*Pbhjuu1Zu|ZL$iGpnYr==kpA{igSAngI{c>1c{Uy^cBxHsTXzu4T@EyPgR&iX%WYSLXP3Iq&FboZ8?klvzoLd{!Siu%Y1B*7x_==q2wKI-P~T?=fS{OwlrDnkBB68GTN%|sqhj45aHitCvo-(7!pV-0)4pjQ3#bG0bXIgW}CO3qooCumIbj0iA3A<#F43@j0BN4(#iE@3jPKO3ZAWIysmR^H<n<oJ?o>UtRIBPCrGB|>)O$;bD3M6vf+h=sD}&3LK1ojuR_SU;k(P7mNYGg6)cwyeQ~SzCddsCVPvyaf&q)Y*`*0~8fb3;gn^*<g9jbOj_`|0Ib-}jdBGJk7iJ|Iu@!minl6t}<|0lm3C_C39k9axdrJUrnF=$B;3n{>fp3lE0K@}%1);LuMFRFdoapmm?~ExUN=PG<ZLoFn1afYO|3Gvd!fo&;lvkua86!ugG&=Y7e3FzMEPb7Hi{j}pq8d+P0QhV!<P%9c5%EzV40Yzzeoz#<)>_tN^+?hT=lFo&M_gnxvj;|m;pCAJG0-|7+h(vTY~=#9xSPwyQ@L2J$zu(LhxZ5ypp0J;B}gSZ5t$H_+du<xs}+8!Sl4cMOW<5rC_N0Vs3a|mQL}EZd$&FBZa;w99-6;b<#xzRkKqH>WcUAjPBv3Uf+SKFFxtQccw9$iZifHcFPC(iGEKxG0M*!y!G~pqVUg-A4hE7wR1uSNjaArjCQ=<JzV)C?P2=hA3e0)s{2%~GW^jj#ae5pc%2h;parAmv*NNmMIw~cC76Z_;lZqyR(HZ12JE@4gElICp%B8+hr##~>GJpK}x{=BeNLioT06%RQI412|Z&aRu)Jd47+)S!gXUE#`(<WQ9UZr_eWlu{}%C-O5pr$Epc(6vAbVb%Bn|y4%6Uo1Guft+24WGOur?ImoNsrp}DO{N4(|W4SGCXZG<*qDcqFoM3@|ZzZy~aD8AW>+58Ms=nF*{!U%p?x@Vin~8GA-mKhFPnq%*pmMZcifQhps=Zi)H<m(Y%mr)V1YkU^j{uvk-!`sskJ4eskcgYfA+Q+CXyDxS4W?dH)a}0zK~_YT%TYm>Fv)Y$~3X9Z_)XK~`^KjC}BbGe#=_$}!q!iPtv7ssMvo1XRMUh4bLFA20MWqUCI5)*o~P=OK`&Z>JOmr;fQ6K62P=G=wyOerBFsyCOQ9Z3*FbfUi;>IvF0vtZ}?9I0FU;i2zuR$C6Ef=YD8?eM9h#E<p|y4NmQ;Q(N@t7&n_Cx~LfINK)-eI;Z5B7l&FTs%$4FRjRG{$)6_w$cKX9*V)!dL}>Pf>WunQ3DuDFRme%Ts<v2plw%ENx%#TgklLHtub?*u>NDp8tcdi8%7g~3pWKGkb%}PMK-^O<G!*d5lZui?*mnA0dPU_xLGXC3$X2SiCXaKKy(#RU+;!&`)Qa^hygm47O1Q8)CZ<IS09x|!-By4raGjFAWRtB1y;Mhvjy0jEjp0Fi5qv0vTuT5aIU>?Dc$!UesM%icszWeK>S~Wfiw>-{t5!{woT(lyZWc+>#AfkvC=iMMEN`TgfgNoEVw6F<1rACm9gjT4@JQg$IY&S}u#=J0wWRgCt8+syOL`I<n0Dc@pln+5OXqcfP+#-DEG*KLjYJ#wklt?`)N3xf!_e`>B{?Hyv*R$3C=om92e>>wo^8_1j+|^rmU+OD*1lfq1KLf;<c+C<e5D&ZNZOq|_1>NC5`8)@3Th!WuO_Zkt1W3rigDCxO}*v=O=KW}1X+QB<P&qMoTCjB&*%&0BZDptN%>ajwDs@*a%mdm1NLePVO5E9#2FgwgF!S2@fBR`9D=g1Drget&~QR1h!PZ~*L7P>uu?@-VDFG+C^qZ!dg!%Dq3+EsJJ?xmIYG+Z{?%wjX{K;IxpmleMO~e78C37U03oxmo!D1^;2kCIz2Ex@6!o&sC>y8+<5VTsq1Bca1bZTj%pLSB^=?dI80(|M!8<f11U6{lGO}BWF_zreMjr=(fe_?Q6H(w&I3;9r+UImwi+elLu%mx|rk1K^WTX^<X-X=pu5fv2?wgf1<O~r3gwwv?4a~^R6~-)b90{KoaAN?auychkr>_DrK!*kmFC==cgr9rJl?$MF1_(Z7OG_C`Ro^T@c!0RmP6;$0=27VGCD^Z}Gc^w<_vJ`BU|U%5TZFHU$}_v5+vrcuWExVw@Kyq$LfhYgt>Sdo&7ExXs0dZ4Uhy1&7Cb5^joIqzlz!d1hmD5q{=~qw9*R98E-@2f8DF%Oj+g;+9g(;PU2>JG2ST`z6*9n|=2Q%A30>#drjNk6QjWt&ifP(yf2=Ac+e1wy^FrBb;GU}7F)?^3*T@LZMZ$wyU&+&(%$m<B{NuJdqC<hQ3{sU@wFND;W8R+2Phg=z^VTgH0Yy|NrMsRdYRJ}DVnOjdvA_ocn9T<0!CUCx3y_C5qoOjBw(CU+fmW{ygE4kgDHIAwvSUX^N4x!L4UbU`x`=dQGfshL=NKhK4Li^%;KtP<!%9HPV{YUi&^TOQvv$s-E4X6-!Y%@5#-_He!=SIuff@)EQt)@MBy+3<tnlF-vLpyin|6~WF|jk}rn;z*fFY20XDugC?IML`@YK=P5*d$MC^@-_Af#+R;x$leAtfs1m8VNk*cAw2Q?mk8G;mgG-YvY72bIhyK>-s;toC^LAdlu3<J_FfY|31yhXp$ab`<D9S=`eptvO)tdj~@bHKfvYg^}_U)thF`A&s8Sqymg>>am?(WpmT`wZ|?UD*uC8#WXM~q7#RJ_R>Bn)^HNDVF#48#g?(QNn<O~s3Pk&QJTj7@<x!k`EJRDT*OM57ccc53@VF+%>spjB66$2O7Xd$;Wlvt+QvvF2(0^0BF3Ozj#rTOiXCT5HMm1z=RBh_cmNL^9ORPg3Zn#Pi54>0L8>hSrQ|PGFmwrZQ70@+G9t6XAih@dNIXHprpX>bWlYH!IS>nb=>;<_op(JJ=GjkCJI*@^>OiBUVmSdMDVgSlXyqcCO`_W_O9oZwFpU<ulmp=twO*E?x&X=`4j&y4ngq7!OzYBm;HC$)3ewk#w&6U%4uWnjLHxR9UlNIrqoFtf;V~x-ggihijA9x0@<DnpJUk&R8E}!=%he;)f%<51UnUaMtd3L|hPK5fZV$TPcoTm_Lh!7^=6l2%gpX_%llJB*eQ1Xo-B22R8Uv6<SwQSTfqJGR`q$OCnJ-(*bVOdZLVqCt!QvrG^Rpa@M;ZDu6QN4_JSpL@>&iHhGM@t-urigEyP2HNB!5$KjZ}q6*|ayboqv`}Cnr?N&fFs%ERayFhOTIc&Gxk`)rwWWunCljoIaDe-TWd^&s}6BIG+hhP?Pr1k<gQN>6b945ByQ7-7Mjzh^Q3~RRDK0N)qvTs+=+`-s1w2ae-JSzgP)dXqgyb4y+DrpFLaWPrki*d;48{`T%rnA3lb`+lQyj+vf3tp=}>OW;LIITknUbTT1Y=Knk9^&J?G!fuhe~VF@mg9yDoj%?$GAu)eFZpAfM}(+Z;c?SFkPYf3l}2)bg0H|_iIK8s~t1g%i->aFqEf#vgE<ANgq7Fq3(3$c8@>rXKgprDb4Az%Gm78Z0kNXj7MLV6A0()i|cSz?xs27>A#g>8o4A9qoI`hQn!foc')))
_DEMO_IMPL = make_agent({0: _DEMO_TAPE})
def agent(obs, config=None):
    return _DEMO_IMPL(obs, config)
agent.telemetry = _DEMO_IMPL.chassis.diagnostics
